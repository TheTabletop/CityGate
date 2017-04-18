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
				"location": "",
				"games": [],
				"members": [],
				"future_sessions": [],
				"previous_sessions": [],
				"hero_requests": [],
				"invited_heros": []
			})

		resp.data = msgpack.packb({"Info": "Successfully created a new hero with id: {}".format(result)})
		resp.status = falcon.HTTP_201

	#Do we want to do anything with this?
	def on_get(self, req, resp):
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

class Name(object):
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
	def __init__(self, db_reference):
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

#TODO: SESSSION STUFFS

class Location(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['location'])

		resp.data = msgpack.packb(result.get('location'))
		resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		result = self.guilds.update_one({'_id': ObjectId(ugid)}, {'$inc': {'location': req.params_get('location')}})

		if result.match_count == 0:
			resp.data = msgpack.packb({"Error": "Guild not found"})
			resp.status = falcon.HTTP_404
		elif result.modified_count == 0:
			resp.data = msgpack.packb({"Error": "Unable to update guild location"})
			resp.status = falcon.HTTP_500
		else:
			resp.data = msgpack.packb("Successfully updated guild location")
			resp.status = falcon.HTTP_202

class Games(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['games'])

		resp.data = msgpack.pack(result.get('games'))
		resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		result = self.guilds.update_one({'_id': ObjectId(ugid)}, {'$push': {'games': req.get_param('games')}})

		resp.data = msgpack.pack({'Success': "Added %s to guild games list".fomrat(req.get_param('games'))})
		resp.status = falcon.HTTP_202

	def on_delete(self, req, resp, ugid):
		result = self.guilds.update_one({'_id': ObjectId(ugid)}, {'$push': {'games': req.get_param('games')}})

		resp.data = msgpack.pack({'Success': "Deleted %s from guild games list".fomrat(req.get_param('games'))})
		resp.status = falcon.HTTP_202

class Members(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['members'])

		if result is None:
			resp.data = msgpack.packb({"Failure": "Guild not found"})
			resp.status = falcon.HTTP_404
		else:
			#TODO serialize ObjectId data
			resp.data = msgpack.packb({"game": result.get('nsgame'), "time": result.get('nstime'), "location": result.get('location')})
			resp.status = falcon.HTTP_200

	#TODO make sure user deleting another user has access
	def on_delete(self, req, resp, ugid):
		pass

class RequestToJoinGuild(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, resp, req, ugid, uhid):
		self.heros.update_one({'_id': ObjectId(uhid)}, {'$push': {'requested_guilds': ObjectId(ugid)}})
		self.guilds.update_one({'_id': ObjectId(ugid)}, {'$push': {'hero_requests': ObjectId(uhid)}})

		resp.data = msgpack.packb({'Success': 'Invited user'})
		resp.status = falcon.HTTP_202

	def on_delete(self, resp, req, ugid, uhid):
		self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'requested_guilds': ObjectId(ugid)}})
		self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'hero_requests': ObjectId(uhid)}})

		resp.data = msgpack.packb({'Success': 'Uninvited user'})
		resp.status = falcon.HTTP_202

class RespondToHeroRequest(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, resp, req, ugid, uhid):
		dec = req.params_get('decision')
		if not (decision == 'Accept' or decision == 'Decline'):
			resp.data = msgpack.packb({"Error": "Must provide decision param as either 'Accept' or 'Decline'"})
			resp.status = falcon.HTTP_400
		else:
			if decision == "Decline":
				self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}})
				self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}})
				resp.data = msgpack.packb({"Success": "Acknowledged decline of invite"})
			elif decision == 'Accept':
				self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}, '$push': {'membsers': ObjectId(uhid)}})
				self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}, '$push': {'guilds': ObjectId(ugid)}})
				resp.data = msgpack.packb({"Success": "Acknowledged acceptance of inivte"})
			resp.status = falcon.HTTP_202

class InviteHeroToJoin(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, resp, req, ugid, uhid):
		self.heros.update_one({'_id': ObjectId(uhid)}, {'$push': {'guild_invites': ObjectId(ugid)}})
		self.guilds.update_one({'_id': ObjectId(ugid)}, {'$push': {'invited_heros': ObjectId(uhid)}})

		resp.data = msgpack.packb({'Success': 'Invited user'})
		resp.status = falcon.HTTP_202

	def on_delete(self, resp, req, ugid, uhid):
		self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}})
		self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}})

		resp.data = msgpack.packb({'Success': 'Uninvited user'})
		resp.status = falcon.HTTP_202

class RespondToGuildInvite(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, resp, req, ugid, uhid):
		dec = req.params_get('decision')
		if not (decision == 'Accept' or decision == 'Decline'):
			resp.data = msgpack.packb({"Error": "Must provide decision param as either 'Accept' or 'Decline'"})
			resp.status = falcon.HTTP_400
		else:
			if decision == "Decline":
				self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}})
				self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}})
				resp.data = msgpack.packb({"Success": "Acknowledged decline of invite"})
			elif decision == 'Accept':
				self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}, '$push': {'membsers': ObjectId(uhid)}})
				self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}, '$push': {'guilds': ObjectId(ugid)}})
				resp.data = msgpack.packb({"Success": "Acknowledged acceptance of inivte"})
			resp.status = falcon.HTTP_202

class LeaveGuild(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, resp, req, ugid, uhid):
		gRemove = self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'members': {'uhid': ObjectId(uhid)}}})
		hRemove = self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild': {'ugid': ObjectId(ugid)}}})
		message = {}
		gSuccess = 0
		hSuccess = 0

		if gRemove.match_count == 0:
			message['Error_gRemove'] = "Hero is not member of guild."
			gSuccess = 1
		elif gRemove.modified_count == 0:
			message['Error_gRemove'] = "Could not remove hero from guild"
			gSuccess = 3
		elif gRemove.modified_count == 1:
			message['Success_gRemove'] = "Hero removed from guild"
			gSuccess = 5
		else:
			message['Error_gRemove'] == "Unexpected issue occured..."

		if hRemove.match_count == 0:
			message['Error_gRemove'] = "Hero is not member of guild."
			hSuccess = 1
		elif hRemove.modified_count == 0:
			message['Error_gRemove'] = "Could not remove hero's associated guild"
			hSuccess = 3
		elif hRemove.modified_count == 1:
			message['Success_hRemove'] = "Hero removed from guild"
			hSuccess = 5
		else:
			message['Error_gRemove'] == "Unexpected issue occured..."

		resp.date = msgpack.packb(message)

		#TODO We might want to run extra stuff in cases where sum is between 1-8
		if hSuccess + gSuccess == 10:
			resp.status = falcon.HTTP_202
		elif hSuccess + gSuccess == 8:
			resp.status = falcon.HTTP_500
		elif hSuccess + gSuccess == 6:
			resp.status = falcon.HTTP_726
		elif hSuccess + gSuccess == 5:
			resp.status = falcon.HTTP_726
		elif hSuccess + gSuccess == 4:
			resp.status = falcon.HTTP_726
		elif hSuccess + gSuccess == 3:
			resp.status = falcon.HTTP_726
		elif hSuccess + gSuccess == 2:
			resp.status = falcon.HTTP_726
		elif hSuccess + gSuccess == 1:
			resp.status = falcon.HTTP_726
		else:
			resp.status = falcon.HTTP_400

class Requests(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=["hero_requests"])
		resp.data = msgpack.packb(json.dumps({"hero_requests": result.get("hero_requests")}))
		resp.status = falcon.HTTP_200

class Invites(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=["invited_heros"])
		resp.data = msgpack.packb(json.dumps({"invited_heros": result.get("invited_heros")}))
		resp.status = falcon.HTTP_200
