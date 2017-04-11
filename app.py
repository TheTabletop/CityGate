import falcon
import msgpack
import resources.hero as hero
import resources.guild as guild
import resources.search as search

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

### HERO RELATED ROUTES
api.add_route('/hero/{uhid}', hero.Hero("TODO"))
api.add_route('/hero/create', hero.NewHero("TODO"))
api.add_route('/hero/{uhid}/playername', hero.PlayerName("TODO"))
api.add_route('/hero/{uhid}/heroname', hero.HeroName("TODO"))
api.add_route('/hero/{uhid}/email', hero.HeroEmail("TODO"))
api.add_route('/hero/{uhid}/companions', hero.Companions("TODO"))
api.add_route('/hero/{uhid}/key', hero.Key("TODO"))
api.add_route('/hero/forgekey/{uiid}', hero.ForgeKey("TODO"))
api.add_route('/hero/commissionkey', hero.CommissionKey("TODO"))

### GUILD RELATED ROUTES
api.add_route('/guild/{ugid}', guild.Guild("TODO"))
api.add_route('/guild/form', guild.FormGuild("TODO"))
api.add_route('/guild/{ugid}/guildname', guild.GuildName("TODO"))
api.add_route('/guild/{ugid}/games', guild.Games("TODO"))
api.add_route('/guild/{ugid}/charter', guild.Charter("TODO"))
api.add_route('/guild/{ugid}/members/{uhid}', guild.Members("TODO"))
api.add_route('/guild/{ugid}/location', guild.Location("TODO"))

### SEARCH RELATED ROUTES
api.add_route('/search/guilds', search.AllGuilds("TODO"))
api.add_route('/search/heros', search.AllHeros("TODO"))

### PIGEON COOP ROUTES
api.add_route('/pigeoncoop/globalPigeonWaiting', pigeoncoop.globalPigeonWaiting("TODO"))
api.add_route('/pigeoncoop/killPigeon', pigeoncoop.killPigeon("TODO"))
