from re import search
import globalConnection
from datetime import datetime
import selectArtist
import searchSongPlaylist

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

# For generating unique playlist ID
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
    print(newID)
    return newID

# For generating the next numbered Sorder when addings songs to a playlist
def generateSorder(playlistID):
    selectHighestPlaylistID = f'''
        SELECT max(sorder)
        FROM plinclude
        WHERE pid = {playlistID};
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
        WHERE lower(uid) = {userID.lower()}
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
            WHERE lower(uid) = {userID.lower()}
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
    
    print("Song has been added into ")
    return

# For ending a session
def endSession(sessionID, sessionStartTime, userID):
    timeEnd = datetime.today().strftime('%Y-%m-%d')
    updateSessionFinished = f'''
        UPDATE sessions
        SET end = {timeEnd}
        WHERE lower(uid) = {userID.lower()}
        AND sno = {sessionID}
    '''
    globalConnection.cursor.execute(updateSessionFinished)
    globalConnection.connection.commit()
    print("Session with ID: " + str(sessionID) + " has ended")
    return

# For displaying the song ID, title, duration and name of a song
# Also the playlist title and playlist ID where the song appears
def displaySongInformation(songID):
    selectSongInformation = f'''
        SELECT distinct s.sid, s.title, s.duration, a.name
        FROM songs s, artists a, perform p
        WHERE p.sid = s.sid and a.aid = p.aid and s.sid = {songID};
    '''
    playlistIncludeSong = f'''
        SELECT playlists.title, playlists.pid
        FROM playlists, songs, plinclude
        WHERE songs.sid = plinclude.sid and playlists.pid = plinclude.pid and songs.sid = {songID};
    '''
    informationData = globalConnection.cursor.execute(selectSongInformation)
    informationRows = informationData.fetchall()

    playlistData = globalConnection.cursor.execute(playlistIncludeSong)
    playlistRows = playlistData.fetchall()

    for i in informationRows:
        print("Song ID: " + str(i[0]))
        print("Title: " + i[1])
        print("Duration (sec): " + str(i[2]))
        print("Artist: " + i[3])
    
    print("\nPlaylists that include the song:")
    for i in playlistRows:
        print("Name: " + i[0] + " ID: " + str(i[1]))
    return

# Adds a give song to a playlist
# The playlist can either already exist or be created by the user
def addSongToPlaylist(songID, userID):
    playlistID = input("Please select the ID of the playlist you would like to add the song into: ")

    checkPlaylist = f'''
        SELECT *
        FROM playlists
        where pid = {playlistID} and lower(uid) = '{userID.lower()}';
    '''
    informationData = globalConnection.cursor.execute(checkPlaylist)
    informationRows = informationData.fetchall()

    # If a playlist exists then add the song into the playlist
    if(informationRows):
        Sorder = generateSorder(playlistID)
        insertSong = f'''
        INSERT INTO plinclude VALUES ({playlistID}, {songID}, {Sorder});
        '''
        print("Song has been added into playlist " + str(playlistID) + " with song order " + str(Sorder))
        globalConnection.cursor.execute(insertSong)
        globalConnection.connection.commit()

    # If not, then give the user the option to add it to a playlist
    else:
        userInput = input("Playlist does not exists, would you like to create a playlist? ")
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
            print("Created new playlist called " + playlistTitle + " with ID: " + str(playlistID))

    return

# Whenever a user selects a song, then it will be given to the selectSong function
def selectSong(songID, userID):
    # Checks if the song exists 
    checkSongID = f'''
        SELECT *
        FROM songs
        WHERE sid = {songID}
    '''
    songData = globalConnection.cursor.execute(checkSongID)
    songRows = songData.fetchall()
    if(len(songRows) == 0):
        print("Song does not exist")
        return

    print("You may now use the three commands: listen, information and add")
    userInput = input("Please enter your song command: ")

    # If a song is selected then the user can listen, information, or add
    if(userInput == "listen"):
        # User has staretd listening to a song and creates a session if one is not already created
        if(globalConnection.onSession == False):
            globalConnection.sessionID, globalConnection.sessionStartTime = startSession(userID)
            globalConnection.onSession = True

        updateListen(userID, globalConnection.sessionID, songID)
    elif(userInput == "information"):
        displaySongInformation(songID)
    elif(userInput == "add"):
        addSongToPlaylist(songID, userID)
    return

# Whenever a user selects a playlist, then it will be given to the selectPlaylist function
def selectPlaylist(playlistID):
    # Checks if the playlist exists and also grabs the needed parameters from the database
    selectPlaylistQuery = f'''
        SELECT playlists.pid, playlists.title, sum(songs.duration)
        FROM playlists, plinclude, songs
        WHERE playlists.pid = plinclude.pid 
        AND plinclude.sid = songs.sid
        AND playlists.pid = {playlistID};
    '''
    playlistData = globalConnection.cursor.execute(selectPlaylistQuery)
    playlistRows = playlistData.fetchall()
    if(playlistRows[0][0] != None):
        print("Playlist Name: " + playlistRows[0][1] + " ID: " + str(playlistRows[0][0]) + " Total Song Duration: " + str(playlistRows[0][2]))
    else:
        print("Playlist does not exist")
    return

# Whenever a user selects a artist, then it will be given to the selectArtist function
def selectArtists(artistID):
    # Checks if the artist exists and also grabs the needed parameters from the database
    selectArtistQuery = f'''
        SELECT songs.sid, songs.title, songs.duration
        FROM songs, artists, perform
        WHERE songs.sid = perform.sid 
        AND artists.aid = perform.aid 
        AND artists.aid = "{artistID}";
    '''
    artistData = globalConnection.cursor.execute(selectArtistQuery)
    artistRows = artistData.fetchall()
    if(artistRows[0][0] != None):
        for i in artistRows:
            print("Song Title: " + i[1] + " ID: " + str(i[0]) + " Total Song Duration: " + str(i[2]))
    else:
        print("Artist does not exist or does not have any songs")
    return

# This handles all of the possible user inputs.
def userInputHandler(userID):
    while True:
        userInput = input("Please enter your command or type 'command' for a list of commands: ").lower()

        # Quits the program
        if(userInput == "quit"):
            if(globalConnection.onSession == True):
                endSession(globalConnection.sessionID, globalConnection.sessionStartTime, userID)
            quit()
        # logout so that another user or artist can login
        elif(userInput == "logout"):
            return
        # Prints out the possible commands and what they do for a user
        elif(userInput == "command"):
            print('''
            quit: Quits the program (exits all sessions the user is in)
            logout: Logout of the program (does not exit sessions the user is in)
            start: Start a session
            end: End a sessions
            search for artists: Allows the user to input keywords to search for artists
            search for songs and playlists: Allows the user to input keywords to search for songs and playlists
            select song: Select a song to either listen, see more information, or add to playlist
            select playlist: See more information on a playlist
            select artist: See more information on an artist
            ''')
        
        # end will always check if the user is in session before attempting to end a session.
        if(userInput == "end" and globalConnection.onSession == True):
            endSession(globalConnection.sessionID, globalConnection.sessionStartTime, userID)

            # Resetting back to default
            globalConnection.sessionID = None
            globalConnection.sessionStartTime = None
            globalConnection.onSession = False
        elif (userInput == "end" and globalConnection.onSession == False):
            print("There is currently no ongoing sesssion")
        
        # Start will not start if the user is already in a session.
        if(userInput == "start" and globalConnection.onSession == False):
            globalConnection.sessionID, globalConnection.sessionStartTime = startSession(userID)
            globalConnection.onSession = True
        elif(userInput == "start" and globalConnection.onSession == True):
            print("Already in a session with ID: " + str(globalConnection.sessionID))
        
        # searching for artists, songs or playlists with keywords
        if(userInput == "search for artists"):
            selectArtist.searchArtistHandler(userID)
        elif(userInput == "search for songs and playlists"):
            searchSongPlaylist.searchSongPlaylist(userID)

        # calls the corresponding select functions
        if(userInput == "select song"):
            songID = input("Please select a song ID: ")
            selectSong(songID, userID)
        elif(userInput == "select playlist"):
            playlistID = input("Please select a playlist ID: ")
            selectPlaylist(playlistID)
        elif(userInput == "select artist"):
            artistID = input("Please select an artist ID: ")
            selectArtists(artistID)
