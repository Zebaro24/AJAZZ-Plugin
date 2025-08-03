from functools import wraps
from threading import Thread
from time import sleep, time

import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def requires_playback(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            if self.playback is None:
                return None
            return func(self, *args, **kwargs)
        except Exception as e:
            print("Error")
            print(e)

    return wrapper


class SpotifyCli:
    def __init__(self):
        spotify_auth = SpotifyOAuth(scope="user-read-playback-state user-modify-playback-state")
        self.sp = Spotify(auth_manager=spotify_auth)

        self.playback = None
        self.update_time = None

        self.load_img_url = None
        self.is_auto_update = False

    def update_playback(self):
        self.playback = self.sp.current_playback()
        self.update_time = time()
        if self.playback is None:
            print("No playback found")

    def _while_update_playback(self, sec=2):
        while self.is_auto_update:
            self.update_playback()
            sleep(sec)

    def auto_update_playback(self, sec=2):
        if self.is_auto_update:
            return
        self.is_auto_update = True
        Thread(target=self._while_update_playback, args=(sec,), daemon=True).start()

    @requires_playback
    def get_json(self):
        print(self.playback)

    @requires_playback
    def play(self):
        if not self.playback["is_playing"]:
            self.sp.start_playback()

    @requires_playback
    def pause(self):
        if self.playback["is_playing"]:
            self.sp.pause_playback()

    @requires_playback
    def toggle_play(self):
        if self.playback["is_playing"]:
            self.sp.pause_playback()
        else:
            self.sp.start_playback()

    @requires_playback
    def next_track(self):
        self.sp.next_track()
        return True

    @requires_playback
    def previous_track(self):
        self.sp.previous_track(self.playback['device']['id'])
        return True

    @requires_playback
    def get_volume(self):
        volume = int(self.playback["device"]["volume_percent"])
        print(f"Current volume: {volume}%")
        return volume

    @requires_playback
    def set_volume(self, volume):
        self.sp.volume(volume)
        print("Volume set", volume, '%')

    def add_volume(self, amount):
        volume = self.get_volume()
        if volume is None:
            return
        volume += amount
        self.sp.volume(volume)
        print("Volume added", amount, 'set', volume, '%')

    @requires_playback
    def get_info(self):
        track = self.playback['item']

        track_info = {
            "is_playing": self.playback['is_playing'],

            "track_name": track['name'],
            "artist_name": track['artists'][0]['name'],
            "full_name": f"{track['name']} - {track['artists'][0]['name']}",
            # "image_url": track['album']['images'][0]['url'],

            "duration_sec": track['duration_ms'] / 1000,
            "progress_sec": self.playback['progress_ms'] / 1000,
        }

        if track_info['is_playing']:
            track_info["real_progress_sec"] = track_info['progress_sec'] + (time() - self.update_time)
        else:
            track_info["real_progress_sec"] = track_info['progress_sec']

        def conv_time(seconds):
            minutes, seconds = divmod(seconds, 60)
            return "{:02d}:{:02d}".format(int(minutes), int(seconds))

        track_info["progress"] = conv_time(track_info['progress_sec'])
        track_info["real_progress"] = conv_time(track_info["real_progress_sec"])

        return track_info

    @requires_playback
    def get_image(self):
        url = self.playback['item']['album']['images'][0]['url']

        if url == self.load_img_url:
            return None

        self.load_img_url = url
        response = requests.get(url, stream=True)
        return response.content, response.headers["Content-Type"]

    def reset_load_image(self):
        self.load_img_url = None


if __name__ == "__main__":
    cli = SpotifyCli()
    cli.update_playback()
    cli.get_info()

    sleep(2)
    cli.get_info()
    sleep(7)
    cli.get_info()

    # os.system(r'start "" "C:\Users\<User>\AppData\Roaming\Spotify\Spotify.exe"')
