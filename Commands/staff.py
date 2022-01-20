import discord
from discord.ext import commands
import sqlite3
import datetime
from helper import utils

class StaffCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Used to promote a user to Warehouse Staff', usage='promote <User>')
    @commands.guild_only()
    async def promote(self, ctx, user : discord.User):
        try:
            if ctx.author.id in self.bot.manager_list or ctx.author.id in self.bot.owner_list:
                conn = sqlite3.connect('./Data/Database/users.db')
                c = conn.cursor()

                if await utils.check_staff(user.id):
                    await ctx.send(embed= discord.Embed(color= 0xFF0000, title='Already Staff', description='**{}** is already a Staff Member'.format(user.name)).set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
                else:
                    guild = self.bot.get_guild(self.bot.official_guild)
                    role = guild.get_role(self.bot.staff_role)
                    member = guild.get_member(user.id)
                    c.execute('UPDATE users SET staff = "yes" WHERE userId = "{}"'.format(user.id))
                    conn.commit()
                    time = datetime.datetime.now().strftime("%c")
                    await ctx.send(embed= discord.Embed(color= 0x008000, title='Promoted to Staff 🎉').add_field(name='User', value=user.name + '#' + user.discriminator).add_field(name='Status', value='{} has been Promoted'.format(user.name)).add_field(name='Time', value=time, inline=False).set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
                    channel = self.bot.get_channel(self.bot.pd_channel)
                    await channel.send("**```css\nUser Promotion Notice```\nWelcome "+str(user.mention)+" To Discord E-Store Warehouse Staff Team!**")
                    await member.add_roles(role, reason="Promoted to Warehouse Staff")
                    try:
                        await user.send(embed= discord.Embed(color= 0x008000, title='Your Warehouse Staff Application Was Accepted 🎉', description="**Welcome To Discord E-Store Staff Team!**\n\nCheck <#757489614998077472> to know about our staff limitations, if you've any query please feel free to ask in <#757489059265380353>").add_field(name='Time', value=time, inline=False))
                    except:
                        pass
            else:
                await ctx.send(embed= discord.Embed(color= 0xFF0000, title='Unauthorized Use', description='**You are not authorized to use this command!**').set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
        except:
            return

    @promote.error
    async def promote_err(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='Could not Find that User'))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='You did not Provide a User/Reason'))

    @commands.command(help='Used to demote a user from Warehouse Staff', usage='demote <User>')
    @commands.guild_only()
    async def demote(self, ctx, user : discord.User, *, reason : str):
        try:
            if ctx.author.id in self.bot.manager_list or ctx.author.id in self.bot.owner_list:
                if user.id not in self.bot.owner_list:
                    conn = sqlite3.connect('./Data/Database/users.db')
                    c = conn.cursor()

                    if await utils.check_staff(user.id):
                        try:
                            guild = self.bot.get_guild(self.bot.official_guild)
                            role = guild.get_role(self.bot.staff_role)
                            member = guild.get_member(user.id)
                            await member.remove_roles(role, reason="Demoted from Warehouse Staff")
                        except:
                            pass
                        c.execute('UPDATE users SET staff = "no" WHERE userId = "{}"'.format(user.id))
                        conn.commit()
                        time = datetime.datetime.now().strftime("%c")
                        await ctx.send(embed= discord.Embed(color= 0x008000, title='Demoted from Staff').add_field(name='User', value=user.name + '#' + user.discriminator).add_field(name='Status', value='{} has been Demoted'.format(user.name)).add_field(name='Time', value=time, inline=False).add_field(name='Reason', value=reason, inline=False).set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
                        channel = self.bot.get_channel(self.bot.pd_channel)
                        await channel.send("**```css\nUser Demotion Notice```\nGoodbye "+str(user.mention)+", You've Been Demoted From Discord E-Store!**")
                        try:
                            await user.send(embed= discord.Embed(color= 0x008000, title='You Have Been Demoted From Discord E-Store Warehouse Staff!').add_field(name='Time', value=time, inline=False).add_field(name='Reason', value=reason, inline=False))
                        except:
                            pass
                    else:
                        await ctx.send(embed= discord.Embed(color= 0xFF0000, title='Not Staff', description='**{}** is not a Staff Member'.format(user.name)).set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
                else:
                    await ctx.send(embed= discord.Embed(color= 0xFF0000, title='Nice Try!', description='**You cannot demote bot owners!**').set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
            else:
                await ctx.send(embed= discord.Embed(color= 0xFF0000, title='Unauthorized Use', description='**You are not authorized to use this command!**').set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator))
        except:
            return

    @demote.error
    async def demote_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='You did not Provide a User/Reason'))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='Could not Find that User'))

def setup(bot):
        bot.add_cog(StaffCog(bot))
