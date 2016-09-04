#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, session, render_template, json

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world!"

if __name__ == '__main__':
    app.run()

