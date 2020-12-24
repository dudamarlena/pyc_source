# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dictionaryutils/dictionary.py
# Compiled at: 2020-04-29 15:07:15
# Size of source mod 2**32: 1790 bytes
"""
This modules provide the same interface as gdcdictionary.gdcdictionary
It can be 'reinstialized' after it's called init() with another dictionary
For example, using
``gdcdictionary.gdcdictionary`` as the dictionary:

.. code-block:: python

    dictionary.init(gdcdictionary.gdcdictionary)
"""
import sys, traceback
from cdislogging import get_logger
from dictionaryutils import add_default_schema
logger = get_logger('__name__', log_level='info')
this_module = sys.modules[__name__]
required_attrs = [
 'resolvers', 'schema']
optional_attrs = [
 'settings']
resolvers = None
schema = None
settings = None

def init(dictionary):
    """
    Initialize this file with the same attributes as ``dictionary``

    Args:
        dictionary (DataDictionary): a dictionary instance

    Return:
        None
    """
    for required_attr in required_attrs:
        try:
            setattr(this_module, required_attr, getattr(dictionary, required_attr))
        except AttributeError:
            raise ValueError('given dictionary does not define ' + required_attr)

    for optional_attr in optional_attrs:
        try:
            setattr(this_module, optional_attr, getattr(dictionary, optional_attr))
        except AttributeError:
            pass


try:
    from gdcdictionary import gdcdictionary
    add_default_schema(gdcdictionary)
    init(gdcdictionary)
except Exception as e:
    logger.error('Unable to initialize gdcdictionary: {}\n{}'.format(e, traceback.format_exc()))