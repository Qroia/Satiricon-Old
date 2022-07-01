import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import urllib
import random
import os
import requests

def prepare_mask(size, antialias = 2):
	mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
	ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
	return mask.resize(size, Image.ANTIALIAS)

# Обрезает и масштабирует изображение под заданный размер.
# Вообще, немногим отличается от .thumbnail, но по крайней мере
# у меня результат получается куда лучше.
def crop(im, s):
	w, h = im.size
	k = w / s[0] - h / s[1]
	if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
	elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
	return im.resize(s, Image.ANTIALIAS)

class profile(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.db = MongoClient("")["server"]

	@commands.command()
	async def profile(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		if await self.db.users.count_documents({"ids": member.id, "server_id": ctx.guild.id}) > 0:
			for row in await self.db.users.find({"ids": member.id, "server_id": ctx.guild.id}):

				indificator = random.randint(3475, 349478)
				image_general = Image.open('./picture/level_design/lvl_general.png').convert("RGBA")
				drawer = ImageDraw.Draw(image_general)

				response = requests.get(member.avatar_url_as(format = 'png'), stream = True).raw
				img = Image.open(response)

				img.save(f'avatar{indificator}.png')

				size = (223, 223)

				im = Image.open(f'avatar{indificator}.png')
				im = crop(im, size)
				im.putalpha(prepare_mask(size, 4))
				im.save(f'avatars{indificator}.png')
				img_avatars = Image.open(f'avatars{indificator}.png')
				image_general.paste(img_avatars, (795, 790), mask=img_avatars)

				lvl = row["lvl"]
				cash = row["cash"]
				xp = row["exp"]
				rep = row["rep"]
				hp = row["hp"]
				mindamage = row["minattack"]
				maxdamage = row["maxattack"]

				xall = ((lvl * 50 + 50) * (lvl + 1))
				x1 = round((int(xp) / int(xall)) * 100)

				font_header = ImageFont.truetype(font='BAHNSCHRIFT 5.TTF', size = 600, encoding='UTF-8')
				font_nick = ImageFont.truetype(font='BAHNSCHRIFT 5.TTF', size = 940, encoding='UTF-8')
				font_rep = ImageFont.truetype(font='BAHNSCHRIFT 5.TTF', size = 390, encoding='UTF-8')
				font_xp = ImageFont.truetype(font='BAHNSCHRIFT 5.TTF', size = 720, encoding='UTF-8')
				font_about = ImageFont.truetype(font='BAHNSCHRIFT 5.TTF', size = 520, encoding='UTF-8')
				font_damage = ImageFont.truetype(font='BAHNSCHRIFT 5.TTF', size = 570, encoding='UTF-8')
				font_hp = ImageFont.truetype(font='BAHNSCHRIFT 5.TTF', size = 460, encoding='UTF-8')

				if x1 in range(0, 5):
					img_status = Image.open('./picture/level_design/status_get_1-02.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(5, 10):
					img_status = Image.open('./picture/level_design/status_get_2-03.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(10, 13):
					img_status = Image.open('./picture/level_design/status_get_3-04.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(13, 20):
					img_status = Image.open('./picture/level_design/status_get_4-05.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(20, 29):
					img_status = Image.open('./picture/level_design/status_get_5-06.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(29, 36):
					img_status = Image.open('./picture/level_design/status_get_6-07.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(37, 44):
					img_status = Image.open('./picture/level_design/status_get_7-08.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(45, 56):
					img_status = Image.open('./picture/level_design/status_get_8-09.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(56, 68):
					img_status = Image.open('./picture/level_design/status_get_9-10.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(68, 75):
					img_status = Image.open('./picture/level_design/status_get_10-11.png')
					image_general.paste(img_status, (200, 338), mask=img_status)
				elif x1 in range(75, 100):
					img_status = Image.open('./picture/level_design/status_get_11-12.png')
					image_general.paste(img_status, (200, 338), mask=img_status)

				drawer.text((403, 617), f'lvl {lvl}', font = font_header, fill = (252,150,75,1))
				drawer.text((816, 518), f'{member.nick}', font = font_nick, fill = (252,150,75,1))
				drawer.text((1134, 245), f'{xp} EXP', font = font_xp, fill = (252,150,75,1))
				drawer.text((1162, 426), f'{rep} REP', font = font_rep, fill = (252,150,75,1))
				drawer.text((900, 364), f'{mindamage}-{maxdamage} Dam', font = font_damage, fill = (252,150,75,1))
				drawer.text((1122, 620), f'{cash} CH', font = font_about, fill = (252,150,75,1))
				drawer.text((1311, 505), f'{hp} HP', font = font_hp, fill = (252,150,75,1))
		
				image_general.save(f'result{indificator}.png')

				await ctx.send(file = discord.File(fp = f'result{indificator}.png'))

				os.remove(f'avatar{indificator}.png')
				os.remove(f'avatars{indificator}.png')
				os.remove(f'result{indificator}.png')

def setup(client):
	client.add_cog(profile(client))
