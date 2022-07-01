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
		self.db = MongoClient('')["server"]

	@commands.command()
	@commands.cooldown(1, 600, commands.BucketType.user)
	async def mine(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Вы получили'
			lan2 = 'Монеты'
			lan3 = 'Опыт'
		else:
			lan1 = 'You got'
			lan2 = 'Coins'
			lan3 = 'Experience'
		for row in await self.db.users.find({"ids": ctx.author.id, "server_id": ctx.guild.id}):
			cash1 = random.randint(1, 2)
			exp = random.randint(4, 5)
			cashup = row['cash'] + cash1
			expup = row['exp'] + exp
			await self.db.users.update_one({"ids": ctx.author.id, "server_id": ctx.guild.id}, {"$set": {"cash": cashup, "exp": expup}})
			emb = discord.Embed(title = lan1, description = f'\n{lan2}: {cash1}\n{lan3}: {exp}')
			await ctx.send(embed = emb)

	@commands.command()
	@commands.cooldown(1, 950, commands.BucketType.user)
	async def fight(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Вы подняли свои характеристики!'
			lan2 = 'Здоровье'
			lan3 = 'Урон'
		else:
			lan1 = 'You have raised your stats!'
			lan2 = 'Health'
			lan3 = 'Damage'
		for row in await self.db.users.find({"ids": ctx.author.id, "server_id": ctx.guild.id}):
			hpfight = random.randint(1, 2)
			maxafight = random.randint(4, 5)
			minafight = random.randint(1, 3)
			hpup = row['hp'] + hpfight
			maxattackup = row['maxattack'] + maxafight
			minattackup = row['minattack'] + minafight
			await self.db.users.update_one({"ids": ctx.author.id, "server_id": ctx.guild.id}, {"$set": {"hp": hpup, "maxattack": maxattackup, "minattack": minattackup}})
			emb = discord.Embed(title = lan1, description = f'\n{lan2}: {hpfight}\n{lan3}: {minattack}-{maxattack}')
			await ctx.send(embed = emb)

def setup(client):
	client.add_cog(User(client))
