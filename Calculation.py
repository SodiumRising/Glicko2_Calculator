from GetChallongeData import get_challonge_data
from DB_Functions import *
from glicko2 import Player

def Calculation():

    userData = get_challonge_data()
    playerList = prepare_player_list(userData)
    set_ratings_and_rds(userData, playerList)
    runTheMath(userData, playerList)
    update_db(playerList)

def prepare_player_list(userData):

    #List to store Player objects
    playerList = []

    #Connect to DB
    conn = sqlite3.connect('player_list.db')
    #Cursor to run SQL commands using execute method
    c = conn.cursor()

    for x in userData:

        #Get current Player's data
        currentPlayer = get_player_by_name(conn, c, x.display_name)

        #If None is returned, then player is new
        if (currentPlayer == None):

            p = Player(x.display_name)
            insert_player(conn, c, p)
            playerList.append(p)

        #Player is Found
        else:
            
            playerList.append(Player(currentPlayer[0], currentPlayer[1], currentPlayer[2], currentPlayer[3]))

    #Close DB 
    conn.close()

    #Return all the gathered data
    return playerList


def set_ratings_and_rds(userData, playerList):

    #Look through each of the ChallongeUsers
    for x in userData:
        
        opponentRatings = []
        opponentRDs = []
        opponents = x.opponents

        #Iterate through each ChallongeUsers' opponents
        for y in opponents:

            #Find matching IDs in both ChallongeUser(userData) and Player(pList)
            for z in playerList:

                #If they match, add their Rating and RD to the list
                if y == z.username:

                    opponentRatings.append(z.rating)
                    opponentRDs.append(z.rd)
             
        #Set completed list to the ChallongeUser(userData)               
        x.setOpponents(opponentRatings)
        x.setRDs(opponentRDs)


def runTheMath(userData, playerList):

    #Iterate through each ChallongeUser
    for x in userData:

        #Iterate through each Player
        for y in playerList:
            
            #If they have matching IDs
            if (x.display_name == y.username):

                #Take the ratings and RDs from the ChallongeUser object and input it into the Player object. RUN THAT MATH
                y.update_player(x.opponents, x.rds, x.outcomes)
                print("Player: ",y.username, "| New Rating: ",y.rating, "| New RD: ",y.rd, "| New Vol: ",y.vol)


def update_db(playerList):

    #Connect to DB
    conn = sqlite3.connect('player_list.db')
    #Cursor to run SQL commands using execute method
    c = conn.cursor()

    for x in playerList:

        update_player(conn, c, x)
    
    conn.close()


if __name__ == "__main__":
    Calculation()