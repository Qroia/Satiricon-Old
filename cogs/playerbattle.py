import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import random

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.command()
	async def online_battle(self, ctx, member: discord.Member = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Выберите с кем вы хотите сразиться'
			lan2 = 'Вы хотите сыграть с'
			lan3 = 'Чтобы начать бой, нужно чтобы'
			lan4 = 'подтвердил начало боя.'
			lan5 = 'Согласен'
			lan6 = 'Не согласен.'
			lan7 = 'В противном случае бой будет отменён в течение 15 секунд.'
			lan8 = 'Выиграл'
			lan9 = 'У'
			lan10 = 'осталось'
			lan11 = 'Ничья'
			lan12 = 'Ваш противник не согласился на битву'
			lan13 = 'Неверная реакция!'
		else:
			lan1 = 'Choose who you want to fight'
			lan2 = 'You want to play with'
			lan3 = 'to start a fight, you need to'
			lan4 = 'confirmed the start of the battle.'
			lan5 = 'Agree'
			lan6 = 'do Not agree.'
			lan7 = 'Otherwise, the fight will be canceled within 15 seconds.'
			lan8 = 'Won'
			lan9 = 'He'
			lan10 = 'left'
			lan11 = 'Draw'
			lan12 = 'Your opponent did not agree to the battle'
			lan13 = 'Incorrect response!'
		if member is None:
			await ctx.send(lan1)
		else:
			r_list = ['✅', '❌']
			msg = await ctx.send(f'{lan2} {member.mention}\n {lan3} {member} {lan4}\n{r_list[0]} - {lan5}\n{r_list[1]} - {lan6}\n {lan7}')
			for r in r_list:
				await msg.add_reaction(r)
			try:
				react, user = await self.client.wait_for('reaction_add', timeout=15.0, check=lambda react, user: user == member and react.message.channel == ctx.channel and react.emoji in r_list)
			except Exception:
				await msg.delete()
			else:
				if str(react.emoji) == r_list[0]:
					await msg.clear_reactions()
					for x in await self.db.users.find({"ids": ctx.author.id, "server_id": ctx.guild.id}):
						for y in await self.db.users.find({"ids": member.id, "server_id": ctx.guild.id}):
							hp1 = int(x['hp'])
							attack1 = int(x['maxattack'])
							mattack1 = int(x['minattack'])
							hp2 = int(y['hp'])
							attack2 = int(y['maxattack'])
							mattack2 = int(y['maxattack'])
							flag = True
							while flag:
								attackrandom1 = random.randint(mattack1, attack1)
								attackrandom2 = random.randint(mattack2, attack2)
								hp1 = hp1 - attackrandom2
								hp2 = hp2 - attackrandom1
								if hp1 > 0 and hp2 > 0:
									flag = True
								elif hp1 > 0 and hp2 < 0:
									emb = discord.Embed(title = f'{lan8} {ctx.author}', description = f'{lan9} {ctx.author} {lan10}: {hp1}\n{lan9} {member} {lan10}: {hp2}')
									await msg.edit(embed = emb, content = None)
									flag = False
								elif hp1 < 0 and hp2 > 0:
									emb = discord.Embed(title = f'{lan8} {member}', description = f'{lan9} {member} {lan10}: {hp1}\n{lan9} {ctx.author} {lan10}: {hp2}')
									await msg.edit(embed = emb, content = None)
									flag = False
								elif hp1 < 0 and hp2 < 0:
									emb = discord.Embed(title = lan11, description = f'{lan9} {member} {lan10}: {hp2}\n{lan9} {ctx.author} {lan10}: {hp1}')
									await msg.edit(embed = emb, content = None)
									flag = False
				elif str(react.emoji) == r_list[1]:
					await ctx.send(lan12)
					await msg.delete()
					await msg.clear_reactions()
				else:
					await msg.delete()
					await ctx.send(lan13, delete_after=10.0)

def setup(client):
	client.add_cog(User(client))
