# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sc/object/dissect/dissect.py
# Compiled at: 2009-11-18 13:46:44
from Products.Five.browser import BrowserView

class Dissect(BrowserView):
    __module__ = __name__

    def __call__(self):
        page = ''
        metodos = dir(self.context)
        metodos = [ m for m in metodos if '__roles__' not in m.lower() if not m.startswith('manage_') ]
        page += '<h1> There are %d available methods/attributes in <strong> %s </strong> </h1> ' % (len(metodos), self.context.absolute_url())
        page += '<table border="1px">'
        page += '<tr><th>%s</th><th>%s</th></tr>' % ('Methods', 'Value')
        for m in metodos:
            try:
                valor = self.context.restrictedTraverse(m)
                if callable(valor) and m != 'unindexObject':
                    valor = valor()
                page += '<tr><td><strong>%s<strong></td><td>%s</td></tr>' % (m, valor)
            except:
                pass

        page += '</table>'
        return page