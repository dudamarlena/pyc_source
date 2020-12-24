# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/vinergy/vinergy.py
# Compiled at: 2011-06-15 15:37:35
"""
  vinergy.vinergy
  ~~~~~~~~~~~~~~~

  Vinergy - CLI Pastebin within VimEnergy
"""
import os, web, time, datetime
from hashlib import md5
import model, config
from util import util
urls = ('/(.*)', 'Index')
rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir + 'templates/', base='base')

class Index:

    def GET(self, got):
        """Browse code"""
        if not got:
            return render.index(config.URL)
        else:
            if got.rfind('/') != -1:
                syntax = got.rsplit('/', 1)[1].lower()
                got = got.rsplit('/', 1)[0]
            else:
                syntax = None
            doc = model.get_code_by_name(got)
            if not doc:
                raise web.notfound(got + ' not found\n')
            codes = dict(doc['content'])
            if syntax is None:
                syntax = web.ctx.query[1:].lower()
            if not syntax:
                return codes['raw']
            syntax = util.norm_filetype(syntax)
            is_t = util.is_termua(web.ctx.env['HTTP_USER_AGENT'])
            s = lambda s: 't_' + s if is_t else s
            code = codes.get(s(syntax), None)
            if code is not None:
                if is_t:
                    return code
                return render.code(code)
            code = codes['raw']
            if is_t:
                r = util.render(code, 'TerminalFormatter', syntax)
                model.update_code(got, r, s(syntax))
                return r
            r = util.render(code, 'HtmlFormatter', syntax)
            model.update_code(got, r, s(syntax))
            return render.code(r)
            return

    def POST(self, got):
        """Insert new code"""
        try:
            code = web.input().vimcn
            if len(code) < 21:
                raise ValueError
            oid = md5(unicode(code).encode('utf8')).hexdigest()
            r = model.get_code_by_oid(oid)
            if r is not None:
                name = r['name']
            else:
                (name, count) = util.name_count()
                epoch = time.mktime(datetime.datetime.utctimetuple(datetime.datetime.utcnow()))
                model.insert_code(oid, name, code, count, epoch)
            raise util.response(' ' + config.URL + '/' + name + '\n')
        except AttributeError:
            status = '400 Bad Request'
            raise util.response('Oops. Please Check your command.\n', status)
        except ValueError:
            status = '400 Bad Request'
            tip = 'Hi, content must be longer than \'print "Hello, world!"\'\n'
            tip = util.render(tip, 'TerminalFormatter', 'py')
            raise util.response(tip, status)

        return


app = web.application(urls, globals())
if __name__ == '__main__':
    app.run()
else:
    web.config.debug = False
    application = app.wsgifunc()