# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_metadata/file_system.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_metadata.metadata import RootMetadata, registerExtractor
from hachoir_metadata.safe import fault_tolerant
from hachoir_parser.file_system import ISO9660
from datetime import datetime

class ISO9660_Metadata(RootMetadata):
    __module__ = __name__

    def extract(self, iso):
        desc = iso['volume[0]/content']
        self.title = desc['volume_id'].value
        self.title = desc['vol_set_id'].value
        self.author = desc['publisher'].value
        self.author = desc['data_preparer'].value
        self.producer = desc['application'].value
        self.copyright = desc['copyright'].value
        self.readTimestamp('creation_date', desc['creation_ts'].value)
        self.readTimestamp('last_modification', desc['modification_ts'].value)

    @fault_tolerant
    def readTimestamp(self, key, value):
        if value.startswith('0000'):
            return
        value = datetime(int(value[0:4]), int(value[4:6]), int(value[6:8]), int(value[8:10]), int(value[10:12]), int(value[12:14]))
        setattr(self, key, value)


registerExtractor(ISO9660, ISO9660_Metadata)