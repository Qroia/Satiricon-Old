import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import datetime
import asyncio

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.command(aliases = ['очистить'])  ### Команда для чистки чата (clear)
	@commands.has_permissions(manage_messages = True)
	async def clear(self, ctx, amount=100):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Чат был почищен! Удалено'
			lan2= 'сообщений'
		else:
			lan1 = 'The chat was cleaned up! Deleted'
			lan2= 'messages'
		await ctx.channel.purge(limit=amount+1)
		await ctx.send(f'{lan1} ```{amount+1}``` {lan2}')


	@commands.command(aliases = ['кик'])
	@commands.has_permissions(manage_messages = True)
	async def kick(self, ctx, member: discord.Member, *, reason: str):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Инфо о кике'
			lan2 = 'Нарушитель'
			lan4 = 'Модератор'
		else:
			lan1 = 'Kick info'
			lan2 = 'Intruder'
			lan4 = 'Moderator'

		await member.kick(reason=reason)
		for row in await self.db.settings.find({"server_id": ctx.guild.id}):
			if row['logchannel'] != 0:
				emb = discord.Embed(title=lan1, colour=discord.Color.red())
				emb.set_author(name=member.name, icon_url=member.avatar_url)
				emb.add_field(name=lan2, value=member.mention)
				emb.add_field(name=lan4, value=ctx.message.author.mention, inline=False)
				channel_log = self.client.get_channel(row['logchannel'])
				await channel_log.send(embed=emb)
				await ctx.message.add_reaction('✅')
			else:
				await ctx.message.add_reaction('✅')

	@commands.command(aliases = ['бан'])  ### Команда для бана участника (ban)
	@commands.has_permissions(manage_messages = True)
	async def ban(self, ctx, member: discord.Member, *, reason: str):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Инфо о бане'
			lan2 = 'Нарушитель'
			lan4 = 'Модератор'
		else:
			lan1 = 'Ban info'
			lan2 = 'Intruder'
			lan4 = 'Moderator'

		await member.ban(reason=reason)
		for row in await self.db.settings.find({"server_id": ctx.guild.id}):
			if row["logchannel"] != 0:
				emb = discord.Embed(title=lan1, colour=discord.Color.red())
				emb.set_author(name=member.name, icon_url=member.avatar_url)
				emb.add_field(name=lan2, value=member.mention)
				emb.add_field(name=lan4, value=ctx.message.author.mention, inline=False)
				channel_log = self.client.get_channel(row['logchannel'])
				await channel_log.send(embed=emb)
				await ctx.message.add_reaction('✅')	
			else:
				await ctx.message.add_reaction('✅')

	@commands.command(aliases = ['анбан'])  ### Команда для разбана участника (unban)
	@commands.has_permissions(manage_messages = True)
	async def unban(self, ctx, *, member: discord.Member):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Инфо о разбане'
			lan2 = 'Нарушитель'
			lan4 = 'Модератор'
		else:
			lan1 = 'Unban info'
			lan2 = 'Intruder'
			lan4 = 'Moderator'
		banned_users = await ctx.guild.bans()

		for ban_entry in banned_users:
			user = ban_entry.user
			await ctx.guild.unban(user)

			return				
		for row in await self.db.settings.find({"server_id": ctx.guild.id}):
			if row["logchannel"] != 0:
				emb = discord.Embed(title=lan1, colour=discord.Color.red())
				emb.set_author(name=member.name, icon_url=member.avatar_url)
				emb.add_field(name=lan2, value=member.mention)
				emb.add_field(name=lan4, value=ctx.message.author.mention, inline=False)
				channel_log = self.client.get_channel(row['logchannel'])
				await channel_log.send(embed=emb)
				await ctx.message.add_reaction('✅')	
			else:
				await ctx.message.add_reaction('✅')

	@commands.command(aliases = ['анмьют'])
	@commands.has_permissions(manage_messages = True)
	async def unmute(self, ctx, member: discord.Member):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Инфо о размьюте'
			lan2 = 'Нарушитель'
			lan4 = 'Модератор'
		else:
			lan1 = 'Unmute info'
			lan2 = 'Intruder'
			lan4 = 'Moderator'
		if discord.Member is None:
			await ctx.send('Выберите пользователя, которого стоит убрать из мута')
		else:
			for row in await self.db.settings.find({"server_id": ctx.guild.id}):
				mute_role = discord.utils.get(ctx.message.guild.roles, name=row["muterole"])
				await member.remove_roles(mute_role)
				if row["logchannel"] != 0:
					emb = discord.Embed(title=lan1, colour=discord.Color.red())
					emb.set_author(name=member.name, icon_url=member.avatar_url)
					emb.add_field(name=lan2, value=member.mention)
					emb.add_field(name=lan4, value=ctx.message.author.mention, inline=False)
					channel_log = self.client.get_channel(row['logchannel'])
					await channel_log.send(embed=emb)
					await ctx.message.add_reaction('✅')	
				else:
					await ctx.message.add_reaction('✅')

	@commands.command(aliases = ['изменитьник'])
	@commands.has_permissions(change_nickname = True)
	async def renameMember(self, ctx, member: discord.Member = None, *, name = None):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Вы не указали человека, у которого нужно изменить ник!'
		else:
			lan1 ='You didnt specify the person to change the nickname for!'
		if member is None:
			await ctx.send(embed = discord.Embed(
				description = lan1,
				color = discord.Color.red()
			))

		if name != None:
			await member.edit(nick = name)
			await ctx.message.add_reaction("✅")
		else:
			await member.edit(nick = member.name)
			await ctx.message.add_reaction("✅")

	@commands.command(aliases = ['проверкабазы'])
	@commands.cooldown(1, 1500, commands.BucketType.guild)
	@commands.has_permissions(administrator = True)
	async def recheck_base(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Проверка пользователей'
			lan2 = 'Всего проверено'
			lan3 = 'Добавлено'
			lan4 = '. Уже были добавлены'
		else:
			lan1 = 'Verification of users'
			lan2 = 'Total checked'
			lan3 = 'Added'
			lan4 = '. Already been added'
		allmembers = 0
		goodadd = 0
		badadd = 0
		for member in ctx.guild.members: 
			if await self.db.users.find({"ids": member.id, "server_id": ctx.guild.id}) is None:
				await self.db.users.insert_one({
					"server_id": ctx.guild.id,
					"ids": member.id,
					"warns": 0,
					"prewarn": 0,
					"wins": 0,
					"cash": 0,
					"rep": 0,
					"lvl": 1,
					"exp": 0,
					"hp": 90,
					"mana": 100,
					"maxattack": 50,
					"minattack": 40
					})
				goodadd += 1
			else:
				badadd += 1
		allmembers = goodadd + badadd
		emb = discord.Embed(title = lan1, description = f"{lan2} {allmembers} {lan3} {goodadd} {lan4} {badadd}")
		await ctx.send(embed=emb)

	@commands.command(aliases = ['мьют'])
	@commands.has_permissions(manage_messages = True)
	async def mute(self, ctx, member: discord.Member, arg: str, *, reason = None):
		for row in await self.db.settings.find({"server_id": ctx.guild.id}):
			if row['logchannel'] != 0:
				if str(ctx.guild.region) == 'russia':
					lan1 = 'уже замьючен!'
					lan2 = 'Правильное использование команды: `mute @пользователь 10m причина`'
					lan3 = 'является создателем этого сервера!'
					lan4 = 'Я не могу замутить самого себя!'
					lan5 = 'Ты не можешь замутить человека с позицией выше твоей!'
					lan6 = 'Напомню, суицид - это не выход!'
					lan7 = 'Я не могу замутить'
					lan8 = 'так как его роль выше моей!'
					lan9 = 'так как роль мута выше моей!'
					lan10 = '***Выдал:***'
					lan11 = '***Тип наказания:***'
					lan12 = '***Время выдачи:***'
					lan13 = '***Причина:***'
					lan14 = 'Не указана.'
					lan15 = 'Не отвечайте на это сообщение.'
				else:
					lan1 = 'already loaded!'
					lan2 = 'Correct use of the command: `mute @user 10m reason`'
					lan3 = 'is the Creator of this server!'
					lan4 = 'I cant mess with myself! '
					lan5 = 'You cant hook up with someone with a higher position than you!'
					lan6 =' let me Remind you, suicide is not an option! '
					lan7 = 'I cant hook up'
					lan8 = 'since his role is higher than mine!'
					lan9 =' since the role of the Muta is higher than mine!'
					lan10 = '***Give out:***'
					lan11 = '***Type of punishment:***'
					lan12 = '***Time of issue:***'
					lan13 = '***Reason:***'
					lan14 = 'Not specified.'
					lan15 = 'Do not respond to this message.'
				channel_log = self.client.get_channel(row['logchannel'])
				await ctx.message.delete()
				now_date = datetime.datetime.now()
				mute_role = discord.utils.get(ctx.message.guild.roles, name=row["muterole"])
				if not mute_role:
					mute_role = await ctx.guild.create_role(name = row["muterole"], permissions = discord.Permissions(send_messages=False), color=discord.Color.red())
					for i in ctx.guild.channels:
						await i.set_permissions(mute_role, read_messages=True, send_messages=False)
					mute_role = discord.utils.get(ctx.message.guild.roles, name=row["muterole"])
				if mute_role in member.roles:
					return await ctx.send(
						embed=discord.Embed(
							description=f'**:warning: {member.mention}, {lan1}**',
							color=0x800080))
				if not member and not arg:
					return await ctx.send(embed=discord.Embed(
						description=f'**:warning: {lan2}**',
						color=0x800080))
				if member.id == ctx.guild.owner.id:
					return await ctx.send(embed=discord.Embed(
						description=f'**:warning: {member.mention}, {lan3}**',
						color=0x800080))
				if member.id == ctx.guild.me.id:
					return await ctx.send(
						embed=discord.Embed(description=f'**:warning: {lan4}**', color=0x800080))
				if ctx.author.top_role.position < member.top_role.position:
					return await ctx.send(embed=discord.Embed(
						description=f'**:warning: {lan5}**',
						color=0x800080))
				if member.id == ctx.author.id:
					return await ctx.send(
						embed=discord.Embed(description=f'**:warning: {lan6}**', color=0x800080))
				if member.top_role > ctx.guild.me.top_role:
					return await ctx.send(embed=discord.Embed(
						description=f'**:warning: {lan7} {member.mention}, {lan8}**',
						color=0x800080))
				if mute_role.position > ctx.guild.me.top_role.position:
					return await ctx.send(embed=discord.Embed(
						description=f'**:warning: {lan7} {member.mention}, {lan9}**',
						color=0x800080))
				emb = discord.Embed(title='Mute', colour=discord.Color.red())
				emb.set_author(name=member.name, icon_url=member.avatar_url)
				emb.add_field(name=lan10, value=ctx.author.display_name, inline=False)
				emb.add_field(name=lan11, value='Mute', inline=False)
				emb.add_field(name=lan12, value=now_date, inline=False)
				amount = int(arg[:-1])
				tip = arg[-1]
				if tip == "s":

					if reason is None:
						emb.add_field(name= lan13, value=lan14, inline=False)
						await member.add_roles(mute_role, reason = lan14, atomic=True)
						await ctx.message.add_reaction('✅')
					else:
						emb.add_field(name = lan13, value = reason, inline=False)
						await member.add_roles(mute_role, reason=reason, atomic=True)
						await ctx.message.add_reaction('✅')
					emb.set_footer(text = lan15, icon_url=ctx.author.avatar_url)
					await channel_log.send(embed=emb)
					await member.send(embed=emb)
					await asyncio.sleep(amount)

				elif tip == "m":

					if reason is None:
						emb.add_field(name= lan13, value=lan14, inline=False)
						await member.add_roles(mute_role, reason = lan14, atomic=True)
						await ctx.message.add_reaction('✅')
					else:
						emb.add_field(name = lan13, value = reason, inline=False)
						await member.add_roles(mute_role, reason=reason, atomic=True)
						await ctx.message.add_reaction('✅')
					emb.set_footer(text = lan15, icon_url=ctx.author.avatar_url)
					await channel_log.send(embed=emb)
					await member.send(embed=emb)
					await asyncio.sleep(amount * 60)

				elif tip == "h":

					if reason is None:
						emb.add_field(name= lan13, value=lan14, inline=False)
						await member.add_roles(mute_role, reason = lan14, atomic=True)
						await ctx.message.add_reaction('✅')
					else:
						emb.add_field(name = lan13, value = reason, inline=False)
						await member.add_roles(mute_role, reason=reason, atomic=True)
						await ctx.message.add_reaction('✅')
					emb.set_footer(text = lan15, icon_url=ctx.author.avatar_url)
					await channel_log.send(embed=emb)
					await member.send(embed=emb)
					await asyncio.sleep(amount * 60 * 60)

				elif tip == "d":
					if reason is None:
						emb.add_field(name = lan13, value=lan14, inline=False)
						await member.add_roles(mute_role, reason = lan14, atomic=True)
						await ctx.message.add_reaction('✅')
					else:
						emb.add_field(name = lan13, value = reason, inline=False)
						await member.add_roles(mute_role, reason=reason, atomic=True)
						await ctx.message.add_reaction('✅')
					emb.set_footer(text = lan15, icon_url=ctx.author.avatar_url)
					await channel_log.send(embed=emb)
					await member.send(embed=emb)
					await asyncio.sleep(amount * 60 * 60 * 24)
				await member.remove_roles(mute_role)

			elif row['logchannel'] is None:
				await ctx.message.add_reaction('✅')

def setup(client):
	client.add_cog(User(client))
