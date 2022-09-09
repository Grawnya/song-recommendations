import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from client_details import *
from music_artists import *

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

def select_artists_from_api(spotify):
    '''
    Takes the spotify connection as an argument and
    gets the spotify IDs for the music artists called
    '''
    music_artists = []
    print('First of all, we need to know who your favourite music artists'\
            'are at the moment?\n\nUp to 5!\n\n'\
            'Examples include: Cardi B, Arctic Monkeys and Bryan Adams\n\n'\
            'Make sure you spell their name correctly\n\n')
    while len(music_artists) <= 5:
        artist = Artist(spotify, input(f'{len(music_artists) + 1}. Music Artist: \n'))
        artist_id = artist.artist_id()
        if artist_id:
            music_artists.append(artist_id)
        else:
            print('\n******\nArtist name is not valid, please enter a new name\n******\n')
        check_for_another_artist = input('\nDo you want to add another: Y or N:\n')
        answer = closed_question_answer_checks(check_for_another_artist)
        if answer == 'y':
            pass
        else:
            break
    return music_artists

def artist_selection(spotify):
    '''
    Sets up the script for asking the user for music artists in the terminal 
    and returns their Spotify ID in a comma separated string
    '''
    print('Are you looking for some new song recommendations?\n'\
        'If yes, then you\'ve come to the right place!\n\n')
    print('In order to make some suitable recommendations, '\
        'we just need to get to know you a bit better!\n\n')
    music_artists = select_artists_from_api(spotify)
    music_artists_string = ','.join([str(item) for item in music_artists])
    return music_artists_string

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
        genre = genre_is_valid(spotify, input('\nPlease input a new genre as the one entered is not valid\n'), all_possible_genres)
    return genre

def ask_for_genre(spotify, user_genre_list, all_possible_genres):
    '''Ask user for up to 5 genres and validate'''
    while len(user_genre_list) <= 5:
        genre_input = genre_is_valid(spotify, input(f'{len(user_genre_list) + 1}. Genre: \n'), all_possible_genres)
        user_genre_list.append(genre_input)
        check_for_another_artist = input('\nDo you want to add another: Y (for Yes) or N (for No):\n')
        answer = closed_question_answer_checks(check_for_another_artist)
        if answer == 'y':
            pass
        else:
            break
    user_genre_string = ','.join([str(item) for item in user_genre_list])
    return user_genre_string

def genre_selection(spotify):
    '''
    Prints list of all possible genres and
    read in the inputted genres from the user
    '''
    print('\n\nNext up is genre selection!!\n'\
        'Now we find out if you are more of a Dancing Queen or a Rock Star?'\
        '\n\n*****\nThe list below consists of the possible genres, which you can input one at a time\n'\
        '*****\n')
    user_genre_list = []
    all_possible_genres = spotify.recommendation_genre_seeds()['genres']
    genre_sentence = ',  '.join(str(genre) for genre in all_possible_genres)
    print(genre_sentence + '\n\n')
    user_genre_string = ask_for_genre(spotify, user_genre_list, all_possible_genres)
    return user_genre_string

def main():
    spotify = run_spotify(CLIENT_ID, CLIENT_SECRET)
    music_artists = artist_selection(spotify)
    print(music_artists)
    print('next stage')

main()
