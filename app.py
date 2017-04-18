import falcon
import msgpack
import resources.hero as hero
import resources.guild as guild
import resources.search as search
import resources.pigeoncoop as pcoop
import resources.pigeon as pigeon
import resources.userAuth as auth

api = application = falcon.API()

DB_PATH = ""

#image_collection = images.Collection(storage_path)
#image = images.Item(storage_path)

#api.add_route('/images', image_collection)
#api.add_route('/images/{name}', image)

#Health check
class CheckCabbage(object):
	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.data = msgpack.packb({"Msg": "We've got cabbages my liege!"})

### HEALTH CHECK
api.add_route('/checkCabbage', CheckCabbage())

### Login
api.add_route('/login', auth.Login("TODO"))

### HERO RELATED ROUTES
api.add_route('/hero/{uhid}', hero.Hero("TODO"))
api.add_route('/hero/create', hero.NewHero("TODO"))
api.add_route('/hero/{uhid}/playername', hero.PlayerName("TODO"))
api.add_route('/hero/{uhid}/heroname', hero.HeroName("TODO"))
api.add_route('/hero/{uhid}/email', hero.Email("TODO"))
api.add_route('/hero/{uhid}/companions', hero.Companions("TODO"))
api.add_route('/hero/{uhid}/key', hero.Key("TODO"))
api.add_route('/hero/forgekey/{uiid}', hero.ForgeKey("TODO"))
api.add_route('/hero/commissionkey', hero.CommissionKey("TODO"))

### GUILD RELATED ROUTES
api.add_route('/guild/{ugid}', guild.Guild("TODO"))
api.add_route('/guild/form', guild.FormGuild("TODO"))
api.add_route('/guild/{ugid}/guildname', guild.Name("TODO"))
api.add_route('/guild/{ugid}/games', guild.Games("TODO"))
api.add_route('/guild/{ugid}/charter', guild.Charter("TODO"))
api.add_route('/guild/{ugid}/members', guild.Members("TODO"))
api.add_route('/guild/{ugid}/location', guild.Location("TODO"))
api.add_route('/guild/{ugid}/leave/{uhid}', guild.LeaveGuild("TODO"))
api.add_route('/guild/{ugid}/request/{uhid}', guild.RequestToJoinGuild("TODO"))
api.add_route('/guild/{ugid}/requestresponse/{uhid}', guild.RespondToHeroRequest("TODO"))
api.add_route('/guild/{ugid}/invite/{uhid}', guild.InviteHeroToJoin("TODO"))
api.add_route('/guild/{ugid}/inviteresponse/{uhid}', guild.RespondToGuildInvite("TODO"))

### SEARCH RELATED ROUTES
api.add_route('/search/guilds', search.AllGuilds("TODO"))
api.add_route('/search/heros', search.AllHeros("TODO"))

### PIGEON COOP ROUTES
api.add_route('/pigeoncoop/{ucid}', pcoop.Coop("TODO"))
api.add_route('/pigeoncoop/{ucid}/owner', pcoop.Coop("TODO")) #Kinda a useless route...
api.add_route('/pigeoncoop/{ucid}/unseencount', pcoop.UnseenCount("TODO"))

### PIGEON ROUTES
api.add_route('/pigeoncoop/{ucid}/newpigeon/', pigeon.NewPigeon("TODO"))
api.add_route('/pigeoncoop/{ucid}/pigeon/{upid}', pigeon.Pigeon("TODO"))
api.add_route('/pigeoncoop/{ucid}/messages/{upid}', pigeon.Messages("TODO"))
