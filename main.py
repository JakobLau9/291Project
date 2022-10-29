import sqlite3
import globalConnection
import login
import sys
import user
import artist

def main():
    loginPerson = None # Neither user or artist
    ID = None

    # if(len(sys.argv) != 2):
    #     print("Please run this code using the format: python3 main.py <path to database>")
    #     quit()

    globalConnection.connection = sqlite3.connect(sys.argv[1])
    globalConnection.cursor = globalConnection.connection.cursor()

    print("Welcome Jakob and Prabh's CMPUT 291 mini-project!!!")
    
    while True:

        while (loginPerson == None or loginPerson == ""):
            selectLogin = input("Would you like to login or quit?: ")
            if(selectLogin == "login"):
                print("Please input your login information")
                loginList = login.login()
                loginPerson = loginList[0]
                ID = loginList[1]
            elif(selectLogin == "quit"):
                quit()

        if(loginPerson == "user"):
            print("User has logged in with ID: " + ID)
            user.userInputHandler(ID)
            loginPerson = None # Neither user or artist
            ID = None
            continue
        elif(loginPerson == "artist"):
            print("Artist %s has logged in" % ID)
            artist.artistInputHandler(ID)
            loginPerson = None # Neither user or artist
            ID = None
            continue


    return

if __name__ == "__main__":
    main()
