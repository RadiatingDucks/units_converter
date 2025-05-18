"""Unit Converter application with Database by Amy Lian 15/5/2025"""

#imports sqlite
import sqlite3

def convert(num, unit1):
    #connecting database
    db = sqlite3.connect('units_converter.db')

    cursor = db.cursor()

    #sql commands
    sql = "SELECT ?*to_si_unit FROM Units WHERE unit_name = ?;"

    cursor.execute(sql, (num,unit1))

    info = cursor.fetchall()

    print(info)

    db.close()

if __name__ == "__main__":
    print("Hi")
    number = input()
    start_unit = input()
    convert(number, start_unit)