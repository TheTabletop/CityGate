import os
import uuid
import mimetypes

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json
import msgpack

class AllHeros(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_get (self, req, resp):
		result = self.heros.find()

		resp.data = msgpack.packb(json.dumps(result))
		resp.status = falcon.HTTP_200

class AllGuilds(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.guilds = self.db.guilds

	def on_get (self, req, resp):
		result = self.guilds.find()

		resp.data = msgpack.packb(json.dumps(result))
		resp.status = falcon.HTTP_200
