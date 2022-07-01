import discord
from discord.ext import commands
from discord.utils import get
import random

# HUG
img5 = "https://thumbs.gfycat.com/AlienatedFearfulJanenschia-small.gif"
img6 = "https://media1.tenor.com/images/b0de026a12e20137a654b5e2e65e2aed/tenor.gif?itemid=7552093"
img7 = "https://i.imgur.com/r9aU2xv.gif"
img8 = "https://media0.giphy.com/media/VHwgHhJLuWt0gjjUzf/source.gif"
img9 = "https://media2.giphy.com/media/lrr9rHuoJOE0w/200.gif"
img10 = "https://64.media.tumblr.com/18fdf4adcb5ad89f5469a91e860f80ba/tumblr_oltayyHynP1sy5k7wo1_400.gifv"
img11 = "https://25.media.tumblr.com/tumblr_ma7l17EWnk1rq65rlo1_500.gif"
img12 = "https://data.whicdn.com/images/45718472/original.gif"
img13 = "https://25.media.tumblr.com/2a3ec53a742008eb61979af6b7148e8d/tumblr_mt1cllxlBr1s2tbc6o1_500.gif"
img14 = "https://media.tenor.com/images/ca88f916b116711c60bb23b8eb608694/tenor.gif"
img15 = "https://otakulounge.files.wordpress.com/2019/02/picture1.gif"
img16 = "https://i.gifer.com/AHb9.gif"
img17 = "https://media0.giphy.com/media/sUIZWMnfd4Mb6/giphy.gif"
img18 = "https://dailysmscollection.org/wp-content/uploads/2019/01/anime-hug-gif.gif"
img19 = "https://i.gifer.com/RrVE.gif"
img20 = "https://cdn.myanimelist.net/s/common/uploaded_files/1461001090-874871175d32f838b0bdd601ee27a0e4.gif"
# HUG

# kill
kill1 = "https://image.myanimelist.net/ui/zG0rTj8uJvxu0II1PgJTq5bqvDOP1t3einEeaQJREqbdIBSx28bLyCZiGQoBUVl-FnPEFCPCYPfY0xxG1R90aTZMjbiL7Ni1FFqduX6bgPN-JnNgzEe7j8fx2j86CIjL"
kill2 = "https://i.gifer.com/KG69.gif"
kill3 = "https://data.whicdn.com/images/58491062/original.gif"
kill4 = "https://media1.tenor.com/images/408decc4b14f86084fd44164d089cf9e/tenor.gif?itemid=6164618"
kill5 = "https://i.gifer.com/5HfE.gif"
kill6 = "https://66.media.tumblr.com/55dd997f9e1c54e8a5ba4fc49dd561b4/tumblr_n7hmsjXIVS1rec90to1_500.gif"
kill7 = "https://pa1.narvii.com/6254/bb13298fa876cea3f09e960cc5f0e2d9036edc02_hq.gif"
kill8 = "https://pa1.narvii.com/7099/b222643af1da684f24c3612b3c8cda7ce3fa80c9r1-500-281_hq.gif"
kill9 = "https://pa1.narvii.com/6810/bb71e06e3a26dc29beae464f04faa9649ccc2d34_hq.gif"
kill10 = "https://pa1.narvii.com/6900/165820d289f316a511c57575cef0bc90dc7f3ae1r1-500-263_hq.gif"
kill11 = "https://i.gifer.com/SGY0.gif"

# kill

#cry
cry1 = "https://media1.tenor.com/images/3102c8c1f8152a2d0d2c9ed5e54626e3/tenor.gif?itemid=6070013"
cry2 = "https://i.gifer.com/338j.gif"
cry3 = "https://99px.ru/sstorage/86/2017/04/image_862404171524538146384.gif"
cry4 = "https://i.gifer.com/6Xgm.gif"
cry5 = "https://data.whicdn.com/images/308584789/original.gif"
cry6 = "https://pa1.narvii.com/6843/265092c191d9baff86871612571a3e36733397b8_hq.gif"
cry7 = "https://data.whicdn.com/images/86380780/original.gif"
cry8 = "https://data.whicdn.com/images/126334883/original.gif"
cry9 = "https://i1.wp.com/pa1.narvii.com/6477/9586256b453045752fd240cb1c8d224d7fbd83b5_hq.gif"
cry10 = "https://cdn130.picsart.com/253064933013202.gif"
cry11 = "https://pa1.narvii.com/6914/138b26c15a0a5437fe86c73a2c0598a602e56522r1-540-303_hq.gif"
cry12 = "https://data.whicdn.com/images/315702627/original.gif"
cry13 = "https://i.gifer.com/Yf7N.gif"
cry14 = "https://media1.tenor.com/images/0614541eed642d0fd7b6b219ff4bd9b6/tenor.gif?itemid=5466779"
#cry

#kiss 
kiss1 = "https://lifeo.ru/wp-content/uploads/gif-anime-kisses-44.gif"
kiss2 = "https://i.gifer.com/XJis.gif"
kiss3 = "https://pa1.narvii.com/7351/63825e3214ac36a482f5676c0f7765396f1179aer1-512-288_hq.gif"
kiss4 = "https://cdn-nus-1.pinme.ru/tumb/600/photo/d6/5317/d653178492f95ad97011052d36549dcb.gif"
kiss5 = "https://lifeo.ru/wp-content/uploads/gif-anime-kisses-43.gif"
kiss6 = "https://cutewallpaper.org/21/romantic-anime-kiss/Romantic-Anime-Kiss-GIF-by-Reactions.gif"
kiss7 = "https://thumbs.gfycat.com/BogusCookedCrossbill-size_restricted.gif"
kiss8 = "https://pa1.narvii.com/6739/e51bb40ec640cd1c314e003c8dbf16cbcf04f9ab_hq.gif"
kiss9 = "https://lifeo.ru/wp-content/uploads/gif-anime-kisses-24.gif"
#kiss

#hit
hit1 = "https://media.moddb.com/images/groups/1/25/24269/t3_56xx0a.gif"
hit2 = "https://i.gifer.com/Vx5G.gif"
hit3 = "https://i.gifer.com/embedded/download/Ua1c.gif"
hit4 = "http://blog-imgs-96.fc2.com/y/a/r/yarakan/fm64184.gif"
hit5 = "https://data.whicdn.com/images/187664188/original.gif"
hit6 = "https://animegif.ru/up/photos/album/nov17/171114_226.gif"
hit7 = "https://64.media.tumblr.com/50d374bdfa585742ae1e981d391b5265/tumblr_oilmal3juJ1sr2fsho1_500.gif"
hit8 = "https://i.gifer.com/VCCJ.gif"
hit9 = "https://img.gifmagazine.net/gifmagazine/images/863158/original.gif"
hit10 = "https://data.whicdn.com/images/82794614/original.gif"
hit11 = "https://i.gifer.com/embedded/download/80kI.gif"
hit12 = "https://i.playground.ru/i/pix/749117/image.jpg"
hit13 = "https://i.gifer.com/YuO7.gif"
hit14 = "https://i.pinimg.com/originals/83/42/0b/83420b6d32aa1417f6f347ea8f50b40d.gif"
#hit

#tickle щекотать
tickle1 = "https://avatars.mds.yandex.net/get-zen_doc/1894366/pub_5dc069ef23bf4800b29930b6_5dc089393d873600afe35081/orig"
tickle2 = "https://pa1.narvii.com/6875/a9b8a99fd3d210694e513b8d0d557e4ab4cdffa5r1-320-180_hq.gif"
tickle3 = "https://thumbs.gfycat.com/DaringGrossJellyfish-size_restricted.gif"
tickle4 = "https://cdn.ebaumsworld.com/mediaFiles/picture/1548104/84617227.gif"
tickle5 = "https://pa1.narvii.com/6837/ba84531dce18a7de0b43c3f13a2e84231a0a1e82_hq.gif"
tickle6 = "https://media.8kun.top/file_store/de60e09a7ee24238b0d465d69e30f1df115ba59dacf591c4d40962ad37156174.gif"
tickle7 = "https://media1.tenor.com/images/5cbe2cb77056ef2faf395b26fdece8eb/tenor.gif?itemid=14132818"
tickle8 = "https://i.gifer.com/O4QR.gif"
tickle9 = "https://i.gifer.com/embedded/download/R6VH.gif"
tickle10 = "https://i.gifer.com/G0Rp.gif"
#tickle

#overtake догонять
overtake1 = "https://i.gifer.com/CQJM.gif"
overtake2 = "https://i.gifer.com/6E5I.gif"
overtake3 = "https://thumbs.gfycat.com/TiredExhaustedBufflehead-size_restricted.gif"
overtake4 = "https://pa1.narvii.com/6878/d82c8cd63e25d91a979dd44af3a94c328210f473r1-577-344_hq.gif"
overtake5 = "https://64.media.tumblr.com/tumblr_m96chsvH5f1qbvovho1_500.gif"
overtake6 = "https://s7.hostingkartinok.com/uploads/images/2014/12/fb8cc3124fd88e29bfa709ad7ee4e6ef.gif"
overtake7 = "https://i.gifer.com/8O7c.gif"
#overtake

#perturbation возмущение
perturbation1 = "https://i.gifer.com/QyYw.gif"
perturbation2 = "https://mlpforums.com/uploads/post_images/sig-4017965.H1m0jDq.gif"
perturbation3 = "https://i.gifer.com/CKTr.gif"
perturbation4 = "https://thumbs.gfycat.com/RemarkableEvergreenBordercollie-size_restricted.gif"
perturbation5 = "https://i.gifer.com/406T.gif"
perturbation6 = "https://i.gifer.com/5Gvg.gif"
#perturbation

#misunderstanding недопонимание
misunderstanding1 = "https://otvet.imgsmail.ru/download/u_2c1fee8a560d25204f7a0dbd5ab384e6_800.gif"
misunderstanding2 = "https://cdn.humoraf.ru/wp-content/uploads/2017/07/skachat-anime-gifki-humoraf-45.gif"
misunderstanding3 = "https://steamuserimages-a.akamaihd.net/ugc/907905820487707033/932D69E377DDA85CDB329526D2619B0AEF703D16/?imw=512&amp;imh=491&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true"
misunderstanding4 = "https://i.kym-cdn.com/photos/images/original/000/846/679/df7.gif"
#misunderstanding

#idk
idk1 = "https://media1.tenor.com/images/dbe1ca7fdb532cf96a9bea40fa1f406e/tenor.gif?itemid=9724581"
idk2 = "https://media1.tenor.com/images/610ba50eee6213017c5b351031923d57/tenor.gif?itemid=15483874"
idk3 = "https://pa1.narvii.com/6847/3e6afc1762a8ccb1b31d49a4f1ac21bb49acf470_hq.gif"
#idk

#hello приветствие
hello1 = "https://pa1.narvii.com/6911/1e57e023f30e37ae05afb412f040432a10aef8e2r1-500-424_hq.gif"
hello2 = "https://thumbs.gfycat.com/HauntingNeighboringBarracuda-size_restricted.gif"
hello3 = "https://pa1.narvii.com/6482/b4862bba0a3633b3bb3e6f4b6a72b8047f932c4a_hq.gif"
hello4 = "https://i.gifer.com/H0ZJ.gif"
hello5 = "https://2.bp.blogspot.com/-V2q6IOsnPLk/V4P5d_ESyEI/AAAAAAAAg_o/P9pTua0vAlAdjwJa3_Tq62vdbmDAoEa3wCKgB/s1600/Omake%20Gif%20Anime%20-%20Love%20Live!%20Sunshine!!%20-%20Episode%202%20-%20Chika%20Waves.gif"
hello6 = "https://pa1.narvii.com/6928/d903d69f3d8994d325f64d3d4462ee9222256cf6r1-570-320_hq.gif"
#hello

#bye
bye1 = "https://image.myanimelist.net/ui/OK6W_koKDTOqqqLDbIoPAtoQNblfWhqkzRboev8RrHA"
bye2 = "https://i.gifer.com/embedded/download/8O7X.gif"
bye3 = "https://i.pinimg.com/originals/5e/ff/3d/5eff3d1f8334f601b31687e26a880181.gif"
bye4 = "https://thumbs.gfycat.com/KeySpiffyDuck-size_restricted.gif"
bye5 = "https://thumbs.gfycat.com/MeekEachHornedtoad-size_restricted.gif"
bye6 = "https://media1.tenor.com/images/972424767943ed34a19f6ff2a9cbe976/tenor.gif?itemid=14192312"
#bye

#happy
happy1 = "https://pa1.narvii.com/6601/7a0c1e919b9ccc50b08f780df514c5c11d45b02d_hq.gif"
happy2 = "https://i.gifer.com/BLDu.gif"
happy3 = "https://data.whicdn.com/images/299405277/original.gif"
happy4 = "https://media1.tenor.com/images/0f260e13b0b3dc3608be20d3860d3c16/tenor.gif?itemid=8618504"
happy5 = "https://pa1.narvii.com/7230/c31e41423c1dbc3526fd775879b97d815b08e1c6r1-640-360_hq.gif"
happy6 = "https://img.gifmagazine.net/gifmagazine/images/545944/original.gif"
happy7 = "https://i.gifer.com/28v3.gif"
happy8 = "https://media1.tenor.com/images/70719144c92afdd1ffea3b99aa007800/tenor.gif?itemid=4704737"
happy9 = "https://i.gifer.com/UiVb.gif"
#happy



class love(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def hug(self, ctx, member: discord.Member):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Обнимашки'
			lan2 = 'Обнял(а)'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Hugs'
			lan2 = 'Hugged'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = f'{ctx.author.mention} {lan2} {member.mention}', color=0xffc7c7)
		emb.set_image(url = random.choice([img5,img6,img7,img8,img9,img10,img11,img12,img13,img14,img15,img16,img17,img18,img19,img20])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def kill(self, ctx, member: discord.Member):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Убийство'
			lan2 = 'убил(а)'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Murder'
			lan2 = 'killed'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = f'{ctx.author.mention} {lan2} {member.mention}', color=0xff496c)
		emb.set_image(url = random.choice([kill1,kill2,kill3,kill4,kill5,kill6,kill7,kill8,kill9,kill10,kill11])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def cry(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Плачет'
			lan2 = 'плачет'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Crying'
			lan2 = 'crying'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = f'{ctx.author.mention} {lan2}', color=0x8ac8ff)
		emb.set_image(url = random.choice([cry1,cry2,cry3,cry4,cry5,cry6,cry7,cry8,cry9,cry10,cry11,cry12,cry13,cry14])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def kiss(self, ctx, member: discord.Member):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Поцелуй'
			lan2 = 'целует'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Kiss'
			lan2 = 'kisses'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = f'{ctx.author.mention} {lan2} {member.mention}', color=0xfa2363)
		emb.set_image(url = random.choice([kiss1,kiss2,kiss3,kiss4,kiss5,kiss6,kiss7,kiss8,kiss9])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def hit(self, ctx, member: discord.Member):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Бьёт'
			lan2 = 'бьёт'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Beats'
			lan2 = 'beats'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = f'{ctx.author.mention} {lan2} {member.mention}', color=0x821e3c)
		emb.set_image(url = random.choice([hit1,hit2,hit3,hit4,hit5,hit6,hit7,hit8,hit9,hit10,hit11,hit12,hit13,hit14])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def tickle(self, ctx, member: discord.Member):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Щекотать'
			lan2 = 'щекотит'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Tickle'
			lan2 = 'tickles'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = f'{ctx.author.mention} {lan2} {member.mention}', color=0xfc89ac)
		emb.set_image(url = random.choice([tickle1,tickle2,tickle3,tickle4,tickle5,tickle6,tickle7,tickle8,tickle9,tickle10])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def overtake(self, ctx, member: discord.Member):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Догонять'
			lan2 = 'догоняет'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Overtake'
			lan2 = 'overtakes'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = f'{ctx.author.mention} {lan2} {member.mention}', color=0xbdbdf2)
		emb.set_image(url = random.choice([overtake1,overtake2,overtake3,overtake4,overtake5,overtake6,overtake7])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def perturbation(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Возмущение'
			lan2 = 'возмущается'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Perturbation'
			lan2 = 'outrages'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = f'{ctx.author.mention} {lan2}', color=0xbdbdf2)
		emb.set_image(url = random.choice([perturbation1,perturbation2,perturbation3,perturbation4,perturbation5,perturbation6])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def misunderstanding(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Недопонимание'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Misunderstanding'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = '', color=0xbdbdf2)
		emb.set_image(url = random.choice([perturbation1,perturbation2,perturbation3,perturbation4,perturbation5,perturbation6])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def shrug(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Недопонимание'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Shrug'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = '', color=0xbdbdf2)
		emb.set_image(url = random.choice([idk1,idk2,idk3])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def hello(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Привет'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Hello'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = '', color=0xbdbdf2)
		emb.set_image(url = random.choice([hello1,hello2,hello3,hello4,hello5,hello6])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def bye(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Пока'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Bye'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = '', color=0xbdbdf2)
		emb.set_image(url = random.choice([bye1,bye2,bye3,bye4,bye5,bye6])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

	@commands.command()
	async def happy(self, ctx):
		if str(ctx.guild.region) == 'russia':
			lan1 = 'Радостная'
			lan3 = 'Вызвано:'
		else:
			lan1 = 'Happy'
			lan3 = 'Induced:'
		emb = discord.Embed(title = f'**{lan1}!**',description = '', color=0xbdbdf2)
		emb.set_image(url = random.choice([happy1,happy2,happy3,happy4,happy5,happy6,happy7,happy8,happy9])) 
		emb.set_footer(text=f'{lan3} {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
		await ctx.send(embed=emb)

def setup(client):
	client.add_cog(love(client))