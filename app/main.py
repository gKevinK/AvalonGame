#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

from flask import Flask, request, session, g, render_template, json

from machine import MachineControl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_profile', methods=['POST'])
def set_profile():
    pass

@app.route('/start_new', methods=['POST'])
def start_new():
    rooms = get_rooms()
    room_num = random.randrange(0, 9999)
    while rooms.has_key(room_num):
        room_num = random.randrange(0, 9999)
    jsonObj = request.get_json()
    num = jsonObj['player_num']
    rooms[room_num] = MachineControl(num)

def get_rooms():
    rooms = getattr(g, 'rooms', None)
    if rooms is None:
        rooms = g.rooms = {}
    return rooms 

@app.route('/join', methods=['POST'])
def join():
    pass


if __name__ == '__main__':
    app.run(debug=True)

