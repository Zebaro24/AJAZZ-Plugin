from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


class SpotifyCli:
    def __init__(self):
        spotify_auth = SpotifyOAuth(scope="user-read-playback-state user-modify-playback-state")
        self.sp = Spotify(auth_manager=spotify_auth)
        self.current_playback = self.sp.current_playback()

        self.volume = self.get_volume()

    def get_volume(self):
        volume = int(self.current_playback["device"]["volume_percent"])
        print(f"Current volume: {volume}%")
        return volume

    def set_volume(self, volume):
        self.volume = volume
        self.sp.volume(self.volume)
        print("Volume set" , volume, '%')

    def add_volume(self, amount):
        self.volume = self.volume + amount
        self.sp.volume(self.volume)
        print("Volume added", amount, 'set', self.volume, '%')

if __name__ == "__main__":
    cli = SpotifyCli()