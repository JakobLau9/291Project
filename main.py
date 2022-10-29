import sqlite3
import globalConnection
import login
import sys
import user

def main():
    loginPerson = None # Neither user or artist
    ID = None

    if(len(sys.argv) != 2):
        print("Please run this code using the format: python3 main.py <path to database>")
        quit()

    globalConnection.connection = sqlite3.connect(sys.argv[1])
    globalConnection.cursor = globalConnection.connection.cursor()

    print("Welcome Jakob and Prabh's CMPUT 291 mini-project!!!")
    print("Please input your login information")
    while True:

        while (loginPerson == None or loginPerson == ""):
            loginList = login.login()
            loginPerson = loginList[0]
            ID = loginList[1]

        if(loginPerson == "user"):
            print("User has logged in")
            user.userInputHandler(ID)
            continue
        elif(loginPerson == "artist"):
            print("Artist has logged in")
            continue


    return

if __name__ == "__main__":
    main()
