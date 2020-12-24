# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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