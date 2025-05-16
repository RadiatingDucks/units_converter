"""Unit Converter application with Database by Amy Lian 15/5/2025"""

import sqlite3

db = sqlite3.connect('units_converter.db')

cursor = db.cursor()

#sql commands
sql = "SELECT * FROM Units"

cursor.execute(sql)

info = cursor.fetchall()

print(info)

db.close()

