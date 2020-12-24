# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/gettextutils.py
# Compiled at: 2016-06-13 14:11:03
"""
gettext for openstack-common modules.

Usual usage in an openstack.common module:

    from vsm.openstack.common.gettextutils import _
"""
import gettext
t = gettext.translation('openstack-common', 'locale', fallback=True)

def _(msg):
    return t.ugettext(msg)