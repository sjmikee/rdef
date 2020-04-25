import sqlite3
import os

path = r'C:\Users\Kobi\Desktop\rdef\rdef\resources\realdefdb.db'

def get_whitelist():
    conn = sqlite3.connect(path, check_same_thread=False)
    c = conn.cursor()
    c.execute('''SELECT * FROM whitelist''')
    query_response = c.fetchall()
    print("whitelist")
    for i in (query_response):
        print(i[0])

def get_blacklist():
    conn = sqlite3.connect(path, check_same_thread=False)
    c = conn.cursor()
    c.execute('''SELECT * FROM blacklist''')
    query_response = c.fetchall()
    print("blacklist")
    for i in (query_response):
        print(i[0])

if __name__ == "__main__":
    get_whitelist()
    get_blacklist()