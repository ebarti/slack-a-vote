from logging import Logger

from config.constants import CREATE_POLL_BUTTON_CALLBACK_ID


def app_home_opened_callback(client, event, logger: Logger):
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return
    try:
        client.views_publish(
            user_id=event["user"],
            view={
                "type":   "home",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Here's what you can do with the Poll App:"
                        }
                    },
                    {
                        "type":     "actions",
                        "elements": [
                            {
                                "type":      "button",
                                "text":      {
                                    "type":  "plain_text",
                                    "text":  "Create a New Poll",
                                    "emoji": True
                                },
                                "style":     "primary",
                                "value":     f"Go",
                                "action_id": f"{CREATE_POLL_BUTTON_CALLBACK_ID}"
                            },
                            {
                                "type":  "button",
                                "text":  {
                                    "type":  "plain_text",
                                    "text":  "Get Help",
                                    "emoji": True
                                },
                                "value": "help"
                            }
                        ]
                    }
                ]
            },
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
