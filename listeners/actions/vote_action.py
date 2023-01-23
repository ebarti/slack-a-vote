import re
from logging import Logger

from slack_bolt import Ack, Respond
from slack_sdk import WebClient

from config.constants import VOTE_ACTION_PREFIX
from poll.message import get_updated_poll_blocks

VOTE_MATCHER = re.compile(f"{VOTE_ACTION_PREFIX}_\\d+", re.IGNORECASE)


def vote_action_callback(ack: Ack, client: WebClient, body: dict, respond: Respond, logger: Logger):
    try:
        ack()
        respond(
            blocks=get_updated_poll_blocks(client, body),
            replace_original=True
        )
    except Exception as e:
        logger.error(e)
