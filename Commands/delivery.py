import discord
import time
from discord.ext import commands
import sqlite3
from helper import utils
import string
import random
import time
import asyncio
import math
from collections import deque
from discord.ext import tasks

class DeliveryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.delivery_task = self.loop.create_task(self.delivery_task())
        self.dq = deque()


    async def delivery_task(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(10.0)
            check = 'packed'
            check2 = 'pending'
            try:
                conn = sqlite3.connect('./Data/Database/orders.db')
                c = conn.cursor()
                conn2 = sqlite3.connect('./Data/Database/invites.db')
                c2 = conn2.cursor()
                packed_orders = c.execute("SELECT orderid FROM orders WHERE status = ? OR status = ?;", (check, check2,)).fetchall()
                for i in packed_orders:
                    for oid in i:
                        start = c2.execute("SELECT claimstamp FROM invites WHERE orderid = ?;", (oid,)).fetchone()
                        end = int(round(time.time() * 1000))
                        ts = (end-int(start[0]))/1000
                        if ts >= 20:
                            set_status = 'pending'
                            c.execute("UPDATE orders SET status = (?) WHERE orderid = (?);", (set_status, oid))
                            conn.commit()
                            channel = self.bot.get_channel(self.bot.queue_channel)
                            if len(self.dq) != 0:
                                user_object = self.dq.popleft()
                                msg = str(user_object.mention)
                                embed = discord.Embed(description="**:truck: | Order `"+oid+"` is ready to get delivered. Send `+deliver "+oid+"` within 20 seconds to get delivery information!**", color=discord.Color.blue())
                                embed.set_footer(text="+deliver "+oid)
                                await channel.send(msg, embed=embed)
                            else:
                                embed = discord.Embed(description="**:truck: | Order `"+oid+"` is ready to get delivered. Send `+deliver "+oid+"` within 20 seconds to get delivery information!**", color=discord.Color.blue())
                                embed.set_footer(text="+deliver "+oid)
                                await channel.send(embed=embed)
                            await asyncio.sleep(20.0)
            except Exception as e:
                print("ERROR IN DELIVERY.PY: "+str(e))
                pass


    @commands.group(aliases=['q'], invoke_without_command=True, help= 'Used to enter delivery queue, if exist then it will show your queue position', usage='queue | queue <leave>')
    @commands.guild_only()
    async def queue(self, ctx):
        try:
            if ctx.channel.id == self.bot.queue_channel:
                await utils.auto_register(ctx.author.id)
                flagged = await utils.check_flagged(ctx.author.id)
                if not flagged:
                    is_staff = await utils.check_staff(ctx.author.id)
                    if is_staff:
                        if ctx.author in self.dq:
                            list_dq = [str(int(idx)+1)+". "+str(user) for idx, user in enumerate(self.dq)]
                            await ctx.send("**Delivery Queue**\n\n"+'\n'.join(list_dq))
                        else:
                            self.dq.append(ctx.author)
                            await ctx.send(ctx.author.mention+" You have joined the delivery queue!")
                    else:
                        await ctx.send("You are not authorized to use this command!")
                else:
                    await ctx.send("You have been restricted to use this bot!")
            else:
                await ctx.send("You cannot use this command in this channel!")
        except:
            return

    @queue.command(help= 'Used to leave delivery queue', usage='queue leave')
    @commands.guild_only()
    async def leave(self, ctx):
        try:
            if ctx.channel.id == self.bot.queue_channel:
                await utils.auto_register(ctx.author.id)
                flagged = await utils.check_flagged(ctx.author.id)
                if not flagged:
                    is_staff = await utils.check_staff(ctx.author.id)
                    if is_staff:
                        if ctx.author in self.dq:
                            self.dq.remove(ctx.author)
                            await ctx.send(ctx.author.mention+" You left the delivery queue.")
                        else:
                            await ctx.send(ctx.author.mention+" You are not in delivery queue!")
                    else:
                        await ctx.send("You are not authorized to use this command!")
                else:
                    await ctx.send("You have been restricted to use this bot!")
            else:
                await ctx.send("You cannot use this command in this channel!")
        except:
            return


    @commands.command(aliases=['d'], help= 'Used to deliver item by specifying order id', usage='deliver <orderid>')
    @commands.guild_only()
    async def deliver(self, ctx, oid:str=None):
        try:
            if oid is not None:
                if ctx.channel.id == self.bot.queue_channel:
                    await utils.auto_register(ctx.author.id)
                    flagged = await utils.check_flagged(ctx.author.id)
                    if not flagged:
                        is_staff = await utils.check_staff(ctx.author.id)
                        if is_staff:
                            conn = sqlite3.connect('./Data/Database/orders.db')
                            c = conn.cursor()
                            conn2 = sqlite3.connect('./Data/Database/invites.db')
                            c2 = conn2.cursor()
                            conn3 = sqlite3.connect('./Data/Database/users.db')
                            c3 = conn3.cursor()
                            conn4 = sqlite3.connect('./Data/Database/pastorders.db')
                            c4 = conn4.cursor()
                            conn5 = sqlite3.connect('./Data/Database/settings.db')
                            c5 = conn5.cursor()
                            check_order = c.execute("SELECT * FROM orders WHERE orderid = ?;", (oid,)).fetchone()
                            if check_order is not None:
                                # USERS DATABASE
                                msg = c3.execute("SELECT delivery_msg FROM users WHERE userid = ?;", (ctx.author.id,)).fetchone()

                                # INVITES DATABASE
                                fetch_orderer = c2.execute("SELECT userid FROM invites WHERE orderid = ?;", (oid,)).fetchone()
                                orderer = self.bot.get_user(int(fetch_orderer[0]))
                                invite = c2.execute("SELECT invite FROM invites WHERE orderid = ?;", (oid,)).fetchone()
                                fetch_packer = c2.execute("SELECT claimerid FROM invites WHERE orderid = ?;", (oid,)).fetchone()
                                packer = self.bot.get_user(int(fetch_packer[0]))
                                deliverer = ctx.author
                                fetch_server = c2.execute("SELECT serverid FROM invites WHERE orderid = ?;", (oid,)).fetchone()
                                guild = self.bot.get_guild(int(fetch_server[0]))
                                fetch_links = c2.execute("SELECT links FROM invites WHERE orderid = ?;", (oid,)).fetchone()
                                order_links = str(fetch_links[0])

                                # ORDERS DATABASE
                                fetch_item = c.execute("SELECT order_item FROM orders WHERE orderid = ?;", (oid,)).fetchone()
                                order_item = str(fetch_item[0])

                                # SETTINGS DATABASE
                                try:
                                    fetch_prefix = c5.execute("SELECT prefix FROM prefix WHERE guildId = ?;", (int(fetch_server[0]),)).fetchone()
                                    prefix = str(fetch_prefix[0])
                                except:
                                    prefix = '+'

                                tval = 0
                                fval = 'None'
                                c4.execute("INSERT INTO pastorders (userid, item, orderid, serverid, claimerid, delivererid, links, tipped, feedback) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (int(fetch_orderer[0]), str(order_item), str(oid), int(fetch_server[0]), int(fetch_packer[0]), int(ctx.author.id), str(order_links[0]), tval, fval))
                                conn4.commit()
                                c.execute("DELETE FROM orders WHERE orderid = (?);", (oid,))
                                conn.commit()
                                c2.execute("DELETE FROM invites WHERE orderid = (?);", (oid,))
                                conn2.commit()
                                adder = 1
                                c3.execute("UPDATE users SET orders_delivered = orders_delivered + (?) WHERE userid = (?);", (adder, ctx.author.id))
                                conn3.commit()
                                c3.execute("UPDATE users SET weekly_orders = weekly_orders + (?) WHERE userid = (?);", (adder, ctx.author.id))
                                conn3.commit()
                                log_channel = self.bot.get_channel(self.bot.order_logs)
                                embed = discord.Embed(description="```\n"+str(msg[0]).format(orderer=orderer, packer=packer, deliverer=deliverer, guild=guild, prefix=prefix, order_item=order_item, order_id=oid, order_links=order_links)+"\n```", color=discord.Color.blue())
                                embed.add_field(name="**Server Invite:**", value="[Click To Join]("+str(invite[0])+")")
                                await ctx.send("Delivery information sent in your DM.")
                                self.dq.append(ctx.author)
                                await ctx.author.send(embed=embed)
                                await log_channel.send("```\nDELIVERY NOTIFICATION!\n```\n**Order `"+str(order_item)+" ("+str(oid)+")` has been delivered by `"+str(ctx.author)+" ("+str(ctx.author.id)+")`**")
                            else:
                                await ctx.send(ctx.author.mention+" Order with that ID does not exist!")
                        else:
                            await ctx.send("You are not authorized to use this command!")
                    else:
                        await ctx.send("You have been restricted to use this bot!")
                else:
                    await ctx.send("You cannot use this command in this channel!")
        except:
            return

def setup(bot):
        bot.add_cog(DeliveryCog(bot))
