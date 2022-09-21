import json
import spotipy
import readline
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_details import *
import os
from os import path
if path.exists("env.py"):
    import env


def run_spotify():
    '''
    Access the Spotify API with a client ID and client secret
    from the client_details.json file
    '''
    creds = {'client_id': os.environ.get("CLIENT_ID"),
             'client_secret': os.environ.get("CLIENT_SECRET")}
    credentials = SpotifyClientCredentials(**creds)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)
    return spotify


def closed_question_answer_checks(y_or_n):
    '''
    Checks if the user inputs a valid y (yes) or n (no) value into the terminal
    '''
    remove_whitespace = y_or_n.replace(' ', '')
    if remove_whitespace == 'yes':
        remove_whitespace = 'y'
    elif remove_whitespace == 'no':
        remove_whitespace = 'n'
    while remove_whitespace.isalpha() is False or \
            remove_whitespace.lower() not in ['y', 'n']:
        remove_whitespace = input('\nAnswer not valid. '
                                  'Please enter y (for yes) or n (for no):\n')
        remove_whitespace.replace(' ', '')
    return remove_whitespace.lower()


def select_from_api(spotify, search_type):
    '''
    Connects to spotify API using credentials and selects user input values
    based on whether they want to enter in an Artist or Track
    '''
    valid_value = False
    while valid_value is False:
        if search_type == 'Artist':
            artist_name = input('Music Artist: \n')
            value = Artist(spotify, artist_name)
        elif search_type == 'Track':
            song_name = input('Song Name:\n')
            while song_name == '':
                song_name = input('\nInvalid key or blank answer given\n'
                                  'Please enter a new Song Name\n')
            song_artist = input('Song Sang By:\n')
            while song_artist == '':
                song_artist = input('\nInvalid key or blank answer given\n'
                                    'Please enter the name of the artist '
                                    f'who sang {song_name}\n')
            value = Track(song_artist, spotify, song_name)
        value_id = value.id()
        if value_id:
            valid_value = True
            return value_id
        else:
            print('\n******\nValue name is not valid'
                  ' please enter a new name\n******\n')


def artist_selection(spotify):
    '''
    Sets up the script for asking the user for music artists in the terminal
    and returns their Spotify ID in a comma separated string
    '''
    print('Are you looking for some new song recommendations?\n'
          'If yes, then you\'ve come to the right place!\n\n'
          'In order to make some suitable recommendations, '
          'we just need to get to know you a bit better!\n\n'
          'First of all, we need to know who your favourite music artists'
          ' are at the moment?\n\nUp to 5!\n\n'
          'Examples include: Cardi B, Arctic Monkeys and Bryan Adams\n\n'
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


def genre_is_valid(genre, all_possible_genres):
    '''Checks if a genre is in the list of spotify genres'''
    if genre.replace(' ', '').isalpha():
        genre = format_genre_input(genre)
    while genre not in all_possible_genres:
        genre = genre_is_valid(input('\nPlease input a new genre as '
                                     'the one entered is not valid\n'),
                               all_possible_genres)
    return genre


def genre_selection(spotify):
    '''
    Prints list of all possible genres and
    read in the inputted genres from the user
    '''
    print('\n\nNext up is genre selection!!\n'
          'Now we find out if you are more of a Dancing Queen or a Rock Star?'
          '\n\n*****\nThe list below consists of the possible genres,'
          'which you can input one at a time\n*****\n')
    all_possible_genres = spotify.recommendation_genre_seeds()['genres']
    genre_sentence = ',  '.join(str(genre) for genre in all_possible_genres)
    print(genre_sentence + '\n\n')
    genre_input = genre_is_valid(input('Genre: \n'),
                                 all_possible_genres)
    return genre_input


def song_selection(spotify):
    '''
    Selects inputted songs and returns their IDs as a comma separated string
    '''
    print('We now need to know what your favourite songs to listen to'
          'are at the moment!\nUp to 5!\n'
          'Firstly put in the name of the song and then the primary artist\n'
          'Examples include:\n\nSong Name:\nTimber\nSong Sang By:\nPitbull'
          '\n\nSong Name:\nBelieve\nSong Sang By:\nCher\n\n'
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
        task_asked_about = f'min_{spotify_category}'
    else:
        task_asked_about = f'max_{spotify_category}'
    return task_asked_about


def song_style_questions():
    '''
    Asks the user if they want to dance,
    focus and listen to something popular
    '''
    print('\n\nWe just need to ask a few more questions to pick out'
          '\nthe perfect songs for you!\n'
          'These ones are more mood based\n\n*******\n\n')
    dancing = want_to(input('1. Do you feel like dancing at the moment?'
                      ' y or n\n'),
                      'danceability')
    focus = want_to(input('\n2. Do you want to focus at the moment? y or n\n'),
                    'instrumentalness')
    popular = want_to(input('\n3. Do you want to listen to something popular?'
                      ' y or n\n'),
                      'popularity')
    mood_values = {dancing: 0.5, focus: 0.5, popular: 50}
    return mood_values


def make_recommendations(spotify, seed_artists, seed_genres,
                         seed_tracks, mood_values):
    '''
    Feed the inputted artist, genre, song and mood
    values into the Spotify API to make recommendations
    '''
    rec = spotify.recommendations(seed_artists=[seed_artists],
                                  seed_genres=[seed_genres],
                                  seed_tracks=[seed_tracks],
                                  **mood_values)
    song_recommendations = rec['tracks']
    for each in song_recommendations:
        song_name = each['name']
        song_artist = each['artists'][0]['name']
        song = Track(song_artist, spotify, song_name)
        print(f'\nSong Name: {song_name}')
        print(f'Song Artist: {song_artist}')
        print(f'Song Preview: {song.preview_link()}')
        if 'No Valid Preview Link' not in song.preview_link():
            print(f'Here\'s the Spotify Link: {song.spotify_link()}')
        if song_recommendations.index(each) < 19:
            another_one = '\nAnother One?....Song recommendation that is '\
                          '(Type y or n)'
            another_song_answer = closed_question_answer_checks(input(
                                                                another_one +
                                                                '\n'))
            if another_song_answer == 'y':
                print('\n')
            else:
                break
    play_again = closed_question_answer_checks(input('\n\n*****\n'
                                                     'Thanks for playing! '
                                                     'Do you want to play '
                                                     'again for more song '
                                                     'recommendations?\n\n'
                                                     'y or n\n\n'))
    print('\n'*2)
    return play_again


def main():
    play_again = 'y'
    while play_again == 'y':
        spotify = run_spotify()
        music_artists = artist_selection(spotify)
        user_genres = genre_selection(spotify)
        favourite_songs = song_selection(spotify)
        mood_values = song_style_questions()
        play_again = make_recommendations(spotify,
                                          music_artists,
                                          user_genres,
                                          favourite_songs,
                                          mood_values)
    else:
        print('*****\n\nThank you for playing!\n'
              'If you have any feedback, please reach out to: '
              'https://www.linkedin.com/in/grainne-donegan/'
              '\n\n*****')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n*****\nYou interrupted the game, lets play again\n*****\n')
        main()
