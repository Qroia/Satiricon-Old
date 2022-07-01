import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import random

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient('')["server"]

	@commands.command(aliases = ['в_инвентарь'])
	async def v_inv(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		if str(ctx.guild.region) == 'russia':
			lan1 = 'ВиТуберы пользователя'
			lan2 = 'Чтобы узнать подробнее о ВиТубере, воспользуйтесь командой'
			collection1 = self.db["vtubers"]
		else:
			lan1 = 'VTubers User'
			lan2 = 'To learn more about VTuber, use the command'
			collection1 = self.db["vtubersen"]
		for s in await self.db.globaluser.find({"ids": member.id}):
			emb = discord.Embed(title = f"{lan1} {member.name}", description = lan2 + " `v_info {id}`")
			emb.add_field(name = "Chests and Balance", value = f"""
			{s['membercash']} <:coins:781555325483483146>

			{s['vchest']['lowchest']} <:lowchest:781554950223822870>
			{s['vchest']['bigchest']} <:bigchest:781555301588926494>
			{s['vchest']['maxchest']} <:maxchest:781555315891634186>
			""")
			for x in await self.db.globaluser.find({"ids": member.id}):
				allo = 0
				for y in x['idv']:
					for z in await collection1.find({"_id": int(x['idv'][int(allo)])}):
						allo += 1
						emb.add_field(name = f"{z['name']}[ID:{z['_id']}]", value = f"Rang: {z['info']['rang']}")

		await ctx.send(embed = emb)

	@commands.command(aliases = ['в_инфо'])
	async def v_info(self, ctx, idvt: int):
		if str(ctx.guild.region) == 'russia':
			collection1 = self.db["vtubers"]
		else:
			collection1 = self.db["vtubersen"]
		for x in await collection1.find({"_id": idvt}):
			emb = discord.Embed(title = x['name'], description = x['info']['description'])
			emb.add_field(name = 'Damage', value = f"{x['info']['damage'][0]}-{x['info']['damage'][1]}")
			emb.add_field(name = 'HP', value = x['info']['hp'])
			emb.add_field(name = 'Weapon', value = x['info']['weapon'])
			emb.add_field(name = 'Rang', value = x['info']['rang'])
			emb.set_image(url = x['img'])
			await ctx.send(embed = emb)

	@commands.command(aliases = ['в_битва'])
	async def v_battle(self, ctx, ids: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = "Вы не выбрали витубера"
			lan2 = 'У вас ещё нет ниодного витубера! Вы можете получить их с помощью команды $vgetfree'
			lan3 = 'проиграла'
			lan4 = '**Ваш противник**'
			lan5 = 'Победила'
			lan6 = 'Вы получили'
			lan7 = 'Ничья'
			lan8 = 'Противник'
			lan9 = 'У вас нет такого витубера!'
			lan10 = 'Вы получили'
		else:
			lan1 = "You didn't choose vtuber"
			lan2 = 'You have no idea of itubera! You can get them using the $vgetfree command'
			lan3 = 'lost'
			lan4 = '**Your opponent**'
			lan5 = 'Won'
			lan6 = 'You got'
			lan7 = 'Draw'
			lan8 = 'Opponent'
			lan9 = 'you dont Have such a vtuber!'
			lan10 = 'You get'
		if ids is None:
			await ctx.send(lan1)
		elif len(self.db.globaluser.find_one({"ids": ctx.author.id})["idv"]) == 0:
			emb = discord.Embed(title='Error', description=lan2)
			await ctx.send(embed=emb)
		else:
			vran = random.randint(1, 11)
			if str(ctx.guild.region) == 'russia':
				connect = self.db.vtubers.find({"_id": vran})
				connect1 = self.db.vtubers.find({"_id": ids})
			else:
				connect = self.db.vtubersen.find({"_id": vran})
				connect1 = self.db.vtubersen.find({"_id": ids})
			for vtb in await connect:
				for x in await self.db.globaluser.find({"ids": ctx.author.id}):
					idv_list = x["idv"]
					if str(ids) in idv_list:
						for vts in await connect1:
							rang = vtb["info"]["rang"]
							if rang == 'C':
								chance = 35
								minval = 1
								maxval = 7
							elif rang == 'B':
								chance = 16
								minval = 10
								maxval = 18
							elif rang == 'A':
								chance = 8
								minval = 7
								maxval = 30
							elif rang == 'S':
								chance = 6
								minval = 25
								maxval = 40
							elif rang == 'SS':
								chance = 3
								minval = 37
								maxval = 54
							elif rang == 'SSS':
								chance = 1
								minval = 70
								maxval = 100
							flag=True
							vhpuser = vts["info"]["hp"]
							vhpunit = vtb["info"]["hp"]
							while flag:
								vdamageuser = random.randint(vts["info"]["damage"][0], vts["info"]["damage"][1])
								vdamageunit = random.randint(vtb["info"]["damage"][0], vtb["info"]["damage"][1])
								vhpuser = vhpuser - vdamageunit
								vhpunit = vhpunit - vdamageuser

								if vhpuser > 0 and vhpunit > 0:
									flag = True

								elif vhpuser < 0 and vhpunit > 0:
									emb = discord.Embed(title = f'{vts["name"]} {lan3}', description = vts["lose"]["1"])
									emb.add_field(value=vtb["name"], name=lan4, inline=False)
									await ctx.send(embed=emb)
									flag = False

								elif vhpuser > 0 and vhpunit < 0:
									getchance = random.randint(1, 100)
									winwords = random.randint(1, 2)
									emb = discord.Embed(title = f'{lan5} {vts["name"]}', description = vts["win"][str(winwords)], color=0xa4e8ed)
									emb.set_image(url= vts["img"])

									if getchance in range(0, chance) and str(vran) not in idv_list:
										emb.add_field(value=vtb["name"], name=lan6, inline = True)
										await self.db.globaluser.update({"ids": ctx.author.id}, {"$push": {"idv": str(vran)}})

									addmoney = random.randint(minval, maxval)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": addmoney}})

									emb.add_field(name = lan10, value = addmoney)
									emb.add_field(value=vtb["name"], name=lan4, inline=True)
									await ctx.send(embed=emb)
									flag = False

								elif vhpuser < 0 and vhpunit < 0:
									emb = discord.Embed(title =lan7, description = f'{lan8}: {vtb["name"]}')
									await ctx.send(embed=emb)
									flag = False

					else:
						await ctx.send(lan9)

	@commands.command(aliases = ['в_получить'])
	async def v_getfree(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'У вас уже есть хотя бы 1 VTuber'
			lan2 = 'Вы успешно получили своего первого Витубера'
		else:
			lan1 = 'You already have at least 1 VTuber'
			lan2 = 'You have successfully got your first Vtuber'
		if len(self.db.globaluser.find({"ids": ctx.author.id})["idv"]) > 0:
			emb = discord.Embed(title="Error", description=lan1)
			await ctx.send(embed = emb)
		else:
			ran = random.randint(1, 11)
			await self.db.globaluser.update({"ids": ctx.author.id}, {"$push": {"idv": str(ran)}})
			for row in self.db.vtubers.find({"_id": ran}):
				emb = discord.Embed(title=lan2, description=row["info"]["description"])
				emb.set_image(url=row["img"])

				await ctx.send(embed=emb)

	@commands.command(aliases = ['в_открыть'])
	async def v_open(self, ctx, chest: str):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Награда:'
			lan2 = 'Вы открыли сундук'
			lan3 = 'У вас недостаточно сундуков'
		else:
			lan1 = 'Reward:'
			lan2 = 'You opened the chest'
			lan3 = 'You dont have enough chests'
		if chest == 'lowchest':

			for x in await self.db.globaluser.find({"ids": ctx.author.id}):
				if x['vchest']['lowchest'] > 0:
					lowchest1 = x['vchest']['lowchest'] - 1
					bigchest1 = x['vchest']['bigchest']
					maxchest1 = x['vchest']['maxchest']
					await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$set": {"vchest": {"lowchest": lowchest1, "bigchest": bigchest1, "maxchest": maxchest1}}})
					select = random.randint(1, 100)
					emb = discord.Embed(title = lan2)

					if select in range(1, 20): #C

						list_all = [9]
						flag = True
						check = 0
						while flag:
							for s in await self.db.globaluser.find({"ids": ctx.author.id}):
								if len(list_all) > len(s['idv']):
									ads = random.randint(40, 62)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
									emb.add_field(name = lan1, value = f'{ads} <:coins:781555325483483146>')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) not in s["idv"]:
									get_tuber = list_all[check]
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$push": {"idv": str(get_tuber)}})
									for y in self.db.vtubers.find({"_id": get_tuber}):
										emb.add_field(name = lan1, value = f'{y["name"]}')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) in s["idv"]:
									check += 1
									flag = True

					elif select in range(20, 30): #B

						list_all = [5]
						flag = True
						check = 0
						while flag:
							for s in self.db.globaluser.find({"ids": ctx.author.id}):
								if len(list_all) > len(s['idv']):
									ads = random.randint(54, 92)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
									emb.add_field(name = lan1, value = f'{ads} <:coins:781555325483483146>')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) not in s["idv"]:
									get_tuber = list_all[check]
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$push": {"idv": str(get_tuber)}})
									for y in self.db.vtubers.find({"_id": get_tuber}):
										emb.add_field(name = lan1, value = f'{y["name"]}')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) in s["idv"]:
									check += 1
									flag = True

					elif select in range(30, 35): #A

						list_all = [1, 8, 10]
						flag = True
						check = 0
						while flag:
							for s in await self.db.globaluser.find({"ids": ctx.author.id}):
								if len(list_all) > len(s['idv']):
									ads = random.randint(140, 172)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
									emb.add_field(name = lan1, value = f'{ads} <:coins:781555325483483146>')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) not in s["idv"]:
									get_tuber = list_all[check]
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$push": {"idv": str(get_tuber)}})
									for y in await self.db.vtubers.find({"_id": get_tuber}):
										emb.add_field(name = lan1, value = f'{y["name"]}')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) in s["idv"]:
									check += 1
									flag = True
						
					else:
						ads = random.randint(20, 40)
						await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
						emb.add_field(name = lan1, value = f'{ads} <:coins:781555325483483146>')
						await ctx.send(embed = emb)
				else:
					await ctx.send(lan3)

		elif chest == 'bigchest':
			
			for x in await self.db.globaluser.find({"ids": ctx.author.id}):
				if x['vchest']['bigchest'] > 0:
					lowchest1 = x['vchest']['lowchest']
					bigchest1 = x['vchest']['bigchest'] - 1
					maxchest1 = x['vchest']['maxchest']
					await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$set": {"vchest": {"lowchest": lowchest1, "bigchest": bigchest1, "maxchest": maxchest1}}})
					select = random.randint(1, 100)
					emb = discord.Embed(title = lan2)

					if select in range(1, 15): #A

						list_all = [1, 8, 10]
						flag = True
						check = 0
						while flag:
							for s in await self.db.globaluser.find({"ids": ctx.author.id}):
								if len(list_all) > len(s['idv']):
									ads = random.randint(124, 143)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
									emb.add_field(name = lan2, value = f'{ads} <:coins:781555325483483146>')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) not in s["idv"]:
									get_tuber = list_all[check]
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$push": {"idv": str(get_tuber)}})
									for y in await self.db.vtubers.find({"_id": get_tuber}):
										emb.add_field(name = lan2, value = f'{y["name"]}')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) in s["idv"]:
									check += 1
									flag = True

					elif select in range(20, 27): #S

						list_all = [2, 6]
						flag = True
						check = 0
						while flag:
							for s in await self.db.globaluser.find({"ids": ctx.author.id}):
								if len(list_all) > len(s['idv']):
									ads = random.randint(183, 213)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
									emb.add_field(name = lan2, value = f'{ads} <:coins:781555325483483146>')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) not in s["idv"]:
									get_tuber = list_all[check]
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$push": {"idv": str(get_tuber)}})
									for y in await self.db.vtubers.find({"_id": get_tuber}):
										emb.add_field(name = lan2, value = f'{y["name"]}')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) in s["idv"]:
									check += 1
									flag = True

					elif select in range(30, 32): #SS

						list_all = [4, 7, 11]
						flag = True
						check = 0
						while flag:
							for s in await self.db.globaluser.find({"ids": ctx.author.id}):
								if len(list_all) > len(s['idv']):
									ads = random.randint(210, 264)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
									emb.add_field(name = lan2, value = f'{ads} <:coins:781555325483483146>')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) not in s["idv"]:
									get_tuber = list_all[check]
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$push": {"idv": str(get_tuber)}})
									for y in await self.db.vtubers.find({"_id": get_tuber}):
										emb.add_field(name = lan2, value = f'{y["name"]}')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) in s["idv"]:
									check += 1
									flag = True
						
					else:
						ads = random.randint(150, 175)
						await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
						emb.add_field(name = lan2, value = f'{ads} <:coins:781555325483483146>')
						await ctx.send(embed = emb)
				else:
					await ctx.send(lan3)

		elif chest == 'maxchest':

			for x in await self.db.globaluser.find({"ids": ctx.author.id}):
				if x['vchest']['maxchest'] > 0:
					lowchest1 = x['vchest']['lowchest']
					bigchest1 = x['vchest']['bigchest']
					maxchest1 = x['vchest']['maxchest'] - 1
					await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$set": {"vchest": {"lowchest": lowchest1, "bigchest": bigchest1, "maxchest": maxchest1}}})
					select = random.randint(1, 100)
					emb = discord.Embed(title = lan1)

					if select in range(1, 20): #S

						list_all = [2, 6]
						flag = True
						check = 0
						while flag:
							for s in await self.db.globaluser.find({"ids": ctx.author.id}):
								if len(list_all) > len(s['idv']):
									ads = random.randint(275, 326)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
									emb.add_field(name = lan2, value = f'{ads} <:coins:781555325483483146>')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) not in s["idv"]:
									get_tuber = list_all[check]
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$push": {"idv": str(get_tuber)}})
									for y in await self.db.vtubers.find({"_id": get_tuber}):
										emb.add_field(name = lan2, value = f'{y["name"]}')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) in s["idv"]:
									check += 1
									flag = True

					elif select in range(20, 30): #SS

						list_all = [4, 7, 11]
						flag = True
						check = 0
						while flag:
							for s in await self.db.globaluser.find({"ids": ctx.author.id}):
								if len(list_all) > len(s['idv']):
									ads = random.randint(342, 380)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
									emb.add_field(name = lan2, value = f'{ads} <:coins:781555325483483146>')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) not in s["idv"]:
									get_tuber = list_all[check]
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$push": {"idv": str(get_tuber)}})
									for y in await self.db.vtubers.find({"_id": get_tuber}):
										emb.add_field(name = lan2, value = f'{y["name"]}')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) in s["idv"]:
									check += 1
									flag = True

					elif select in range(30, 35): #SSS

						list_all = [3]
						flag = True
						check = 0
						while flag:
							for s in await self.db.globaluser.find({"ids": ctx.author.id}):
								if len(list_all) > len(s['idv']):
									ads = random.randint(500, 700)
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
									emb.add_field(name = lan2, value = f'{ads} <:coins:781555325483483146>')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) not in s["idv"]:
									get_tuber = list_all[check]
									await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$push": {"idv": str(get_tuber)}})
									for y in await self.db.vtubers.find({"_id": get_tuber}):
										emb.add_field(name = lan2, value = f'{y["name"]}')
									await ctx.send(embed = emb)
									flag = False
								elif str(list_all[check]) in s["idv"]:
									check += 1
									flag = True
						
					else:
						ads = random.randint(350, 400)
						await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": ads}})
						emb.add_field(name = lan2, value = f'{ads} <:coins:781555325483483146>')
						await ctx.send(embed = emb)
				else:
					await ctx.send(lan3)

	@commands.command(aliases = ['в_магазин'])
	async def v_shop(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Магазин'
			lan2 = 'Маленький сундук'
			lan3 = 'Средний сундук'
			lan4 = 'Большой сундук'
			lan5 = 'У вас есть'
		else:
			lan1 = 'Shop'
			lan2 = 'Small chest'
			lan3 = 'Medium chest'
			lan4 = 'Big chest'
			lan5 = 'You have'
		for x in await self.db.globaluser.find({"ids": ctx.author.id}):
			emb = discord.Embed(title = f'{lan1} VTubers', description = f'{lan5} {x["membercash"]} <:coins:781555325483483146>')
		emb.add_field(name = f'{lan2} <:lowchest:781554950223822870>', value = '500 <:coins:781555325483483146>')
		emb.add_field(name = f'{lan3} сундук <:bigchest:781555301588926494>', value = '1000 <:coins:781555325483483146>')
		emb.add_field(name = f'{lan4} <:maxchest:781555315891634186>', value = '2000 <:coins:781555325483483146>')
		await ctx.send(embed = emb)

	@commands.command(aliases = ['в_купить'])
	async def v_buy(self, ctx, chest: str):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Успешно куплено'
			lan2 = 'маленький сундук'
			lan3 = 'средний сундук'
			lan4 = 'большой сундук'
			lan6 = 'Вы получили'
			lan7 = 'У вас недостаточно денег'
		else:
			lan1 = 'Successfully purchased'
			lan2 = 'Small chest'
			lan3 = 'Medium chest'
			lan4 = 'Big chest'
			lan6 = 'Ylan7t have enough money'
		if chest == 'lowchest':

			for x in await self.db.globaluser.find({"ids": ctx.author.id}):
				if x['membercash'] > 500:
					await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": -500}})
					lowchest1 = x['vchest']['lowchest'] + 1
					bigchest1 = x['vchest']['bigchest']
					maxchest1 = x['vchest']['maxchest']
					await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$set": {"vchest": {"lowchest": lowchest1, "bigchest": bigchest1, "maxchest": maxchest1}}})
					emb = discord.Embed(title = lan1, description = f'{lan6} 1 {lan2}')
					await ctx.send(embed = emb)
				else:
					await ctx.send(lan7)

		elif chest == 'bigchest':
			
			for x in await self.db.globaluser.find({"ids": ctx.author.id}):
				if x['membercash'] > 1000:
					await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": -1000}})
					lowchest1 = x['vchest']['lowchest']
					bigchest1 = x['vchest']['bigchest'] + 1
					maxchest1 = x['vchest']['maxchest']
					await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$set": {"vchest": {"lowchest": lowchest1, "bigchest": bigchest1, "maxchest": maxchest1}}})
					emb = discord.Embed(title = lan1, description = f'{lan6} 1 {lan3}')
					await ctx.send(embed = emb)
				else:
					await ctx.send(lan7)
		
		elif chest == 'maxchest':
			
			for x in await self.db.globaluser.find({"ids": ctx.author.id}):
				if x['membercash'] > 2000:
					await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$inc": {"membercash": -2000}})
					lowchest1 = x['vchest']['lowchest']
					bigchest1 = x['vchest']['bigchest']
					maxchest1 = x['vchest']['maxchest'] + 1
					await self.db.globaluser.update_one({"ids": ctx.author.id}, {"$set": {"vchest": {"lowchest": lowchest1, "bigchest": bigchest1, "maxchest": maxchest1}}})
					emb = discord.Embed(title = lan1, description = f'{lan6} 1 {lan4}')
					await ctx.send(embed = emb)
				else:
					await ctx.send(lan7)

def setup(client):
	client.add_cog(User(client))
