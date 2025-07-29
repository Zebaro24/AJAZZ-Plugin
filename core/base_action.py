import settings

from streamdeck_sdk import Action


class BaseAction(Action):
    ICON = "images/spotify"
    NAME = "Name"
    CONTROLLERS = ["Knob"]
    TOOLTIP = "Tooltip"

    def __init__(self):
        name = self.__class__.__name__
        self.UUID = settings.PLUGIN_ID + '.' + name[:1].lower() + name[1:]
        super().__init__()
