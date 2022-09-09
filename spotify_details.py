class SpotifyDetails:
    '''
    docstring to be updated
    '''
    def __init__(self, spotify_credentials, name, search_type_value):
        self.spotify = spotify_credentials
        self.name = name
        self.search_value = search_type_value

    def id(self):
        results = self.spotify.search(q=f'{self.search_value}' + self.name, type=f'{self.search_value}')
        narrowing_down_element_details = results[f'{self.search_value}s']
        try:
            final_value = narrowing_down_element_details['items'][0]
            value_spotify_id = final_value['id']
        except IndexError:
            value_spotify_id = False
        return value_spotify_id

class Artist(SpotifyDetails):
    '''
    artist subclass
    '''
    def __init__(self, spotify_credentials, name):
        super().__init__(spotify_credentials, name, 'artist')

class Track(SpotifyDetails):
    '''
    track subclass
    '''
    def __init__(self, spotify_credentials, name):
        super().__init__(spotify_credentials, name, 'track')