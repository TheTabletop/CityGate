import os
import uuid
import mimetypes

from pymongo import MongoClient
from pymongo import ReturnDocument
from bson import ObjectId

import falcon
import json
import datetime

import resources.pigeoncoop as coop

class NewPigeon(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.pigeons = self.db.pigeons

	def on_post(self, req, resp, ucid):
		params = req.json()
		participants = params.get("send_to")
		toUpdate = participants
		participants.append(ucid)
		# TODO: Check if a pigeon in the hero's inbox already exists with the passed participants, else
		if True:
			createResult = self.pigeons.insert_one(
				{
						"participants": participants,
						"has_not_read": toUpdate,
						"messages": [{"message": params.get("message"), "sender": ucid, "ts": datatime.datetime.utcnow()}]
				})

			if createResult is not None:
				coop.Pigeons.add_pigeon(ucid, createResult.inserted_id, True)

				for uhid in toUpdate:
					coop.Pigeons.add_pigeon(uhid, createResult.inserted_id, False)
			else:
				resp.data = str.encode(json.dumps({"Error": "Unable to create message"}))
				resp.status = falcon.HTTP_500
		else:
			Messages.add_message(req, resp, ucid)

class Pigeon(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.pigeons = self.db.pigeons
		self.coops = self.db.pigeoncoops

	def on_get(self, req, resp, ucid, upid):
		result = self.pigeons.find_one({"_id": ObjectId(upid)})

		resp.data = str.encode(json.dumps(result))
		resp.status = falcon.HTTP_200

	def on_delete(self, req, resp, ucid, upid):
		resultForRemoveP = self.pigeons.update_one({"_id": ObjectId(upid)}, {"$pull": {"has_not_read": ObjectId(ucid), "participants": ObjectId(ucid)}})
		resultForRemoveInC = coop.Pigeons.remove_pigeon(ucid, upid)

		resp.data = str.encode(json.dumps({"Success": "Removed hero from the pigeon's list of participants"}))
		resp.status = falcon.HTTP_202


class Messages(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.pigeons = self.db.pigeons
		self.heros = self.db.heros

	def on_get(self, req, resp, ucid, upid):
		result = self.pigeons.find_one({"_id": ObjectId(upid)}, projection=["messages"])

		if result is None:
			resp.status = falcon.HTTP_404
			resp.data = str.encode(json.dumps({"Error": "Unable to find associated pigeon."}))
		else:
			resp.data = str.encode(json.dumps(result.get("messages")))
			resp.status = falcon.HTTP_200

	def on_post(self, req, resp, ucid, upid):
		add_message(self, req, resp, ucid, upid)


	def add_message(self, req, resp, ucid, upid):
		result = self.pigeons.find_one({"_id": ObjectId(upid)})

		if result is not None:
			params = req.json

			message = params.get('message')
			sender = params.get('sender')

			if message is None or len(message)==0:
				resp.data = str.encode(json.dumps({'error': 'Must provide a message to send'}))
				resp.status = falcon.HTTP_400
				return
			if sender is None:
				resp.data = str.encode(json.dumps({"error": "Must proived the uhid of the hero that is sending the message"}))
				resp.status = falcon.HTTP_400
				return

			ts = datetime.datetime.utcnow()
			result = self.pigeons.find_one_and_update({'_id': ObjectId(upid)}, {'$push': {"messages": message, "sender": sender, "ts": ts}}, return_document=ReturnDocument.AFTER)

			if result is None:
				resp.data = str.encode(json.dumps({'error': 'Unable to update pigeon with new message'}))
				resp.status = falcon.HTTP_500
				return

			resp.data = str.encode(json.dumps({'upid': "%s".format(result.get('_id')), 'participants': result.get('participants'), 'messages': result.get('messages')}))

			#TODO notify recipients

		else:
			resp.data = str.encode(json.dumps({"error": "Unable to find pigeon to add message"}))
			resp.status = falcon.HTTP_404
