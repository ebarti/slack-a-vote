from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from config.constants import OPTIONS_BLOCK_ID, QUESTION_BLOCK_ID, VOTE_ACTION_PREFIX
from listeners.actions.vote_action import vote_action_callback
from poll.message import get_initial_poll_blocks


@pytest.fixture
def client():
    def user_info(user):
        return SimpleNamespace(data={"user": {
            "id": user,
            "profile": {"display_name": user, "image_24": f"https://example.invalid/{user}.png"},
        }})

    return SimpleNamespace(users_info=Mock(side_effect=user_info))


@pytest.fixture
def initial_blocks(client):
    body = {"user": {"id": "U_CREATOR"}, "view": {"state": {"values": {
        QUESTION_BLOCK_ID: {"plain_text": {"value": "Choose lunch"}},
        OPTIONS_BLOCK_ID: {"plain_text": {"value": "Option A\nOption B"}},
    }}}}
    return [block.to_dict() for block in get_initial_poll_blocks(client, body)]


def vote(client, blocks, user="U_FIRST", choice=0):
    ack, respond, logger = Mock(), Mock(), Mock()
    body = {
        "user": {"id": user},
        "actions": [{"action_id": f"{VOTE_ACTION_PREFIX}_{choice}"}],
        "message": {"blocks": blocks},
    }
    vote_action_callback(ack, client, body, respond, logger)
    ack.assert_called_once_with()
    logger.error.assert_not_called()
    respond.assert_called_once()
    assert respond.call_args.kwargs["replace_original"] is True
    return [block.to_dict() for block in respond.call_args.kwargs["blocks"]]


def voters(blocks, choice):
    context = next(block for block in blocks if block.get("block_id") == f"{VOTE_ACTION_PREFIX}_{choice}_context")
    return [element["alt_text"] for element in context["elements"] if element["type"] == "image"]


def test_first_vote_preserves_blocks_without_ids(client, initial_blocks):
    assert "block_id" not in initial_blocks[0]
    assert "block_id" not in initial_blocks[1]
    updated = vote(client, initial_blocks)
    assert updated[:2] == initial_blocks[:2]
    assert voters(updated, 0) == ["U_FIRST"]
    assert voters(updated, 1) == []
    assert updated[3]["elements"][-1]["text"] == "1 vote"


def test_repeated_vote_keeps_one_avatar_and_count(client, initial_blocks):
    first = vote(client, initial_blocks)
    repeated = vote(client, first)
    assert repeated == first


def test_changed_vote_removes_previous_choice_and_retains_other_voter(client, initial_blocks):
    first = vote(client, initial_blocks)
    second = vote(client, first, user="U_SECOND")
    assert voters(second, 0) == ["U_SECOND", "U_FIRST"]
    assert second[3]["elements"][-1]["text"] == "2 votes"
    moved = vote(client, second, choice=1)
    assert voters(moved, 0) == ["U_SECOND"]
    assert voters(moved, 1) == ["U_FIRST"]
    assert moved[3]["elements"][-1]["text"] == "1 vote"
    assert moved[5]["elements"][-1]["text"] == "1 vote"


def test_profile_failure_acknowledges_and_logs_then_next_vote_succeeds(client, initial_blocks):
    ack, respond, logger = Mock(), Mock(), Mock()
    client.users_info.side_effect = RuntimeError("synthetic profile failure")
    body = {"user": {"id": "U_FIRST"}, "actions": [{"action_id": f"{VOTE_ACTION_PREFIX}_0"}],
            "message": {"blocks": initial_blocks}}
    vote_action_callback(ack, client, body, respond, logger)
    ack.assert_called_once_with()
    respond.assert_not_called()
    assert str(logger.error.call_args.args[0]) == "synthetic profile failure"
    client.users_info.side_effect = None
    client.users_info.return_value = SimpleNamespace(data={"user": {"profile": {
        "image_24": "https://example.invalid/U_FIRST.png",
    }}})
    assert voters(vote(client, initial_blocks), 0) == ["U_FIRST"]
