# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dhclientlist\__init__.py
# Compiled at: 2013-08-08 16:54:43
import util

class AccessError(Exception):
    pass


def get(address, username, password, driver=None):
    """
    Calls get method from appropriate driver.
    If no driver is passed to this function, it will try to choose the best driver.
    """
    if driver is None:
        driver = util.find_driver(address, username, password)
    try:
        return driver.get(address, username, password)
    except:
        raise AccessError("Error trying to get client list from DHCP server %s with username '%s' and password '%s'" % (address, username, password))

    return