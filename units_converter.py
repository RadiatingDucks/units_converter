"""Unit Converter application with Database by Amy Lian 15/5/2025"""

#imports sqlite
import sqlite3

def convert(num, unit1, unit2):
    #connecting database
    db = sqlite3.connect('units_converter.db')

    cursor = db.cursor()

    #sql command that converts unit 1 to unit 2
    convert_si = """SELECT (? * unit1.to_si_unit) / unit2.to_si_unit 
                    FROM Units unit1, Units unit2
                    WHERE (unit1.unit_abbreviation = ? OR unit1.unit_name = ?)
                    AND (unit2.unit_abbreviation = ? OR unit2.unit_name = ?)
                    AND unit1.unit_type = unit2.unit_type;"""

    cursor.execute(convert_si, (num,unit1,unit1, unit2, unit2))

    info = cursor.fetchone()
    
    print(f"amount:{info}")

    db.close()

if __name__ == "__main__":

    #input values from user
    number = input("Please type your number: \n")
    start_unit = input("Please type your starting unit: \n")
    end_unit = input("Please enter the unit you want to convert to: \n")

    #function
    convert(number, start_unit, end_unit)

