import pygame as pg
import pytmx
import requests
import json

from core.domain.map import Map
from core.util.constants import *
import os.path as path

from core.util.settings import tilemap_folder


def make_get_request(url, headers=None):
    if headers != None:
        resp = requests.get(url, headers)
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
    ck = {'Authorization': f'token {Login_Token}'}
    return room_from_json(make_get_request(f'{ROOM_BY_ID_URL}{id}', ck))


def room_from_json(input):
    input_json = json.loads(input)

    return Room(input_json['asset'],
                input_json['n_to'],
                input_json['s_to'],
                input_json['e_to'],
                input_json['w_to'],
                input_json['x'],
                input_json['y'])


def login():
    ck = {'username': 'newtyler1', 'password': 'newtyler1'}
    test = requests.post('https://jibadventuregame.herokuapp.com/api/login/', ck)
    return json.loads(test.content)['key']


Login_Token = login()


def room_to_json(room):
    return {'asset': room.asset,
            'n_to': room.n_to,
            's_to': room.s_to,
            'e_to': room.e_to,
            'w_to': room.w_to,
            'x': room.x,
            'y': room.y
            }


def map_from_json(input):
    input_json = json.loads(input)

    return Map(input_json['asset'], room_from_json(input_json['current_room']))


def get_room_by_id(id):
    return room_from_json(make_get_request(id))


def get_map():
    ck = {'Authorization': f'token {Login_Token}'}
    return room_from_json(make_get_request(f'{MAP_URL}', ck))


class Room():
    def __init__(self, asset="", n_to=None, s_to=None, e_to=None, w_to=None, x=None, y=None, visited=None):
        self.asset = path.join(tilemap_folder, asset)
        self.n_to = n_to
        self.s_to = s_to
        self.e_to = e_to
        self.w_to = w_to
        self.x = x
        self.y = y
        self.visited = visited

    def get_coordinates(self):
        return (self.x, self.y)

    def init(self):
        tm = pytmx.load_pygame(self.asset, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledImageLayer):
                surface.blit(layer.image, (-5, 0))
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


def player_change_room(dir):
    # ck = {'Authorization': f'Token {Login_Token}'}
    # make_get_request('https://jibadventuregame.herokuapp.com/api/adv/init/', ck)
    ck = {'Authorization': f'Token {Login_Token}', "Content-Type": "application/json"}
    request_data = ""
    if dir == 'w':
        request_data = '{"direction":"w"}'
    if dir == 'n':
        request_data = '{"direction":"n"}'
    if dir == 's':
        request_data = '{"direction":"s"}'
    if dir == 'e':
        request_data = '{"direction":"e"}'
    request = make_post_request(MOVE_URL, ck, request_data)
    print(request)
