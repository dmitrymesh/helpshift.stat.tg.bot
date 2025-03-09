import requests

class TelegramBot:
    def __init__(self, config):
        self.api_url = f'https://api.telegram.org/{config["telegram_bot_token"]}/sendMessage'
        self.chat_id = config["telegram_chat_id"]
        self.alarm_chat_id = config["telegram_alarm_chat_id"]

    def send_message(self, chat_id, text):
        payload = {'chat_id': chat_id, 'text': text}
        try:
            requests.get(self.api_url, params=payload).raise_for_status()
        except requests.exceptions.RequestException as err:
            print("Telegram Error:", err)
