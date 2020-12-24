# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/l0/ss9rqt5j7xbg0x2bpvmjx_k40000gp/T/pip-install-n2xwwglt/workstation/workstation/server/manager.py
# Compiled at: 2019-09-24 08:15:55
# Size of source mod 2**32: 646 bytes
import flask
from flask_script import Manager
from main import app
manager = Manager(app)

@manager.command
def list_routes():
    import urllib.parse
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = '[{0}]'.format(arg)

        methods = ','.join(rule.methods)
        url = (flask.url_for)((rule.endpoint), **options)
        line = urllib.parse.unquote('{:50s} {:20s} {}'.format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == '__main__':
    manager.run()