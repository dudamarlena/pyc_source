# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/xspfish.py
# Compiled at: 2011-05-02 06:48:02
from lxml import objectify
namespace = 'http://xspf.org/ns/0/'
E = objectify.ElementMaker(annotate=False, namespace=namespace, nsmap={None: namespace})