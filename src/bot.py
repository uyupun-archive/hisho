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
def handle_app_mentions(body, say, logger) -> None:
    logger.info(body)

    sender_message = re.sub(r"<@\w+>", "", body["event"]["text"]).strip()

    if sender_message == "usage":
        receiver_message = reply_usage()
    elif sender_message == "minutes":
        receiver_message = reply_minutes_pic()
    elif sender_message == "presen":
        receiver_message = reply_presentation_order()
    else:
        receiver_message = reply_random_message()

    say(receiver_message)


def reply_usage() -> str:
    usage_messages = [
        "@hisho minutes: 議事録の各担当者を決めます。",
        "@hisho presen: 発表順を決めます。",
        "@hisho usage: このメッセージを表示します。",
        "それ以外のメッセージ: ランダムなメッセージを返します。",
    ]
    message =  "秘書の井ノ上たきなです。\n私にできる仕事をまとめました。\n\n" + "\n".join(usage_messages)
    return message


def reply_minutes_pic() -> str:
    selected_members = random.sample(members, 3)
    roles = ["ファシリテーター", "書記", "Googleカレンダー入力者"]
    assign_message = [f"{role}は <@{member['id']}> さんです。" for role, member in zip(roles, selected_members)]
    message = "議事録の担当者をお伝えします。\n\n" + "\n".join(assign_message) + "\n\nよろしくお願いします。"
    return message


def reply_presentation_order() -> str:
    presenters = random.sample(members, len(members))
    presenters_message = [f"{i + 1}番目は <@{presenters[i]['id']}> さんです。" for i in range(len(presenters))]
    message = "発表順をお伝えします。\n\n" + "\n".join(presenters_message) + "\n\nよろしくお願いします。"
    return message


def reply_random_message() -> str:
    messages = [
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
    message = random.choice(messages)
    return message


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.start(port=port)
