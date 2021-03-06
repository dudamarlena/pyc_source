# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/column/api/run.py
# Compiled at: 2017-08-02 01:06:09
import logging, os, flask, flask_restful
from column.api.controller import credential_controller
from column.api.controller import run_controller
from column import cfg
application = flask.Flask(__name__)
api = flask_restful.Api(application)
api.add_resource(run_controller.Run, '/runs/<id>')
api.add_resource(run_controller.RunList, '/runs')
api.add_resource(credential_controller.Credential, '/credentials')
LOG_FILE = cfg.get('DEFAULT', 'log_file')
LOG_LEVEL = cfg.get('DEFAULT', 'log_level')
if os.access(LOG_FILE, os.W_OK):
    logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(levelname)s %(name)s %(message)s', level=LOG_LEVEL)
else:
    print 'Unable to log to the file: %s' % LOG_FILE
SERVER = cfg.get('DEFAULT', 'server')
PORT = cfg.getint('DEFAULT', 'port')
if __name__ == '__main__':
    application.run(host=SERVER, port=PORT)