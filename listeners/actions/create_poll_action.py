from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from ..views.create_poll_view import get_view as get_create_poll_view


def create_poll_action_callback(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        ack()
        client.views_open(
            trigger_id=body["trigger_id"],
            view=get_create_poll_view(),
        )
    except Exception as e:
        logger.error(e)
