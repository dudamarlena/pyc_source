# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/data_source.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 1599 bytes
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import makeOptions, callsite

class DataSource(object):

    def __init__(self, j_source, sql_ctx, name):
        self._jsource = j_source
        self._sql_ctx = sql_ctx
        self.name = name

    def setFormat(self, format, **options):
        options['callSite'] = callsite()
        self._jsource.setFormat(format, makeOptions(self._sql_ctx._sc, options))

    def getFrame(self, **options):
        minPartitions = targetPartitions = None
        if 'minPartitions' in options:
            minPartitions = options['minPartitions']
            targetPartitions = options.get('targetPartitions', minPartitions)
        else:
            if 'targetPartitions' in options:
                minPartitions = targetPartitions = options['targetPartitions']
            elif minPartitions is None:
                jframe = self._jsource.getDynamicFrame()
            else:
                jframe = self._jsource.getDynamicFrame(minPartitions, targetPartitions)
            return DynamicFrame(jframe, self._sql_ctx, self.name)