# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/demos/books_service.py
# Compiled at: 2019-03-04 21:32:08
# Size of source mod 2**32: 2174 bytes
import tornado.ioloop, pyrestful.rest
from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete

class Book(object):
    isbn = int
    title = str


class BookResource(pyrestful.rest.RestHandler):

    @get(_path='/books/json/{isbn}', _types=[int], _produces=(mediatypes.APPLICATION_JSON))
    def getBookJSON(self, isbn):
        book = Book()
        book.isbn = isbn
        book.title = 'My book for isbn ' + str(isbn)
        return book

    @get(_path='/books/xml/{isbn}', _types=[int], _produces=(mediatypes.APPLICATION_XML))
    def getBookXML(self, isbn):
        book = Book()
        book.isbn = isbn
        book.title = 'My book for isbn ' + str(isbn)
        return book

    @post(_path='/books/xml', _types=[Book], _consumes=(mediatypes.APPLICATION_XML), _produces=(mediatypes.APPLICATION_XML))
    def postBookXML(self, book):
        """ this is an echo...returns the same xml document """
        return book

    @post(_path='/books/json', _types=[Book], _consumes=(mediatypes.APPLICATION_JSON), _produces=(mediatypes.APPLICATION_JSON))
    def postBookJSON(self, book):
        """ this is an echo...returns the same json document """
        return book

    @post(_path='/books', _types=[Book])
    def postBook(self, book):
        """ this is an echo, returns json or xml depending of request content-type """
        return book


if __name__ == '__main__':
    try:
        print('Start the service')
        app = pyrestful.rest.RestService([BookResource])
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('\nStop the service')