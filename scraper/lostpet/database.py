import sqlite3

def getClients():
    conn = sqlite3.connect('../web/db.sqlite3')
    c = conn.cursor()

    c.execute('SELECT * FROM Client')
    clients = c.fetchall()

    conn.close()

    return clients

def checkPet(conn, item):
    cur = conn.cursor()

    cur.execute('SELECT * FROM Pet WHERE client_id=? and url=?', (item["client_id"], item["url"]))
    pets = cur.fetchall()

    if len(pets) == 0:
        cur.execute("INSERT INTO Pet (client_id, url) VALUES (?,?)", (item["client_id"], item["url"]))
        conn.commit()

    return len(pets) 

def checkPaidUser(conn, email):
    cur = conn.cursor()

    cur.execute('SELECT * FROM Client WHERE email=? and pricing=0', (email, ))
    clients = cur.fetchall()

    if len(clients) > 0:
        return False

    return True
