# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/unno/.pyenv/versions/2.7.8/lib/python2.7/site-packages/mrepserver/server.py
# Compiled at: 2014-10-10 01:45:07
import argparse, json, os, traceback, tornado.ioloop, tornado.web, mrep.builder as builder, mrep.morph as morph, mrep.pattern as pattern

class Database(object):

    def __init__(self, sentences):
        parser = morph.MeCabParser()
        data = []
        for s in sentences:
            data.append({'original': s, 
               'morphemes': parser.parse(s)})

        self.data = data

    def find(self, pat):
        matcher = builder.parse(pat.encode('utf-8'))
        results = []
        for datum in self.data:
            ms = datum['morphemes']
            result = pattern.find(ms, matcher)
            if len(result) > 0:
                results.append({'original': datum['original'], 
                   'result': result})

        return results


class TopHandler(tornado.web.RequestHandler):

    def initialize(self, db):
        self.db = db

    def get(self):
        self.render('find.html', results=None, pat='', error=None, trace=None)
        return


class FindHandler(tornado.web.RequestHandler):

    def initialize(self, db):
        self.db = db

    def get(self):
        pat = self.get_argument('pat')
        try:
            results = self.db.find(pat)
            self.render('find.html', results=results, pat=pat, error=None)
        except Exception as e:
            self.render('find.html', results=None, pat=pat, error=e, trace=traceback.format_exc())

        return


def run():
    parser = argparse.ArgumentParser(description='MREP server: morpheme regular expression printer')
    parser.add_argument('file', metavar='FILE', help='data file')
    parser.add_argument('-p', '--port', type=int, required=False, default=8080, help='port number')
    args = parser.parse_args()
    root = os.path.dirname(os.path.abspath(__file__))
    sentences = []
    with open(args.file) as (f):
        for line in f:
            sentences.append(line.strip())

    db = Database(sentences)
    prop = {'db': db}
    handlers = [
     (
      '/', TopHandler, prop),
     (
      '/find', FindHandler, prop)]
    application = tornado.web.Application(handlers, static_path=os.path.join(root, 'static'), template_path=os.path.join(root, 'template'), debug=True)
    application.listen(args.port)
    print 'The server is running on port %d' % args.port
    print 'Type <Ctrl-C> to stop the server'
    tornado.ioloop.IOLoop.instance().start()