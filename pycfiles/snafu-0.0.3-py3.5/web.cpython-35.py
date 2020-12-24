# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/connectors/web.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 879 bytes
import flask, threading, os, configparser
app = flask.Flask('snafu')
gcb = None

@app.route('/invoke/<function>')
def invoke(function):
    global gcb
    response = gcb(function)
    if not response:
        flask.abort(500)
    return response


def initinternal(function, configpath):
    connectconfig = None
    if not configpath:
        configpath = 'snafu.ini'
    if not function:
        function = 'snafu'
    if os.path.isfile(configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        if function in config and 'connector.web' in config[function]:
            connectconfig = int(config[function]['connector.web'])
    if connectconfig:
        app.run(host='0.0.0.0', port=connectconfig)


def init(cb, function=None, configpath=None):
    global gcb
    gcb = cb
    t = threading.Thread(target=initinternal, daemon=True, args=(function, configpath))
    t.start()