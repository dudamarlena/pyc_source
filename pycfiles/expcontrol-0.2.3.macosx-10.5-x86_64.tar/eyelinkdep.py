# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jc01/miniconda2/envs/psychopyenv/lib/python2.7/site-packages/expcontrol/eyelinkdep.py
# Compiled at: 2016-05-13 13:21:44
"""Functionality for interfacing with an EyeLink (SR Research) eye tracker.
Assumes that their pylink package is on your path."""
import time, numpy, pylink

class EyeLinkTracker(object):
    """
    Handle common eye tracker tasks with a somewhat more intuitive
    interface than stock pylink.
    """

    def __init__(self, size=[
 1024, 768], calibscale=1.0, ip='100.1.1.1', bgcolor=[
 127, 127, 127], fgcolor=[255, 255, 255], targetdiameter=20, targethole=5, calibrationtype='HV9', calibrationpacing=0.9, viewdistance=None, screenwidth=None):
        self.size = tuple(size)
        self.tracker = pylink.EyeLink(ip)
        self.eyeused = None
        pylink.flushGetkeyQueue()
        self.tracker.setOfflineMode()
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.targetdiameter = targetdiameter
        self.targethole = targethole
        self.remotefilename = time.strftime('%m%d%H%M')
        self.tracker.openDataFile(self.remotefilename)
        self.calibsize = numpy.array(self.size) * calibscale
        calibarea = numpy.round(numpy.array(self.size) - self.calibsize)
        alldims = (calibarea[0], calibarea[1], self.calibsize[0],
         self.calibsize[1])
        self.tracker.sendCommand('screen_pixel_coords =  %d %d %d %d' % alldims)
        self.tracker.sendMessage('DISPLAY_COORDS  %d %d %d %d' % alldims)
        self.tracker.sendMessage('SCREEN_COORDS  0 0 %d %d' % self.size)
        if viewdistance:
            self.tracker.sendCommand('simulation_screen_distance=%d' % (viewdistance * 10))
            self.tracker.sendMessage('VIEW_DISTANCE %d' % (viewdistance * 10))
        self.tracker.sendCommand('automatic_calibration_pacing=%d' % (calibrationpacing * 1000))
        if screenwidth:
            self.tracker.sendMessage('SCREEN_WIDTH %d' % screenwidth)
        self.tracker.sendCommand('calibration_type=' + calibrationtype)
        if self.tracker.getTrackerVersion() == 2:
            self.tracker.sendCommand('select_parser_configuration 0')
        else:
            self.tracker.sendCommand('saccade_velocity_threshold = 35')
            self.tracker.sendCommand('saccade_acceleration_threshold = 9500')
            self.tracker.setFileEventFilter('LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON')
            self.tracker.setFileSampleFilter('LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS')
            self.tracker.setLinkEventFilter('LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON')
            self.tracker.setLinkSampleFilter('LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS')
            self.tracker.sendCommand("button_function 5 'accept_target_fixation'")
        return

    def calibrate(self):
        """
        Open a pygame window, run a calibration routine and close it.
        """
        pylink.openGraphics(self.size)
        pylink.setCalibrationColors(self.fgcolor, self.bgcolor)
        pylink.setTargetSize(self.targetdiameter, self.targethole)
        self.tracker.doTrackerSetup()
        self.eyeused = self.tracker.eyeAvailable()
        pylink.closeGraphics()

    def start(self):
        """
        start recording eye tracking data.
        """
        err = self.tracker.startRecording(1, 1, 1, 1)
        assert not err, 'EyeLink error: ' + err

    def message(self, msg):
        """
        send the str msg to the eye tracker.
        """
        self.tracker.sendMessage(msg)

    def stop(self, outfile):
        """
        stop recording and receive the data file if outfile is not None.
        """
        pylink.pumpDelay(100)
        self.tracker.setOfflineMode()
        pylink.msecDelay(500)
        self.tracker.closeDataFile()
        if outfile is not None:
            self.tracker.receiveDataFile(self.remotefilename, outfile)
        self.tracker.close()
        return