# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/serv-2.py
# Compiled at: 2019-03-14 22:19:25
# Size of source mod 2**32: 685 bytes
import tornado.ioloop, pyrestful.rest
from pyrestful import mediatypes
from pyrestful.rest import get, post

class EchoService(pyrestful.rest.RestHandler):

    @post('/echo', {'format': 'xml'}, _catch_fire=True)
    def sayHello(self, doc):
        return doc

    @get('/echo/{name}/v1?<age>', {'format': 'json'}, _catch_fire=True)
    def getData(self, name, age):
        return {'name':name, 
         'age':age}


if __name__ == '__main__':
    try:
        print('Start the echo service')
        app = pyrestful.rest.RestService([EchoService])
        app.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('\nStop the echo service')