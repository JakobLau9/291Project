import globalConnection

def newID():
    newUserID = input("Please input an ID: ")
    newName = input("Please input a name: ")
    newPassword = input("Please enter a password: ")

    insertNewUser = f'''
        INSERT INTO users(uid, name, pwd) VALUES
        ('{newUserID}', '{newName}', '{newPassword}');
        '''
    globalConnection.cursor.execute(insertNewUser)

    print("New user registration successful!!!")
    return newUserID


def checkArtistUser(ID, password):
    checkUser = f'''
        SELECT *
        FROM users
        WHERE lower(uid) = {ID.lower()} and pwd = {password.lower()};
    '''
    globalConnection.cursor.execute(checkUser)
    userExist = globalConnection.cursor.fetchall()
    if(userExist):
        return "customer"

    checkArtist = f'''
        SELECT *
        FROM artists
        WHERE lower(aid) = {ID.lower()} and pwd = {password.lower()};
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
        print("Login Successful!")
        return(check, userID)
    else:
        print("Wrong credentials! type 'retry' to try again or 'signup' to register a new account")
        input = input()
        while input != "retry" and input != "signup":
            print("Invalid command.")
            input = input()
        if input == "retry":
            return ("", "")
        elif input == "signup":
            newID = newID()
            print("Login successfully!")
            return ("user", newID)
    return
