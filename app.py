import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners


# Initialization
# Socket Mode uses the app token; retain HTTP signature checks when configured.
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    request_verification_enabled=bool(os.environ.get("SLACK_SIGNING_SECRET")),
)
logging.basicConfig(level=logging.DEBUG)

# Register Listeners
register_listeners(app)

# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
