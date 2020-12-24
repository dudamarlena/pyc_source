# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: paxmusica/cli.py
# Compiled at: 2013-03-05 17:11:20
from controller import app
from player import play_it
import config

def serve():
    app.run(debug=True, use_reloader=False, port=config.port, host='')


def play():
    play_it()