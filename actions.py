from threading import Thread
from time import sleep

from streamdeck_sdk import events_received_objs, image_bytes_to_base64

from core.base_action import BaseAction
from core.audio_mixer import AudioMixer
from core.spotify_cli import SpotifyCli
from core.text_widget import TextWidget

spotify_cli = SpotifyCli()
text_widget = TextWidget()
spotify_mixer = AudioMixer("Spotify.exe")
discord_mixer = AudioMixer("Discord.exe")


class DiscordKnobAct(BaseAction):
    IMAGE = "images/discord"
    NAME = "Dicord mixer"
    CONTROLLERS = ["Knob"]
    TOOLTIP = "Tooltip"

    def on_dial_rotate(self, obj: events_received_objs.DialRotate):
        volume = discord_mixer.add_volume(obj.payload.ticks * 2)
        if volume is not None:
            text_widget.show_text(f"Громкость Discord: {volume}%")
            return
        text_widget.show_text(f"Приложение Discord не запущено!")

    def on_dial_down(self, obj: events_received_objs.SendToPlugin):
        print(obj)


class SpotifyKnobAct(BaseAction):
    IMAGE = "images/spotify"
    NAME = "Spotify mixer"
    CONTROLLERS = ["Knob"]
    TOOLTIP = "Tooltip"

    def on_dial_rotate(self, obj: events_received_objs.DialRotate):
        volume = spotify_mixer.add_volume(obj.payload.ticks * 2)
        if volume is not None:
            text_widget.show_text(f"Громкость Spotify: {volume}%")
            return
        text_widget.show_text(f"Приложение Spotify не запущено!")

    def on_dial_down(self, obj: events_received_objs.SendToPlugin):
        print(obj)


class SpotifyTrackAct(BaseAction):
    IMAGE = "images/spotify"
    NAME = "Spotify Track Image"
    CONTROLLERS = ["Keypad"]



    def on_key_down(self, obj: events_received_objs.KeyDown):
        spotify_cli.toggle_play()
        spotify_cli.update_playback()

    def __init__(self):
        super().__init__()

        self.is_auto_update_button = False

    def _while_update_button(self, obj):
        while self.is_auto_update_button:
            info = spotify_cli.get_info()
            if info:
                if not info["is_playing"]:
                    self.set_title(obj.context, "Пауза")
                    continue

                full_name = "🔊 " + info["full_name"] + "  "
                n = int(info["real_progress_sec"]*1.5) % len(full_name)
                title = full_name[n:] + full_name[:n]
                title += "\n\n\n"
                title += info["real_progress"]
                self.set_title(obj.context, title)
            else:
                self.set_title(obj.context, "")

            image = spotify_cli.get_image()
            if image:
                img_obj, img_mime = image

                image_base64 = image_bytes_to_base64(obj=img_obj, image_mime=img_mime)
                self.set_image(obj.context, image_base64)
            elif not spotify_cli.playback:
                spotify_cli.reset_load_image()
                self.set_image(obj.context, "")

            sleep(0.1)

    def auto_update_button(self, obj):
        if self.is_auto_update_button:
            spotify_cli.reset_load_image()
            return
        self.is_auto_update_button = True
        Thread(target=self._while_update_button, args=(obj,), daemon=True).start()

    def on_will_appear(self, obj):
        spotify_cli.auto_update_playback()
        self.auto_update_button(obj)


class SpotifyPrevAct(BaseAction):
    IMAGE = "images/previous"
    NAME = "Spotify Previous Track"
    CONTROLLERS = ["Keypad"]

    def on_key_down(self, obj: events_received_objs.KeyDown):
        spotify_cli.previous_track()
        spotify_cli.update_playback()


class SpotifyNextAct(BaseAction):
    IMAGE = "images/next"
    NAME = "Spotify Next Track"
    CONTROLLERS = ["Keypad"]

    def on_key_down(self, obj: events_received_objs.KeyDown):
        spotify_cli.next_track()
        spotify_cli.update_playback()