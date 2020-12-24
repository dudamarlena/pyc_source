# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jsonstore/run.py
# Compiled at: 2013-02-28 11:07:21
"""Usage: jsonstore [options] 

Options:
  -h --help                 Show this help message and exit
  -i IP --ip=IP             The ip to listen to [default: 127.0.0.1]
  -p PORT --port=PORT       The port to connect [default: 31415]
  -d FILE --database=FILE   Database file [default: index.db]

"""

def main():
    from docopt import docopt
    from jsonstore.rest import JSONStore
    from werkzeug.serving import run_simple
    arguments = docopt(__doc__)
    app = JSONStore(arguments['--database'])
    run_simple(arguments['--ip'], int(arguments['--port']), app)


if __name__ == '__main__':
    main()