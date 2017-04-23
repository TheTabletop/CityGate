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

    def UpdateSessionGame(self, game, usid):
        result = self.sessions.find_one_and_update({'_id': ObjectId(usid)}, {'$set': {'game': game}}, return_document=ReturnDocument.AFTER)
        return result.get('game')

    def UpdateSessionTime(self, time, usid):
        result = self.sessions.find_one_and_update({'_id': ObjectId(usid)}, {'$set': {'time': time}}, return_document=ReturnDocument.AFTER)
        return result.get('time')

    def UpdateSessionNotes(self, notes, usid):
        result = self.sessions.find_one_and_update({'_id': ObjectId(usid)}, {'$set': {'notes': notes}}, return_document=ReturnDocument.AFTER)
        return result.get('notes')

    def DeleteSession(self, usid):
        result = self.sessions.delete_one({'_id': ObjectId(usid)})

        return result.acknowledged and result.delete_count!=0


    def DeleteAllGuildSessions(self, ugid):
        self.sessions.delete_many({'ugid': ugid})
        result = self.sessions.find({'ugid': ugid})

        return result.count==0
