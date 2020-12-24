# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/txoids/ports/deferreds.py
# Compiled at: 2017-10-10 03:34:26
# Size of source mod 2**32: 602 bytes
from txoids.generic.deferreds import BaseAction
from txoids.ports import processors

class FetchPorts(BaseAction):
    method = 'walk'

    def get_processor(self):
        model = self.parser.model
        if model == 'D-Link DES-3010G':
            cls = processors.DES3010GPortsProcessor
        else:
            if model == 'D-Link DGS-3100-24':
                cls = processors.DGS3100PortsProcessor
            else:
                if model == 'D-Link DGS-3100-24TG':
                    cls = processors.DGS3100TGPortsProcessor
                else:
                    cls = processors.PortsProcessor
        return cls(self.parser)