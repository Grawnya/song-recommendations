class SpotifyDetails:
    '''
    docstring to be updated
    '''
    def __init__(self, spotify_credentials, name, search_type_value):
        self.spotify = spotify_credentials
        self.name = name
        self.search_value = search_type_value
        self.specific_returned_item = self.search()
    
    def search(self):
        '''docstring'''
        results = self.spotify.search(q=f'{self.search_value}:{self.name}', type=f'{self.search_value}')
        narrowing_down_element_details = results[f'{self.search_value}s']
        return narrowing_down_element_details

    def characteristic(self, specific):
        '''docstring'''
        try:
            final_value = self.specific_returned_item['items'][0]
            value_spotify = final_value[specific]
        except IndexError:
            value_spotify = False
        return value_spotify

    def id(self):
        '''docstring'''
        return self.characteristic('id')

class Artist(SpotifyDetails):
    '''
    artist subclass
    '''
    def __init__(self, spotify_credentials, name):
        super().__init__(spotify_credentials, name, search_type_value='artist')

class Track(SpotifyDetails):
    '''
    track subclass
    '''
    def __init__(self, artist_name, spotify_credentials, name):
        self.artist_name = artist_name
        super().__init__(spotify_credentials, name, search_type_value='track')

    def search(self):
        '''docstring'''
        results = self.spotify.search(q=f'artist:{self.artist_name} {self.search_value}:{self.name}', type=f'{self.search_value}')
        narrowing_down_element_details = results[f'{self.search_value}s']
        return narrowing_down_element_details
    
    def preview_link(self):
        '''docstring'''
        link = self.characteristic('preview_url')
        if link == None:
            link = f'No Valid Preview Link - try the spotify link:\n{self.spotify_link()}'
        return link

    def spotify_link(self):
        '''docstring'''
        try:
            final_value = self.specific_returned_item['items'][0]
            spotify_link = final_value['external_urls']['spotify']
        except IndexError:
            spotify_link = False
        return spotify_link