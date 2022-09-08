import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from client_details import *

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID,
                                                    client_secret=CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def main():
    print('place functions here')

main()