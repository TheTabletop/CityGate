import os
import uuid
import mimetypes

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json
import msgpack
import datetime

class Coop(object)
    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.coops = self.db.pigeoncoops

    def create(self, uhid):
        coopObject = self.coops.insert_one({
            '_id': uhid,
            'pigeons': [],
            'unseen_count': 0
        })
        return coopObject.inserted_id

    def on_get(self, resp, req, ucid):
        coop = self.coops.find_one({'_id': ObjectId(ucid)})

        resp.data = msgpack.packb(json.dumps(coop))
        resp.status = falcon.HTTP_200

	def increase_count(self, ucid):
		self.coops.update_one({'_id': ObjectId(ucid)}, {"$inc": {"unseen_count": 1}})

	def decrease_count(self, ucid):
		self.coops.update_one({'_id': ObjectId(ucid)}, {"$inc": {"unseen_count": -1}})

#Needs the uhid in the req object
class globalPigeonWaiting(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.coops = self.db.pigeoncoops

	def on_get(self, req, resp, ucid):
		num = self.coops.find_one({"_id": ObjectId(ucid)}, projection=['unread_messages'])

		if num is None:
			resp.data = msgpack.packb({"Failed": "Unable to get number of unread messages"})
			resp.status = falcon.HTTP_500
		else:
			resp.data = msgpack.packb({"unread_messages": num.get('unread_messages')})
			resp.status = falcon.HTTP_202

class killPigeon(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.coops = self.db.pigeoncoops

	def on_post(self, req, resp):
		coopId = self.db.heros.find_one({"_id": ObjectId(req.params_get('uhid'))}, projection=['ucid'])
		#remove pigeon from coop
		result = self.coops.update_one({"_id":coopId.get("_id")}, {'$pull':{'pigeons':{'upid':{ObjectId(req.params_get('upid'))}}}})
		if result.modified_count != 1:
			resp.data = msgpack.packb({"Failed": "Unable to remove pigeon from coop"})
			resp.status = falcon.HTTP_500
		#remove things from the pigeon itself
		result2 = self.db.pigeons.update_one({"_id":ObjectId(req.params_get('upid'))}, {'$pull':{'recipents':ObjectId(req.params_get('uhid'))}})
		if result2.modified_count != 1:
			resp.data = msgpack.packb({"Failed": "Unable to remove hero from pigeon recipent list"})
			resp.status = falcon.HTTP_500

		result3 = self.db.pigeons.update_one({"_id":ObjectId(req.params_get('upid'))}, {'$pull':{'has_not_seen':ObjectId(req.params_get('uhid'))}})
		if result3.matched_count == 0 and result3.modified_count == 0:
			resp.data = msgpack.packb({"Failed": "Unable to remove hero from pigeon recipent list"})
			resp.status = falcon.HTTP_500
		else:
			resp.data = msgpack.packb({"Success": "Successfully removed pigeon"})
			resp.status = falcon.HTTP_202

class Pigeons(object):
    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.coops = self.db.pigeoncoops

    def on_get(self, resp, req, ucid):
        coop = self.coops.find_one({'_id': ObjectId(ucid)}, projection=['pigeons'])

        resp.data = msgpack.packb(json.dumps({'pigeons': coop.get('pigeons')}))
        resp.status = falcon.HTTP_200

    def add_pigeon(self, ucid, upid, seen):
        self.coops.update_one({'_id': ObjectId(ucid)}, {'$push': {'pigeons': {'upid': ObjectId(upid), 'last_update': datetime.datetime.utcnow(), 'seen': seen}}})

    def remove_pigeon(self, ucid, upid):
        self.coops.update_one({'_id': ObjectId(ucid)}, {'$pull': {'pigeons': {'upid': ObjectId(upid)}}})

class Owner(object):
    def on_get(self, req, resp, ucid):
        resp.data = msgpack.packb(json.dumps({"uhid": ucid}))
        resp.status = falcon.HTTP_200

class UnseenCount(object):
    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.coops = self.db.pigeoncoops

    def on_get(self, req, resp, ucid):
        coop = self.coops.find_one({'_id': ObjectId(ucid)}, projection=['unseen_count'])

        resp.data = msgpack.packb(json.dumps({'unseen_count': coop.get('unseen_count')}))
        resp.status = falcon.HTTP_200
