import os
import uuid
import mimetypes

from pymongo import MongoClient
from bson import ObjectId
from multiprocessing import Process

import falcon
import json
import msgpack


#Needs the uhid in the req object
class buildCoop(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.coops = self.db.pigeoncoops
		
	def on_post(self, req, resp):
	
		result = self.coops.insert_one({
			"pigeons":[],
			"unread_messages":0
		})
		if result.inserted_id is None:
			resp.data = msgpack.packb({"Failed": "Unable to create hero's coop"})
			resp.status = falcon.HTTP_500
		
		result2 = self.db.heros.update_one({"_id":ObjectId(req.params_get('uhid'))}, {'$set':{'ucid':ObjectIdresult.inserted_id}})
		if result2.modified_count == 1:
			resp.data = msgpack.packb({"Success": "Successfully created hero's coop"})
			resp.status = falcon.HTTP_202
		else:
			resp.data = msgpack.packb({"Failed": "Unable to add coop id to hero's ucid field"})
			resp.status = falcon.HTTP_500
			
		def on_get(self, req, resp, uiid):
		resp.data = msgpack.pack({"Message": "The coop isn't built yet, try the post method."})
		resp.status = falcon.HTTP_403

#Needs the uhid in the req object
class globalPigeonWaiting(object):
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.coops = self.db.pigeoncoops
		
	def on_get(self, req, resp):
		coopId = self.db.heros.find_one({"_id": ObjectId(req.params_get('uhid'))}, projection=['ucid'])
		num = self.coops.find_one({"_id": coopId.get("_id")}, projection=['unread_messages'])
		
		if num is None:
			resp.data = msgpack.packb({"Failed": "Unable to get number of unread messages"})
			resp.status = falcon.HTTP_500
		else:
			resp.data = msgpack.packb({"unread_messages": num.get('unread_messages')})
			resp.status = falcon.HTTP_202

			
#needs the uhid and upid identifiers in the req
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
		
#needs uhid in the req
class pigeonRollCall(object)
	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.coops = self.db.pigeoncoops
		
	def on_get(self, req, resp):
		coopId = self.db.heros.find_one({"_id": ObjectId(req.params_get('uhid'))}, projection=['ucid'])
		
		pidgeonList = self.db.
		