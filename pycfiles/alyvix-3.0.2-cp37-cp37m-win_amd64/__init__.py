# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\AlyFlask2\views\__init__.py
# Compiled at: 2018-11-28 10:11:07
import os, time, hmac, json, shutil, datetime, mimetypes
from threading import Thread
from hashlib import sha1
from flask import Flask, request, redirect, make_response, render_template, current_app, Markup, g, send_file
from AlyFlask2 import app
import logging, urllib, time, re

@app.route('/table', methods=['GET', 'POST'])
def index():
    return render_template('table.html', variables={})


@app.route('/draw', methods=['GET', 'POST'])
def draw():
    return render_template('draw.html')


@app.route('/build_screen', methods=['GET', 'POST'])
def build_screen():
    return render_template('build_screen.html')