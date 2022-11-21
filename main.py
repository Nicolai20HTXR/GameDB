import os
import random
import sqlite3 as sql

#Various variables
amountOfTries = 0
secretNumber = random.randrange(0, 100)
guess = None
nameInDB = False

#Setting up connection with DB
db = sql.connect("myDB.db")
c = db.cursor()

#Asking for input from user
#Checks if name already in DB
name = input("Indtast navn:\n").lower()
allNames = c.execute("""SELECT Name FROM `Users`""").fetchall()
for s in allNames:
    if(name == s[0].lower()):
        nameInDB = True

#clears system log
os.system("cls")

#Prompt user welcome and add to DB if already in DB then welcomeback
if nameInDB:
    print("Welcome Back!")
else:
    print("Welcome new user!")
    c.execute(f"""INSERT INTO Users(Name) VALUES ('{name}')""")
    db.commit()

#Stores userID variable from name
userID = c.execute(f"""SELECT userID FROM Users WHERE Name='{name}'""").fetchone()[0]

#Debugging userID
#print("Player userID: " + str(userID))

#Add new game in DB and when it started
addGameS = f"""INSERT INTO Games(UserID, event, data) VALUES ('{userID}', 'Game started', CURRENT_TIMESTAMP)"""
c.execute(addGameS)
db.commit()

#Get current game ID from just created record/row
curGameID = c.execute(f"""SELECT gameID FROM Games ORDER BY gameID DESC""").fetchone()[0]

#Debugging Current GameID
#print("Current Game ID: " + str(curGameID))

#Takes input and check if it is a number and within 0 to 100, then returns
def getGuess():
    
    guess = input("Guess number between 0 - 100:\n")
    if guess.isnumeric():
        guess = int(guess)
    else:
        os.system("cls")
        print("Indtast et tal!")
        getGuess()
    
    if (guess < 0 or guess > 100):
        os.system("cls")
        print("Dit gæt er ikke inden for 0 - 100")
        getGuess()
    else:
        return guess

#While number have not been guessed, game is on.
while (guess != secretNumber):
    guess = getGuess()

    #Old variable for counting attemps used
    #amountOfTries += 1

    #Prompt user depending of number compared to the secret number.
    #Also saves the the guess within the Current Game ID under Rounds table
    if (guess < secretNumber):
        print("Nummer er større end dit gæt")
        c.execute(f"""INSERT INTO Rounds(gameID, event, data) VALUES ('{curGameID}', 'Nummer er større end dit gæt', '{guess}')""")
        db.commit()
    elif (guess > secretNumber):
        print("Nummer er mindre end dit gæt")
        c.execute(f"""INSERT INTO Rounds(gameID, event, data) VALUES ('{curGameID}','Nummer er mindre end dit gæt', '{guess}')""")
        db.commit()

#If secret number been guessed prompt user
print("Du gættede det hemmelig nummer :) " + str(secretNumber))

#Add the last guess to DB as correct answer
c.execute(f"""INSERT INTO Rounds(gameID, event, data) VALUES ('{curGameID}','Nummer er gættede', '{guess}')""")
db.commit()

#End game in DB with timestamp of end
updateGameDB = f"""UPDATE Games SET event = 'Game ended', extraData = CURRENT_TIMESTAMP WHERE gameID = {curGameID} AND userID = {userID}"""
c.execute(updateGameDB)
db.commit()
db.close()