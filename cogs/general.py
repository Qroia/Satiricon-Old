import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.Cog.listener()
	async def on_member_join(self):
		for guild in self.client.guilds:
			for member in guild.members: 
				if await self.db.users.find({"ids": member.id, "server_id": member.guild.id}) is None:
					await self.db.users.insert_one({
						"server_id": member.guild.id,
						"ids": member.id,
						"warns": 0,
						"prewarn": 0,
						"wins": 0,
						"cash": 0,
						"rep": 0,
						"lvl": 1,
						"exp": 0,
						"hp": 90,
						"mana": 100,
						"maxattack": 50,
						"minattack": 40
						})
				else:
 					pass

	@commands.Cog.listener()
	async def on_member_remove(self, member, guild):
		await self.db.users.delete_one({"ids": member.id, "server_id": guild.id})

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		for guild in self.client.guilds:
			for member in guild.members: 
				if await self.db.users.find({"ids": member.id, "server_id": guild.id}) is None:
					await self.db.users.insert_one({
						"server_id": guild.id,
						"ids": member.id,
						"warns": 0,
						"prewarn": 0,
						"wins": 0,
						"cash": 0,
						"rep": 0,
						"lvl": 1,
						"exp": 0,
						"hp": 90,
						"mana": 100,
						"maxattack": 50,
						"minattack": 40
						})
				else:
					pass
				if await self.db.settings.find({"server_id": guild.id}) is None:
					await self.db.settings.insert_one({
						"server_id": guild.id, #id сервера
						"prefix": "$",
						"rolelevels": 0, # количество зарегестрированных уровней для опыта
						"itemshop": 0, # количество зарегестрированных предметов в магазине
						"roleshop": 0, # количество зарегестрированных ролей в магазине
						"logchannel": 0, # канал куда отправляются логи
						"onlinesettings": 
						{
							"maxcash": 0,
							"mincash": 0,
							"maxexp": 0, 
							"minexp": 0
						}, # настройки наград для битв между игроками
						"boxsettings": 
						{
							"switch": 0, # 0 - выключено, 1 - вкл
							"maxcash": 0,
							"mincash": 0,
							"maxexp": 0, 
							"minexp": 0,
							"chancebox": 0,
							"chance": 0
						}, # настройки выпадения боксов. Первые два значение шанс выпадения награды, третий шанс выпадения предмета из roleshops и itemshops
						"levelelements": 
						{
							"symbols": 12, 
							"mingetexp": 1, 
							"maxgetexp": 2, 
							"cashget": 1, 
							"integerexp": 50, 
							"newminattack": 1, 
							"newmaxattack": 2, 
							"newhp": 1
						}, # 1 - сколько нужно символов, остальное кроме "50" - награды.
						"minesetting": 
						{
							"maxcash": 0, 
							"mincash": 0, 
							"maxexp": 0, 
							"minexp": 0
						}, # для works
						"fightsettingss": 
						{
							"mindamage": 0, 
							"maxdamage": 0, 
							"mindamage2": 0, 
							"maxdamage2": 0, 
							"minhp": 0, 
							"maxhp": 0
						}, # для works
						"coinsname": 
						{
							"cash": "Cash", 
							"id_emoji": ["dollar", 778652353246920754]
						}, # named coins named and emoji cash
						"coockiename": 
						{
							"coockie": "Coockie`s",
							"id_emoji": ["cookie", 778882928679321640]
						}, # named coockie`s named and emoji coockie
						"muterole": "Muted", # name mute role
						"maxwarn": 3,  # maximum warns per 1 user
						"maxprewarn": 10, # maximum prewarns per 1 users
						"accesscommand": 0, # access on nfsw pictures
						"wordblock": [], # words black list
						"wordacces": 0, # access on black list words 
						"servercash": 0, # valute server "BETA
						"days": 0, # ACCES PRO COMMANDS
						"startmessage": 
						{
							"tosend": 2, # 0 - отправка в лс, 1 - отправка в системный канал, 2 - отключено
							"contentsend": "hi"
						},
						"leavemessage":
						{
							"tosend": 2, # 0 - отправка в лс, 1 - отправка в системный канал, 2 - отключено
							"contentsend": "hi"
						},
						"boostmessage":
						{
							"tosend": 2, # 0 - отправка в лс, 1 - отправка в системный канал, 2 - отключено
							"contentsend": "hi"
						}
					})
				else:
					pass

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		await self.db.users.remove({"server_id": guild.id})
		await self.db.dange.remove({"server_id": guild.id})
		await self.db.unit.remove({"server_id": guild.id})
		await self.db.itemshop.remove({"guild": guild.id})
		await self.db.shop.remove({"guild": guild.id})
		await self.db.settings.remove({"server_id": guild.id})
		await self.db.customcommands.remove({"server_id": guild.id})


	@commands.command()
	@commands.has_permissions(administrator=True)
	async def setprefix(self, ctx, prefix):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Префикс изменён на:'
		else:
			lan1 = 'Prefix changed to:'
		await self.db.settings.update({"server_id": ctx.guild.id}, {"$set": {"prefix": prefix}})
		await ctx.channel.purge(limit=1)
		await ctx.send(lan1 + f"```{prefix}```")


def setup(client):
	client.add_cog(User(client))
