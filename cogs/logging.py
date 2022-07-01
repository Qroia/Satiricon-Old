import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient

class logging(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

def setup(client):
	client.add_cog(logging(client))
