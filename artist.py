import globalConnection
import datetime

def findTopFans(artistID):
    print("Artist %s Top Fans" % artistID)

    getTopFans = f'''
        select l.uid, p.aid, sum(l.cnt*s.duration)
        from listen l, songs s, perform p
        where l.sid=s.sid and s.sid=p.sid and lower(p.aid) = '{artistID.lower()}'
        group by l.uid
        order by sum(l.cnt*s.duration) desc
        limit 3;
    '''
    fans = globalConnection.cursor.execute(getTopFans)
    rows = fans.fetchall()
    for each in rows:
        duration = float(each[2]) # so we can fix precision
        print("{}|{:.1f}".format(each[0], duration)) # to 1 decimal point
    return

def findTopPlaylists(artistID):
    print("top playlists")
    getTopPlaylists = f'''
        select plinclude.pid, count(perform.sid)
        from plinclude, perform
        where plinclude.sid = perform.sid
        and lower(perform.aid) = '{artistID.lower()}'
        group by plinclude.pid
        order by count(perform.sid) desc
        limit 3;
    '''
    playlists = globalConnection.cursor.execute(getTopPlaylists)
    rows = playlists.fetchall()
    for each in rows:
        print("playlist {} has {} of your songs".format(each[0], each[1]))
    return


def addSong(artistID):
    title = input("Please enter a title: ")
    duration = input("Please enter a duration: ")
    checkNewSong = f'''
        select songs.sid
        from perform, songs
        where lower(perform.aid) = '{artistID.lower()}'
        and perform.sid = songs.sid
        and lower(songs.title) = '{title.lower()}'
        and songs.duration = '{duration}';
    '''
    songExists = globalConnection.cursor.execute(checkNewSong)
    songExists = songExists.fetchall()

    if (songExists):
        print("Rejected: song already exists")
    else:
        print("continue to add a song")

    
def artistInputHandler(artistID):

    while True:
        artistInput = input("Please enter your command: ")
        if(artistInput == "find top fans"):
            findTopFans(artistID)

        elif (artistInput == "find top playlists"):
            findTopPlaylists(artistID)
        elif (artistInput == "add a song"):
            addSong(artistID)

        elif (artistInput == "exit"):
            return

        else:
            print("invalid")




# def userInputHandler(userID):
#     sessionID = None
#     songID = None
#     sessionStartTime = None
#     songStartTime = None
#     onSession = False
#     onSong = False
    

#     while True:
#         userInput = input("Please enter your command: ")
#         if(userInput == "logout"):
#             return

#         if(userInput == "end" and onSession == True):
#             if(onSong == True):
#                 updateListen(userID, sessionID, songID, songStartTime)

#             endSession(sessionID, sessionStartTime, userID)

#             # Resetting back to default
#             sessionID = None
#             sessionStartTime = None
#             songStartTime = None
#             onSession = False
#             onSong = False
#             songID = None
#         else:
#             print("There is currently no ongoing sesssion")
        
#         if(userInput == "start" and onSession == False):
#             sessionID, sessionStartTime = startSession(userID)
#             onSession = True
#         else:
#             print("Already in a session with ID: " + sessionID)