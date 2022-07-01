import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import random
import asyncio

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.id == self.client.user.id:
			pass
		else:	
			for xr in await self.db.settings.find({"server_id": message.guild.id}):
				symbols = xr['levelelements']['symbols']

				if len(message.content) > int(symbols):
					mingetexp = xr['levelelements']['mingetexp']
					maxgetexp = xr['levelelements']['maxgetexp']
					cashget = xr['levelelements']['cashget']
					integerexp = xr['levelelements']['integerexp']
					newminattack = xr['levelelements']['newminattack']
					newmaxattack = xr['levelelements']['newmaxattack']
					newhp = xr['levelelements']['newhp']

					for row in self.db.users.find({"ids": message.author.id, "server_id": message.guild.id}):
						expi = random.randint(mingetexp, maxgetexp)
						await self.db.users.update({"ids": message.author.id, "server_id": message.guild.id}, {"$inc": {"exp": expi}})
						lvl = row["lvl"]
						lvch = row["exp"] / ((lvl * integerexp) + 50)
						lv = round(lvch)

						if row["lvl"] < lv:
							if str(message.guild.region) == 'russia':
								lan1 = '**Повышение уровня!**'
								lan2 = 'Уровень повышен!'
								lan3 = 'ОЗ'
								lan4 = 'Максимальная атака:'
								lan5 = 'Минимальная атака:'
							else:
								lan1 = '**The level-up!**'
								lan2 = 'Level up!'
								lan3 = 'OH'
								lan4 = 'Maximum attack:'
								lan5 = 'Minimum attack:'
							emb = discord.Embed(title = lan1, description = f'''
								{lan2}
								{lan3}: {row["hp"]} + {newhp}
								{lan4} {row["maxattack"]} + {newmaxattack}
								{lan5}: {row["minattack"]} + {newminattack}
								''', color = 0xb3ffe5)
							emb.set_author(name = message.author, icon_url = message.author.avatar_url)
							await message.channel.send(embed = emb)
							hpnew = row["lvl"] * newhp
							maxattacknew = row["lvl"] * newmaxattack
							minattacknew = row["lvl"] * newminattack
							await self.db.users.update({"ids": message.author.id, "server_id": message.guild.id}, {"$inc": {"hp": hpnew, "maxattack": maxattacknew, "minattack": minattacknew, "lvl": 1}})
							await self.db.users.update({"ids": message.author.id, "server_id": message.guild.id}, {"$set": {"exp": 0}})

				if  xr["logchannel"] != 0:
					for word in str(message.content.split()):
						if word.isupper() is True:
							await message.delete()
							await self.db.users.update({"ids": message.author.id, "server_id": message.guild.id}, {"$inc": {"prewarn": 1}})
							if str(message.guild.region) == 'russia':
								lan1 = 'использует капс, мы выдали ему пре-нарушение. Чтобы узнать его пре-нарушения используйте `$info <@user#0000>`'
							else:
								lan1 = 'uses caps, we gave him a pre-violation. To find out its pre-violations, use  `$info <@user#0000>`'
							emb = discord.Embed(title = 'AutoModeration[:robot:]', description = f'{message.author} {lan1}')
							channel_log = self.client.get_channel(xr["logchannel"])
							await channel_log.send(embed = emb)

				if xr["wordacces"] == 1:
					word_list = xr["wordblock"]
					for word in message.content.split():
						if word.lower() in word_list:
							await message.delete()
							await self.db.users.update({"ids": message.author.id, "server_id": message.guild.id}, {"$inc": {"prewarn": 1}})
							if  xr["logchannel"] != 0:
								if str(message.guild.region) == 'russia':
									lan1 = 'использует запрещённое слово, мы выдали ему пре-нарушение. Чтобы узнать его пре-нарушения используйте `$info <@user#0000>`'
								else:
									lan1 = 'uses bad word, we gave him a pre-violation. To find out its pre-violations, use  `$info <@user#0000>`'
								emb = discord.Embed(title = 'AutoModeration[:robot:]', description = f'{message.author} {lan1}')
								channel_log = self.client.get_channel(xr["logchannel"])
								await channel_log.send(embed = emb)

				for xs in self.db.customcommands.find({"server_id": message.guild.id}):
					if message.content.split() == xr['prefix'] + xs['name']:
						await message.channel.send(xs["body"])

				random_word_message = random.randint(1, 450)
				if random_word_message in range(45, 110):
					if str(message.guild.region) == 'russia':
						lan1



def setup(client):
	client.add_cog(User(client))
