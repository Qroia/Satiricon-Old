import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot 

import json
import random
import asyncio
import math
import requests
import datetime

class game(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.command(aliases = ['ор'])
	async def o_r(self, ctx):
		if str(ctx.guild.region):
			lan1 = "Орел или решка"
			lan2 = "Команда вызвана"
			lan3 = "Подбрасываем монетку"
			lan4 = "**Решка**"
			lan5 = "**Орёл**"
		else:
			lan1 = "Heads or tails"
			lan2 = " Command called"
			lan3 = " Flip a coin"
			lan4 = "**Tails**"
			lan5 = "**Eagle**"
		robot = ["орёл", "решка"]
		robot_choice = random.choice(robot)
								   
		emb = discord.Embed(title=lan1, colour=discord.Colour.red(), timestamp=ctx.message.created_at)
		emb.set_author(name="⠀", icon_url="https://www.iconpacks.net/icons/2/free-dollar-coin-icon-2139-thumb.png")
		emb.set_footer(text=f'{lan2}: {ctx.author.name}', icon_url=ctx.author.avatar_url)
								   
		if robot_choice == "орёл":
			val1 = lan5
		if robot_choice == "решка":
			val1 = lan4

		emb.add_field(name=f"{lan3}....", value=val1)

		await ctx.send(embed=emb)
								   

	@commands.command(aliases = ['кнб'])
	async def rsp(self, ctx, mess):
		robot = ['Камень', 'Ножницы', 'Бумага']
		stone_list = ["stone", "камень","к"]
		paper_list = ["paper", "бумага", "б"]
		scissors_list = ["scissors", "ножницы","н"]  
								   
		out = {"icon": None, "value": None, "img": None}
								   
		robot_choice = random.choice(robot)  
								   
		win_list = ["Вы выиграли!","Вы проиграли :с", "Ничья!"]
			
		# Embed
		emb = discord.Embed(title=robot_choice, colour=discord.Colour.red(), timestamp=ctx.message.created_at)
								   
		if mess.lower() in stone_list:       
			if robot_choice == 'Ножницы':
				win = win_list[0]
				out["icon"] = "✂"
			elif robot_choice == 'Бумага':
				win = win_list[1]
				out["icon"] = "🧻"
			else:
				win = win_list[2]
				out["icon"] = "🥔"

		elif mess.lower() in paper_list:
			if robot_choice == 'Камень':
				win = win_list[0]
				out["icon"] = "🥔"     
			elif robot_choice == 'Ножницы':
				win = win_list[1]
				out["icon"] = "✂"             
			else:
				win = win_list[2]
				out["icon"] = "🧻"               

		elif mess.lower() in scissors_list:
			if robot_choice == 'Бумага':
				win = win_list[0]
				out["icon"] = "🧻"               
			elif robot_choice == 'Камень':
				win = win_list[1]
				out["icon"] = "🥔"                
			else:
				win = win_list[2]  
				out["icon"] = "✂"     
		else:
			await ctx.send("Error!")
			return
				
		if win == "Вы выиграли!":
			out["img"] = "https://cdn.4archive.org/img/VCgadmDm.jpg"
		elif win == "Вы проиграли :с":
			out["img"] = "https://get.wallhere.com/photo/anime-anime-girls-brunette-brown-eyes-1194271.jpg"
		else:
			out["img"] = "https://i.imgur.com/zw1BKld.png"
								   
		emb.add_field(name=out["icon"], value=win)
		emb.set_author(name="⠀",
		icon_url=out["img"])
		emb.set_footer(icon_url=ctx.author.avatar_url)
		await ctx.send(embed=emb)


	@commands.command(aliases = ['сапёр'])
	async def sap(self, ctx):
		await ctx.message.delete()
		if str(ctx.guild.region) == 'russia':
			lan1 = "Выберете сложность"
			lan2 = "Неверная реакция!"
			lan3 = "Кол-во столбцов:"
			lan4 = "Кол-во строк:"
			lan5 = "Кол-во клеток:"
			lan6 = "Кол-во бомб:"
		else:
			lan1 = "Choose a difficulty"
			lan2 = "Wrong reaction!"
			lan3 = "number of columns:"
			lan4 = "Number of rows: "
			lan5 = "Number of cells: "
			lan6 = "Nnumber of bombs:"

		r_list = ['🟩', '🟧', '🟥']

		rows = None
		columns = None

		msg = await ctx.send(f'{lan1} :\n\n{r_list[0]}— Easy\n{r_list[1]}— Medium\n{r_list[2]}— Hard')
		for r in r_list:
			await msg.add_reaction(r)
		try:
			react, user = await self.client.wait_for('reaction_add', timeout=30.0, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in r_list)
		except Exception:
			await msg.delete()
		else:
			if str(react.emoji) == r_list[0]:
				columns = 4
				rows = 4
				await msg.clear_reactions()
			elif str(react.emoji) == r_list[1]:
				columns = 8
				rows = 8
				await msg.clear_reactions()
			elif str(react.emoji) == r_list[2]:
				columns = 12
				rows = 12
				await msg.clear_reactions()
			else:
				await msg.delete()
				await ctx.send(lan2, delete_after=10.0)

		bombs = columns * rows - 1
		bombs = bombs / 2.5
		bombs = round(random.randint(5, round(bombs)))

		columns = int(columns)
		rows = int(rows)
		bombs = int(bombs)

		grid = [[0 for num in range(columns)] for num in range(rows)]

		loop_count = 0
		while loop_count < bombs:
			x = random.randint(0, columns - 1)
			y = random.randint(0, rows - 1)

			if grid[y][x] == 0:
				grid[y][x] = 'B'
				loop_count = loop_count + 1

			if grid[y][x] == 'B':
				pass

		pos_x = 0
		pos_y = 0
		while pos_x * pos_y < columns * rows and pos_y < rows:

			adj_sum = 0

			for (adj_y, adj_x) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:

				try:
					if grid[adj_y + pos_y][adj_x + pos_x] == 'B' and adj_y + pos_y > -1 and adj_x + pos_x > -1:
						adj_sum = adj_sum + 1
				except Exception:
					pass

			if grid[pos_y][pos_x] != 'B':
				grid[pos_y][pos_x] = adj_sum

			if pos_x == columns - 1:
				pos_x = 0
				pos_y = pos_y + 1
			else:
				pos_x = pos_x + 1

		not_final = []

		for the_rows in grid:
			not_final.append(''.join(map(str, the_rows)))

		not_final = '\n'.join(not_final)

		not_final = not_final.replace('0', '||:zero:||')
		not_final = not_final.replace('1', '||:one:||')
		not_final = not_final.replace('2', '||:two:||')
		not_final = not_final.replace('3', '||:three:||')
		not_final = not_final.replace('4', '||:four:||')
		not_final = not_final.replace('5', '||:five:||')
		not_final = not_final.replace('6', '||:six:||')
		not_final = not_final.replace('7', '||:seven:||')
		not_final = not_final.replace('8', '||:eight:||')
		final = not_final.replace('B', '||:bomb:||')

		percentage = columns * rows
		percentage = bombs / percentage
		percentage = 100 * percentage
		percentage = round(percentage, 2)

		emb = discord.Embed(
			description=final,
			color=0xC0C0C0
		)
		emb.add_field(
			name=lan3,
			value=columns,
			inline=True
		)
		emb.add_field(
			name=lan4,
			value=rows,
			inline=True
		)
		emb.add_field(
			name=lan5,
			value=columns * rows,
			inline=True
		)
		emb.add_field(
			name=lan6,
			value=bombs,
			inline=True
		)
		await msg.edit(embed=emb, content=None)

	@commands.command(aliases = ['шар'])
	async def ball(self, ctx):
		answers = [
			"Несомненно!",
			"Можете быть уверены!",
			"Сомневаюсь в этом...",
			"Спроси позже... "
		]

		embed = discord.Embed(
			title = "🔮 Магический шар 🧙‍♀️",
			description = random.choice(answers),
			color = 0xf5ce42
		)

		await ctx.send(embed = embed)

	@commands.command(aliases = ['кость'])
	async def dice(self, ctx, dicepar1: int = None, dicepar2: int = None):
		for x in range(dicepar1):
			itog = random.randint(1, dicepar2)
		await ctx.send(f'```#{itog}, dice{dicepar1} [{dicepar2} - {itog}]```')


	@commands.command(aliases = ['рр'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	@commands.has_guild_permissions(manage_messages=True)
	async def rr(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Вы не находитесь в каком либо голосовом канале!'
			lan2 = "БУМ"
			lan3 = "словил пулю..."
		else:
			lan1 = 'You are not in any voice channel!'
			lan2 ="BOOM"
			lan3 = "caught a bullet..."
		try:
			channel = ctx.message.author.voice.channel
		except:
			return await ctx.send(lan1)
		
		await ctx.message.delete()
		message = await ctx.send("``3``")
		await asyncio.sleep(0.5)
		await message.edit(content="``2``")
		await asyncio.sleep(0.5)
		await message.edit(content="``1``")
		await asyncio.sleep(0.5)
		dead = random.choice(channel.members)
		await message.edit(content=lan2)
		await asyncio.sleep(0.5)
		await dead.move_to(None)
		await message.edit(content=None, embed=discord.Embed(description=f'{dead.mention} {lan3}'))

	@commands.command()
	async def crash(self, ctx, bet: int = None, coef: int = None):
		if bet is None:
			await ctx.send(f"{ctx.author.name}, Укажи сумму!")

		elif coef is None:
			await ctx.send(f"{ctx.author.name}, Укажи коэффициент!")

		elif coef <= 1:
			await ctx.send(f"{ctx.author.name}, Коэффициент должен быть выше 1x!")

		else:
			for row in await self.db.users.find({"ids": ctx.author.id, "server_id": ctx.guild.id}):
				cash = row["cash"]
				if cash < bet:
					await ctx.send(f"{ctx.author.name}, У тебя недостаточно денег!")

				else:
					# ограничение по беттингу (10/100000)
					if bet < 10:
						await ctx.send("Минимальная ставка 10 монет!")
					elif bet > 100000:
						await ctx.send("Максимальная ставка 100000 монет!")

					else:
				#Для генерации результата в режиме Crash требуется 1 случайное число в интервале (0..1), 
				#которое затем переводится в коэффициент Crash, имеющий экспоненциальное распределение,
				#по следующему алгоритму.
						number = random.uniform(0, 1)
						crashOutcome = 1000000 / (math.floor(number * 1000000) + 1) * (1 - 0.05)

				#Иногда может выпасть число по типу 0.99 или меньше, в самой игре такого нет,
				#этот IF спасает от таких ситуации.
						if crashOutcome <= 1:
							crashOutcome = 1.00
			
				#если коэф пользователя выше или равен крашу, то он выиграл
						if crashOutcome >= coef:
							roundWinCash = round(bet * coef - bet)
							await ctx.send(content= ctx.author.mention, embed = discord.Embed(title="📈 Сломанный Краш", description=f"{ctx.author.name}, ты выиграл: **+{round(roundWinCash)} :dollar:**\n\nКоэф: **{round(crashOutcome, 2)}**\nТы поставил на коэф: **{round(coef,2)}**\nТвоя ставка: **{bet}**"))

							await self.db.users.update({"ids": ctx.author.id, "server_id": ctx.guild.id}, {"$inc": {"cash": roundWinCash}})
					#Тут уже входит в силу ваша база данных.
					#переменная roundWinCash, это выигрыш пользователя.

				#или проиграл :(
						else:
	   						await ctx.send(content= ctx.author.mention, embed = discord.Embed(title="📈 Сломанный Краш", description=f"{ctx.author.name}, ты проиграл: **{bet} :dollar:**\n\nКоэф: **{round(crashOutcome, 2)}**\nТы поставил на коэф: **{round(coef,2)}**\nТвоя ставка: **{bet}**"))
							await self.db.users.update({"ids": ctx.author.id, "server_id": ctx.guild.id}, {"$inc": {"cash": -bet}})

					#Тут уже входит в силу ваша база данных.
					#тут вы должны снять с баланса пользователя его ставку

def setup(client):
	client.add_cog(game(client))
