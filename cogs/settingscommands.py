import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import random
import asyncio

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient('')["server"]

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_logchannel_1(self, ctx, channel: discord.TextChannel = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Вы не указали канал логирования.'
			lan3 = 'Готово'
			lan4 = 'Вы установили канал для отправки событий'
		else:
			lan1 = 'Error'
			lan2 = 'You didnt specify a logging channel.'
			lan3 = 'Done'
			lan4 = 'You have set up a channel for sending events'
		if channel is None:
			emb = discord.Embed(title=lan1, description=lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"logchannel": channel.id}})
			emb = discord.Embed(title =lan3, description = lan4)
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_minecommands(self, ctx, minmoney: int = None, maxmoney: int = None, minexp: int = None, maxexp: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для команды '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for the team '
		if minmoney is None or maxmoney is None or minexp is None or maxexp is None or minmoney > maxmoney or minexp > maxexp:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"minesetting": {"maxcash": maxmoney, "mincash": minmoney, "maxexp": maxexp, "minexp": minexp}}})
			emb = discord.Embed(title = lan3, description = f'{lan4}mine')
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_fightcommands(self, ctx, mindamagem: int = None, minmindamagem: int = None, maxdamage: int = None, maxmaxdamage: int = None, minhp: int = None, hp: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для команды '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for the team '
		if mindamagem is None or minmindamagem is None or maxdamage is None or maxmaxdamage is None or minhp is None or hp is None or mindamagem < minmindamagem or maxmaxdamage > maxdamage or minhp > hp:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"fightsettingss": {"mindamage": mindamagem, "maxdamage": maxdamage, "mindamage2": minmindamagem, "maxdamage2": maxmaxdamage, "minhp": minhp, "maxhp": hp}}})
			emb = discord.Embed(title = lan3, description = f'{lan4}fight')
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_boxsettings(self, ctx, switch: int = None, minmoney: int = None, maxmoney: int = None, minexp: int = None, maxexp: int = None, chance: int = None, boxchance: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для команды '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for the team '
		if switch > 1 or switch is None or minmoney is None or maxmoney is None or minexp is None or maxexp is None or chance is None or boxchance is None or minmoney > maxmoney or minexp > maxexp or chance > 100 or boxchance > 100:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"boxsettings": {"switch": switch, "maxcash": maxmoney, "mincash": minmoney, "maxexp": maxexp, "minexp": minexp, "chance": chance, "chancebox": boxchance}}})
			emb = discord.Embed(title = lan3, description = f'{lan4}online_battle')
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_symbols(self, ctx, symbol: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для команды '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for the team '
		if symbol is None or symbol > 99:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"levelelements": {"symbols": symbol}}})
			emb = discord.Embed(title = lan3, description = f'{lan4}```Symbols```')
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_levelxp(self, ctx, int1: int = None, int2: int = None, int3: int = None, int4: int = None, int5: int = None, int6: int = None, int7: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for '
		if int1 is None or int2 is None or int3 is None or int4 is None or int5 is None or int6 is None or int7 is None or int1 > int2 or int5 > int6:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"levelelements": {"mingetexp": int1, "maxgetexp": int2, "cashget": int3, "integerexp": int4, "newminattack": int5, "newmaxattack": int6, "newhp": int7}}})
			emb = discord.Embed(title =lan3, description = f"{lan4}```XP```")
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_muterole(self, ctx, namerole: str = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for '
		if namerole is None:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"muterole": namerole}})
			emb = discord.Embed(title =lan3, description = f"{lan4}```Muted_Role```")
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_maxwarn(self, ctx, warns: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for '
		if warns is None:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"maxwarn": warns}})
			emb = discord.Embed(title =lan3, description = f"{lan4}```Warns```")
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_maxprewarn(self, ctx, maxprewarns: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for '
		if maxprewarns is None:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"maxprewarn": maxprewarns}})
			emb = discord.Embed(title =lan3, description = f"{lan4}```Pre_Warns```")
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_accesnfsw(self, ctx, access: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for '
		if access > 1:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"accesscommand": access}})
			emb = discord.Embed(title =lan3, description = f"{lan4}```AccesCommand```")
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def add_wordlist(self, ctx, word: str = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы добавили новое слово в блокированные!'
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have added a new word to blocked!'
		if word is None:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$push": {"wordblock": word}})
			emb = discord.Embed(title =lan3, description = f"{lan4}```{word}```")
			await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_wordlist_acces(self, ctx, access: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка'
			lan2 = 'Неправильное использование команды.'
			lan3 = 'Готово'
			lan4 = 'Вы установили настройки для '
		else:
			lan1 = 'Error'
			lan2 = 'Incorrect use of the command.'
			lan3 = 'Done'
			lan4 = 'You have set the settings for '
		if access is None or access > 1:
			emb = discord.Embed(title=lan1, description = lan2)
			await ctx.send(embed=emb)
		else:
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"wordacces": access}})
			emb = discord.Embed(title =lan3, description = f"{lan4}```Acces_Word```")
		await ctx.send(embed=emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_cashname(self, ctx, *, valuetype: str):
		if str(ctx.guild.region) == 'russia':
			lan1 = "Успешно установлен параметр"
			lan2 = "Теперь валюта вашего сервера:"
		else:
			lan1 = "Parameter set successfully"
			lan2 = "Now the currency of your server:"
		for x in self.db.settings.find({"server_id": ctx.guild.id}):
			idem = x['coinsname']['id_emoji'][1]
			namem = x['coinsname']['id_emoji'][0]
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"coinsname": {"cash": valuetype, "id_emoji": [str(namem), int(idem)]}}})
			emb = discord.Embed(title = lan1, description = f"{lan2} `{valuetype}`")
			await ctx.send(embed = emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_cookiename(self, ctx, *, valuetype: str):
		if str(ctx.guild.region) == 'russia':
			lan1 = "Успешно установлен параметр"
			lan2 = "Теперь репутация вашего сервера:"
		else:
			lan1 = "Parameter set successfully"
			lan2 = "Now the rep of your server:"
		for x in self.db.settings.find({"server_id": ctx.guild.id}):
			idem = x['coockiename']['id_emoji'][1]
			namem = x['coockiename']['id_emoji'][0]
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"coockiename": {"coockie": valuetype, "id_emoji": [str(namem), int(idem)]}}})
			emb = discord.Embed(title = lan1, description = f"{lan2} `{valuetype}`")
			await ctx.send(embed = emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_cashemoji(self, ctx, emoji: discord.Emoji):
		if str(ctx.guild.region) == 'russia':
			lan1 = "Успешно установлен эмодзи"
			lan2 = "Теперь эмодзи вашего сервера:"
		else:
			lan1 = "Emoji set successfully"
			lan2 = "Now the emoji of your server:"
		nameemoji = emoji.name
		idemoji = emoji.id
		for x in self.db.settings.find({"server_id": ctx.guild.id}):
			namevalute = x['coinsname']['cash']
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"coinsname": {"cash": namevalute, "id_emoji": [str(nameemoji), int(idemoji)]}}})
			emb = discord.Embed(title = lan1, description = f"{lan2} <:{str(nameemoji)}:{int(idemoji)}>")
			await ctx.send(embed = emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def set_cookieemoji(self, ctx, emoji: discord.Emoji):
		if str(ctx.guild.region) == 'russia':
			lan1 = "Успешно установлен эмодзи"
			lan2 = "Теперь эмодзи вашего сервера:"
		else:
			lan1 = "Emoji set successfully"
			lan2 = "Now the emoji of your server:"
		nameemoji = emoji.name
		idemoji = emoji.id
		for x in self.db.settings.find({"server_id": ctx.guild.id}):
			namevalute = x['coockiename']['coockie']
			self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"coockiename": {"coockie": namevalute, "id_emoji": [str(nameemoji), int(idemoji)]}}})
			emb = discord.Embed(title = lan1, description = f"{lan2} <:{str(nameemoji)}:{int(idemoji)}>")
			await ctx.send(embed = emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def create_command(self, ctx, namecommand: str, *, bodycommand: str):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Комманда была успешно создана'
			lan2 = 'Вызов комманды'
			lan3 = 'Ответ на комманду от бота'
		else:
			lan1 = 'You have successfully created a command'
			lan2 = 'Calling a command'
			lan3 = 'Response to a command from the bot'
		self.db.customcommands.insert_one(
			{
				"name": namecommand,
				"body": bodycommand,
				"server_id": ctx.guild.id
			}
		)
		emb = discord.Embed(title = lan1, description = f'{lan2} `{namecommand}`. {lan3}: {bodycommand}')
		await ctx.send(embed = emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def delete_command(self, ctx, namecommand: str):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Комманды была успешно удалена'
		else:
			lan1 = 'The command was successfully deleted'
		self.db.customcommands.delete_one({"server_id": ctx.guild.id, "name": namecommand})
		emb = discord.Embed(title = lan1)
		await ctx.send(embed = emb)

def setup(client):
	client.add_cog(User(client))
