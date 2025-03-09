import json
import requests


class HelpshiftAPI:
    def __init__(self, config):
        self.api_url = config['helpshift_api_url']
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {config["helpshift_api_key"]}'
        }

    def send_request(self, creation_since, creation_until, app_name=None, app_id=None):
        payload = {
            'created-since': str(creation_since),
            'created-until': str(creation_until)
        }

        if app_name:
            payload['custom_fields'] = json.dumps({
                "dropdown": {
                    "and": {
                        "application": {
                            "is_set": True,
                            "is": app_name
                        }
                    }
                }
            })
        elif app_id:
            payload['app-ids'] = json.dumps([app_id])

        try:
            response = requests.get(self.api_url, headers=self.headers, params=payload)
            response.raise_for_status()
            return response.json().get('total-hits', 0), "Success"
        except requests.exceptions.RequestException as err:
            print(f"Helpshift API Error: {err}")
            return 0, f"Error: {err}"
