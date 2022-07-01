#!/usr/bin/env python

import discord
from discord.ext import commands
from discord.ext.commands import errors
from discord import errors as dpy_errors
from config import settings
import json
import os
import pymongo
from pymongo import MongoClient

mongo_url = ""
cluster = MongoClient(mango_url)
db = cluster["server"]

collection = db["users"]

def get_prefix(client, message):
	for row in db.settings.find({"server_id": message.guild.id}):
		return row["prefix"]

intents = discord.Intents.all()
intents.integrations = False
intents.webhooks = False
intents.typing = False
intents.guild_typing = False
intents.dm_typing = False
intents.dm_reactions = False

client = commands.Bot(command_prefix=get_prefix, intents = intents)
client.remove_command('help')

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="satiricon.xyz | $help v1"))
	for guild in client.guilds:
		for member in guild.members: 
			if collection.find({"ids": member.id, "server_id": guild.id}) is None:
				collection.insert_one({
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
			if db.settings.find({"server_id": guild.id}) is None:
				db.settings.insert_one({
					"server_id": int(guild.id), #id сервера
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
			if db.globaluser.find_one({"ids": member.id}) is None:
				db.globaluser.insert_one({
					"ids": member.id,
					"membercash": 0,
					"idv": [],
					"vchest": {
						"lowchest": 0,
						"bigchest": 0,
						"maxchest": 0
					}
				})
			else:
				pass
	print('bot start')

@client.command()
async def load(ctx, extension):
	if ctx.author.id == '':
		client.load_extension(f"cogs.{extension}")
		await ctx.send("Cogs is loaded")
	else:
		await ctx.send("Error 0x_kekW")

@client.command()
async def unload(ctx, extension):
	if ctx.author.id == '':
		client.unload_extension(f"cogs.{extension}")
		await ctx.send("Cogs is loaded")
	else:
		await ctx.send("Error 0x_kekW")

@client.command()
async def reload(ctx, extension):
	if ctx.author.id == '':
		client.unload_extension(f"cogs.{extension}")
		client.load_extension(f"cogs.{extension}")
		await ctx.send("Cogs is loaded")
	else:
		await ctx.send("Error 0x_kekW")

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

##@client.event
#async def on_command_error(ctx, err):
#	if str(ctx.guild.region) == 'russia':
#		lan2 = 'У бота отсутствуют права'
#		lan3 = 'Выдайте их ему для полного функционирования бота'
#		lan4 = 'У вас недостаточно прав для запуска этой команды'
#		lan5 = 'Правильное использование команды'
#		lan6 = 'У вас еще не прошел кулдаун на команду'
#		lan7 = 'Подождите еще'
#		lan8 = 'У бота нет прав на запуск этой команды'
#		lan9 = 'Произошла неизвестная ошибка'
#		lan10 = 'Пожалуйста, свяжитесь с разработчиками для исправления этой ошибки'
#	else:
#		lan2 = 'The bot has no rights'
#		lan3 = 'Give them to him for the full functioning of the bot'
#		lan4 = 'You Dont have enough permissions to run this command'
#		lan5 = 'Correct use of the command'
#		lan6 = 'You havent had a team cooldown yet'
#		lan7 = 'Wait a bit longer'
#		lan8 = 'The bot doesn t have permission to run this command'
#		lan9 = 'An unknown error occurred'
#		lan10 = 'Please contact the developers to fix this error'
#	if isinstance(err, errors.BotMissingPermissions):
#		await ctx.send(embed=discord.Embed(description=f"{lan2}: {' '.join(err.missing_perms)}\n{lan3}"))
#
#	elif isinstance(err, errors.MissingPermissions):
#		await ctx.send(embed=discord.Embed(description=f"{lan4}!"))
#
#	elif isinstance(err, errors.UserInputError):#
#		await ctx.send(embed=discord.Embed(description=f"{lan5} {ctx.command}({ctx.command.brief}): `{ctx.command.usage}`"))
#
#	elif isinstance(err, commands.CommandOnCooldown):
#		await ctx.send(embed=discord.Embed(description=f"{lan6} {ctx.command}!\n{lan7} {err.retry_after:.2f}"))
#
#	elif isinstance(err, dpy_errors.Forbidden):
#		await ctx.send(embed=discord.Embed(description=f"{lan8}!"))
#	else:
#		await ctx.send(embed=discord.Embed(description=f"{lan9}: `{err}`\n{lan10}"))

client.run(settings["TOKEN"])
