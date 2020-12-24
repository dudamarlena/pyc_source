# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyThesaurus/ioDing.py
# Compiled at: 2008-10-06 10:31:21
import sys
from pyThesaurus.Thesaurus import Thesaurus
from pyThesaurus.Concept import Concept
from re import sub
import csv, io

def _simplify(s):
    s = sub('\\s+', ' ', s)
    s = s.replace('\n', '')
    return s.strip()


def _clean(s):
    s = sub('(\\([^\\)]*)', '', s)
    return s


class ding(csv.Dialect):
    __module__ = __name__
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = '\r\n'
    escapechar = '\\'
    quoting = csv.QUOTE_MINIMAL


csv.register_dialect('ding', ding)

class ioDing:
    """

        """
    __module__ = __name__

    def __init__(self, language, contexts=[], thesaurus=Thesaurus()):
        self._t = thesaurus
        self._contexts = contexts
        self._dl = language

    def read(self, istream, encoding='utf-8'):

        class NoCommentsStream:
            """ Elimina los comentarios del archivo de entrada. """
            __module__ = __name__

            def __init__(self, stream):
                self.stream = stream

            def __iter__(self):
                return self

            def next(self):
                n = self.stream.next()
                return n.split('#')[0]

        reader = csv.reader(NoCommentsStream(istream), dialect='ding')
        for row in reader:
            c = Concept(et=[ '%s@%s' % (unicode(_clean(t), encoding), self._dl) for t in row ], contexts=self._contexts)
            self._t.append_concept(c)

        return

    def write(self, ostream, encoding='utf-8'):
        writer = csv.writer(ostream, dialect='ding')
        ctls = [ map(lambda s: s.split('@'), self._t[cid]['=']) for cid in self._t.concepts() ]
        ts = [ [ t.decode(encoding) for (t, l) in tls if l == self._dl ] for tls in ctls ]
        writer.writerows(ts)
        return

    def thesaurus(self):
        return self._t


io.registerFormat('Ding', ioDing)