# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/ossf/json_.py
# Compiled at: 2012-10-12 07:02:39
try:
    import ijson
except:
    HAS_IJSON = False
else:
    HAS_IJSON = True

import json
from coils.core import NotImplementedException, BLOBManager
from filter import OpenGroupwareServerSideFilter

class JSONOSSFilter(OpenGroupwareServerSideFilter):

    @property
    def handle(self):
        if self._mimetype != 'application/json':
            raise Exception('Input type for JSONDecoder is not mimetype application/json')
        if hasattr(self, '_mode'):
            if self._mode == 'pagination':
                return self.paginate()
            if self._mode == 'count':
                return self.count()
            raise NotImplementedException(('JSON OSSF mode {0} not implemented').format(self._mode))
        else:
            return self._rfile

    def paginate(self):
        if not HAS_IJSON:
            raise NotImplementedException('JSON OSSF currently requires the ijson module.')
        if hasattr(self, '_path'):
            if hasattr(self, '_range'):
                value = self._range.split('-')
                if len(value[0]) == 0:
                    floor = 0
                else:
                    floor = int(value[0])
                if len(value[1]) == 0:
                    cieling = None
                else:
                    cieling = int(value[1])
            else:
                floor = 0
                cieling = None
            if hasattr(self, '_criteria'):
                (key, value) = self._criteria.split(',')
                try:
                    int_key = int(key)
                except:
                    int_key = None

            else:
                (key, value, int_key) = (None, None, None)
            data = []
            counter = 0
            for item in ijson.items(self._rfile, self._path):
                if key is not None:
                    if isinstance(item, basestring) or isinstance(item, list):
                        if int_key is not None:
                            if item[int_key] != value:
                                item = None
                        else:
                            item = None
                    elif isinstance(item, dict):
                        if item[key] != value:
                            item = None
                if item:
                    counter += 1
                    if counter >= floor:
                        data.append(item)
                    if cieling:
                        if counter >= cieling:
                            break

            tmp = BLOBManager.ScratchFile()
            json.dump(data, tmp)
            tmp.seek(0)
            return tmp
        else:
            return self._rfile
            return

    def count(self):
        counter = 0
        if hasattr(self, '_path'):
            if HAS_IJSON:
                for item in ijson.items(self._rfile, self._path):
                    counter += 1

            else:
                raise NotImplementedException('JSON OSSF currently requires the ijson module.')
        tmp = BLOBManager.ScratchFile()
        tmp.write(unicode(counter))
        tmp.seek(0)
        return tmp

    @property
    def mimetype(self):
        if self._mode == 'pagination':
            return 'application/json'
        if self._mode == 'count':
            return 'text/plain'