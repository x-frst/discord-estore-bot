import discord
import time
from discord.ext import commands
import sqlite3
from helper import utils

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Sends info about the bot', usage='info')
    @commands.guild_only()
    async def info(self, ctx):
        await utils.auto_register(ctx.author.id)
        embed = discord.Embed(title='Amazon Shopping').set_thumbnail(url=self.bot.user.avatar_url).add_field(name='Date Created :', value='08 September 2020')
        await ctx.send(embed=embed)

    @commands.command(help='Gives you bot official server link', usage='support')
    @commands.guild_only()
    async def support(self, ctx):
        await utils.auto_register(ctx.author.id)
        await ctx.send("**Join Official Bot Guild:**\nhttps://discord.gg/inv_link")

    @commands.command(help='Gives you bot invite link', usage='invite')
    @commands.guild_only()
    async def invite(self, ctx):
        await utils.auto_register(ctx.author.id)
        await ctx.send("**Invite Discord E-Store:**\nhttps://discord.com/oauth2/authorize?client_id=*****")

    @commands.command(help='Gives you apply link to apply for Discord E-Store Warehouse Staff', usage='apply')
    @commands.guild_only()
    async def apply(self, ctx):
        await utils.auto_register(ctx.author.id)
        await ctx.send("**Apply For Warehouse Staff:**\n"+self.bot.official_website+"/apply")

    @commands.command(help='Gives you appeal link to appeal for Guild/Bot ban', usage='appeal')
    @commands.guild_only()
    async def appeal(self, ctx):
        await ctx.send("**You Can Send Your Appeal Here:**\n"+self.bot.official_website+"/appeal")

    @commands.command(aliases=['db', 'dashboard'], help='Gives you bot dashboard link', usage='website')
    @commands.guild_only()
    async def website(self, ctx):
        await utils.auto_register(ctx.author.id)
        await ctx.send("**Visit Bot Dashboard Here:**\n"+self.bot.official_website+"")

    @commands.command(help='Shows the latency of the bot', usage='ping')
    @commands.guild_only()
    async def ping(self, ctx):
        await utils.auto_register(ctx.author.id)
        t1 = time.perf_counter()
        await ctx.channel.trigger_typing()
        t2 = time.perf_counter()
        embed = discord.Embed(description='Pong!🏓 {}ms'.format(round((t2-t1)*100)))

        await ctx.send(embed=embed)

    @commands.command(help='Shows the ordering rules of Bot', usage='rules')
    @commands.guild_only()
    async def rules(self, ctx):
        await utils.auto_register(ctx.author.id)
        embed = discord.Embed(title='Rules', description="""
```
General Item Rules
```

1. Troll/invalid orders are subject to deletion.
2. We don’t accept fictional items that do not exist in real life.
3. Repetitive forbidden/troll orders will get your account blacklisted.
4. Respect the Staff Team.
5. Please refrain from ordering in large amounts. (Example: 100 Mobiles)
6. We don't accept unreleased items.
7. We don't accept animals/humans or their body parts.
8. We don't accept drugs/medicines or any other pharmacy items.
9. Use your knowledge and common sense before making orders.

```
Food/Drink Item Rules
```

1. Some countries may serve food like snakes, dog, cat, frogs, but we can't accept it!
2. We don't accept raw food, you can only request for cooked food!
3. We don't serve insects or bugs (Example: Worms, Cockroaches).
4. Don't request food if it is not available in real life, this includes TV-Shows, Movies & In-Game items! (Example: Shield Potion, Jellyfish Sandwich, Enchanted Golden Apple)
5. We don't accept pet as food (however, you can always order a pet to play with it).
6. You can't order things like human/animal pee, any body part of human, animal eyes/tongue/private parts/tail/hair/nails/bones.
7. We don't accept any tobacco orders like cigarettes, bidi, hookah, any type of chewing tobacco.

```
Wallpaper Rules
```

1. We don't accept NSFW/Loli/Half Naked/ wallpapers.
2. Please don't request for any GIF/Animated wallpaper.
3. You must specify wallpaper category/title/name.

**Forbidden Orders:**
```diff
- NSFW Items (Example: Condom, Dildo)
- Unreleased Items (Example: iPhone 69, PS20)
- Meme Orders (Example: Pepe Coin, Doge Pet)
- Fictional Orders (Example: In-Game Money/Points, Doraemon Gadgets)
```
""").set_footer(text='● ' + ctx.author.name + '#' + ctx.author.discriminator)
        await ctx.send(embed=embed)

    @commands.command(aliases=['bal', 'money'], help="Shows your or mentioned user's economy balance", usage='balance | balance <User>')
    @commands.guild_only()
    async def balance(self, ctx, user : discord.User = None):
        try:
            await utils.auto_register(ctx.author.id)
            flagged = await utils.check_flagged(ctx.author.id)
            if not flagged:
                conn = sqlite3.connect('./Data/Database/users.db')
                c = conn.cursor()
                if user == None:
                    balance = c.execute('SELECT balance FROM users WHERE userid = "{}"'.format(ctx.author.id)).fetchone()

                    await ctx.send(embed= discord.Embed(color= 0xFFFF00,description='**{}** has ${:,} 💸'.format(ctx.author.display_name, int(balance[0]))))
                else:
                    await utils.auto_register(user.id)
                    get_balance = c.execute('SELECT balance FROM users WHERE userid = "{}"'.format(user.id)).fetchone()

                    await ctx.send(embed= discord.Embed(color= 0xFFFF00,description='**{}** has ${:,} 💸'.format(user.display_name, int(balance[0]))))
            else:
                await ctx.send("Your bot account has been flagged!")
        except:
            return

    @commands.command(help="Shows your or mentioned user's weekly orders", usage='orders | orders <User>')
    @commands.guild_only()
    async def orders(self, ctx, user : discord.User = None):
        try:
            await utils.auto_register(ctx.author.id)
            flagged = await utils.check_flagged(ctx.author.id)
            if not flagged:
                conn = sqlite3.connect('./Data/Database/users.db')
                c = conn.cursor()
                is_staff = await utils.check_staff(ctx.author.id)
                if is_staff:
                    if user == None:
                        orders = c.execute('SELECT weekly_orders FROM users WHERE userid = "{}"'.format(ctx.author.id)).fetchone()
                        await ctx.send(embed= discord.Embed(color= discord.Color.dark_orange(),description='**{}** has done {}/20 weekly orders!'.format(ctx.author.display_name, int(orders[0]))))
                    else:
                        await utils.auto_register(user.id)
                        is_user_staff = await utils.check_staff(user.id)
                        if is_user_staff:
                            orders = c.execute('SELECT weekly_orders FROM users WHERE userid = "{}"'.format(user.id)).fetchone()
                            await ctx.send(embed= discord.Embed(color= discord.Color.dark_orange(),description='**{}** has done {}/20 weekly orders!'.format(user.display_name, int(orders[0]))))
                        else:
                            await ctx.send("That user is not Warehouse Staff!")
                else:
                    await ctx.send("You're not authorized to use this command!")
            else:
                await ctx.send("Your bot account has been flagged!")
        except:
            return

    @commands.command(help="Shows your or mentioned user's sent, managed, delivered & total orders", usage='stats | stats <User>')
    @commands.guild_only()
    async def stats(self, ctx, user : discord.User = None):
        try:
            await utils.auto_register(ctx.author.id)
            flagged = await utils.check_flagged(ctx.author.id)
            if not flagged:
                conn = sqlite3.connect('./Data/Database/users.db')
                c = conn.cursor()
                is_staff = await utils.check_staff(ctx.author.id)
                if is_staff:
                    if user == None:
                        sent = c.execute('SELECT orders_sent FROM users WHERE userid = "{}"'.format(ctx.author.id)).fetchone()
                        managed = c.execute('SELECT orders_handled FROM users WHERE userid = "{}"'.format(ctx.author.id)).fetchone()
                        delivered = c.execute('SELECT orders_delivered FROM users WHERE userid = "{}"'.format(ctx.author.id)).fetchone()
                        deleted = c.execute('SELECT orders_deleted FROM users WHERE userid = "{}"'.format(ctx.author.id)).fetchone()
                        total = int(managed[0]) + int(delivered[0])
                        embed= discord.Embed(description="**"+str(ctx.author.name)+" Order Statistics**\n\n```\nCustomer Stats\n```**Orders Sent:** `"+str(sent[0])+"`\n**Orders Got Deleted:** `"+str(deleted[0])+"`\n\n```\nWarehouse Staff Stats\n```**Orders Managed:** `"+str(managed[0])+"`\n**Orders Delivered:** `"+str(delivered[0])+"`\n**Total Orders:** `"+str(total)+"`", color= discord.Color.blurple())
                        embed.set_author(name=ctx.author)
                        await ctx.send(embed=embed)
                    else:
                        await utils.auto_register(user.id)
                        sent = c.execute('SELECT orders_sent FROM users WHERE userid = "{}"'.format(user.id)).fetchone()
                        managed = c.execute('SELECT orders_handled FROM users WHERE userid = "{}"'.format(user.id)).fetchone()
                        delivered = c.execute('SELECT orders_delivered FROM users WHERE userid = "{}"'.format(user.id)).fetchone()
                        deleted = c.execute('SELECT orders_deleted FROM users WHERE userid = "{}"'.format(user.id)).fetchone()
                        total = int(managed[0]) + int(delivered[0])
                        embed= discord.Embed(description="**"+str(user.name)+" Order Statistics**\n\n```\nCustomer Stats\n```**Orders Sent:** `"+str(sent[0])+"`\n**Orders Got Deleted:** `"+str(deleted[0])+"`\n\n```\nWarehouse Staff Stats\n```**Orders Managed:** `"+str(managed[0])+"`\n**Orders Delivered:** `"+str(delivered[0])+"`\n**Total Orders:** `"+str(total)+"`", color= discord.Color.blurple())
                        embed.set_author(name=ctx.author)
                        await ctx.send(embed=embed)
                else:
                    await ctx.send("You're not authorized to use this command!")
            else:
                await ctx.send("Your bot account has been flagged!")
        except:
            return

def setup(bot):
        bot.add_cog(MiscCog(bot))
