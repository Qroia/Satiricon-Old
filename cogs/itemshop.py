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

	@commands.command(aliases = ['добавитьпредмет'])
	@commands.has_permissions(administrator = True)
	async def add_item(self, ctx, item: str = None, ids: int = None, cost: int = None, hp: int = None, mindamage: int = None, damage: int = None, accessbox: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Ошибка в синтаксисе. Пожалуйста проверьте правильность введённых вами данными или прочтите документацию - > https://docs.satiricon.xyz/ '
			lan11 = 'Вы успешно добавили'
			lan12 = 'ID покупки'
			lan13 = 'Цена'
			lan14 = 'Название предмета'
		else:
			lan1 = 'Error in the syntax. Please check that the data you entered is correct or read the documentation - > https://docs.satiricon.xyz/v/english'
			lan11 = 'You have successfully added'
			lan12 = 'Purchase ID'
			lan13 = 'Price'
			lan14 = 'Item Name'
		if not ids or not cost or not item or not hp or not mindamage or not damage or mindamage == 0 and damage > 0 or mindamage > 0 and damage == 0 or mindamage >= damage or accessbox > 1 or accessbox is None:
			emb = discord.Embed(title='Error', description = lan1)
			emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)
			await ctx.send(embed = emb)
		else:
			if await self.db.itemshop.count_documents({"guild": ctx.guild.id, "ids": ids}) == 0:
				for x in await self.db.settings.find({"server_id": ctx.guild.id}):
					if x["itemshop"] < 99:
						await self.db.settings.update_one({"server_id": ctx.guild.id}, {"$inc": {"itemshop": 1}})
						await self.db.itemshop.insert_one({
							"item": item,
							"ids": ids,
							"cost": cost,
							"hp": hp,
							"mindamage": mindamage,
							"damage": damage,
							"accessbox": accessbox,
							"guild": ctx.guild.id
						})
					emb = discord.Embed(description = f'{lan11} {item}')
			
					emb.add_field(name = f'{lan12}:', value = ids)
					emb.add_field(name = f'{lan13}:', value = cost)
					emb.add_field(name = f'{lan14}:', value = item)
			
					await ctx.send(embed = emb)

	@commands.command(aliases = ['удалитьпредмет'])
	@commands.has_permissions(administrator = True)
	async def remove_item(self, ctx, itemid: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Укажите <id> предмета!'
			lan2 = 'Вы успешно удалили'
			lan3 = 'из магазина'
		else:
			lan1 = 'Specify the <id> of the item!'
			lan2 = 'You have successfully deleted'
			lan3 = 'from the store'
		if not itemid:
			emb = discord.Embed(description = lan1)
			await ctx.send(embed = emb)
		else:
			if await self.db.itemshop.count_documents({"guild": ctx.guild.id, "ids": itemid}) > 0:
				await self.db.itemshop.delete_one({"ids": itemid, "guild": ctx.guild.id})
				await self.db.settings.update_one({"server_id": ctx.guild.id}, {"$inc": {"itemshop": -1}})

				emb = discord.Embed(description = f'{lan2} {itemid} {lan3}!')
				emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)

				await ctx.send(embed = emb)

	@commands.command(aliases = ['магазинпредметов'])
	async def itemshop(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Магазин предметов сервера'
			lan4 = 'ОЗ'
			lan5 = 'Урон'
			lan6 = 'Напишите `buy_item <id>` для покупки роли. Пример - `buy_item 543`'
		else:
			lan1 = 'server item Store'
			lan4 = 'OH'
			lan5 = 'Damage'
			lan6 = 'Write `buy_item <id>` to purchase the role. Example - `buy_item 3`'

		emb = discord.Embed(title = f'{lan1} {ctx.guild.name}')
		
		for x in await self.db.itemshop.find({"guild": ctx.guild.id}):

			emb.add_field(
				name = x["item"],
				value = f"**`ID: {x['ids']}`** **`Price: {x['cost']}`**\n **`{lan4}: {x['hp']}`** **`{lan5}: {x['mindamage']}-{x['damage']}`**",
				inline = True
			)

		emb.set_footer(text = lan6)
		await ctx.send(embed = emb)


	@commands.command(aliases = ['купитьпредмет'])
	async def buy_item(self, ctx, ids = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Укажите <id> предмета!'
			lan2 = 'У вас недостаточно денег!'
			lan3 = 'Вы успешно купили'
			lan4 = 'Такого ID предмта не существует!'
		else:
			lan1 = 'Specify the < id> of the item!'
			lan2 = 'You dont have enough money!'
			lan3 = 'You have successfully purchased'
			lan4 = 'There is no such script ID!'
		if not ids:
			emb = discord.Embed(description = lan1)
			await ctx.send(embed = emb)
		else:
			for y in await self.db.itemshop.find({"guild": ctx.guild.id}):
				if ids == y['ids']:

					for x in await self.db.users.find({"ids": ctx.author.id, "server_id": ctx.guild.id}):

						if x['cash'] < y['cost']:
							emb = discord.Embed(description = lan2)
							emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)
							await ctx.send(embed = emb)
						else:
							emb = discord.Embed(description = f'{lan3} {y["item"]}')
							emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)
							await ctx.send(embed = emb)

							await self.db.users.update_one({"ids": ctx.author.id, "server_id": ctx.guild.id}, {"$inc": {"cash": -int(y["cost"]), "hp": int(y["hp"]), "minattack": int(y["mindamage"]), "maxattack": int(y["damage"])}})
				else:
					emb = discord.Embed(description = lan4)
					emb.set_author(icon_url = ctx.author.avatar_url , name = ctx.author)
					await ctx.send(embed = emb)


def setup(client):
	client.add_cog(User(client))
