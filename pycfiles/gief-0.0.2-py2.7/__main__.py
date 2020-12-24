# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gief/__main__.py
# Compiled at: 2015-12-22 12:01:12
import argparse, os
from .gief import __doc__, app
parser = argparse.ArgumentParser(prog='gief', description=__doc__)
parser.add_argument('path', nargs='?', default=os.getcwd(), help='Folder where files will be uploaded to (CWD by default)')
parser.add_argument('-H', '--host', default='0.0.0.0')
parser.add_argument('-p', '--port', type=int, default=5000)
args = parser.parse_args()
app.config['path'] = args.path
app.run(args.host, args.port)