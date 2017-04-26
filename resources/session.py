import os
import uuid
import mimetypes

from pymongo import MongoClient
from bson import ObjectId

import datetime

class Session(object):
    def __init__(self, DB_REF):
        self.db = DB_REF
        self.sessions = self.db.sessions

    def NewSession(self, start, game, notes, ugid):
        result = self.sessions.insert_one({'start': start, 'game': game, 'notes': notes, 'ugid': ugid})

        if result.acknowledged:
            return result.inserted_id
        else:
            return None

    def UpdateSession(self, usid, game=None, start=None, notes=None):
        mongoDict = {'$set': {}}
        if game:
            mongoDict['$set']['game'] = game
        if time:
            mongoDict['$set']['start'] = start
        if notes:
            mongoDict['$set']['notes'] = notes
        result = self.sessions.find_one_and_update({'_id': ObjectId(usid)}, mongoDict, return_document=ReturnDocument.AFTER)

        return result

    def GetSession(self, usid):
        return self.sessions.find_one({'_id': ObjectId(usid)})

    def GetAllGuildSessions(self, ugid):
        return self.sessions.find({'ugid': ugid})

    def DeleteSession(self, usid):
        result = self.sessions.delete_one({'_id': ObjectId(usid)})

        return result.acknowledged and result.delete_count!=0

    def DeleteAllGuildSessions(self, ugid):
        self.sessions.delete_many({'ugid': ugid})
        result = self.sessions.find({'ugid': ugid})

        return result.count==0
