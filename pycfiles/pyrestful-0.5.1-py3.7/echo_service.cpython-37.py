# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/demos/echo_service.py
# Compiled at: 2019-03-02 23:45:23
# Size of source mod 2**32: 581 bytes
import tornado.ioloop, pyrestful.rest
from pyrestful import mediatypes
from pyrestful.rest import get

class EchoService(pyrestful.rest.RestHandler):

    @get(_path='/echo/{name}', _produces=(mediatypes.APPLICATION_JSON))
    def sayHello(self, name):
        return {'Hello': name}


if __name__ == '__main__':
    try:
        print('Start the echo service')
        app = pyrestful.rest.RestService([EchoService])
        app.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('\nStop the echo service')