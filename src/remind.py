from . import config


config = config.config


def remind_mtg_candidate_date() -> None:
    channel_id = config.get_post_channel_id()
    config.app.client.chat_postMessage(
        channel=channel_id,
        text="<!channel> 今月の月次報告会の候補日を提出してください。"
    )


def remind_mtg_date() -> None:
    channel_id = config.get_post_channel_id()
    config.app.client.chat_postMessage(
        channel=channel_id,
        text="<!channel> 明日の21時〜月次報告会です。"
    )
