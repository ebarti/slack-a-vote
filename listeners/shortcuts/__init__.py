from slack_bolt import App

from config.constants import SHORTCUT_CALLBACK_ID
from .create_poll_shortcut import create_poll_shortcut_callback


def register(app: App):
    app.shortcut(SHORTCUT_CALLBACK_ID)(create_poll_shortcut_callback)
