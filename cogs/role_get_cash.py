import discord
from discord.py import commands
import pymongo
from pymongo import MongoClient

class profile(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient('')["server"]

def setup(client):
	client.add_cog(profile(client))
