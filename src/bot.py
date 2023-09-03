import os
import re

from slack_bolt import App

from . import config, mention


config_ = config.config
app = App(token=config_["bot_user_oauth_token"], signing_secret=config_["signing_secret"])
config.set_app(app)


@app.event("app_mention")
def handle_app_mentions(body, say, logger) -> None:
    logger.info(body)

    sender_message = re.sub(r"<@\w+>", "", body["event"]["text"]).strip().split()
    sender_command = sender_message[0] if len(sender_message) >= 1 else None
    sender_options = sender_message[1:] if len(sender_message) >= 2 else []

    if sender_command == "usage":
        receiver_message = mention.reply_usage()
    elif sender_command == "mtg":
        date = None
        if len(sender_options) >= 1:
            date = sender_options[0]
        receiver_message = mention.set_mtg_date(date=date)
    elif sender_command == "minutes":
        receiver_message = mention.reply_minutes_pic()
    elif sender_command == "order":
        receiver_message = mention.reply_presentation_order()
    elif sender_command == "remind:list":
        receiver_message = mention.get_reminds()
    elif sender_command == "remind:remove":
        id = None
        if len(sender_options) >= 1:
            id = sender_options[0]
        receiver_message = mention.remove_remind(id=id)
    else:
        receiver_message = mention.reply_random_message()

    say(receiver_message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.start(port=port)
