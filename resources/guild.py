import os
import uuid
import mimetypes

from pymongo import MongoClient
from pymongo import ReturnDocument
from bson import ObjectId

import falcon
import json

import resources.session
import resources.util

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
		self.guilds = self.db.guilds

	def on_post(self, req, resp):
		params = req.json

		guildname = params.get('guildname')
		charter = params.get('charter')
		address = params.get('address')
		coord = params.get('coord')
		games = params.get('games')
		creator = params.get('creator')

		if guildname is None or guildname =="":
			resp.data = str.encode(json.dumps({'error': 'The guild must have a guildname'}))
			resp.status = falcon.HTTP_400
			return
		if charter is None or charter == "":
			resp.data = str.encode(json.dumps({'error': 'Please provide a charter, a brief description of the guild'}))
			resp.status = falcon.HTTP_400
			return
		if games is None or len(games) == 0:
			resp.data = str.encode(json.dumps({'error': 'Please provide at least one game that the guild plays'}))
			resp.status = falcon.HTTP_400
			return
		if address is None:
			address = ""
		if coord is None:
			coord = ""
		if creator is None or creator == "":
			resp.data = str.encode(json.dumps({'error': ''}))
			resp.status = falcon.HTTP_400
			return

		result = self.guilds.insert_one(
			{
				"guildname": guildname,
				"charter": charter,
				"address": address,
				"coord": coord,
				"games": games,
				"members": [{'uhid': creator, 'admin': True}],
				"future_sessions": [],
				"previous_sessions": [],
				"hero_requests": [],
				"invited_heros": []
			})

		resp.data = str.encode(json.dumps({"success": "Successfully formed new guild", 'ugid': str(result.inserted_id)}))
		resp.status = falcon.HTTP_201

class Guild(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({"_id": ObjectId(ugid)})

		if result is None:
			resp.data = str.encode(json.dumps({"error": "We could not find that guild, maybe they disbanded?"}))
			resp.status = falcon.HTTP_404
			return
		else:
			resp.data = str.encode(json.dumps({
				'ugid': str(result.get('_id')),
				'guildname': result.get('guildname'),
				'charter': result.get('charter'),
				'address': result.get('address'),
				'games': result.get('games'),
				'members': result.get('members'),
				'future_sessions': result.get('future_sessions'),
				'previous_sessions': result.get('previous_sessions')
			}))
			resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		params = req.json

		guildname = params.get('guildname')
		charter = params.get('charter')
		address = params.get('address')
		coord = params.get('coord')
		games = params.get('games')
		creator = params.get('creator')
		myDict = {}

		if guildname is not None and guildname != "":
			if myDict.get('$set') is None:
				myDict['$set'] = {}
			myDict['$set']['guildname'] = guildname
		if charter is not None and charter != "":
			if myDict.get('$set') is None:
				myDict['$set'] = {}
			myDict['$set']['charter'] = charter
		if games is not None and len(games) != 0:
			if myDict.get('$push') is None:
				myDict['$push'] = {}
		if address is not None and address != "":
			if myDict.get('$set') is None:
				myDict['$set'] = {}
		if coord is not None and coord != "":
			if myDict.get('$set') is None:
				myDict['$set'] = {}

class Name(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['guildname'])

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Unable to find specified guild"}))
			resp.status = falcon.HTTP_410
			return

		resp.data = str.encode(json.dumps({'uhid': str(result.get('_id')), 'guildname': result.get('guildname')}))
		resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		params = req.json

		guildname = params.get('guildname')
		if guildname is None or len(guildname) == 0:
			resp.data = str.encode(json.dumps({'error': 'Must provide a guildname with this route'}))
			resp.status = falcon.HTTP_400
			return

		result = self.guilds.find_one_and_update({'_id': ObjectId(ugid)}, {'$set': {'guildname': guildname}}, return_document=ReturnDocument.AFTER)

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Unable to update guild's name"}))
			resp.status = falcon.HTTP_500
			return

		resp.data = str.encode(json.dumps({'ugid': str(result.get('_id')), 'guildname': result.get('guildname')}))
		resp.status = falcon.HTTP_202

class Charter(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guild

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=["charter"])

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Unable to find specified guild"}))
			resp.status = falcon.HTTP_410
			return

		resp.data = str.encode(json.dumps({'uhid': str(result.get('_id')), 'charter': result.get('charter')}))
		resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		params = req.json

		charter = params.get('charter')
		if charter is None or len(charter) == 0:
			resp.data = str.encode(json.dumps({'error': 'Must provide a charter with this route'}))
			resp.status = falcon.HTTP_400
			return

		result = self.guilds.find_one_and_update({'_id': ObjectId(ugid)}, {'$set': {'charter': charter}}, return_document=ReturnDocument.AFTER)

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Unable to update guild's charter"}))
			resp.status = falcon.HTTP_500
			return

		resp.data = str.encode(json.dumps({'ugid': str(result.get('_id')), 'charter': result.get('charter')}))
		resp.status = falcon.HTTP_202

class Location(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=["address"])

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Unable to find specified guild"}))
			resp.status = falcon.HTTP_410
			return

		resp.data = str.encode(json.dumps({'uhid': str(result.get('_id')), 'address': result.get('address')}))
		resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		params = req.json

		address = params.get('address')
		coord = params.get('coord')
		if address is None or len(address) == 0:
			resp.data = str.encode(json.dumps({'error': 'Must provide a address with this route'}))
			resp.status = falcon.HTTP_400
			return
		if coord is None or len(coord) == 0:
			resp.data = str.encode(json.dumps({'error': 'Must provide a coord with this route'}))
			resp.status = falcon.HTTP_400
			return

		result = self.guilds.find_one_and_update({'_id': ObjectId(ugid)}, {'$set': {'address': address, 'coord': coord}}, return_document=ReturnDocument.AFTER)

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Unable to update guild's location."}))
			resp.status = falcon.HTTP_500
			return

		resp.data = str.encode(json.dumps({'ugid': str(result.get('_id')), 'address': result.get('address')}))
		resp.status = falcon.HTTP_202

class Games(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['games'])

		if result is None:
			resp.data = str.encode(json.dumps({'error': 'Unable to find specified guild.'}))
			resp.status = falcon.HTTP_410
			return

		resp.data = str.encode(json.dumps({'ugid': str(result.get('_id')), 'games': result.get('games')}))
		resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ugid):
		params = req.json

		add = params.get('addgames')
		remove = params.get('removegames')
		myDict = {}

		if add is not None:
			myDict['$push'] = {'games': {'$each': add}}
		if remove is not None:
			myDict['$pull'] = {'games': {'$each': remove}}

		result = self.guilds.find_one_and_update({'_id': ObjectId(ugid)}, myDict, return_document=ReturnDocument.AFTER)

		if result is None:
			resp.data = str.encode(json.dumps({'error': 'Unable to update guild\'s game list'}))
			resp.status = falcon.HTTP_500
			return

		resp.data = str.encode(json.dumps({'ugid': str(result.get('_id')), 'games': result.get('games')}))
		resp.status = falcon.HTTP_202

	#Deprecated
	def on_delete(self, req, resp, ugid):
		result = self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'games': {'$each': req.get_param('games')}}})

		resp.data = str.encode(json.dumps({'success': "Removed games from guild's list"}))
		resp.status = falcon.HTTP_202

class Members(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['members'])

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Unable to find specified guild."}))
			resp.status = falcon.HTTP_410

		party = []
		for member in result.get('members'):
			hero = self.heros.find_one({'_id': ObjectId(member.get('uhid'))}, projection = ['heroname', 'playername'])
			party.append({'uhid': member.get('uhid'), 'admin': member.get('admin'), 'heroname': hero.get('heroname'), 'playername': hero.get('playername')})

		resp.data = str.encode(json.dumps({'ugid': str(result.get('_id')), 'members': party}))
		resp.status = falcon.HTTP_200

	#TODO make sure user deleting another user has access
	def on_delete(self, req, resp, ugid):
		params = req.json

		hero = params.get('uhid')
		if hero is None or len(hero) == 0:
			resp.data = str.encode(json.dumps({'error': 'Must provide the uhid of a member to remove'}))
			resp.status = falcon.HTTP_400
			return

		result = self.guild.find_one_and_update({'_id': ObjectId(ugid)}, {'$pull': {'members': {'uhid': hero}}}, return_document=ReturnDocument.AFTER)

		if result is None:
			resp.data = str.encode(json.dumps({'error': 'Unable to remove member from guild'}))
			resp.status = falcon.HTTP_500
			return

		party = []
		for member in result.get('members'):
			hero = self.heros.find_one({'_id': ObjectId(member.get('uhid'))}, projection = ['heroname', 'playername'])
			party.append({'uhid': member.get('uhid'), 'admin': member.get('admin'), 'heroname': hero.get('heroname'), 'playername': hero.get('playername')})

		resp.data = str.encode(json.dumps({'ugid': str(result.get('_id')), 'members': party}))
		resp.status = falcon.HTTP_202

class RequestToJoinGuild(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, req, resp, ugid, uhid):
		self.heros.update_one({'_id': ObjectId(uhid)}, {'$push': {'requested_guilds': ObjectId(ugid)}})
		self.guilds.update_one({'_id': ObjectId(ugid)}, {'$push': {'hero_requests': ObjectId(uhid)}})

		resp.data = str.encode(json.dumps({'success': 'Invited hero.'}))
		resp.status = falcon.HTTP_202

	def on_delete(self, req, resp, ugid, uhid):
		self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'requested_guilds': ObjectId(ugid)}})
		self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'hero_requests': ObjectId(uhid)}})

		resp.data = str.encode(json.dumps({'success': 'Uninvited hero.'}))
		resp.status = falcon.HTTP_202

class RespondToHeroRequest(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, req, resp, ugid, uhid):
		params = req.json

		accept = params.get('accept')

		if accept is None or type(accept) is not bool:
			resp.data = str.encode(json.dumps({"error": "The data value 'accept' must be given as either a true or false value"}))
			resp.status = falcon.HTTP_400
			return

		data = None
		if accept:
			self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}, '$push': {'membsers': ObjectId(uhid)}})
			self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}, '$push': {'guilds': ObjectId(ugid)}})
			data = {"Success": "Acknowledged acceptance of inivte"}
		else:
			self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}})
			self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}})
			data = {"Success": "Acknowledged decline of invite"}

		resp.data = str.encode(json.dumps(data))
		resp.status = falcon.HTTP_202

class InviteHeroToJoin(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, req, resp, ugid, uhid):
		self.heros.update_one({'_id': ObjectId(uhid)}, {'$push': {'guild_invites': ObjectId(ugid)}})
		self.guilds.update_one({'_id': ObjectId(ugid)}, {'$push': {'invited_heros': ObjectId(uhid)}})

		resp.data = str.encode(json.dumps({'success': 'Invited user'}))
		resp.status = falcon.HTTP_202

	def on_delete(self, req, resp, ugid, uhid):
		self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}})
		self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}})

		resp.data = str.encode(json.dumps({'Success': 'Uninvited user'}))
		resp.status = falcon.HTTP_202

class RespondToGuildInvite(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, req, resp, ugid, uhid):
		params = req.json

		accept = params.get('accept')

		if accept is None or type(accept) is not bool:
			resp.data = str.encode(json.dumps({"error": "The data value 'accept' must be given as either a true or false value"}))
			resp.status = falcon.HTTP_400
			return

		data = None
		if accept:
			self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}, '$push': {'membsers': ObjectId(uhid)}})
			self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}, '$push': {'guilds': ObjectId(ugid)}})
			data = {"success": "Acknowledged acceptance of inivte"}
		else:
			self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'invited_heros': ObjectId(uhid)}})
			self.heros.update_one({'_id': ObjectId(uhid)}, {'$pull': {'guild_invites': ObjectId(ugid)}})
			data = {"success": "Acknowledged decline of invite"}

		resp.data = str.encode(json.dumps(data))
		resp.status = falcon.HTTP_202

class LeaveGuild(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_post(self, req, resp, ugid, uhid):
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

		resp.date = str.encode(json.dumps(message))

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
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=["hero_requests"])

		if result is None:
			resp.data = str.encode(json.dumps({'error': 'Unable to find specified guild.'}))
			resp.status = falcon.HTTP_410
			return

		resp.data = str.encode(json.dumps({'ugid': str(result.get('_id')), "hero_requests": result.get("hero_requests")}))
		resp.status = falcon.HTTP_200

class Invites(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=["invited_heros"])

		if result is None:
			resp.data = str.encode(json.dumps({'error': 'Unable to find specified guild.'}))
			resp.status = falcon.HTTP_410
			return

		resp.data = str.encode(json.dumps({'ugid': str(result.get('_id')), "invited_heros": result.get("invited_heros")}))
		resp.status = falcon.HTTP_200

#TODO Garuantee that user is admin of guild
class NewSession(object):
	def __init__(self, db_reference):
		self.session = session.Session(db_reference)

	def on_post(self, req, resp, ugid):
		params = req.json

		game = params.get('game')
		start_string = params.get('start')
		notes = params.get('notes')

		if game is None or game =="":
			resp.data = str.encode(json.dumps({'error': 'Session must have a game'}))
			resp.status = falcon.HTTP_400
			return
		if time is None or time =="":
			resp.data = str.encode(json.dumps({'error': 'Session time must be set with \'start\''}))
			resp.status = falcon.HTTP_400
			return
		if notes is None:
			notes = ""

		start = util.RfgStrptime(when_string)

		if start is not None and when > datetime.datetime.utcnow():
			session_id = self.session.NewSession(start, game, notes, ugid)

			if session_id is None:
				#TODO LOG THIS SHIT
				resp.data = str.encode(json.dumps({"error": "Unable to create session"}))
				resp.status = falcon.HTTP_722
			else:
				result = self.guilds.find_one_and_update({'_id': ObjectId(ugid)}, {"$push": {"future_sessions": {'usid': session_id, 'ts': when}}}, return_document=ReturnDocument.AFTER)

				resp.data = str.encode(json.dumps({"future_sessions": result.get("future_sessions")}))
				resp.status = falcon.HTTP_202
		else:
			resp.data = str.encode(json.dumps({"error": "Invalid ts format for 'when', should be 'DD-MM-YY HH24:MI'"}))
			resp.status = falcon.HTTP_723

#TODO Garuantee that user is admin of guild
class UpdateSession(object):
	def __init__(self, db_reference):
		self.guilds = db_reference.guilds
		self.session = session.Session(db_reference)

	def on_post(self, req, resp, ugid, usid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['future_sessions'])

		found_session = GuildHasSession(ugid, usid, self.guilds, just_future=True)
		if not found_session:
			resp.data = str.encode(json.dump({'error': 'Session not found in guilds sessions'}))
			resp.status = falcon.HTTP_410
			return

		params = req.json

		game = params.get('game')
		start_string = params.get('start')
		notes = params.get('notes')
		start = None

		if game =="":
			game = None
		if string =="":
			None
		else:
			start = util.RfgStrptime(start_string)
			if start is None:
				resp.data = str.encode(json.dumps({'error': 'Improper ts format'}))
				resp.status = falcon.HTTP_400
				return
		if notes =="":
			None

		result = self.session.UpdateSession(game, time, notes, usid)

		if result is None:
			resp.json = {"error": "Unable to update the session"}
			resp.status = falcon.HTTP_500
		else:
			resp.data = str.encode(json.dumps({
				"usid": "{}".format(result.get('_id')),
				"game": result.get('game'),
				"start": result.get('start'),
				"notes": result.get('notes')
			}))
			resp.status = falon.HTTP_202

class Session(object):
	def __init__(self, db_reference):
		self.guilds = db_reference.guilds
		self.session = session.Session(db_reference)

	def on_get(self, req, resp, ugid, usid):
		found_session = GuildHasSession(ugid, usid, self.guilds)

		if found_session:
			session = self.session.GetSession(usid)
			if session is not None:
				resp.data = str.encode(json.dumps({
					'usid': session.get('_id'),
					'game': session.get('game'),
					'start': session.get('start'),
					'notes': session.get('notes')
				}))
				resp.status = falcon.HTTP_200
			else:
				#TODO Log this shit
				resp.data = str.encode(json.dumps({'error': 'Session belongs to guild, but could not be found in database of sessions.'}))
				resp.status = falcon.HTTP_744
		else:
			resp.json =str.encode(json.dumps({'error': 'Session identifier does not belong to guild referenced.'}))
			resp.status = falcon.HTTP_409

	#TODO Garuantee that user is admin of guild
	def on_delete(self, req, resp, ugid, usid):
		found_session = GuildHasSession(ugid, usid, self.guilds)

		if found_session:
			delete_success = self.session.DeleteSession(usid)

			if delete_success:
				resp.data = str.encode(json.dumps({'success': 'Deleted session!'}))
				resp.status = falcon.HTTP_202
			else:
				#TODO Log this shit
				resp.data = str.encode(json.dumps({'error': 'Session belongs to guild, but we were unable to delete it.'}))
				resp.status = falcon.HTTP_744
		else:
			resp.data = str.encode(json.dumps({'error': 'Session identifier does not belong to guild referenced.'}))
			resp.status = falcon.HTTP_409

class Sessions(object):
	def __init__(self, db_reference):
		self.guilds = db_reference.guilds
		self.session = session.Session(db_reference)

	def on_get(self, req, resp, ugid):
		# resp.json = self.session.GetAllGuildSessions(ugid)

		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['future_sessions', 'previous_sessions'])
		fs_mini = reslt.get('future_sessions')
		fs_big = []
		ps_mini = reuslt.get('previous_sessions')
		ps_big = []
		for sesh in fs_mini:
			full_session = self.session.GetSession(sesh.get('usid'))
			if full_session:
				fs_big.append(full_session)
		for sesh in ps_mini:
			full_session = self.session.GetSession(sesh.get('usid'))
			if full_session:
				ps_big.append(full_session)

		resp.data = str.encode(json.dumps({'future_sessions': fs_big, 'previous_sessions': ps_big}))
		resp.status = falcon.HTTP_200

class NextSession(object):
	def __init__(self, db_reference):
		self.guilds = db_reference.guilds
		self.session = session.Session(db_reference)

	def on_get(self, req, resp, ugid):
		result = self.guilds.find_one({'_id': ObjectId(ugid)}, projection=['future_sessions'])
		sessions = sorted(result.get('future_sessions'),  key=lambda x:x['start'])
		while sessions[0]['start'] < datetime.datetime.utcnow():
			session = sessions.pop(0)
			self.guilds.update_one({'_id': ObjectId(ugid)}, {'$pull': {'future_sessions': {'usid': session.usid}}, '$push': {'previous_sessions': session}})

		next_session = self.session.GetSession(sessions[0].get('usid'))

		resp.data = str.encode(json.dumps({
			'usid': str(next_session.get('_id')),
			'game': next_session.get('game'),
			'start': next_session.get('start'),
			'notes': next_session.get('notes')
		}))
		resp.status = falcon.HTTP_200

# If you set both just_future and just_previoust to True, you will automatically get False, don't be stupid.
def GuildHasSession(ugid, usid, guild_col_ref, just_future=False, just_perivious=False):
	result = guild_col_ref.find_one({'_id': ObjectId(ugid)}, projection=['future_sessions', 'previous_sessions'])

	if result:
		if not just_perivious:
			for session in result.get('future_sessions'):
				if usid == session.get('usid'):
					return True
		if not just_future:
			for session in result.get('previous_sessions'):
				if usid == session.get('usid'):
					return True
	return False
