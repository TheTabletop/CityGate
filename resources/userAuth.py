import os
import uuid
import mimetypes
import datetime

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json
import resources.util

class Login(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.emails = self.db.emails
		self.heros = self.db.heros
		self.userAuth = self.db.userAuth
		#ignore create index issue for now as we will be switching to redis
		#self.userAuth.create_index({"expires": 1}, {'expireAfterSeconds': 0})

	def on_post(self, req, resp):
		params = req.json

		email = params.get('email')
		key = params.get('key')
		if email is None or key is None:
			resp.data = str.encode(json.dumps({'error': 'Must provided both hero email address and account key'}))
			resp.status = falcon.HTTP_400
			return

		emailHeroObject = self.emails.find_one({'_id': email})
		if emailHeroObject is None:
			resp.data = str.encode(json.dumps({'error': 'Bad email and key pair'}))
			resp.status = falcon.HTTP_406

		heroKey = self.heros.find_one({'_id': ObjectId(emailHeroObject.get('uhid'))}, projection = ['key'])
		if heroKey is None:
			resp.data = str.encode(json.dumps({'error': 'Issue locating hero, server side problem'}))
			resp.status = falcon.HTTP_500
			return

		if util.RfgKeyEncrypt(key) != heroKey.get('key'):
			resp.data = str.encode(json.dumps({'error': 'Bad email and key pair'}))
			resp.status = falcon.HTTP_406

		result = self.userAuth.insert_one(
			{
				"uhid": req.get_param('uhid'),
				"expires": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
			 })
		resp.data = str.encode(json.dumps({'usid': result.inserted_id, 'uhid': emailHeroObject.get('uhid')}))
		resp.status = falcon.HTTP_202

class updateExpire(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.userAuth = self.db.userAuth

	def incrementExpire(self, usid):
		self.userAuth.update_one(
			{'_id': ObjectId(usid)},
			{'$set': {"expires": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}}
		)

class checkuhid(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.userAuth = self.db.userAuth

	def checkid(self, currUserID, sessionID):
		result = self.userAuth.find_one({'_id': ObjectId(sessionID)},projection=['uhid'])
		return currUserID==result.get('uhid')

class Tokens(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.userAuth = self.db.userAuth

	def TokenExists(self, req, resp):
		token = req.parmas_get('session_token')
		result = self.userAuth.find_one({'_id': ObjectId(token)})
		if result is None:
			msg = 'Invalid session token!'
			raise falcon.HTTPBadRequest('Bad request', msg)

	def HeroMatchesToken(self, req, resp, uhid):
		result = self.userAuth.find_one({'_id': ObjectId(req.params_get('session_token'))})
		if "{}".format(result.get('uhid')) != uhid:
			msg = 'Session token not associated with appropriate hero'
			raise falcon.HTTPBadRequest('Bad request', msg)
