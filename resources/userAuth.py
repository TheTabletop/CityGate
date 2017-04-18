import os
import uuid
import mimetypes
import datetime

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json
import msgpack

class Login(object):

    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.userAuth = self.db.userAuth
        self.userAuth.create_index({"expires": 1}, {'expireAfterSeconds': 0})

    def on_post(self, req, resp):
        result = self.userAuth.insertone(
            {
                "uhid": req.get_param('uhid'),
                "expires": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
             })
        resp.data=msgpack.packb(json.dumps({'sessionID': result.inserted_id}))
        resp.status = falcon.HTTP_201

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_404

class updateExpire(object):

    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.userAuth = self.db.userAuth

    def incrementExpire(self):
        self.userAuth.updateon(
            {
                "expires": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }
        )

class checkuhid(object):

    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.userAuth = self.db.userAuth

    def checkid(self, currUserID, sessionID):
        result = self.userAuth.findone({'_id': ObjectId(sessionID)},projection=['uhid'])
        return currUserID==result.get('uhid')
