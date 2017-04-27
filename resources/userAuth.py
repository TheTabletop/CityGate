import os
import uuid
import mimetypes
import datetime

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json
import msgpack

class Login(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.userAuth = self.db.userAuth
		#ignore create index issue for now as we will be switching to redis
		#self.userAuth.create_index({"expires": 1}, {'expireAfterSeconds': 0})

	def on_post(self, req, resp):
		result = self.userAuth.insert_one(
			{
				"uhid": req.get_param('uhid'),
				"expires": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
			 })
		resp.data=msgpack.packb(json.dumps({'sessionID': result.inserted_id}))
		resp.status = falcon.HTTP_201

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_404

class updateExpire(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.userAuth = self.db.userAuth

	def incrementExpire(self):
		self.userAuth.update_one(
			{
				"expires": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
			}
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
