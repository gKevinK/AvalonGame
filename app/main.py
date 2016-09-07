#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import queue
from flask import Flask, request, session, render_template, json, redirect

from machine import MachineControl
import appconfig

app = Flask(__name__)
app.rooms = {}

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
        mc = MachineControl(player_num)
        print('Room ' + str(room_id) + ' established.')
        rooms[room_id] = mc
        if request.form['use_id'] == 'true':
            player_id = int(request.form['player_id'])
            if player_id == -1:
                return 'Player_id invalid.'
            session['player_id'] = player_id
            mc.register(player_id)
        else:
            session['player_id'] = mc.register()
        print('Room ' + str(room_id) + ', Player ' + str(session['player_id'])
            + ', ' + session['name'] + ' joined.')
        session['room_id'] = room_id
        return ''
    except Exception as e:
        print(e)
        return 'error'
        # raise e

def get_rooms():
    rooms = getattr(app, 'rooms', None)
    if rooms is None:
        rooms = app.rooms = {}
    return rooms

@app.route('/join', methods=['POST'])
def join():
    try:
        session['name'] = request.form['name']
        rooms = get_rooms()
        room_id = int(request.form['room_id'])
        if room_id not in rooms:
            return 'This room don\'t exist.'
        mc = rooms[room_id]
        if request.form['use_id'] == 'true':
            player_id = int(request.form['player_id'])
            if player_id == -1:
                return 'Player id invalid.'
            session['player_id'] = player_id
            mc.register(player_id)
        else:
            session['player_id'] = mc.register()
        print('Room ' + str(room_id) + ', Player ' + str(session['player_id'])
            + ', ' + session['name'] + ' joined.')
        session['room_id'] = room_id
        return ''
    except Exception as e:
        print(e)
        return 'error'
        # raise e

@app.route('/game')
def game():
    if session.get('room_id', None) is None:
        return redirect('/')
    if session['room_id'] not in get_rooms():
        session.pop('room_id')
        return redirect('/')
    return render_template('game.html', room_id = str(session.get('room_id', -1)))

@app.route('/game/init')
def game_init():
    print(len(get_rooms()))
    room = get_rooms()[session['room_id']]
    player_id = session['player_id']
    message = room.get_init_info(player_id)
    message['player_id'] = player_id
    return json.jsonify(message)

@app.route('/game/comet')
def game_comet():
    room = get_rooms()[session['room_id']]
    mqueue = room.get_mq(session['player_id'])
    try:
        m = mqueue.get(timeout=appconfig.COMET_TIMEOUT)
        return m if isinstance(m, str) else json.jsonify(m)
    except queue.Empty:
        return ''
    # for i in range(appconfig.COMET_TIMEOUT):
    #     if not mqueue.empty():
    #         m = mqueue.get_nowait()
    #         return m if isinstance(m, str) else json.jsonify(m)
    #     time.sleep(appconfig.COMET_POLL_TIME)
    # return ''

@app.route('/game/action', methods=['POST'])
def game_action():
    if request.form['action'] == 'message':
        room = get_rooms()[session['room_id']]
        room.message(request.form['content'])
    return ''

@app.route('/exit', methods=['POST'])
def exit_game():
    room_id = session['room_id']
    room = get_rooms().get(room_id, None)
    if room is None:
        pass
    else:
        room.unregister(session['player_id'])

    session.pop('name', None)
    session.pop('room_id', None)
    session.pop('player_id', None)
    return ''

app.secret_key = appconfig.SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
