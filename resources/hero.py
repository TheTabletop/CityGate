import os
import uuid
import mimetypes

from pymongo import MongoClient
from pymongo import ReturnDocument
from bson import ObjectId

import falcon
import json

import resources.pigeoncoop as pcoop
import resources.util as util

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
		self.heros = self.db.heros
		self.emails = self.db.emails
		self.coop = pcoop.Coop(db_reference)

	def on_post(self, req, resp):
		params = req.json

		email = params.get('email')
		playername = params.get('playername')
		heroname = params.get('heroname')
		backstory = params.get('backstory')
		key = params.get('key')
		games = params.get('games')
		location = params.get('location')
		address = params.get('location')

		if email is None:
			resp.data = str.encode(json.dumps({'error': 'The email param is required'}))
			resp.status = falcon.HTTP_400
			return
		if playername is None:
			resp.data = str.encode(json.dumps({'error': 'The playername param is required'}))
			resp.status = falcon.HTTP_400
			return
		if heroname is None:
			resp.data = str.encode(json.dumps({'error': 'The heroname param is required'}))
			resp.status = falcon.HTTP_400
			return
		if key is None:
			resp.data = str.encode(json.dumps({'error': 'The key param is required'}))
			resp.status = falcon.HTTP_400
			return
		if games is None:
			games = []
		if backstory is None:
			backstory = ""

		try:
			self.emails.insert_one({'_id': email, 'uhid': None})
		except Exception as e:
			resp.data = str.encode(json.dumps({'error': 'Hero with %s alread exists'.format(email)}))
			resp.status = falcon.HTTP_409
			return
		heroObject = self.heros.insert_one(
			{
				"email": email,
				"playername": playername,
				"heroname": heroname,
				"games": games,
				"guilds": [],
				"backstory": backstory,
				"key": util.RfgKeyEncrypt(key),
				"companions": [],
				"guild_invites": [],
				"requested_guilds": [],
				"requested_companions": [],
				"companion_requests": [],
				"ucid": None,
				"location": "",
				"address": "",
			})
		uhid = str(heroObject.inserted_id)
		self.emails.update_one({'_id': email}, {'$set': {'uhid': uhid}})
		self.heros.update_one({'_id': heroObject.inserted_id}, {'$set': {'ucid': str(self.coop.create(heroObject.inserted_id))}})
		resp.data = str.encode(json.dumps({"success": "Created a hero.", "uhid": str(heroObject.inserted_id)}))
		resp.status = falcon.HTTP_201

class Hero(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	# For updating a hero's Info
	# Can only edit hero info for hero id of session token
	def on_post(self, req, resp, uhid):
		params = req.json

		email = params.get('email')
		playername = params.get('playername')
		heroname = params.get('heroname')
		backstory = params.get('backstory')
		games = params.get('games')
		location = params.get('location')
		address = params.get('location')
		myDict = {}

		if email is not None:
			if myDict.get('$set') is None:
				myDict['$set'] = {}
			myDict['$set']['email'] = email
		if playername is not None:
			if myDict.get('$set') is None:
				myDict['$set'] = {}
			myDict['$set']['playername'] = playername
		if heroname is not None:
			if myDict.get('$set') is None:
				myDict['$set'] = {}
			myDict['$set']['heroname'] = heroname
		if backstory is not None:
			if myDict.get('$set') is None:
				myDict['$set'] = {}
			myDict['$set']['backstory'] = backstory
		if location is not None:
			if myDict.get('$set') is None:
				myDict['$set'] = {}
			myDict['$set']['location'] = location
		if address is not None:
			if myDict.get('$set') is None:
				myDict['$set'] = {}
			myDict['$set']['address'] = address
		if games is not None:
			if myDict.get('$push') is None:
				myDict['$push'] = {}
			myDict['$push']['games'] = {'$each': games}

		result = self.heros.find_one_and_update({'_id': ObjectId(uhid)}, myDict, return_document=ReturnDocument.AFTER)

		data = {
			'uhid': str(result.get('_id')),
			'email': result.get('email'),
			'playername': result.get('playername'),
			'heroname': result.get('heroname'),
			'games': result.get('games'),
			'backstory': result.get('backstory'),
			"companions": result.get('companions'),
			"guild_invites": result.get('guild_invites'),
			"requested_guilds": result.get('requested_guilds'),
			"requested_companions": result.get('requested_companions'),
			"companion_requests": result.get('companion_requests'),
			"ucid": result.get('ucid'),
			"location": result.get('location'),
			"address": result.get('address'),
			'guilds': result.get('guilds')
		}
		resp.data = str.encode(json.dumps(data))
		resp.status = falcon.HTTP_202

	# Get a hero by unique hero id (uhid)
	# Must have an active user session token
	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)})

		if result is None:
			resp.data = str.encode(json.dumps({'error': 'Could not find hero with uhid'}))
			resp.status = falcon.HTTP_405
			returns

		data = {
			'uhid': str(result.get('_id')),
			'email': result.get('email'),
			'playername': result.get('playername'),
			'heroname': result.get('heroname'),
			'games': result.get('games'),
			'backstory': result.get('backstory'),
			"companions": result.get('companions'),
			"guild_invites": result.get('guild_invites'),
			"requested_guilds": result.get('requested_guilds'),
			"requested_companions": result.get('requested_companions'),
			"companion_requests": result.get('companion_requests'),
			"ucid": result.get('ucid'),
			"location": result.get('location'),
			"address": result.get('address'),
			'guilds': result.get('guilds')
		}

		resp.data = str.encode(json.dumps(data))
		resp.status = falcon.HTTP_200

class PlayerName(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		params = req.json

		pname = params.get('playername')
		if pname is None:
			resp.data = str.encode(json.dumps({'error': 'no playername key in json provided'}))
			resp.status = falcon.HTTP_400
			return

		result = self.heros.find_one_and_update({'_id': ObjectId(uhid)}, {'$set': {'playername': pname}}, return_document=ReturnDocument.AFTER)

		if result is not None:
			resp.data = str.encode(json.dumps({"uhid": str(result.get('_id')), 'playername': result.get('playername')}))
			resp.status = falcon.HTTP_202
		else:
			resp.data = str.encode(json.dumps({"error": "Was unable to update hero's player name"}))
			resp.status = falcon.HTTP_500

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['playername'])

		if result is None:
			resp.data = srt.encode(json.dumps({"error": "Hero not found"}))
			resp.status = falcon.HTTP_404
		else:
			pname = result.get('playername')
			resp.data = str.encode(json.dumps({"uhid": str(result.get('_id')), "playername": pname}))
			resp.status = falcon.HTTP_200

class HeroName(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		params = req.json

		hname = params.get('heroname')
		if hname is None:
			resp.data = str.encode(json.dumps({'error': 'no heroname key in json provided'}))
			resp.status = falcon.HTTP_400
			return

		result = self.heros.find_one_and_update({'_id': ObjectId(uhid)}, {'$set': {'heroname': hname}}, return_document=ReturnDocument.AFTER)

		if result is not None:
			resp.data = str.encode(json.dumps({'uhid': str(result.get('_id')), 'heroname': result.get('heroname')}))
			resp.status = falcon.HTTP_202
		else:
			resp.data = str.encode(json.dumps({"error": "Was unable to update hero's name"}))
			resp.status = falcon.HTTP_500

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['heroname'])

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Hero not found"}))
			resp.status = falcon.HTTP_404
		else:
			hname = result.get('heroname')
			resp.data = str.encode(json.dumps({'uhid': str(result.get('_id')), "heroname": hname}))
			resp.status = falcon.HTTP_200

class Email(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros
		self.emails = self.db.emails

	def on_post(self, req, resp, uhid):
		params = req.json

		#check to make sure they provided a new email
		newemail = params.get('email')
		if newemail is None:
			resp.data = str.encode(json.dumps({'error': 'no email key in json provided'}))
			resp.status = falcon.HTTP_400
			return

		#make sure the hero of the uhid exists
		heroObject = self.heros.find_one({'_id': ObjectId(uhid)}, projection = ['email'])
		if heroObject is None:
			resp.data = str.encode(json.dumps({'error': 'Invalid hero id, was not found'}))
			resp.status = falcon.HTTP_410
		oldemail = heroObject.get('email')

		#try and insert the new email into the email Collection
		#if it already exists, it will throw an exception
		try:
			self.emails.insert_one({'_id': newemail, 'uhid': uhid})
		except:
			resp.data = str.encode(json.dumps({'error': 'Emails already belongs to another hero.'}))
			resp.status = falcon.HTTP_409

		#update the hero with the new email
		updatedHeroObject = self.heros.find_one_and_update({'_id': ObjectId(uhid)}, {'$set': {'email': email}}, return_document=ReturnDocument.AFTER)

		if result is not None:
			#remove the old email from the email Collection
			self.emails.delete_one({'_id': oldemail})

			resp.data = str.encode(json.dumps({'uhid': str(updatedHeroObject.get('_id')), 'email': updatedHeroObject.get('email')}))
			resp.status = falcon.HTTP_202
		else:
			resp.data = str.encode(json.dumps({"error": "Was unable to update hero's email"}))
			resp.status = falcon.HTTP_500

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['email'])

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Hero not found"}))
			resp.status = falcon.HTTP_404
		else:
			email = result.get('email')
			resp.data = str.encode(json.dumps({'uhid': result.get('_id'), "email": email}))
			resp.status = falcon.HTTP_200

class Guilds(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros
		self.guilds = self.db.guilds

	def on_get(self, req, resp):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['guilds'])

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Hero not found"}))
			resp.status = falcon.HTTP_410
			return

		data = []
		guilds = result.get('guilds')
		for guild in guilds:
			gObj = self.guilds.find_one({'_id': ObjectId(temp['ugid'])}, projection=['guildname'])
			if guild is not None:
				temp = {}
				temp['ugid'] = guild.get('ugid')
				temp['admin'] = guild.get('admin')
				temp['guildname'] = gObj.get('guildname')
				data.append(temp)

		resp.data = str.encode(json.dumps({'uhid': str(result.get('_id')), 'guilds': data}))
		resp.status = falcon.HTTP_200

class Companions(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['companions'])

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Hero not found"}))
			resp.status = falcon.HTTP_410
		else:
			companions = result.get('companions')
			data = []
			for companion in companions:
				temp = self.hero.find_one({"_id": ObjectId(companion)}, projection=['playername', 'heroname'])
				if temp is not None:
					data.append({'uhid': companion, 'playername': temp.get('playername'), 'heroname': temp.get('heroname')})

			resp.data = str.encode(json.dumps(data))
			resp.status = falcon.HTTP_200

	def on_delete(self, req, resp, uhid):
		resp.data = str.encode(json.dumps({'error': 'route not yet implemented'}))
		resp.status = falcon.HTTP_500

class Key(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		params = req.json

		oldkey = params.get('oldkey')
		newkey = params.get('newkey')
		if oldkey is None or newkey is None:
			resp.data = str.encode(json.dumps({'error': 'both newkey and old key are required as data from req'}))
			resp.status = falcon.HTTP_400
			return
		result = self.heros.find_one({"_id": ObjectId(uhid)}, projection=['key'])
		if result.get("key") == util.RfgKeyEncrypt(oldkey):
			result = self.heros.update_one({'_id': ObjectId(uhid)}, {'$set': {'key': util.RfgKeyEncrypt(newkey)}})
			if result.modified_count == 1:
				resp.data = str.encode(json.dumps({"success": "Successfully updated hero's key"}))
				resp.status = falcon.HTTP_202
			else:
				resp.data = str.encode(json.dumps({"error": "Unable to update key"}))
				resp.status = falcon.HTTP_500
		else:
			resp.data = str.encode(json.dumps({"error": "Incorrect account key for authorization"}))
			resp.status = falcon.HTTP_400

	def on_get(self, req, resp, uhid):
		resp.data = str.encode(json.dumps({"error": "Yea right, like we'd allow that."}))
		resp.status = falcon.HTTP_740

class ForgeKey(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros
		self.forgeCommissions = self.db.forgeCommissions

	def on_post(self, req, resp, uiid):
		params = req.json

		newkey = params.get('newkey')
		if newkey is None:
			resp.data = str.encode(json.dumps({'error': 'both newkey is required as data from req'}))
			resp.status = falcon.HTTP_400
			return

		forgeToken = self.forgeCommissions.find_one({"_id": ObjectId(uiid)})
		if forgeToken is None:
			resp.data = str.encode(json.dumps({'error': 'forge token does not exist'}))
			resp.status = falcon.HTTP_400
			return
		else:
			uhid = forgeToken.get('uhid')
			result = self.heros.update_one({'_id': ObjectId(uhid)}, {'$set': {'key': util.RfgKeyEncrypt(newkey)}})
			if result.modified_count == 1:
				resp.data = str.encode(json.dumps({"success": "Successfully forged a new key"}))
				resp.status = falcon.HTTP_202
				self.forgeCommissions.delete_one({"_id": ObjectId(uiid)})
			else:
				resp.data = str.encode(json.dumps({"error": "Unable to update key"}))
				resp.status = falcon.HTTP_500

	def on_get(self, req, resp, uiid):
		resp.data = str.encode(json.dumps({"error": "Yea right, like we'd allow that."}))
		resp.status = falcon.HTTP_740

class CommissionKey(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros
		self.forgeCommissions = self.db.forgeCommissions

	def on_post(self, req, resp):
		params = req.json

		email = params.get('email')
		if email is None:
			resp.data = str.encode(json.dumps({'error': 'email is required as data from req'}))
			resp.status = falcon.HTTP_400
			return
		user = self.heros.find_one({'email': email}, projection=['_id'])

		#TODO
		# Implement sending an e-mail to specified e-mail address
		# If e-mail does not exist, send an e-mail that states it's not registered
		# If e-mail exists, send e-mail with a link in the form:
		# http://www.rollforguild.com/forgekey/<uiid>
		# where uiid is the id for the commission, that way the front end
		# know's what commission request to use
		if user is None:
			#we fake whether or not the email exists because we don't want to give away information
			resp.data = str.encode(json.dumps({'success': 'an email has been sent'}))
			resp.status = falcon.HTTP_202
			return
		else:
			self.forgeCommissions.remove({'user': user})
			result = self.forgeCommissions.insert_one({'user': user})
			uiid = str(result.get('inserted_id'))
			resp.data = str.encode(json.dumps({'success': 'an email has been sent'}))
			resp.status = falcon.HTTP_202
			#TODO email link

	def on_get(self, req, resp):
		resp.data = str.encode(json.dumps({"error": "This is not a route that is allowed"}))
		resp.status = falcon.HTTP_405

class Requests(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({'_id': ObjectId(uhid)}, projection=["requested_guilds"])
		if result is None:
			resp.data = str.encode(json.dumps({'error': 'Unable to locate hero'}))
			resp.status = falcon.HTTP_404
		resp.data = str.encode(json.dumps({"uhid": result.get('_id'), "requested_guilds": resp.get('requested_guilds')}))
		resp.status = falcon.HTTP_200

class Invites(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({'_id': ObjectId(uhid)}, projection=["guild_invites"])
		if result is None:
			resp.data = str.encode(json.dumps({'error': 'Unable to locate hero'}))
			resp.status = falcon.HTTP_404
		resp.data = str.encode(json.dumps({"uhid": result.get('_id'), "guild_invites": resp.get('guild_invites')}))
		resp.status = falcon.HTTP_200

class CompanionRequest(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		params = req.json

		requestee = params.get('requestee')
		if email is None:
			resp.data = str.encode(json.dumps({'error': 'requestee is required as data from req'}))
			resp.status = falcon.HTTP_400
			return

		result = self.heros.update_one({'_id': ObjectId(requestee)}, {'$push': {'companion_requests': uhid}})

		if result.matcheds_count == 0:
			resp.json = {"error": "Hero not found"}
			resp.status = falcon.HTTP_410
		elif result.modified_count == 0:
			resp.json = {"error": "Could not get on hero's companion requests list"}
			resp.status = falcon.HTTP_500
		else:
			result = self.heros.find_one_and_update({'_id': ObjectId(uhid)}, {'$push': {'requested_companions': requestee}}, return_document=ReturnDocument.AFTER)
			resp.data = str.encode(json.dumps({"uhid": result.get('_id'), "requested_companions": result.get('requested_companions')}))
			resp.status = falcon.HTTP_202

	def on_delete(self, req, resp, uhid):
		params = req.json

		requestee = params.get('requestee')
		if email is None:
			resp.data = str.encode(json.dumps({'error': 'requestee is required as data from req'}))
			resp.status = falcon.HTTP_400
			return
		r1 = self.heros.update_one({'_id': requestee}, {'$pull': {'companion_requests': uhid}})
		r2 = self.heros.find_one_and_update({'_id': uhid}, {'$pull': {'requested_companions': requestee}}, return_document=ReturnDocument.AFTER)

		if r1.matched_count == 0:
			resp.data = str.encode(json.dumps({'error': 'Could not locate specified hero', 'requested_companions': r2.get('requested_companions')}))
			resp.status = falcon.HTTP_410
		else:
			resp.data = str.encode(json.dumps({'uhid': r2.get('_id'), 'requested_companions': r2.get('requested_companions')}))
			resp.stats = falcon.HTTP_202

class CompanionRequestResponse(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_post(self, req, resp, uhid):
		params = req.json

		requester = params.get('requestee')
		accept = params.get('accept')
		if requester is None or accept is None:
			resp.data = str.encode(json.dumps({'error': 'requester and accept are both required as data from req'}))
			resp.status = falcon.HTTP_400
			return
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
			resp.data = str.encode(json.dumps({'uhid': final_r.get('uhid'), "companions": final_r.get("companions"), "companion_requests": final_r.get("companion_requests")}))
			resp.status = falon.HTTP_200
		elif r1.matched_count + r2.matched_count < 2:
			resp.data = str.encode(json.dumps({"error": "Could not find requester"}))
			resp.status = falcon.HTTP_410
		else:
			resp.data = str.encode(json.dumps({"error": "Invalid companion request"}))
			resp.status = falcon.HTTP_740


class CompanionRequests(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_get(self, req, resp, uhid):
		result = self.heros.find_one({'_id': ObjectId(uhid)}, projection=["companion_requests", "requested_companions"])
		resp.data = str.encode(json.dumps({'companion_requests': result.get('companion_requests'), 'requested_companions': result.get('requested_companions')}))
		resp.status = falcon.HTTP_200
