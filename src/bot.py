import os
import random
import re
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from dotenv import load_dotenv
from slack_bolt import App


load_dotenv()

bot_user_oauth_token = os.environ["BOT_USER_OAUTH_TOKEN"]
signing_secret = os.environ["SIGNING_SECRET"]
app = App(token=bot_user_oauth_token, signing_secret=signing_secret)
scheduler = BackgroundScheduler()

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
    sender_command = sender_message.split()[0]

    if sender_command == "usage":
        receiver_message = reply_usage()
    elif sender_command == "mtg":
        date = sender_message.split()[1]
        receiver_message = set_mtg_date(date=date)
    elif sender_command == "minutes":
        receiver_message = reply_minutes_pic()
    elif sender_command == "presen":
        receiver_message = reply_presentation_order()
    else:
        receiver_message = reply_random_message()

    say(receiver_message)


def reply_usage() -> str:
    usage_messages = [
        "@hisho mtg: 今月の月次報告会の日時を設定します。"
        "@hisho minutes: 議事録の各担当者を決めます。",
        "@hisho presen: 発表順を決めます。",
        "@hisho usage: このメッセージを表示します。",
        "それ以外のメッセージ: ランダムなメッセージを返します。",
    ]
    message =  "秘書の井ノ上たきなです。\n私にできる仕事をまとめました。\n\n" + "\n".join(usage_messages)
    return message


def remind_mtg_candidate_date():
    # channel_id = "C01U1QN5M5E"
    channel_id = "C05QN0U6U3U"
    app.client.chat_postMessage(
        channel=channel_id,
        text="<!channel> 今月の月次報告会の候補日を提出してください。"
    )


def remind_mtg_date():
    # channel_id = "C01U1QN5M5E"
    channel_id = "C05QN0U6U3U"
    app.client.chat_postMessage(
        channel=channel_id,
        text="<!channel> 明日の21時〜月次報告会です。"
    )


def set_mtg_date(date: str) -> str:
    mtg_date = datetime.strptime(date, "%Y/%m/%d")
    reminder_time = mtg_date - timedelta(days=1)
    reminder_time = reminder_time.replace(hour=9, minute=0, second=0, microsecond=0)
    scheduler.add_job(
        remind_mtg_date,
        trigger=DateTrigger(reminder_time),
    )
    return "月次報告会の前日の朝9時にリマインドを設定しました。"


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


scheduler.add_job(
    remind_mtg_candidate_date,
    # trigger=CronTrigger(minute="30"),
    trigger=CronTrigger(day="15"),
)
scheduler.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.start(port=port)
