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
If successful, status is 201

**Expects a json with the request**
```json
{
  "hero": "<hero_name>",
  "key": "<heros_password>"
}
```
**Returns a json with the response**
```json
{
  "session_token": "<random alhpa numeric string>",
  "uhid": "<unique_hero_id>"
}
```
# Hero Routes
## NewHero
www.todo.com/hero/create
### on_post
If successful, status is 201
**Expects a json with the request**
```json
{
  "email": "<email address>",
  "key": "<password>",
  "playername": "<persons_name>",
  "heroname" : "<what they want to be called>",
  "games": ["game1", "game2", "game3", ...] #optional
}
```
**Returns a json with the response**
```json
{"uhid": "<created hero uhid"}
```
## Hero
### on_get
### on_post
### on_delete
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
