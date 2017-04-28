import falcon
import falcon_jsonify
import msgpack
import json
import resources.hero as hero
import resources.guild as guild
import resources.search as search
import resources.pigeoncoop as pcoop
import resources.pigeon as pigeon
import resources.userAuth as auth
from falcon_cors import CORS

from pymongo import MongoClient

cors = CORS(allow_all_origins=True)

api = application = falcon.API(middleware=[falcon_jsonify.Middleware(help_messages=True), cors.middleware])

#TODO Edit <USR> and <PASSWORD> before deploy
#TODO Edit Change TestLibrary to GreatLibrary before deploy
#DB_REF = MongoClient("mongodb://<USR>:<PASSWORD>@cluster0-shard-00-00-ygomb.mongodb.net:27017,cluster0-shard-00-01-ygomb.mongodb.net:27017,cluster0-shard-00-02-ygomb.mongodb.net:27017/TestLibrary?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin").GreatLibrary
DB_REF = MongoClient().GreatLibary

#image_collection = images.Collection(storage_path)
#image = images.Item(storage_path)

#api.add_route('/images', image_collection)
#api.add_route('/images/{name}', image)

#Health check
class CheckCabbage(object):
	def on_get(self, req, resp):
		resp.data = str.encode(json.dumps({"success": "We've got cabbages my liege!"}))
		resp.status = falcon.HTTP_200

### HEALTH CHECK
api.add_route('/checkCabbage', CheckCabbage())

### Login
api.add_route('/login', auth.Login(DB_REF))

### HERO RELATED ROUTES
api.add_route('/hero/{uhid}', hero.Hero(DB_REF))
api.add_route('/hero/create', hero.NewHero(DB_REF))
api.add_route('/hero/{uhid}/playername', hero.PlayerName(DB_REF))
api.add_route('/hero/{uhid}/heroname', hero.HeroName(DB_REF))
api.add_route('/hero/{uhid}/email', hero.Email(DB_REF))
api.add_route('/hero/{uhid}/companions', hero.Companions(DB_REF))
api.add_route('/hero/{uhid}/key', hero.Key(DB_REF))
api.add_route('/hero/forgekey/{uiid}', hero.ForgeKey(DB_REF))
api.add_route('/hero/commissionkey', hero.CommissionKey(DB_REF))
api.add_route('/hero/{uhid}/companionrequests', hero.CompanionRequests(DB_REF))
api.add_route('/hero/{uhid}/companionrequest', hero.CompanionRequest(DB_REF))
api.add_route('/hero/{uhid}/companionrequestresponse', hero.CompanionRequestResponse(DB_REF))

### GUILD RELATED ROUTES
api.add_route('/guild/{ugid}', guild.Guild(DB_REF))
api.add_route('/guild/form', guild.FormGuild(DB_REF))
api.add_route('/guild/{ugid}/guildname', guild.Name(DB_REF))
api.add_route('/guild/{ugid}/games', guild.Games(DB_REF))
api.add_route('/guild/{ugid}/charter', guild.Charter(DB_REF))
api.add_route('/guild/{ugid}/members', guild.Members(DB_REF))
api.add_route('/guild/{ugid}/location', guild.Location(DB_REF))
api.add_route('/guild/{ugid}/leave/{uhid}', guild.LeaveGuild(DB_REF))
api.add_route('/guild/{ugid}/request/{uhid}', guild.RequestToJoinGuild(DB_REF))
api.add_route('/guild/{ugid}/requestresponse/{uhid}', guild.RespondToHeroRequest(DB_REF))
api.add_route('/guild/{ugid}/invite/{uhid}', guild.InviteHeroToJoin(DB_REF))
api.add_route('/guild/{ugid}/inviteresponse/{uhid}', guild.RespondToGuildInvite(DB_REF))

### SEARCH RELATED ROUTES
api.add_route('/search/guilds', search.AllGuilds(DB_REF))
api.add_route('/search/heros', search.AllHeros(DB_REF))

### PIGEON COOP ROUTES
api.add_route('/pigeoncoop/{ucid}', pcoop.Coop(DB_REF))
api.add_route('/pigeoncoop/{ucid}/owner', pcoop.Coop(DB_REF)) #Kinda a useless route...
api.add_route('/pigeoncoop/{ucid}/unseencount', pcoop.UnseenCount(DB_REF))

### PIGEON ROUTES
api.add_route('/pigeoncoop/{ucid}/newpigeon/', pigeon.NewPigeon(DB_REF))
api.add_route('/pigeoncoop/{ucid}/pigeon/{upid}', pigeon.Pigeon(DB_REF))
api.add_route('/pigeoncoop/{ucid}/messages/{upid}', pigeon.Messages(DB_REF))
