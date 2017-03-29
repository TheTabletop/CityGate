import os
import uuid
import mimetypes

from pymongo import MongoClient
from bson import ObjectId

import falcon
import json
import msgpack

#ALLOWED_IMAGE_TYPES = (
#    'image/gif',
#    'image/jpeg',
#    'image/png',
#)

#def validate_image_type(req, resp, resource, params):
#	if req.content_type not in ALLOWED_IMAGE_TYPES:
#		msg = 'Image type not allowed, Must be PNG, JPEG, or GIF'
#		raise falcon.HTTPBadRequest('Bad request', msg)

class NewGuild(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	def on_post(self, req, resp):
		result = self.heros.insert_one(
			{
				"email": req.get_param('email'),
				"first": req.get_param('first'),
				"last" : req.get_param('last'),
				"games": req.get_param('games'),
				"pass": req.get_param('password'),
			})

		resp.data = msgpack.packb({"Info": "Successfully created a new hero with id: {}".format(result)})
		resp.status = falcon.HTTP_201

class Hero(object):

	def __init__(self, db_reference):
		self.db = db_reference
		self.db = MongoClient().greatLibrary
		self.heros = self.db.heros

	# For updating a hero's Info
	# Can only edit hero info for hero id of session token
	def on_post(self, req, resp):

	# Get a hero by unique hero id (uhid)
	# Must have an active user session token
	def on_get(self, req, resp, uhid):
		result = self.heros.find({"_id": ObjectId(uhid)})

		if result.count() == 0:
			resp.data = msgpack.packb({"Error": "We could not find that hero, they must have nat 20'd  their stealth check"})
			resp.status = falcon.HTTP_404
		elif result.count() == 1:
			hero = result[0]
			for k,v in hero.items():
				if type(hero[k]) is ObjectId:
					temp = "{}".format(hero[k])
					hero[k] = temp
			resp.data = msgpack.packb(json.dumps(hero))
			resp.status = falcon.HTTP_200
		else:
			resp.data = msgpack.packb({"Error": "Somehow there is hero identity theft, damn rogues..."})
			resp.status = falcon.HTTP_724
