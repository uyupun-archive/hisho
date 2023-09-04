from . import config


config_ = None


def init() -> None:
    global config_
    config_ = config.get_config()


def remind_mtg_candidate_date() -> None:
    channel_id = config_.get_post_channel_id()
    config_.app.client.chat_postMessage(
        channel=channel_id,
        text="<!channel> 今月の月次報告会の候補日を提出してください。"
    )


def remind_mtg_date() -> None:
    channel_id = config_.get_post_channel_id()
    config_.app.client.chat_postMessage(
        channel=channel_id,
        text="<!channel> 明日の21時〜月次報告会です。"
    )
