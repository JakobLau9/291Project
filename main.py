import sqlite3
import globalConnection
import login
import sys
import user
import artist

def main():
    loginPerson = None # Neither user or artist
    ID = None

    # Checking if a database is given
    if(len(sys.argv) != 2):
        print("Please run this code using the format: python3 main.py <path to database>")
        quit()

    # These are the variables that the functions will use to do SQL queries
    globalConnection.connection = sqlite3.connect(sys.argv[1])
    globalConnection.cursor = globalConnection.connection.cursor()

    print("Welcome Jakob and Prabh's CMPUT 291 mini-project!!!")
    
    while True:
        # Checking if the input is a user or artist or both
        while (loginPerson == None or loginPerson == ""):
            selectLogin = input("Would you like to login, signup or quit?: ").lower()
            if(selectLogin == "login"):
                print("Please input your login information")
                loginList = login.login()
                loginPerson = loginList[0]
                ID = loginList[1]
            elif(selectLogin == "quit"):
                quit()
            elif(selectLogin == "signup"):
                ID = login.newID()
                loginPerson = "user"

        if(loginPerson == "user"):
            print("User has logged in with ID: " + ID)
            user.userInputHandler(ID)

            # Resesting for when the user logouts
            loginPerson = None
            ID = None
            continue
        elif(loginPerson == "artist"):
            print("Artist %s has logged in" % ID)
            artist.artistInputHandler(ID)

            # Resesting for when the artist logouts
            loginPerson = None 
            ID = None
            continue
        elif(loginPerson == "both"):
            print("Artist and User detected")
            choose = input("Would you like to login as an artist or user: ").lower()
            if(choose == "user"):
                print("User has logged in with ID: " + ID)
                user.userInputHandler(ID)
                loginPerson = None 
                ID = None
                continue
            elif(choose == "artist"):
                print("Artist %s has logged in" % ID)
                artist.artistInputHandler(ID)
                loginPerson = None 
                ID = None
                continue


    return

if __name__ == "__main__":
    main()
