import os
import uuid
import mimetypes

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

		resp.data = str.encode(json.dumps(result))
		resp.status = falcon.HTTP_200

class AllGuilds(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.guilds = self.db.guilds

	def on_get (self, req, resp):
		result = self.guilds.find()

		resp.data = str.encode(json.dumps(result))
		resp.status = falcon.HTTP_200
