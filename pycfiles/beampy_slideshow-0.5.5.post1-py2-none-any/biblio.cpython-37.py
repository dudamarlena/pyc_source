# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/biblio.py
# Compiled at: 2018-12-02 10:29:04
# Size of source mod 2**32: 564 bytes
import beampy.modules.text as text
from beampy.functions import check_function_args

def cite(list_authors, **kwargs):
    """
    function to write citation on slide

    Arguments
    ---------

    list_authors : python list of authors
    """
    if type(list_authors) == type('this_is_a_string'):
        list_authors = [
         list_authors]
    citestr = '[' + ', '.join(list_authors) + ']'
    args = check_function_args(cite, kwargs)
    text(citestr, **args)