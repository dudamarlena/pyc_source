# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/introspection.py
# Compiled at: 2016-02-23 09:40:42
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'

def get_class_no_arg(class_name):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)

    return m()


def get_class_one_arg(class_name, par1):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)

    return m(par1)


def get_class_two_arg(class_name, par1, par2):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)

    return m(par1, par2)


def get_class_three_arg(class_name, par1, par2, par3):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)

    return m(par1, par2, par3)


def get_class_four_arg(class_name, par1, par2, par3, par4):
    parts = class_name.split('.')
    module = parts[0]
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)

    return m(par1, par2, par3, par4)