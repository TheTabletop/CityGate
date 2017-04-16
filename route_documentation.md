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
www.todo.com/hero/{uhid}/key
### on_post
* **Send session token with requests:** Yes
* __returns 202 on success__

Used for updating the password of a logged in hero. Session token must be associated with hero who's password is being updated.

**Expects a json with the request**
```python
{
  "newkey": "<their new pass>"
  "oldkey": "<their old pass>"
}
```
## ForgeKey
www.todo.com/hero/forgekey/{uiid}
### on_post
* **Send a key forge token with :** No
* __returns 202 on success__

Used for forging a key that has been commissioned (i.e. a user setting their new password after forgetting it)

**Expects a json with the request**
```python
{
  "commission_id": "<the commission request>"
  "new_key": "<the new password>"
}
```
## CommissionKey
www.todo.com/hero/forgekey/
### on_post
* **Send a key forge token with :** No
* __returns 202 on success__

Used for commissioning a new key for a hero (when a person forgets their password). Send a link in an e-mail to the e-mail address provided (if there is a hero associated with the e-mail) with a link ending with /{commission_id}. This link should bring them to a page where they can reset their password using the ForgeKey route.

**Expects a json with the request**
```python
{
  "email": "<assumed account email>"
}
```
# Guild Routes
## FormGuild
www.todo.com/guild/formguild
### on_post
* **Send a key forge token with :** No
* __returns 201 on success__

Used for creating a new guild!
## Guild
www.todo.com/guild/{ugid}
### on_get
### on_post
### on_delete
## Name
www.todo.com/guild/{ugid}/name
### on_get
### on_post
## Charter
www.todo.com/guild/{ugid}/charter
### on_get
### on_post
## Session
www.todo.com/guild/{ugid}/session
### on_get
### on_post
## Location
www.todo.com/guild/{ugid}/location
### on_get
### on_post
## Games
www.todo.com/guild/{ugid}/games
### on_get
### on_post
### on_delete
## Members
www.todo.com/guild/{ugid}/members
### on_get
### on_delete
## RequestToJoinGuild
www.todo.com/guild/{ugid}/request/{uhid}
### on_post
### on_delete
## RespondToHeroRequest
www.todo.com/guild/{ugid}/requestresponse/{uhid}
### on_post
## InviteHeroToJoin
www.todo.com/guild/{ugid}/invite/{uhid}
### on_post
### on_delete
## RespondToGuildInvite
www.todo.com/guild/{ugid}/inviteresponse/{uhid}
### on_post
## LeaveGuild
www.todo.com/guild/{ugid}/leave/{uhid}
### on_post

# Pigeon Coop Routes
**NOTE**: The ucid (unique coop id) is the same as the associated hero's uhid (unique hero id). Thus if you know the hero's uhid, you automatically have what you need get that hero's pigeon coop (inbox).
## Coop
www.todo.com/coop/{ucid}
### on_get
## Pigeons
www.todo.com/coop/{ucid}/pigeons
### on_get
## Owner
www.todo.com/coop/{ucid}/owner (**note**: somewhat useless considering the ucid is the uhid)
### on_get
## UnseenCount
www.todo.com/coop/{ucid}/unseencount
### on_get

# Pigeon Routes
## NewPigeon
www.todo.com/coop/{ucid}/pigeon/newpigeon
### on_post
## Pigeon
www.todo.com/coop/{ucid}/pigeon/{upid}
### on_get
### on_delete
## Messages
www.todo.com/coop/{ucid}/pigeon/{upid}/messages
### on_get
### on_post
### on_delete
