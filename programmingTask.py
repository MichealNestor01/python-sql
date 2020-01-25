#SQL task
#This is my first program using sql
#It was homework set by my teacher who gave us the database and said:
#Create a menu system which will allow options for the user to:
#	Run a script which will prompt the user to enter data for a new film record, the record is save to the database and a confirmation is given	
#	Run a script which will allow the user to search for a record on either "Title" or "Studio" and print results in a user friendly way.
#   Run a script which allow the user to delete a specific record
#Modify the script in b) above to check is a record exists before adding it in

#Imports:
import sqlite3

#Subroutine to print a gap, used to make the output look nicer
def gap():
    print('')

#subroutine to record a new record to the database
def recordRecord():
    #setting up teh database connection:
    databaseFile = 'MoviesdB.db'
    databaseConnection = sqlite3.connect(databaseFile)
    cursor = databaseConnection.cursor()
    print('You have selected the "record a new film record" function!')
    cursor.execute('SELECT Title FROM tblFilm')
    fetchedTitles = cursor.fetchall()
    databaseConnection.commit()
    #loop to check that the movie is not already in the database:
    while True:
        newMovie = input('What is the title of the movie you want to record: ')
        escape = False 
        duplicate = False
        for i in fetchedTitles:
            if i[0] == newMovie:
                duplicate = True
                print('Sorry that movie is already in the database')
                escape = input('Would you like to add another movie? (y/n): ')
                if escape != 'y':
                    break
                else: 
                    escape = True
                    break
        if duplicate != True:
            break
    #the following statement makes sure you don't want to return to the main menu and the makes you input all the data for the fields
    if escape == False:
        studio = input(f'What studio released {newMovie}?: ')        
        releaseDate = input(f'What was the date {newMovie} was released? (yyyy-mm-dd): ')
        productionCost = int(input(f'What was the total production cost of {newMovie}? (in $millions): '))
        boxOffice = int(input(f'How much did {newMovie} make at the box office? (in $millions): '))
        seen = input(f'Have you seen {newMovie}? (y/n): ')
        if seen == 'y':
            seen = 1
        else: 
            seen = 0
        classification = input(f'What was the classification for {newMovie}? (U/12/15/18): ')
        cursor.execute(('INSERT INTO tblFilm (Title, Studio, ReleaseDate, ProductionCost, BoxOffice, Seen, Classification) VALUES(?, ?, ?, ?, ?, ?, ?)'), (newMovie, studio, releaseDate, productionCost, boxOffice, seen, classification))
        print(f'Success! {newMovie} has been added to the database!')
        databaseConnection.commit()
    #closing the database connection:
    cursor.close()
    databaseConnection.close()

#subroutine to delete a specific record
def deleteRecord():
    #setting up teh database connection:
    databaseFile = 'MoviesdB.db'
    databaseConnection = sqlite3.connect(databaseFile)
    cursor = databaseConnection.cursor()
    print('You have selected the "delete a record" function!')
    cursor.execute('SELECT Title FROM tblFilm')
    fetchedTitles = cursor.fetchall()
    databaseConnection.commit() 
    #loop to make sure that the movie you are trying to delete actually exists in the database
    while True:
        escape = False 
        found = False
        movie = input('What is the title of the movie you want to delete: ')
        for i in fetchedTitles:
            if i[0] == movie:
                found = True
        if found == False:
            print(f'Sorry there is no movie with the name {movie} in the database!')
            again = input('Would you like to try again? (y/n): ')
            if again != 'y':
                escape = True
                break
        else:
            break
    #only runs if you have successfully selected a movie to delete:
    if escape == False:
        #gives the user a chance to not delete the movie you have selected:
        abort = input(f'You have selected {movie}, are you sure you want to delete {movie}? (y/n): ')
        if abort == 'y':
            cursor.execute(('DELETE FROM tblFilm WHERE Title = ?'), (movie, ))
            print(f'Success! {movie} has been removed from the database!')
            databaseConnection.commit()
        else:
            print('Process aborted, no movie was deleted!')
    #closing the database connection:
    cursor.close()
    databaseConnection.close()

#stubroutine to search for data in the database by either title or studio 
def recordSearch():
    #setting up teh database connection:
    databaseFile = 'MoviesdB.db'
    databaseConnection = sqlite3.connect(databaseFile)
    cursor = databaseConnection.cursor()
    print('You have selected the "search for a record" function!')
    #this loop decides whether you want to search via studio or title
    valid = False
    while True:
        valid = True    
        search = input('Would you like to search by title or studio? (t/s): ')
        if search != 't':
            if search != 's':
                print(f'Sorry "{search}" is not a valid input.')
                valid = False
        if valid == True:
            break
    cursor.execute('SELECT Title, Studio FROM tblFilm')
    fetchedMovies = cursor.fetchall()
    databaseConnection.commit()
    #statement to searh for data by studio
    if search == 's':
        again = False
        valid = True
        #loop to check whether the studio the user selects actually exists in the database:
        while True:
            valid = False
            studio = input('What studio would you like to return data from?: ')
            for i in fetchedMovies:
                if i[1] == studio:
                    valid = True
            if valid == False:
                again = input(f'Sorry {studio} is not a studio in the database, would you like to try again? (y/n): ')
                if again != 'y':
                    again = True
            if again != True:
                break 
        #statement to return the infromation from the database that corresponds to the selected studio, in a user friendly format
        if valid == True:
            cursor.execute(('SELECT * FROM tblFilm WHERE Studio = ?'), (studio, ))
            records = cursor.fetchall()
            databaseConnection.commit()
            gap()
            print(f"Here is the information on {studio}'s movies: ")
            gap()
            #forloop to display all of the data:
            for i in range(len(records)):
                movie = records[i][1]
                print(f'This is the information on {movie} which was released by {studio}: ')
                print(f'{movie} was released on the date: {records[i][3][0:10]}')
                print(f"{movie}'s total production cost was: {records[i][4]} million USD")
                print(f'{movie} brought in {records[i][5]} million USD at the box office')
                if records[i][6] == 1:
                    print(f'You have seen {movie}')
                else:
                    print(f'You have not seen {movie}')
                print(f'{movie} is classified as a {records[i][7]}')
                gap()
    #statement to searh for data by studio
    if search == 't':
        again = False
        valid = True
        #loop to check that the movie they are searching for actually exists in the database
        while True:
            valid = False
            movie = input('What movie would you like to return data from?: ')
            for i in fetchedMovies:
                if i[0] == movie:
                    valid = True
            if valid == False:
                again = input(f'Sorry {movie} is not a movie in the database, would you like to try again? (y/n): ')
                if again != 'y':
                    again = True
            if again != True:
                break 
        #statement to return the infromation from the database that corresponds to the selected movie, in a user friendly format
        if valid == True:
            cursor.execute(('SELECT * FROM tblFilm WHERE Title = ?'), (movie, ))
            records = cursor.fetchall()
            databaseConnection.commit()
            gap()
            print(f'Here is the information on {movie}: ')
            gap()
            print(f'{movie} was released by the studio: {records[0][2]}')
            print(f'{movie} was released on the date: {records[0][3][0:10]}')
            print(f"{movie}'s total production cost was: {records[0][4]} million USD")
            print(f'{movie} brought in {records[0][5]} million USD at the box office')
            if records[0][6] == 1:
                print(f'You have seen {movie}')
            else:
                print(f'You have not seen {movie}')
            print(f'{movie} is classified as a {records[0][7]}')

#main subroutine
def main():
    title = ' Database Homework '
    bar = '-'*len(title)
    bar.join('----')
    gap()
    print(bar)
    print(title)
    print(bar)
    #main menu loop that allows the user to select all of the functions or quit the program
    while True:
        print('''
Functions:
1. Record a new film record
2. Search for a record 
3. Delete a record
4. Quit
        ''')
        function = input('Enter the number of the function you wish to use: ')
        if function == '4':
            print('''
Thank you for using this program!
''')
            break
        elif function == '3':
            deleteRecord()
        elif function == '2':
            recordSearch()
        elif function == '1':
            recordRecord()
        else:
            print(f'''
Sorry '{function}' is not a valid choice, please choose one of functions 1-4!''')

main()