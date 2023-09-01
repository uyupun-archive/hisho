import os

from dotenv import load_dotenv
from slack_bolt import App


load_dotenv()

bot_user_oauth_token = os.environ["BOT_USER_OAUTH_TOKEN"]
signing_secret = os.environ["SIGNING_SECRET"]
app = App(token=bot_user_oauth_token, signing_secret=signing_secret)


@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info(body)
    say("Hello there!")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.start(port=port)
