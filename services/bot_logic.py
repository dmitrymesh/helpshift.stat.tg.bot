import time
from helpers.config_loader import ConfigLoader
from helpers.time_utils import time_to_str, unixtime_to_date
from services.helpshift_api import HelpshiftAPI
from services.telegram_bot import TelegramBot


class BotLogic:
    def __init__(self, config_file='config.json'):
        config = ConfigLoader.load_config(config_file)
        self.helpshift = HelpshiftAPI(config['helpshift_api_url'], config['helpshift_api_key'])
        self.telegram = TelegramBot(config['telegram_bot_token'])
        self.chat_id = config['telegram_chat_id']
        self.alarm_chat_id = config['telegram_alarm_chat_id']
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
            messages.append(f"{total_hits} {app_name} ticket(s), request status: {status}")

            if total_hits > threshold:
                alert_message = f'ALARM!!! {app_name} has {total_hits} tickets'
                for _ in range(self.alert_repeats):
                    self.telegram.send_message(self.alarm_chat_id, alert_message)
                    time.sleep(5)

        for app_id, threshold in self.tracked_app_ids.items():
            total_hits, status = self.helpshift.send_request(creation_since, creation_until, app_id=app_id)
            messages.append(f"{total_hits} tickets for email, request status: {status}")

            if total_hits > threshold:
                alert_message = f'ALARM!!! Email has {total_hits} ticket(s)'
                for _ in range(self.alert_repeats):
                    self.telegram.send_message(self.alarm_chat_id, alert_message)
                    time.sleep(5)

        message_text = (
                f'From {unixtime_to_date(start_time)} to {unixtime_to_date(finish_time)} we got:\n'
                + "\n".join(messages)
        )
        self.telegram.send_message(self.chat_id, message_text)
