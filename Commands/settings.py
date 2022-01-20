import discord
from discord.ext import commands
import sqlite3
from helper import utils

class SettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help= 'Used to set the prefix of the bot in this server, use default to default to the global prefix', usage='prefix <prefix> | default')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix = None):
        try:
            await utils.auto_register(ctx.author.id)
            conn = sqlite3.connect('./Data/Database/settings.db')
            c = conn.cursor()
            rows = c.execute('SELECT * FROM prefix WHERE guildId = "{}"'.format(ctx.guild.id)).fetchall()

            if prefix == None:
                if len(rows) == 0:
                    pr = '+'
                else :
                    pr = rows[0][1]
                await ctx.send(embed= discord.Embed(color= 0xf1c40f, description= 'The Current Prefix is **{}**'.format(pr)))
            elif prefix == 'default':
                c.execute('DELETE FROM prefix WHERE guildId = "{}"'.format(ctx.guild.id))
                conn.commit()
                await ctx.send(embed= discord.Embed(color= 0x008000, description= 'Prefix changed to **default prefix (+)**'))
            else:
                if len(prefix) > 3:
                    return await ctx.send(embed= discord.Embed(color= 0xFF0000, description= 'Prefix exceeded the 3 character limit'))
                if len(rows) == 0:
                    c.execute('INSERT INTO prefix (guildId, prefix) VALUES ("{0}", "{1}")'.format(ctx.guild.id, prefix))
                    conn.commit()
                    await ctx.send(embed= discord.Embed(color= 0x008000,description= 'Prefix set to **{}**'.format(prefix)))
                else:
                    c.execute('UPDATE prefix SET prefix = "{1}" WHERE guildId = "{0}"'.format(ctx.guild.id, prefix))
                    conn.commit()
                    await ctx.send(embed= discord.Embed(color= 0x008000,description= 'Prefix changed to **{}**'.format(prefix)))
        except:
            return

    @prefix.error
    async def prefix_error(self, error, ctx):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send(embed= discord.Embed(color= 0xFF0000, description= 'You do not have **ADMINISTRATOR** permission!'))

def setup(bot):
        bot.add_cog(SettingsCog(bot))
