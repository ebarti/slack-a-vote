from typing import List

from slack_sdk import WebClient
from slack_sdk.models.blocks import (
    Block, ButtonElement, ContextBlock, DividerBlock, ImageElement, SectionBlock, TextObject,
)

from config.constants import BASE_WORKSPACE_URL, OPTIONS_BLOCK_ID, QUESTION_BLOCK_ID, VOTE_ACTION_PREFIX


def get_user_url(client: WebClient, user: str) -> str:
    user_info = client.users_info(user=user)
    if 'profile' in user_info.data['user'] and 'display_name' in user_info.data['user']['profile']:
        name = user_info.data['user']['profile']['display_name']
    else:
        name = user_info.data['user']['profile']['first_name']

    return f"<{BASE_WORKSPACE_URL}/team/{user_info.data['user']['id']}|{name}>"


def get_user_img24(client: WebClient, user: str) -> str:
    user_info = client.users_info(user=user)
    return user_info.data['user']['profile']['image_24']


def get_initial_poll_blocks(client: WebClient, body: dict) -> List[Block]:
    creator = body["user"]["id"]
    question = body["view"]['state']['values'][QUESTION_BLOCK_ID]["plain_text"]["value"]
    options = body["view"]['state']['values'][OPTIONS_BLOCK_ID]["plain_text"]["value"]
    blocks = [SectionBlock(
        text=TextObject(text=f"*{question}* Poll by {get_user_url(client, creator)}", type="mrkdwn")),
        DividerBlock()]
    choices = options.split("\n")

    for idx, choice in enumerate(choices):
        blocks.append(SectionBlock(
            block_id=f"{VOTE_ACTION_PREFIX}_{idx}_section",
            text=TextObject(text=choice, type="mrkdwn"),
            accessory=ButtonElement(text="Vote", action_id=f"{VOTE_ACTION_PREFIX}_{idx}", value="")))
        blocks.append(ContextBlock(block_id=f"{VOTE_ACTION_PREFIX}_{idx}_context",
                                   elements=[TextObject(text="0 votes", type="plain_text")]))
    return blocks


def get_updated_poll_blocks(client: WebClient, body: dict) -> List[Block]:
    user_id = body["user"]["id"]
    action_id = body['actions'][0]['action_id']
    user_img = get_user_img24(client, user_id)
    existent_blocks: List[Block] = []
    updated_blocks: List[Block] = []
    for block in body["message"]["blocks"]:
        existent_blocks.append(Block.parse(block))
    for block in existent_blocks:
        if block.block_id.endswith("_context") and block.type == ContextBlock.type:
            elements = [ImageElement(image_url=user_img, alt_text=user_id)] if block.block_id == f"{action_id}_context" else []
            elements.extend([element for element in block.elements if element.type == ImageElement.type and element.image_url != user_img])
            text = f"{len(elements)} votes" if len(elements) > 1 else f"{len(elements)} vote"
            elements.append(TextObject(text=text, type="plain_text"))
            block.elements = elements
        updated_blocks.append(block)
    return updated_blocks
