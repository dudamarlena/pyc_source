# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/util/taurusscreenshot.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides Qt color management for taurus"""
__all__ = [
 'Grabber', 'grabWidget']
__docformat__ = 'restructuredtext'
import time, threading, os.path
from taurus.external.qt import Qt
from taurus.core.util.log import Logger
_LOGGER = None

def _getLogger():
    global _LOGGER
    if _LOGGER is None:
        _LOGGER = Logger('Grabber')
    return _LOGGER


class GrabberThread(threading.Thread):

    def __init__(self, widget, fileName, period):
        threading.Thread.__init__(self, name='Grabber')
        self.daemon = True
        if period <= 0:
            raise ValueError('period MUST be greater than 0')
        self._period = period
        self._continue = True
        self._grabber = Grabber(widget, fileName)

    def run(self):
        period = self._period
        while self._continue:
            self._grabber.grabTrigger()
            time.sleep(period)

    def stop(self):
        self._continue = False


class Grabber(Qt.QObject, Logger):
    grab = Qt.pyqtSignal()

    def __init__(self, widget, fileName):
        Qt.QObject.__init__(self)
        Logger.__init__(self)
        self._widget = widget
        self._fileName = fileName
        self.grab.connect(self.onGrab)

    def grabTrigger(self):
        self.grab.emit()

    def onGrab(self):
        Grabber._grabWidget(self._widget, self._fileName)

    @staticmethod
    def _grabWidget(widget, fileName):
        _getLogger().debug("Grabbing widget to '%s':", fileName)
        try:
            pixmap = Qt.QPixmap.grabWidget(widget)
            if fileName.endswith('.svg'):
                from taurus.external.qt import QtSvg
                generator = QtSvg.QSvgGenerator()
                generator.setFileName(fileName)
                generator.setSize(pixmap.size())
                if hasattr(generator, 'setViewBox'):
                    viewBox = Qt.QRect(Qt.QPoint(0, 0), pixmap.size())
                    generator.setViewBox(viewBox)
                generator.setTitle('Taurus widget')
                generator.setDescription('An SVG drawing created by the taurus widget grabber')
                painter = Qt.QPainter()
                painter.begin(generator)
                try:
                    painter.drawPixmap(0, 0, -1, -1, pixmap)
                finally:
                    painter.end()

            else:
                pixmap.save(fileName, quality=100)
        except:
            _getLogger().warning("Could not save file into '%s':", fileName, exc_info=1)

    @staticmethod
    def grabWidget(widget, fileName, period=None):
        """Grabs the given widget into the given image filename. If period is
        not given (or given with None) means grab immediately once and return.
        If period is given and >0 means grab the image every period seconds

        .. warning:
            this method **MUST** be called from the same thread which created
            the widget

        :param widget: (Qt.QWidget) the qt widget to be grabbed
        :param fileName: (str) the name of the image file
        :param period: (float) period (seconds)
        """
        if period is None:
            return Grabber._grabWidget(widget, fileName)
        else:
            ret = GrabberThread(widget, fileName, period)
            ret.start()
            return ret


def grabWidget(widget, fileName, period=None):
    return Grabber.grabWidget(widget, fileName, period=period)


grabWidget.__doc__ = Grabber.grabWidget.__doc__