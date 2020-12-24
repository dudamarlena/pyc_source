# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/collectors/general/collectcomment.py
# Compiled at: 2020-05-13 18:50:22
# Size of source mod 2**32: 211 bytes
import pyblish.api

class CollectComment(pyblish.api.ContextPlugin):
    label = 'Collect Comment'
    order = pyblish.api.CollectorOrder

    def process(self, context):
        context.data['comment'] = ''