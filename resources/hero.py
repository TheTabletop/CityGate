import os
import uuid
import mimetypes

from pymongo import MongoClient
from pymongo import ReturnDocument
from bson import ObjectId

import falcon
import json
import msgpack
import hashlib

import resources.pigeoncoop as pcoop

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
		params = json.loads(req.stream.read().decode("utf-8") )
		heroObject = self.heros.insert_one(
			{
				"email": params.get('email'),
				"playername": params.get('playername'),
				"heroname" : params.get('heroname'),
				"games": params.get('games'),
				"backstory": params.get('backstory'),
				"key": hashlib.sha224(params.get('key').encode('utf-8')).hexdigest(),
				"companions": [],
				"guild_invites": [],
				"requested_guilds": [],
				"requested_companions": [],
				"companion_requests": [],
				"ucid": None,
				"upcoming_sessions": []
			})
		self.heros.update_one({'_id': heroObject}, {'$set': {'ucid': pcoop.Coop.Create(heroObject.inserted_id).inserted_id}})
		resp.data = msgpack.packb({"uhid": "{}".format(heroObject.inserted_id)})
		resp.status = falcon.HTTP_201

	#Do we want to do anything with this?
	def on_get(self, req, resp):
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

class Email(object):
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
		if result.get("key") == hashlib.sha224(req.get_param('oldkey')).hexdigest():
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

class Requests(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({'_id': ObjectId(uhid)}, projection=["requested_guilds"])
		resp.data = msgpack.packb(json.dumps({"requested_guilds": resp.get('requested_guilds')}))
		resp.status = falcon.HTTP_200

class Invites(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({'_id': ObjectId(uhid)}, projection=["guild_invites"])
		resp.data = msgpack.packb(json.dumps({"guild_invites": resp.get('guild_invites')}))
		resp.status = falcon.HTTP_200

class CompanionRequest(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		requestee = req.get_json('requestee', dtype=str)
		result = self.heros.update_one({'_id': ObjectId(requestee)}, {'$push': {'companion_requests': uhid}})

		if result.matcheds_count == 0:
			resp.json = {"error": "Hero not found"}
			resp.status = falcon.HTTP_410
		elif result.modified_count == 0:
			resp.json = {"error": "Could not get on hero's companion requests list"}
			resp.status = falcon.HTTP_500
		else:
			result = self.heros.find_one_and_update({'_id': ObjectId(uhid)}, {'$push': {'requested_companions': requestee}}, return_document=ReturnDocument.AFTER)
			resp.json = {"requested_companions": result.get('requested_companions')}
			resp.status = falcon.HTTP_202

	def on_delete(self, req, resp, uhid):
		requestee = req.get_json('requestee', dtype=str)
		r1 = self.heros.update_one({'_id': requestee}, {'$pull': {'companion_requests': uhid}})
		r2 = self.heros.find_one_and_update({'_id': uhid}, {'$pull': {'requested_companions': requestee}}, return_document=ReturnDocument.AFTER)

		if r1.matched_count == 0:
			resp.json = {'error': 'Could not locate specified hero', 'requested_companions': r2.get('requested_companions')}
			resp.status = falcon.HTTP_410
		else:
			resp.json = {'requested_companions': r2.get('requested_companions')}
			resp.stats = falcon.HTTP_202

class CompanionRequestResponse(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		accept = req.get_json('decision', dtype=bool)
		requester = req.get_json('requester', dtype=str)
		r1 = None
		r2 = None
		if accept:
			r1 = self.heros.update_one({'_id': ObjectId(requester)}, {'$pull': {'requested_companions': uhid}, '$push': {'companions': uhid}})
			r2 = self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'companion_requests': requester}, '$push': {'companions': requester}})
		else:
			r1 = self.heros.update_one({'_id': ObjectId(requester)}, {'$pull': {'requested_companions': uhid}})
			r2 = self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'companion_requests': requester}})

		final_r = self.heros.find_one({'_id': ObjectId(uhid)}, project=["companions", "companion_requests"])

		if r1.matched_count + r2.matched_count == 2 and r1.modified_count + r2.modified_count >= 1:
			resp.json = {"result": "Success!", "companions": final_r.get("companions"), "companion_requests": final_r.get("companion_requests")}
			resp.status = falon.HTTP_200
		elif r1.matched_count + r2.matched_count < 2:
			resp.json = {"error": "Could not find requester"}
			resp.status = falcon.HTTP_410
		else:
			resp.json = {"error": "Invalid companion request"}
			resp.status = falcon.HTTP_740


class CompanionRequests(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({'_id': ObjectId(uhid)}, projection=["companion_requests", "requested_companions"])
		resp.json = {'companion_requests': result.get('companion_requests'), 'requested_companions': result.get('requested_companions')}
		resp.status = falcon.HTTP_200
