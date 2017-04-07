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
        self.pcoops = self.db.pigeoncoops

    def create(self, uhid):
        coopObject = self.pcoops.insert_one({
            '_id': uhid,
            'pigeons': [],
            'unseen_count': 0
        })
        return coopObject.inserted_id

    def on_get(self, resp, req, ucid):
        coop = self.pcoops.find_one({'_id': ObjectId(ucid)})

        resp.data = msgpack.packb(json.dumps(coop))
        resp.status = falcon.HTTP_200

class Pigeons(object):
    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.pcoops = self.db.pigeoncoops

    def on_get(self, resp, req, ucid):
        coop = self.pcoops.find_one({'_id': ObjectId(ucid)}, projection=['pigeons'])

        resp.data = msgpack.packb(json.dumps({'pigeons': coop.get('pigeons')}))
        resp.status = falcon.HTTP_200

    def add_pigeon(self, ucid, upid, sender_uhid):
        self.pcoops.update_one({'_id': ObjectId(ucid)}, {'$push': {'pigeons': {'upid': ObjectId(upid), 'last_update': datetime.datetime.utcnow(), 'seen': (sender_uhid == ucid)}}})

    def remove_pigeon(self, ucid, upid):
        self.pcoops.update_one({'_id': ObjectId(ucid)}, {'$pull': {'pigeons': {'upid': ObjectId(upid)}}})

class Owner(object):
    def on_get(self, req, resp, ucid):
        resp.data = msgpack.packb(json.dumps({"uhid": ucid}))
        resp.status = falcon.HTTP_200

class UnseenCount(object):
    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.pcoops = self.db.pigeoncoops

    def on_get(self, req, resp, ucid):
        coop = self.pcoops.find_one({'_id': ObjectId(ucid)}, projection=['unseen_count'])

        resp.data = msgpack.packb(json.dumps({'unseen_count': coop.get('unseen_count')}))
        resp.status = falcon.HTTP_200
