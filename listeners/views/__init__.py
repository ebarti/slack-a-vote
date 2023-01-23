from slack_bolt import App

from config.constants import CREATE_POLL_CALLBACK_ID
from .create_poll_view import create_poll_submission_callback


def register(app: App):
    app.view(CREATE_POLL_CALLBACK_ID)(create_poll_submission_callback)
