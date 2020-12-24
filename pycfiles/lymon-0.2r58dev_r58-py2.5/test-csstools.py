# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lymon/view/test-csstools.py
# Compiled at: 2008-06-23 12:24:02
from lymon.core import *
from time import time
start = time()
html = Document()
html.div(slot='a.b', attrs={'class': 'classB'})
html.div(slot='d.b', id=False)
html.div(slot='a.c')
html.h6(slot='a.b.c', attrs={'id': 'title'})
tag = html.context[(-1)]
s = Selector(tag=tag, context=html.context)
print s.build()
end = time()
print 'Build time: %s' % (end - start)