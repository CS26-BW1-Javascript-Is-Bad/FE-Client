from core.data.remote_data_source import *
import core.util.constants as constants


def get_room_by_id(id):
    return room_from_json(make_get_request(id))


def get_map():
    ck = {'Authorization': f'Token {constants.TOKEN}'}
    return map_from_json(make_get_request(f'{constants.MAP_URL}', ck))

