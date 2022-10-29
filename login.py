import globalConnection

def checkUniqueID(userID):
    idCheck = f'''
        SELECT *
        FROM users
        WHERE uid = {userID}
    '''
    data = globalConnection.cursor.execute(idCheck)
    rows = data.fetchall()
    if(rows):
        return False
    return True

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


def checkArtistUser(ID, password):
    checkUser = f'''
        SELECT *
        FROM users
        WHERE lower(uid) = '{ID.lower()}' AND pwd = '{password.lower()}';
    '''



    globalConnection.cursor.execute(checkUser)
    userExist = globalConnection.cursor.fetchall()
    if(userExist):
        return "user"

    checkArtist = f'''
        SELECT *
        FROM artists
        WHERE lower(aid) = '{ID.lower()}' AND pwd = '{password.lower()}';
    '''
    globalConnection.cursor.execute(checkArtist)
    artistExist = globalConnection.cursor.fetchall()
    if(artistExist):
        return "artist"

    return ""



def login():

    userID = input("ID: ")
    password = input("password: ")
    check = checkArtistUser(userID, password)

    if(check == "user" or check == "artist"):
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
