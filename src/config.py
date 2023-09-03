import os
from typing import Any

from dotenv import load_dotenv


load_dotenv()


class Config:
    def __init__(self):
        self._config = {
            "port": self._get_env_as_int("PORT", 3000),
            "bot_user_oauth_token": self._get_env("BOT_USER_OAUTH_TOKEN"),
            "signing_secret": self._get_env("SIGNING_SECRET"),
            "is_debug": self._get_env_as_bool("IS_DEBUG", False),
            "members": [
                {"id": "U01SX25JC6B", "name": "Daisuke"},
                {"id": "U01T7J3GXSR", "name": "kakimoto"},
                {"id": "U01TP8Y2MLZ", "name": "Kazukichi"},
                {"id": "U01TC1RLQR1", "name": "takashi"},
            ],
            "channels": {
                "std-mtg": "C01U1QN5M5E",
                "proj-hisho-sandbox": "C05QN0U6U3U"
            },
            "app": None
        }

    def _get_env(self, key: str, default: Any = None) -> str:
        return os.environ.get(key, default)

    def _get_env_as_int(self, key: str, default: int = 0) -> int:
        return int(self._get_env(key, default))

    def _get_env_as_bool(self, key: str, default: bool = False) -> bool:
        return self._get_env(key, "true" if default else "false").lower() == "true"

    @property
    def port(self) -> int:
        return self._config["port"]

    @property
    def bot_user_oauth_token(self) -> str:
        return self._config["bot_user_oauth_token"]

    @property
    def signing_secret(self) -> str:
        return self._config["signing_secret"]

    @property
    def is_debug(self) -> bool:
        return self._config["is_debug"]

    @property
    def members(self) -> list[dict[str, str]]:
        return self._config["members"]

    @property
    def channels(self) -> dict[str, str]:
        return self._config["channels"]

    @property
    def app(self):
        return self._config["app"]

    @app.setter
    def app(self, app):
        self._config["app"] = app

    def get_post_channel_id(self) -> str:
        return self.channels["proj-hisho-sandbox"] if self.is_debug else self.channels["std-mtg"]

config = Config()
