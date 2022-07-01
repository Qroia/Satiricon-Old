import discord
from discord.ext import commands
import datetime
import asyncio
import random

class Giveaway(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command(aliases = ['раздача'])
    @commands.has_permissions(manage_messages=True)
    async def gstart(self, ctx, arg: str, *, prize):
        if str(ctx.guild.region) == 'russia':
            lan1 = 'Розыгрыш!'
            lan2 = 'Заканчивается:'
            lan3 = 'Закончится через'
            lan4 = 'Никто не участвовал в вашем розыгрыше'
            lan5 = 'И у нас победитель! Поздравим'
            lan6 = 'Он получает:'
            lan7 = 'Ошибка!'
            lan8 = 'Вы неправильно ввели аргумент!'
        else:
            lan1 = 'Raffle!'
            lan2 =' Ends: '
            lan3 = 'Ends in'
            lan4 = 'No one participated in your draw'
            lan5 = 'And we have a winner! Congratulations to'
            lan6 = 'It gets:'
            lan7 = 'Error!'
            lan8 = 'You entered the argument incorrectly!'
        await ctx.message.delete()
        e = discord.Embed(title=lan1, description = prize, color= discord.Color.dark_gray())
        embError = discord.Embed(color= discord.Color.red())
        end = datetime.datetime.utcnow()
        amount = int(arg[:-1])
        tip = arg[-1]
        if tip == "s":
            endS = end + datetime.timedelta(seconds=amount)
            e.add_field(name=lan2, value=f"{endS} UTC")
            e.set_footer(text=f"{lan3} {arg[:-1]}s.")
            self.msg = await ctx.send(embed=e)
            await self.msg.add_reaction("🎉")
            await asyncio.sleep(amount)
            new_msg = await ctx.channel.fetch_message(self.msg.id)
            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.client.user))

            if len(users) == 0:
                await ctx.author.send(lan4)
                return
            else:
                winner = random.choice(users)

                await ctx.send(f"{lan5} {winner.mention}! {lan6} {prize}!")
                await asyncio.sleep(18000)
                await self.msg.delete()
        
        elif tip == "m":
            endM = end + datetime.timedelta(seconds=amount*60)
            e.add_field(name=lan2, value=f"{endM} UTC")
            e.set_footer(text=f"{lan3} {arg[:-1]}min.")
            self.msg = await ctx.send(embed=e)
            await self.msg.add_reaction("🎉")
            await asyncio.sleep(amount*60)
            new_msg = await ctx.channel.fetch_message(self.msg.id)
            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.client.user))

            if len(users) == 0:
                await ctx.author.send(lan4)
                return
            else:
                winner = random.choice(users)

                await ctx.send(f"{lan5} {winner.mention}! {lan6} {prize}!")
                await asyncio.sleep(18000)
                await self.msg.delete()

        elif tip == "h":
            endH = end + datetime.timedelta(seconds=amount*60*60)
            e.add_field(name=lan2, value=f"{endH} UTC")
            e.set_footer(text=f"{lan3} {arg[:-1]}h.")
            self.msg = await ctx.send(embed=e)
            await self.msg.add_reaction("🎉")
            await asyncio.sleep(amount*60*60)
            new_msg = await ctx.channel.fetch_message(self.msg.id)

            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.client.user))
            if len(users) == 0:
                await ctx.author.send(lan4)
                return
            else:
                winner = random.choice(users)

                await ctx.send(f"{lan5} {winner.mention}! {lan6} {prize}!")
                await asyncio.sleep(18000)
                await self.msg.delete()

        elif tip == "d":
            endD = end + datetime.timedelta(seconds=amount*60*60*24)
            e.add_field(name=lan2, value=f"{endD} UTC")
            e.set_footer(text=f"{lan3} {arg[:-1]}d.")
            self.msg = await ctx.send(embed=e)
            await self.msg.add_reaction("🎉")
            await asyncio.sleep(amount*60*60*24)
            new_msg = await ctx.channel.fetch_message(self.msg.id)
            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.client.user))
            if len(users) == 0:
                await ctx.author.send(lan4)
                return
            else:
                winner = random.choice(users)

                await ctx.send(f"{lan5} {winner.mention}! {lan6} {prize}!")
                await asyncio.sleep(18000)
                await self.msg.delete

        else:
            embError.add_field(name=lan7, value=lan8)
            await ctx.send(embed =embError)

def setup(client):
    client.add_cog(Giveaway(client))