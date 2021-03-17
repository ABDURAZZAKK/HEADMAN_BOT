import sqlite3

conn = sqlite3.connect('db/df.db')
cursor = conn.cursor()

scrs = [['id, name, active_group','members'],['name','groups'],['id, name','category']]

def fetchall():
    res = 0
    for i in cursor:
        print('   ',i)
        res+=1
    print(' count lines:',res)

for s in scrs:
    cursor.execute(f"select {s[0]} from {s[1]}")
    fetchall()
    input('Enter to continue')
