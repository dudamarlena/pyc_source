# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zoinksftp/utils.py
# Compiled at: 2009-02-04 08:33:07
"""
Handy utilities that don't have a specific module yet

Oisin Mulvihill
2009-02-04

"""
import logging

def log_init(level=logging.CRITICAL):
    """Used mainly in testing to create a default catch all logging set up
       Note, this is not necessary if you've used setup() above and specified logging config 
       in the config file

    This set up catches all channels regardless of whether they
    are in other projects or in our own project.

    """
    log = logging.getLogger()
    hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(level)