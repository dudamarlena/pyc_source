# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/status_handler.py
# Compiled at: 2019-04-05 15:23:31
# Size of source mod 2**32: 9705 bytes
VERSION_STRING = '$Id: status_handler.py,v 1.7 2003/12/24 16:08:16 akuchling Exp $'
import string, time, re
from cgi import escape
import asyncore_25 as asyncore, http_server, medusa_gif, producers
from counter import counter
START_TIME = long(time.time())

class status_extension:
    hit_counter = counter()

    def __init__(self, objects, statusdir='/status', allow_emergency_debug=0):
        self.objects = objects
        self.statusdir = statusdir
        self.allow_emergency_debug = allow_emergency_debug
        self.hyper_regex = re.compile('/status/object/([0-9]+)/.*')
        self.hyper_objects = []
        for object in objects:
            self.register_hyper_object(object)

    def __repr__(self):
        return '<Status Extension (%s hits) at %x>' % (
         self.hit_counter,
         id(self))

    def match(self, request):
        path, params, query, fragment = request.split_uri()
        return path[:len(self.statusdir)] == self.statusdir or path[:len('/status/object/')] == '/status/object/'

    def handle_request(self, request):
        path, params, query, fragment = request.split_uri()
        self.hit_counter.increment()
        if path == self.statusdir:
            up_time = ''.join(english_time(long(time.time()) - START_TIME))
            request['Content-Type'] = 'text/html'
            request.push('<html><title>Medusa Status Reports</title><body bgcolor="#ffffff"><h1>Medusa Status Reports</h1><b>Up:</b> %s' % up_time)
            for i in range(len(self.objects)):
                try:
                    request.push(self.objects[i].status())
                except:
                    import traceback, StringIO
                    stream = StringIO.StringIO()
                    traceback.print_exc(None, stream)
                    request.push('<h2><font color="red">Error in Channel %3d: %s</font><pre>%s</pre>' % (i, escape(repr(self.objects[i])), escape(stream.getvalue())))
                else:
                    request.push('<hr>\r\n')
            else:
                request.push('<p><a href="%s/channel_list">Channel List</a><hr><img src="%s/medusa.gif" align=right width=%d height=%d></body></html>' % (
                 self.statusdir,
                 self.statusdir,
                 medusa_gif.width,
                 medusa_gif.height))
                request.done()

        else:
            if path == self.statusdir + '/channel_list':
                request['Content-Type'] = 'text/html'
                request.push('<html><body>')
                request.push(channel_list_producer(self.statusdir))
                request.push('<hr><img src="%s/medusa.gif" align=right width=%d height=%d>' % (
                 self.statusdir,
                 medusa_gif.width,
                 medusa_gif.height) + '</body></html>')
                request.done()
            else:
                if path == self.statusdir + '/medusa.gif':
                    request['Content-Type'] = 'image/gif'
                    request['Content-Length'] = len(medusa_gif.data)
                    request.push(medusa_gif.data)
                    request.done()
                else:
                    if path == self.statusdir + '/close_zombies':
                        message = '<h2>Closing all zombie http client connections...</h2><p><a href="%s">Back to the status page</a>' % self.statusdir
                        request['Content-Type'] = 'text/html'
                        request['Content-Length'] = len(message)
                        request.push(message)
                        now = int(time.time())
                        for channel in asyncore.socket_map.keys():
                            if channel.__class__ == http_server.http_channel and channel != request.channel and now - channel.creation_time > channel.zombie_timeout:
                                channel.close()
                        else:
                            request.done()

                    else:
                        if self.allow_emergency_debug and path == self.statusdir + '/emergency_debug':
                            request.push('<html>Moving All Servers...</html>')
                            request.done()
                            for channel in asyncore.socket_map.keys():
                                if channel.accepting and type(channel.addr) is type(()):
                                    ip, port = channel.addr
                                    channel.socket.close()
                                    channel.del_channel()
                                    channel.addr = (ip, port + 10000)
                                    fam, typ = channel.family_and_type
                                    channel.create_socket(fam, typ)
                                    channel.set_reuse_addr()
                                    channel.bind(channel.addr)
                                    channel.listen(5)

                        else:
                            m = self.hyper_regex.match(path)
                            if m:
                                oid = int(m.group(1))
                                for object in self.hyper_objects:
                                    if id(object) == oid and hasattr(object, 'hyper_respond'):
                                        object.hyper_respond(self, path, request)

                            else:
                                request.error(404)
                                return

    def status(self):
        return producers.simple_producer('<li>Status Extension <b>Hits</b> : %s' % self.hit_counter)

    def register_hyper_object(self, object):
        if object not in self.hyper_objects:
            self.hyper_objects.append(object)


import logger

class logger_for_status(logger.tail_logger):

    def status(self):
        return 'Last %d log entries for: %s' % (
         len(self.messages),
         html_repr(self))

    def hyper_respond(self, sh, path, request):
        request['Content-Type'] = 'text/plain'
        messages = self.messages[:]
        messages.reverse()
        request.push(lines_producer(messages))
        request.done()


class lines_producer:

    def __init__(self, lines):
        self.lines = lines

    def more(self):
        if self.lines:
            chunk = self.lines[:50]
            self.lines = self.lines[50:]
            return '\r\n'.join(chunk) + '\r\n'
        return ''


class channel_list_producer(lines_producer):

    def __init__(self, statusdir):
        channel_reprs = map(lambda x: '&lt;' + repr(x)[1:-1] + '&gt;', asyncore.socket_map.values())
        channel_reprs.sort()
        lines_producer.__init__(self, [
         '<h1>Active Channel List</h1>',
         '<pre>'] + channel_reprs + [
         '</pre>',
         '<p><a href="%s">Status Report</a>' % statusdir])


def html_repr(object):
    so = escape(repr(object))
    if hasattr(object, 'hyper_respond'):
        return '<a href="/status/object/%d/">%s</a>' % (id(object), so)
    return so


def html_reprs(list, front='', back=''):
    reprs = map(lambda x, f=front, b=back: '%s%s%s' % (f, x, b), map(lambda x: escape(html_repr(x)), list))
    reprs.sort()
    return reprs


def progressive_divide(n, parts):
    result = []
    for part in parts:
        n, rem = divmod(n, part)
        result.append(rem)
    else:
        result.append(n)
        return result


def split_by_units(n, units, dividers, format_string):
    divs = progressive_divide(n, dividers)
    result = []
    for i in range(len(units)):
        if divs[i]:
            result.append(format_string % (divs[i], units[i]))
        result.reverse()
        if not result:
            return [
             format_string % (0, units[0])]
        return result


def english_bytes(n):
    return split_by_units(n, ('', 'K', 'M', 'G', 'T'), (1024, 1024, 1024, 1024, 1024), '%d %sB')


def english_time(n):
    return split_by_units(n, ('secs', 'mins', 'hours', 'days', 'weeks', 'years'), (60,
                                                                                   60,
                                                                                   24,
                                                                                   7,
                                                                                   52), '%d %s')