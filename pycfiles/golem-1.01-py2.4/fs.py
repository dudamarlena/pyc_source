# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/golem/db/fs.py
# Compiled at: 2008-08-22 15:02:55
import sys, os, shutil, golem
from lxml import etree
import md5

class xmldb(object):
    __module__ = __name__

    def __init__(self, path):
        """open-or-create xml collection

in the flatfile context, that corresponds to a directory, doesn't it...
- so all we do is store the file in the directory.
        """
        self.files = [ x for x in os.listdir(path) if x.endswith('.xml') ]
        self.dir = path

    def add(self, *filenames):
        """ add files to database - which just means copy to directory."""
        for file in filenames:
            shutil.copy(f, self.dir)

    def qfile(self, filename, conceptlist, single=False):
        tree = etree.parse(filename)
        xpath = golem.helpers.xpath.xpath(conceptlist)
        res = []
        for x in xpath:
            res.extend(tree.xpath(x, conceptlist[(-1)].parentdictionary.namespaces))

        if single:
            if len(res) != 1:
                raise AssertionError('Insufficiently specific search set - multiple instances returned.\n')
        del tree
        return res

    def query(self, *conceptsets):
        evaluators = [ x[(-1)] for x in conceptsets ]
        rawres = []
        for fn in self.files:
            f = os.path.join(self.dir, fn)
            rawres.append(golem.db.resultlist([], filename=f))
            for conceptlist in conceptsets:
                rawres[(-1)].extend(self.qfile(f, conceptlist, single=True))

        results = []
        for rawrow in rawres:
            row = golem.db.resultlist([], filename=rawrow.filename)
            for idx in range(len(rawrow)):
                ev = evaluators[idx]
                row.append(ev.getvalue(rawrow[idx]))

            results.append(row)

        return results

    def query_cached(self, cache, *conceptsets):
        evaluators = [ x[(-1)] for x in conceptsets ]
        res = []
        for fn in self.files:
            f = os.path.join(self.dir, fn)
            row = golem.db.resultlist([], filename=f)
            res.append(row)
            md5sum = md5.md5(open(f, 'r').read()).hexdigest()
            if f in cache and md5sum in cache[f]:
                for idx in range(len(conceptsets)):
                    conceptlist = conceptsets[idx]
                    clkey = ('').join([ c.id for c in conceptlist ])
                    ev = evaluators[idx]
                    if clkey in cache[f][md5sum]:
                        row.append(cache[f][md5sum][clkey])
                    else:
                        xv = self.qfile(f, conceptlist, single=True)
                        assert len(xv) == 1
                        val = ev.getvalue(xv[0])
                        row.append(val)
                        cache[f][md5sum][clkey] = val

            else:
                cache[f] = {}
                cache[f][md5sum] = {}
                for idx in range(len(conceptsets)):
                    conceptlist = conceptsets[idx]
                    clkey = ('').join([ c.id for c in conceptlist ])
                    ev = evaluators[idx]
                    xv = self.qfile(f, conceptlist, single=True)
                    assert len(xv) == 1
                    val = ev.getvalue(xv[0])
                    row.append(val)
                    cache[f][md5sum][clkey] = val

        return res


if __name__ == '__main__':
    pass