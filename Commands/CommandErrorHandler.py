import traceback
import sys
from discord.ext import commands
import discord
import json

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send('{} has been disabled.'.format(ctx.command))

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed = discord.Embed(description=("**{} Can't Be Used In Private Messages.**".format(str(ctx.command).title())), color=discord.Color.red())
                embed.set_footer(text='Command Error Handler')
                return await ctx.author.send(embed=embed)
            except:
                pass

        elif isinstance(error, commands.CommandOnCooldown):
            try:
                seconds = error.retry_after
                m, s = divmod(seconds, 60)
                embed = discord.Embed(description="**Command Is On Cooldown, Try Again After: `"+str(round(m))+" Minutes, "+str(round(s))+" Seconds`!**".format(error.retry_after), color=discord.Color.red())
                embed.set_author(name=ctx.author)
                embed.set_footer(text = "Command Error Handler")
                await ctx.send(embed=embed)
                return
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                return await ctx.send('I could not find that member. Please try again.')


        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
