#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

from flask import Flask, request, session, g, render_template, redirect

from machine import MachineControl
import appconfig

app = Flask(__name__)

@app.route('/')
def index():
    if session.get('room_id'):
        return redirect('/game')
    return render_template('index.html')

@app.route('/start_new', methods=['POST'])
def start_new():
    try:
        session['name'] = request.form['name']
        rooms = get_rooms()
        room_id = random.randrange(1000, 9999)
        while room_id in rooms:
            room_id = random.randrange(1000, 9999)
        player_num = int(request.form['player_num'])
        session['room_id'] = room_id
        mc = MachineControl(player_num)
        rooms[room_id] = mc
        if request.form['use_id'] == 'true':
            player_id = int(request.form['player_id'])
            session['player_id'] = player_id
            mc.use_id(player_id)
        else:
            session['player_id'] = mc.register()
        return redirect('/game')
    except Exception:
        return 'error'

def get_rooms():
    rooms = getattr(g, 'rooms', None)
    if rooms is None:
        rooms = g.rooms = {}
    return rooms 

@app.route('/join', methods=['POST'])
def join():
    pass

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/exit', methods=['POST'])
def exit_game():
    session.pop('name', None)
    session.pop('room_id', None)
    session.pop('player_id', None)
    return ''

app.secret_key = appconfig.SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True)
