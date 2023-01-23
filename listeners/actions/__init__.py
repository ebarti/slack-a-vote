from slack_bolt import App

from config.constants import CREATE_POLL_BUTTON_CALLBACK_ID
from .create_poll_action import create_poll_action_callback
from .vote_action import VOTE_MATCHER, vote_action_callback


def register(app: App):
    app.action(CREATE_POLL_BUTTON_CALLBACK_ID)(create_poll_action_callback)
    app.action(VOTE_MATCHER)(vote_action_callback)
