import os
import uuid
import mimetypes

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json
import datetime

class Coop(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.coops = self.db.pigeoncoops

	def create(self, uhid):
		coopObject = self.coops.insert_one({
			'_id': ObjectId(uhid),
			'pigeons': [],
			'unseen_count': 0
		})
		return str(coopObject.inserted_id)

	def on_get(self, req, resp, ucid):
		#TODO take out objectids before return
		coop = self.coops.find_one({'_id': ObjectId(ucid)})

		resp.data = str.encode((json.dumps(coop)))
		resp.status = falcon.HTTP_200

	def increase_count(self, ucid):
		self.coops.update_one({'_id': ObjectId(ucid)}, {"$inc": {"unseen_count": 1}})

	def decrease_count(self, ucid):
		self.coops.update_one({'_id': ObjectId(ucid)}, {"$inc": {"unseen_count": -1}})

class Pigeons(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.coops = self.db.pigeoncoops

	def on_get(self, req, resp, upid):
		coop = self.coops.find_one({'_id': ObjectId(ucid)}, projection=['pigeons'])

		if coop is None:
			resp.data = str.encode(json.dumps({'error': 'Unable to find specified coop'}))
			resp.status = falcon.HTTP_410

		resp.data = str.encode(json.dumps({'pigeons': coop.get('pigeons')}))
		resp.status = falcon.HTTP_200

	def add_pigeon(self, ucid, upid, seen):
		self.coops.update_one({'_id': ObjectId(ucid)}, {'$push': {'pigeons': {'upid': ObjectId(upid), 'last_update': datetime.datetime.utcnow(), 'seen': seen}}})

	def remove_pigeon(self, ucid, upid):
		result = self.coops.find_one_and_update({'_id': ObjectId(ucid)}, {"$pull": {"pigeons": {"upid": ObjectId(upid)}}})
		for pigeon in result.get("pigeons"):
			if "{}".format(pigeon.get("upid")) == upid and not pigeon.get("seen"):
				self.coops.update_one({'_id': ObjectId(ucid)}, {'$inc': {"unseen_count": -1}})

class Owner(object):
	def on_get(self, req, resp, ucid):
		resp.data = str.encode(json.dumps({"uhid": ucid}))
		resp.status = falcon.HTTP_200

class UnseenCount(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.coops = self.db.pigeoncoops

	def on_get(self, req, resp, ucid):
		result = self.coops.find_one({'_id': ObjectId(ucid)}, projection=['unseen_count'])

		if result is None:
			resp.data = str.encode(json.dumps({"error": "Unable to find specified coop"}))
			resp.status = falcon.HTTP_410
			return

		resp.data = str.encode(json.dumps({"unread_messages": num.get('unseen_count')}))
		resp.status = falcon.HTTP_202
