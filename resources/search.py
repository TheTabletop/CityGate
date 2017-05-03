import os
import uuid
import mimetypes
import random

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json

class AllHeros(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.heros = self.db.heros

	def on_get (self, req, resp):
		result = self.heros.find()
		heros = []
		distance = 0.0
		random.seed(1337)

		for i in range(0, result.count()):
			temp = {}
			temp['uhid'] = str(result[i].get('_id'))
			temp['playername'] = result[i].get('playername')
			temp['heroname'] = result[i].get('heroname')
			temp['games'] = result[i].get('games')
			heros.append(temp)
			distance += (random.randint(0,1) * i) + random.random()
			temp['distance'] = distance

		resp.data = str.encode(json.dumps(heros))
		resp.status = falcon.HTTP_200

class AllGuilds(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds
		self.heros = self.db.heros

	def on_get (self, req, resp):
		result = self.guilds.find()
		guilds = []
		distance = 0.0
		random.seed(1337)

		for i in range(0, result.count()):
			temp = {}
			temp['ugid'] = str(result[i].get('uhid'))
			temp['name'] = result[i].get('name')
			temp['games'] = result[i].get('games')

			members = result[i].get('members')
			temp['members'] = []
			for member in members:
				uhid = member.get('uhid')
				hero = self.heros.find_one({'_id': ObjectId(uhid)})
				if hero is not None:
					temp['members'].append({'uhid': uhid, 'playername': hero.get('playername'), 'heroname': hero.get('heroname')})
			distance += (random.randint(0,1) * i) + random.random()
			temp['distance'] = distance
			guilds.append(temp)

		resp.data = str.encode(json.dumps(guilds))
		resp.status = falcon.HTTP_200
