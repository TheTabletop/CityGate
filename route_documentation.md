d
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
* **Send session with requests:** No
* __Returns 202 on success__

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
### on_post
* **Send session with requests:** No
* __Returns 201 on success__

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
* **Send session token with requests:** Yes
* __returns 200 on success__

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
* **Send session token with requests:** Yes
* __returns 202 on success__

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

### on_delete
* **Send session token with requests:** Yes
* __Returns 742 on success__

Used for deleting a hero (NOOOOOOO). No json parameters are required to be sent. If you sent any, they will be ignored.

## PlayerName
www.todo.com/hero/{uhid}/playername
### on_get
* **Send session token with requests:** Yes
* __returns 200 on success__

Used for getting the name of the person behind the hero.

**Returns a json with the response**
```python
{
  "_id": "<uhid>",
  "playername": "<player's name>"
}
```

### on_post
* **Send session token with requests:** Yes
* __returns 202 on success__

Used for getting updating a hero's name. Session token must be associated with the hero trying to be updated (i.e. you can only update your own hero name)

**Expects a json with the request**
```python
{
  "playername": "<player's new name>"
}
```

**Returns a json with the response**
```python
{
  "_id": "<uhid>",
  "playername": "<player's name>"
}
```

## HeroName
www.todo.com/hero/{uhid}/heroname
### on_get
* **Send session token with requests:** Yes
* __returns 200 on success__

Used for getting the name of the hero.

**Returns a json with the response**
```python
{
  "_id": "<uhid>",
  "heroname": "<hero's name>"
}
```

### on_post
* **Send session token with requests:** Yes
* __returns 202 on success__

Used for getting updating a hero's name. Session token must be associated with the hero try to be updated (i.e. you can only update your own hero name)

**Expects a json with the request**
```python
{
  "heroname": "<hero's new name>"
}
```

**Returns a json with the response**
```python
{
  "_id": "<uhid>",
  "heroname": "<hero's name>"
}
```
## Email
www.todo.com/hero/{uhid}/email
### on_get
* **Send session token with requests:** Yes
* __returns 200 on success__

Used for getting the hero's email.

**Returns a json with the response**
```python
{
  "_id": "<uhid>",
  "email": "<hero's email>"
}
```

### on_post
* **Send session token with requests:** Yes
* __returns 202 on success__

Used for getting updating a hero's email. Session token must be associated with the hero try to be updated (i.e. you can only update your own hero name)

**Expects a json with the request**
```python
{
  "email": "<hero's new email>"
}
```

**Returns a json with the response**
```python
{
  "_id": "<uhid>",
  "email": "<hero's email>"
}
```
## Companions
www.todo.com/hero/{uhid}/companions
### on_get
* **Send session token with requests:** Yes
* __returns 200 on success__

Used for the list of the hero's companions (friends).

**Returns a json with the response**
```python
{
  "_id": "<uhid>",
  "companions": ["List", "of", "companions"]
}
```

### on_delete
* **Send session token with requests:** Yes
* __returns 202 on success__

Used for removing a companion from a heros companion list. Session token must be associated with either the uhid provided in url of the http request or the `uhid_companion` in the data json data sent with the http request. 

**Expects a json with the request**
```python
{
  "uhid_companion": "<uhid of hero you want to remove>"
}
```
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
