import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from client_details import *


def run_spotify(client_id, client_secret):
    '''Access the Spotify API with a client ID and client secret'''
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                        client_secret=client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return spotify

def select_artists():
    music_artists = []
    print('First of all, we need to know who your favourite music artists'\
            'are at the moment?\n\nUp to 5!\n\n'\
            'Examples include: Cardi B, Arctic Monkeys and Bryan Adams\n\n'\
            'Make sure you spell their name correctly\n\n')

def main():
    spotify = run_spotify(CLIENT_ID, CLIENT_SECRET)
    print('Are you looking for some new song recommendations?\nIf yes, then you\'ve come to the right place!\n\n')
    print('In order to make some suitable recommendations, we just need to get to know you a bit better!\n\n')


main()