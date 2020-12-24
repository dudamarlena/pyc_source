# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\mpl_builders\mpl_animations.py
# Compiled at: 2016-02-07 12:02:19
from matplotlib.animation import ArtistAnimation as AA

class MPL_ArtistAnimation(AA):

    def updateArtists(self, artists):
        print 'updating artists %s ....' % artists
        for line in artists:
            collection = line.abcModel
            line.set_xdata(collection.get_X().getVariableData())
            line.set_ydata(collection.get_Y().getVariableData())

        return artists

    def _step(self, *a, **k):
        artists = self._framedata[0]
        self.updateArtists(artists)
        AA._step(self, *a, **k)