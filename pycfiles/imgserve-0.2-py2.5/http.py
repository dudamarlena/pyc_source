# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/imgserve/http.py
# Compiled at: 2009-08-22 09:16:17
"""
This file contains a http server that receives json request from
users, and code for json request parsing, quick nonblocking
validation, reply object creation.
"""
from __future__ import with_statement
import os, sys, time, uuid
from pprint import pprint
from cogen.web import wsgi
from cogen.common import *
from cogen.web.async import SynchronousInputMiddleware
from imgserve.utils import get_filename_parts_from_url, make_reply
from imgserve import version
if sys.version_info >= (2, 6):
    import json
else:
    import simplejson as json
OPS = ('rasterize', 'resize')
EXTENTIONS = {'rasterize': ('svg', ), 
   'resize': ('png', 'gif', 'jpg', 'jpeg')}
REQUIRED_ARGS = {'rasterize': {'width': int, 
                 'height': int}, 
   'resize': {'width': int, 
              'height': int}}
assert set(EXTENTIONS.keys()) == set(REQUIRED_ARGS.keys()) == set(OPS)
SRC_PREFIXES = ('http', 'ftp', 'file')
DST_PREFIXES = ('http', 'ftp', 'file')
EXTRA_ARGS = {'http': {'field_file': (
                         str, unicode)}, 
   'ftp': {}, 'file': {}}
assert set(EXTRA_ARGS.keys()) == set(DST_PREFIXES)

def quick_check(req):
    """
    Do basic nonblocking validation for request object, return a tuple
    where the first element is a boolean value that tells whether the
    request is valid, the second element is a error code if invalid,
    None if valid.

    See README for more description about request format
    specification.
    """
    if not set(req.keys()) == set(['operationType', 'args', 'srcURL', 'dstURL']):
        return (
         False, 101)
    op = req['operationType']
    if op not in OPS:
        return (
         False, 102)
    if not isinstance(req['args'], dict):
        return (
         False, 103)
    if not req['srcURL']:
        return (
         False, 104)
    if not req['dstURL']:
        return (
         False, 105)
    req_args = set(req['args'].keys())
    required_args = set(REQUIRED_ARGS[op].keys())
    if not required_args.issubset(req_args):
        return (
         False, 106)
    for arg in required_args:
        if not isinstance(req['args'][arg], REQUIRED_ARGS[op][arg]):
            return (
             False, 107)

    (src_basename, src_ext) = get_filename_parts_from_url(req['srcURL'])
    if src_ext.lower() not in EXTENTIONS[op]:
        return (
         False, 108)
    substitute_maps = (
     (
      '{$width}', str(req['args']['width'])),
     (
      '{$height}', str(req['args']['height'])),
     (
      '{$basename}', src_basename),
     (
      '{$ext}', src_ext))
    (prefix, sub_body) = req['dstURL'].rsplit(':', 1)
    for (token, value) in substitute_maps:
        sub_body = sub_body.replace(token, value)

    req['dstURL'] = prefix + ':' + sub_body
    src_prefix = req['srcURL'].split(':', 1)[0]
    dst_prefix = req['dstURL'].split(':', 1)[0]
    if src_prefix not in SRC_PREFIXES:
        return (
         False, 109)
    if dst_prefix not in DST_PREFIXES:
        return (
         False, 110)
    extra_args = set(EXTRA_ARGS[dst_prefix].keys())
    if not extra_args.issubset(req_args):
        return (
         False, 111)
    for arg in extra_args:
        if isinstance(EXTRA_ARGS[dst_prefix], list):
            bool_list = (map(lambda x: isinstance(req['args'][arg], x), EXTRA_ARGS[dst_prefix]),)
            correct = reduce(lambda (x, y): x and y, bool_list)
        else:
            correct = isinstance(req['args'][arg], EXTRA_ARGS[dst_prefix][arg])
        if not correct:
            return (
             False, 112)

    (dst_basename, dst_ext) = get_filename_parts_from_url(req['dstURL'])
    compare_target = {'rasterize': 'png', 'resize': src_ext}
    if dst_ext.lower() != compare_target[op]:
        return (
         False, 113)
    return (True, None)


def load_json(environ):
    """
    Convert a WSGI environ of json request to a python dict.
    """
    entity = environ['wsgi.input'].read()
    if not entity:
        return
    try:
        req = json.loads(entity)
    except:
        return
    else:
        return req

    return


def reply_json(start_response, reply):
    """
    Make a json reply that is used by our tiny WSGI application.
    """
    body = json.dumps(reply)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [body]


def get_worker_reply(i_queue, o_queue, req):
    """
    Dispatch request to worker process, and get the result back.
    """
    req_id = uuid.uuid1()
    i_queue.put((req_id, req))
    temp_buf = []
    sleep = 0.5
    while True:
        reply = o_queue.get()
        if reply[0] == req_id:
            break
        temp_buf.append(reply)
        time.sleep(sleep)
        sleep *= 2

    if temp_buf:
        for reply in temp_buf:
            o_queue.put(reply)

    return reply[1]


def httpserv(host, port, i_queue, o_queue):
    """
    Start the http server.
    """

    @SynchronousInputMiddleware
    def http_handler(environ, start_response):
        """
        WSGI request handler that do othe real work of receiving json
        request from users.
        """
        if environ['REQUEST_METHOD'] != 'POST':
            start_response('404 OK', [('Content-Type', 'text/html')])
            return [
             '404 Not Found - %s %s' % (
              version.NAME, version.VERSION['version'])]
        print 'Got a request from %s, %s' % (environ['REMOTE_ADDR'],
         environ['HTTP_USER_AGENT'])
        req = load_json(environ)
        if not req:
            return reply_json(start_response, make_reply('parse'))
        pprint(req)
        (valid, data) = quick_check(req)
        if not valid:
            error_code = data
            return reply_json(start_response, make_reply('invalid', error_code))
        print 'Passing the request to a worker process'
        reply = get_worker_reply(i_queue, o_queue, req)
        return reply_json(start_response, reply)

    m = Scheduler()
    server = wsgi.WSGIServer((host, port), http_handler, m)
    m.add(server.serve)
    try:
        m.run()
    except (KeyboardInterrupt, SystemExit):
        return