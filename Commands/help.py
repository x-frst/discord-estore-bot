import discord
from discord.ext import commands
from helper import utils

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help= 'Sends this message', usage='help | help <Command>')
    @commands.guild_only()
    async def help(self, ctx, *, cmd = None):

        await utils.auto_register(ctx.author.id)
        async def get_cmd():
            for x in self.bot.commands:
                if x.name == cmd:
                    embed = discord.Embed(color= 0xf1c40f).add_field(name='Name',value=x.name, inline=False).add_field(name='Description', value=x.help, inline=False).add_field(name='Usage', value=x.usage, inline=False).add_field(name='Aliases', value=', '.join(x.aliases) or 'None', inline=False).set_footer(text='● ' + ctx.author.name)
                    await ctx.send(embed=embed)
                    return True
                    break

        if cmd == None:
            if await utils.check_staff(ctx.author.id):
                embed = discord.Embed(title= 'Command Groups', color= 0xf1c40f, description='**Help** - Sends this Message | help <Command>').add_field(name='Miscellanious',value='Ping, Info, Rules, Balance, Support, Invite, Apply, Appeal, Website, Stats', inline=False).add_field(name='Settings',value='Prefix', inline=False).add_field(name='Delivery', value='Queue, Queue Leave, Deliver, Orders', inline=False).add_field(name='Order', value='Order, Track, Tip, Feedback', inline=False).add_field(name='Staff', value='Promote, Demote, DM, Resetweekly', inline=False).set_footer(text='● ' + ctx.author.name)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title= 'Command Groups', color= 0xf1c40f, description='**Help** - Sends this Message | help <Command>').add_field(name='Miscellanious',value='Ping, Info, Rules, Balance, Support, Invite, Apply, Appeal, Website, Stats', inline=False).add_field(name='Settings',value='Prefix', inline=False).add_field(name='Order', value='Order, Track, Tip, Feedback', inline=False).set_footer(text='● ' + ctx.author.name)
                await ctx.send(embed=embed)
        else:
            if await get_cmd() != True:
                await ctx.send('Command : ' + cmd + ' not Found')

def setup(bot):
        bot.add_cog(HelpCog(bot))
