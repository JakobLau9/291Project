import globalConnection
import user


# select distinct artists.aid
# from artists, perform, songs
# where perform.sid = songs.sid
# and perform.aid = artists.aid
# and ((artists.name LIKE '%y%') or (songs.title LIKE '%y'));

def selectArtists(artistID):
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

def displayFive(rows):
    i = 0
    for each in rows:
        print("{} | {}".format(each[0], each[1]))
        i+=1
        if(i == 5):
            break

def displayAll(rows):
    for each in rows:
        print("{} | {}".format(each[0], each[1]))

def display(rows):
    if len(rows) > 5:
        print("only showing 5")
        displayFive(rows)
        more = input("Type 'all' to see more: ")
        if (more == "all"):
            displayAll(rows)

    else:
        displayAll(rows)

def searchArtistHandler(userID):
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
    display(rows)
    globalConnection.cursor.execute("PRAGMA case_sensitive_like=OFF;")
    globalConnection.connection.commit()


    selection = input("you may select an artist: ")
    selectArtists(selection)
