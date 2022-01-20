from requests_oauthlib import OAuth2Session
import getpass
from flask import Flask, request, redirect, session, render_template, url_for, send_file, jsonify
import os
import json
import sqlite3
import logging
import datetime as dt
from datetime import timedelta
import time
import requests
import hashlib
import re
import ssl
#from flask_sslify import SSLify


# Settings for your app

base_discord_api_url = 'https://discordapp.com/api'
client_id = '1234567890' # Get from https://discordapp.com/developers/applications
client_secret = 'CLIENT_SECRET_HERE' # Get from https://discordapp.com/developers/applications
client_token = 'CLIENT_TOKEN_HERE' # Get from https://discordapp.com/developers/applications
redirect_uri='https://mysite.com/oauth_callback' # Set it from https://discordapp.com/developers/applications
scope = ['identify', 'guilds'] # It'll ask only for common profile info access with guilds you're in...
token_url = 'https://discordapp.com/api/oauth2/token'
authorize_url = 'https://discordapp.com/api/oauth2/authorize'
revoke_url = 'https://discordapp.com/api/oauth2/token/revoke'
root_page = 'https://www.estorebot.me'
developers = [123, 456, 789] # Developer user IDs
server_id = 1234567890 # Official guild server ID (important!)
resign_channel = 1234567890 # Channel where bot will send user resign logs
application_channel = 1234567890 # Channel where bot will send application logs
appeal_channel = 1234567890 # Channel where bot will send user appeal logs
order_channel = 1234567890 # Channel where bot will send order status logs
staff_role = 1234567890 # Warehouse Staff role id


app = Flask(__name__)
app.secret_key = os.urandom(24)
#sslify = SSLify(app)

@app.route("/full_check")
def full_check():
    try:
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        uid = user.json()['id']
        headers = {"Authorization": "Bot {}".format(client_token), "Content-Type":"application/json"}
        try:
            g_user = requests.get(base_discord_api_url + '/guilds/'+str(server_id)+'/members/'+str(uid), headers=headers)
            user_roles = g_user.json()['roles']
        except:
            return redirect(url_for('error', err="You Must Be A Staff Member To Access This Page!"))
        # https://discordapp.com/developers/docs/resources/user#user-object-user-structure
        if staff_role in user_roles:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()
            check = c.execute('SELECT * FROM users WHERE userid = ?;', (int(uid),)).fetchone()
            if check is not None:
                getStaff = c.execute('SELECT staff FROM users WHERE userid = ?;', (int(uid),)).fetchone()
                if str(getStaff[0]) == 'yes':
                    return True
                else:
                    return redirect(url_for('error', err="You Must Be A Staff Member To Access This Page!"))
            else:
                return redirect(url_for('error', err="You Must Order Something To Unlock Website!"))
        else:
            return redirect(url_for('error', err="You Must Join Official Bot Server!"))
    except:
        return redirect('/login')


@app.route("/check_staff")
def check_staff():
    try:
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        uid = user.json()['id']
        # https://discordapp.com/developers/docs/resources/user#user-object-user-structure
        conn = sqlite3.connect('./Data/Database/users.db')
        c = conn.cursor()
        check = c.execute('SELECT * FROM users WHERE userid = ?;', (int(uid),)).fetchone()
        if check is not None:
            getStaff = c.execute('SELECT staff FROM users WHERE userid = ?;', (int(uid),)).fetchone()
            if str(getStaff[0]) == 'yes':
                return True
            else:
                return redirect(url_for('error', err="You Must Be A Staff Member To Access This Page!"))
        else:
            return redirect(url_for('error', err="You Must Order Something To Unlock Website!"))
    except:
        return redirect('/login')

@app.route("/error")
def error():
    err = request.args['err']
    return render_template("error.html", error=err)

def is_url_image(image_url):
    try:
        links = image_url.split('nTnsLRK,')
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        for i in links:
            r = requests.head(str(i).replace('nTnsLRK', ''))
            if r.headers["content-type"] not in image_formats:
                return False
        return True
    except:
        return False


@app.route("/get_orders", methods=['GET'])
def get_orders():
    try:
        if check_staff() == True:
            conn = sqlite3.connect('./Data/Database/orders.db')
            c = conn.cursor()
            orders = c.execute('SELECT * FROM orders').fetchall()
            return jsonify(orders)
        else:
            return "Not Authorized", 400
    except:
        return "None"



@app.route("/get_managed", methods=['GET'])
def get_managed():
    try:
        if check_staff() == True:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            get_item = c.execute('SELECT orders_handled FROM users WHERE userid = ?;', (uid,)).fetchone()
            return str(get_item[0])
        else:
            return "Loading..."
    except:
        return "Loading..."

@app.route("/get_weekly", methods=['GET'])
def get_weekly():
    try:
        if check_staff() == True:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            get_item = c.execute('SELECT weekly_orders FROM users WHERE userid = ?;', (uid,)).fetchone()
            return str(get_item[0])
        else:
            return "Loading..."
    except:
        return "Loading..."

@app.route("/get_delivered", methods=['GET'])
def get_delivered():
    try:
        if check_staff() == True:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            get_item = c.execute('SELECT orders_delivered FROM users WHERE userid = ?;', (uid,)).fetchone()
            return str(get_item[0])
        else:
            return "Loading..."
    except:
        return "Loading..."

@app.route("/get_sent", methods=['GET'])
def get_sent():
    try:
        if check_staff() == True:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            get_item = c.execute('SELECT orders_sent FROM users WHERE userid = ?;', (uid,)).fetchone()
            return str(get_item[0])
        else:
            return "Loading..."
    except:
        return "None"

@app.route("/get_msg", methods=['GET'])
def get_msg():
    try:
        if check_staff() == True:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            get_item = c.execute('SELECT delivery_msg FROM users WHERE userid = ?;', (uid,)).fetchone()
            return str(get_item[0])
        else:
            return "Loading..."
    except:
        return "None"


@app.route("/delivery_msg", methods=['GET', 'POST'])
def delivery_msg():
    try:
        if check_staff() == True:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            plain_msg = request.form['delivery_message']
            check_links = re.findall(r'{(order_links)}', plain_msg)
            if len(check_links) == 1:
                allowed_variables = ['orderer', 'orderer.name', 'orderer.mention', 'orderer.id', 'packer', 'packer.name', 'packer.id', 'deliverer', 'deliverer.name', 'deliverer.mention', 'deliverer.id', 'guild.name', 'guild.id', 'prefix', 'order_item', 'order_id', 'order_links']
                re_check = re.findall(r"{(.*?)}", plain_msg)
                check_others = all(var in allowed_variables for var in re_check)
                if check_others == True:
                    c.execute("UPDATE users SET delivery_msg = (?) WHERE userid = (?);", (plain_msg, int(uid)))
                    conn.commit()
                    return "Successfully Set New Delivery Message!"
                else:
                    return "Any Other Variables Are Not Allowed!", 400
            else:
                return "Order Links Variable Not Found OR Used More Than Once!", 400
        else:
            return "Not Authorized", 400
    except:
        return "An Internal Error Occured!", 400

@app.route("/resign_user", methods=['GET', 'POST'])
def resign_user():
    try:
        if check_staff() == True:
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            uname = user.json()['username']+'#'+user.json()['discriminator']
            set_resign = 'no'
            c.execute("UPDATE users SET staff = (?) WHERE userid = (?);", (set_resign, int(uid)))
            conn.commit()
            headers = {"Authorization": "Bot {}".format(client_token), "Content-Type":"application/json"}
            try:
                requests.delete(base_discord_api_url + '/guilds/'+str(server_id)+'/members/'+str(uid)+'/roles/'+str(staff_role), headers=headers)
            except:
                pass
            log_message = "**```css\nUser Resign Notice```\n`"+str(uname)+" ("+str(uid)+")` Just Resigned From Discord E-Store, Goodbye!**"
            log_json = json.dumps ( {"content":log_message} )
            requests.post(base_discord_api_url + '/channels/'+str(resign_channel)+'/messages', headers=headers, data=log_json)
            return '/'
        else:
            return "Not Authorized", 400
    except:
        return "An Internal Error Occured!", 400

@app.route("/user_application", methods=['GET', 'POST'])
def user_application():
    try:
        conn = sqlite3.connect('./Data/Database/users.db')
        c = conn.cursor()
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        uid = user.json()['id']
        uname = user.json()['username']+'#'+user.json()['discriminator']
        getFlagged = c.execute('SELECT flagged FROM users WHERE userid = ?;', (int(uid),)).fetchone()
        if str(getFlagged[0]) == 'no':
            getStaff = c.execute('SELECT staff FROM users WHERE userid = ?;', (int(uid),)).fetchone()
            if str(getStaff[0]) == 'no':
                reason = request.form['application_reason']
                stamp = dt.datetime.now()
                cur_time = '%H:%M'
                cur_date = '%A, %d %b'
                headers = {"Authorization": "Bot {}".format(client_token), "Content-Type":"application/json"}
                log_message = "**```css\nNew User Application```\n**Username:** `"+str(uname)+"`\n**User ID:** `"+str(uid)+"`\n**Apply Reason:** ```\n"+str(reason)+"\n```\n**Date-Time:** `"+str(stamp.strftime(cur_date))+" At "+str(stamp.strftime(cur_time))+"`**"
                log_json = json.dumps ( {"content":log_message} )
                requests.post(base_discord_api_url + '/channels/'+str(application_channel)+'/messages', headers=headers, data=log_json)
                return 'Your Application Delivery Was Successful, We Will Get Back To You Shortly!'
            else:
                return "You Are Already A Staff Member!", 400
        else:
            return "You Have Been Blacklisted From Bot!", 400
    except:
        return "An Internal Error Occured!", 400

@app.route("/user_appeal", methods=['GET', 'POST'])
def user_appeal():
    try:
        conn = sqlite3.connect('./Data/Database/users.db')
        c = conn.cursor()
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        uid = user.json()['id']
        uname = user.json()['username']+'#'+user.json()['discriminator']
        type = request.form['appeal_type']
        chance = request.form['appeal_chance']
        reason = request.form['appeal_reason']
        stamp = dt.datetime.now()
        cur_time = '%H:%M'
        cur_date = '%A, %d %b'
        headers = {"Authorization": "Bot {}".format(client_token), "Content-Type":"application/json"}
        log_message = "**```css\nNew User Appeal```\n**Username:** `"+str(uname)+"`\n**User ID:** `"+str(uid)+"`\n**Appeal Type:** `"+str(type)+"`\n**Ban Reason:** `"+str(reason)+"`\n**Ban Chance:** `"+str(chance)+"`\n**Date-Time:** `"+str(stamp.strftime(cur_date))+" At "+str(stamp.strftime(cur_time))+"`**"
        log_json = json.dumps ( {"content":log_message} )
        requests.post(base_discord_api_url + '/channels/'+str(appeal_channel)+'/messages', headers=headers, data=log_json)
        return 'Your Appeal Delivery Was Successful, We Will Get Back To You Shortly!'
    except:
        return "An Internal Error Occured!", 400

@app.route("/get_bal", methods=['GET'])
def get_bal():
    try:
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        uid = user.json()['id']
        conn = sqlite3.connect('./Data/Database/users.db')
        c = conn.cursor()
        bal = c.execute('SELECT balance FROM users WHERE userid = ?;', (int(uid),)).fetchone()
        return '${:,}'.format(int(bal[0]))
    except:
        return "None"


@app.route("/order")
def order():
    try:
        if full_check() == True:
            get_code = request.args.get("oid", "")
            code = "{}".format(get_code)
            conn = sqlite3.connect('./Data/Database/orders.db')
            c = conn.cursor()
            conn2 = sqlite3.connect('./Data/Database/invites.db')
            c2 = conn2.cursor()
            conn3 = sqlite3.connect('./Data/Database/claimers.db')
            c3 = conn3.cursor()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            uname = user.json()['username']+'#'+user.json()['discriminator']
            uav = "https://cdn.discordapp.com/avatars/"+str(uid)+"/"+user.json()['avatar']
            check_order = c.execute('SELECT * FROM orders WHERE orderid = ?;', (code,)).fetchone()
            if check_order is not None:
                same_person = c.execute('SELECT userid FROM orders WHERE orderid = ?;', (code,)).fetchone()
                if int(same_person[0]) != int(uid):
                    check_claimer = c3.execute('SELECT * FROM claimers WHERE userid = ?;', (uid,)).fetchone()
                    if check_claimer is None:
                        get_status = c.execute('SELECT status FROM orders WHERE orderid = ?;', (code,)).fetchone()
                        get_claimer = c2.execute('SELECT claimerid FROM invites WHERE orderid = ?;', (code,)).fetchone()
                        if ((str(get_status[0]) == 'unclaimed') and (bool(get_claimer[0]) == False or bool(get_claimer[0]) == None)):
                            set_status = 'claimed'
                            now = int(round(time.time() * 1000))
                            c.execute("UPDATE orders SET status = (?) WHERE orderid = (?);", (set_status, code))
                            conn.commit()
                            c2.execute("UPDATE invites SET claimerid = (?) WHERE orderid = (?);", (uid, code))
                            conn2.commit()
                            c2.execute("UPDATE invites SET claimstamp = (?) WHERE orderid = (?);", (now, code))
                            conn2.commit()
                            c3.execute("INSERT INTO claimers (userid, orderid) VALUES (?, ?)", (uid, code))
                            conn3.commit()
                            get_order = c.execute('SELECT order_item FROM orders WHERE orderid = ?;', (code,)).fetchone()
                            get_username = c.execute('SELECT username FROM orders WHERE orderid = ?;', (code,)).fetchone()
                            get_avatar = c.execute('SELECT avatar FROM orders WHERE orderid = ?;', (code,)).fetchone()
                            get_stamp = c.execute('SELECT stamp FROM orders WHERE orderid = ?;', (code,)).fetchone()
                            get_server = c.execute('SELECT server FROM orders WHERE orderid = ?;', (code,)).fetchone()
                            get_dm = json.dumps( {"recipient_id": int(same_person[0])} )
                            dm_message = "**:baggage_claim: | Your order has been claimed by `"+str(uname)+"`**"
                            headers = {"Authorization": "Bot {}".format(client_token), "Content-Type":"application/json"}
                            try:
                                req_dm = requests.post(base_discord_api_url + '/users/@me/channels', headers=headers, data=get_dm)
                                user_dm = req_dm.json()['id']
                            except:
                                pass
                            dm_json = json.dumps ( {"content":dm_message} )
                            try:
                                requests.post(base_discord_api_url + '/channels/'+user_dm+'/messages', headers=headers, data=dm_json)
                            except:
                                pass
                            return render_template('order.html', order_item=str(get_order[0]), username=str(get_username[0]), avatar=str(get_avatar[0]), stamp=int(get_stamp[0]), server=str(get_server[0]), o_code=str(code), user_name=str(uname), user_image=str(uav))
                    else:
                        claimed_oid = c3.execute('SELECT orderid FROM claimers WHERE userid = ?;', (uid,)).fetchone()
                        if str(claimed_oid[0]) == code:
                            get_status = c.execute('SELECT status FROM orders WHERE orderid = ?;', (code,)).fetchone()
                            get_claimer = c2.execute('SELECT claimerid FROM invites WHERE orderid = ?;', (code,)).fetchone()
                            if str(get_status[0]) == 'claimed' and int(get_claimer[0]) == int(uid):
                                get_order = c.execute('SELECT order_item FROM orders WHERE orderid = ?;', (code,)).fetchone()
                                get_username = c.execute('SELECT username FROM orders WHERE orderid = ?;', (code,)).fetchone()
                                get_avatar = c.execute('SELECT avatar FROM orders WHERE orderid = ?;', (code,)).fetchone()
                                get_stamp = c.execute('SELECT stamp FROM orders WHERE orderid = ?;', (code,)).fetchone()
                                get_server = c.execute('SELECT server FROM orders WHERE orderid = ?;', (code,)).fetchone()
                                return render_template('order.html', order_item=str(get_order[0]), username=str(get_username[0]), avatar=str(get_avatar[0]), stamp=int(get_stamp[0]), server=str(get_server[0]), o_code=str(code), user_name=str(uname), user_image=str(uav))
                            else:
                                return render_template("error.html", error="Someone Already Claimed This Order!")
                        else:
                            return render_template("error.html", error="You Have Already Claimed Another Order!")
                else:
                    return render_template("error.html", error="You Can't Claim Your Own Order!")
        else:
            return redirect("/full_check")
    except:
        return render_template("error.html", error="An Internal Error Occured!")

@app.route("/pack_order", methods=['GET', 'POST'])
def pack_order():
    try:
        if full_check() == True:
            conn = sqlite3.connect('./Data/Database/orders.db')
            c = conn.cursor()
            conn2 = sqlite3.connect('./Data/Database/invites.db')
            c2 = conn2.cursor()
            conn3 = sqlite3.connect('./Data/Database/claimers.db')
            c3 = conn3.cursor()
            code = request.form['order_id']
            get_status = c.execute('SELECT status FROM orders WHERE orderid = ?;', (code,)).fetchone()
            get_claimer = c2.execute('SELECT claimerid FROM invites WHERE orderid = ?;', (code,)).fetchone()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            uname = user.json()['username']+'#'+user.json()['discriminator']
            if str(get_status[0]) == 'claimed' and int(get_claimer[0]) == int(uid):
                get_links = request.form['img_links']
                if is_url_image(get_links):
                    links = get_links.split('nTnsLRK,')
                    l = []
                    for i in links:
                        l.append(str(i).replace('nTnsLRK', ''))
                    p = '\n'.join(l)
                    set_status = 'packed'
                    now = int(round(time.time() * 1000))
                    db_users = sqlite3.connect('./Data/Database/users.db')
                    users_cursor = db_users.cursor()
                    adder = 1
                    users_cursor.execute("UPDATE users SET orders_handled = orders_handled + (?) WHERE userid = (?);", (adder, int(uid)))
                    db_users.commit()
                    users_cursor.execute("UPDATE users SET weekly_orders = weekly_orders + (?) WHERE userid = (?);", (adder, int(uid)))
                    db_users.commit()
                    c3.execute('DELETE FROM claimers WHERE userid = ?;', (uid,))
                    conn3.commit()
                    c2.execute("UPDATE invites SET links = (?) WHERE orderid = (?);", (p, code))
                    conn2.commit()
                    c2.execute("UPDATE invites SET claimstamp = (?) WHERE orderid = (?);", (now, code))
                    conn2.commit()
                    c.execute("UPDATE orders SET status = (?) WHERE orderid = (?);", (set_status, code))
                    conn.commit()
                    orderer_name = c.execute('SELECT username FROM orders WHERE orderid = ?;', (code,)).fetchone()
                    orderer_id = c.execute('SELECT userid FROM orders WHERE orderid = ?;', (code,)).fetchone()
                    order_name = c.execute('SELECT order_item FROM orders WHERE orderid = ?;', (code,)).fetchone()
                    order_server = c.execute('SELECT server FROM orders WHERE orderid = ?;', (code,)).fetchone()
                    order_server_id = c2.execute('SELECT serverid FROM invites WHERE orderid = ?;', (code,)).fetchone()
                    get_dm = json.dumps( {"recipient_id": int(orderer_id[0])} )
                    headers = {"Authorization": "Bot {}".format(client_token), "Content-Type":"application/json"}
                    try:
                        req_dm = requests.post(base_discord_api_url + '/users/@me/channels', headers=headers, data=get_dm)
                        user_dm = req_dm.json()['id']
                    except:
                        pass
                    dm_message = "**:package: | Your order has been packed & shipped by `"+str(uname)+"`, delivery may take upto 3 minutes!**"
                    log_message = "**```css\nOrder Packed & Shipped```\nOrder: `"+str(order_name[0])+" ("+str(code)+")`\nOrdered By: `"+str(orderer_name[0])+" ("+str(orderer_id[0])+")`\nGuild: `"+str(order_server[0])+" ("+str(order_server_id[0])+")`\nPacked By: `"+str(uname)+" ("+str(uid)+")`**"
                    dm_json = json.dumps ( {"content":dm_message} )
                    log_json = json.dumps ( {"content":log_message} )
                    requests.post(base_discord_api_url + '/channels/'+str(order_channel)+'/messages', headers=headers, data=log_json)
                    try:
                        requests.post(base_discord_api_url + '/channels/'+user_dm+'/messages', headers=headers, data=dm_json)
                    except:
                        pass
                    return '/orders'
                else:
                    return "One Of The Link Does Not Contain Any Image!", 400
            else:
                return "Order Not Found Or Already Claimed!", 400
        else:
            return redirect("/full_check")
    except:
        return "An Internal Error Occured!", 400


@app.route("/delete_order", methods=['GET', 'POST'])
def delete_order():
    try:
        if full_check() == True:
            conn = sqlite3.connect('./Data/Database/orders.db')
            c = conn.cursor()
            conn2 = sqlite3.connect('./Data/Database/invites.db')
            c2 = conn2.cursor()
            conn3 = sqlite3.connect('./Data/Database/claimers.db')
            c3 = conn3.cursor()
            code = request.form['order_id']
            reason = request.form['deletion_reason']
            get_status = c.execute('SELECT status FROM orders WHERE orderid = ?;', (code,)).fetchone()
            get_claimer = c2.execute('SELECT claimerid FROM invites WHERE orderid = ?;', (code,)).fetchone()
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            uname = user.json()['username']+'#'+user.json()['discriminator']
            if str(get_status[0]) == 'claimed' and int(get_claimer[0]) == int(uid):
                orderer_name = c.execute('SELECT username FROM orders WHERE orderid = ?;', (code,)).fetchone()
                orderer_id = c.execute('SELECT userid FROM orders WHERE orderid = ?;', (code,)).fetchone()
                order_name = c.execute('SELECT order_item FROM orders WHERE orderid = ?;', (code,)).fetchone()
                order_server = c.execute('SELECT server FROM orders WHERE orderid = ?;', (code,)).fetchone()
                order_server_id = c2.execute('SELECT serverid FROM invites WHERE orderid = ?;', (code,)).fetchone()
                get_dm = json.dumps( {"recipient_id": int(orderer_id[0])} )
                headers = {"Authorization": "Bot {}".format(client_token), "Content-Type":"application/json"}
                try:
                    req_dm = requests.post(base_discord_api_url + '/users/@me/channels', headers=headers, data=get_dm)
                    user_dm = req_dm.json()['id']
                except:
                    pass
                dm_message = "**:wastebasket: | Your order has been deleted by `"+str(uname)+"`, with reason:\n`"+str(reason)+"`\n\n_Read `rules` before sending any order!_**"
                log_message = "**```css\nOrder Deleted```\nOrder: `"+str(order_name[0])+" ("+str(code)+")`\nOrdered By: `"+str(orderer_name[0])+" ("+str(orderer_id[0])+")`\nGuild: `"+str(order_server[0])+" ("+str(order_server_id[0])+")`\nDeleted By: `"+str(uname)+" ("+str(uid)+")`**"
                dm_json = json.dumps ( {"content":dm_message} )
                log_json = json.dumps ( {"content":log_message} )
                db_users = sqlite3.connect('./Data/Database/users.db')
                users_cursor = db_users.cursor()
                adder = 1
                users_cursor.execute("UPDATE users SET orders_handled = orders_handled + (?) WHERE userid = (?);", (adder, int(uid)))
                db_users.commit()
                users_cursor.execute("UPDATE users SET weekly_orders = weekly_orders + (?) WHERE userid = (?);", (adder, int(uid)))
                db_users.commit()
                users_cursor.execute("UPDATE users SET orders_deleted = orders_deleted + (?) WHERE userid = (?);", (adder, int(orderer_id[0])))
                db_users.commit()
                requests.post(base_discord_api_url + '/channels/'+str(order_channel)+'/messages', headers=headers, data=log_json)
                try:
                    requests.post(base_discord_api_url + '/channels/'+user_dm+'/messages', headers=headers, data=dm_json)
                except:
                    pass
                c3.execute('DELETE FROM claimers WHERE userid = ?;', (uid,))
                conn3.commit()
                c2.execute('DELETE FROM invites WHERE orderid = ?;', (code,))
                conn2.commit()
                c.execute('DELETE FROM orders WHERE orderid = ?;', (code,))
                conn.commit()
                return '/orders'
            else:
                return "Order Not Found Or Already Claimed!", 400
        else:
            return redirect("/full_check")
    except:
        return "An Internal Error Occured!", 400


@app.route("/")
def index():
    try:
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        uid = user.json()['id']
        uname = user.json()['username']+'#'+user.json()['discriminator']
        uav = "https://cdn.discordapp.com/avatars/"+str(uid)+"/"+user.json()['avatar']
        return render_template("home.html", user_image=uav, user_name=str(uname))
    except:
        return render_template("index.html")

@app.route("/orders")
def orders():
    try:
        if full_check() == True:
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            uname = user.json()['username']+'#'+user.json()['discriminator']
            uav = "https://cdn.discordapp.com/avatars/"+str(uid)+"/"+user.json()['avatar']
            return render_template("orders.html", user_image=uav, user_name=str(uname))
        else:
            return redirect("/full_check")
    except:
        return redirect('/login')

@app.route("/staff")
def staff():
    try:
        if full_check() == True:
            discord = OAuth2Session(client_id, token=session['discord_token'])
            user = discord.get(base_discord_api_url + '/users/@me')
            uid = user.json()['id']
            uname = user.json()['username']+'#'+user.json()['discriminator']
            uav = "https://cdn.discordapp.com/avatars/"+str(uid)+"/"+user.json()['avatar']
            conn = sqlite3.connect('./Data/Database/users.db')
            c = conn.cursor()
            val = 'yes'
            get_toppers = c.execute('SELECT userid FROM users WHERE staff = (?) ORDER BY weekly_orders DESC LIMIT 3;', (val,)).fetchall()
            order_count = c.execute('SELECT weekly_orders FROM users WHERE staff = (?) ORDER BY weekly_orders DESC LIMIT 3;', (val,)).fetchall()
            headers = {"Authorization": "Bot {}".format(client_token), "Content-Type":"application/json"}
            toppers = []
            for i in get_toppers:
                for topper_id in i:
                    req_dm = requests.get(base_discord_api_url + '/users/'+str(topper_id), headers=headers)
                    toppers.append(str(req_dm.json()['username']+'#'+req_dm.json()['discriminator']))
            orders_list = [j for t in order_count for j in t]
            return render_template("staff.html", user_image=uav, user_name=str(uname), top_users=toppers, top_orders=orders_list)
        else:
            return redirect("/full_check")
    except:
        return redirect('/login')

@app.route("/apply")
def apply():
    try:
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        uid = user.json()['id']
        uname = user.json()['username']+'#'+user.json()['discriminator']
        uav = "https://cdn.discordapp.com/avatars/"+str(uid)+"/"+user.json()['avatar']
        return render_template("apply.html", user_image=uav, user_name=str(uname), user_id=str(uid))
    except:
        return redirect('/login')

@app.route("/appeal")
def appeal():
    try:
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        uid = user.json()['id']
        uname = user.json()['username']+'#'+user.json()['discriminator']
        uav = "https://cdn.discordapp.com/avatars/"+str(uid)+"/"+user.json()['avatar']
        return render_template("appeal.html", user_image=uav, user_name=str(uname), user_id=str(uid))
    except:
        return redirect('/login')

@app.route("/profile")
def profile():
    try:
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        uid = user.json()['id']
        uname = user.json()['username']+'#'+user.json()['discriminator']
        uav = "https://cdn.discordapp.com/avatars/"+str(uid)+"/"+user.json()['avatar']
        conn = sqlite3.connect('./Data/Database/users.db')
        c = conn.cursor()
        getStaff = c.execute('SELECT staff FROM users WHERE userid = ?;', (int(uid),)).fetchone()
        if int(uid) in developers:
            position = "Bot Developer"
            badge_list = ["<img data-toggle='tooltip' style='cursor: pointer;' data-placement='top' title='Bot Developer' src='./static/images/dev.png' width='12%' />", "<img data-toggle='tooltip' style='cursor: pointer;' data-placement='top' title='Warehouse Staff' src='./static/images/packer.png' width='12%' />", "<img data-toggle='tooltip' style='cursor: pointer;' data-placement='top' title='Customer' src='./static/images/customer.png' width='12%' />"]
        elif str(getStaff[0]) == 'yes':
            position = "Warehouse Staff"
            badge_list = ["<img data-toggle='tooltip' style='cursor: pointer;' data-placement='top' title='Warehouse Staff' src='./static/images/packer.png' width='12%' />", "<img data-toggle='tooltip' style='cursor: pointer;' data-placement='top' title='Customer' src='./static/images/customer.png' width='12%' />"]
        else:
            position = "Customer"
            badge_list = ["<img data-toggle='tooltip' style='cursor: pointer;' data-placement='top' title='Customer' src='./static/images/customer.png' width='12%' />"]
        return render_template("profile.html", user_image=uav, user_name=str(uname), user_id=str(uid), user_position=position, badges=badge_list)
    except:
        return redirect('/login')

@app.route("/login")
def login():
    """
    Presents the 'Login with Discord' link
    """
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    session['state'] = state
    return redirect(login_url)


@app.route("/logout")
def logout():
    """
    It'll logout your session & clear your session key if found!
    """
    try:
        session['discord_token'] = ""
        token = ""
        return redirect('/')
    except:
        return redirect('/')


@app.route("/oauth_callback")
def oauth_callback():
    try:
        """
        This callback is called just after the /login state
        This is the last landing page which will show your
        Userid & Username to check if you're logged in or not
        """
        discord = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['state'], scope=scope)
        token = discord.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url,
        )
        session['discord_token'] = token
        discord = OAuth2Session(client_id, token=session['discord_token'])
        user = discord.get(base_discord_api_url + '/users/@me')
        getID = user.json()['id']
        getName = user.json()['username']+'#'+user.json()['discriminator']
        return redirect('/')
    except Exception as e:
        return render_template("error.html", error="You've Denied The Authorization!")


@app.errorhandler(Exception)
def exception_handler(error):
    if '404' in str(error):
        return render_template("error.html", error="404 : I Think You Have Lost Your Way!")
    elif '405' in str(error):
        print(str(error))
        return render_template("error.html", error="405 : The Method Is Not Allowed!")
    else:
        print(str(error))
        return render_template("error.html", error="500 : Critical Internal Error Occured!")


if __name__ == '__main__':
    app._static_folder = './static' # Default Initialization
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # I don't know what is this
    app.debug = False
    log = logging.getLogger('werkzeug') # Common logger type
    log.disabled = True #Use while publish (this will show logs if commented)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #context.load_cert_chain('./Data/server.crt', './Data/server.key') # Site certificates if SSL
    app.run(host='0.0.0.0', port=443, ssl_context=context) # Set this as per your site preferences
