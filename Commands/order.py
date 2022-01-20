import discord
import time
from discord.ext import commands
import sqlite3
from helper import utils
import string
import random
import time
import asyncio

class OrderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.claim_task = self.loop.create_task(self.check_claims())


    async def check_claims(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(15.0)
            check = 'claimed'
            try:
                conn = sqlite3.connect('./Data/Database/orders.db')
                c = conn.cursor()
                conn2 = sqlite3.connect('./Data/Database/invites.db')
                c2 = conn2.cursor()
                conn3 = sqlite3.connect('./Data/Database/claimers.db')
                c3 = conn3.cursor()
                claim_orders = c.execute("SELECT orderid FROM orders WHERE status = ?;", (check,)).fetchall()
                for i in claim_orders:
                    for oid in i:
                        start = c2.execute("SELECT claimstamp FROM invites WHERE orderid = ?;", (oid,)).fetchone()
                        end = int(round(time.time() * 1000))
                        ts = (end-int(start[0]))/1000
                        if ts >= 420:
                            set_status = 'unclaimed'
                            c.execute("UPDATE orders SET status = (?) WHERE orderid = (?);", (set_status, oid))
                            conn.commit()
                            c2.execute("UPDATE invites SET claimerid = (?), claimstamp = (?) WHERE orderid = (?);", (None, None, oid))
                            conn2.commit()
                            c3.execute('DELETE FROM claimers WHERE orderid = ?;', (oid,))
                            conn3.commit()
            except:
                print("ERROR IN ORDER.PY: "+str(e))
                pass


    @commands.command(help='Orders an item for you', usage='order <Item>')
    @commands.guild_only()
    async def order(self, ctx, *, order_item:str):
        try:
            if ctx.channel.permissions_for(ctx.guild.me).create_instant_invite == True:
                await utils.auto_register(ctx.author.id)
                flagged = await utils.check_flagged(ctx.author.id)
                if not flagged:
                    conn = sqlite3.connect('./Data/Database/orders.db')
                    c = conn.cursor()
                    check_order = c.execute("SELECT * FROM orders WHERE userid = ?;", (ctx.author.id,)).fetchone()
                    if not check_order:
                        invite_url = await ctx.channel.create_invite(max_uses=1, reason='Delivery Purpose')
                        order_id = ''.join(random.choices(string.ascii_letters + string.digits, k = 6))
                        time_stamp = int(round(time.time() * 1000))
                        set_status = 'unclaimed'
                        await utils.insert_order(str(ctx.author), int(ctx.author.id), str(ctx.author.avatar_url).replace('?size=1024', ''), str(order_item), str(order_id), str(ctx.guild.name), int(ctx.guild.id), int(time_stamp), str(invite_url), set_status)
                        await ctx.send("Your order has been placed\n\n**Order ID: "+str(order_id)+"**")
                        channel = self.bot.get_channel(self.bot.order_logs)
                        await channel.send("```\nNEW ORDER RECEIVED\n```\n**User:** "+str(ctx.author)+" `("+str(ctx.author.id)+")`\n**Order Item:** "+str(order_item)+"\n**Order ID:** "+str(order_id)+"\n**Guild:** "+str(ctx.author.guild.name)+" (`"+str(ctx.author.guild.id)+"`)")
                    else:
                        await ctx.send("You have one pending order!")
                else:
                    await ctx.send("You have been restricted to give orders!")
            else:
                await ctx.send("I don't have permission to create invite in this channel!")
        except:
            return

    @commands.command(help='Track your current order status', usage='track')
    @commands.guild_only()
    async def track(self, ctx):
        try:
            await utils.auto_register(ctx.author.id)
            flagged = await utils.check_flagged(ctx.author.id)
            if not flagged:
                conn = sqlite3.connect('./Data/Database/orders.db')
                c = conn.cursor()
                check_order = c.execute("SELECT * FROM orders WHERE userid = ?;", (ctx.author.id,)).fetchone()
                if check_order:
                    order_item = c.execute("SELECT order_item FROM orders WHERE userid = ?;", (ctx.author.id,)).fetchone()
                    order_id = c.execute("SELECT orderid FROM orders WHERE userid = ?;", (ctx.author.id,)).fetchone()
                    order_status = c.execute("SELECT status FROM orders WHERE userid = ?;", (ctx.author.id,)).fetchone()
                    await ctx.send("**📦 | Order Information\n\nOrder: `"+str(order_item[0])+"`\nOrder ID: `"+str(order_id[0])+"`\nOrder Status: `"+str(order_status[0]).title()+"`**")
                else:
                    await ctx.send("You have no active order, send one!")
            else:
                await ctx.send("You have been restricted to give orders!")
        except:
            return

    @commands.command(help='Give certain amount of tip to packer & deliverer for your last order', usage='tip <Amount>')
    @commands.guild_only()
    async def tip(self, ctx, tip_amount : int):
        try:
            await utils.auto_register(ctx.author.id)
            flagged = await utils.check_flagged(ctx.author.id)
            if not flagged:
                conn = sqlite3.connect('./Data/Database/pastorders.db')
                c = conn.cursor()
                conn2 = sqlite3.connect('./Data/Database/users.db')
                c2 = conn2.cursor()

                check_order = c.execute("SELECT * FROM pastorders WHERE userid = ?;", (ctx.author.id,)).fetchone()
                if check_order:
                    is_tipped = c.execute("SELECT tipped FROM pastorders WHERE userid = ? ORDER BY id DESC;", (ctx.author.id,)).fetchone()
                    if int(is_tipped[0]) == 0:
                        if tip_amount >= 10:
                            user_balance = c2.execute("SELECT balance FROM users WHERE userid = ?;", (ctx.author.id,)).fetchone()
                            if int(user_balance[0]) < tip_amount:
                                return await ctx.send("You do not have enough balance to tip this amount!")
                            else:
                                div = tip_amount / 2
                                oid = c.execute("SELECT orderid FROM pastorders WHERE userid = ? ORDER BY id DESC;", (ctx.author.id,)).fetchone()
                                claimer = c.execute("SELECT claimerid FROM pastorders WHERE orderid = ?;", (oid[0],)).fetchone()
                                deliverer = c.execute("SELECT delivererid FROM pastorders WHERE orderid = ?;", (oid[0],)).fetchone()
                                c2.execute("UPDATE users SET balance = balance - (?) WHERE userid = (?);", (tip_amount, ctx.author.id)) # UPDATE USER BAL
                                conn2.commit()
                                c2.execute("UPDATE users SET balance = balance + (?) WHERE userid = (?);", (div, claimer[0])) # UPDATE CLAIMER BAL
                                conn2.commit()
                                c2.execute("UPDATE users SET balance = balance + (?) WHERE userid = (?);", (div, deliverer[0])) # UPDATE DELIVERER BAL
                                conn2.commit()
                                c.execute("UPDATE pastorders SET tipped = (?) WHERE orderid = (?);", (tip_amount, oid[0])) # UPDATE TIPPED
                                conn.commit()

                                await ctx.send("${} has been tipped successfully! 🎉".format(tip_amount))
                                tip_channel = self.bot.get_channel(self.bot.tip_logs)
                                await tip_channel.send("```\n"+str(ctx.author.name)+" just tipped for an order!\n```\n**Packer:** <@"+str(claimer[0])+">\n**Deliverer:** <@"+str(deliverer[0])+">\n**Tip Amount:** $"+str(tip_amount)+"\n**OrderID:** "+str(oid[0])+"\n\n`They both got $"+str(div)+"`")
                        else:
                            await ctx.send("Minimum amount to tip is 10!")
                    else:
                        await ctx.send("You have already tipped for your last order!")
                else:
                    await ctx.send("You haven't ordered anything yet!")
            else:
                await ctx.send("Your account has been flagged!")
        except:
            return

    @commands.command(help='Give feedback for your last order', usage='feedback <Your Review>')
    @commands.guild_only()
    async def feedback(self, ctx, *, feedback_str : str):
        try:
            await utils.auto_register(ctx.author.id)
            flagged = await utils.check_flagged(ctx.author.id)
            if not flagged:
                conn = sqlite3.connect('./Data/Database/pastorders.db')
                c = conn.cursor()
                conn2 = sqlite3.connect('./Data/Database/users.db')
                c2 = conn2.cursor()

                check_order = c.execute("SELECT * FROM pastorders WHERE userid = ?;", (ctx.author.id,)).fetchone()
                if check_order:
                    is_feedback = c.execute("SELECT feedback FROM pastorders WHERE userid = ? ORDER BY id DESC;", (ctx.author.id,)).fetchone()
                    if str(is_feedback[0]) == 'None':
                        oid = c.execute("SELECT orderid FROM pastorders WHERE userid = ? ORDER BY id DESC;", (ctx.author.id,)).fetchone()
                        item = c.execute("SELECT item FROM pastorders WHERE orderid = ?;", (str(oid[0]),)).fetchone()
                        c.execute("UPDATE pastorders SET feedback = (?) WHERE orderid = (?);", (feedback_str, oid[0])) # UPDATE TIPPED
                        conn.commit()

                        await ctx.send("Your feedback has been successfully sent! ✅")
                        feedback_channel = self.bot.get_channel(self.bot.feedback_logs)
                        await feedback_channel.send("```\n"+str(ctx.author.name)+" shared an order feedback!\n```\n**Order Item:** "+str(item[0])+"\n**OrderID:** "+str(oid[0])+"\n**Feedback:** "+feedback_str)
                    else:
                        await ctx.send("You have already given your feedback for your last order!")
                else:
                    await ctx.send("You haven't ordered anything yet!")
            else:
                await ctx.send("Your account has been flagged!")
        except:
            return

    @feedback.error
    async def feedback_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed= discord.Embed(color= 0xFF0000,title='You did not Provide your Feedback'))

def setup(bot):
        bot.add_cog(OrderCog(bot))
