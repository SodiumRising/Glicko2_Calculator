from asyncio.windows_events import NULL
import challonge
import asyncio
from ChallongeUser import *
from DB_Functions import get_tournaments, insert_tournament
import sqlite3

#Reference: https://achallonge.readthedocs.io/en/latest/api.html#user

myUsername = ""
myAPIKey = ""

async def challongeLoop(loop, endURL):
    
    #List of all data needed for glicko2.py
    userData = []

    #get info for specific tournament using my username and key
    my_user = await challonge.get_user(myUsername, myAPIKey)
    my_tournament = await my_user.get_tournament(endURL)

    #list of participants in the tournament
    participants = []

    #Get each of the participants
    participants = await my_tournament.get_participants()

    #Get information for each participant and store in a ChallongeUser object inside the userData list
    for player in participants:

        #ID of current participant
        pUsername = player.display_name

        #lists for opponent ID, and outcome of a match [0 = loss, 1 = win]
        opponents = []
        outcomes = []

        #match information of current participant
        matches = await player.get_matches()

        #Each match in the tournament
        for match in matches:

            #Ternary opperators to populate opponent and outcome lists
            opponents.append(getUsername(match.player2_id,participants) if pUsername == getUsername(match.player1_id,participants) else getUsername(match.player1_id,participants))
            outcomes.append(1 if pUsername == getUsername(match.winner_id,participants) else 0)

        #assign all collected data from the user to ChallongeUser object
        user = ChallongeUser(player.display_name, opponents, [], outcomes)

        #append user object to list of users
        userData.append(user)

        print(user.display_name, user.opponents, user.outcomes)

    return userData


def getUsername(id, participants):

    for p in participants:

        if id == p.id:

            return p.display_name


def checkEndURL():

    challongeLink = input("Please copy and paste your Challonge URL from the 'Bracket' tab, or enter '0' to cancel.\nExample: https://challonge.com/g6kmqn5b\n")

    if(challongeLink.rfind("https://challonge.com/") != -1):

        lastBackslash = challongeLink.rfind("/")
        lastBackslash = lastBackslash + 1
        endURL = challongeLink[lastBackslash:]
        
        if (endURL == ("announcements") or endURL == ("standings") or endURL == ("log") or endURL == ("stations") or endURL == ("participants") or endURL == ("form_fields") or endURL == ("participant_responses") or endURL == ("form_fields") or endURL == ("settings")):

            print("Incorrect URL. Make sure to be on the 'Bracket' tab")

        else:

            flag = checkIfTournamentExists(endURL)

            if flag == True:
                
                print("This tournament has already been used.")

            else:

                #Connect to DB
                conn = sqlite3.connect('player_list.db')
                #Cursor to run SQL commands using execute method
                c = conn.cursor()
                insert_tournament(conn,c,endURL)
                conn.close()
                
                return endURL 
                
    elif challongeLink == "0":

        exit()

    else:
        
        print("Incorrect URL. Make sure to be on the 'Bracket' tab")


def checkIfTournamentExists(endURL):

    #Connect to DB
    conn = sqlite3.connect('player_list.db')
    #Cursor to run SQL commands using execute method
    c = conn.cursor()

    tournament = get_tournaments(conn, c, endURL)
    conn.close()

    if tournament == None:

        return False

    else: 

        return True


def get_challonge_data():
    #endURL = "pymwsvnf" #dbz
    #endURL = "g6kmqn5b" #BBCF
    #endURL = "3mulu0r4" #strive

    #Input Challonge URL and check formatting
    endURL = checkEndURL()

    while (endURL == None):

        endURL = checkEndURL()

    loop = asyncio.get_event_loop()
    userData = loop.run_until_complete(challongeLoop(loop, endURL))

    return userData