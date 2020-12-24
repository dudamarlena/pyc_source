# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hsync\server.py
# Compiled at: 2017-11-01 10:09:03
import argparse, json, os
from flask import Flask, request
from werkzeug.routing import BaseConverter
from .dir import ServerDir, File

def _parse_args_server():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=6688, help='http server bind port default: 6688')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.1')
    return parser.parse_args()


class RegexConverter(BaseConverter):

    def __init__(self, _map, *args):
        super(RegexConverter, self).__init__(_map)
        self.map = map
        self.regex = args[0]


def run():
    args = _parse_args_server()
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter

    @app.route('/<regex("([:\\/\\w-]+)*$"):root_path>', methods=['GET'])
    def get(root_path):
        root_path = '/' + root_path
        server_dir = ServerDir(root_path, (), ())
        return json.dumps([ i.__dict__ for i in server_dir.get_file_list() ])

    @app.route('/<regex("([:\\/\\w-]+)*$"):root_path>', methods=['POST'])
    def post(root_path):
        root_path = '/' + root_path
        os.chdir(root_path)
        f = File.from_json(json.dumps(request.form))
        file_body = request.files.get('file_body')
        f.write_file(file_body)
        return 'success!'

    app.run(host='0.0.0.0', debug=False, port=args.port)


if __name__ == '__main__':
    run()