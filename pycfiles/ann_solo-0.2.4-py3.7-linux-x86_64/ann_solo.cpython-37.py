# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ann_solo/ann_solo.py
# Compiled at: 2019-08-06 14:14:58
# Size of source mod 2**32: 778 bytes
import logging
from ann_solo import spectral_library
from ann_solo import writer
import ann_solo.config as config

def main():
    logging.basicConfig(format='{asctime} [{levelname}/{processName}] {module}.{funcName} : {message}', style='{',
      level=(logging.DEBUG))
    config.parse()
    spec_lib = spectral_library.SpectralLibrary(config.spectral_library_filename)
    identifications = spec_lib.search(config.query_filename)
    writer.write_mztab(identifications, config.out_filename, spec_lib._library_reader)
    spec_lib.shutdown()
    logging.shutdown()


if __name__ == '__main__':
    main()