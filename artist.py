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

def getCollabArtists(artistID, title, duration):
    getCollab = f'''
        select perform.aid
        from perform, songs
        where perform.sid = songs.sid
        and lower(songs.title) = '{title.lower()}'
        and songs.duration = '{duration}'
        and lower(perform.aid) != '{artistID.lower()}';
    '''
    collab = globalConnection.cursor.execute(getCollab)
    rows = collab.fetchall()

    collabList = []
    for each in rows:
        collabList.append(each[0])
    return collabList

def generateSongID():
    selectHighestID = f'''
        SELECT max(sid)
        FROM songs;
    '''
    data = globalConnection.cursor.execute(selectHighestID)
    rows = data.fetchall()
    newID = rows[0][0] + 1
    return newID


def soloAdd(artistID, sid, title, duration):
    insertPerform = f'''
        INSERT INTO perform(aid, sid) VALUES
        ('{artistID}', '{sid}');
    '''

    insertSong = f'''
        INSERT INTO songs(sid, title, duration) VALUES
        ('{sid}', '{title}', {duration});
    '''
    globalConnection.cursor.execute(insertPerform)
    globalConnection.cursor.execute(insertSong)
    globalConnection.connection.commit()

def collabAdd(artistID, sid, title, duration, collabList):
    # add potentional collaborators
    for each in collabList:
        collabID = each
        insertCollab = f'''
            INSERT INTO perform(aid, sid) VALUES
            ('{collabID}', '{sid}');
        '''
    # also add the artist and create song
    soloAdd(artistID, sid, title, duration)
    globalConnection.cursor.execute(insertCollab)
    globalConnection.connection.commit()



def addSong(artistID):
    title = input("Please enter a title: ")
    duration = input("Please enter a duration in seconds: ")
    checkNewSong = f'''
        select songs.sid
        from perform, songs
        where perform.sid = songs.sid
        and lower(perform.aid) = '{artistID.lower()}'
        and lower(songs.title) = '{title.lower()}'
        and songs.duration = '{duration}';
    '''
    songExists = globalConnection.cursor.execute(checkNewSong)
    songExists = songExists.fetchall()

    if (songExists):
        print("Rejected: song already exists")
    else:
        # add a new song
        # first generate new sid and get collablist
        sid = generateSongID()
        collabList = getCollabArtists(artistID, title, duration)

        if (len(collabList) == 0): # no other collaborators, simply insert
            soloAdd(artistID, sid, title, duration)
            print("added song %s as new solo" % sid)
        
        else:
            collabAdd(artistID, sid, title, duration, collabList)
            print("added collab song %s" %sid)
        
    
def artistInputHandler(artistID):
    commands = '''
        find top fans
        find top playlists
        add song
        exit
    '''
    
    while True:
        artistInput = input("Please enter your command: ").lower()
        if(artistInput == "find top fans"):
            findTopFans(artistID)

        elif (artistInput == "find top playlists"):
            findTopPlaylists(artistID)
        elif (artistInput == "add song"):
            addSong(artistID)

        elif (artistInput == "logout"):
            return

        elif (artistInput == "quit"):
            quit()

        elif(artistInput == "command"):
            print(commands)
        
        else:
            print("invalid")
