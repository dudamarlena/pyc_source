# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/eventsource/request.py
# Compiled at: 2013-05-23 13:18:59
import sys, argparse, json, urllib2

def send_json(url, data):
    """
    Sends a JSON query to eventsource's URL

    :param url: string url to send to
    :param data: string data to send to given URL
    """
    if isinstance(data, basestring):
        data = json.dumps(json.loads(data))
    else:
        data = json.dumps(data)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    try:
        response = f.read()
        return response
    finally:
        f.close()


def send_string(url, data):
    """
    Sends a string query to eventsource's URL

    :param url: string url to send to
    :param data: string data to send to given URL
    """
    f = urllib2.urlopen(url, data)
    try:
        response = f.read()
        return response
    finally:
        f.close()


def start():
    """helper method to create a commandline utility"""
    parser = argparse.ArgumentParser(prog=sys.argv[0], description='Generates event for Event Source Library')
    parser.add_argument('token', help='Token to be used for connection')
    parser.add_argument('action', help='Action to send')
    parser.add_argument('data', nargs='?', default='', help='Data to be sent')
    parser.add_argument('-H', '--host', dest='host', default='127.0.0.1', help='Host to connect to')
    parser.add_argument('-P', '--port', dest='port', default='8888', help='Port to be used connection')
    parser.add_argument('-j', '--json', dest='json', action='store_true', help='Treat data as JSON')
    args = parser.parse_args(sys.argv[1:])
    try:
        if args.json:
            print send_json('http://%(host)s:%(port)s/%(action)s/%(token)s' % args.__dict__, args.data)
        else:
            print send_string('http://%(host)s:%(port)s/%(action)s/%(token)s' % args.__dict__, args.data)
        sys.exit(0)
    except Exception, err:
        print 'Unable to send request (%s): %s' % (err, err.readline().split('<body>')[(-1)].split('</body>')[0])
        sys.exit(1)


if __name__ == '__main__':
    start()