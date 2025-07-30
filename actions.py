from streamdeck_sdk import events_received_objs

from core.base_action import BaseAction
from core.audio_mixer import AudioMixer
from core.text_widget import TextWidget

# spotify_cli = SpotifyCli()
text_widget = TextWidget()
spotify_mixer = AudioMixer("Spotify.exe")
discord_mixer = AudioMixer("Discord.exe")

class DiscordAct(BaseAction):
    ICON = "images/spotify"
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

class SpotifyAct(BaseAction):
    ICON = "images/spotify"
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


class TestAct2(BaseAction):
    CONTROLLERS = ["Keypad"]
    def on_key_down(self, obj: events_received_objs.KeyDown):
        # self.open_url("https://github.com/gri-gus/streamdeck-python-sdk")
        # self.show_ok(context=obj.context)
        print(obj)
        # current_playback = sp.current_playback()
        #
        # if current_playback and current_playback.get('item'):
        #     track_id = current_playback['item']['id']
        #
        #     # Получение данных о треке
        #     track_data = sp.track(track_id)
        #
        #     # Извлечение изображения
        #     images = track_data['album']['images']
        #
        #     if images:
        #         # Обычно первое изображение с самым высоким качеством
        #         track_image_url = images[0]['url']
        #         # print(track_image_url)
        #
        #         # Загрузка изображения
        #         response = requests.get(track_image_url, stream=True)
        #         image_binary = response.content
        #         image_mime = response.headers["Content-Type"]
        #         image_base64 = image_bytes_to_base64(obj=image_binary, image_mime=image_mime)
        #         self.set_image(obj.context, image_base64)
        #         self.set_title(obj.context, current_playback['item']['name'])
        #         if current_playback and current_playback['is_playing']:
        #             # Если играет, ставим на паузу
        #             sp.pause_playback()
        #         else:
        #             # Если на паузе, запускаем воспроизведение
        #             sp.start_playback()