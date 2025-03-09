import time
from helpers.config_loader import ConfigLoader
from helpers.time_utils import time_to_str, unixtime_to_date
from services.helpshift_api import HelpshiftAPI
from services.telegram_bot import TelegramBot
from services.mattermost_notifier import MattermostNotifier


class BotLogic:
    def __init__(self):
        config = ConfigLoader.load_config()
        self.enabled_channels = config.get("enabled_channels", ["telegram"])
        self.helpshift = HelpshiftAPI(config)

        self.telegram = None
        if "telegram" in self.enabled_channels:
            self.telegram = TelegramBot(config)

        self.mattermost = None
        if "mattermost" in self.enabled_channels:
            self.mattermost = MattermostNotifier(config)

        self.tracked_apps = config['tracked_apps']
        self.tracked_app_ids = config.get('tracked_app_ids', {})
        self.alert_repeats = config.get('alert_repeats', 10)
        self.lookback_period = config.get('lookback_period', 3600)

    def run(self):
        start_time = time.time() - self.lookback_period
        finish_time = time.time()
        creation_since = time_to_str(start_time)
        creation_until = time_to_str(finish_time)

        messages = []

        for app_name, threshold in self.tracked_apps.items():
            total_hits, status = self.helpshift.send_request(creation_since, creation_until, app_name=app_name)
            total_hits = int(total_hits) if isinstance(total_hits, (int, float)) else 0
            messages.append(f"{total_hits} {app_name} ticket(s), request status: {status}")

            if total_hits > threshold:
                alert_message = f'ALARM!!! {app_name} has {total_hits} tickets'
                self.send_alert(alert_message)

        for app_id, threshold in self.tracked_app_ids.items():
            total_hits, status = self.helpshift.send_request(creation_since, creation_until, app_id=app_id)
            total_hits = int(total_hits) if isinstance(total_hits, (int, float)) else 0
            messages.append(f"{total_hits} tickets from Email, request status: {status}")

            if total_hits > threshold:
                alert_message = f'ALARM!!! Email has {total_hits} tickets'
                self.send_alert(alert_message)

        message_text = (
                f'From {unixtime_to_date(start_time)} to {unixtime_to_date(finish_time)} we got:\n'
                + "\n".join(messages)
        )

        self.send_report(message_text)

    def send_report(self, text):
        if self.telegram:
            self.telegram.send_message(self.telegram.chat_id, text)
        if self.mattermost:
            self.mattermost.send_message(text)

    def send_alert(self, text):
        for _ in range(self.alert_repeats):
            if self.telegram:
                self.telegram.send_message(self.telegram.alarm_chat_id, text)
            if self.mattermost:
                self.mattermost.send_message(text)
            time.sleep(5)