# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\kram\kram\kram.py
# Compiled at: 2015-07-21 10:50:34
"""
Kram
"""
import requests, threading, server, webbrowser, json
EXPERIMENT_NAME = ''
run = 0
root = 'http://localhost:5000'

def init(name):
    """
    Initialize the experiment
    """
    global EXPERIMENT_NAME
    EXPERIMENT_NAME = name
    t = threading.Thread(target=server.run_server, args=())
    t.start()
    webbrowser.open(root)


def end():
    """
    Signals the end of experiment
    """
    end_data = {'x': 'end'}
    t = threading.Thread(target=requests.get, args=(
     root + '/push', {'data': json.dumps(end_data)}))
    t.start()


def shutdown():
    """
    Shutdown server
    """
    requests.get(root + '/stop')


class kram(object):
    """
    Decorator class
    """

    def __init__(self):
        """
        Initialize experiment and store
        """
        self.experiment = EXPERIMENT_NAME
        self.live = True

    def __call__(self, func):
        """
        Call function and log results
        """

        def krammed(*args, **kwargs):
            global run
            output = func(*args, **kwargs)
            data = {'in': args, 
               'out': output}
            if self.live:
                plot_data = {'x': run, 
                   'y': data['out'], 
                   'func': func.__name__, 
                   'title': EXPERIMENT_NAME}
                self.push(json.dumps(plot_data))
                run += 1

        return krammed

    def push(self, data):
        t = threading.Thread(target=requests.get, args=(
         root + '/push', {'data': data}))
        t.start()