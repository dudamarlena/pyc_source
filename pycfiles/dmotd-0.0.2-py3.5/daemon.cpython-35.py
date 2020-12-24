# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmotd/daemon.py
# Compiled at: 2019-02-02 12:55:22
# Size of source mod 2**32: 1331 bytes
from flask import Flask, abort, jsonify, Response
from logging import getLogger, ERROR

class DMOTD(Flask):

    def __init__(self, path='/etc/motd'):
        super().__init__('dmotd_daemon')
        self.dmotd_path = path
        log = getLogger('werkzeug')
        log.disabled = True
        self.dmotd_routes()

    def dmotd_routes(self):

        @self.route('/raw', methods=['GET'])
        def raw():
            try:
                with open(self.dmotd_path, 'r') as (f):
                    contents = f.read()
            except FileNotFoundError:
                return Response('Error: not found.', mimetype='text/plain')

            return Response(contents, mimetype='text/plain')

        @self.route('/json', methods=['GET'])
        def json():
            try:
                with open(self.dmotd_path, 'r') as (f):
                    contents = f.read()
            except FileNotFoundError:
                return jsonify({'ok': False, 
                 'error-code': 404, 
                 'error-desc': 'Not Found.'})

            return jsonify({'ok': True, 
             'lines': contents})