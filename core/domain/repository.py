from core.data.remote_data_source import *
from core.util.constants import *


def get_room_by_id(id):
    return room_from_json(make_get_request(id))


def get_map():
    ck = {'Authorization': f'Token {Login_Token}'}
    return map_from_json(make_get_request(f'{MAP_URL}', ck))


Login_Token = login()
