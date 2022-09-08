class Artist:
    
    def __init__(self, spotify_credentials, name):
        self.spotify = spotify_credentials
        self.name = name
        self.id = self.artist_id()

    def artist_id(self):
        results = self.spotify.search(q='artist:' + self.name, type='artist')
        narrowing_down_artist_details = results['artists']
        try:
            final_artist = narrowing_down_artist_details['items'][0]
            music_artist_spotify_id = final_artist['id']
        except IndexError:
            music_artist_spotify_id = False
        return music_artist_spotify_id