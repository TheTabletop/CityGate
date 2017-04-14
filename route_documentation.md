# API Routing Documentation
**NOTE:** It has not been put up on github yet, so the domain is listed as www.todo.com/

If you think a route should be accepting/returning different things or if routes are missing, please slack members of the backend team (and possibly even create a [ticket](https://github.com/TheTabletop/CityGate/issues) on github).

## Table Of Contents
* [Login Route](#login-route)
  * [Login](#login)
* [Hero Routes](#hero-routes)
  * [NewHero](#newhero)
  * [Hero](#hero)
  * [PlayerName](#playername)
  * [HeroName](#heroname)
  * [Email](#email)
  * [Companions](#companions)
  * [Key](#key)
  * [ForgeKey](#forgekey)
  * [CommissionKey](#commissionkey)
* [Guild Routes](#guild-routes)
  * [FormGuild](#formguild)
  * [Guild](#guild)
  * [Name](#name)
  * [Charter](#charter)
  * [Session](#session)
  * [Location](#location)
  * [Games](#games)
  * [Members](#members)
  * [RequestToJoinGuild](#requesttojoinguild)
  * [RespondToHeroRequest](#respondtoherorequest)
  * [InviteHeroToJoin](#inviteherotojoin)
  * [RespondToGuildInvite](#respondtoguildinvite)
  * [LeaveGuild](#leaveguild)
* [Pigeon Coop Routes](#pigeon-coop-routes)
  * [Coop](#coop)
  * [Pigeons](#pigeons)
  * [Owner](#owner)
  * [UnseenCount](#unseencount)
* [Pigeon Routes](#pigeon-routes)
  * [NewPigeon](#newpigeon)
  * [Pigeon](#pigeon)
  * [Messages](#messages)

# Login Route
## Login
www.todo.com/login

### on_post
**Send session with requests:** No
__Returns 202 on success__

**Expects a json with the request**
```python
{
  "hero": "<hero_name>",
  "key": "<heros_password>"
}
```
**Returns a json with the response**
```python
{
  "session_hash": "<random alhpa numeric string>",
  "uhid": "<unique_hero_id>"
}
```
# Hero Routes
## NewHero
www.todo.com/hero/create
**Send session with requests:** No
### on_post
__Returns 201 on success__
Used when a new hero (user) wants to create an account.
**Expects a json with the request**
```python
{
  "email": "<email address>",
  "key": "<password>",
  "playername": "<persons_name>",
  "heroname" : "<what they want to be called>",
  "games": ["game1", "game2", "game3", ...] #optional
  "backstory": "<backstory>" #optional
}
```
**Returns a json with the response**
```python
{
  "uhid": "<created hero uhid>"
}
```
## Hero
www.todo.com/hero/{uhid}

### on_get
**Send session token with requests:** Yes
__returns 200 on success__
Used when you want to get info about a hero. Returns slightly different information based on whether the session_hash is related to the requested hero or not. No json parameters are required to be sent.
**Returns a json with the response**
```python
{
  "_id": "<uhid>",
  "playername": "<player's name>",
  "heroname" : "<hero's name>",
  "games": ["list", "of", "games"],
  "companions": ["list", "of", "friends"],
  "guilds": ["list", "of", "guild", "ugids"]
  # the below are only returned if session token relates to hero requested (i.e. you request yourself)
  "email": "heros email",
  "guild_invites": ["guild", "ugids", "who", "invited", "hero"],
  "requested_guilds": ["guild", "ugids", "hero", "request", "to join"],
  "ucid": "<ucid>"
}
```

### on_post
**Send session token with requests:** Yes
__returns 202 on success__
Used for updating multiple data variables about the hero at once, can only be used if session token relates to the hero trying to be updated (i.e. you can only update yourself). Each key value pair is **OPTIONAL**.
**Expects a json with the request (it can be empty if you want)**
```python
{
  "playername": "<player's new name>",
  "heroname" : "<hero's new name>",
  "games": ["list", "of", "games"],
  "email": "<new email>",
  "backstory": "updated backstory>"
}
```

**Send session token with requests:** Yes
### on_delete
Used for deleting a hero (NOOOOOOO). No json parameters are required to be sent. If you sent any, they will be ignored.
__Returns 202 on success__

## PlayerName
### on_get
### on_post
## HeroName
### on_get
### on_post
## Email
### on_get
### on_post
## Companions
### on_get
### on_post
### on_delete
## Key
### on_post
## ForgeKey
### on_post
## CommissionKey
### on_post

# Guild Routes
## FormGuild
### on_post
## Guild
### on_get
### on_post
### on_delete
## Name
### on_get
### on_post
## Charter
### on_get
### on_post
## Session
### on_get
### on_post
## Location
### on_get
### on_post
## Games
### on_get
### on_post
### on_delete
## Members
### on_get
### on_delete
## RequestToJoinGuild
### on_post
### on_delete
## RespondToHeroRequest
### on_post
## InviteHeroToJoin
### on_post
### on_delete
## RespondToGuildInvite
### on_post
## LeaveGuild
### on_post

# Pigeon Coop Routes
## Coop
### on_get
## Pigeons
### on_get
## Owner
### on_get
## UnseenCount
### on_get

# Pigeon Routes
## NewPigeon
### on_post
## Pigeon
### on_get
### on_delete
## Messages
### on_get
### on_post
### on_delete
