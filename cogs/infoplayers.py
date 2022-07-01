import discord
from discord.ext import commands
import datetime
import pymongo
import datetime
import time
from pymongo import MongoClient
from Cybernator import Paginator

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.command(aliases = ['инфо'])
	async def info(self, ctx, member:discord.Member = None):
		if member == None:
			member = ctx.author
		if member.nick == None:
			nick = member.name
		else:
			nick = member.nick
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Общая характеристика'
			lan2 = 'Характеристики'
			lan3 = 'Уровень'
			lan4 = 'ОЗ'
			lan5 = 'Урон'
			lan6 = 'Остальное'
			lan7 = 'Варны'
			lan8 = 'Пре-варны'
			lan9 = 'Всего ролей'
			lan10 = 'Гл.Роль'
			lan11 = 'Дата создания аккаунта'
			lan12 = 'Дата входа на сервер'
			lan13 = 'Информация о пользователе'
			lan14 = 'Баланс'
		else:
			lan1 = 'General characteristics'
			lan2 = 'Characteristics'
			lan3 = 'Level'
			lan4 = 'OH'
			lan5 = 'Damage'
			lan6 = 'Other'
			lan7 = 'Warns'
			lan8 = 'The pre-Warns'
			lan9 = 'Total roles'
			lan10 = 'Leading role of'
			lan11 = 'Account creation date'
			lan12 = 'Server login date'
			lan13 = 'User Information'
			lan14 = 'Balance'
		for x in await self.db.settings.find({"server_id": ctx.guild.id}):
			for y in await self.db.users.find({"ids": member.id, "server_id": ctx.guild.id}):
				xall = ((y["lvl"] * x['levelelements']["integerexp"]) + 50) * (y["lvl"] + 1)
				x1 = round((int(y["exp"]) / int(xall)) * 100)
				if x1 in range(1, 20):
					x2 = '⬜⬛⬛⬛⬛'
				elif x1 in range(20, 40):
					x2 = '⬜⬜⬛⬛⬛'
				elif x1 in range(40, 60):
					x2 = '⬜⬜⬜⬛⬛'
				elif x1 in range(60, 80):
					x2 = '⬜⬜⬜⬜⬛'
				elif x1 in range(80, 100):
					x2 = '⬜⬜⬜⬜⬜'
				else:
					x2 = '⬛⬛⬛⬛⬛'
				emb = discord.Embed(title = lan1,description = f'''
			**--------{lan14}-----------**
			{x["coinsname"]["cash"]}: {y["cash"]} <:{x["coinsname"]["id_emoji"][0]}:{x["coinsname"]["id_emoji"][1]}>
			{x["coockiename"]["coockie"]}: {y["rep"]} <:{x["coockiename"]["id_emoji"][0]}:{x["coockiename"]["id_emoji"][1]}>
			**--------{lan2}-------**
			{x1}% / 100% ({y["exp"]} / {xall})
			{x2}

			{lan3}: {y["lvl"]}
			{lan4}: {y["hp"]}
			{lan5}: {y["minattack"]}-{y["maxattack"]}

			**--------{lan6}-------**

			{lan7}: {y["warns"]}
			{lan8}: {y["prewarn"]}

			ID: {member.id}
			{lan9}: {len(member.roles)}
			{lan10}: {member.top_role.name}
			
			{lan11}: {str(member.created_at)[:16]}
			{lan12}: {str(member.joined_at)[:16]}
				''', color = 0x556B2F )
				emb.set_author(name = f'{lan13} {nick}', icon_url = f'{member.avatar_url}')
				emb.set_thumbnail(url=member.avatar_url)
				await ctx.send(embed = emb)

	@commands.command(aliases = ['пинг'])
	async def ping(self, ctx):
		ping = self.client.latency
		ping_emoji = "🟩🔳🔳🔳🔳"
		ping_list = [
			{"ping": 0.10000000000000000, "emoji": "🟧🟩🔳🔳🔳"},
			{"ping": 0.15000000000000000, "emoji": "🟥🟧🟩🔳🔳"},
			{"ping": 0.20000000000000000, "emoji": "🟥🟥🟧🟩🔳"},
			{"ping": 0.25000000000000000, "emoji": "🟥🟥🟥🟧🟩"},
			{"ping": 0.30000000000000000, "emoji": "🟥🟥🟥🟥🟧"},
			{"ping": 0.35000000000000000, "emoji": "🟥🟥🟥🟥🟥"}]
	
		for ping_one in ping_list:
			if ping > ping_one["ping"]:
				ping_emoji = ping_one["emoji"]
				break
		if str(ping_emoji) == '🟩🔳🔳🔳🔳' or str(ping_emoji) == '🟧🟩🔳🔳🔳' or str(ping_emoji) == '🟥🟧🟩🔳🔳':
			emb = discord.Embed(title='Pong! :ping_pong:', description=f'{ping_emoji} `{ping * 1000:.0f}ms`', colour=0x00e600)
			await ctx.send(embed=emb)
		elif str(ping_emoji) == '🟥🟥🟧🟩🔳' or str(ping_emoji) == '🟥🟥🟥🟧🟩':
			emb = discord.Embed(title='Pong! :ping_pong:', description=f'{ping_emoji} `{ping * 1000:.0f}ms`', colour=0xffa500)
			await ctx.send(embed=emb)
		elif str(ping_emoji) == '🟥🟥🟥🟥🟧' or str(ping_emoji) == '🟥🟥🟥🟥🟥':
			emb = discord.Embed(title='Pong! :ping_pong:', description=f'{ping_emoji} `{ping * 1000:.0f}ms`', colour=0xff0000)
			await ctx.send(embed=emb)

	@commands.command(aliases = ['сервер'])
	@commands.has_permissions(administrator = True)
	async def server(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Пользователей'
			lan2 = 'Участников'
			lan3 = 'Ботов'
			lan4 = 'Онлайн'
			lan5 = 'Отошёл'
			lan6 = 'Не Беспокоить'
			lan7 = 'Оффлайн'
			lan8 = 'Каналов'
			lan9 = 'Голосовые'
			lan10 = 'Текстовые'
			lan11 = 'Уровень Буста'
			lan12 = 'Бустеров'
			lan13 = 'Количество Ролей'
			lan14 = 'Создатель сервера'
			lan15 = 'Регион сервера'
			lan16 = 'Дата создания сервера'
		else:
			lan1 = 'Users'
			lan2 = 'Participants'
			lan3 = 'Bots'
			lan4 = 'Online'
			lan5 = 'Moved away'
			lan6 = 'Do not Disturb'
			lan7 = 'Offline'
			lan8 = 'Channels'
			lan9 = 'Voice'
			lan10 = 'Text'
			lan11 = 'Boost Level'
			lan12 = 'Boosters'
			lan13 = 'Number of Roles'
			lan14 = 'Server Creator'
			lan15 = 'Server Region'
			lan16 = 'Server creation date'
 
		members = ctx.guild.members
		bots = len([m for m in members if m.bot])
		users = len(members) - bots
		online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
		offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
		idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
		dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
		allvoice = len(ctx.guild.voice_channels)
		alltext = len(ctx.guild.text_channels)
		allroles = len(ctx.guild.roles)
 
		embed = discord.Embed(title=f"{ctx.guild.name}", color=0xd84b20, timestamp=ctx.message.created_at)
		embed.set_thumbnail(url=ctx.guild.icon_url)
 
		embed.add_field(name=lan1, value=f"{lan2}: **{users}**\n"
												f"{lan3}: **{bots}**\n"
												f"{lan4}: **{online}**\n"
												f"{lan5}: **{idle}**\n"
												f"{lan6}: **{dnd}**\n"
												f"{lan7}: **{offline}**")
 
		embed.add_field(name=lan8, value=f"{lan9}: **{allvoice}**\n"
											 f"{lan10}: **{alltext}**\n")
 
		embed.add_field(name=lan11, value=f"{ctx.guild.premium_tier} ({lan12}: {ctx.guild.premium_subscription_count})")
		embed.add_field(name=lan13, value=f"{allroles}")
		embed.add_field(name=lan14, value=f"{ctx.guild.owner}")
		embed.add_field(name=lan15, value=f"{ctx.guild.region}")
		embed.add_field(name=lan16, value=f"{ctx.guild.created_at.strftime('%b %#d %Y')}")
		await ctx.send(embed=embed)

	@commands.command(aliases = ['помощь'])
	async def help(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = """
Узнать побольше о нашем боте, ты сможешь с помощью нашей документации - https://docs.satiricon.xyz/

Из-за нескольких трудных комманд мы не можем сюда всё вместить. Но ниже ты увидишь список без полного синтаксиса.
			"""
			typelan = "ru"
		else:
			lan1 = """
To learn more about our bot, you can use our documentation - https://docs.satiricon.xyz/

due to several difficult commands, we can't fit everything in here. But below you will see a list without the full syntax.
			"""
			typelan = "en"
		for x in await self.db.settings.find({"server_id": ctx.guild.id}):
			prefixs = x["prefix"]
		embed1 = discord.Embed(title="Info[Help]", description=lan1)
		embed1.add_field(name = "Bot Version:", value = "1.0", inline=True)
		embed1.add_field(name = "WebSite", value = "SOON", inline=True)
		embed1.add_field(name = "Language", value = "RU and EN", inline=True)
		embeddange = discord.Embed(title="Dange Commands[All-Moderation]", description= f'''
		{prefixs}dange

		{prefixs}createdange
		{prefixs}createunit
		{prefixs}deleteunit
		''')
		embedeconomia = discord.Embed(title="Economia Commands[All-Moderation]", description=f'''
		{prefixs}roleshop
		{prefixs}itemshop
		{prefixs}buy_role
		{prefixs}buy_item

		{prefixs}add_item
		{prefixs}add_role
		{prefixs}delete_role
		{prefixs}delete_item
		''')
		embedgame = discord.Embed(title="Game Commands [All-Moderators]", description=f'''
		{prefixs}o_r
		{prefixs}rsp
		{prefixs}sap
		{prefixs}eightball
		{prefixs}dice
		{prefixs}rr
		''')
		embedother = discord.Embed(title="Other commands [All]", description=f"""
		{prefixs}spotify
		{prefixs}gstart
		{prefixs}weather
		{prefixs}restr
		{prefixs}youtube
		{prefixs}translate
		{prefixs}wiki
		{prefixs}google
		{prefixs}short
		{prefixs}whoyou
		{prefixs}calc
		{prefixs}emoji_flex
		{prefixs}embed_builder
		{prefixs}poll
		{prefixs}covid_19
		""")
		embedadmins = discord.Embed(title="Settings commands [Admin]", description=f"""
		{prefixs}set_prefix
		{prefixs}set_logchannel
		{prefixs}set_minecommands
		{prefixs}set_fightcommands
		{prefixs}set_boxsettings
		{prefixs}set_symbols
		{prefixs}set_levelexp
		{prefixs}set_muterole
		{prefixs}set_maxwarn
		{prefixs}set_maxprewarn
		{prefixs}set_accesnfsw
		{prefixs}add_wordlist
		{prefixs}set_wordlist_acces
		""")
		embedmoderation = discord.Embed(title="Moderation commands [Moderators Flex Permission]", description=f"""
		{prefixs}ban
		{prefixs}mute
		{prefixs}kick
		{prefixs}unban
		{prefixs}unmute
		{prefixs}renameMember
		{prefixs}clear
		""")
		embedrp = discord.Embed(title="RP commands [All]", description=f"""
		{prefixs}hug
		{prefixs}kill
		{prefixs}cry
		{prefixs}kiss
		{prefixs}hit
		{prefixs}tickle
		{prefixs}overtake
		{prefixs}perturbation
		{prefixs}misunderstanding
		{prefixs}shrug
		{prefixs}hello
		{prefixs}bye
		{prefixs}happy
		""")
		embeds = [embed1, embeddange, embedeconomia, embedgame, embedother, embedadmins, embedmoderation, embedrp]
		message = await ctx.send(embed=embed1)
		page = Paginator(self.client, message, only=ctx.author, use_more=False, embeds=embeds, language = typelan)
		await page.start()

	@commands.command()
	async def roleinfo(self, ctx):
		await ctx.send("Send")

	@commands.command()
	async def leaders(self, ctx, types: str = None):
		emb = discord.Embed(title = "Leaders", color = 0xFF00FF)
		#emb.add_field(name = "", value = "", inline=False)
		contr = 0
		for x in await self.db.users.find({"server_id": ctx.guild.id}).sort("cash", -1).limit(10):
			for y in await self.db.settings.find({"server_id": ctx.guild.id}):
				member = await self.client.get_user(x['ids'])
				contr += 1
				if contr == 1:
					emb.add_field(name = f":crown: #{contr} :crown: ", value = f"**{member.display_name}**•{x['cash']} <:{y['coinsname']['id_emoji'][0]}:{y['coinsname']['id_emoji'][1]}>•{x['rep']} <:{y['coockiename']['id_emoji'][0]}:{y['coockiename']['id_emoji'][1]}>", inline = False)
				else:
					emb.add_field(name = f"#{contr}", value = f"**{member.display_name}**•{x['cash']} <:{y['coinsname']['id_emoji'][0]}:{y['coinsname']['id_emoji'][1]}>•{x['rep']} <:{y['coockiename']['id_emoji'][0]}:{y['coockiename']['id_emoji'][1]}>", inline = False)
				#emb.add_field(name = "```Name```", value = f"``````", inline = True)
				#emb.add_field(name = "```Balance```", value = f"```{x['cash']}```", inline = True)
				#emb.add_field(name = f"```{valuerep}```", value = f"```{x['rep']}```", inline = True)
		await ctx.send(embed=emb)

def setup(client):
	client.add_cog(User(client))
