from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from ..views.create_poll_view import get_view as get_create_poll_view


def create_poll_shortcut_callback(body: dict, ack: Ack, client: WebClient, logger: Logger):
    try:
        ack()
        client.views_open(
            trigger_id=body["trigger_id"],
            view=get_create_poll_view(),
        )
    except Exception as e:
        logger.error(e)
