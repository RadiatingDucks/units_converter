"""Unit Converter application with Database made by Amy Lian 15/5/2025"""

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

    cursor.execute(convert_si, (num, unit1, unit1, unit2, unit2))
    #fetching the answer :D
    info = cursor.fetchone()
    #prints the answer
    print(f"amount:{info}")
    #closing the database
    db.close()

def showAllUnits():
    #hmmmmm what should I put here
    print("hmmmmm what should I put here")

if __name__ == "__main__":

    #input values from user
    while input:
        try:
            number = float(input("Please type your number: \n"))
        except ValueError:
            print("Please enter a valid value\n")
            number = float(input("Please type your number: \n"))
        break

    start_unit = str(input("Please type your starting unit: \n"))
    end_unit = str(input("Please enter the unit you want to convert to: \n"))

    #function
    convert(number, start_unit, end_unit)

