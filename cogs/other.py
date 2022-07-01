import discord
from discord.ext import commands
from discord import Spotify
import googletrans 
from googletrans import Translator
from bs4 import BeautifulSoup
import time
import json
import os
import requests
from requests import get
from datetime import datetime
import asyncio
import random
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import pyshorteners
import pydantic
from PIL import Image, ImageDraw, ImageFont, ImageOps
from covid import Covid
import io

class User(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def spotify(self, ctx, member: discord.Member = None):
		if str(ctx.guild.region) == 'russia':
			lan = 'не слушает Spotify :mute:'
			lan1 = 'слушает Spotify :notes:'
			lan2 = 'Песня'
			lan3 = 'Исполнитель'
			lan4 = 'Альбом'
			lan5 = 'Пати ID'
			lan6 = 'Трек ID'
			lan7 = 'Длительность аудио'
		else:
			lan = 'doesn t listen to Spotify :mute:'
			lan1 = 'listens to Spotify :notes:'
			lan2 = 'Song'
			lan3 = 'Executor'
			lan4 = 'Album'
			lan5 = 'Party ID'
			lan6 = 'Track ID'
			lan7 = 'The length of audio'
		member = member or ctx.author
		def strfdelta(tdelta, fmt):
			d = {"days": tdelta.days}
			d["hours"], rem = divmod(tdelta.seconds, 3600)
			d["minutes"], d["seconds"] = divmod(rem, 60)
			return fmt.format(**d)
		spot = next((activity for activity in member.activities if isinstance(activity, discord.Spotify)), None)

		if not spot:
			return await ctx.send(f"{member.mention}, {lan}")

		embed = discord.Embed(title = f"{member}, {lan1}", color = spot.color)

		embed.add_field(name = lan2, value = spot.title)
		embed.add_field(name = lan3, value = spot.artist)
		embed.add_field(name = lan4, value = spot.album)
		embed.add_field(name = lan5, value = spot.party_id[8:])
		embed.add_field(name = lan6, value = spot.track_id)
		embed.add_field(name = lan7, value = strfdelta(spot.duration, '{hours:02}:{minutes:02}:{seconds:02}'))
		embed.set_thumbnail(url = spot.album_cover_url)

		await ctx.send(embed = embed)

	@commands.command()
	async def weather(self, ctx,  *, city):
		data = get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID=fb9df86d9c484eba8a69269cfb0beac9").json()
		cleared_data = {
			'City': data['name'],
			'Time': datetime.utcfromtimestamp(data['dt']).strftime('%H:%M:%S'),
			'Weather': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
			'Temperature': f"{data['main']['temp']}°C",
			'Feels like': f"{data['main']['feels_like']}°C",
			'Min temperature': f"{data['main']['temp_min']}°C",
			'Max temperature': f"{data['main']['temp_max']}°C",
			'Humidity': f"{data['main']['humidity']}%",
			'Pressure': f"{data['main']['pressure']}Pa",
			'Clouds': f"{data['clouds']['all']}%",
			'Wind': f"{data['wind']['speed']} km/h",
			'Sunset': datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
			'Sunrise': datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
		}
		embed = discord.Embed(title=f":white_sun_small_cloud: Weather in {cleared_data['City']}", color=0x3498db)
		for key, value in cleared_data.items():
			embed.add_field(name=key, value=value)
		await ctx.send(embed=embed)

	@commands.command()
	async def restr(self, ctx,*,message=None):
		a = {"q":"й","w":"ц","e":"у","r":"к","t":"е","y":"н","u":"г","i":"ш","o":"щ","p":"з","[":"х","{":"х","}":"ъ","]":"ъ","a":"ф","s":"ы","d":"в","f":"а","g":"п","h":"р","j":"о","k":"л","l":"д",":":"ж",";":"ж",'"':"э","'":"э","z":"я","x":"ч","c":"с","v":"м","b":"и","n":"т","m":"ь","<":"б",",":"б",">":"ю",".":"ю","?":",","/":".","`":"ё","~":"ё"," ":" "}
		if message is None:
			await ctx.send("Ты ...")
		else:
			itog = ""
			errors = ""
			for i in message:
				if i.lower() in a:
					itog += a[i.lower()]
				else:
					errors += f"`{i}` "
				if len(errors) <= 0:
					errors_itog=""
				else:
					errors_itog=f"\nЯ не смог их перевести: {errors}"
		if len(itog) <= 0:
			itog_new= "Перевода нет!"
		else:
			itog_new=f"Перевод: {itog}"
		await ctx.send(f"{itog_new}{errors_itog}")

	@commands.command()
	async def youtube(self, ctx, *, query: str):

		req = requests.get(
			('https://www.googleapis.com/youtube/v3/search?part=id&maxResults=1'
			 '&order=relevance&q={}&relevanceLanguage=en&safeSearch=moderate&type=video'
			 '&videoDimension=2d&fields=items%2Fid%2FvideoId&key=')
			.format(query) + "AIzaSyC_viihkRiUg3N5bv0DRvOrmaNdUNJ852U")
		await ctx.send('https://www.youtube.com/watch?v={}'.format(req.json()['items'][0]['id']['videoId']))

	@commands.command()
	async def translate(self, ctx, dest, *, txt: str):
		if str(ctx.guild.region) == 'russia':
			lan = '**Перевод твоего сообщения**'
			lan1 = '**Твое сообщение:** -'
			lan2 = '**Перевод:** -'
			lan3 = 'данного **языка** не существует, я отправлю список **языков** тебе в **лс** :x:'
			lan4 = '**Список всех языков:**'
		else:
			lan = '**Translation of your message**'
			lan1 = '**Your message:** -'
			lan2 = '**Translation:** -'
			lan3 = 'this **language** does not exist, I will send a list of **languages** to you in **BOS** :x:'
			lan4 = '**List of all languages:**'
		try:
			translator = Translator()
			result = translator.translate(txt, dest = dest)

			embed = discord.Embed(title = lan,
							  description = f"{lan1} {result.origin}\n\n"
										  f"{lan2} {result.text}\n\n",
							timestamp = datetime.utcnow(), color = 0x00FF00)
			embed.set_footer(icon_url = self.client.user.avatar_url)
			embed.set_thumbnail(
				url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/Google_Translate_logo_%28old%29.png')
	
			await ctx.send(embed = embed)

		except ValueError:
			embed = discord.Embed(
				description = f':x: {ctx.author.mention}, {lan3}',
				timestamp = datetime.utcnow(), color = 0xff0000)

			embed.set_author(icon_url='https://www.flaticon.com/premium-icon/icons/svg/1828/1828665.svg',
							 name = 'Error')
			embed.set_footer(icon_url = self.client.user.avatar_url)

			await ctx.send(embed = embed)

			languages = ", ".join(googletrans.LANGUAGES)

			embed = discord.Embed(description = f'{lan4} {languages}', timestamp = datetime.utcnow(),
								  color = 0x00FF00)

			embed.set_footer(icon_url = self.client.user.avatar_url)

			await ctx.author.send(embed = embed)

	@commands.command()
	async def wiki(self, ctx, *, query: str):
		if str(ctx.guild.region) == 'russia':
			lan0 = 'Пожалуйста, подождите. . .'
			lan = 'По запросу **'
			lan1 = '** ничего не найдено :confused:'
		else:
			lan0 = 'Please wait. . .'
			lan = 'on request **'
			lan1 = '** nothing found :confused:'
		msg = await ctx.send(lan0)
		sea = requests.get(
			('https://ru.wikipedia.org//w/api.php?action=query'
			 '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
			).format(query)).json()['query']

		if sea['searchinfo']['totalhits'] == 0:
			await ctx.send(f'{lan}"{query}"{lan1}')
		else:
			for x in range(len(sea['search'])):
				article = sea['search'][x]['title']
				req = requests.get('https://ru.wikipedia.org//w/api.php?action=query'
								   '&utf8=1&redirects&format=json&prop=info|images'
								   '&inprop=url&titles={}'.format(article)).json()['query']['pages']
				if str(list(req)[0]) != "-1":
					break
			article = req[list(req)[0]]['title']
			arturl = req[list(req)[0]]['fullurl']
			artdesc = requests.get('https://ru.wikipedia.org/api/rest_v1/page/summary/' + article).json()['extract']
			embed = discord.Embed(title = article, url = arturl, description = artdesc, timestamp = datetime.utcnow(), color = 0x00ffff)
			embed.set_author(name = 'Google | Wikipedia', url = 'https://en.wikipedia.org/', icon_url = 'https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
			embed.set_footer(icon_url = self.client.user.avatar_url)

			await msg.delete()
			await ctx.send(embed = embed)

	translator = Translator()

	@commands.command()
	@commands.cooldown(1, 30, commands.BucketType.user)
	async def google(self, ctx, *, question = None):
		if str(ctx.guild.region) == 'russia':
			lan0 = 'Введите запрос!'
			lan = 'Результаты поиска по запросу:'
			lan1 = 'Ссылка'
		else:
			lan0 = 'Enter a request!'
			lan = 'search results for the query:'
			lan1 = 'Link'
		if question is None:
			await ctx.send(lan0)
		else:
			url = f'https://www.google.com/search?b-d&q=' + str(question).replace(' ', '+')
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
				'accept': '*/*'
			}

			r = requests.get(url, headers = headers)
			soup = BeautifulSoup(r.content, 'html.parser')
			items = soup.findAll('div', class_ = "rc")

			comps = []

			for item in items:
				comps.append({
						'link': item.find('a').get('href'),
						'title': item.find('h3', class_ = 'LC20lb DKV0Md').get_text(strip = True)
					})
		
			for comp in comps:
				link = comp['link']
				emb = discord.Embed(description=f'{lan} {question}', color = 0x00ffff)
				emb.set_author(name = 'Google', url = 'https://google.com/', icon_url = 'https://www.apkappbox.com/wp-content/uploads/2018/05/google-llc-tools-768x768.png')
				emb.add_field(
						name = comp['title'],
						value = f'[{lan1}]({link})',
						inline = False
					)

		await ctx.send(embed = emb)

	@commands.command()
	@commands.cooldown(1, 30, commands.BucketType.user)
	async def short(self, ctx, url : str = None):
		if str(ctx.guild.region) == 'russia':
			lan = 'Система сокращения ссылок'
			lan1 = 'Ошибка | Укажите ссылку которую хотите укоротить'
			lan2 = 'Ваша ссылка готова : '
		else:
			lan = 'Link shortening system'
			lan1 = 'Error | Specify the link you want to shorten'
			lan2 = 'Your link is ready : '
		if url is None:
			await ctx.send(embed = discord.Embed(
					title       = lan,
					description = lan1,
					colour      = discord.Color.red()
				))
		else:
			shortener = pyshorteners.Shortener()
			short_url = shortener.tinyurl.short(url)
			await ctx.send(f"{lan2} {short_url}")

	@commands.command()
	async def whoyou(self, ctx, member: discord.Member = None, idk: str = None):
		if str(ctx.guild.region) == 'russia':
			lan = 'Введите имя пользователя'
			lan1 = 'Введите параметр рандома'
			lan2 = ', на'
			lan3 = '% гeй'
			lan4 = '% является Python программистом'
			lan5 = '% является C программистом'
			lan6 = '% является C++ программистом'
		else:
			lan = 'Enter the user name'
			lan1 = 'Enter the random parameter'
			lan2 = ', on'
			lan3 = '% - gay'
			lan4 = '% - is a Python programmer'
			lan5 = '% - is a C programmer'
			lan6 = '% - is a C++ programmer'
		if member is None:
			memver = ctx.author
		elif idk is None:
			await ctx.send(f'{lan1} - gay, python, c, c++')
		elif idk == 'gay':
			gayrandom = random.randint(1, 100)
			await ctx.send(f'{member.mention}{lan2} {gayrandom}{lan3}')
		elif idk == 'python':
			pythonrandom = random.randint(1, 100)
			await ctx.send(f'{member.mention}{lan2} {pythonrandom}{lan4}')
		elif idk == 'c':
			crandom = random.randint(1, 100)
			await ctx.send(f'{member.mention}{lan2} {crandom}{lan5}')
		elif idk == 'c++':
			ccrandom = random.randint(1, 100)
			await ctx.send(f'{member.mention}{lan2} {ccrandom}{lan6}')

	@commands.command(aliases=['calculator'])
	async def calc(self, ctx, *, exp = None):
		if str(ctx.guild.id) == 'russia':
			lan1 = '**Укажите пример!**'
			lan2 = 'Калькулятор'
			lan3 = 'Задача:'
			lan4 = 'Решение:'
			lan5 = '**Это калькулятор, тексту тут нет места 0_o**'
		else:
			lan1 = '**Specify an example!**'
			lan2 = 'Calculator'
			lan3 = 'Problem:'
			lan4 = 'Solution:'
			lan5 = '**This is a calculator, there is no place for text 0_o**'
		if exp is None:
			await ctx.send(lan1)
		else:
			link = 'http://api.mathjs.org/v4/'

			data = {"expr": [exp]}

			try:
				re = requests.get(link, params=data)
				responce = re.json()

				e = discord.Embed(title=lan2, color = discord.Color.dark_gray())
				e.add_field(name=lan3, value=exp)
				e.add_field(name=lan4, value=str(responce))
				await ctx.send(embed=e)
			except:
				await ctx.send(lan5)

	@commands.command()
	async def emoji_flex(self, ctx, emoji: discord.Emoji = None):
		if str(ctx.guild.id) == 'russia':
			lan1 = 'укажи **эмодзи**, о которым хочешь узнать **информацию**'
			lan2 = 'Название эмодзи:'
			lan3 = 'Автор:'
			lan4 = 'Дата добавления:'
			lan5 = 'ID эмодзи:'
			lan6 = 'Эмодзи'
		else:
			lan1 = ' specify * * Emoji** that you want to know * * information about**'
			lan2 = 'Emoji Name:'
			lan3 = 'Author:'
			lan4 = 'date added:'
			lan5 = 'Emoji ID:'
			lan6 = 'Emoji'
		if not emoji:
			e = discord.Embed(description = f":x: {ctx.author.mention}, {lan1} :x:", color = 0xFF0000)

			await ctx.send(embed = e)

		e = discord.Embed(description = f"[{lan6}]({emoji.url}) сервера - {emoji}", color = 0x00FF00)

		e.add_field(name = lan2, value = "**`{0}`**".format(emoji.name))
		e.add_field(name = lan3, value = "{0}".format((await ctx.guild.fetch_emoji(emoji.id)).user.mention))
		e.add_field(name = "‎‎‎‎", value = "‎‎‎‎")
		e.add_field(name = lan4, value = "**`{0}`**".format((emoji.created_at.date())))
		e.add_field(name = lan5, value = emoji.id)
		e.add_field(name = "‎‎‎‎", value = "‎‎‎‎")
		e.set_thumbnail(url = emoji.url)
		e.set_author(icon_url = 'https://www.flaticon.com/premium-icon/icons/svg/3084/3084443.svg', name = 'Satiricon | Emoji')
		e.timestamp = datetime.utcnow()

		await ctx.send(embed = e)

	@commands.command()
	async def embed_builder(self, ctx, *, arg = None):

		try:
			emb = discord.Embed()
			a = json.loads(arg.replace("'", '"'))
			
			if 'title' in a:
				emb.title = a['title']

			if 'plainText' in a:
				await ctx.send(a['plainText'])

			if 'description' in a:
				emb.description = a['description']

			if 'color' in a:
				emb.color = int('0x' + a['color'], 16)
			
			if 'author' in a:
				if 'icon_url' in a['author']:
					emb.set_author(name = a['author']['name'], icon_url = a['author']['icon_url'])

				else:
					emb.set_author(name = a['author']['name'])

			if 'footer' in a:
				if 'icon_url' in a['footer']:
					emb.set_footer(text = a['footer']['text'], icon_url = a['footer']['icon_url'])
				else:
					emb.set_footer(text = a['footer']['text'])

			if 'image' in a:
				emb.set_image(url = a['image'])

			if 'thumbnail' in a:
				emb.set_thumbnail(url = a['thumbnail'])
			
			if 'fields' in a:

				for x in a['fields']:

					emb.add_field(name = x['name'], value = x['value'], inline = x['inline'])

			await ctx.send(embed = emb)

		except:
			emb = discord.Embed(description = 'JSON Error!', timestamp = datetime.utcnow())
			emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
			await ctx.send(embed = emb)

	@commands.command()
	@commands.has_permissions(manage_channels=True)
	async def poll(self, message, stime: int = None, *, question=None):
		if str(message.guild.region) == 'russia':
			lan1 = 'Укажите тему голосования!'
			lan2 = 'Голосование'
			lan3 = 'Yes'
			lan4 = 'No'
			lan5 = 'Голосование закончено!'
			lan6 = 'Текст голосования:'
		else:
			lan1 = 'Specify the subject of the vote! '
			lan2 = 'Vote'
			lan3 = 'Yes'
			lan4 = 'No'
			lan5 = 'Voting is over!'
			lan6 = 'Voting Text:'
		if question is None:
			embed = discord.Embed(title="Error", description=lan1, color=discord.Color.red())
			await message.send(embed=embed)
		else:
			embed = discord.Embed(title=lan2, description=f"{question}\n:white_check_mark: - {lan3}\n:x: - {lan4}", color=discord.Color.green())
			msg = await message.send(embed=embed)
			react_list = ["❌", "✅"]
			for ra in react_list:
				await msg.add_reaction(ra)
			if stime > 10:
				await asyncio.sleep(stime)
				for ra1 in react_list:
					no = msg.reactions
				for ra2 in react_list[1]:
					yes = msg.reactions.count(ra2)
				emb = discord.Embed(title = lan5, description=f"{lan6} {question}\n{yes} {no}")
				await msg.edit(embed=emb, content=None)

	@commands.command(aliases = ['ковид'])
	async def covid_19(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Подтверждено:'
			lan2 = 'Сегодня:'
			lan3 = 'Выздоровело:'
			lan4 = 'Смертей:'
		else:
			lan1 = 'Confirmed:'
			lan2 = 'Today:'
			lan3 = 'Recovered:'
			lan4 =' Deaths:'
		covidl = Covid(source="worldometers")
		total_confirmed = covidl.get_total_confirmed_cases()
		total_recovered = covidl.get_total_recovered()
		total_deaths = covidl.get_total_deaths()
		count = 0

		embed = discord.Embed(
			title=f"TOP 6 COVID-19 Confirmed Cases",
			description=f"**{lan1}** {total_confirmed} \n **{lan2}** {total_recovered} \n **{lan4}** {total_deaths}"
		)

		for count in range(6):
			country = covidl.get_data()[count]['country']
			confirmed = covidl.get_data()[count]['confirmed']
			new_cases = covidl.get_data()[count]['new_cases']
			recovered = covidl.get_data()[count]['recovered']
			deaths = covidl.get_data()[count]['deaths']
			count += 1
			embed.add_field(name = f"#{count} {country}", value = f"**{lan1}** {confirmed} \n**{lan2}** {new_cases} \n**{lan3}** {recovered} \n**{lan4}** {deaths} \n")

		await ctx.send(embed=embed)

	@commands.command()
	async def hypixelplayer_test_1090930_anhave_token_invalid(self, ctx, name):
		key = 'token'
		r = requests.get(f'https://api.hypixel.net/player?key={key}&name={name}')
		bww = r.json()["player"]["stats"]["Bedwars"]["wins_bedwars"]
		sww = r.json()["player"]["stats"]["SkyWars"]["win_streak"]
		bwa = r.json()["player"]["stats"]["Bedwars"]["games_played_bedwars_1"]
		swa = r.json()["player"]["stats"]["SkyWars"]["games_played_skywars"]
		embed = discord.Embed(title=f"Information about {name} ")
		embed.add_field(name='BedWars', value=f'Wins: {bww} \n Games: {bwa}', inline=False)
		embed.add_field(name='SkyWars', value=f'Wins: {sww} \n Games: {swa}', inline=False)
		embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/hypixelserver/images/1/12/SkyWars_Hypixel_Logo_Spray.jpg/revision/latest/scale-to-width-down/340?cb=20180116022506")
		await ctx.send(embed=embed)

	@commands.command()
	async def dem(self, ctx, text1: str = None,*, text2: str = None):
		sds = random.randint(0, 9000)
		for file in ctx.message.attachments:
			fp = io.BytesIO()
			await file.save(fp = f'getphoto{sds}.jpg')

		img = Image.new('RGB', (1280, 1024), color=('#000000'))
		img_border = Image.new('RGB', (1060, 720), color=('#000000'))
		border = ImageOps.expand(img_border, border=2, fill='#ffffff')
		user_img = Image.open(f'getphoto{sds}.jpg').convert("RGBA").resize((1050, 710))
		img.paste(border, (111, 96))
		img.paste(user_img, (118, 103))
		drawer = ImageDraw.Draw(img)
		font_1 = ImageFont.truetype(font='times.ttf', size=60, encoding='UTF-8')
		font_2 = ImageFont.truetype(font='arialbd.ttf', size=30, encoding='UTF-8')
		size_1 = drawer.textsize(text1, font=font_1)
		drawer.text(((1280 - size_1[0]) / 2, 850), text1, fill=(240, 230, 210), font=font_1)
		size_2 = drawer.textsize(text2, font=font_2)
		drawer.text(((1280 - size_2[0]) / 2, 950), text2, fill=(240, 230, 210), font=font_2)
		img.save(f'result{sds}.jpg')

		await ctx.send(file = discord.File(fp = f'result{sds}.jpg'))
		os.remove(f'result{sds}.jpg')
		os.remove(f'getphoto{sds}.jpg')

	@commands.command()
	async def discord_status(self, ctx):
		site = requests.get("https://discordstatus.com")

		soup = BeautifulSoup(site, 'lxml')

		tag = soup.find("color-secondary")
		print(tag)
		await ctx.send(tag)

def setup(client):
	client.add_cog(User(client))