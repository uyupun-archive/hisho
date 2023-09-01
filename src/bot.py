import os
import random
import re

from dotenv import load_dotenv
from slack_bolt import App


load_dotenv()

bot_user_oauth_token = os.environ["BOT_USER_OAUTH_TOKEN"]
signing_secret = os.environ["SIGNING_SECRET"]
app = App(token=bot_user_oauth_token, signing_secret=signing_secret)

members = [
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
]


@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info(body)

    message = re.sub(r"<@\w+>", "", body["event"]["text"]).strip()

    if message == "minutes":
        minutes_pic_reply(say)
    elif message == "presen":
        presentation_order_reply(say)
    else:
        random_reply(say)


def minutes_pic_reply(say):
    selected_members = random.sample(members, 3)
    roles = ["ファシリテーター", "書記", "Googleカレンダー入力者"]
    assign_message = [f"{role}は <@{member['id']}> さんです。" for role, member in zip(roles, selected_members)]
    message = "議事録の担当者をお伝えします。\n\n" + "\n".join(assign_message) + "\n\nよろしくお願いします。"
    say(message)


def presentation_order_reply(say):
    presenters = random.sample(members, len(members))
    presenters_message = [f"{i + 1}番目は <@{presenters[i]['id']}> さんです。" for i in range(len(presenters))]
    message = "発表順をお伝えします。\n\n" + "\n".join(presenters_message) + "\n\nよろしくお願いします。"
    say(message)


def random_reply(say):
    replies = [
        "それはできません。",
        "そこになければないです。",
        "何を言っているんですか？",
        "気持ちが悪いです。",
        "気分が悪くなってきました。",
        "いいかげんにしてください。",
        "そろそろキレますよ。",
        "私は召使いではないので。",
        "今回だけ、特別ですよ...？",
    ]
    reply = random.choice(replies)
    say(reply)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.start(port=port)
