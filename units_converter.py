"""Unit Converter application with Database made by Amy Lian 15/5/2025"""

#imports
import sqlite3

import sys

import random



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
    print(f"\n{num} {unit1}(s) equal to {info} {unit2}(s)!")

    history(unit1, unit2, num, info)

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







#the main function of showAllUnits(typeOfUnit) is to show units with their type

#it takes in the parameter typeOfUnit, which has 3 significant uses

# if typeOfUnit is 1-6, each number represents a unit type in the SQL tables. The function will
# then call all rows with that unit type and print it. This is useful because it suggests
# the second unit the user can input since the second input is limited by the type of the first 
# unit the user inputted

# if typeOfUnit is 7, all units with their type will be inputted.
# this is for the option 'show all units' in menu

# if typeOfUnit is 8, five randomly selected units will be printed. This is for suggesting units the 
# user can use for the first input unit

def showAllUnits(typeOfUnit):

    db = sqlite3.connect('units_converter.db')

    cursor = db.cursor()

    #
    if typeOfUnit >= 7:

        show_all = """SELECT unit_name, Unit_type.type_name
                    FROM Units 
                    JOIN Unit_type ON Units.unit_type = Unit_type.id
                    ORDER BY Unit_type.id;"""
    
        cursor.execute(show_all)
        
        results = cursor.fetchall()

        #this is a list with all units
        #it stores smaller lists of units with their type
        unit_list = []

            #this is checking if the typeOfUnit is 8, which means only 5 random units are needed.\
            #this is used to suggest units to the user
        if typeOfUnit == 8:

            #prints the results
            for value, value1 in results:
                #making a temporary list with the unit name and type to store in another bigger list
                temporary_list = [value, value1]

                #adding the temporary list to the bigger unit_list
                unit_list.append(temporary_list)

            #selecting k random samples of data(aka units) from unit_list
            random_sample = random.sample(unit_list, k=5)

            #This is to remove the brackets and output the suggestions neatly

            #this removes the values from the random_sample
            for theUnit, theType in random_sample:
                    print(f"Unit: {theUnit} | Type: {theType}")


        #if the typeOfUnit is 7, which signifies that all units need to be printed out
        else:

            #prints the results
            for value, value1 in results:

                print(f"Unit: {value}    | Type: {value1}")
    
        typeOfUnit == 8


    
    else:
        show_some = """SELECT unit_name, Unit_type.type_name
                    FROM Units 
                    JOIN Unit_type ON Units.unit_type = Unit_type.id
                    WHERE Unit_type.id = ?
                    ORDER BY Unit_type.id;"""
    
        cursor.execute(show_some, (typeOfUnit,))
        
        results = cursor.fetchall()

        #prints the results
        for value, value1 in results:
            print(f"Unit: {value}    | Type: {value1}")
        
    
    db.close()





#user menu
def menu():

    #variable for loop for user input
    menu_loop = False

    menu_answer = cool_input("\n(a) How to use?\n(b) Convert Units \n(c) See all units\n(d) Conversion history \n(e) Exit\n\n")

    while not menu_loop:
        if menu_answer == "b":

            #stopping the loop that was catching the invalid inputs
            menu_loop = True
            calc_units()
            menu()
            
        
        elif menu_answer == "c":

            #stopping the loop that was catching the invalid inputs
            menu_loop = True
            showAllUnits(7)
            menu()
            
        
        elif menu_answer == "d":

            #stopping the loop that was catching the invalid inputs
            menu_loop = True
            #testing history
            print(history_dict)
            menu()
            
        
        elif menu_answer == "a":

            #stopping the loop that was catching the invalid inputs
            menu_loop = True

            #printing the instructions on how to use this application
            print("\nThis is a units converter, and it can convert units of length, area, volume, time, mass, and temperature!\n" \
            "\nTyping 'menu' will get you to menu, and typing 'exit' will stop the program.\n" \
            "\nYou can only convert units of the same type (length cannot be converted into area!)" \
            "\nHope you enjoy using this program! ")

            #variuable for the while loop to work
            valid_ans = False

            #loop to catch invalid answers
            while not valid_ans:
                #input for user to go back to menu or stop the program
                going_back = cool_input("\ntype menu to go back or exit to stop the program: ")

                #if user did not read the sentence above properly
                if going_back != "menu" or "exit":

                    #asking the user to try again
                    going_back = cool_input("\nPlease type menu to go back or exit to stop the program:")
            

        elif menu_answer == "e":
            print("\nExiting Program...thank you for using the Units Converter!\n")
            sys.exit()

            
        else:
            print("\nplease choose a valid answer because you made Barry sad.")
            menu()

        



def cool_input(prompt):
    user_input = input(prompt).lower().strip()
    if user_input == "exit":
        print("\nExiting Program...thank you for using the Units Converter!\n")
        sys.exit()
    elif user_input == "menu":
        menu()
    else:
        return user_input


# the function history(unit1, unit2, inputNum, outputNum) stores the past conversions the user
# have done 

# it refreshes everytime the program runs 

# it uses dictionaries to store past conversions, with the keys being a number and the values being
# a list of the units the user used, the number they inputted, and the number that was outputted

#this is the key for dictionary
counting_number = 1

#this is the dictionary
history_dict = {}

def history(unit1, unit2, inputNum, outputNum):

    global counting_number

    #putting the data in a list
    history_list = [unit1, unit2, inputNum, outputNum]

    #putting the data into the dictionary
    history_dict[counting_number] = history_list

    #making sure the key for the dictionary don't overlap
    counting_number += 1

    


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
            number = float(cool_input("\nPlease type the number of measurement you want to convert: \n"))

            #breaking out of the while loop
            is_number = True

            #if number is zero
            if number == 0:
                print("\nPlease enter a valid number\n")
                is_number = False

        except ValueError:
            print("\nPlease enter a valid value\n")

    #if user types a non-existent unit as start_unit
    while not is_valid_input1:

        print("\nSuggestions:")
        showAllUnits(8)
        start_unit = cool_input("\nPlease type the unit you want to convert: \n")

        #checking if unit is valid
        if is_it_valid(start_unit) == True:
            #storing unit type
            unit1_type = unit_type
            break
        else:
            print("\nPlease enter a valid unit\n")
    
    #if user types a non-existent unit as start_unit
    while not is_valid_input2:

        print(f"\nHere are some units you can convert {start_unit} to:\n")
        showAllUnits(unit1_type)
        end_unit = cool_input(f"\nPlease enter the unit you want to convert {start_unit} to: \n")

        #checking if unit is valid
        if is_it_valid(end_unit) == True:

            #storing the unit type
            unit2_type = unit_type

            #checking if units are the same with function
            if is_it_the_same(unit1_type, unit2_type):
                break
            else:
                print("\nPlease use a unit that is the same type as the unit you want to convert\n")
        else:
            print("\nPlease enter a valid unit\n")
    
    #converting the input
    convert(number, start_unit, end_unit)
    menu()
    
#main
if __name__ == "__main__":

    #informs user of this program   
    print("\nGreetings! This is a Unit Converter\nWhat would you like to do today?")
    #activates the menu
    menu()


