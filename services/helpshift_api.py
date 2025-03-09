import json
import requests


class HelpshiftAPI:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {api_key}'
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
            return None, f"Error: {err}"
