import globalConnection
from datetime import datetime
import selectArtist

# For generating unique session ID
def generateSessionID():
    selectHighestSessionID = f'''
        SELECT max(sno)
        FROM sessions;
    '''
    data = globalConnection.cursor.execute(selectHighestSessionID)
    rows = data.fetchall()
    if(rows[0][0] != None):
        newID = rows[0][0] + 1
    else:
        newID = 1
    return newID

def generatePlaylistID():
    selectHighestPlaylistID = f'''
        SELECT max(pid)
        FROM playlists;
    '''
    data = globalConnection.cursor.execute(selectHighestPlaylistID)
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
def updateListen(userID, sessionID, songID):

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
        listenTime = listenTime + 1
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
            ('{userID}', {sessionID}, {songID}, 1.0);
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

def displaySongInformation(songID):
    selectSongInformation = f'''
        SELECT distinct s.sid, s.title, s.duration, a.name
        FROM songs s, artists a, perform p
        WHERE p.sid=s.sid and a.aid=p.aid and s.sid = {songID};
    '''
    playlistIncludeSong = f'''
        SELECT playlists.title
        FROM playlists, songs, plinclude
        WHERE songs.sid = plinclude.sid and playlists.pid = plinclude.pid and songs.sid = {songID};
    '''
    informationData = globalConnection.cursor.execute(selectSongInformation)
    informationRows = informationData.fetchall()

    playlistData = globalConnection.cursor.execute(playlistIncludeSong)
    playlistRows = playlistData.fetchall()

    for i in informationRows:
        print("song ID: " + str(i[0]))
        print("title: " + i[1])
        print("Duration (sec): " + str(i[2]))
        print("Artist: " + i[3])
    
    print("\nPlaylists that include the song:")
    for i in playlistRows:
        print(i[0])
    return

def addSongToPlaylist(songID, userID):
    playlistID = input("Please select the ID of the playlist you would like to add the song into: ")

    checkPlaylist = f'''
        SELECT *
        FROM playlists
        where pid = {playlistID} and uid = '{userID}';
    '''
    informationData = globalConnection.cursor.execute(checkPlaylist)
    informationRows = informationData.fetchall()

    # If a playlist exists then add the song into the playlist
    if(informationRows):

        #TODO: The sorder has to be one higher than the max in the playlist
        insertSong = f'''
        INSERT INTO plinclude VALUES ({playlistID}, {songID}, 1);
        '''

        globalConnection.cursor.execute(insertSong)
        globalConnection.connection.commit()

    # If not, then give the user the option to add it to a playlist
    else:
        userInput = input("Playlist does not exists, would you like to create this playlist? ")
        if(userInput == "n" or userInput == "no"):
            return
        elif(userInput == "y" or userInput == "yes"):
            playlistTitle = input("Please give this playlist a name: ")

            playlistID = generatePlaylistID()

            createPlaylist = f'''
                INSERT INTO playlists(pid, title, uid) VALUES 
                ({playlistID}, '{playlistTitle}', '{userID}');
            '''
            globalConnection.cursor.execute(createPlaylist)
            globalConnection.connection.commit()
            addSongToPlaylist = f'''
                INSERT INTO plinclude(pid, sid, sorder) VALUES 
                ({playlistID}, {songID}, 1);
            '''
            globalConnection.cursor.execute(addSongToPlaylist)
            globalConnection.connection.commit()
            print("Created new playlist called " + playlistTitle + " with ID: " + playlistID)

    return


def userInputHandler(userID):
    sessionID = None
    songID = None
    ArtistID = None
    PlaylistID = None

    sessionStartTime = None
    onSession = False
    onSong = False
    

    while True:
        userInput = input("Please enter your command: ")

        if(userInput == "quit"):
            if(onSession == True):
                endSession(sessionID, sessionStartTime, userID)
            quit()
        
        if(userInput == "logout"):
            return

        if(userInput == "end" and onSession == True):
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
            print("Already in a session with ID: " + str(sessionID))


        if(userInput == "select"):
            userSelect = input("Would you like to select a song, artist or playlist? ")
            if(userSelect == "song"):
                userSelectSong = input("Please input the ID of the song: ")
                songID = userSelectSong
                print("You may now use the three commands: listen, information and add")
            elif(userSelect == "artist"):
                userSelectArtist = input("Please input the ID of the artist: ")
                selectArtist.selectArtistHandler(userSelectArtist, userID)
            elif(userSelect == "playlist"):
                userSelectPlaylist = input("Please input the ID of the playlist: ")


        # If a song is selected then the user can listen, information, or add
        if(songID != None and userInput == "listen"):
            # User has staretd listening to a song and creates a session if one is not already created
            songStartTime = datetime.today()
            onSong = True
            if(onSession == False):
                sessionID, sessionStartTime = startSession(userID)
                onSession = True

            updateListen(userID, sessionID, songID)
        elif(songID != None and userInput == "information"):
            displaySongInformation(songID)
        elif(songID != None and userInput == "add"):
            addSongToPlaylist(songID, userID)

