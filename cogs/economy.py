import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import asyncio

class economy(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db     = MongoClient("")["server"]

	@commands.command(aliases = ['добавитьденьги'])
	@commands.has_permissions(manage_channels = True)
	async def add_cash(self, ctx, member: discord.Member, count: int):
		await self.db.users.update_one({"server_id": ctx.guild.id, "ids": member.id}, {"$inc": {"cash": count}})
		await ctx.message.add_reaction('✅')

	@commands.command(aliases = ['убратьденьги'])
	@commands.has_permissions(manage_channels = True)
	async def reduce_cash(self, ctx, member: discord.Member, count: int):
		await self.db.users.update_one({"server_id": ctx.guild.id, "ids": member.id}, {"$inc": {"cash": -count}})
		await ctx.message.add_reaction('✅')

	@commands.command(aliases = ['добавитьуровень'])
	@commands.has_permissions(administrator = True)
	async def add_level(self, ctx, member: discord.Member, amount: int):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'укажите пользователя которому хотите добавить уровень'
			lan2 = 'укажите уровень который хотите добавить'
			lan3 = 'укажите уровень больше 1'
		else:
			lan1 = 'specify the user you want to add a level to'
			lan2 = 'specify the level you want to add'
			lan3 = 'specify a level greater than 1'
		if member is None:
			await ctx.send(f"**{ctx.author}**, {lan1}")
		elif amount is None:
			await ctx.send(f"**{ctx.author}**, {lan2}")
		elif amount < 1:
			await ctx.send(f"**{ctx.author}**, {lan3}")
		else:
			await self.db.users.update_one({"ids": member.id, "server_id": ctx.guild.id}, {"$inc": {"lvl": amount}})
			await ctx.message.add_reaction('✅')

	@commands.command(aliases=['убратьуровень'])
	@commands.has_permissions(administrator=True)
	async def reduce_level(self, ctx, member: discord.Member, amount: int):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'укажите пользователя которому хотите уменьшить уровень'
			lan2 = 'укажите уровень который хотите убрать'
			lan3 = 'укажите уровень больше 1'
		else:
			lan1 = 'specify the user you want to reduce a level to'
			lan2 = 'specify the level you want to reduce'
			lan3 = 'specify a level greater than 1'
		if member is None:
			await ctx.send(f"**{ctx.author}**, {lan1}")
		elif amount is None:
			await ctx.send(f"**{ctx.author}**, {lan2}")
		elif amount < 1:
			await ctx.send(f"**{ctx.author}**, {lan3}")
		else:
			await self.db.users.update_one({"ids": member.id, "server_id": ctx.guild.id}, {"$inc": {"lvl": -amount}})
			await ctx.message.add_reaction('✅')

	#@commands.Cog.listener()
	#async def on_reaction_add(self, reaction, user):
	#	if reaction.message.author != user:
	#		for guild in self.client.guilds:
	#			db.users.update_one({"ids": reaction.message.author, "server_id": guild.id}, {"$inc": {"rep": 1}})


def setup(client):
	client.add_cog(economy(client))
