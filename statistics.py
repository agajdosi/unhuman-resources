import sqlite3
import sys
import os

def countVisitor(handler):
    cookie = handler.get_cookie("bio_vegan_cookie")
    conn = sqlite3.connect(os.path.join(sys.path[0], 'visitors.db'))

    if cookie == None:
        cursor = conn.execute("INSERT INTO visitors (ip) VALUES ('{0}')".format(handler.request.remote_ip))
        conn.commit()
        cursor = conn.execute("SELECT last_insert_rowid()")
        visitorID = str(cursor.fetchone()[0])
        handler.set_cookie("bio_vegan_cookie", visitorID)
        cookie = visitorID
    else:
        cursor = conn.execute("UPDATE visitors SET visits = visits + 1 WHERE id = '{0}'".format(cookie))
        conn.commit()

    #print("access from:", handler.request, handler.request.headers.get("User-Agent"), "cookie=", cookie)

    conn.close()
    return
