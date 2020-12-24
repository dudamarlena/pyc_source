# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/jwst_gtvt/utils.py
# Compiled at: 2020-04-10 13:48:06
# Size of source mod 2**32: 1042 bytes
"""
Utility functions for package
"""
import astropy, os, shutil

class Error(Exception):
    __doc__ = 'Base class for other exceptions'


class ChoiceError(Error):
    __doc__ = 'Raised when input is not y or n'


def delete_cache():
    """Delete astroquery Horizons cache"""
    cache = astropy.config.get_cache_dir()
    horizons_cache = os.path.join(cache, 'astroquery', 'Horizons')
    if os.path.exists(horizons_cache):
        print('Horizons cache located: {}'.format(horizons_cache))
        choice = input('Do you wish to delete this folder? [y/n]: ')
        try:
            if choice == 'y':
                shutil.rmtree(horizons_cache)
                print('Cache deleted..')
            else:
                if choice == 'n':
                    print('You chose to not delete the cache, exiting.')
                else:
                    raise ChoiceError
        except ChoiceError:
            print('Input was not y or n, try again and provide valid input!')

    else:
        print('There is no Horizons cache available, exiting')