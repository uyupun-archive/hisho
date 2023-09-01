import os
import random

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

    text = body["event"]["text"].replace("<@U05RC02JLQ0> ", "")

    if text == "minutes":
        minutes_reply(say)
    else:
        random_reply(say)


def minutes_reply(say):
    selected_members = random.sample(members, 3)
    say(f"議事録の担当者をお伝えします。\n\nファシリテーターは <@{selected_members[0]['id']}> さんです。\n書記は <@{selected_members[1]['id']}> さんです。\nGoogleカレンダー入力者は <@{selected_members[2]['id']}> さんです。\n\nよろしくお願いします。")


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
