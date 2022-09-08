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
    print('Are you looking for some new song recommendations?\n'\
        'If yes, then you\'ve come to the right place!\n\n')
    print('In order to make some suitable recommendations, '\
        'we just need to get to know you a bit better!\n\n')
    music_artists = select_artists_from_API(spotify)

def main():
    spotify = run_spotify(CLIENT_ID, CLIENT_SECRET)
    artist_selection(spotify)
    print('next stage')

main()
