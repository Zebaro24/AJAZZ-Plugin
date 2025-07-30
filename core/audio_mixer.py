from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from functools import wraps


def require_mixer(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.mixer = self.mixer or self._get_mixer()
        if self.mixer is None:
            return None
        return func(self, *args, **kwargs)

    return wrapper


class AudioMixer:
    def __init__(self, target):
        self.target = target
        self.mixer = None

    def _get_mixer(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            mixer = session._ctl.QueryInterface(ISimpleAudioVolume)  # noqa
            if session.Process and session.Process.name() == self.target:
                return mixer
        return None

    def _get_volume(self):
        return round(self.mixer.GetMasterVolume() * 100)

    @require_mixer
    def get_volume(self):
        return self._get_volume()

    @require_mixer
    def set_volume(self, volume):
        self.mixer.SetMasterVolume(volume / 100, None)
        return volume

    @require_mixer
    def add_volume(self, amount):
        volume_now = self._get_volume() + amount
        if volume_now > 100:
            volume_now = 100
        if volume_now < 0:
            volume_now = 0
        print('Volume', self.target, 'set', volume_now)
        return self.set_volume(volume_now)


if __name__ == "__main__":
    audio_mixer = AudioMixer("Spotify.exe")

    print(audio_mixer.get_volume())
