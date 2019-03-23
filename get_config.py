import json
import os


def get_config():
    if os.path.exists(os.path.abspath('config/config.json')):
        with open(os.path.abspath('config/config.json'), 'r') as f:
            config = json.load(f)
    else:
        with open(os.path.abspath('config/config.json'), 'w') as f:
            config = {
                'token': '',
                'owner_id': ''
            }
            json.dump(config, f)
        raise Exception('Needs config.json')

    return config
