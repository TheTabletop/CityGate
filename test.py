import unittest
import requests
from pymongo import MongoClient
import json

class CheckCabbage(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.db = MongoClient().greatLibrary

    def tearDown(self):
        """Call after every test case."""
        pass

    def testCheckCabbage(self):
        r = requests.get('http://localhost:8000/checkCabbage')
        self.assertEqual(r.status_code, 200)
        #self.assertEqual('')

class CreateHero(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.db = MongoClient().greatLibrary

    def tearDown(self):
        """Call after every test case."""
        pass

    def testHeroCreate(self):
        """Test that we can create a hero"""
        payload = {
            "email": 'foobar@rollforguild.com',
            "playername": 'Foo Bar',
            "heroname" : 'BarredFoo',
            "games": ['D&D 5e', 'D&D 3.5', 'Pathfinder'],
            "key": 'badpassword',
        }
        r = requests.post('http://localhost:8000/hero/create', data=json.dumps(payload))
        self.assertEqual(r.status_code, 201)
        self.assertNotEqual(self.db.heros.find_one({'email': 'foobar@rollforguild.com'}), None)

class LoginHero(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        pass

    def tearDown(self):
        """Call after every test case."""
        pass

    def testHeroLogin(self):
        """Test that we can login a hero"""
        self.assertTrue(True)

class checkPidgeons(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
         payload = {
            "email": 'foobar@rollforguild.com',
            "playername": 'Foo Bar',
            "heroname" : 'BarredFoo',
            "games": ['D&D 5e', 'D&D 3.5', 'Pathfinder'],
            "key": 'badpassword',
        }
		r = requests.post('http://localhost:8000/hero/create', data=json.dumps(payload))
		self.fooId = self.db.heros.find_one({'email': 'foobar@rollforguild.com'}).get('_id')
		payload = {
            "email": 'barfoo@rollforguild.com',
            "playername": 'Bar Foo',
            "heroname" : 'Fooey',
            "games": ['D&D 4rrie', 'D&D 3.75', 'Homebrew Abomination'],
            "key": 'asspassword',
        }
		requests.post('http://localhost:8000/hero/create', data=json.dumps(payload))
		self.barId = self.db.heros.find_one({'email': 'barfoo@rollforguild.com'}).get('_id')
		
	
    def tearDown(self):
        """Call after every test case."""
        pass

	def testPigeonCreateDuo(self):
		payload = {
		"send_to": [self.barId]
		"messages": ["blah blah blah", "words words"]
		}
		r = requests.post(string.Formatter.vformat("http://localhost:8000/pidgeon/{barId}/{barId}/newPidgeon"), data=json.dumps(payload))
		params = json.loads(r.content.stream.read().decode("utf-8")) #or r.text
        assertNotEqual(params.get("upid"), 0)
		assertEqual(r.status_code, 202)
		
	def testPigeonGet(self):
		r = requests.get(string.Formatter.vformat("http://localhost:8000/pidgeon/{barId}/{barId}/newPidgeon"), data=json.dumps(payload))
		assertNotEqual(data, None)
		
if __name__ == '__main__':
    unittest.main()
