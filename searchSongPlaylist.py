import globalConnection
import numpy as np
import user

# Counts the amount of keywords in a given dataset
def countMatching(keywords, data):
    # considered is so there are no duplicates
    considered = {}
    keywordsList = keywords.split()

    if ',' in data:
        data = data.replace(",", " ")

    dataList = data.split()
    counter = 0
    for word in dataList:
        if word.upper() in considered:
            continue
        for keyword in keywordsList:
            if keyword.upper() in word.upper():
                considered[word.upper()] = 1
                counter += 1
    return counter

def searchSongPlaylist(userID):
    print("Please enter one or more unique keywords to search for in Songs and Playlists sperated by a space:")
    keywords = input()
    globalConnection.connection.create_function('countMatching', 2, countMatching)

    selectSongQuery = f'''
        SELECT countMatching('{keywords}', title) as matches, "song" , sid, title, duration
        FROM songs
        WHERE matches > 0;
    '''
    songData = globalConnection.cursor.execute(selectSongQuery)
    songRows = songData.fetchall()

    selectPlaylistQuery = f'''
        SELECT countMatching('{keywords}', playlists.title) as matches, "playlist", playlists.pid, playlists.title, sum(songs.duration)
        FROM playlists, plinclude, songs
        WHERE playlists.pid = plinclude.pid 
        AND plinclude.sid = songs.sid
        AND matches > 0
        group by playlists.pid, playlists.title;
    '''
    playlistData = globalConnection.cursor.execute(selectPlaylistQuery)
    playlistRows = playlistData.fetchall()

    if(len(playlistRows) > 0 and len(songRows) > 0):
        arr = np.concatenate((playlistRows, songRows))

    elif(len(playlistRows) > 0 and len(songRows) == 0):
        arr = playlistRows

    elif(len(playlistRows) == 0 and len(songRows) > 0):
        arr = songRows
    else:
        print("No results were found")
        return
    
    #https://stackoverflow.com/questions/20099669/sort-multidimensional-array-based-on-2nd-element-of-the-subarray
    # For sorting a 2d array
    arr = sorted(arr, key=lambda x: x[0], reverse=True)

    count = 0
    for i in arr:
        if(count == 5):
            break
        if(i[1] == "playlist"):
            print("Playlist Name: " + i[3] + " ID: " + str(i[2]) + " Total Song Duration: " + str(i[4]))
        else:
            print("Song Name: " + i[3] + " ID: " + str(i[2]) + " Song Duration: " + str(i[4]))
        count = count + 1
    
    print("You can now: see more, select song, select playlist or exit")
    userInput = input("Please enter your command after searching: ")

    if(userInput == "exit"):
        return
    elif(userInput == "select song"):
        songID = input("Please select a song ID: ")
        user.selectSong(songID, userID)
        return
    elif(userInput == "see more"):
        if(len(arr) <= 5):
            print("There are no more results to see")
        else:
            for i in arr[5:]:
                if(i[1] == "playlist"):
                    print("Playlist Name: " + i[3] + " ID: " + str(i[2]) + " Total Song Duration: " + str(i[4]))
                else:
                    print("Song Name: " + i[3] + " ID: " + str(i[2]) + " Song Duration: " + str(i[4]))
    elif(userInput == "select playlist"):
        playlistID = input("Please select a playlist ID: ")
        user.selectPlaylist(playlistID)
        return

    return
