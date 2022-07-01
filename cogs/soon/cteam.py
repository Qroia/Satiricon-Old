import discord
from discord.ext import commands
import asyncio
import math
import pymongo
from pymongo import MongoClient
import random
import requests
import os

class Clans(commands.Cog):
	def __init__(self,client):
		self.client = client
		self.db = MongoClient('')["server"]

	@commands.command()
	async def clan(self,ctx,category = None,*,name = None):
		category2 = ['create','delete','info','invite','leave','kick']
		if category != None:
			if category in category2:
				if category == 'create':
					clan = db.child(f'{ctx.author.id}{ctx.guild.id}{ctx.guild.id}').get()
					clan = clan.val()
					try:
						clan = clan['clan']
					except:
						clan = None
					else:
						if clan == 'None':
							clan = None
						else:
							clan = True
					if clan == None:
						cash = DB.child(f'{ctx.author.id}{ctx.guild.id}').get()
						cash = cash.val()
						cash = cash['cash']
						cash = int(cash)
						if cash >= 10000:
							if name != None:
								data = {'cash':str(cash - 10000)}
								DB.child(f'{ctx.author.id}{ctx.guild.id}').update(data)
								members = []
								members.append(ctx.author.id)
								dataclan = {'name':name,'owner':str(ctx.author.id),'members':members}
								db.child(f'{ctx.author.id}{ctx.guild.id}').set(dataclan)
								data = {'name':ctx.author.name,'id':str(ctx.author.id),'clan':f'{ctx.author.id}{ctx.guild.id}'}
								db.child(f'{ctx.author.id}{ctx.guild.id}{ctx.guild.id}').set(data)
								embed = discord.Embed(title = 'Кланы',description = f'{ctx.author.mention} вы успешно создали клан {name}')
								await ctx.send(embed = embed)
							else:
								await ctx.send(f'**{ctx.author.name}** вы не ввели название клана!')
						else:
							await ctx.send(f'**{ctx.author.name}** что бы создать клан у вас должно быть 10 тысяч!')
					else:
						await ctx.send(f'**{ctx.author.name}** у вас и так уже есть клан!Что-бы создать новый клан выйдите со старого или распуте(если вы создатель)!')
				if category == 'info':
					clan2 = db.child(f'{ctx.author.id}{ctx.guild.id}{ctx.guild.id}').get()
					clan2 = clan2.val()
					try:
						clan = clan2['clan']
					except:
						clan = None
					else:
						if clan == 'None':
							clan = None
						else:
							clan = True
					if clan != None:
						clanmembers22 = []
						clan = clan2['clan']
						clan = db.child(clan).get()
						clan = clan.val()
						clanname = clan['name']
						clanowner = clan['owner']
						clanowner = int(clanowner)
						clanowner = ctx.guild.get_member(clanowner)
						clanmembers = clan['members']
						for i in clanmembers:
							clanmembers3333 = ctx.guild.get_member(int(i))
							clanmembers22.append(f'{clanmembers3333.mention}')
						emb = discord.Embed(title = f'Кланы',description = f'**Информация о клане {clanname}**\n\nСоздатель клана: {clanowner.mention}\nУчастников в клане: {len(clanmembers)}\nУчастники клана:' + '{}'.format('`|`'.join(clanmembers22)))
						await ctx.send(embed = emb)
					else:
						emb = discord.Embed(title = f'Вы не состоите ни в одном клане!')
						await ctx.send(embed = emb)
				if category == 'delete':
					clan2 = db.child(f'{ctx.author.id}{ctx.guild.id}{ctx.guild.id}').get()
					clan2 = clan2.val()
					try:
						clan = clan2['clan']
					except:
						clan = None
					else:
						if clan == 'None':
							clan = None
						else:
							clan = True
					if clan != None:
						clan = clan2['clan']
						clan = db.child(f'{clan}').get()
						clan = clan.val()
						clanowner = clan['owner']
						clanowner = int(clanowner)
						if clanowner == int(ctx.author.id):
							clanmembers = clan['members']
							for member in clanmembers:
								data = {'clan': 'None'}
								db.child(f'{member}{ctx.guild.id}{ctx.guild.id}').update(data)
							db.child(f'{ctx.author.id}{ctx.guild.id}').remove()
							embed = discord.Embed(title = 'Кланы',description = f'{ctx.author.mention} ваш клан был успешно удалён')
							await ctx.send(embed = embed)
						else:
							emb = discord.Embed(title = f'{ctx.author.name} вы не владеете ни одним кланом!')
							await ctx.send(embed = emb)
					else:
						emb = discord.Embed(title = f'{ctx.author.name} вы не владеете ни одним кланом!')
						await ctx.send(embed = emb)
				if category == 'invite':
					if name != None:
						name = name.replace('<@','')
						name = name.replace('!','')
						name = name.replace('>','')
						try:
							name = int(name)
						except:
							await ctx.send(f'**{ctx.author.name}** укажите пользователя которого хотите пригласить в клан!')
						else:
							try:
								member = ctx.guild.get_member(name)
							except:
								await ctx.send(f'**{ctx.author.name}** вы указали не существующего пользователя!')
							else:
								result = db.child(f'{member.id}{ctx.guild.id}{ctx.guild.id}').get()
								result = result.val()
								if result != None:
									clan = db.child(f'{ctx.author.id}{ctx.guild.id}{ctx.guild.id}').get()
									clan = clan.val()
									clan = clan['clan']
									clan = db.child(f'{clan}').get()
									clan = clan.val()
									if clan != None:
										owner = clan['owner']
										if str(owner) == str(ctx.author.id):
											members = clan['members']
											if member.id not in members:
												clanowner = clan['owner']
												clanname = clan['name']
												data = {'invite': f'{clanowner}{ctx.guild.id}'}
												db.child(f'{member.id}{ctx.guild.id}{ctx.guild.id}').update(data)
												embed = discord.Embed(title = 'Кланы',description = f'{member.mention} {ctx.author.mention} пригласил вас в клан **{clanname}**\nУ его есть 30 секунд чтобы принять приглашение!')
												new = await ctx.send(embed = embed)
												await new.add_reaction('✅')
												await new.add_reaction('❎')
												def check(reaction,user):
													if reaction.message == new:
														return user == member and reaction.emoji in '❎✅'
												try:
													reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
												except asyncio.TimeoutError:
													await new.delete()
													embed = discord.Embed(title = 'Кланы',description = f'{ctx.author.mention} у {member.mention} вышло время инвайта!')
													await ctx.send(embed = embed)
												else:
													if reaction.emoji == '✅':
														await new.delete()
														clan = f'{ctx.author.id}{ctx.guild.id}'
														clan = db.child(clan).get()
														clan = clan.val()
														members = clan['members']
														owner = clan['owner']
														name = clan['name']
														members.append(member.id)
														data = {'members':members}
														db.child(f'{ctx.author.id}{ctx.guild.id}').update(data)
														emb = discord.Embed(title = 'Кланы',description = f'{member.mention} вы успешно вступили в клан {name}!')
														await ctx.send(embed = emb)
													if reaction.emoji == '❎':
														await new.delete()
														embed = discord.Embed(title = 'Кланы',description = f'{member.mention} вы успешно отвергли вход в клан {clanname}!')
														await ctx.send(embed = embed)
											else:
												await ctx.send(f'**{ctx.author.name}** данный пользователь и так находится в вашем клане!')
										else:
											await ctx.send(f'**{ctx.author.name}** вы не состоите ни в одном клане!')
									else:
										await ctx.send(f'**{ctx.author.name}** только создатель клана может приглошать туда людей!')
					else:
						await ctx.send(f'**{ctx.author.name}** вы не указали пользователя которому хотите отправить приглошение!')
				if category == 'leave':
					member = db.child(f'{ctx.author.id}{ctx.guild.id}{ctx.guild.id}').get()
					member = member.val()
					clan = member['clan']
					if clan != 'None':
						clan = db.child(clan).get()
						clan = clan.val()
						clanname = clan['name']
						owner = clan['owner']
						if str(ctx.author.id) != owner:
							data = {'clan':'None'}
							db.child(f'{ctx.author.id}{ctx.guild.id}{ctx.guild.id}').update(data)
							members = clan['members']
							for i in range(len(members)):
								if members[i] == int(ctx.author.id):
									members.pop(i)
									break
							data = {'members':members}
							db.child(f'{owner}{ctx.guild.id}').update(data)
							embed = discord.Embed(title = 'Кланы',description = f'{ctx.author.name} вы успешно покинуди клан {clanname}')
							await ctx.send(embed = embed)
						else:
							await ctx.send(f'**{ctx.author.name}** вы не можете выйти из клана,так как вы создатель клана!')
				if category == 'kick':
					member = db.child(f'{ctx.author.id}{ctx.guild.id}{ctx.guild.id}').get()
					member = member.val()
					clan = member['clan']
					if clan != 'None':
						clan = db.child(clan).get()
						clan = clan.val()
						owner = clan['owner']
						if str(ctx.author.id) == owner:
							if name != None:
								name = name.replace('<@','')
								name = name.replace('!','')
								name = name.replace('>','')
								try:
									name = int(name)
								except:
									await ctx.send(f'**{ctx.author.id}** вы не указали пользователя которого хотите кикнуть!')
								else:
									try:
										member = ctx.guild.get_member(name)
									except:
										await ctx.send(f'**{ctx.author.name}** вы указали не существующего на этом сервере пользователя!')
									else:
										members = clan['members']
										if int(member.id) in members:
											for i in range(len(members)):
												if member.id == members[i]:
													data = {'clan':'None'}
													db.child(f'{member.id}{ctx.guild.id}{ctx.guild.id}').update(data)
													members.pop(i)
													data = {'members':members}
													db.child(f'{ctx.author.id}{ctx.guild.id}').update(data)
													emb = discord.Embed(title = 'Кланы',description = f'{ctx.author.mention} вы успешно кикнули из своего клана {member.mention}')
													await ctx.send(embed = emb)
							else:
								await ctx.send(f'**{ctx.author.name}** вы не указали пользователя которого хотите кикнуть')
						else:
							await ctx.send(f'**{ctx.author.name}** только создатель клана может кикать!')
			else:
				await ctx.send('Данной категории не существует!Вот список всех категорий `{}`!'.format('` `'.join(category2)))

def setup(client):
	client.add_cog(Clans(client))
