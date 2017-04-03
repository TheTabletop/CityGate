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

class FormGuild(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_post(self, req, resp):
		result = self.guilds.insert_one(
			{
				"guildname": req.get_param('guildname'),
				"charter": req.get_param('charter'),
				"nstime": "",
				"nsgame": "",
				"location": "",
				"last session": "",
				"games": [],
				"members": []
			})

		resp.data = msgpack.packb({"Info": "Successfully created a new hero with id: {}".format(result)})
		resp.status = falcon.HTTP_201

	#Do we want to do anything with this?
	def on_get(self, req, resp, something_else):
		resp.status = falcon.HTTP_404

class Guild(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find({"_id": ObjectId(ugid)})

		if result.count() == 0:
			resp.data = msgpack.packb({"Error": "We could not find that guild, maybe they disbanded?"})
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
			resp.data = msgpack.packb({"Error": "Somehow there is are multiple guilds claiming to be this guild, damn thieves guilds"})
			resp.status = falcon.HTTP_724

	def on_post(self, req, resp, ugid):
		pass

class GuildName(object)
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['guildname'])

		if result is None:
			resp.data = msgpack.packb({"Failure": "Guild not found"})
			resp.status = falcon.HTTP_404
		else:
			gName = result.get('guildname')
			resp.data = msgpack.packb({"guildname": gName})
			resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		result = self.guilds.update_one({'_id': ObjectId(ugid)}, {'$inc': {'guildname': req.params_get('guildname')}})

		if result.modified_count == 1:
			resp.data = msgpack.packb({"Success": "Successfully changed guild's name"})
			resp.status = falcon.HTTP_202
		else:
			resp.data = msgpack.packb({"Failed": "Unable to update guild's name"})
			resp.status = falcon.HTTP_500

class Charter(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guild

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=["charter"])

		if result is None:
			resp.data = msgpack.packb({"Failure": "Guild not found"})
			resp.status = falcon.HTTP_404
		else:
			charter = result.get('charter')
			resp.data = msgpack.packb({"charter": charter})
			resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		result = self.guilds.update_one({'_id': ObjectId(ugid)}, {'$inc': {'charter': charter}})

		if result.modified_count == 1:
			resp.data = msgpack.packb({"Success": "Successfully updated guild's charter"})
			resp.status = falcon.HTTP_202
		else:
			resp.data = msgpack.packb({"Failed": "Unable to update guild's charter"})
			resp.status = falcon.HTTP_500

class Session(object):
	def __init__(object, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': objectId(ugid)}, projection=['nstime', 'nsgame', 'location'])

		if result is None:
			resp.data = msgpack.packb({"Failure": "Guild not found"})
			resp.status = falcon.HTTP_404
		else:
			resp.data = msgpack.packb({"game": result.get('nsgame'), "time": result.get('nstime'), "location": result.get('location')})
			resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		result = self.guilds.update_one({'_id': ObjectId(ugid)}, {'$inc': {'nsgame': req.params_get('game'), 'nstime': req.params_get('time'), 'location': req.params_get('location')}})

		if result.modified_count == 1:
			resp.data = msgpack.packb({"Success": "Successfully updated guild's next session"})
			resp.status = falcon.HTTP_202
		else:
			resp.data = msgpack.packb({"Failed": "Unable to update guild's next session"})
			resp.status = falcon.HTTP_500

class Nstime(object):
	def __init__(object, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

class Nsgame(object):
	def __init__(object, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

class Location(object):
	def __init__(object, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

class Games(object):
	def __init__(object, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

class Memebers(object):
	def __init__(object, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds
