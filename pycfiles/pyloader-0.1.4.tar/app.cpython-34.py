# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/lq/TornadoAJAXSample/app.py
# Compiled at: 2015-04-11 02:14:44
# Size of source mod 2**32: 2329 bytes
import logging, tornado.auth, tornado.escape, tornado.ioloop, tornado.options, tornado.web, os.path, uuid, json, pprint
from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
         (
          '/', MainHandler),
         (
          '/test/', TestHandler)]
        settings = dict(debug=True, template_path=os.path.join(os.path.dirname(__file__), 'templates'), static_path=os.path.join(os.path.dirname(__file__), 'static'))
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html', messages=None)


class TestHandler(tornado.web.RequestHandler):

    def get(self):
        example_response = {}
        example_response['name'] = 'example'
        example_response['width'] = 1020
        self.write(json.dumps(example_response))

    def post(self):
        jsonobj = json.loads(self.request.body)
        print('Post data received')
        for key in list(jsonobj.keys()):
            print('key: %s , value: %s' % (key, jsonobj[key]))

        response_to_send = {}
        response_to_send['newkey'] = jsonobj['key1']
        print('Response to return')
        pprint.pprint(response_to_send)
        self.write(json.dumps(response_to_send))


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()