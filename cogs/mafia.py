import discord
from discord.ext import commands
import asyncio
import random
import pymongo
from pymongo import MongoClient
import string

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.command()
	async def mcreate_party(self, ctx):
		def buildblock(size):
			return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
		partycode = buildblock(10)

		self.db.mafiaparty.insert_one({
			"admin": ctx.author.id,
			"code": partycode,
			"server_id": ctx.guild.id,
			"users": [ctx.author.id]
		})

	@commands.command()
	async def m_start(self, ctx, member: discord.Member = None):
		if member == None:
			member = ctx.author
		if self.db.mafiaparty.find({"admin": member.id, "server_id": ctx.guild.id}) != 0:
			reaction_list_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
			for x in self.db.mafiaparty.find({"admin": member.id, "server_id": ctx.guild.id}):
				if len(x["users"]) in range(3, 5):
					mafiauser = x["users"][random.randint(0, ((len(x["users"]) - 1)))]
					overwrites = {
						ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
						self.client.get_user(mafiauser): discord.PermissionOverwrite(read_messages=True)
					}
					mafiachannel = await ctx.guild.create_text_channel('only_for_mafia',  overwrites = overwrites, reason = 'Этот канал создан автоматически для игры в mafia между участниками.')
					emb1 = discord.Embed(title = 'Игра началась!', description = f'Всего игроков: {len(x["users"])}. Надеюсь вы знаете правила. Один из вас оказался предателем. Вычислите его и выгоните с города! Нажмите на кнопку ⏩, чтобы начать ночь.')
					mosg = await ctx.send(embed = emb1)
					await mosg.add_reaction('⏩')
					embmafia = discord.Embed(title = 'Ты мафия!', description = 'Начиная с следующей ночи, ты сможешь выбирать кого убить. Не дай себя выдать!')
					await mafiachannel.send(embed = embmafia)
					try:
						react, user = await self.client.wait_for('reaction_add', timeout=180.0, check=lambda react, user: user == self.client.get_user(x['admin']) and react.message.channel == ctx.channel and react.emoji in '⏩')
					except Exception:
						await mosg.delete()
					else:
						user_list = x['users']
						flag = True
						while flag:

							msgmafia = discord.Embed(title = 'Время выбирать!', description = 'Убей кого-нибудь, что бы приблизиться к захвату города!')
							nums = 0
							for x in user_list:
								nums += 1
								msgmafia.add_field(name= f'#{nums}', value = f'{reaction_list_numbers[nums - 1]} - {self.client.get_user(user_list[nums - 1])}')
							msgmafia_add = await mafiachannel.send(embed = msgmafia)
							numsemoji = 0
							for y in reaction_list_numbers:
								if numsemoji < len(user_list):
									numsemoji += 1
									await msgmafia_add.add_reaction(y)
							try:
								react, user = await self.client.wait_for('reaction_add', timeout=180.0, check=lambda react, user: user == self.client.get_user(mafiauser) and react.message.channel == mafiachannel.channel and react.emoji in reaction_list_numbers)
							except Exception:
								await msgmafia_add.delete()
							if str(react.emoji) == reaction_list_numbers[0]:
								user_remove = user_list[0]
								user_list.remove(user_remove)
								await mafiachannel.send(f"Ты убил {self.client.get_user(user_remove)}")
							elif str(react.emoji) == reaction_list_numbers[1]:
								user_remove = user_list[1]
								user_list.remove(user_remove)
								await mafiachannel.send(f"Ты убил {self.client.get_user(user_remove)}")
							elif str(react.emoji) == reaction_list_numbers[2]:
								user_remove = user_list[2]
								user_list.remove(user_remove)
								await mafiachannel.send(f"Ты убил {self.client.get_user(user_remove)}")
							elif str(react.emoji) == reaction_list_numbers[3]:
								user_remove = user_list[3]
								user_list.remove(user_remove)
								await mafiachannel.send(f"Ты убил {self.client.get_user(user_remove)}")
							elif str(react.emoji) == reaction_list_numbers[4]:
								user_remove = user_list[4]
								user_list.remove(user_remove)
								await mafiachannel.send(f"Ты убил {self.client.get_user(user_remove)}")
							msgusers = discord.Embed(title = 'Время выбирать!', description = 'Найдите мафию, и выгоните его из города!')
							nums = 0
							for x in user_list:
								nums += 1
								msgusers.add_field(name= f'#{nums}', value = f'{reaction_list_numbers[nums - 1]} - {self.client.get_user(user_list[nums - 1])}')
							msguser1 = await mafiachannel.send(embed = msgusers)
							numsemoji = 0
							for y in reaction_list_numbers:
								if numsemoji < len(user_list):
									numsemoji += 1
									await msguser1.add_reaction(y)
							try:
								react, user = await self.client.wait_for('reaction_add', timeout=180.0, check=lambda react, user: user == self.client.get_user(x['admin']) and react.message.channel == ctx.channel and react.emoji in '⏩')
							except Exception:
								await msguser1.delete()
							if str(react.emoji) == reaction_list_numbers[0]:
								user_remove = user_list[0]
								user_list.remove(user_remove)
								if user_remove == mafiauser:
									flag = False
									await mafiachannel.delete(reason = 'Игра была закончена')
									await ctx.send(f'Победили игроки! Маифей был {self.client.get_user(mafiauser)}')
								else:
									await ctx.send(f"{self.client.get_user(user_remove)} не был мафией!")
									flag = True
							elif str(react.emoji) == reaction_list_numbers[1]:
								user_remove = user_list[1]
								user_list.remove(user_remove)
								if user_remove == mafiauser:
									flag = False
									await mafiachannel.delete(reason = 'Игра была закончена')
									await ctx.send(f'Победили игроки! Маифей был {self.client.get_user(mafiauser)}')
								else:
									await ctx.send(f"{self.client.get_user(user_remove)} не был мафией!")
									flag = True
							elif str(react.emoji) == reaction_list_numbers[2]:
								user_remove = user_list[2]
								user_list.remove(user_remove)
								if user_remove == mafiauser:
									flag = False
									await mafiachannel.delete(reason = 'Игра была закончена')
									await ctx.send(f'Победили игроки! Маифей был {self.client.get_user(mafiauser)}')
								else:
									await ctx.send(f"{self.client.get_user(user_remove)} не был мафией!")
									flag = True
							elif str(react.emoji) == reaction_list_numbers[3]:
								user_remove = user_list[3]
								user_list.remove(user_remove)
								if user_remove == mafiauser:
									flag = False
									await mafiachannel.delete(reason = 'Игра была закончена')
									await ctx.send(f'Победили игроки! Маифей был {self.client.get_user(mafiauser)}')
								else:
									await ctx.send(f"{self.client.get_user(user_remove)} не был мафией!")
									flag = True
							elif str(react.emoji) == reaction_list_numbers[4]:
								user_remove = user_list[4]
								user_list.remove(user_remove)
								if user_remove == mafiauser:
									flag = False
									await mafiachannel.delete(reason = 'Игра была закончена')
									await ctx.send(f'Победили игроки! Маифей был {self.client.get_user(mafiauser)}')
								else:
									await ctx.send(f"{self.client.get_user(user_remove)} не был мафией!")
									flag = True
										
				elif len(x["users"]) in range(5, 8):
					...
				elif len(x["users"]) in range(8, 10):
					...
				else:
					...
			

def setup(client):
	client.add_cog(User(client))
