# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dreegdl/model.py
# Compiled at: 2020-03-05 17:58:13
# Size of source mod 2**32: 1586 bytes
from config import Config

class Model:
    defaults = {'epochs':[
      50, 100, 500, 1000], 
     'batch_size':lambda x: len(x), 
     'methods':[
      'normal', 'oversample'], 
     'transforms':[
      'scale', 'norm'], 
     'channels':Config.chs, 
     'events':Config.valid_events}
    show_summary = False

    def __init__(self, name='', model=None, version=1, usegen=False, batch_size=defaults['batch_size'], epochs=defaults['epochs'], methods=defaults['methods'], transforms=defaults['transforms'], channels=defaults['channels'], events=defaults['events'], x_conv=None, y_conv=None):
        self.name = name
        self.model = model
        self.version = version
        self.usegen = usegen
        self.channels = channels
        self.events = events
        self.batch_size = batch_size
        self.epochs = epochs
        self.methods = methods
        self.transforms = transforms
        self.x_conv = x_conv
        self.y_conv = y_conv