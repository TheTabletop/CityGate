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


if __name__ == '__main__':
    unittest.main()
