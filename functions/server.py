import json
import os


def get_server(server):
    path = os.path.abspath(r"servers/" + server.id + ".json")

    if os.path.exists(path):
        return json.load(open(path))

    return edit_server(server)


def edit_server(server, server_setting=None):
    path = os.path.abspath(r"servers/" + server.id + ".json")

    if server_setting is None:
        server_setting = {  # about server
            'id': server.id,
            'owner_id': server.owner.id,
            'configured': False,
            'sfw': False,
            'nsfw_channels': [],
            # fine tuning
            'favorites': False,
            'a_channel_id': None,
            'f_channel_id': None,
            'n_channel_id': None,
            'r34_channel_id': None}

    json_servers = open(path, 'w')
    json.dump(server_setting, json_servers, indent=4)
    json_servers.close()
    return server_setting


def remove_server(server):
    path = os.path.abspath(r"servers/" + server.id + ".json")

    os.remove(path)


if __name__ == '__main__':
    pass
