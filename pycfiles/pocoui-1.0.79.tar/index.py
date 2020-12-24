# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/xapian/index.py
# Compiled at: 2006-12-26 17:18:03
__doc__ = '\n    pocoo.pkg.xapian.index\n    ~~~~~~~~~~~~~~~~~~~~~~\n\n    Run the following commands in the pocoo cli to create the index::\n\n        from pocoo.pkg.xapian.index import Index\n        idx = Index(ctx)\n        idx.rebuild()\n\n    :copyright: 2006 by Christoph Hack.\n    :license: GNU GPL, see LICENSE for more details.\n'
import re, cPickle
from os import path
from pocoo.db import meta
from pocoo.pkg.core import db
from pocoo.pkg.core.forum import get_post
import xapian
try:
    from Stemmer import Stemmer
except ImportError:
    Stemmer = None

UNICODE_ENCODING = 'UTF-8'
UNICODE_ERROR_POLICY = 'replace'

class PostQueue(object):
    """ A class for collecting all new, edited and deleted posts. """
    __module__ = __name__

    def __init__(self, ctx):
        self.ctx = ctx

    def __iter__(self):
        p = db.posts.c
        start_id = 0
        posts = self.ctx.engine.execute(meta.select([p.post_id, p.title, p.text, p.root_post_id], p.post_id > start_id))
        for post in posts:
            yield {'post_id': post[0], 'title': post[1], 'text': post[2], 'root_post_id': post[3]}


class PostAnalyzer(object):
    __module__ = __name__
    token_re = re.compile('(?P<word>\\w+)', re.U)

    def __init__(self, language=None):
        if Stemmer and language:
            self.stemmer = Stemmer(language)
        else:
            self.stemmer = None
        return

    def raw_tokenize(self, text):

        def enc(uc):
            return uc.lower().encode(UNICODE_ENCODING, UNICODE_ERROR_POLICY)

        tokenstream = re.finditer(self.token_re, text)
        for m in tokenstream:
            if m.group('word'):
                word = m.group('word')
                yield (enc(word), m.start())

    def tokenize(self, text):
        for (word, pos) in self.raw_tokenize(text):
            if self.stemmer:
                yield (
                 self.stemmer.stemWord(word), pos)
            else:
                yield (
                 word, pos)


class Index(object):
    """ A class for all index related jobs like indexing and searching. """
    __module__ = __name__

    def __init__(self, ctx):
        self.ctx = ctx
        self.db_dir = path.join(ctx.cfg.root, 'cache', 'xapian')
        self.stem_language = 'en'

    def rebuild(self):
        """ Rebuild the entire Index. """
        db = xapian.WritableDatabase(self.db_dir, xapian.DB_CREATE_OR_OVERWRITE)
        analyzer = PostAnalyzer(self.stem_language)
        for post in PostQueue(self.ctx):
            doc = xapian.Document()
            position = 0
            for (term, pos) in analyzer.tokenize(post['text']):
                doc.add_posting(term, position)
                position += 1

            datastr = cPickle.dumps((post['root_post_id'], post['post_id']))
            doc.set_data(datastr)
            print 'Adding Post %i' % db.add_document(doc)

        db.flush()

    def search(self, req, query):
        """ Search a single word in the index. """
        if not path.exists(self.db_dir):
            raise RuntimeError('Please run index.rebuild() first!')
        db = xapian.Database(self.db_dir)
        enq = xapian.Enquire(db)
        qry = xapian.Query(query.encode(UNICODE_ENCODING, UNICODE_ERROR_POLICY))
        print 'Performing query "%s"' % qry.get_description()
        enq.set_query(qry)
        matches = enq.get_mset(0, 20)
        print '%i results found' % matches.get_matches_estimated()
        result = [ cPickle.loads(match[xapian.MSET_DOCUMENT].get_data()) for match in matches ]
        result.sort(lambda a, b: cmp(a[0], b[0]))
        last = None
        rval = []
        for thread in result:
            if thread[0] == last:
                continue
            rval.append(get_post(req, thread[1]))
            last = thread[0]

        return rval