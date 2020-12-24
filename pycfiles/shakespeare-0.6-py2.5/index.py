# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/index.py
# Compiled at: 2008-10-29 17:02:13
"""
Provide an index of available material including all shakespeares texts
"""
import shakespeare.model

class ShakespeareIndex(object):
    """Main index of texts (ShakespeareIndex class).
    """

    def __init__(self):
        self.all = shakespeare.model.Material.query.order_by('name').all()


all = ShakespeareIndex().all