# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tprofile/test_server.py
# Compiled at: 2015-05-25 02:14:29
import sys, time, tornado.web, tornado.ioloop
from tprofile import ProfileMeta

def condition(self):
    if self.get_argument('profile', None) == '2':
        return True
    else:
        return False


ProfileMeta.set_condition(condition)

class BaseHandler(tornado.web.RequestHandler):
    """this is base class of all handlers"""
    __metaclass__ = ProfileMeta

    def prepare(self):
        self.write('this is prepare.\n')


class MainHandler(BaseHandler):

    def block(self, n):
        time.sleep(n)

    def get(self):
        self.block(1)
        self.write('this is get.\n')
        self.block(0.8)
        self._write_buffer.append('end.\n')


app = tornado.web.Application([
 (
  '/test/profile', MainHandler)])

def main():
    port = 9876
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()