import random
import re
from datetime import datetime, timedelta

from apscheduler.triggers.date import DateTrigger

from . import config, remind


config_ = None
scheduler = None


def init() -> None:
    global config_, scheduler
    config_ = config.get_config()
    scheduler = config_.scheduler


def format_message(message: str, messages: list[str]) -> str:
    return f"{message}\n\n" + "\n".join(messages)


def generate_code_block(messages: list[str]) -> str:
    return "```\n" + "\n".join(messages) + "\n```"


def reply_usage() -> str:
    messages = [
        "@hisho mtg YYYY/mm/dd: 今月の月次報告会の日時を設定し、前日の朝9時にリマインドします。",
        "@hisho minutes: 議事録の各担当者を決めます。",
        "@hisho order: 発表順を決めます。",
        "@hisho remind:ls: 予約されているリマインドの一覧を表示します。",
        "@hisho remind:rm ID: 指定されたIDのリマインドを削除します。",
        "@hisho usage: このメッセージを表示します。",
        "@hisho それ以外のメッセージ: ランダムなメッセージを返します。",
    ]
    return format_message("秘書の井ノ上たきなです。\n私にできる仕事をまとめました。", [generate_code_block(messages)])


def get_reminds() -> str:
    jobs = scheduler.get_jobs()
    messages = [f"名前: {job.name}, ID: {job.id}, 日時: {job.next_run_time.strftime('%Y/%m/%d %H:%M:%S')}" for job in jobs]
    return format_message("予約されているリマインドの一覧をお伝えします。", [generate_code_block(messages)])


def remove_remind(id: str | None) -> str:
    if not id:
        return "IDが指定されていません。\n`@hisho remind:remove ID` の形式で指定してください。"
    elif id == "mtg_candidate_reminder":
        return "指定されたリマインドは削除できません。"

    is_removed = scheduler.remove_job(id)
    if is_removed:
        return "指定されたIDのリマインドを削除しました。"
    else:
        return "指定されたIDのリマインドは存在しませんでした。"


def set_mtg_date(date: str | None) -> str:
    if not date:
        return "日時が指定されていません。\n`@hisho mtg YYYY/mm/dd` の形式で指定してください。"
    elif not re.match(r"\d{4}/\d{2}/\d{2}", date):
        return "日時の形式が違います。\n`@hisho mtg YYYY/mm/dd` の形式で指定してください。"

    reminder_time = (datetime.strptime(date, "%Y/%m/%d") - timedelta(days=1)).replace(hour=9, minute=0)
    if reminder_time < datetime.now():
        return "前日の朝9時以降に月次報告会の日時は設定できません。"

    id = f"mtg_reminder_{reminder_time.strftime('%Y_%m_%d_%H_%M_%S')}"
    is_added = scheduler.add_job(remind.remind_mtg_date, trigger=DateTrigger(reminder_time), id=id, name="月次報告会直前リマインド")
    if not is_added:
        return "既に同じ日時にリマインドが設定されています。"
    return "月次報告会の前日の朝9時にリマインドを設定しました。"


def reply_minutes_pic() -> str:
    selected_members = random.sample(config_.members, 3)
    roles = ["ファシリテーター", "書記", "スケジュール記録担当者"]
    messages = [f"{role}は <@{member['id']}> さんです。" for role, member in zip(roles, selected_members)]
    return format_message("議事録の担当者をお伝えします。", messages + ["\nよろしくお願いします。"])


def reply_presentation_order() -> str:
    presenters = random.sample(config_.members, len(config_.members))
    messages = [f"{i + 1}番目は <@{presenter['id']}> さんです。" for i, presenter in enumerate(presenters)]
    return format_message("発表順をお伝えします。", messages + ["\nよろしくお願いします。"])


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
    return random.choice(messages)
