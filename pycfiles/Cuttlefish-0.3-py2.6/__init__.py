# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/cuttlefish/__init__.py
# Compiled at: 2009-10-26 16:28:30
"""
    Browser-based search tool for quickly `grep`ing source code.
"""
from bottle import redirect, request, route, send_file
from mako.exceptions import TopLevelLookupException
from mako.lookup import TemplateCollection
from mako.template import Template
import os.path, subprocess
__version__ = '0.3'
__license__ = 'MIT'

class Config:
    """
    Cuttlefish config from plist file.
    """
    filename = 'cuttlefish-config.plist'
    path_to_static = '.'
    plist = {}
    kleene_collection = ['.']

    @classmethod
    def collections(cls):
        return cls.plist['collections'].keys()

    @classmethod
    def loadFromVicinity(cls, path):
        from os.path import expanduser, expandvars, isdir, dirname, join
        from plistlib import readPlist
        path = expanduser(expandvars(path))
        if not isdir(path):
            path = dirname(path)
        file = join(path, cls.filename)
        cls.plist = readPlist(file)
        cls.kleene_collection = sum([ cls.plist['collections'][k] for k in cls.collections() ], [])
        cls.path_to_static = join(dirname(__file__), 'static')


class SourceTemplate(Template):
    """
    Mako Template subclass provides globals to render context.
    """
    globals = {}

    def render(self, **kwargs):
        extra_kwargs = SourceTemplate.globals.copy()
        extra_kwargs.update(kwargs)
        return super(SourceTemplate, self).render(**extra_kwargs)


class SourceTemplateCollection(TemplateCollection):
    """
    Mako TemplateCollection embedded in the source.
    """

    def __init__(self):
        TemplateCollection.__init__(self)
        kwargs = {'input_encoding': 'utf-8', 
           'output_encoding': 'utf-8', 
           'encoding_errors': 'replace', 
           'format_exceptions': True, 
           'lookup': self}
        self.builtins = {}
        self.builtins['attribution'] = Template('# -*- coding: utf-8 -*-\n            <center id="copyleft" class="tiny">\n                <p>Copyright &copy; 2009 Kaelin Colclasure &bull; MIT License &bull; See <a href=${self_url("/LICENSE.html")}>LICENSE</a> for details&hellip;<br/>\n                Cuttlefish logo by Randall Munroe &bull; <a href="http://www.xkcd.com/520">www.xkcd.com</a></p>\n            </center>\n        ', **kwargs)
        self.builtins['formq'] = Template('# -*- coding: utf-8 -*-\n            <%def name="mkoption(label,value,selected=None)">\n                % if value == selected:\n                    <option value="${value}" selected="True">\\\n                % else:\n                    <option value="${value}">\\\n                % endif\n                ${label | h}</option>\n            </%def>\n            <form action=${self_url("/search")} accept-charset="utf-8" method="get">\n            <table align="center">\n            <tr>\n                <td class="nobr">\n                    <input name="q" value="${q | u}" type="search" placeholder="" autosave="net.colclasure.cuttlefish.q" results="20" maxLength="256" size="55" />\n                    <input name="c" value="3" type="hidden" />\n                    <input name="r" value="cooked" type="hidden" />\n                    <input type="submit" value="Search" name="btn" />\n                </td>\n            </tr>\n            <tr>\n                <td class="nobr" align="center">\n                    Collection: <select id="collection" name="cn">\n                                ${mkoption("All collections", "*", cn)}\n                                <optgroup label="Select collection">\n                                % for collection in Config.collections():\n                                    ${mkoption(collection, collection, cn)}\n                                % endfor\n                                </optgroup>\n                                </select>\n                </td>\n            </tr>\n            </table>\n            </form>\n        ', **kwargs)
        self.builtins['root'] = SourceTemplate('# -*- coding: utf-8 -*-\n            <html>\n            <head>\n                <title>Cuttlefish Search: ${subtitle | h}</title>\n                <link rel="stylesheet" type="text/css" href=${self_url("/static/style.css")} />\n            </head>\n            <body>\n                <center id="logo">\n                    <p><a href=${self_url("/")} class="logolink">\n                    <img src=${self_url("/static/cuttlefish.png")} height="150" />[cuttlefish]\n                    </a></p>\n                </center>\n                <%include file=\'formq\' />\n                <%include file=\'attribution\' />\n            </body>\n            </html>\n        ', **kwargs)
        self.builtins['cooked'] = Template('# -*- coding: utf-8 -*-\n            <table width="100%">\n            % for r in results:\n                <tr><td>${r.filename | h}&nbsp;(${r.match_count | h})</td></tr>\n                <tr><td><div class="context">\n                % for l in r.lines:\n                %   if l[0] == -1:\n                </div><div class="context">\n                %   else:\n                %     if l[2]:\n                <a href="txmt://open?url=file%3A%2F%2F${r.filename | u}&line=${l[0]}">\n                %     endif\n                <div class="${(\'contextline\', \'matchline\')[l[2]]}">${u"%5d %s" % (l[0], l[1]) | h}</div>\n                %     if l[2]:\n                </a>\n                %     endif\n                %   endif\n                % endfor\n                </div></td></tr>\n            % endfor\n            </table>\n        ', **kwargs)
        self.builtins['raw'] = Template('# -*- coding: utf-8 -*-\n            <pre>${results.raw_results | h}\n            </pre>\n        ', **kwargs)
        self.builtins['results'] = SourceTemplate('# -*- coding: utf-8 -*-\n            <html>\n            <head>\n                <title>Cuttlefish Search: &laquo;${subtitle | h}&raquo;</title>\n                <link rel="stylesheet" type="text/css" href=${self_url("/static/style.css")} />\n            </head>\n            <body>\n                <center id="logosmall">\n                    <p><a href=${self_url("/")} class="logolink">\n                    <img src=${self_url("/static/cuttlefish.png")} height="100" /><br/>[cuttlefish]\n                    </a></p>\n                </center>\n                <%include file=\'formq\' />\n                % if render == \'cooked\':\n                  <%include file=\'cooked\' />\n                % elif render == \'raw\':\n                  <%include file=\'raw\' />\n                % else:\n                  <%include file=\'nonesuch\' />\n                % endif\n                <%include file=\'attribution\' />\n            </body>\n            </html>\n        ', **kwargs)
        self.builtins['license'] = SourceTemplate('# -*- coding: utf-8 -*-\n            <html>\n            <head>\n                <title>Cuttlefish Search: LICENSE</title>\n                <link rel="stylesheet" type="text/css" href=${self_url("/static/style.css")} />\n            </head>\n            <body>\n                <center id="logosmall">\n                    <p><a href=${self_url("/")} class="logolink">\n                    <img src=${self_url("/static/cuttlefish.png")} height="100" />[cuttlefish]\n                    </a></p>\n                </center>\n                <center id="license">\n                    <table>\n                        <tr><td align="right" class="tiny">Version ${VERSION | h}</td></tr>\n                        <tr><td><pre>${LICENSE | h}</pre></td></tr>\n                    </table>\n                </center>\n                <div id="kudos" align="center">\n                Built with <a href="http://bottle.paws.de/"><img src=${self_url("/static/bottle-sig.png")} /></a>\n                &amp; <a href="http://www.makotemplates.org/"><img src=${self_url("/static/mako-sig.png")} height="38" /></a>\n                </div>\n                <%include file=\'attribution\' />\n            </body>\n            </html>\n        ', **kwargs)

    def get_template(self, uri, request=None):
        if request != None:
            SourceTemplate.globals['Config'] = Config
            SourceTemplate.globals['self_url'] = lambda path: '"%s%s"' % (request.environ['SCRIPT_NAME'], path)
        try:
            return self.builtins[uri]
        except KeyError:
            raise TopLevelLookupException("Cant locate template for uri '%s'" % uri)

        return


stc = SourceTemplateCollection()
results = None

@route('/')
def root():
    global results
    results = None
    return stc.get_template('root', request=request).render(subtitle='Python Source Code', q='', cn='*')


class MatchChunk:
    """
    Represent one or more matches with their surrounding context.
    """

    def __init__(self):
        self.filename = None
        self.lines = []
        self.match_count = 0
        self.is_last = False
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if exc_type is StopIteration:
                self.is_last = True
            else:
                return False
        return True

    def append(self, lnum, line, is_match=False):
        if is_match:
            self.match_count += 1
        self.lines.append((lnum, line, is_match))


class MatchParser:
    """
    Parse matches from `grep`.
    """

    def __init__(self, input):
        self.input = input
        self.chunk = None
        self.defer = None
        self.fin = False
        return

    def _match(self, raw_result):
        try:
            parts = raw_result.split(':', 2)
            lnum = int(parts[1])
            line = parts[2]
        except (IndexError, ValueError):
            return False
        else:
            if self.chunk.filename != None:
                if parts[0] != self.chunk.filename:
                    return False
            else:
                if not os.path.isfile(parts[0]):
                    return False
                self.chunk.filename = parts[0]
                [ self._context(raw_defer) for raw_defer in self.defer ]

        self.chunk.append(lnum, line, is_match=True)
        return True

    def _context(self, raw_result):
        if self.chunk.filename == None:
            return False
        else:
            assert raw_result.startswith(self.chunk.filename), "filename:'%s' raw_result:'%s'" % (self.chunk.filename, raw_result)
            raw_result = raw_result[len(self.chunk.filename):]
            parts = raw_result.split('-', 2)
            lnum = int(parts[1])
            line = parts[2]
            self.chunk.append(lnum, line, is_match=False)
            return True

    def next(self):
        if self.fin:
            raise StopIteration
        with MatchChunk() as (self.chunk):
            self.defer = []
            raw_result = unicode(self.input.next(), 'utf-8', 'replace').rstrip()
            while raw_result != '--':
                if self._match(raw_result) or self._context(raw_result):
                    pass
                else:
                    self.defer.append(raw_result)
                raw_result = unicode(self.input.next(), 'utf-8', 'replace').rstrip()

        if self.chunk.is_last:
            self.fin = True
            if len(self.chunk.lines) == 0:
                raise StopIteration
        return self.chunk


class MatchChunkRunParser:
    """
    Collect runs of chunks from a MatchParser.
    """

    def __init__(self, input):
        self.parser = MatchParser(input)
        self.next_chunk = None
        return

    def next(self):
        if self.next_chunk == None:
            self.next_chunk = self.parser.next()
        chunk = self.next_chunk
        while not chunk.is_last:
            chunk = self.parser.next()
            if chunk.filename != self.next_chunk.filename:
                self.next_chunk, chunk = chunk, self.next_chunk
                return chunk
            self.next_chunk.append(-1, None)
            [ self.next_chunk.append(*line) for line in chunk.lines ]

        self.next_chunk, chunk = None, self.next_chunk
        return chunk


class SearchSubprocess:
    """
    Search using `grep` in a subprocess.
    """

    def __init__(self, query, c=3, cn='*', parser=MatchChunkRunParser):
        self.query = query
        self.parser = parser
        cmd = ['/usr/bin/grep',
         '--recursive',
         '--binary-files=without-match',
         '--line-number',
         '--context=%d' % c,
         '--fixed-strings', query]
        if cn == '*':
            cmd.extend([ os.path.abspath(path) for path in Config.kleene_collection ])
        else:
            cmd.extend([ os.path.abspath(path) for path in Config.plist['collections'][cn] ])
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._raw_results = None
        return

    def __iter__(self):
        return self.parser(self.proc.stdout)

    @property
    def raw_results(self):
        if self._raw_results == None:
            self._raw_results = unicode(self.proc.communicate()[0], 'utf-8', 'replace')
        return self._raw_results


def quicklook(q):
    from pprint import pprint
    results = SearchSubprocess(q)
    for chunk in results:
        pprint((chunk.filename, chunk.match_count, chunk.lines))


@route('/search')
def search():
    global results
    try:
        q = unicode(request.GET['q'], 'utf-8', 'replace')
        c = unicode(request.GET['c'], 'utf-8', 'replace')
        r = unicode(request.GET['r'], 'utf-8', 'replace')
        cn = unicode(request.GET['cn'], 'utf-8', 'replace')
        if results != None and results.query == q:
            pass
        results = SearchSubprocess(query=q, c=int(c), cn=cn)
        return stc.get_template('results', request=request).render(subtitle=q, q=q, render=r, cn=cn, results=results)
    except KeyError:
        redirect(request.environ['SCRIPT_NAME'])

    return


@route('/static/:filename')
def static(filename):
    send_file(filename, root=Config.path_to_static)


@route('/LICENSE.html')
def license():
    with open(os.path.join(Config.path_to_static, 'LICENSE.txt'), 'r') as (file):
        LICENSE = file.read()
    return stc.get_template('license', request=request).render(LICENSE=LICENSE, VERSION=__version__)


def see_bottle_run():
    import bottle
    Config.loadFromVicinity(__file__)
    kwargs = Config.plist['bottle-run-kwargs']
    bottle.run(**kwargs)


if __name__ == '__main__':
    see_bottle_run()