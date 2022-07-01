import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import random
import asyncio
import string

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.command(aliases = ['создать_данж'])
	@commands.has_permissions(administrator = True)
	async def createdange(self, ctx, namedun: str = None, unith: int = None, money: int = None, minmoney: int = None, exp: int = None, minexp: int = None):
		if ctx.guild.region == 'russia':
			lan1 = 'Вы неправильно используете команду. Прочтите документацию'
			lan2 = 'Данж создан!'
			lan3 = 'Вы создали максимальное количество данжей'
		else:
			lan1 = 'You are using the command incorrectly. Read the documentation'
			lan2 = 'Dungeon created!'
			lan3 = 'You have created the maximum number of dungeons'
		if namedun is None or unith is None or minmoney > money or minexp > exp or unith == 0:
			await ctx.send(lan1)
		else:
			ohmygod = random.randint(22, 23)
			def buildblock(size):
				return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
			indificator = buildblock(ohmygod) #Создаём рандомный 23-значный индефикатор данжа
			if unith in range(1, 4):
				## vdange - Номер данжа
				## getunit - Количество использованных юнитов
				## unit - Количество доступных юнитов для этого данжа
				## indificator - ID данжа для глубокого использования
				## name - Название Данжа
				## cash - Максимальное количество выигрышных денег
				## mincash - Минимальное количество выигрышных денег
				## exp - Максимальное количество выигрышного опыта
				## minexp - Минимальное количество выигранного опыта
				## server_id - ID гильдии к которому привязан данж
				if self.db.dange.count_documents({"server_id": ctx.guild.id}) == 0:
					await ctx.send(lan2)
					self.db.dange.insert_one({
						"vdange": 1,
						"getunit": 0,
						"unit": unith,
						"indificator": indificator,
						"name": str(namedun),
						"cash": money,
						"mincash": minmoney,
						"exp": exp,
						"minexp": minexp,
						"server_id": ctx.guild.id
						})
				elif self.db.dange.count_documents({"server_id": ctx.guild.id}) == 1:
					await ctx.send(lan2)
					self.db.dange.insert_one({
						"vdange": 2,
						"getunit": 0,
						"unit": unith,
						"indificator": indificator,
						"name": namedun,
						"cash": money,
						"mincash": minmoney,
						"exp": exp,
						"minexp": minexp,
						"server_id": ctx.guild.id
						})
				elif self.db.dange.count_documents({"server_id": ctx.guild.id}) == 2:
					await ctx.send(lan2)
					self.db.dange.insert_one({
						"vdange": 3,
						"getunit": 0,
						"unit": unith,
						"indificator": indificator,
						"name": namedun,
						"cash": money,
						"mincash": minmoney,
						"exp": exp,
						"minexp": minexp,
						"server_id": ctx.guild.id
						})
				elif self.db.dange.count_documents({"server_id": ctx.guild.id}) == 3:
					await ctx.send(lan3)

	@commands.command(aliases = ['данж'])
	@commands.cooldown(1, 25, commands.BucketType.user)
	async def dange(self, ctx, numberdun: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1  = 'На этом сервере нет дыр, для входа в данж'
			lan2  = 'Этот данж ещё не настроен'
			lan3  = 'Информация о бое'
			lan4  = 'Вы победили'
			lan5  = 'У вас осталось'
			lan6  = 'хп'
			lan7  = 'В'
			lan8  = 'побеждён'
			lan9  = 'Ваше вознаграждение'
			lan10 = 'Монеты'
			lan11 = 'Опыт'
			lan12 = 'Вы проиграли'
			lan13 = 'осталось'
			lan14 = 'Ничья'
			lan15 = 'Вы были оба повержены'
			lan16 = 'У'
		else:
			lan1  = 'There are no holes on this server to enter the dungeon'
			lan2  = 'This dungeon is not configured yet'
			lan3  = 'Battle information'
			lan4  = 'You won'
			lan5  = 'You have left'
			lan6  = 'HP'
			lan7  = 'In'
			lan8  = 'defeated'
			lan9  = 'Your reward'
			lan10 = 'Coins'
			lan11 = 'Experience'
			lan12 = 'You lost'
			lan13 = 'left'
			lan14 = 'Draw'
			lan15 = 'You were both defeated'
			lan16 = 'he'
		if self.db.dange.count_documents({"server_id": ctx.guild.id}) == 0:
			await ctx.send(lan1)
		else:
			for y in self.db.dange.find({"server_id": ctx.guild.id, "vdange": numberdun}):
				x = y["unit"]
				z = y["getunit"]
				s = y["indificator"]
				for o in self.db.unit.find({"vid": 1, "indificator": s}):
					if x == 1:
						if z < 1:
							await ctx.send(lan2)
						else:
							dunname       = y["name"]
							minunithp     = o["minhp"]
							unithp        = o["hp"]
							unitmaxdamage = o["damage"]
							unitmindamage = o["mindamage"]
							connectio = self.db.users.find({"server_id": ctx.guild.id, "ids": ctx.author.id})
							for row in connectio:
								unithp    = random.randint(minunithp, unithp)
								maxattack = row["maxattack"]
								minattack = row["minattack"]
								hp        = row["hp"]
								minmoney  = y["mincash"]
								maxmoney  = y["cash"]
								minexp    = y["minexp"]
								maxexp    = y["exp"]
								unitname  = o["name"]
								prize0    = row["cash"]
								prize01   = row["exp"]
								flag      = True
								while flag:									
									unitattack = random.randint(unitmindamage, unitmaxdamage)
									userattack = random.randint(minattack, maxattack)
									hp         = hp - unitattack
									unithp     = unithp - userattack
									if hp > 0 and unithp < 0:
										prize1 = random.randint(minmoney, maxmoney)
										prize2 = random.randint(minexp, maxexp)
										embed  = discord.Embed(title=lan3, color=discord.Color.green())
										embed.add_field(name=lan4, value=f'''
								{lan5}: {hp} {lan6}
								{lan7} {dunname} {lan8} {unitname}
								{lan9}: \n{lan10}: {prize1}\n {lan11}: {prize2}
								''', inline=False)
										prize13 = prize1 + prize0
										prize23 = prize2 + prize01
										self.db.users.update_one({"ids": ctx.author.id, "server_id": ctx.guild.id}, { "$set": {"cash": prize13, "exp": prize23}})
										await ctx.send(embed=embed)
										flag = False
									elif hp < 0 and unithp > 0:
										embed = discord.Embed(title=lan3, color=discord.Color.red())
										embed.add_field(name=lan12, value=f'{lan16} {unitname} {lan13} {unithp} {lan6}', inline=False)
										await ctx.send(embed=embed)
										flag = False
									elif hp < 0 and unithp < 0:
										embed = discord.Embed(title=lan3)
										embed.add_field(name=lan14, value=lan15, inline=False)
										await ctx.send(embed=embed)
										flag = False
									elif hp > 0 and unithp > 0:
										flag = True
					elif x == 2:
						if z < 2:
							await ctx.send(lan2)
						else:
							for unit2 in self.db.unit.find({"vid": 2, "indificator": s}):
								dunname        = y["name"]
								unitname      = 0
								minunithp     = 0
								unithp        = 0
								unitmindamage = 0
								unitmaxdamage = 0
								unitselect    = random.randint(1, 100)
								def unitselecto():
									nonlocal minunithp, unithp, unitmaxdamage, unitmindamage, unitname
									if unitselect in range(1, 51):
										unitname      = o["name"]
										minunithp     = o["minhp"]
										unithp        = o["hp"]
										unitmaxdamage = o["damage"]
										unitmindamage = o["mindamage"]
									elif unitselect in range(52, 100):
										unitname      = unit2["name"]
										minunithp     = unit2["minhp"]
										unithp        = unit2["hp"]
										unitmaxdamage = unit2["damage"]
										unitmindamage = unit2["mindamage"]
								unitselecto()
								connectio = self.db.users.find({"server_id": ctx.guild.id, "ids": ctx.author.id})
								for row in connectio:
									unithp    = random.randint(minunithp, unithp)
									maxattack = row["maxattack"]
									minattack = row["minattack"]
									hp        = row["hp"]
									minmoney  = y["mincash"]
									maxmoney  = y["cash"]
									minexp    = y["minexp"]
									maxexp    = y["exp"]
									prize0    = row["cash"]
									prize01   = row["exp"]
									flag      = True
									while flag:									
										unitattack = random.randint(unitmindamage, unitmaxdamage)
										userattack = random.randint(minattack, maxattack)
										hp         = hp - unitattack
										unithp     = unithp - userattack
										if hp > 0 and unithp < 0:
											prize1 = random.randint(minmoney, maxmoney)
											prize2 = random.randint(minexp, maxexp)
											embed  = discord.Embed(title=lan3, color=discord.Color.green())
											embed.add_field(name=lan4, value=f'''
									{lan5}: {hp} {lan6}
									{lan7} {dunname} {lan8} {unitname}
									{lan9}: \n{lan10}: {prize1}\n {lan11}: {prize2}
									''', inline=False)
											prize13 = prize1 + prize0
											prize23 = prize2 + prize01
											self.db.users.update_one({"ids": ctx.author.id, "server_id": ctx.guild.id}, { "$set": {"cash": prize13, "exp": prize23}})
											await ctx.send(embed=embed)
											flag = False
										elif hp < 0 and unithp > 0:
											embed = discord.Embed(title=lan3, color=discord.Color.red())
											embed.add_field(name=lan12, value=f'{lan16} {unitname} {lan13} {unithp} {lan6}', inline=False)
											await ctx.send(embed=embed)
											flag = False
										elif hp < 0 and unithp < 0:
											embed = discord.Embed(title=lan3)
											embed.add_field(name=lan14, value=lan15, inline=False)
											await ctx.send(embed=embed)
											flag = False
										elif hp > 0 and unithp > 0:
											flag = True
					elif x == 3:
						if z < 3:
							await ctx.send(lan2)
						else:
							for unit2 in self.db.unit.find({"vid": 2, "indificator": s}):
								for unit3 in self.db.unit.find({"vid": 3, "indificator": s}):
									dunname       = y["name"]
									unitname      = 0
									minunithp     = 0
									unithp        = 0
									unitmindamage = 0
									unitmaxdamage = 0
									unitselect    = random.randint(1, 100)
									def unitselecto():
										nonlocal minunithp, unithp, unitmaxdamage, unitmindamage, unitname
										if unitselect in range(1, 33):
											unitname      = o["name"]
											minunithp     = o["minhp"]
											unithp        = o["hp"]
											unitmaxdamage = o["damage"]
											unitmindamage = o["mindamage"]
										elif unitselect in range(34, 65):
											unitname      = unit2["name"]
											minunithp     = unit2["minhp"]
											unithp        = unit2["hp"]
											unitmaxdamage = unit2["damage"]
											unitmindamage = unit2["mindamage"]
										elif unitselect in range(65, 100):
											unitname      = unit3["name"]
											minunithp     = unit3["minhp"]
											unithp        = unit3["hp"]
											unitmaxdamage = unit3["damage"]
											unitmindamage = unit3["mindamage"]
									unitselecto()
									connectio = self.db.users.find({"server_id": ctx.guild.id, "ids": ctx.author.id})
									for row in connectio:
										hp   = random.randint(minunithp, unithp)
										flag = True
										while flag:
											unithp    = random.randint(minunithp, unithp)
											maxattack = row["maxattack"]
											minattack = row["minattack"]
											hp        = row["hp"]
											minmoney  = y["mincash"]
											maxmoney  = y["cash"]
											minexp    = y["minexp"]
											maxexp    = y["exp"]
											prize0    = row["cash"]
											prize01   = row["exp"]
											flag      = True
											while flag:									
												unitattack = random.randint(unitmindamage, unitmaxdamage)
												userattack = random.randint(minattack, maxattack)
												hp         = hp - unitattack
												unithp     = unithp - userattack
												if hp > 0 and unithp < 0:
													prize1 = random.randint(minmoney, maxmoney)
													prize2 = random.randint(minexp, maxexp)
													embed  = discord.Embed(title=lan3, color=discord.Color.green())
													embed.add_field(name=lan4, value=f'''
										{lan5}: {hp} {lan6}
										{lan7} {dunname} {lan8} {unitname}
										{lan9}: \n{lan10}: {prize1}\n {lan11}: {prize2}
										''', inline=False)
													prize13 = prize1 + prize0
													prize23 = prize2 + prize01
													self.db.users.update_one({"ids": ctx.author.id, "server_id": ctx.guild.id}, { "$set": {"cash": prize13, "exp": prize23}})
													await ctx.send(embed=embed)
													flag = False
												elif hp < 0 and unithp > 0:
													embed = discord.Embed(title=lan3, color=discord.Color.red())
													embed.add_field(name=lan12, value=f'{lan16} {unitname} {lan13} {unithp} {lan6}', inline=False)
													await ctx.send(embed=embed)
													flag = False
												elif hp < 0 and unithp < 0:
													embed = discord.Embed(title=lan3)
													embed.add_field(name=lan14, value=lan15, inline=False)
													await ctx.send(embed=embed)
													flag = False
												elif hp > 0 and unithp > 0:
													flag = True
					elif x == 4:
						if z < 4:
							await ctx.send(lan2)
						else:
							for unit2 in self.db.unit.find({"vid": 2, "indificator": s}):
								for unit3 in self.db.unit.find({"vid": 3, "indificator": s}):
									for unit4 in self.db.unit.find({"vid": 4, "indificator": s}):
										dunname       = y["name"]
										unitname      = 0
										minunithp     = 0
										unithp        = 0
										unitmindamage = 0
										unitmaxdamage = 0
										unitselect    = random.randint(1, 100)
										def unitselecto():
											nonlocal minunithp, unithp, unitmaxdamage, unitmindamage, unitname
											if unitselect in range(1, 25):
												unitname      = o["name"]
												minunithp     = o["minhp"]
												unithp        = o["hp"]
												unitmaxdamage = o["damage"]
												unitmindamage = o["mindamage"]
											elif unitselect in range(26, 50):
												unitname      = unit2["name"]
												minunithp     = unit2["minhp"]
												unithp        = unit2["hp"]
												unitmaxdamage = unit2["damage"]
												unitmindamage = unit2["mindamage"]
											elif unitselect in range(51, 75):
												unitname      = unit3["name"]
												minunithp     = unit3["minhp"]
												unithp        = unit3["hp"]
												unitmaxdamage = unit3["damage"]
												unitmindamage = unit3["mindamage"]
											elif unitselect in range(76, 100):
												unitname      = unit3["name"]
												minunithp     = unit4["minhp"]
												unithp        = unit4["hp"]
												unitmaxdamage = unit4["damage"]
												unitmindamage = unit4["mindamage"]
										unitselecto()
										connectio = self.db.users.find({"server_id": ctx.guild.id, "ids": ctx.author.id})
										for row in connectio:
											hp   = random.randint(minunithp, unithp)
											flag = True
											while flag:
												unithp    = random.randint(minunithp, unithp)
												maxattack = row["maxattack"]
												minattack = row["minattack"]
												hp        = row["hp"]
												minmoney  = y["mincash"]
												maxmoney  = y["cash"]
												minexp    = y["minexp"]
												maxexp    = y["exp"]
												prize0    = row["cash"]
												prize01   = row["exp"]
												flag      = True
												while flag:									
													unitattack = random.randint(unitmindamage, unitmaxdamage)
													userattack = random.randint(minattack, maxattack)
													hp         = hp - unitattack
													unithp     = unithp - userattack
													if hp > 0 and unithp < 0:
														prize1 = random.randint(minmoney, maxmoney)
														prize2 = random.randint(minexp, maxexp)
														embed  = discord.Embed(title=lan3, color=discord.Color.green())
														embed.add_field(name=lan4, value=f'''
												{lan5}: {hp} {lan6}
												{lan7} {dunname} {lan8} {unitname}
												{lan9}: \n{lan10}: {prize1}\n {lan11}: {prize2}
												''', inline=False)
														prize13 = prize1 + prize0
														prize23 = prize2 + prize01
														self.db.users.update_one({"ids": ctx.author.id, "server_id": ctx.guild.id}, { "$set": {"cash": prize13, "exp": prize23}})
														await ctx.send(embed=embed)
														flag = False
													elif hp < 0 and unithp > 0:
														embed = discord.Embed(title=lan3, color=discord.Color.red())
														embed.add_field(name=lan12, value=f'{lan16} {unitname} {lan13} {unithp} {lan6}', inline=False)
														await ctx.send(embed=embed)
														flag = False
													elif hp < 0 and unithp < 0:
														embed = discord.Embed(title=lan3)
														embed.add_field(name=lan14, value=lan15, inline=False)
														await ctx.send(embed=embed)
														flag = False
													elif hp > 0 and unithp > 0:
														flag = True


	@commands.command(aliases = ['создать_юнита'])
	@commands.has_permissions(administrator = True)
	async def createunit(self, ctx, numberdun: int = None, name: str = None, damage: int = None, mindamage: int = None, hp: int = None, minhp: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Введите id данжа'
			lan2 = 'Такого данжа нет, или я что-то не понял?'
			lan3 = 'Вы неправильно используете команду. Прочтите документацию'
			lan4 = 'Вы уже создали максимальное количество юнитов в этом данже'
		else:
			lan1 = 'Enter the dungeon id'
			lan2 = 'there is no such dungeon, or did I not understand something?'
			lan3 = 'You are using the command incorrectly. Read the documentation'
			lan4 = 'You have already created the maximum number of units in this dungeon'
		if numberdun is None:
			await ctx.send(lan1)
		elif self.db.dange.count_documents({"vdange": numberdun, "server_id": ctx.guild.id}) is None:
			await ctx.send(lan2)
		elif name is None or damage is None or mindamage is None or hp is None or minhp is None or minhp > hp or mindamage > damage:
			await ctx.send(lan3)
		else:
			for x in self.db.dange.find({"server_id": ctx.guild.id, "vdange": numberdun}):
				unitdown    = x["unit"]
				unitup      = x["getunit"]
				indeficator = str(x["indificator"])
				if unitdown == 1:
					if unitup >= unitdown:
						await ctx.send(lan4)
					else:
						self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
						self.db.unit.insert_one({
							"vid": 1,
							"indificator": indeficator,
							"name": name,
							"minhp": minhp,
							"hp": hp,
							"damage": damage,
							"mindamage": mindamage,
							"server_id": ctx.guild.id
							})
				elif unitdown == 2:
					if unitup >= unitdown:
						await ctx.send(lan4)
					else:
						if unitup == 0:
							self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
							self.db.unit.insert_one({
								"vid": 1,
								"indificator": indeficator,
								"name": name,
								"minhp": minhp,
								"hp": hp,
								"damage": damage,
								"mindamage": mindamage,
								"server_id": ctx.guild.id
								})
						elif unitup == 1:
							self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
							self.db.unit.insert_one({
								"vid": 2,
								"indificator": indeficator,
								"name": name,
								"minhp": minhp,
								"hp": hp,
								"damage": damage,
								"mindamage": mindamage,
								"server_id": ctx.guild.id
								})
				elif unitdown == 3:
					if unitup >= unitdown:
						await ctx.send(lan4)
					else:
						if unitup == 0:
							self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
							self.db.unit.insert_one({
								"vid": 1,
								"indificator": indeficator,
								"name": name,
								"minhp": minhp,
								"hp": hp,
								"damage": damage,
								"mindamage": mindamage,
								"server_id": ctx.guild.id
								})
						elif unitup == 1:
							self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
							self.db.unit.insert_one({
								"vid": 2,
								"indificator": indeficator,
								"name": name,
								"minhp": minhp,
								"hp": hp,
								"damage": damage,
								"mindamage": mindamage,
								"server_id": ctx.guild.id
								})
						elif unitup == 2:
							self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
							self.db.unit.insert_one({
								"vid": 3,
								"indificator": indeficator,
								"name": name,
								"minhp": minhp,
								"hp": hp,
								"damage": damage,
								"mindamage": mindamage,
								"server_id": ctx.guild.id
								})
				elif unitdown == 4:
					if unitup >= unitdown:
						await ctx.send(lan4)
					else:
						if unitup == 0:
							self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
							self.db.unit.insert_one({
								"vid": 1,
								"indificator": indeficator,
								"name": name,
								"minhp": minhp,
								"hp": hp,
								"damage": damage,
								"mindamage": mindamage,
								"server_id": ctx.guild.id
								})
						elif unitup == 1:
							self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
							self.db.unit.insert_one({
								"vid": 2,
								"indificator": indeficator,
								"name": name,
								"minhp": minhp,
								"hp": hp,
								"damage": damage,
								"mindamage": mindamage,
								"server_id": ctx.guild.id
								})
						elif unitup == 2:
							self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
							self.db.unit.insert_one({
								"vid": 3,
								"indificator": indeficator,
								"name": name,
								"minhp": minhp,
								"hp": hp,
								"damage": damage,
								"mindamage": mindamage,
								"server_id": ctx.guild.id
								})
						elif unitup == 3:
							self.db.dange.update_one({"server_id": ctx.guild.id, "vdange": numberdun, "indificator": indeficator}, { "$inc": {"getunit": 1}})
							self.db.unit.insert_one({
								"vid": 4,
								"indificator": indeficator,
								"name": name,
								"minhp": minhp,
								"hp": hp,
								"damage": damage,
								"mindamage": mindamage,
								"server_id": ctx.guild.id
								})

	@commands.command(aliases = ['удалитьданж'])
	@commands.has_permissions(administrator = True)
	async def deletedange(self, ctx, numberdun: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = "Ошибка!"
			lan2 = "Укажите id данжа"
			lan3 = "Удачно!"
			lan4 = "Вы удалили данж и всё его содержимое! Это дыры больше нет"
		else:
			lan1 = "Error!"
			lan2 = "Enter the dungeon id"
			lan3 = "Successful!"
			lan4 = "You deleted the dungeon and all its contents! This hole is no longer there"
		if numberdun is None:
			emb = discord.Embed(title=lan1, description=lan2)
			await ctx.send(embed=emb)
		for row in self.db.dange.find({"vdange": numberdun, "server_id": ctx.guild.id}):
			indificator = row["indificator"]
			self.db.unit.delete_many({"indificator": indificator})
			self.db.dange.delete_one({"vdange": numberdun, "server_id": ctx.guild.id})
			emb = discord.Embed(title=lan3, description=lan4)
			await ctx.send(embed=emb)

def setup(client):
	client.add_cog(User(client))
