import globalConnection
import user

# approach for keyword selection:
# select distinct artists.aid
# from artists, perform, songs
# where perform.sid = songs.sid
# and perform.aid = artists.aid
# and ((artists.name LIKE '%y%') or (songs.title LIKE '%y'));

def selectArtists(artistID, userID):
    # display artist's songs
    # and then allow for song selection
    selectArtistQuery = f'''
        SELECT songs.sid, songs.title, songs.duration
        FROM songs, artists, perform
        WHERE songs.sid = perform.sid 
        AND artists.aid = perform.aid 
        AND artists.aid = "{artistID}";
    '''
    artistData = globalConnection.cursor.execute(selectArtistQuery)
    artistRows = artistData.fetchall()

    if (len(artistRows) != 0): # if artist has songs display them
        print("{}'s songs".format(artistID))
        for each in artistRows:
            print("{} | {} | {}".format(each[0], each[1], each[2]))
        song = input("Select a song id: ")
        if (len(song)==0):
            return
        user.selectSong(song, userID)
    else: 
        print("Artist does not exist or does not have any songs")
    return

def displayFive(rows):
    # only display top 5 artist for keyword match selection
    i = 0
    for each in rows:
        artistID = each[0]
        match = each[1]
        query = f'''
        select {match}, artists.aid, artists.name, artists.nationality, count(songs.sid)
        from perform, songs, artists
        where perform.sid = songs.sid
        and perform.aid = artists.aid
        and artists.aid = '{artistID}';
        '''
        # for each aid run the query
        # print the data
        artistData = globalConnection.cursor.execute(query)
        artistRow = artistData.fetchone()
        print(artistRow)
        i+=1
        if (i==5):
            break

def displayAll(rows):
    # row contains aid and count
    # for each element in row
    # run a query to also obtain the aid's other information
    # including nationality, name, # of songs
    # then display that information
    for each in rows:
        artistID = each[0]
        match = each[1]
        query = f'''
        select {match}, artists.aid, artists.name, artists.nationality, count(songs.sid)
        from perform, songs, artists
        where perform.sid = songs.sid
        and perform.aid = artists.aid
        and artists.aid = '{artistID}';
        '''
        # for each aid run the query
        # print the data
        artistData = globalConnection.cursor.execute(query)
        artistRow = artistData.fetchone()
        print(artistRow)
    

def display(rows):
    # if we have more than 5 matches only show 5
    # allow them to type all to see all matches
    # otherwise display all matches
    if len(rows) > 5:
        print("only showing 5")
        displayFive(rows)
        more = input("Type 'all' to see more: ")
        if (more == "all"):
            displayAll(rows)
    else:
        displayAll(rows)

def searchArtistHandler(userID):
    # generate sql query
    # get distinct aid where the keyword is a hit
    # union and keep duplicates with next keyword and so forth
    globalConnection.cursor.execute("PRAGMA case_sensitive_like=OFF;")
    globalConnection.connection.commit()
    print("Please enter one or more unique keywords (space-separated)")
    words = list(map(str, input().split()))
    unions = ""
    first = True
    for word in words:
        if first:
            first = False
            unions += f'''
                select distinct artists.aid
                from artists, perform, songs
                where perform.sid = songs.sid
                and perform.aid = artists.aid
                and ((artists.name LIKE '%{word}%') or (songs.title LIKE '%{word}%'))
            '''
        else:
            unions += 'union all'
            unions += f'''
                select distinct artists.aid
                from artists, perform, songs
                where perform.sid = songs.sid
                and perform.aid = artists.aid
                and ((artists.name LIKE '{word}') or (songs.title LIKE '%{word}%'))
            '''
    query = "select aid, count(*) as q from("
    query += unions
    query += ") t "
    query += "group by aid order by count(*) desc;"
    data = globalConnection.cursor.execute(query)
    rows = data.fetchall()
    # now we have the distinct aid and the count which is # of hits
    display(rows) # handles displaying and display all functionality
    # remember to turn off case sensitive like because that is the default
    globalConnection.cursor.execute("PRAGMA case_sensitive_like=OFF;")
    globalConnection.connection.commit()

    # after artists are displayed
    # allow aid selection
    selection = input("you may select an artist by id: ")
    selectArtists(selection, userID)
