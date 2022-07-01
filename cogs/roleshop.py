import discord
from discord.ext import commands
from pymongo import MongoClient
import random
import asyncio
import string

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient('')["server"]

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def add_role(self, ctx, role: discord.Role = None, ids = None, cost: int = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Укажите <id> предмета!'
			lan2 = 'Укажите <cost> предмета!'
			lan3 = 'Укажите <role> предмета!'
			lan4 = 'Вы успешно добавили'
			lan5 = 'ID покупки:'
			lan6 = 'Цена:'
			lan7 = 'ID роли:'

		else:
			lan1 = 'Specify the <id> of the item!'
			lan2 = 'Specify the <cost> of the item!'
			lan3 = 'Specify the <role> of the item!'
			lan4 = 'You have successfully added'
			lan5 = 'Purchase ID:'
			lan6 = 'Price:'
			lan7 = 'Role ID:'

		if not ids:
			emb = discord.Embed(description = lan1)
			emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)
			await ctx.send(embed = emb)
		elif not cost:
			emb = discord.Embed(description = lan2)
			emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)
			await ctx.send(embed = emb)
		elif not role:
			emb = discord.Embed(description = lan3)
			emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)
			await ctx.send(embed = emb)

		else:
			if await self.db.roles.count_documents({"guild": ctx.guild.id, "ids": ids}) == 0:
				for x in await self.db.settings.find({"server_id": ctx.guild.id}):
					if x["roleshop"] < 99:
						await self.db.settings.update_one({"server_id": ctx.guild.id}, {"$inc": {"roleshop": 1}})
						await self.db.shop.insert_one({
							"role_id": role.id,
							"ids": ids,
							"cost": cost,
							"guild": ctx.guild.id
						})

				emb = discord.Embed(description = lan4 + role.mention)
			
				emb.add_field(name = lan5, value = ids)
				emb.add_field(name = lan6, value = cost)
				emb.add_field(name = lan7, value = role.id)
			
				await ctx.send(embed = emb)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def remove_role(self, ctx, role: discord.Role = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Укажите <role> предмета!'
			lan2 = 'Вы успешно удалили'
			lan3 = 'из магазина!'
		else:
			lan1 = 'Specify the < role> of the item!'
			lan2 = 'You have successfully deleted'
			lan3 = 'from the store!'

		if not role:
			emb = discord.Embed(description = lan1)
			await ctx.send(embed = emb)
		else:
			await self.db.shop.delete_one({"role_id": role.id, "guild":  ctx.author.id})
			for x in await self.db.settings.find({"server_id": ctx.guild.id}):
				ggtt = x["roleshop"] - 1
				await self.db.settings.update_one({"server_id": ctx.guild.id}, {"$set": {"roleshop": ggtt}})

			emb = discord.Embed(description = f'{lan2} {role.mention} {lan3}')
			emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)

			await ctx.send(embed = emb)

	@commands.command()
	async def shop(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Магазин ролей сервера'
			lan3 = 'Напишите `buy_role <ID>` для покупки роли. Пример - `buy_role 9`'
		else:
			lan1 = 'Server role store'
			lan3 = 'Write `buy_role <ID>` to purchase the role. Example -  `buy_role 10`'
		emb = discord.Embed(title = f'{lan1} **{ctx.guild.name}**')
		
		for x in await self.db.shop.find({"guild": ctx.guild.id}):
			ids = x['ids']
			role = x['role_id']
			cost = x['cost']
			
			for y in await self.db.settings.find({"server_id": ctx.guild.id}):
				emojiname = y["coinsname"]["id_emoji"][0]
				emojiid = y["coinsname"]["id_emoji"][1]

				if ctx.guild.get_role(role) != None:

					if ctx.guild.get_role(role) in ctx.author.roles:
						pass

					else:
						emb.add_field(
							name = ctx.guild.get_role(role), 
							value = f'**`ID: {ids}`**  **`{cost}`**<:{emojiname}:{emojiid}>', 
							inline=True
						)

		emb.set_footer(text = lan3)
		await ctx.send(embed = emb)

	@commands.command()
	async def buy_role(self, ctx, ids = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Укажите <id> предмета!'
			lan2 = 'У вас недостаточно денег!'
			lan3 = 'Вы успешно купили роль'
			lan4 = 'Такого ID предмта не существует!'
		else:
			lan1 = 'Specify the <id> of the item!'
			lan2 = 'You dont have enough money!'
			lan3 = 'You have successfully purchased the role'
			lan4 = 'There is no such script ID!'
		if not ids:
			emb = discord.Embed(description = lan1)
			await ctx.send(embed = emb)

		else:
			for y in await self.db.shop.find({"guild": ctx.guild.id}):
				if ids == y['ids']:

					for x in await self.db.users.find({"ids": ctx.author.id, "server_id": ctx.guild.id}):

						if x['cash'] < y['cost']:
							emb = discord.Embed(description = lan2)
							emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)
							await ctx.send(embed = emb)
						else:
							emb = discord.Embed(description = f'{lan3} {ctx.guild.get_role(y["role_id"]).mention}')
							emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)
							await ctx.send(embed = emb)

							result = x['cash'] - y['cost']
							await self.db.users.update_one({"ids": ctx.author.id, "server_id": ctx.guild.id}, {"$set": {"cash": result}})

							role = discord.utils.get(ctx.guild.roles, id = y['role_id'])
							await ctx.author.add_roles(role)
				else:
					emb = discord.Embed(description = lan4)
					emb.set_author(icon_url = ctx.author.avatar_url, name = ctx.author)
					await ctx.send(embed = emb)

	@add_role.error
	async def add_role_error(self, ctx, error):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Вы не можете использовать данную команду!'
			lan2 = 'Нужные права: `Администратор`'
		else:
			lan1 = 'You cant use this command!'
			lan2 = 'Required rights: `Administrator`'
		if isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(title = lan1, description = lan2)
			await ctx.send(embed = emb)

	@remove_role.error
	async def remove_role_error(self, ctx, error):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Вы не можете использовать данную команду!'
			lan2 = 'Нужные права: `Администратор`'
		else:
			lan1 = 'You cant use this command!'
			lan2 = 'Required rights: `Administrator`'
		if isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(title = lan1, description = lan2)
			await ctx.send(embed = emb)


def setup(client):
	client.add_cog(User(client))
