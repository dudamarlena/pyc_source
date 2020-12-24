# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/comzeradd/Projects/monopati/monopati/helpers.py
# Compiled at: 2020-03-16 13:47:31
# Size of source mod 2**32: 2103 bytes
import http.server, socketserver
from os import path, mkdir, listdir, makedirs, chdir
from shutil import copy2, copytree
import sys, yaml

def config():
    """
    Parse the configuration yaml file.
    """
    try:
        cfg = yaml.load((open('config.yml', 'r').read()), Loader=(yaml.BaseLoader))
    except IOError:
        print('No config.yml found. Copy config.yml-dist and edit it to fit your needs')
        sys.exit(0)

    try:
        output = cfg['output']
    except KeyError:
        cfg['output'] = '.'
        return cfg
    else:
        if output.endswith('/'):
            output = output[:-1]
        try:
            makedirs(output)
        except OSError:
            pass

        return cfg


def kickstart(folder):
    dest = path.abspath(folder)
    if not path.isdir(dest):
        mkdir(dest)
        print('Creating website folder...')
    else:
        print('Folder already exists')
        sys.exit()
    skel = path.join(path.dirname(path.abspath(__file__)), 'skel')
    for item in listdir(skel):
        s = path.join(skel, item)
        d = path.join(dest, item)
        if path.isdir(s):
            copytree(s, d)
        else:
            copy2(s, d)


def serve(port):
    cfg = config()
    Handler = http.server.SimpleHTTPRequestHandler
    chdir(cfg['output'])
    with socketserver.TCPServer(('', port), Handler) as (httpd):
        print('Serving at http://localhost:{0}'.format(port))
        httpd.serve_forever()