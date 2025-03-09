import requests


class MattermostNotifier:
    def __init__(self, config):
        self.webhook_url = config.get("mattermost_webhook_url")

    def send_message(self, text):
        if not self.webhook_url:
            print("Mattermost webhook URL is not set.")
            return

        payload = {"text": text}

        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print("Mattermost Error:", err)
