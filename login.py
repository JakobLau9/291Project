import globalConnection

# Checks if the ID given is already taken
def checkUniqueID(userID):
    idCheck = f'''
        SELECT *
        FROM users
        WHERE uid = '{userID}'
    '''
    data = globalConnection.cursor.execute(idCheck)
    rows = data.fetchall()
    if(rows):
        return False
    return True

# Created a new account for the user and returns the new ID
def newID():
    newUserID = input("Please input an ID: ")
    while (checkUniqueID(newUserID) == False):
        newUserID = input("ID already taken, please try again: ")
    newName = input("Please input a name: ")
    newPassword = input("Please enter a password: ")

    insertNewUser = f'''
        INSERT INTO users(uid, name, pwd) VALUES
        ('{newUserID}', '{newName}', '{newPassword}');
        '''
    globalConnection.cursor.execute(insertNewUser)
    globalConnection.connection.commit()
    print("New user registration successful!!!")
    return newUserID


# Checks if the ID and password given is a user, artist, both or neither
def checkArtistUser(ID, password):
    user = False    
    artist = False
    checkUser = f'''
        SELECT *
        FROM users
        WHERE lower(uid) = '{ID.lower()}' AND pwd = '{password}';
    '''

    globalConnection.cursor.execute(checkUser)
    userExist = globalConnection.cursor.fetchall()
    if(userExist):
        user = True

    checkArtist = f'''
        SELECT *
        FROM artists
        WHERE lower(aid) = '{ID.lower()}' AND pwd = '{password}';
    '''
    globalConnection.cursor.execute(checkArtist)
    artistExist = globalConnection.cursor.fetchall()
    if(artistExist):
        artist = True

    
    if(user == False and artist == False):
        return ""
    elif(user == True and artist == False):
        return "user"
    elif(user == False and artist == True):
        return "artist"
    elif(user == True and artist == True):
        return "both"
    
    return ""



def login():

    userID = input("ID: ")
    password = input("password: ")
    check = checkArtistUser(userID, password)

    if(check == "user" or check == "artist" or check == "both"):
        return(check, userID)
    else:
        print("Wrong credentials! type 'retry' to try again or 'signup' to register a new account")
        input1 = input()
        while input1 != "retry" and input1 != "signup":
            print("Invalid command.")
            input1 = input("Please try again: ")
        if input1 == "retry":
            return ("", "")
        elif input1 == "signup":
            newUserID = newID()
            return ("user", newUserID)
    return
