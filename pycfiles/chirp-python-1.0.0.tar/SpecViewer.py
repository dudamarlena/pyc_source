# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\gui\SpecViewer.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\nClasses deriving from TSViewer.TSDataHandler and TSViewer.TSViewer\nwith specializations for plotting spectrograms.\n\nCopyright (C) 2009 Daniel Meliza <dan // meliza.org>\nCreated 2009-07-16\n'
from __future__ import division
import wx
from chirp.gui import TSViewer
from chirp.common.signal import spectrogram
from chirp.common.config import _configurable
from matplotlib import cm

class SpecHandler(TSViewer.TSDataHandler, _configurable):
    """
    Data handler subclass for spectrograms. The plot_data() method
    will compute the spectrogram of a signal.
    """
    options = dict(colormap='hot', freq_range=(0.0, 15000.0), dynrange=60)
    config_sections = ('spectrogram', 'gui')

    def __init__(self, configfile=None):
        self.spectrogram = spectrogram(configfile=configfile)
        self.readconfig(configfile)
        self.signal = None
        self.image = None
        self.Fs = None
        return

    def set_axes(self, axes):
        """ After getting axes, set the default ylim """
        super(SpecHandler, self).set_axes(axes)
        f1, f2 = (f / 1000.0 for f in self.options['freq_range'])
        self.axes.set_ylim((f1, f2))

    def get_colormap(self, obj=False):
        if obj:
            return getattr(cm, self.options['colormap'], 'Greys')
        else:
            return self.options['colormap']

    def set_colormap(self, value):
        if value == self.options['colormap']:
            return
        self.options['colormap'] = value
        if self.image:
            self.image.set_cmap(self.get_colormap(obj=True))
            self.draw()

    colormap = property(get_colormap, set_colormap)

    def get_method(self):
        return self.spectrogram.options['spec_method']

    def set_method(self, value):
        self.spectrogram.options['spec_method'] = value
        if self.signal is not None:
            self.plot_data(self.signal, self.Fs)
        return

    method = property(get_method, set_method)

    def get_shift(self):
        return self.spectrogram.options['window_shift']

    def set_shift(self, value):
        if value == self.spectrogram.options['window_shift']:
            return
        else:
            self.spectrogram.options['window_shift'] = value
            if self.signal is not None:
                self.plot_data(self.signal, self.Fs)
            return

    shift = property(get_shift, set_shift)

    def get_window_len(self):
        return self.spectrogram.options['window_len']

    def set_window_len(self, value):
        if value == self.spectrogram.options['window_len']:
            return
        else:
            self.spectrogram.options['window_len'] = value
            if self.signal is not None:
                self.plot_data(self.signal, self.Fs)
            return

    window_len = property(get_window_len, set_window_len)

    def get_dynrange(self):
        return self.options['dynrange']

    def set_dynrange(self, value):
        if value == self.options['dynrange']:
            return
        self.options['dynrange'] = value
        if self.image:
            sigmax = self.image.get_array().max()
            self.image.set_clim((sigmax - value / 10, sigmax))
            self.draw()

    dynrange = property(get_dynrange, set_dynrange)

    def plot_data(self, signal, Fs=20):
        """ Compute spectrogram and plot it to the current axes """
        self.signal = signal
        self.Fs = float(Fs)
        S, extent = self.spectrogram.dbspect(signal, Fs)
        if self.image is None:
            y1, y2 = self.ylim
            self.image = self.axes.imshow(S, extent=extent, cmap=self.get_colormap(obj=True), origin='lower')
            self.ylim = (y1, y2)
        else:
            self.image.set_data(S)
        Smax = S.max()
        self.image.set_clim((Smax - self.dynrange / 10, Smax))
        self.draw()
        return


class SpecViewer(TSViewer.TSViewer):
    """ Combines a TSViewer panel with some spectrogram controls """

    def __init__(self, parent, id, figure=None, configfile=None):
        handler = SpecHandler(configfile=configfile)
        super(SpecViewer, self).__init__(parent, id, figure, handler=handler, configfile=configfile)


def test(soundfile):
    from ewave import wavfile
    fp = wavfile(soundfile)
    signal, Fs = fp.read(), fp.sampling_rate

    class SpecViewFrame(wx.Frame):

        def __init__(self, parent=None):
            super(SpecViewFrame, self).__init__(parent, title='TSViewer Test App', size=(1000,
                                                                                         300), style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
            self.figpanel = SpecViewer(self, -1)
            self.figpanel.plot_data(signal, Fs)

    app = wx.PySimpleApp()
    app.frame = SpecViewFrame()
    app.frame.Show()
    app.MainLoop()