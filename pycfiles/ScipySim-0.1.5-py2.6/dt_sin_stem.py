# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/dt_sin_stem.py
# Compiled at: 2010-04-22 06:03:43
from scipysim.actors import Channel, Model
from scipysim.actors.display import Stemmer
from scipysim.actors.math.trig import DTSinGenerator

class DT_Sin_Plot(Model):
    """
    This simulation is made up of a composite model containing a sin generator
    and a standard plotting actor.
    """

    def __init__(self):
        super(DT_Sin_Plot, self).__init__()
        chan1 = Channel('DT')
        src = DTSinGenerator(chan1)
        pltr = Stemmer(chan1)
        self.components = [
         src, pltr]


if __name__ == '__main__':
    DT_Sin_Plot().run()