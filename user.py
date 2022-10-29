import globalConnection
from datetime import datetime

# For generating unique session ID
def generateSessionID():
    selectHighestID = f'''
        SELECT max(sno)
        FROM sessions;
    '''
    data = globalConnection.cursor.execute(selectHighestID)
    rows = data.fetchall()
    if(rows[0][0] != None):
        newID = rows[0][0] + 1
    else:
        newID = 1
    return newID


# Adds the session into the table and returns the ID and start time
def startSession(userID):
    sessionID = generateSessionID()
    timeNow = datetime.today().strftime('%Y-%m-%d')
    startSession = f'''
        INSERT INTO sessions(uid, sno, start, end) VALUES
        ('{userID}', '{sessionID}', '{timeNow}', NULL);
    '''
    globalConnection.cursor.execute(startSession)
    globalConnection.connection.commit()
    print("Started session with ID: " + str(sessionID))
    return(sessionID, timeNow)


# If a user was listening to a song, then it will update the listen table with the count of how long the user was listening
def updateListen(userID, sessionID, songID, songStartTime):
    # TODO: FIX DATETIME FOR HERE, use .today() for songs, and datetime.today().strftime('%Y-%m-%d') for sessions
    # timeTotal is the total time listened to this one song CURRENTLY.
    timeEnd = datetime.today()
    timeTotal = timeEnd - songStartTime

    # Getting the duration of the songs and comparing it to the time total listened to see if the entire song was listened to or not
    getSongDuration = f'''
        SELECT duration
        FROM songs
        WHERE sid = {songID};
    '''
    data = globalConnection.cursor.execute(getSongDuration)
    rows = data.fetchall()
    songDuration = rows[0][0]

    # listenCount holds the total duration of the song listened
    # If the song was listened to longer than the duration, then it will return the duration
    # otherwise, it will return the ratio between the total time listened/song duration
    listenCount = 0
    if(timeTotal.total_seconds() >= songDuration):
        listenCount = songDuration
    else:
        listenCount = timeTotal.total_seconds()/songDuration

    # Now have to check if the user has listened to this song before
    getListenData = f'''
        SELECT cnt
        FROM listen
        WHERE uid = {userID}
        AND sno = {sessionID}
        AND sid = {songID};
    '''
    listenData = globalConnection.cursor.execute(getListenData)
    listenRows = listenData.fetchall()

    # If the user has listened to the song before then update the entry
    if listenRows:
        listenTime = listenRows[0][0]
        listenTime = listenTime + listenCount
        updateListenDuration = f'''
            UPDATE listen
            SET cnt = {listenTime}
            WHERE uid = {userID}
            AND sno = {sessionID}
            AND sid = {songID};
        '''
        globalConnection.cursor.execute(updateListenDuration)
        globalConnection.connection.commit()

    # Else, insert the entry into listen
    else:
        enterListenDuration = f'''
            INSERT INTO listen VALUES
            ('{userID}', '{sessionID}', '{songID}', '{listenCount}');
        '''
        globalConnection.cursor.execute(enterListenDuration)
        globalConnection.connection.commit()
    return

def endSession(sessionID, sessionStartTime, userID):
    timeEnd = datetime.today().strftime('%Y-%m-%d')
    updateSessionFinished = f'''
        UPDATE sessions
        SET end = {timeEnd}
        WHERE uid = {userID}
        AND sno = {sessionID}
    '''
    globalConnection.cursor.execute(updateSessionFinished)
    globalConnection.connection.commit()
    print("Session with ID: " + str(sessionID) + " has ended")
    return


def userInputHandler(userID):
    sessionID = None
    songID = None
    sessionStartTime = None
    songStartTime = None
    onSession = False
    onSong = False
    

    while True:
        userInput = input("Please enter your command: ")
        if(userInput == "logout"):
            return

        if(userInput == "end" and onSession == True):
            if(onSong == True):
                updateListen(userID, sessionID, songID, songStartTime)

            endSession(sessionID, sessionStartTime, userID)

            # Resetting back to default
            sessionID = None
            sessionStartTime = None
            songStartTime = None
            onSession = False
            onSong = False
            songID = None
        elif (userInput == "end" and onSession == False):
            print("There is currently no ongoing sesssion")
        
        if(userInput == "start" and onSession == False):
            sessionID, sessionStartTime = startSession(userID)
            onSession = True
        elif(userInput == "start" and onSession == True):
            print("Already in a session with ID: " + sessionID)

