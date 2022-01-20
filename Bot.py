# Imports
import discord
from discord.ext import commands
import sqlite3

# Default prefix
PREFIX = '+'

# To Determine Custom Prefix for a Server
async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        conn = sqlite3.connect('./Data/Database/settings.db')
        c = conn.cursor()
        rows = c.execute('SELECT prefix FROM prefix WHERE guildId = "{}"'.format(message.guild.id)).fetchone()
        if rows:
            return rows[0]
        else:
            return PREFIX
    else:
        return PREFIX

# Bot Setup
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=determine_prefix, intents=intents)
bot.remove_command('help')
bot.official_guild = 1234567890 # Official support guild id
bot.staff_role = 1234567890 # Warehouse Staff role id
bot.pd_channel = 1234567890 # Channel id where bot will send user promotion/demotion logs
bot.queue_channel = 1234567890 # Channel id where bot will delivery queue
bot.delivery_logs = 1234567890 # Channel id where bot will send delivery logs
bot.order_logs = 1234567890 # Channel id where bot will send order logs
bot.tip_logs = 1234567890 # Channel id where bot will send user's tip logs
bot.feedback_logs = 1234567890 # Channel id where bot will send user's feedback logs
bot.owner_list = [] # Owner list who can promote/demote/flag users
bot.manager_list = [] # Owner list who can promote/demote users
bot.official_website = "https://mywebsite.com" # Official dashboard link

@bot.event
async def on_ready():
    setType = discord.ActivityType.listening
    status = "+help"
    await bot.change_presence(activity=discord.Activity(type=setType, name=status))
    print('Bot is ready')

@bot.command()
@commands.is_owner()
@commands.guild_only()
async def load(ctx, *, module : str):
    try:
        bot.load_extension(module)
    except Exception as e:
        await ctx.send('`{}:` {}'.format(type(e).__name__, e))
    else:
        await ctx.send('`{}` Module Loaded.'.format(module))

@bot.command()
@commands.is_owner()
@commands.guild_only()
async def unload(ctx, *, module : str):
    try:
        bot.unload_extension(module)
    except Exception as e:
        await ctx.send('`{}:` {}'.format(type(e).__name__, e))
    else:
        await ctx.send('`{}` Module unloaded.'.format(module))

@bot.command(name='reload')
@commands.is_owner()
@commands.guild_only()
async def _reload(ctx, *, module : str):
    try:
        bot.reload_extension(module)
    except Exception as e:
        await ctx.send('`{}:` {}'.format(type(e).__name__, e))
    else:
        await ctx.send('`{}` Module reloaded.'.format(module))

@bot.command()
@commands.guild_only()
async def shutdown(ctx):
    await ctx.send('Shutting down')
    await bot.logout()

# Cogs Setup
initial_extensions = ['Commands.misc', 'Commands.help', 'Commands.order', 'Commands.settings', 'Commands.delivery', 'Commands.owner', 'Commands.staff', 'Commands.eval', 'Commands.CommandErrorHandler']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
        print('Loaded {}'.format(extension))

bot.run('TOKEN_HERE')
