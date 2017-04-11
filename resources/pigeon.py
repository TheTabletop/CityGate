import os
import uuid
import mimetypes

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json
import msgpack
import datetime

import resources.pigeoncoop as coop

class NewPigeon(object):
    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.pigeons = self.db.pigeons

    def on_post(self, req, resp, ucid):
        params = json.loads(req.stream.read().decode("utf-8"))
        participants = params.get("send_to")
        toUpdate = participants
        participants.append(ucid)
        # TODO: Check if a pigeon in the hero's inbox already exists with the passed participants, else

        createResult = self.pigeons.insert_one(
            {
                    "participants": participants,
                    "has_not_read": to_update,
                    "messages": [params.get("message")]
            })

        if createResult is not None:
            coop.Pigeons.add_pigeon(ucid, createResult.inserted_id, True)

            for uhid in toUpdate:
                coop.Pigeons.add_pigeon(uhid, createResult.inserted_id, False)
        else:
            resp.data = msgpack.packb(json.dumps({"Error": "Unable to create message"}))
            resp.status = falcon.HTTP_500

class Pigeon(object):
    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.pigeons = self.db.pigeons

    def on_get(self, req, resp, ucid, upid):
        pass

    def on_delete(self, req, resp, ucid, upid):
        pass

def Messages(object):
    def __init__(self, db_reference):
        self.db = db_reference
        self.db = MongoClient().greatLibrary
        self.pigeons = self.db.pigeons

    def on_get(self, req, resp, ucid, upid):
        result = self.pigeons.find_one({"_id": ObjectId(upid)}, projection=["messages"])

        if result is None:
            resp.status = falcon.HTTP_404
            resp.data = msgpack.packb(json.dumps({"Error": "Unable to find associated pigeon."}))
        else:
            resp.data = msgpack.packb(json.dumps(result.get("messages")))
            resp.status = falcon.HTTP_200

    def on_post(self, req, resp, ucid, upid):
        pass

    def add_message(self, req, resp, ucid, upid):
        result = self.pigeons.find_one({"_id": ObjectId(upid)})

        if result is not None:
            toNotify = result.
        else:
            resp.data = msgpack.packb(json.dumps({"Error": "Unable to find pigeon to add message"}))
            resp.status = falon.HTTP_404
