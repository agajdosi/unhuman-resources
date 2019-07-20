import sqlite3

def countVisitor(handler):
    cookie = handler.get_cookie("bio_vegan_cookie")
    conn = sqlite3.connect('visitors.db')

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

    conn.close()
    return
