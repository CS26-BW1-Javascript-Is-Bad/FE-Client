from core.domain.map import Map
from core.domain.room import Room
import core.util.constants as constants
import requests
import json

def make_get_request(url, headers=None):
    if headers != None:
        resp = requests.get(url=url, headers=headers)
    else:
        resp = requests.get(url)
    if resp.status_code != 200:
        pass
        # Error!
    else:
        return resp.content


def make_post_request(input_url, input_headers="", input_data=""):
    resp = requests.post(url=input_url, headers=input_headers, data=input_data)
    if resp.status_code != 200:
        return resp.status_code
    else:
        return resp.content


def room_from_id(id):
    ck = {'Authorization': f'Token {constants.TOKEN}'}
    return room_from_json(make_get_request(f'{constants.ROOM_BY_ID_URL}{id}', ck))


def room_from_json(input="", parsed_input=""):
    input_json = ""
    if parsed_input == "":
        input_json = json.loads(input)
    else:
        input_json = parsed_input
    return Room(input_json['asset'],
                input_json['n_to'],
                input_json['s_to'],
                input_json['e_to'],
                input_json['w_to'],
                input_json['x'],
                input_json['y'])


def login(username, password):
    ck = {'username': {username}, 'password': {password}}
    login_test = requests.post(constants.LOGIN_URL, ck)
    if login_test.status_code != 200:
        return None
    else:
        return json.loads(login_test.content)['key']


def register(username, password):
    ck = {'username': {username}, 'password1': {password}, 'password2' : {password}}
    register_test = requests.post(constants.REGISTER_URL, ck)
    if register_test.status_code != 201:
        return None
    else:
        constants.TOKEN = json.loads(register_test.content)['key']
        ck = {'Authorization': f'Token {constants.TOKEN}'}
        make_get_request(url='https://jibadventuregame.herokuapp.com/api/adv/init/', headers=ck)
        return json.loads(register_test.content)['key']


def room_to_json(room):
    return {'asset': room.asset,
            'n_to': room.n_to,
            's_to': room.s_to,
            'e_to': room.e_to,
            'w_to': room.w_to,
            'x': room.x,
            'y': room.y
            }


def map_from_json(input_raw):
    input_json = json.loads(input_raw)
    json_rooms = input_json['map']

    rooms = []
    for room in json_rooms:
        rooms.append(room_from_json(parsed_input=room))
    current_room = room_from_id(input_json['current_room'])
    return Map(rooms), current_room




def player_change_room(dir):
    # ck = {'Authorization': f'Token {Login_Token}'}
    # make_get_request('https://jibadventuregame.herokuapp.com/api/adv/init/', ck)
    ck = {'Authorization': f'Token {constants.TOKEN}', "Content-Type": "application/json"}
    request_data = ""
    if dir == 'w':
        request_data = '{"direction":"w"}'
    if dir == 'n':
        request_data = '{"direction":"n"}'
    if dir == 's':
        request_data = '{"direction":"s"}'
    if dir == 'e':
        request_data = '{"direction":"e"}'
    request = make_post_request(constants.MOVE_URL, ck, request_data)
    print(request)
