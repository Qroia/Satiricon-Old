import discord
from discord import commands
import pymongo
from pymongo import MongoClient

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
        self.db = MongoClient('')["server"]

    ...

def setup(client):
	client.add_cog(User(client))
