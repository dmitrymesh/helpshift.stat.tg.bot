import json

class ConfigLoader:
    _config = None

    @staticmethod
    def load_config(filename='config.json'):
        if ConfigLoader._config is None:
            with open(filename, 'r', encoding='utf-8') as file:
                ConfigLoader._config = json.load(file)
        return ConfigLoader._config