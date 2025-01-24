import json
import os

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def save_config(config):
    with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=4)

def get_config_value(key):
    config = load_config()
    return config.get(key)

def set_config_value(key, value):
    config = load_config()
    config[key] = value
    save_config(config)