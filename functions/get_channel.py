import requests
import json


def get_channel(client_token, channel_id):
    header = {'Authorization': 'Bot ' + client_token}
    return json.loads(requests.get('https://discordapp.com/api/channels/' + channel_id, headers=header).content)
