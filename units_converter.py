"""Unit Converter application with Database made by Amy Lian 15/5/2025"""

#imports
import sqlite3

import sys

import random

import difflib


#This is a function that converts units using a database with the conversion values. 

#When all the parameters are valid the sql code will output the value of unit1 but with the unit of unit2

# In def convert(num, unit1, unit2), num is the input number, unit1 is the unit being converted, and 
# unit2 is the unit unit1 is being converted to. 

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
    #this is in a for loop since it removes the brackets around the output
    for ans in cursor.fetchone():
        info = ans

    #prints the answer
    print(f"\n{num} {unit1}(s) is equal to {info} {unit2}(s)!")

    #storing this conversion
    history(unit1, unit2, num, info)

    #closing the database
    db.close()







#This function checks if the user input is actually in the database.

#If the user input is in the database then the function will find its type and store it,
# and return the boolean True

#If the user input is not in the database the function will return False

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

    #fetching the answewr
    answer = cursor.fetchone()

    #this is to check if answer is None or an actual unit
    if answer:
        #executing code which finds type of unit
        cursor.execute(inputType, (inputFromUser,inputFromUser))

        #fetching the type of unit, getting it out of a turple, and storing it in a variable
        for x in cursor.fetchone():
            unit_type = x
        
        db.close()
        #returns boolean which means the unit is valid
        return(True)
        
    else:
        db.close()
        #returns boolean false which means the unit is invalid
        return(False)







#Function which checks if units are same type
#This is so the user will not convert units like grams to metres

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

# if typeOfUnit is 1-5, each number represents a unit type in the SQL tables. The function will
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

    #chcking if it's a special case like calling all the units or a random suggestion
    if typeOfUnit >= 7:

        #selects all units with their
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


    #if the parameter is 1-5, which calls for one of the five types units can have
    #this is for the second unit input to show the users some units fo teh saem type they can use
    else:

        #selecting units by matching their type id with the parameter
        show_some = """SELECT unit_name, Unit_type.type_name
                    FROM Units 
                    JOIN Unit_type ON Units.unit_type = Unit_type.id
                    WHERE Unit_type.id = ?
                    ORDER BY Unit_type.id;"""
    
        cursor.execute(show_some, (typeOfUnit,))
        
        #fteching the data
        results = cursor.fetchall()

        #prints the results
        for value, value1 in results:
            print(f"Unit: {value}    | Type: {value1}")
        
    
    db.close()







#user menu
#this is where the user can choose to do different things
#it can be called by typing menu

def menu():

    #variable for loop for user input to catch any invalid inputs
    menu_loop = False

    #showing users the options
    menu_answer = cool_input("\n(a) How to use?\n(b) Convert Units \n(c) See all units\n(d) Conversion history \n(e) Exit\n\n")

    #big loop with lots of actions you can choose to take
    while not menu_loop:

        #this activates the calc_units function which will calculate units
        if menu_answer == "b":

            #stopping the loop that was catching the invalid inputs
            menu_loop = True
            calc_units()

            #returning to menu
            menu()
            
        #This shows the list of units the user can use
        elif menu_answer == "c":

            #stopping the loop that was catching the invalid inputs
            menu_loop = True
            showAllUnits(7)

            #returning to menu
            menu()
            
        #this option activates the history function
        #it will input 'No history available' if there is no history
        elif menu_answer == "d":

            #stopping the loop that was catching the invalid inputs
            menu_loop = True

            #checking if tehre are values in the history dictionary
            if history_dict:

                print("\nHistory\n")

                for key, information in history_dict.items():
                    print(str(key) + " | " + information[0] + " | " + information[1] + " | " + str(information[2]) + " | " + str(information[3]))

            #if there are no values in the history dictionary
            else:
                print("\nNo history avaliable\n")

            #returning to menu
            menu()
            
        
        #this option informs the user on how to use this application
        elif menu_answer == "a":

            #stopping the loop that was catching the invalid inputs
            menu_loop = True

            #printing the instructions on how to use this application
            print("\nThis is a units converter, and it can convert units of length, area, volume, time, andf mass!\n" \
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
            

        #this option will stop the program
        elif menu_answer == "e":
            print("\nExiting Program...thank you for using the Units Converter!\n")

            #exiting
            sys.exit()

        #if the user did not choose any of the options above
        else:
            print("\nplease choose a valid answer.")

            #shows the menu again
            menu()



        



#this function detects if the user typed exit or menu, which will then perform these actions
def cool_input(prompt):

    #making the user input lowercase and removing whitespace behind it
    user_input = input(prompt).lower().strip()

    #if the user typed exit
    if user_input == "exit":
        print("\nExiting Program...thank you for using the Units Converter!\n")

        #stops program
        sys.exit()
    
    #if user typed meu
    elif user_input == "menu":

        #goes to menu
        menu()

    #not a special input
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

    #making the variable counting_number accessible
    global counting_number

    #putting the data in a list
    history_list = [unit1, unit2, inputNum, outputNum]

    #putting the data into the dictionary
    history_dict[counting_number] = history_list

    #making sure the key for the dictionary don't overlap
    counting_number += 1







#suggests units close to the user's input if tehir input is invalid

#makes the program frinedly for dyslexic people

def didYouMean(inputUnit):

    db = sqlite3.connect('units_converter.db')

    cursor = db.cursor()

    #selecting everything from units table
    code = """SELECT unit_name 
              FROM Units"""
    
    cursor.execute(code)

    #list of all the units
    unit_list = cursor.fetchall()
    
    #this is a new list to store data after the data from unit_list is stripped
    new_list = []

    #stripping the brackets around the data in the unit_list
    for sub_list in unit_list:

        for unit in sub_list:

            #adding unit to new_list
            new_list.append(unit)

    #using difflib
    #this is the most important part of this function
    #this gives close matches based on an accuracy you can change
    #gives you 5 suggestions of units similar to the input

    suggestions = difflib.get_close_matches(inputUnit, new_list, n=5, cutoff= 0.6)


    #checking if there are suggestions
    if len(suggestions) != 0:
        
        #Printing the 'did you mean'
        print("\nDid you mean:")
        for unit in suggestions:
            print(" - " + unit )
    
    #if there are no suggestions found
    else:
        print("\nNo suggestions found D:")


    db.close()


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

        #if the user enters not a numebr but letters or symbols
        except ValueError:
            print("\nPlease enter a valid value\n")

    #variable that stops the while loop below from printing again and again
    didIthappen = False

    #if user types a non-existent unit as start_unit
    while not is_valid_input1:

        if didIthappen == False:
            #printing suggestions for units
            print("\nSuggestions:")
            showAllUnits(8)
            #making the variable false so suggestions don't show up again
            didIthappen = True
        
        start_unit = cool_input("\nPlease type the unit you want to convert: \n")

        #checking if unit is valid
        if is_it_valid(start_unit) == True:
            #storing unit type
            unit1_type = unit_type
            break
        else:
            print("\nPlease enter a valid unit\n")

            #checking if the user forgot how to spell a unit
            didYouMean(start_unit)
    
    didIthappen2 = False

    #if user types a non-existent unit as start_unit
    while not is_valid_input2:

        if didIthappen2 == False:
            #printing suggestions for units
            print(f"\nHere are some units you can convert {start_unit} to:\n")
            showAllUnits(unit1_type)
            #making the variable false so suggestions don't show up again
            didIthappen2 = True

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

            #checking if the user forgot how to spell a unit
            didYouMean(end_unit)
    
    #converting the input
    convert(number, start_unit, end_unit)
    
    #checking if the user wants to calculate units again
    restart = cool_input("\nPress 'r' to convert again or type anything to go back to menu: ")

    #if they wanted to restart
    if restart == "r":
        calc_units()

    #if they didn't want to restart
    else:
        menu()
    






#main
if __name__ == "__main__":

    #informs user of this program   
    print("\nGreetings! This is a Unit Converter\nWhat would you like to do today?")
    #activates the menu
    menu()


