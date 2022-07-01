import asyncio
import datetime
import discord
import humanize
import itertools
import re
import sys
import traceback
import wavelink
from discord.ext import commands, tasks
from typing import Union
 
PREFIX = "YOUR_PREFIX_HERE"
TOKEN = "YOUR_TOKEN_HERE"
 
RURL = re.compile('https?:\/\/(?:www\.)?.+')
 
class Bot(commands.Bot):
	def __init__(self):
		super(Bot, self).__init__(command_prefix=commands.when_mentioned_or(PREFIX), intents = discord.Intents.all())
 
		self.add_cog(Music(self))
		
	async def on_ready(self):
		print(f'Logged in as {self.user.name} | {self.user.id}')
		
class MusicController:
	def __init__(self, bot, guild_id):
		self.bot = bot
		self.guild_id = guild_id
		self.channel = None
 
		self.next = asyncio.Event()
		self.queue = asyncio.Queue()
 
		self.volume = 40
		self.now_playing = None
 
		self.bot.loop.create_task(self.controller_loop())
		
	async def controller_loop(self):
		await self.bot.wait_until_ready()
 
		player = self.bot.wavelink.get_player(self.guild_id)
		await player.set_volume(self.volume)
 
		while True:
			if self.now_playing:
				await self.now_playing.delete()
 
			self.next.clear()
 
			song = await self.queue.get()
			await player.play(song)
			self.now_playing = await self.channel.send(f'Now playing: `{song}`')
 
			await self.next.wait()
			
class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.controllers = {}
 
		if not hasattr(bot, 'wavelink'):
			self.bot.wavelink = wavelink.Client(bot=self.bot)
 
		self.bot.loop.create_task(self.start_nodes())
 
	async def start_nodes(self):
		await self.bot.wait_until_ready()
 
		node = await self.bot.wavelink.initiate_node(host='localhost',
													port=2333,
													rest_uri='',
													password='',
													identifier=f'{self.bot.user}',
													region='us_central')
		
		node.set_hook(self.on_event_hook)
		
	async def on_event_hook(self, event):
		if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
			controller = self.get_controller(event.player)
			controller.next.set()
 
	def get_controller(self, value: Union[commands.Context, wavelink.Player]):
		if isinstance(value, commands.Context):
			gid = value.guild.id
		else:
			gid = value.guild_id
 
		try:
			controller = self.controllers[gid]
		except KeyError:
			controller = MusicController(self.bot, gid)
			self.controllers[gid] = controller
 
		return controller
 
	async def cog_check(self, ctx):
		if not ctx.guild:
			raise commands.NoPrivateMessage
		return True
 
	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.NoPrivateMessage):
			try:
				return await ctx.send('Command cannot be used in DM')
			except discord.HTTPException:
				pass
 
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		
	@commands.command(name='join', aliases = ["j"])
	async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
		if not channel:
			try:
				channel = ctx.author.voice.channel
			except AttributeError:
				return await ctx.send('You not in voice, join in any voice or use ID of channel')
 
		player = self.bot.wavelink.get_player(ctx.guild.id)
		await ctx.send(f'Connect to **`{channel.name}`**', delete_after=15)
		await player.connect(channel.id)
 
		controller = self.get_controller(ctx)
		controller.channel = ctx.channel
 
	@commands.command()
	@commands.is_owner()
	async def servers(self, ctx):
		desc = ""
		desc += f"Servers: {len(self.bot.guilds)}\n"
		for guild in self.bot.guilds:
			desc += f"Name: {guild.name} - ID: {guild.id} - Members: {len(guild.members)}\n"
 
		await ctx.send(embed = discord.Embed(title = "Bot servers", description = desc, color = 0x00ff00))
 
	@commands.command(aliases = ["p"])
	async def play(self, ctx, *, query: str):
		if not RURL.match(query):
			query = f'ytsearch:{query}'
 
		tracks = await self.bot.wavelink.get_tracks(query)
 
		if not tracks:
			return await ctx.send('Not found')
 
		player = self.bot.wavelink.get_player(ctx.guild.id)
		if not player.is_connected:
			await ctx.invoke(self.connect_)
 
		track = tracks[0]
 
		controller = self.get_controller(ctx)
		await controller.queue.put(track)
		await ctx.send(f'`{str(track)}` added to the queue', delete_after=15)
 
	@commands.command()
	async def pause(self, ctx):
		player = self.bot.wavelink.get_player(ctx.guild.id)
		if not player.is_playing:
			return await ctx.send('No songs playing at this moment', delete_after=15)
 
		await ctx.send('Song paused', delete_after=15)
		await player.set_pause(True)
 
	@commands.command()
	async def resume(self, ctx):
		player = self.bot.wavelink.get_player(ctx.guild.id)
		if not player.paused:
			return await ctx.send('Song not paused at this moment', delete_after=15)
 
		await ctx.send('Resumed', delete_after=15)
		await player.set_pause(False)
 
	@commands.command(aliases = ["s"])
	async def skip(self, ctx):       
		player = self.bot.wavelink.get_player(ctx.guild.id)
 
		if not player.is_playing:
			return await ctx.send('No songs playing at this moment', delete_after=15)
 
		await ctx.send('Song skipped', delete_after=15)
		await player.stop()
 
	@commands.command(aliases = ["leave_all", "la"])
	@commands.is_owner()
	async def leave_servers(self, ctx):
		for guild in self.bot.guilds:
			player = self.bot.wavelink.get_player(guild.id)
 
			try:
				del self.controllers[guild.id]
			except KeyError:
				await player.disconnect()
 
			await player.disconnect()
		await ctx.send("Left from all voices")
 
	@commands.command()
	@commands.is_owner()
	async def send(self, ctx, *, message: str):
		for guild in self.bot.guilds:
			for channel in guild.text_channels:
				if "чат" in channel.name.lower() or "chat" in channel.name.lower() or "general" in channel.name.lower():
					try:
						await channel.send(message)
					except:
						continue
						
	@commands.command()
	async def volume(self, ctx, *, vol: int = None):
		if not ctx.author.guild_permissions.administrator:
			return await ctx.send("You need administrator permission to use that")
		player = self.bot.wavelink.get_player(ctx.guild.id)
		controller = self.get_controller(ctx)
 
		if not vol:
			return await ctx.send(f"Current volume: {controller.volume}")
 
		vol = max(min(vol, 1000), 0)
		controller.volume = vol
 
		await ctx.send(f'Volume set to `{vol}`')
		await player.set_volume(vol)
 
	@commands.command(aliases=['np', 'current'])
	async def now_playing(self, ctx):      
		player = self.bot.wavelink.get_player(ctx.guild.id)
 
		if not player.current:
			return await ctx.send('No songs playing at this moment')
 
		controller = self.get_controller(ctx)
		await controller.now_playing.delete()
 
		controller.now_playing = await ctx.send(f'Now playing: `{player.current}`')
 
	@commands.command(aliases=['q'])
	async def queue(self, ctx):   
		player = self.bot.wavelink.get_player(ctx.guild.id)
		controller = self.get_controller(ctx)
 
		if not player.current or not controller.queue._queue:
			return await ctx.send('There is no queue', delete_after=20)
 
		upcoming = list(itertools.islice(controller.queue._queue, 0, 5))
 
		fmt = '\n'.join(f'**`{str(song)}`**' for song in upcoming)
		embed = discord.Embed(title=f'Queue length: {len(upcoming)}', description=fmt)
 
		await ctx.send(embed=embed)
 
	@commands.command(aliases=['disconnect', 'dc'])
	async def leave(self, ctx):       
		for vc in ctx.guild.voice_channels:
			members = [member.id for member in vc.members]
			if self.bot.user.id in members and ctx.author.id not in members:
				return await ctx.send("You need to be in voice with bot to use this")
 
		player = self.bot.wavelink.get_player(ctx.guild.id)
 
		try:
			del self.controllers[ctx.guild.id]
		except KeyError:
			await player.disconnect()
			return await ctx.send('Bot not in voice')
 
		await player.disconnect()
		await ctx.send('Disconnected', delete_after=20)
 
	@commands.command()
	async def info(self, ctx):       
		player = self.bot.wavelink.get_player(ctx.guild.id)
		node = player.node
 
		used = humanize.naturalsize(node.stats.memory_used)
		total = humanize.naturalsize(node.stats.memory_allocated)
		free = humanize.naturalsize(node.stats.memory_free)
		cpu = node.stats.cpu_cores
 
		fmt = f'**{self.bot.user.name}:**\nAmount of nodes: `{len(self.bot.wavelink.nodes)}`\nBest using node: `{self.bot.wavelink.get_best_node().__repr__().split("(")[0][:-3]}`\nBot using `{len(self.bot.wavelink.players)}` nodes\n`{node.stats.players}` nodes\n`{node.stats.playing_players}` nodes now playing\n\nBot\'s server memory: `{used}/{total}` | `({free} free)`\nCPU of server: `{cpu}`\n\nServer online: `{str(datetime.timedelta(milliseconds=node.stats.uptime)).split(".")[0]}`'
		await ctx.send(fmt)
