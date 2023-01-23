from logging import Logger

from slack_bolt import Ack, Respond
from slack_sdk import WebClient
from slack_sdk.models.blocks import (ConversationSelectElement,
                                     InputBlock,
                                     PlainTextInputElement,
                                     PlainTextObject,
                                     )
from slack_sdk.models.views import View

from config.constants import CREATE_POLL_CALLBACK_ID, OPTIONS_BLOCK_ID, QUESTION_BLOCK_ID
from poll.message import get_initial_poll_blocks

SELECT_CHANNEL_BLOCK_ID = 'select_channel_block_id'


def get_view() -> View:
    return View(
        type="modal",
        title=PlainTextObject(text="Create a Poll"),
        callback_id=CREATE_POLL_CALLBACK_ID,
        submit=PlainTextObject(text="Submit"),
        blocks=[
            InputBlock(
                block_id=QUESTION_BLOCK_ID,
                label=PlainTextObject(text="What do you want to ask?"),
                element=PlainTextInputElement(action_id='plain_text')
            ),
            InputBlock(
                block_id=OPTIONS_BLOCK_ID,
                label=PlainTextObject(text="What options should the poll have? Type every option in a new line"),
                element=PlainTextInputElement(action_id='plain_text', multiline=True)
            ),
            InputBlock(
                block_id=SELECT_CHANNEL_BLOCK_ID,
                label=PlainTextObject(text="Select a channel to send the poll to"),
                element=ConversationSelectElement(action_id='select_channel_id', response_url_enabled=True)
            )
        ]
    )


def create_poll_submission_callback(ack: Ack, body: dict, client: WebClient, respond: Respond, logger: Logger):
    try:
        ack()
        channel = body["view"]['state']['values'][SELECT_CHANNEL_BLOCK_ID]["select_channel_id"]["selected_conversation"]
        client.chat_postMessage(channel=channel, blocks=get_initial_poll_blocks(client, body))
    except Exception as e:
        logger.error(e)
