import falcon
import msgpack
import resources.hero as hero

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

### HERO RELATED ROUTES
api.add_route('/checkCabbage', checkCabbage())
api.add_route('/hero/{uhid}', hero.Hero("TODO"))
api.add_route('/hero/create', hero.NewHero("TODO"))
api.add_route('/hero/{uhid}/playername', hero.PlayerName("TODO"))
api.add_route('/hero/{uhid}/heroname', hero.HeroName("TODO"))
api.add_route('/hero/{uhid}/email', hero.HeroEmail("TODO"))
api.add_route('/hero/{uhid}/companions', hero.Companions("TODO"))
api.add_route('/hero/{uhid}/key', hero.Key("TODO"))
api.add_route('/hero/{uiid}/forgekey', hero.ForgeKey("TODO"))
