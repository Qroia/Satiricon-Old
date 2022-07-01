import discord
from discord.ext import commands
from discord_slash import SlashCommand
import pymongo
from pymongo import MongoClient
import random
import asyncio

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient('')["server"]
        slash = SlashCommand(self.client, auto_register=True)

    @slash.slash(name="ping", description="Возращает скорость ответа бота",) 
    async def _ping(self, ctx):
        await ctx.send(f"Pong! ({client.latency*1000}ms)")

    @slash.slash(name="help", description="Помощь по коммандам")
    async def _help(self, ctx, arg: str = None):
        if arg == "?":
            await ctx.send("Ссылка на документацию")
        if arg == "economy":
            ...


def setup(client):
	client.add_cog(User(client))
