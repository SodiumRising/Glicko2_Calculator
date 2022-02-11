from DB_Functions import *
from Calculation import Calculation

def main_menu():

    display_menu()
    userInput = input("What would you like to do? \n")

    if (userInput == '1'):

        show_all()
        main_menu()
    
    elif (userInput == '2'):

        run_calculation()
        main_menu()

    elif (userInput == '0'):

        exit()

    else:

        print("Invalid Choice.")
        main_menu()


def display_menu():
    print("""
***************************************
 Glicko2 Calculator       Version: 3.0
***************************************

* 1) Show All     *
* 2) Update DB    *
* 0) Exit         *

***************************************
Created by:  SodiumRising (@Sodium_FGC)
***************************************
    """)


def run_calculation():

    #Connect to player_list DB
    conn = sqlite3.connect('player_list.db')
    #Cursor to run SQL commands using execute method
    c = conn.cursor()

    try:

        create_players_table(conn, c)
        create_tournaments_table(conn, c)
        Calculation()

    except:
        
        Calculation()

    conn.close()


def show_all():
        
    conn = sqlite3.connect('player_list.db')
    #Cursor to run SQL commands using execute method
    c = conn.cursor()
    allPlayers = get_all_players(conn, c)
    counter = 1

    print("\n{0:<10}{1:^20}{2:^20}\n".format("Rank", "Username", "Rating"))

    for x in allPlayers:

        print("{0:<10}{1:<20}{2:^20}".format(counter, x[0], round(x[1])))
        counter += 1

    conn.close()


if __name__ == "__main__":
   main_menu()