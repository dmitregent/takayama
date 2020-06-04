import re
from mpd import MPDClient


class TakayamaMpdClient:
    def __init__(self):
        self.client = MPDClient()
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None
        self.client.connect("127.0.0.1", 9009)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.client.disconnect()

    def clear_playlist(self):
        self.client.clear()

    def add_tracks_by_artist(self, artist, track_name):
        artist = re.sub(r'^The ', '', artist)
        artist = TakayamaMpdClient.mpd_quote(artist)
        track_name = TakayamaMpdClient.mpd_quote(track_name)
        search_string = '((artist =~ \".*' + artist + '.*\") AND (title =~ \".*' + track_name + '.*\"))'
        count = len(self.client.search(search_string))
        if count == 0:
            print('No ' + artist + ' - ' + track_name + ' in library!')
            return
        if count > 2:
            print('WTF request with ' + str(count) + ' results => ' + search_string)
        self.client.searchadd(search_string)

    @staticmethod
    def mpd_quote(s):
        return s\
            .replace('(', r'.')\
            .replace(')', '.')\
            .replace(':', '.')\
            .replace('/', '.')\
            .replace('[', '.')\
            .replace(']', '.')\
            .replace("'", '.')
