#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

from flask import Flask, request, session, g, render_template, json

from machine import MachineControl

app = Flask(__name__)

@app.route('/')
def index():
    if session['name']:
        return render_template('game.html')
    return render_template('index.html')

@app.route('/start_new', methods=['POST'])
def start_new():
    session['name'] = request.form['name']
    if request.form['use_index']:
        session['index'] = int(request.form['index'])
    rooms = get_rooms()
    room_num = random.randrange(0, 9999)
    while room_num in rooms:
        room_num = random.randrange(0, 9999)
    num = int(request.form['player_num'])
    session['room_num'] = num
    rooms[room_num] = MachineControl(num)
    return ''

def get_rooms():
    rooms = getattr(g, 'rooms', None)
    if rooms is None:
        rooms = g.rooms = {}
    return rooms 

@app.route('/join', methods=['POST'])
def join():
    pass

app.secret_key = 'A0Zr98w46yt&56ujt357/,?RT'

if __name__ == '__main__':
    app.run(debug=True)
