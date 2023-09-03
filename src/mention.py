import random
import re
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.base import JobLookupError

from . import config, remind


config = config.config
scheduler = BackgroundScheduler()


def reply_usage() -> str:
    usage_messages = [
        "@hisho mtg YYYY/mm/dd: 今月の月次報告会の日時を設定し、前日の朝9時にリマインドします。",
        "@hisho minutes: 議事録の各担当者を決めます。",
        "@hisho order: 発表順を決めます。",
        "@hisho remind:list: 予約されているリマインドの一覧を表示します。",
        "@hisho remind:remove ID: 指定されたIDのリマインドを削除します。",
        "@hisho usage: このメッセージを表示します。",
        "@hisho それ以外のメッセージ: ランダムなメッセージを返します。",
    ]
    code_block_message = "```\n" + "\n".join(usage_messages) + "\n```"
    message = "秘書の井ノ上たきなです。\n私にできる仕事をまとめました。\n\n" + code_block_message
    return message


def get_reminds() -> str:
    jobs = scheduler.get_jobs()
    job_messages = [f"ID: {job.id}, 日時: {job.next_run_time.strftime('%Y/%m/%d %H:%M:%S')}" for job in jobs]
    code_block_message = "```\n" + "\n".join(job_messages) + "\n```"
    message = "予約されているリマインドの一覧をお伝えします。\n\n" + code_block_message
    return message


def remove_remind(id: str | None) -> str:
    if id is None:
        return "IDが指定されていません。\n`@hisho remind:remove ID` の形式で指定してください。"
    elif id == "mtg_candidate_reminder":
        return "指定されたリマインドは削除できません。"

    try:
        scheduler.remove_job(id)
        return "指定されたIDのリマインドを削除しました。"
    except JobLookupError:
        return f"指定されたIDのリマインドは存在しませんでした。"


def set_mtg_date(date: str | None) -> str:
    if date is None:
        return "日時が指定されていません。\n`@hisho mtg YYYY/mm/dd` の形式で指定してください。"
    elif not re.match(r"\d{4}/\d{2}/\d{2}", date):
        return "日時の形式が違います。\n`@hisho mtg YYYY/mm/dd` の形式で指定してください。"

    mtg_date = datetime.strptime(date, "%Y/%m/%d")
    reminder_time = mtg_date - timedelta(days=1)
    reminder_time = reminder_time.replace(hour=9, minute=0, second=0, microsecond=0)

    if reminder_time < datetime.now():
        return "前日の朝9時以降に月次報告会の日時は設定できません。"

    id = "mtg_reminder_" + reminder_time.strftime('%Y-%m-%d %H:%M:%S').replace('-', '_').replace(' ', '_').replace(':', '_')
    scheduler.add_job(
        remind.remind_mtg_date,
        trigger=DateTrigger(reminder_time),
        id=id,
    )
    return "月次報告会の前日の朝9時にリマインドを設定しました。"


def reply_minutes_pic() -> str:
    selected_members = random.sample(config.members, 3)
    roles = ["ファシリテーター", "書記", "Googleカレンダー入力者"]
    assign_message = [f"{role}は <@{member['id']}> さんです。" for role, member in zip(roles, selected_members)]
    message = "議事録の担当者をお伝えします。\n\n" + "\n".join(assign_message) + "\n\nよろしくお願いします。"
    return message


def reply_presentation_order() -> str:
    members = config.members
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
    remind.remind_mtg_candidate_date,
    trigger=CronTrigger(day="15", hour="9", minute="0"),
    id="mtg_candidate_reminder",
)
scheduler.start()
