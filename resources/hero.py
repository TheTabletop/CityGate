import os
import uuid
import mimetypes

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json
import msgpack

#ALLOWED_IMAGE_TYPES = (
#    'image/gif',
#    'image/jpeg',
#    'image/png',
#)

#def validate_image_type(req, resp, resource, params):
#	if req.content_type not in ALLOWED_IMAGE_TYPES:
#		msg = 'Image type not allowed, Must be PNG, JPEG, or GIF'
#		raise falcon.HTTPBadRequest('Bad request', msg)

class NewHero(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_post(self, req, resp):
		result = self.heros.insert_one(
			{
				"email": req.get_param('email'),
				"playername": req.get_param('playername'),
				"heroname" : req.get_param('heroname'),
				"games": req.get_param('games'),
				"key": req.get_param('key'),
				"companions": [],
				"guild_invites": [],
				"requested_guilds": []
			})

		resp.data = msgpack.packb({"Info": "Successfully created a new hero with id: {}".format(result)})
		resp.status = falcon.HTTP_201

	#Do we want to do anything with this?
	def on_get(self, req, resp, something_else):
		resp.status = falcon.HTTP_404

class Hero(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	# For updating a hero's Info
	# Can only edit hero info for hero id of session token
	def on_post(self, req, resp, uhid):
		pass #TODO

	# Get a hero by unique hero id (uhid)
	# Must have an active user session token
	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)})

		if result.count() == 0:
			resp.data = msgpack.packb({"Error": "We could not find that hero, they must have nat 20'd  their stealth check"})
			resp.status = falcon.HTTP_404
		elif result.count() == 1:
			hero = result
			for k, v in hero.items():
				if type(hero[k]) is ObjectId:
					temp = "{}".format(v)
					hero[k] = temp
			resp.data = msgpack.packb(json.dumps(hero))
			resp.status = falcon.HTTP_200
		else:
			resp.data = msgpack.packb({"Error": "Somehow there is hero identity theft, damn rogues..."})
			resp.status = falcon.HTTP_724

class PlayerName(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		result = self.heros.update_one({'_id': ObjectId(uhid)}, {'$inc': {'playername': req.params_get('playername')}})

		if result.modified_count == 1:
			resp.data = msgpack.packb({"Success": "Successfully changed hero's player name"})
			resp.status = falcon.HTTP_202
		else:
			resp.data = msgpack.packb({"Failed": "Unable to update hero's player name"})
			resp.status = falcon.HTTP_500

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['playername'])

		if result is None:
			resp.data = msgpack.packb({"Failure": "Hero not found"})
			resp.status = falcon.HTTP_404
		else:
			pName = result.get('playername')
			resp.data = msgpack.packb({"playername": pName})
			resp.status = falcon.HTTP_200

class HeroName(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		result = self.heros.update_one({'_id': ObjectId(uhid)}, {'$inc': {'heroname': req.params_get('heroname')}})

		if result.modified_count == 1:
			resp.data = msgpack.packb({"Success": "Successfully changed hero's name"})
			resp.status = falcon.HTTP_202
		else:
			resp.data = msgpack.packb({"Failed": "Unable to update hero's name"})
			resp.status = falcon.HTTP_500

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['heroname'])

		if result is None:
			resp.data = msgpack.packb({"Failure": "Hero not found"})
			resp.status = falcon.HTTP_404
		else:
			hName = result.get('heroname')
			resp.data = msgpack.packb({"heroname": hName})
			resp.status = falcon.HTTP_200

class HeroEmail(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		result = self.heros.update_one({'_id': ObjectId(uhid)}, {'$inc': {'email': req.params_get('email')}})

		if result.modified_count == 1:
			resp.data = msgpack.packb({"Success": "Successfully changed hero's email"})
			resp.status = falcon.HTTP_202
		else:
			resp.data = msgpack.packb({"Failed": "Unable to update hero's email"})
			resp.status = falcon.HTTP_500

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['email'])

		if result is None:
			resp.data = msgpack.packb({"Failure": "Hero not found"})
			resp.status = falcon.HTTP_404
		else:
			email = result.get('heroname')
			resp.data = msgpack.packb({"email": email})
			resp.status = falcon.HTTP_200

class Companions(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		result = self.heros.update_one({'_id': ObjectId(uhid)}, {'$push': {'companions': ObjectId(req.params_get('companion'))}})

		if result.modified_count == 1:
			resp.data = msgpack.packb({"Success": "Successfully added companion"})
			resp.status = falcon.HTTP_202
		else:
			resp.data = msgpack.packb({"Failed": "Unable to add companion"})
			resp.status = falcon.HTTP_500

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['companions'])

		if result is None:
			resp.data = msgpack.packb({"Failure": "Hero not found"})
			resp.status = falcon.HTTP_404
		else:
			companions = result.get('companions')
			for k, v in companions.items():
				companions[k] = "{}".format(v)
			resp.data = msgpack.packb({"companions": companions})
			resp.status = falcon.HTTP_200

class Key(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['key'])
		if result[key] == hashlib.sha224(req.get_param('oldkey')).hexdigest():
			result = self.heros.update_one({'_id': ObjectId(uhid)}, {'$inc': {'key': hashlib.sha224(req.get_param('newkey').hexdigest())}})
			if result.modified_count == 1:
				resp.data = msgpack.packb({"Success": "Successfully added companion"})
				resp.status = falcon.HTTP_202
			else:
				resp.data = msgpack.packb({"Failed": "Unable to update key"})
				resp.status = falcon.HTTP_500
		else:
			resp.data = msgpack.packb({"Failed": "Incorrect account key for authorization"})
			resp.status = falcon.HTTP_400


	def on_get(self, req, resp, uhid):
		resp.data = msgpack.pack({"Message": "Yea right, like we'd allow that."})
		resp.status = falcon.HTTP_740

class ForgeKey(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros
		self.forgeCommissions = self.db.forgeCommissions

	def on_post(self, req, resp, uiid):
		forgeToken = self.forgeCommissions.find_one({"_id": ObjectId(uiid)})
		if forgeToken is None:
			pass
		else:
			uhid = forgeToken.get('uhid')
			result = self.heros.update_one({'_id': ObjectId(uhid)}, {'$inc': {'key': hashlib.sha224(req.get_param('newkey').hexdigest())}})
			if result.modified_count == 1:
				resp.data = msgpack.packb({"Success": "Successfully updated key"})
				resp.status = falcon.HTTP_202
				self.forgeCommissions.delete_one({"_id": ObjectId(uiid)})
			else:
				resp.data = msgpack.packb({"Failed": "Unable to update key"})
				resp.status = falcon.HTTP_500

	def on_get(self, req, resp, uiid):
		resp.data = msgpack.pack({"Message": "Yea right, like we'd allow that."})
		resp.status = falcon.HTTP_740

class CommissionKey(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros
		self.forgeCommissions = self.db.forgeCommissions

	def on_post(self, req, resp):
		email = req.params_get('email')
		user = self.heros.find_one({'email': email}, projection=['_id'])

		#TODO
		# Implement sending an e-mail to specified e-mail address
		# If e-mail does not exist, send an e-mail that states it's not registered
		# If e-mail exists, send e-mail with a link in the form:
		# http://www.rollforguild.com/forgekey/<uiid>
		# where uiid is the id for the commission, that way the front end
		# know's what commission request to use
		if user is None:
			pass #TODO E-mail that email isn't registered with us
		else:
			self.forgeCommissions.remove({'user': user})
			result = self.forgeCommissions.insert_one({'user': user})
			uiid = "{}".format(result['inserted_id'])
			#TODO email link

	def on_get(self, req, resp):
		resp.data = msgpack.packb({"Message": "This is not a route that is allowed"})
		resp.status = falcon.HTTP_405
