# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload_friendly/datatypes.py
# Compiled at: 2016-03-06 10:23:22
import json
from funkload.utils import Data

class JSONData(Data):
    """Support JSON
    """

    def __init__(self, data, content_type='application/json'):
        Data.__init__(self, content_type, json.dumps(data))