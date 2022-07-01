import discord
from discord.ext import commands
import os
import pymongo
from pymongo import MongoClient
#import psutil as ps

def insert_returns(body):
	if isinstance(body[-1], ast.Expr):
		body[-1] = ast.Return(body[-1].value)
		ast.fix_missing_locations(body[-1])

	if isinstance(body[-1], ast.If):
		insert_returns(body[-1].body)
		insert_returns(body[-1].orelse)

	if isinstance(body[-1], ast.With):
		insert_returns(body[-1].body)

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.command()
	async def aping(self, ctx):
		if ctx.author.id == '':
			def b2h(number, typer=None):
				# Пример Работы Этой Функции перевода чисел:
				# >> bytes2human(10000)
				# >> '9.8K'
				# >> bytes2human(100001221)
				# >> '95.4M'

				if typer == "system":
					symbols = ('KБ', 'МБ', 'ГБ', 'TБ', 'ПБ', 'ЭБ', 'ЗБ', 'ИБ')  # Для перевода в Килобайты, Мегабайты, Гигобайты, Террабайты, Петабайты, Петабайты, Эксабайты, Зеттабайты, Йоттабайты
				else:
					symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')  # Для перевода в обычные цифры (10k, 10MM)

				prefix = {}

				for i, s in enumerate(symbols):
					prefix[s] = 1 << (i + 1) * 10

				for s in reversed(symbols):
					if number >= prefix[s]:
						value = float(number) / prefix[s]
						return '%.1f%s' % (value, s)

				return f"{number}B"

			mem = ps.virtual_memory()
			ping = int(self.client.latency)
			ping_emoji = "🟩🔳🔳🔳🔳"
			ping_list = [
				{"ping": 0.00000000000000000, "emoji": "🟩🔳🔳🔳🔳"},
				{"ping": 0.10000000000000000, "emoji": "🟧🟩🔳🔳🔳"},
				{"ping": 0.15000000000000000, "emoji": "🟥🟧🟩🔳🔳"},
				{"ping": 0.20000000000000000, "emoji": "🟥🟥🟧🟩🔳"},
				{"ping": 0.25000000000000000, "emoji": "🟥🟥🟥🟧🟩"},
				{"ping": 0.30000000000000000, "emoji": "🟥🟥🟥🟥🟧"},
				{"ping": 0.35000000000000000, "emoji": "🟥🟥🟥🟥🟥"}
			]
			for ping_one in ping_list:
				if ping <= ping_one["ping"]:
					ping_emoji = ping_one["emoji"]
					break

			embed = discord.Embed(title='Статистика Бота', color=0x0c0c0c)
			embed.add_field(name='Использование CPU', value=f'В настоящее время используется: {ps.cpu_percent()}%', inline=True)
			embed.add_field(name='Использование RAM', value=f'Доступно: {b2h(mem.available, "system")}\n' f'Используется: {b2h(mem.used, "system")} ({mem.percent}%)\n' f'Всего: {b2h(mem.total, "system")}', inline=True)
			embed.add_field(name='Пинг Бота', value=f'Пинг: {ping * 1000:.0f}ms\n' f'`{ping_emoji}`', inline=True)

 
			await ctx.send(embed=embed)

	@commands.command()
	async def fileget(self, ctx):
		if ctx.author.id == '':
			directory = os.getcwd()
			list_files = os.listdir(directory)
			files_and_folders = "\n".join(list_files)
			await ctx.send(files_and_folders)

	@commands.command()
	async def updatebase(self, ctx):
		if ctx.author.id == '':
			for guild in self.client.guilds:
				await self.db.settings.update({"server_id": ctx.guild.id}, {"$set": {"logging": 0}})
			#for guild in self.client.guilds:
				#db.settings.update({"server_id": guild.id}, {"$set": {"coinsname": {"cash": "Cash", "id_emoji": ["dollar", 778652353246920754]}}})
				#db.settings.update({"server_id": guild.id}, {"$set": {"coockiename": {"coockie": "Coockie`s", "id_emoji": ["cookie", 778882928679321640]}}})
			await ctx.send('GOOD WORK!!!')
				#await ctx.send('Во мне пока не прописано обновление базы. Может ты ничего не обновлял?')

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def playk(self, ctx, *, arg):
		if ctx.author.id == '':
			embed=discord.Embed(title='Статус бота изменен!',color=0x37393F, description=' Бот теперь играет в ' + arg )
			await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name=arg))
			await ctx.send(embed=embed)
			await ctx.message.delete()

	# .watch
	@commands.command()
	@commands.has_permissions(administrator = True)
	async def watch(self, ctx, *, arg):
		if ctx.author.id == '':
			embed=discord.Embed(title='Статус бота изменен!',color=0x37393F, description=' Бот теперь смотрит ' + arg )
			await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(name=arg, type=discord.ActivityType.watching))
			await ctx.send(embed=embed)
			await ctx.message.delete()

	# .listen
	@commands.command()
	@commands.has_permissions(administrator = True)
	async def listen(self, ctx, *, arg):
		if ctx.author.id == '':
			embed=discord.Embed(title='Статус бота изменен!',color=0x37393F, description=' Бот теперь слушает ' + arg )
			await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(name=arg, type=discord.ActivityType.listening))
			await ctx.send(embed=embed)
			await ctx.message.delete()
  
	# .stream
	@commands.command()
	@commands.has_permissions( administrator = True)
	async def stream(self, ctx, *, arg):
		if ctx.author.id == '':
			embed=discord.Embed(title='Статус бота изменен!',color=0x37393F, description=' Бот теперь стримит ' + arg )
			await self.client.change_presence( status = discord.Status.online, activity = discord.Streaming(name= arg , url='url'))
			await ctx.send(embed=embed)
			await ctx.message.delete()

	@commands.command()
	async def adminconsole(self, ctx):
		if ctx.author.id == '':
			await ctx.send('''
Доступные комманды: fileget, updatebase, watch, stream, game, listen, unload, load, reload

Команда !fileget без аргументов, выводит все файлы в папке бота
Команды !watch, stream, game, listen <arg: любое количество слов>. Устанавливает статус бота
Команды !unload, load, reload, updatebase без аргументов
				''')
def setup(client):
	client.add_cog(User(client))
