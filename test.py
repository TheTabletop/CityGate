import string
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

###HERO CLASS TESTS###

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

class ChangeHeroName(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"email": 'foobar@rollforguild.com',
			"playername": 'Foo Bar',
			"heroname": 'BarredFoo',
			"games": ['D&D 5e', 'D&D 3.5', 'Pathfinder'],
			"key": 'badpassword',
		}
		r = requests.post('http://localhost:8000/hero/create', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testChangeHeroName(self):
		"""Test that we can create a hero"""
		payload = {
			"heroname" : 'FooedBar',
		}
		r = requests.post('http://localhost:8000/hero/{uuid}/heroname', data=json.dumps(payload))#TODO: Set UUID
		self.assertEqual(r.status_code, 201)
		self.assertEqual("FooedBar", (self.db.heros.find_one({'email': 'foobar@rollforguild.com'}))["heroname"]) #TODO: Test correct DB reference

class ChangePlayerName(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"email": 'foobar@rollforguild.com',
			"playername": 'Foo Bar',
			"heroname": 'BarredFoo',
			"games": ['D&D 5e', 'D&D 3.5', 'Pathfinder'],
			"key": 'badpassword',
		}
		r = requests.post('http://localhost:8000/hero/create', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testChangePlayerName(self):
		"""Test that we can create a hero"""
		payload = {
			"playername" : 'Bar Foo',
		}
		r = requests.post('http://localhost:8000/hero/{uuid}/playername', data=json.dumps(payload))#TODO: Set UUID
		self.assertEqual(r.status_code, 201)
		self.assertEqual("Bar Foo", (self.db.heros.find_one({'email': 'foobar@rollforguild.com'}))["playername"]) #TODO: Test correct DB reference


class ChangeEmail(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"email": 'foobar@rollforguild.com',
			"playername": 'Foo Bar',
			"heroname": 'BarredFoo',
			"games": ['D&D 5e', 'D&D 3.5', 'Pathfinder'],
			"key": 'badpassword',
		}
		r = requests.post('http://localhost:8000/hero/create', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testChangeEmail(self):
		"""Test that we can create a hero"""
		payload = {
			"email": 'barfoo@rollforguild.com',
		}
		r = requests.post('http://localhost:8000/hero/{uuid}/email', data=json.dumps(payload))  # TODO: Set UUID
		self.assertEqual(r.status_code, 201)
		self.assertNotEqual(None, (self.db.heros.find_one({'email': 'barfoo@rollforguild.com'})).get("playername")) # TODO: Test correct DB reference

class ChangeKey(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"email": 'foobar@rollforguild.com',
			"playername": 'Foo Bar',
			"heroname": 'BarredFoo',
			"games": ['D&D 5e', 'D&D 3.5', 'Pathfinder'],
			"key": 'badpassword',
		}
		r = requests.post('http://localhost:8000/hero/create', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testChangeKey(self):
		"""Test that we can create a hero"""
		payload = {
			"key": 'goodpassword',
		}
		r = requests.post('http://localhost:8000/hero/{uuid}/key', data=json.dumps(payload))  # TODO: Set UUID
		self.assertEqual(r.status_code, 201)
		self.assertEqual("goodpassword", (self.db.heros.find_one({'email': 'barfoo@rollforguild.com'})).get(
			"key"))  # TODO: Test correct DB reference

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

##TODO: Forge and Commission key routes as well as Companion

###GUILD CLASS TESTS###

class CreateGuild(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"email": 'foobar@rollforguild.com',
			"playername": 'Foo Bar',
			"heroname": 'BarredFoo',
			"games": ['D&D 5e', 'D&D 3.5', 'Pathfinder'],
			"key": 'badpassword',
		}
		r = requests.post('http://localhost:8000/hero/create', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testGuildCreate(self):
		"""Test that we can create a hero"""
		payload = {
			"guildname": 'Foos Guild',
			"charter": 'The Charter',
			"location": 'Madison',
			"games": [],
			"members": ['foobar@rollforguild.com'],
			"future_sessions": [],
			"previous_sessions": [],
			"hero_requests": [],
			"invited_heros": []
		}
		r = requests.post('http://localhost:8000/guild/form', data=json.dumps(payload))
		self.assertEqual(r.status_code, 201)
		self.assertNotEqual(self.db.guild.find_one({'Foos Guild'}), None)

class ChangeGuildName(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"guildname": 'Foos Guild',
			"charter": 'The Charter',
			"location": 'Madison',
			"games": [],
			"members": ['foobar@rollforguild.com'],
			"future_sessions": [],
			"previous_sessions": [],
			"hero_requests": [],
			"invited_heros": []
		}
		r = requests.post('http://localhost:8000/guild/form', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testChangeGuildName(self):
		"""Test that we can create a hero"""
		payload = {
			"guildname": 'Bars Guild',
		}
		r = requests.post('http://localhost:8000/guild/{ugid}/guildname', data=json.dumps(payload))  # TODO: Set UGID
		self.assertEqual(r.status_code, 201)
		self.assertNotEqual(None, self.db.guild.find_one({'Bars Guild'}))

class ChangeGuildGames(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"guildname": 'Foos Guild',
			"charter": 'The Charter',
			"location": 'Madison',
			"games": [],
			"members": ['foobar@rollforguild.com'],
			"future_sessions": [],
			"previous_sessions": [],
			"hero_requests": [],
			"invited_heros": []
		}
		r = requests.post('http://localhost:8000/guild/form', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testChangeGuildGames(self):
		"""Test that we can create a hero"""
		payload = {
		   "games": ['Pathfinder'],
		}
		r = requests.post('http://localhost:8000/guild/{ugid}/games', data=json.dumps(payload))  # TODO: Set UGID
		self.assertEqual(r.status_code, 201)
		self.assertEqual(['Pathfinder'], (self.db.guild.find_one({'Foos Guild'})).get("games")) # TODO: Test correct DB reference

class ChangeGuildCharter(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"guildname": 'Foos Guild',
			"charter": 'The Charter',
			"location": 'Madison',
			"games": [],
			"members": ['foobar@rollforguild.com'],
			"future_sessions": [],
			"previous_sessions": [],
			"hero_requests": [],
			"invited_heros": []
		}
		r = requests.post('http://localhost:8000/guild/form', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testChangeGuildCharter(self):
		"""Test that we can create a hero"""
		payload = {
			"charter": 'The NEW Charter',
		}
		r = requests.post('http://localhost:8000/guild/{ugid}/charter', data=json.dumps(payload))  # TODO: Set UGID
		self.assertEqual(r.status_code, 201)
		self.assertEqual('The NEW Charter', (self.db.guild.find_one({'Foos Guild'})).get("charter"))  # TODO: Test correct DB reference

class ChangeGuildLocation(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"guildname": 'Foos Guild',
			"charter": 'The Charter',
			"location": 'Madison',
			"games": [],
			"members": ['foobar@rollforguild.com'],
			"future_sessions": [],
			"previous_sessions": [],
			"hero_requests": [],
			"invited_heros": []
		}
		r = requests.post('http://localhost:8000/guild/form', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testChangeGuildLocation(self):
		"""Test that we can create a hero"""
		payload = {
			"location": 'Middleton',
		}
		r = requests.post('http://localhost:8000/guild/{ugid}/location', data=json.dumps(payload))  # TODO: Set UGID
		self.assertEqual(r.status_code, 201)
		self.assertEqual('Middleton', (self.db.guild.find_one({'Foos Guild'})).get("location"))  # TODO: Test correct DB reference

class ChangeGuildMembers(unittest.TestCase):
	def setUp(self):
		"""Call before every test case."""
		self.db = MongoClient().greatLibrary
		payload = {
			"guildname": 'Foos Guild',
			"charter": 'The Charter',
			"location": 'Madison',
			"games": [],
			"members": ['foobar@rollforguild.com'],
			"future_sessions": [],
			"previous_sessions": [],
			"hero_requests": [],
			"invited_heros": []
		}
		r = requests.post('http://localhost:8000/guild/form', data=json.dumps(payload))

	def tearDown(self):
		"""Call after every test case."""
		pass

	def testChangeGuildMembers(self):
		"""Test that we can create a hero"""
		payload = {
			"members": ['foobar@rollforguild.com', ' barfoo@rollforguild.com'],
		}
		r = requests.post('http://localhost:8000/guild/{ugid}/members', data=json.dumps(payload))  # TODO: Set UGID
		self.assertEqual(r.status_code, 201)
		self.assertEqual(['foobar@rollforguild.com', ' barfoo@rollforguild.com'], (self.db.guild.find_one({'Foos Guild'})).get("members"))  # TODO: Test correct DB reference

##TODO: Member requests, Invites, etc

###PIDGEON CLASS TESTS###

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
		"send_to": [self.barId],
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
