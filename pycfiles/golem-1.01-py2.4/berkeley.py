# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/golem/db/berkeley.py
# Compiled at: 2008-08-22 15:02:55
import sys, os, dbxml, golem
from bsddb3.db import *
from _dbxml import XmlException, DATABASE_ERROR
import StringIO
from lxml import etree
from conceptlist import conceptlist
DATABASE = 'NaCl.dbxml'
namespaces = {'cml': 'http://www.xml-cml.org/schema', 'golem': 'http://www.lexical.org.uk/golem', 'h': 'http://www.w3.org/1999/xhtml', 'xsl': 'http://www.w3.org/1999/XSL/Transform', 'xsd': 'http://www.w3.org/2001/XMLSchema'}

class xpathlist(list):
    __module__ = __name__

    def __init__(self, *args):
        list.__init__(self, list(args))

    def setpredicate(self, predicate):
        self.predicate = predicate

    def getpredicate(self):
        try:
            return self.predicate
        except AttributeError:
            return

        return


class xmldb(object):
    __module__ = __name__

    def __init__(self, f):
        """ open-or-create xml database/collection """
        self.manager = dbxml.XmlManager()
        self.database = f
        if os.path.exists(f):
            self.container = self.manager.openContainer(f)
        else:
            self.container = self.manager.createContainer(f)

    def add(self, *files):
        """ add files to database"""
        uc = self.manager.createUpdateContext()
        for f in files:
            data = open(f, 'r').read()
            self.container.putDocument(f, data, uc)

    def getcontext(self):
        """ get the default query-context handler, with the cml namespace
        already set """
        querycontext = self.manager.createQueryContext()
        for key in namespaces:
            querycontext.setNamespace(key, namespaces[key])

        querycontext.setDefaultCollection(self.database)
        querycontext.setReturnType(querycontext.DeadValues)
        return querycontext

    def xquery(self, *xpathsets):
        """ turn xpaths into xquery and query database """
        queries = []
        context = self.getcontext()
        for pathset in xpathsets:
            query = ''
            for path in pathset:
                query += path

            queries.append(query)

        pred = xpathsets[0].getpredicate()
        if pred is not None:
            queries[0] += pred
        fullquery = '\nfor $doc in //collection()\nwhere $doc%s\nreturn \n<golem:results>' % queries[0]
        for q in queries:
            fullquery += '\n\n  <golem:sep>\n    {$doc%s}\n  </golem:sep>' % q

        fullquery += '\n</golem:results>'
        print >> sys.stderr, 'QUERY: ', fullquery
        results = self.manager.query(fullquery, context)
        results.reset()
        res = []
        for value in results:
            res.append(etree.parse(StringIO.StringIO(value.asString())))

        return res

    def cquery(self, *conceptsets):
        """assemble XPath from components in a Golem dictionary"""
        qsets = []
        for concepts in conceptsets:
            xpaths = [ obj.gxpath.path.strip() for obj in concepts ]
            sanitized = xpathlist()
            sanitized.setpredicate(concepts.getpredicate())
            for path in xpaths:
                if path.startswith('./'):
                    sanitized.append('/' + path)
                elif not path.startswith('/'):
                    sanitized.append('/' + path)
                else:
                    sanitized.append(path)

            qsets.append(sanitized)

        res = self.xquery(*qsets)
        return res

    def query(self, *conceptsets):
        evaluators = [ x[(-1)] for x in conceptsets ]
        res = self.cquery(*conceptsets)
        results = []
        for resultset in res:
            row = []
            frags = resultset.xpath('/golem:results/golem:sep', namespaces)
            for idx in range(len(frags)):
                row.append(evaluators[idx].getvalue(frags[idx][0]))

            results.append(row)

        return results


def bigtest():
    db = xmldb(DATABASE)
    db.add(*sys.argv[1:])
    results = db.xquery("/.//cml:module[@title='Final system']", "/.//cml:crystal[@dictRef='castep:ucell']")
    print len(results)


def _test():
    mgr = dbxml.XmlManager()
    uc = mgr.createUpdateContext()
    xmldata = file('NaBr_00GPa.xml', 'r').read()
    try:
        container = mgr.createContainer('test.dbxml')
        container.putDocument('NaBr_00GPa.xml', xmldata, uc)
        qc = mgr.createQueryContext()
        qc.setNamespace('cml', 'http://www.xml-cml.org/schema')
        results = mgr.query("collection('test.dbxml')//cml:module", qc)
        results.reset()
        res = []
        for value in results:
            document = value.asString()
            res.append(document)

        print len(res)
    except XmlException, inst:
        print 'XMLException (', inst.ExceptionCode, '): ', inst.What
        if inst.ExceptionCode == DATABASE_ERROR:
            print 'Database error code:', inst.DBError


if __name__ == '__main__':
    bigtest()