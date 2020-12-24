# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/demos/person_service.py
# Compiled at: 2019-04-19 00:05:32
# Size of source mod 2**32: 1531 bytes
import tornado.ioloop, pyrestful.rest
from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete

class Person(object):
    idperson = int
    name = str


class PersonService(pyrestful.rest.RestHandler):

    @get('/person/{idperson}', {'format': 'json'})
    def getPerson(self, idperson):
        p = Person()
        p.idperson = int(idperson)
        p.name = 'Mr.Robot'
        return p

    @post('/person', {'format': 'json'}, _catch_fire=True)
    def postPerson(self, person):
        return {'status':'person OK',  'person':person}


if __name__ == '__main__':
    try:
        print('Start the service')
        app = pyrestful.rest.RestService([PersonService])
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('\nStop the service')