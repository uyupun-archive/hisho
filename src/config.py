import os

from dotenv import load_dotenv


load_dotenv()

config = {
    "is_debug": os.getenv("IS_DEBUG", "false").lower() == "true",
    "bot_user_oauth_token": os.environ["BOT_USER_OAUTH_TOKEN"],
    "signing_secret": os.environ["SIGNING_SECRET"],
    "members": [
        {
            "id": "U01SX25JC6B",
            "name": "Daisuke",
        },
        {
            "id": "U01T7J3GXSR",
            "name": "kakimoto",
        },
        {
            "id": "U01TP8Y2MLZ",
            "name": "Kazukichi",
        },
        {
            "id": "U01TC1RLQR1",
            "name": "takashi",
        },
    ],
    "channels": {
        "std-mtg": "C01U1QN5M5E",
        "proj-hisho-sandbox": "C05QN0U6U3U"
    },
    "app": None,
}


def set_app(app):
    config["app"] = app


def get_app():
    return config["app"]


def get_post_channel_id() -> str:
    channels = config["channels"]
    if config["is_debug"]:
        return channels["proj-hisho-sandbox"]
    else:
        return channels["std-mtg"]
