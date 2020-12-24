# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/suds/umx/basic.py
# Compiled at: 2009-08-19 20:25:52
"""
Provides basic unmarshaller classes.
"""
from logging import getLogger
from suds import *
from suds.umx import *
from suds.umx.core import Core

class Basic(Core):
    """
    A object builder (unmarshaller).
    """

    def process(self, node):
        """
        Process an object graph representation of the xml I{node}.
        @param node: An XML tree.
        @type node: L{sax.element.Element}
        @return: A suds object.
        @rtype: L{Object}
        """
        content = Content(node)
        return Core.process(self, content)