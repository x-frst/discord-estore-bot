import sqlite3
import asyncio


async def insert_order(uname, uid, av, order_val, oid, sname, sid, ts, invite, status):
    conn = sqlite3.connect('./Data/Database/orders.db')
    c = conn.cursor()
    conn2 = sqlite3.connect('./Data/Database/invites.db')
    c2 = conn2.cursor()
    conn3 = sqlite3.connect('./Data/Database/users.db')
    c3 = conn3.cursor()
    adder = 1
    c.execute("INSERT INTO orders (username, userid, avatar, order_item, orderid, server, stamp, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (uname, uid, av, order_val, oid, sname, ts, status))
    conn.commit()
    c2.execute("INSERT INTO invites (userid, orderid, serverid, invite) VALUES (?, ?, ?, ?)", (uid, oid, sid, invite))
    conn2.commit()
    c3.execute("UPDATE users SET orders_sent = orders_sent + (?) WHERE userid = (?);", (adder, uid))
    conn3.commit()

async def auto_register(uid):
    conn = sqlite3.connect('./Data/Database/users.db')
    c = conn.cursor()
    check_user = c.execute('SELECT * FROM users WHERE userid = ?;', (int(uid),)).fetchone()
    if not check_user:
        msg = "Hello everyone! I'm from Discord E-Store & I'm here to deliver an order received from {orderer.mention}.\n\nI remember you ordered `{order_item} ({order_id})`, enjoy & please make sure to share your feedback!\n\n{order_links}"
        default_bal = 50
        default_val = 'no'
        default_orders = 0
        c.execute("INSERT INTO users (userid, balance, staff, flagged, orders_sent, orders_deleted, orders_handled, orders_delivered, weekly_orders, delivery_msg) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (uid, default_bal, default_val, default_val, default_orders, default_orders, default_orders, default_orders, default_orders, msg))
        conn.commit()

async def check_flagged(uid):
    conn = sqlite3.connect('./Data/Database/users.db')
    c = conn.cursor()
    is_flagged = c.execute("SELECT flagged FROM users WHERE userid = ?;", (uid,)).fetchone()
    if str(is_flagged[0]) == 'yes':
        return True
    else:
        return False

async def check_staff(uid):
    conn = sqlite3.connect('./Data/Database/users.db')
    c = conn.cursor()
    is_staff = c.execute("SELECT staff FROM users WHERE userid = ?;", (uid,)).fetchone()
    if str(is_staff[0]) == 'yes':
        return True
    else:
        return False
