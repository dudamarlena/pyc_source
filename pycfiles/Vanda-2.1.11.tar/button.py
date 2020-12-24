# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/vanda/vanda/apps/dashboard/widgets/button.py
# Compiled at: 2013-01-07 03:52:15
from base import Widget

class Button(Widget):
    title = ''
    name = 'button'
    image = False
    template = 'dashboard/widgets/button.html'

    def to_dict(self):
        a = super(Button, self).to_dict()
        a.update({'image': self.image})
        return a