import re

from slack_bolt import App

from . import config, scheduler, mention, remind


config_ = config.get_config()

app = App(token=config_.bot_user_oauth_token, signing_secret=config_.signing_secret)
config_.app = app

scheduler = scheduler.Scheduler()
config_.scheduler = scheduler

mention.init()
remind.init()


def parse_command(body) -> tuple[str, list[str]]:
    message = re.sub(r"<@\w+>", "", body["event"]["text"]).strip().split()
    command = message[0] if message else ""
    options = message[1:]
    return command, options


@app.event("app_mention")
def handle_app_mentions(body, say, logger) -> None:
    logger.info(body)

    command, options = parse_command(body)

    command_funcs = {
        "usage": mention.reply_usage,
        "mtg": lambda: mention.set_mtg_date(date=options[0] if options else None),
        "minutes": mention.reply_minutes_pic,
        "order": mention.reply_presentation_order,
        "remind:ls": mention.get_reminds,
        "remind:rm": lambda: mention.remove_remind(id=options[0] if options else None),
    }

    command_func = command_funcs.get(command, mention.reply_random_message)
    say(command_func())


if __name__ == "__main__":
    port = config_.port
    app.start(port=port)
