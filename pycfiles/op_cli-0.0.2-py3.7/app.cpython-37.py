# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/op_cli/functions/app.py
# Compiled at: 2019-12-13 10:06:51
# Size of source mod 2**32: 1730 bytes
import sys, requests

class CLI:

    def __init__(self):
        self.func_map = {}

    def register(self, name=None):

        def func_wrapper(func):
            _name = name if name else func.__name__
            self.func_map[_name] = func
            return func

        return func_wrapper

    def call_command(self):
        command = sys.argv[1]
        command = self.call_registered(command)
        return command

    def run_command(self, command):
        try:
            res = eval(command, self.func_map)
        except NameError as e:
            try:
                print('No such command is found: {} '.format(str(e)))
                return
            finally:
                e = None
                del e

        except SyntaxError as e:
            try:
                print('Command SyntaxError: {} '.format(str(e)))
                return
            finally:
                e = None
                del e

        return res

    def get_command(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            print('No such command is found: {} '.format(str(e)))
        return func


app = CLI()

@app.register()
def add(x, y):
    """Add values"""
    return x + y


@app.register()
def minus(x, y):
    return x - y


@app.register()
def grte(x, y):
    return x > y


@app.register()
def lste(x, y):
    return x < y


@app.register()
def pretify(json):
    return json.keys()


@app.register()
def jobs(q):
    url = f"https://indreed.herokuapp.com/api/jobs/?q={q}"
    req = requests.get(url)
    if req.status_code == 200:
        return req.json()


@app.register()
def rand(min=100, max=1000):
    """
    rand()
    """
    url = f"https://jvnyl60l6b.execute-api.eu-west-2.amazonaws.com/prod/add-number-generator?min={min}&max={max}"
    req = requests.get(url)
    return int(req.content.decode('utf-8'))