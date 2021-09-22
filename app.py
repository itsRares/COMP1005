#
# Student Name: Rares Popa
# Student ID  : 19159700
#
# app.py: Main menu for the program, gives a menu
#

from power_usage import *
from power_modelling import *
from power_simulation import *
from helpers import *
from community import *

#Main menu, User can select what section they would like
def menu():
    os.system('clear') #Clear the console
    print("-- Please input details before starting --\n")
    suburb = input("What Suburb are you located in? ")
    #create suburb
    street_number = input("What is your house number? ")
    #create house
    print("Finding house ...")
    house = House(street_number, suburb)
    time.sleep(1.0) # Sleep for 1 sec, to add some delay to the 'Finding'

    #Refresh the console
    os.system('clear')
    print("---=== Welcome to TESLA Power ===---")

    option=True
    while option:
        print("""
        1. Power Usage
        2. Power Modelling
        3. Power Simulation
        4. Exit/Quit
        """)
        option=input("What would you like to do? ") #Choose an option

        if option=="1":
            menuUsage(house) #Power Usage
        elif option=="2":
            menuModelling(house) #Power Modelling
        elif option=="3":
            menuSimulation(house) #Power Simulation
        elif option=="4":
            #Exit the app
            print("\n---=== Thank You & Goodbye ===---\n") 
            option = None
        else:
            os.system('clear')
            print("Invalid choice, What would you like to do? ")

if __name__ == "__main__":
    	menu()