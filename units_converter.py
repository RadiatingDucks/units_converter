"""Unit Converter application with Database made by Amy Lian 15/5/2025"""

#imports
import sqlite3

import sys

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

    #executing the convert_si with variables in order replacing the '?'s
    cursor.execute(convert_si, (num, unit1, unit1, unit2, unit2))

    #fetching the answer :D
    for ans in cursor.fetchone():
        info = ans

    #prints the answer
    print(f"amount:{info}")

    #closing the database
    db.close()

#variable that stores unit types
unit_type = None

def is_it_valid(inputFromUser):
    #allowing to modify unit1_type in the function
    global unit_type
    
    db = sqlite3.connect('units_converter.db')

    cursor = db.cursor()

    #sql code for checking if input is a unit stored in the database
    is_input_in_tables = """SELECT unit_name
                            FROM Units
                            WHERE (unit_name = ? OR unit_abbreviation = ?);"""
    
    #sql code for finding the type of unit
    inputType = """SELECT Unit_type.id
                            FROM Units
                            JOIN Unit_type ON Units.unit_type = Unit_type.id 
                            WHERE (unit_name = ? OR unit_abbreviation = ?);"""
    
    cursor.execute(is_input_in_tables, (inputFromUser,inputFromUser))

    answer = cursor.fetchone()


    if answer:
        #executing code which finds type of unit1
        cursor.execute(inputType, (inputFromUser,inputFromUser))

        #fetching the type of unit, getting it out of a turple, and storing it in a variable
        for x in cursor.fetchone():
            unit_type = x
        
        db.close()
        #returns boolean
        return(True)
        
    else:
        db.close()
        #returns boolean
        return(False)

#Function which checks if units are same type
def is_it_the_same(type1, type2):
    
    #declaring global variables
    global unit1_type
    global unit2_type

    if unit1_type == unit2_type:
        #returns boolean
        return(True)
    else: 
        #returns boolean
        return(False)




def showAllUnits():

    global unit2_type

    db = sqlite3.connect('units_converter.db')

    cursor = db.cursor()

    show_all = """SELECT unit_name, Unit_type.type_name
                  FROM Units 
                  JOIN Unit_type ON Units.unit_type = Unit_type.id
                  WHERE Unit_type.id = ?
                  ORDER BY Unit_type.id;"""
    
    cursor.execute(show_all, (unit2_type,))
    
    results = cursor.fetchall()

    #prints the results
    for value, value1 in results:
        print(f"Unit: {value} | Type: {value1}")
        
    
    db.close()


#user menu
def menu():

    print("\nGreetings! This is a Unit Converter\nWhat would you like to do today?\n")
    menu_answer = cool_input("(a) Convert Units \n(b) See all units\n(c) Surprise Me!\n\n").lower()

    if menu_answer == "a":
        print("yay")
    
    elif menu_answer == "b":
        print("yipeeee")
    
    elif menu_answer == "c":
        print("boombaclat")
    
    else:
        print("please choose an answer because you made Barry sad.")


def cool_input(prompt):
    user_input = input(prompt).lower().strip()
    if user_input == "exit":
        print("\nExiting Program...thank you for using the Units Converter!\n")
        sys.exit()
    return user_input


#getting input, checking input then converting and giving output
def calc_units():

    #global variables
    global unit1_type
    global unit2_type
    
    #useful variables for detecting if user inputed correct type of answer
    is_number = False
    is_valid_input1 = False
    is_valid_input2 = False

    #If user types a non-float input
    while not is_number:
        try:
            number = float(cool_input("Please type your number: \n"))

            #breaking out of the while loop
            is_number = True

            #if number is zero
            if number == 0:
                print("Please enter a valid number\n")
                is_number = False

        except ValueError:
            print("Please enter a valid value\n")

    #if user types a non-existent unit as start_unit
    while not is_valid_input1:

        start_unit = cool_input("Please type your starting unit: \n").lower()

        #checking if unit is valid
        if is_it_valid(start_unit) == True:
            #storing unit type
            unit1_type = unit_type
            break
        else:
            print("Please enter a valid unit\n")
    
    #if user types a non-existent unit as start_unit
    while not is_valid_input2:

        end_unit = cool_input(f"Please enter the unit you want to convert {start_unit} to: \n").lower()

        #checking if unit is valid
        if is_it_valid(end_unit) == True:

            #storing the unit type
            unit2_type = unit_type

            #checking if units are the same with function
            if is_it_the_same(unit1_type, unit2_type):
                break
            else:
                print("Please use a unit that is the same type as the unit you want to convert")
        else:
            print("Please enter a valid unit\n")
    
    #converting the input
    convert(number, start_unit, end_unit)
    
#main
if __name__ == "__main__":
    menu()
    calc_units()
    showAllUnits()


