import discord
from discord.ext import commands
import random
import os

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		
	@commands.command()
	async def neko(self, ctx):
		askrandom = random.randint(1, 2)
		await ctx.send(file = discord.File(f"./picture/neko/image{askrandom}.png"))

	@commands.command()
	async def anime_ass(self, ctx):
		askrandom = random.randint(1, 2)
		await ctx.send(file = discord.File(f"./picture/animeass/image{askrandom}.png"))

	@commands.command()
	async def ass(self, ctx):
		askrandom = random.randint(1, 2)
		await ctx.send(file = discord.File(f"./picture/ass/image{askrandom}.png"))
	
	@commands.command()
	async def hentai(self, ctx):
		askrandom = random.randint(1, 2)
		await ctx.send(file = discord.File(f"./picture/hentai/image{askrandom}.png"))
	
	@commands.command()
	async def art(self, ctx):
		askrandom = random.randint(1, 52)
		await ctx.send(file = discord.File(f"./picture/art/image ({askrandom}).jpg"))
	
	@commands.command()
	async def waifu(self, ctx):
		askrandom = random.randint(1, 2)
		await ctx.send(file = discord.File(f"./picture/waifu/image{askrandom}.png"))

	@commands.command()
	async def porno(self, ctx):
		askrandom = random.randint(1, 2)
		await ctx.send(file = discord.File(f"./picture/porno/image{askrandom}.png"))

def setup(client):
	client.add_cog(User(client))