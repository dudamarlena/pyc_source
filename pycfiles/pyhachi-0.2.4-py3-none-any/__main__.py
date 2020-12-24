# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyhacc/http/__main__.py
# Compiled at: 2013-09-08 13:48:31
from .serve import app
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyHacc http view')
    parser.add_argument('--conn', type=str, default='sqlite://', help='connection string sqlalchemy style')
    args = parser.parse_args()
    app.conn = args.conn
    app.run(host='0.0.0.0', debug=True)