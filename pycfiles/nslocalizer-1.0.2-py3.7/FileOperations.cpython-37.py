# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Helpers/FileOperations.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 2367 bytes
import os, sys
from pbPlist import pbParser

class FileOperations(object):

    @classmethod
    def getData(cls, file_path) -> object:
        data = None
        if os.path.isfile(file_path) is True:
            try:
                encoding = pbParser.GetFileEncoding(file_path)
                file_descriptor = pbParser.OpenFileWithEncoding(file_path, encoding)
                data = file_descriptor.read()
                file_descriptor.close()
            except IOError as exception:
                try:
                    print('I/O error({0}): {1}'.format(exception.errno, exception.strerror))
                finally:
                    exception = None
                    del exception

            except:
                print('Unexpected error:' + str(sys.exc_info()[0]))
                raise

        return data