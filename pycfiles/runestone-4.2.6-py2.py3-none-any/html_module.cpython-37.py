# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/codelens/html_module.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 64 bytes


def display_img(src):
    setHTML('<img src="%s"/>' % str(src))