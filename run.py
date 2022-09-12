import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from client_details import *
from spotify_details import *

def run_spotify(client_id, client_secret):
    '''
    Access the Spotify API with a client ID and client secret
    '''
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                        client_secret=client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return spotify

def closed_question_answer_checks(y_or_n):
    '''
    Checks if the user inputs a valid y (yes) or n (no) value into the terminal
    '''
    remove_whitespace = y_or_n.replace(' ', '')
    while remove_whitespace.isalpha() == False or remove_whitespace.lower() not in ['y','n']:
        remove_whitespace = input('\nAnswer not valid. Please enter Y or N:\n')
        remove_whitespace.replace(' ', '')
    return remove_whitespace.lower()

def select_from_api(spotify, search_type):
    '''
    Connects to spotify API using credentials and selects user input values 
    based on whether they want to enter in an Artist or Track
    '''
    list_of_searched_values = []
    while len(list_of_searched_values) < 5:
        if search_type == 'Artist':
            artist_name = input(f'{len(list_of_searched_values) + 1}. Music Artist: \n')
            value = Artist(spotify, artist_name)
        elif search_type == 'Track':
            song_name = input(f'{len(list_of_searched_values) + 1}. Song Name:\n')
            song_artist = input('Song Sang By:\n')
            value = Track(song_artist, spotify, song_name)
            print(value.preview_link())
        value_id = value.id()
        if value_id and value_id not in list_of_searched_values:
            list_of_searched_values.append(value_id)
        else:
            print('\n******\nValue name is not valid or has already been entered'\
                ' please enter a new name\n******\n')
        if len(list_of_searched_values) < 5:
            check_for_another_artist = input('\nDo you want to add another: Y or N:\n')
            answer = closed_question_answer_checks(check_for_another_artist)
            if answer == 'y':
                pass
            else:
                break
    return list_of_searched_values

def artist_selection(spotify):
    '''
    Sets up the script for asking the user for music artists in the terminal 
    and returns their Spotify ID in a comma separated string
    '''
    print('Are you looking for some new song recommendations?\n'\
        'If yes, then you\'ve come to the right place!\n\n')
    print('In order to make some suitable recommendations, '\
        'we just need to get to know you a bit better!\n\n')
    print('First of all, we need to know who your favourite music artists'\
            'are at the moment?\n\nUp to 5!\n\n'\
            'Examples include: Cardi B, Arctic Monkeys and Bryan Adams\n\n'\
            'Make sure you spell their name correctly\n\n')
    music_artists = select_from_api(spotify, 'Artist')
    return music_artists

def format_genre_input(genre):
    '''
    Help validate genre name by removing whitespace either side, 
    making the genre all lower case and converting spaces to "-"
    '''
    genre = genre.lower()
    genre = genre.strip(' ')
    genre = genre.replace(' ', '-')
    return genre

def genre_is_valid(spotify, genre, all_possible_genres):
    '''Checks if a genre is in the list of spotify genres'''
    if genre.replace(' ', '').isalpha():
        genre = format_genre_input(genre)
    while genre not in all_possible_genres:
        genre = genre_is_valid(spotify, 
                                input('\nPlease input a new genre as the one entered is not valid\n'), 
                                all_possible_genres)
    return genre

def ask_for_genre(spotify, user_genre_list, all_possible_genres):
    '''Ask user for up to 5 genres and validate'''
    while len(user_genre_list) < 5:
        print(len(user_genre_list))
        genre_input = genre_is_valid(spotify, 
                                    input(f'{len(user_genre_list) + 1}. Genre: \n'), 
                                    all_possible_genres)
        if genre_input in user_genre_list:
            print('\nGenre has already been inputted, please select another one')
        while genre_input not in user_genre_list:
            user_genre_list.append(genre_input)
            if len(user_genre_list) < 5:
                check_for_another_artist = input('\nDo you want to add another: Y (for Yes) or N (for No):\n')
                answer = closed_question_answer_checks(check_for_another_artist)
                if answer == 'y':
                    pass
                else:
                    break
    return user_genre_list

def genre_selection(spotify):
    '''
    Prints list of all possible genres and
    read in the inputted genres from the user
    '''
    print('\n\nNext up is genre selection!!\n'\
        'Now we find out if you are more of a Dancing Queen or a Rock Star?'\
        '\n\n*****\nThe list below consists of the possible genres,'\
        'which you can input one at a time\n*****\n')
    user_genre_list = []
    all_possible_genres = spotify.recommendation_genre_seeds()['genres']
    genre_sentence = ',  '.join(str(genre) for genre in all_possible_genres)
    print(genre_sentence + '\n\n')
    user_genre_string = ask_for_genre(spotify, user_genre_list, all_possible_genres)
    return user_genre_string

def song_selection(spotify):
    '''
    Selects inputted songs and returns their IDs as a comma separated string
    '''
    print('We now need to know what your favourite songs to listen to'\
            'are at the moment!\nUp to 5!\n'\
            'Firstly put in the name of the song and then the primary artist\n'\
            'Examples include:\n\nSong Name:\nTimber\nSong Sang By:\nPitbull'\
            '\n\nSong Name:\nBelieve\nSong Sang By:\nCher\n\n'\
            'Watch out for spelling mistakes\n\n')
    songs = select_from_api(spotify, 'Track')
    return songs

def want_to(question, spotify_category):
    '''
    Asks the user a question about their mood, 
    which is related to a certain spotify category
    '''
    task_asked_about = closed_question_answer_checks(question)
    if task_asked_about == 'y':
        task_asked_about = f'max_{spotify_category}'
    else:
        task_asked_about = f'min_{spotify_category}'
    return task_asked_about

def song_style_questions():
    '''Asks the user if they want to dance, focus and listen to something popular'''
    print('\n\nWe just need to ask a few more questions to pick out'\
        '\nthe perfect songs for you!\n'\
        'These ones are more mood based\n\n*******\n\n'
    )
    dancing = want_to(input('1. Do you feel like dancing at the moment? Y or N\n'),
                        'danceability')
    focus = want_to(input('\n2. Do you want to focus at the moment? Y or N\n'), 'instrumentalness')
    popular = want_to(input('\n3. Do you want to listen to something popular? Y or N\n'), 'popularity')
    return dancing, focus, popular
    
def make_recommendations(spotify, seed_artists, seed_genres, seed_tracks):
    '''docstring'''
    rec = spotify.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks)

def main():
    spotify = run_spotify(CLIENT_ID, CLIENT_SECRET)
    # music_artists = artist_selection(spotify)
    # user_genres = genre_selection(spotify)
    favourite_songs = song_selection(spotify)
    print(favourite_songs)
    # dancing, focus, popular = song_style_questions()
    print('next stage')

main()
