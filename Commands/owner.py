import discord
from discord.ext import commands
import sqlite3
import datetime
from helper import utils
import os

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['blacklist'], help='Used to flag user account to blacklist them', usage='flag <User> <Reason>')
    @commands.is_owner()
    @commands.guild_only()
    async def flag(self, ctx, user : discord.User, *, reason : str):
        try:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()

            if await utils.check_flagged(user.id):
                await ctx.send(embed= discord.Embed(color= 0xf1c40f, title='Already Flagged 🚩').add_field(name='User', value=user.name + '#' + user.discriminator).add_field(name='Status', value='{} is already Flagged'.format(user.name)).set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
            else:
                c.execute('UPDATE users SET flagged = "yes" WHERE userId = "{}"'.format(user.id))
                conn.commit()
                time = datetime.datetime.now().strftime("%c")
                await ctx.send(embed= discord.Embed(color= 0x008000, title='Flagged 🚩').add_field(name='User', value=user.name + '#' + user.discriminator).add_field(name='Status', value='{} has been Flagged'.format(user.name)).add_field(name='Reason', value=reason, inline=False).add_field(name='Time', value=time, inline=False).set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
                try:
                    await user.send(embed= discord.Embed(color= 0xFF0000, title='You have been Flagged from {} Bot'.format(self.bot.user.name)).add_field(name='Reason', value=reason, inline=False).add_field(name='Time', value=time, inline=False))
                except:
                    pass
        except:
            return

    @flag.error
    async def flag_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='You did not Provide a User/Reason'))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='Could not Find that User'))

    @commands.command(aliases=['whitelist'], help='Used to unflag user account to whitelist them', usage='unflag <User>')
    @commands.is_owner()
    @commands.guild_only()
    async def unflag(self, ctx, user : discord.User):
        try:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()

            if await utils.check_flagged(user.id):
                c.execute('UPDATE users SET flagged = "no" WHERE userId = "{}"'.format(user.id))
                conn.commit()
                time = datetime.datetime.now().strftime("%c")
                await ctx.send(embed= discord.Embed(color= 0x008000, title='Unflagged 🏳️').add_field(name='User', value=user.name + '#' + user.discriminator).add_field(name='Status', value='{} has been Unflagged'.format(user.name)).add_field(name='Time', value=time, inline=False).set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
                try:
                    await user.send(embed= discord.Embed(color= 0x008000, title='You have been Unflagged from {} Bot'.format(self.bot.user.name)).add_field(name='Time', value=time, inline=False))
                except:
                    pass
            else:
                await ctx.send(embed= discord.Embed(color= 0xf1c40f, title='Not Flagged 🏳️').add_field(name='User', value=user.name + "#" + user.discriminator).add_field(name='Status', value='{} is not currently Flagged'.format(user.name)).set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
        except:
            return

    @unflag.error
    async def unflag_err(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='Could not Find that User'))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='You did not Provide a User/Reason'))

    @commands.command(help='Sends direct message to specified user', usage='dm <User> <Message>')
    @commands.is_owner()
    @commands.guild_only()
    async def dm(self, ctx, user : discord.User, *, msg: str):
        try:
            await user.send(embed= discord.Embed(color= discord.Color.gold(), title='You have received a message from {} Bot Team'.format(self.bot.user.name), description=msg))
            await ctx.send("Successfully sent message to "+str(user.name)+"!")
        except:
            await ctx.send("Failed to send message to user: Not found or DMs are disabled!")
            return

    @dm.error
    async def dm_err(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='Could not Find that User'))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='You did not Provide Message'))


    @commands.command(help='Reset weekly orders from all users', usage='resetweekly')
    @commands.is_owner()
    @commands.guild_only()
    async def resetweekly(self, ctx):
        try:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()

            is_staff = 'yes'
            reset = 0
            c.execute("UPDATE users SET weekly_orders = (?) WHERE staff = (?);", (reset, is_staff))
            conn.commit()
            await ctx.send("Successfully reset everyone's weekly orders!")
        except:
            await ctx.send("Failed to reset weekly orders!")
            return

    @commands.command(help='Remotely restart website', usage='restartwebsite')
    @commands.is_owner()
    @commands.guild_only()
    async def restartwebsite(self, ctx):
        try:
            os.system('sudo pm2 restart 0')
            await ctx.send("Successfully restarted website!")
        except Exception as e:
            await ctx.send("Failed to restart website with reason: `"+str(e)+"`")
            return

def setup(bot):
        bot.add_cog(OwnerCog(bot))
