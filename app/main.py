#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, session, g, render_template, json

from machine import MachineControl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_profile', methods=['Post'])
def set_profile():
    pass

@app.route('/start_new')
def start_new():
    pass

@app.route('/join')
def join():
    pass



if __name__ == '__main__':
    app.run()

