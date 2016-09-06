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
        print('Room ' + str(room_id) + 'established.')
        rooms[room_id] = mc
        if request.form['use_id'] == 'true':
            player_id = int(request.form.get('player_id', -1, type=int))
            session['player_id'] = player_id
            mc.register(player_id)
        else:
            session['player_id'] = mc.register()
        return ''
    except Exception as e:
        print(e)
        # return 'error'
        raise e

def get_rooms():
    rooms = getattr(g, 'rooms', None)
    if rooms is None:
        rooms = g.rooms = {}
    return rooms 

@app.route('/join', methods=['POST'])
def join():
    try:
        session['name'] = request.form['name']
        rooms = get_rooms()
        room_id = int(request.form['room_id'])
        if room_id not in rooms:
            raise Exception()
        session['room_id'] = room_id
        mc = rooms[room_id]
        if request.form['use_id'] == 'true':
            player_id = int(request.form['player_id'])
            session['player_id'] = player_id
            mc.register(player_id)
        else:
            session['player_id'] = mc.register()
        return ''
    except Exception as e:
        print(e)
        # return 'error'
        raise e

@app.route('/game')
def game():
    return render_template('game.html', room_id = str(session.get('room_id', -1)))

@app.route('/exit', methods=['POST'])
def exit_game():
    session.pop('name', None)
    session.pop('room_id', None)
    session.pop('player_id', None)
    return ''

app.secret_key = appconfig.SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True)
