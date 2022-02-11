import sqlite3
from glicko2 import Player

#:memory: is used for an in memory database
#connect method will create the file if it does not exist, or opens it up if it does exist
#conn = sqlite3.connect('player_list.db')

#Cursor to run SQL commands using execute method
#c = conn.cursor()

#Creates a new DB Table
def create_players_table(conn, c):

    c.execute("""CREATE TABLE players (
                Username text,
                Rating real,
                RD real,
                Vol real
                )""")


def create_tournaments_table(conn, c):

    c.execute("""CREATE TABLE tournaments (
            URL text
            )""")

#Insert a new player
def insert_player(conn, c, p1):

    with conn:
        c.execute("INSERT INTO players VALUES (:username, :rating, :rd, :vol)", {'username':p1.username, 'rating':p1.rating, 'rd':p1.rd, 'vol':p1.vol})


#Insert a new tournament
def insert_tournament(conn, c, endURL):

    with conn:
        c.execute("INSERT INTO tournaments VALUES (:endURL)", {'endURL': endURL})


#Find tournaments by endURL
def get_tournaments(conn, c, endURL):

    c.execute("SELECT * FROM tournaments WHERE URL = :endURL", {'endURL': endURL})
    return c.fetchone()


#Find players by Username
def get_player_by_name(conn, c, username):

    c.execute("SELECT * FROM players WHERE Username = :username", {'username': username})
    return c.fetchone()


#Returns all players in the DB
def get_all_players(conn, c):

    c.execute("SELECT * FROM players ORDER BY Rating DESC")
    return c.fetchall()


#Update new ratings for given player
def update_player(conn, c, p1):

    with conn:
        #Set Rating
        c.execute("""UPDATE players SET Rating = :rating
                        WHERE Username = :username""",
                        {'username': p1.username, 'rating':p1.rating})

        #Set RD
        c.execute("""UPDATE players SET RD = :rd
                        WHERE Username = :username""",
                        {'username': p1.username, 'rd':p1.rd})

        #Set Vol
        c.execute("""UPDATE players SET Vol = :vol
                        WHERE Username = :username""",
                        {'username': p1.username, 'vol':p1.vol})


#Remove an existing player
def remove_player(conn, c, p1):

    with conn:
        c.execute("DELETE FROM players WHERE Username = :username", {'username':p1.username})


#Video Tutorial: https://www.youtube.com/watch?v=pd-0G0MigUA