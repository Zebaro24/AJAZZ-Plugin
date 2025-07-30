from pathlib import Path
from logging import DEBUG

from streamdeck_sdk import StreamDeck
from dotenv import load_dotenv
load_dotenv()

import actions

if __name__ == '__main__':
    StreamDeck(
        actions=[action_class() for action_class in actions.BaseAction.__subclasses__()],
        log_file=Path("logs") / "last.log",
        log_level=DEBUG,
        log_backup_count=1,
    ).run()
