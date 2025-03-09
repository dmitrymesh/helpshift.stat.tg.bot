import requests

class TelegramBot:
    def __init__(self, bot_token):
        self.api_url = f'https://api.telegram.org/{bot_token}/sendMessage'

    def send_message(self, chat_id, text):
        payload = {'chat_id': chat_id, 'text': text}
        try:
            requests.get(self.api_url, params=payload).raise_for_status()
        except requests.exceptions.RequestException as err:
            print("Telegram Error:", err)
