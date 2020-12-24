# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: VideoAnalysis/Helms.py
# Compiled at: 2014-12-16 15:21:52
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, os, cv2, inspect, PIL, copy, sys
from cStringIO import StringIO
import numpy as np, wormtracker as wt
from functools import total_ordering
from collections import OrderedDict
from IPython import get_ipython
from IPython.html.widgets import FloatTextWidget, HTMLWidget, ButtonWidget, ContainerWidget, TextWidget, PopupWidget, TabWidget, IntTextWidget, TextWidget, CheckboxWidget, IntSliderWidget, RadioButtonsWidget
from IPython.html.widgets.widget import CallbackDispatcher
from IPython.utils.traitlets import Unicode, Instance
from IPython.display import display, display_javascript, clear_output, Javascript
from ROIWidgets import ROILineWidget, ROIMultiRectWidget, ROIMultiEllipseWidget
from Avery.interaction.widgets import FileChoiceWidget, AlertWidget
from wormtracker.wormimageprocessor import WormImageProcessor, cropImageToRegion
from VideoAnalysis import argNames, filterArgs, firstFrame, HTMLImageWidget, Rectangle, PlotToImage, Capturing

class WormImageProcessor2(WormImageProcessor, object):
    """
    WormImageProcessor2 is a WormImageProcessor that allows
    wormAreaThresholdRange[0] and wormAreaThresholdRange[1] to be set
    and retrieved through the pseudoattributes wormAreaThresholdLB and
    wormAreaThresholdUB.
    """

    def __getattr__(self, name):
        if name == 'wormAreaThresholdLB':
            return self.wormAreaThresholdRange[0]
        if name == 'wormAreaThresholdUB':
            return self.wormAreaThresholdRange[1]
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'wormAreaThresholdLB':
            self.wormAreaThresholdRange[0] = value
        elif name == 'wormAreaThresholdUB':
            self.wormAreaThresholdRange[1] = value
        else:
            super(WormImageProcessor2, self).__setattr__(name, value)

    def upcast(self):
        """
        Return a copy of the WormImageProcessor2 converted to
        WormImageProcessor.
        """
        wip = WormImageProcessor()
        for k, v in self.__dict__.items():
            setattr(wip, k, v)

        return wip


class DefaultParameterSets(object):

    @staticmethod
    def helmsParams(params=None):
        """
        Return a list of video analysis parameters formatted for
        passing to VideoParameterWidget.

        Arguments:
        ----------
        params=None: A list of input parameters. Each parameter is
            represented by a dict with 'name', 'value', 'description',
            and (optionally) 'type' keys. 
        """
        defaultParams = [
         {'name': 'expectedWormWidth', 'description': 'Expected Worm Width', 
            'value': 70, 
            'type': int},
         {'name': 'expectedWormLength', 'description': 'Expected Worm Length', 
            'value': 1000, 
            'type': int},
         {'name': 'wormAreaThresholdLB', 'description': 'Worm Area Threshold Lower Bound', 
            'value': 0.5, 
            'type': float},
         {'name': 'wormAreaThresholdUB', 'description': 'Worm Area Threshold Upper Bound', 
            'value': 1.5, 
            'type': float},
         {'name': 'numberOfPosturePoints', 'description': 'Number of Posture Points', 
            'value': 30, 
            'type': int},
         {'name': 'backgroundDiskRadius', 'description': 'Background Disk Radius', 
            'value': 5, 
            'type': int},
         {'name': 'threshold', 'description': 'Threshold', 
            'value': 0.9, 
            'type': float},
         {'name': 'wormDiskRadius', 'description': 'Worm Disk Radius', 
            'value': 2, 
            'type': int},
         {'name': 'resultsStorePath', 'description': 'Results Store Path', 
            'value': '/worms', 
            'type': str},
         {'name': 'videoInfoStorePath', 'description': 'Video Info Store Path', 
            'value': '/video', 
            'type': str}]
        wip = WormImageProcessor2()
        for p in defaultParams:
            setattr(wip, p['name'], p['value'])

        if params == None:
            inp = defaultParams
        else:
            inp = params
            for p in inp:
                setattr(wip, p['name'], p['value'])

        if 'numberOfPosturePoints' in inp:
            wip.determineNumberOfPosturePoints()
        outp = [ {'name': p['name'], 'description': p['description'], 'value': getattr(wip, p['name'], 0.0), 'type': p['type']} for p in inp
               ]
        return outp


class VideoConfigWidget(TabWidget):
    """
    Widget for multistep configuration of a video analysis.

    The VideoConfigWidget is a TabWidget that leads the user through
    the configuration process. There are five steps: Choose Files,
    Calibrate, Regions, Food Regions, and Parameters. When first
    created, the VideoConfigWidget has only a single tab, Choose
    Files. As each step is completed, a tab is added for the next step
    and the new tab becomes active, leading the user through the
    configuration. Submission of the final tab, Parameters, fires the
    submit method of the VideoConfigWidget.

    After submission, the value attribute contains a dict with the
    following keys: 'configFile', 'cropRegions', 'frameRate',
    'nFrames', 'numberFrames', 'pixelSize', 'pixelsPerMicron',
    'referenceDistance', 'resultsStorePath', 'storeFile', 'videoFile',
    'videoInfoStorePath', 'wormImageProcessor'. In addition, the video
    attribute is a WormVideo object with appropriately set attributes.
    """
    description = Unicode(sync=True)

    def __init__(self, description='', resultsStorePath='/worms', videoInfoStorePath='/video', videoDir=os.getcwdu(), resultsDir=os.getcwdu(), configDir=os.getcwdu(), **kwargs):
        """
        Create a VideoConfigWidget

        Parameters:
        -----------
        description=u'': Widget description
        resultsStorePath='/worms', videoInfoStorePath='/video':
            default dataset store paths for the data file. (Can be
            changed at the Parameters step.)
        videoDir=os.getcwdu(), resultsDir=os.getcwdu(),
            configDir=os.getcwdu(): initial directories for the Choose
            Files step.

        Any keyword parameters in addition to these are passed on to
        the component FileChoiceWidget, VideoCalibrateWidget,
        RegionWidget, FoodRegionWidget, or VideoParameterWidget or the
        parent TabWidget. 
        """
        super(VideoConfigWidget, self).__init__(description=description, **kwargs)
        self.description = description
        self.videoDir = videoDir
        self.resultsDir = resultsDir
        self.configDir = configDir
        self.value = {}
        self.value['resultsStorePath'] = resultsStorePath
        self.value['videoInfoStorePath'] = videoInfoStorePath
        self.submissionCallbacks = CallbackDispatcher()
        self.cancelCallbacks = CallbackDispatcher()
        self.stubWidget = TextWidget(value=' ', description='Stub')
        self.on_displayed(self.onDisplay)
        self.addFCW(**kwargs)

    __init__.argNames = lambda : argNames(TabWidget, VideoFileChoiceWidget, VideoCalibrateWidget, RegionWidget, FoodRegionWidget, VideoParameterWidget)

    def on_submit(self, callback, remove=False):
        """
        (Un)Register a callback to handle result submission.

        Triggered when the user clicks the Done button.

        Parameters
        ----------
        callback: callable
            Will be called with exactly one argument: the Widget instance
        remove: bool (optional)
            Whether to unregister the callback
        """
        self.submissionCallbacks.register_callback(callback, remove=remove)

    def on_cancel(self, callback, remove=False):
        """
        (Un)Register a callback to cancel calibration.

        Triggered when the user clicks the Cancel button. (The Cancel
        button will not appear until a callback is registered.)

        Parameters
        ----------
        callback: callable
            Will be called with exactly one argument: the Widget instance
        remove: bool (optional)
            Whether to unregister the callback
        """
        self.cancelCallbacks.register_callback(callback, remove=remove)

    def cancel(self, name=None):
        """Fire cancel callbacks."""
        self.cancelCallbacks(self)

    def submit(self, name=None):
        """Fire submit callbacks."""
        self.submissionCallbacks(self)

    def onDisplay(self, name=None):
        titles = [ self.get_title(i) for i in range(len(self.children)) ]
        self.children = (
         self.stubWidget,) + self.children
        self.set_title(0, 'Stub')
        self.selected_index = 0
        self.children = self.children[1:]
        for i, t in enumerate(titles):
            self.set_title(i, t)

        try:
            self.selected_index = self.current_tab
        except AttributeError:
            pass

        self.children[self.current_tab].onDisplay()

    def addFCW(self, **kwargs):
        """Add the FileChoiceWidget."""
        wArgs, otherArgs = filterArgs(VideoFileChoiceWidget, **kwargs)
        self.fcw = VideoFileChoiceWidget(videoDir=self.videoDir, resultsDir=self.resultsDir, configDir=self.configDir, description='Choose Files', **wArgs)
        self.fcw.on_submit(self.onFCWSubmit)
        self.fcw.vaw = self
        self.fcw.index = len(self.children)
        self.children += (self.fcw,)
        self.set_title(self.fcw.index, self.fcw.description)
        self.current_tab = self.fcw.index
        self.onDisplay()

    def onFCWSubmit(self, name=None):
        self.value.update(self.fcw.value)
        self.value['videoFile'] = str(self.value['videoFile'])
        self.value['storeFile'] = str(self.value['storeFile'])
        self.value['configFile'] = str(self.value['configFile'])
        videoFile = self.value['videoFile']
        if not videoFile:
            raise Error('Video file must be specified')
        video = cv2.VideoCapture(videoFile)
        if not video.isOpened():
            raise Error('Unable to open video file ' + videoFile)
        success, firstFrame = video.read()
        if not success:
            raise Error('Unable to read video file ' + videoFile)
        self.image = firstFrame
        self.value['nFrames'] = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        self.value['frameRate'] = round(video.get(cv2.cv.CV_CAP_PROP_FPS), 3)
        video.release()
        self.image = PIL.Image.fromarray(self.image)
        self.image = self.image.convert('L')
        self.image = np.array(self.image)
        self.addVCW()

    def addVCW(self, **kwargs):
        """Add the VideoCalibrateWidget."""
        wArgs, otherArgs = filterArgs(VideoCalibrateWidget, **kwargs)
        self.vcw = VideoCalibrateWidget(description='Calibrate', image=self.image, frameRate=self.value['frameRate'], videoFile=self.value['videoFile'], **wArgs)
        self.vcw.on_submit(self.onVCWSubmit)
        self.vcw.on_cancel(self.cancel)
        self.vcw.vaw = self
        self.vcw.index = len(self.children)
        self.children += (self.vcw,)
        self.set_title(self.vcw.index, self.vcw.description)
        self.current_tab = self.vcw.index
        self.onDisplay()

    def onVCWSubmit(self, name=None):
        self.value.update(self.vcw.value)
        self.wip2 = WormImageProcessor2()
        self.wip2.pixelSize = self.value['pixelsPerMicron']
        self.value['wormImageProcessor'] = self.wip2.upcast()
        self.addRW()

    def addRW(self, **kwargs):
        """Add the RegionWidget."""
        wArgs, otherArgs = filterArgs(RegionWidget, **kwargs)
        self.rw = RegionWidget(description='Regions', image=self.image, videoFile=self.value['videoFile'], **wArgs)
        self.rw.on_submit(self.onRWSubmit)
        self.rw.on_cancel(self.cancel)
        self.rw.vaw = self
        self.rw.index = len(self.children)
        self.children += (self.rw,)
        self.set_title(self.rw.index, self.rw.description)
        self.current_tab = self.rw.index
        self.onDisplay()

    def onRWSubmit(self, name=None):
        nRegions = len(self.rw.value['cropRegions'])
        self.regions = [ wt.WormVideoRegion(videoFile=self.value['videoFile'], imageProcessor=self.wip2, resultsStoreFile=self.value['storeFile'], cropRegion=self.rw.value['cropRegions'][i], pixelSize=self.value['pixelsPerMicron'], resultsStorePath=self.value['resultsStorePath'], strainName=self.rw.value['strainName'], wormName=self.rw.value['wormNames'][i]) for i in range(nRegions)
                       ]
        self.addFRW()

    def addFRW(self, **kwargs):
        """Add the FoodRegionWidget."""
        wArgs, otherArgs = filterArgs(FoodRegionWidget, **kwargs)
        self.frw = FoodRegionWidget(description='Food Regions', image=self.image, videoFile=self.value['videoFile'], **wArgs)
        self.frw.on_submit(self.onFRWSubmit)
        self.frw.on_cancel(self.cancel)
        self.frw.index = len(self.children)
        self.children += (self.frw,)
        self.set_title(self.frw.index, self.frw.description)
        self.current_tab = self.frw.index
        self.onDisplay()

    def onFRWSubmit(self, name=None):
        """Assign food circles to regions, then proceed to parameters."""
        assignCirclesToRegions(self.frw.value['foodCircles'], self.regions)
        self.addVPW()

    def addVPW(self, **kwargs):
        """Add the VideoParameterWidget."""
        wArgs, otherArgs = filterArgs(VideoParameterWidget, **kwargs)
        params = DefaultParameterSets.helmsParams()
        self.vpw = VideoParameterWidget(params=params, cropRegions=self.regions, description='Parameters', image=self.image, videoFile=self.value['videoFile'], **wArgs)
        self.vpw.on_submit(self.onVPWSubmit)
        self.vpw.on_cancel(self.cancel)
        self.vpw.vaw = self
        self.vpw.index = len(self.children)
        self.children += (self.vpw,)
        self.set_title(self.vpw.index, self.vpw.description)
        self.current_tab = self.vpw.index
        self.onDisplay()

    def onVPWSubmit(self, name=None):
        """Finish."""
        self.video = wt.WormVideo(videoFile=str(self.value['videoFile']), storeFile=str(self.value['storeFile']), videoInfoStorePath=str(self.value['videoInfoStorePath']), resultsStorePath=str(self.value['resultsStorePath']), numberOfRegions=len(self.regions), allSameStrain=True, referenceDistance=float(self.value['referenceDistance']))
        wip = self.wip2.upcast()
        self.video.imageProcessor = wip
        self.video.pixelsPerMicron = self.value['pixelsPerMicron']
        self.video.regions = copy.deepcopy(self.regions)
        for r in self.video.regions:
            r.imageProcessor = wip

        self.value['cropRegions'] = self.video.regions
        self.frameSize = self.image.shape
        self.nFrames = self.value['numberFrames']
        self.logFile = self.value['videoFile'] + '_.log'
        self.submit(name)


class VideoFileChoiceWidget(ContainerWidget):
    """
    The VideoFileChoiceWidget contains three FileChoiceWidgets, one
    for the input video file, one for the output analysis results
    (called the store file), and one for the configuration fle. It
    fires a submission event when all have been set. Upon submission,
    .value contains a dict with keys 'videoFile', 'storeFile', and
    'configFile' whose values are paths to the three files.
    """
    description = Unicode(sync=True)
    value = Instance(object, sync=True)

    def __init__(self, videoDir='./video', videoFilter='*.avi', resultsDir='./out', resultsFilter='*.h5', configDir='./out', configFilter='*.yml', **kwargs):
        """
        Create a VideoFileChoiceWidget.

        Parameters:
        -----------
        videoDir: initial directory for the video file.
        videoFilter=u'*.avi': filter for the video file.
        resultsDir: initial directory for the store file.
        resultsFilter=u'*.h5': filter for the store file.
        configDir: initial directory for the config file.
        configFilter=u'*.yml': filter for the config file.
        """
        super(VideoFileChoiceWidget, self).__init__(**kwargs)
        self.vfw = FileChoiceWidget(dir=videoDir, filter=videoFilter, description='Video:')
        self.sfw = FileChoiceWidget(dir=resultsDir, filter=resultsFilter, description='Store:', newFile=True)
        self.cfw = FileChoiceWidget(dir=configDir, filter=configFilter, description='Config:', newFile=True)
        self.vscw = ContainerWidget(children=[self.vfw, self.sfw])
        self.children = [self.vscw, self.cfw]
        self.vfwSet = self.sfwSet = self.cfwSet = self.set = False
        self.vfw.on_submit(self.onVFWSubmit)
        self.sfw.on_submit(self.onSFWSubmit)
        self.cfw.on_submit(self.onCFWSubmit)
        self.value = {'videoFile': '', 'storeFile': '', 'configFile': ''}
        self.submissionCallbacks = CallbackDispatcher()
        self.on_displayed(self.onDisplay)

    __init__.argNames = lambda : argNames(ContainerWidget)

    def onDisplay(self, name=None):
        """Place the FileChoiceWidgets side-by-side."""
        self.vscw.remove_class('vbox')
        self.vscw.add_class('hbox')
        self.set_css('width', '100%')
        self.add_class('center')

    def onVFWSubmit(self, name=None):
        self.value['videoFile'] = self.vfw.value
        self.vfwSet = True
        self.testSet()

    def onSFWSubmit(self, name=None):
        self.value['storeFile'] = self.sfw.value
        self.sfwSet = True
        self.testSet()

    def onCFWSubmit(self, name=None):
        self.value['configFile'] = self.cfw.value
        self.cfwSet = True
        self.testSet()

    def testSet(self):
        """Fire submission callbacks once both files set"""
        self.set = self.vfwSet and self.sfwSet and self.cfwSet
        if self.set:
            self.submissionCallbacks(self)

    def on_submit(self, callback, remove=False):
        """(Un)Register a callback to handle choice submission.

        Triggered when the user clicks enter.

        Parameters
        ----------
        callback: callable
            Will be called with exactly one argument: the Widget instance
        remove: bool (optional)
            Whether to unregister the callback"""
        self.submissionCallbacks.register_callback(callback, remove=remove)


class VideoROIWidget(ContainerWidget):
    """
    VideoROIWidget is an abstract (more-or-less) superclass for the
    video ROI widgets.
    """
    description = Unicode(sync=True)
    value = Instance(object, sync=True)

    def __init__(self, image=None, scratchDir=None, videoFile=None, description='', **kwargs):
        """
        Create a VideoROIWidget.

        Parameters:
        -----------
        image: The background image, either as a numpy ndarray, or a
            PIL image. 
        scratchDir: the scratch directory in which to store images for
            web retrieval. Defaults to <static_dir>/scratch. 
        videoFile: The video to be analyzed. The first frame will be
            used as the background image. One of image or videoFile
            must be supplied. If the image is taken from a video file,
            it may be retrieved as the image instance variable.
        description=u'': Widget description.
        """
        super(VideoROIWidget, self).__init__(**kwargs)
        if image is not None and image.any():
            self.image = image
        else:
            if not videoFile:
                raise Error('Either image or videoFile must be specified')
            video = cv2.VideoCapture(videoFile)
            if not video.isOpened():
                raise Error('Unable to open video file ' + videoFile)
            success, firstFrame = video.read()
            if not success:
                raise Error('Unable to read video file ' + videoFile)
            self.image = firstFrame
            self.nFrames = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
            self.frameRate = round(video.get(cv2.cv.CV_CAP_PROP_FPS), 3)
            video.release()
        self.description = description
        self.value = {}
        self.submissionCallbacks = CallbackDispatcher()
        self.cancelCallbacks = CallbackDispatcher()
        self.insw = HTMLWidget(value=self.toHTML(''))
        self.donew = ButtonWidget(description='Done')
        self.donew.on_click(self.submit)
        self.cancelw = ButtonWidget(description='Cancel')
        self.cancelw.on_click(self.cancel)
        self.cancelw.visible = False
        self.binsw = ContainerWidget()
        self.binsw.on_displayed(self.sideBySide)
        self.alertw = AlertWidget()
        self.children = [self.binsw, self.alertw]
        self.on_displayed(self.onDisplay)
        return

    __init__.argNames = lambda : argNames(ContainerWidget)

    def onDisplay(self, name=None):
        self.sideBySide(name)

    def sideBySide(self, name=None):
        """Arrange children horizontally."""
        self.binsw.remove_class('vbox')
        self.binsw.add_class('hbox')
        self.binsw.add_class('center')

    def toHTML(self, text):
        """Convert text to HTML."""
        html = '<table><tr height=40><th width=15 />\n'
        html += '<th style="vertical-align: center;"><b>' + text + '</b></th>'
        html += '<th width=15 /></tr></table>'
        return html

    def setInstructions(self, text):
        self.insw.value = self.toHTML(text)

    def submit(self, name=None):
        """
        Calculate and submit results when Done button clicked.

        This is more-or-less an abstract method. You should override
        it, but call the superclass method AFTER you have set
        self.value correctly.
        """
        self.send('value')
        self.submissionCallbacks(self)

    def cancel(self, name=None):
        """Fire cancel callbacks."""
        self.cancelCallbacks(self)

    def alert(self, text):
        """Pop up and alert to the user."""
        self.alertw.value = text

    def on_submit(self, callback, remove=False):
        """
        (Un)Register a callback to handle result submission.

        Triggered when the user clicks the Done button.

        Parameters
        ----------
        callback: callable
            Will be called with exactly one argument: the Widget instance
        remove: bool (optional)
            Whether to unregister the callback
        """
        self.submissionCallbacks.register_callback(callback, remove=remove)

    def on_cancel(self, callback, remove=False):
        """
        (Un)Register a callback to cancel calibration.

        Triggered when the user clicks the Cancel button. (The Cancel
        button will not appear until a callback is registered.)

        Parameters
        ----------
        callback: callable
            Will be called with exactly one argument: the Widget instance
        remove: bool (optional)
            Whether to unregister the callback
        """
        self.cancelw.visible = True
        self.cancelCallbacks.register_callback(callback, remove=remove)


class VideoCalibrateWidget(VideoROIWidget):
    """
    The VideoCalibrateWidget allows user calibration before video
    analysis to set frame rate and pixel size. Frame rate is set by a
    text field. To determine pixel size, the user draws on an image a
    line of a defined reference length. The reference length is set
    by a second text field. When finished, the user clicks a Done
    button and the widget fires a submission event. Upon submission,
    .value contains a dict with keys pixelsPerMicron, pixelSize,
    frameRate, and referenceDistance. numberFrames may also be
    specified, if this information was learned in opening a video
    file. 
    """
    description = Unicode(sync=True)
    value = Instance(object, sync=True)

    def __init__(self, image=None, videoFile=None, frameRate=None, referenceDistance=25000, description='', **kwargs):
        """
        Create a VideoCalibrateWidget.

        Parameters:
        -----------
        image: The background image, either as a numpy ndarray, or a
            PIL image. 
        videoFile: The video to be analyzed. The first frame will be
            used as the background image. One of image or videoFile
            must be supplied. If the image is taken from a video file,
            it may be retrieved as the image instance variable.
        frameRate: Initial value of the video frame rate field. If not
            supplied and there is a videoFile, will be read from that.
        referenceDistance=25000: Initial value of the reference
            distance field, in micrometers. This will be converted to
            mm in the user instructions. 
        description=u'': Widget description.
        """
        super(VideoCalibrateWidget, self).__init__(image=image, videoFile=videoFile, description=description, **kwargs)
        defaultFrameRate = 11.5
        try:
            frameRate = frameRate and frameRate > 0.0 or self.frameRate and self.frameRate > 0.0 or defaultFrameRate
        except AttributeError:
            frameRate = defaultFrameRate

        try:
            nFrames = self.nFrames
        except AttributeError:
            nFrames = 'undefined'

        self.value = {'frameRate': frameRate, 'numberFrames': nFrames, 'referenceDistance': referenceDistance, 
           'pixelsPerMicron': 1.0, 
           'pixelSize': 1.0}
        self.frw = FloatTextWidget(value=frameRate, description='Frame rate:')
        self.frw.on_trait_change(self.onFRChange, name='value')
        self.mmDistance = referenceDistance / 1000.0
        self.rdw = FloatTextWidget(value=self.mmDistance, description='Reference:')
        self.rdw.on_trait_change(self.onRefChange, name='value')
        instruction = 'Draw a {:.1f} mm line on the figure'
        instruction = instruction.format(self.mmDistance)
        self.insw.value = self.toHTML(instruction)
        self.sw = ROILineWidget(self.image)
        self.binsw.children = [self.frw, self.rdw, self.insw,
         self.donew, self.cancelw]
        self.children = list(self.children) + [self.sw]

    __init__.argNames = lambda : argNames(VideoROIWidget)

    def onRefChange(self, name, value):
        """
        Reference distance change handler: record new value and update
        instructions.
        """
        self.mmDistance = self.rdw.value
        self.value['referenceDistance'] = 1000.0 * self.mmDistance
        instruction = 'Draw a {:.1f} mm line on the figure'
        instruction = instruction.format(self.mmDistance)
        self.insw.value = self.toHTML(instruction)

    def onFRChange(self, name, value):
        """Framerate change handler: record new rate."""
        self.value['frameRate'] = self.frw.value

    def submit(self, name=None):
        """
        Calculate pixel size and submit results when Done button
        clicked.
        """
        handles = self.sw.scaledHandles()
        if handles.shape != (2, 2):
            self.alert('You must draw a line on the image.')
            return
        d = float(np.linalg.norm(handles[1] - handles[0]))
        pixelSize = 1000.0 * self.rdw.value / d
        self.value['pixelSize'] = pixelSize
        self.value['pixelsPerMicron'] = 1.0 / pixelSize
        super(VideoCalibrateWidget, self).submit(name)


class RegionWidget(VideoROIWidget):
    """
    The RegionWidget allows the user to define any number of
    rectangular regions for analysis. A strain name can also be
    set. To submit the results, click the Done button. Upon
    submission, .value is a dict with the following keys:
    'strainName': the strain name (duh).
    'cropRegions': a list of rectangles. Each rectangle is represented
        by an [x, y, w, h] list. The numbers are of type float.
    'wormNames': A list of str's, onme for each region. This is
        currently set to the text representation of the numbers from 1
        to n.
    """
    description = Unicode(sync=True)
    value = Instance(object, sync=True)

    def __init__(self, image=None, videoFile=None, strainName='N2', description='', **kwargs):
        """
        Create a RegionWidget.

        Parameters:
        -----------
        image: The background image, either as a numpy ndarray, or a
            PIL image. 
        videoFile: The video to be analyzed. The first frame will be
            used as the background image. One of image or videoFile
            must be supplied. If the image is taken from a video file,
            it may be retrieved as the image instance variable.
        strainName=u'N2': The initial strain name.
        description=u'': Widget description.
        """
        super(RegionWidget, self).__init__(image=image, videoFile=videoFile, description=description, **kwargs)
        self.value = {'strainName': strainName, 'wormNames': [], 'cropRegions': []}
        self.submissionCallbacks = CallbackDispatcher()
        self.cancelCallbacks = CallbackDispatcher()
        instruction = 'Draw a rectangle for each region to be analyzed.'
        self.setInstructions(instruction)
        self.snw = TextWidget(value=strainName, description='strain name:')
        self.snw.on_trait_change(self.onSNChange, name='value')
        self.rw = ROIMultiRectWidget(self.image)
        self.binsw.children = [self.snw, self.insw,
         self.donew, self.cancelw]
        self.children = list(self.children) + [self.rw]

    __init__.argNames = lambda : argNames(VideoROIWidget)

    def onSNChange(self, name, value):
        """
        Strain name change handler: record new value.
        """
        self.value['strainName'] = self.snw.value

    def submit(self, name=None):
        """
        Record strain and region names and submit.
        """
        handles = self.rw.scaledHandles()
        if len(handles) % 2 != 0:
            raise Error("Can't happen: odd number of handles " + 'from Rectangle Widget.')
        rects = [ Rectangle(*handles[i:i + 2].T) for i in range(0, len(handles), 2)
                ]
        rects = sorted(rects)
        n = len(rects)
        self.value['wormNames'] = [ str(i) for i in range(1, n + 1) ]
        self.value['cropRegions'] = [ [float(r.xi.lb), float(r.yi.lb), float(r.xi.ub - r.xi.lb), float(r.yi.ub - r.yi.lb)] for r in rects
                                    ]
        super(RegionWidget, self).submit(name)


class FoodRegionWidget(VideoROIWidget):
    """
    The FoodRegionWidget allows the user to define any number of
    circular regions for analysis. Upon submission, .value is a dict
    with the following key:
    'cropCircles': a list of circles. Each circle is represented by an
        [x, y, r] list. The numbers are of type float.

    FoodRegionWidget does not force the circles to correspond to the
    rectangular crop regions defined by a RegionWidget -- they are
    entirely independent.
    """
    description = Unicode(sync=True)
    value = Instance(object, sync=True)

    def __init__(self, image=None, videoFile=None, description='', **kwargs):
        """
        Create a FoodRegionWidget.

        Parameters:
        -----------
        image: The background image, either as a numpy ndarray, or a
            PIL image. 
        videoFile: The video to be analyzed. The first frame will be
            used as the background image. One of image or videoFile
            must be supplied. If the image is taken from a video file,
            it may be retrieved as the image instance variable.
        description=u'': Widget description.
        """
        super(FoodRegionWidget, self).__init__(image=image, videoFile=videoFile, description=description, **kwargs)
        self.value = {'foodCircles': []}
        self.submissionCallbacks = CallbackDispatcher()
        self.cancelCallbacks = CallbackDispatcher()
        instruction = 'Draw a circle covering the food for each region.'
        self.setInstructions(instruction)
        self.rw = ROIMultiEllipseWidget(self.image)
        self.binsw.children = [self.insw, self.donew, self.cancelw]
        self.children = list(self.children) + [self.rw]

    __init__.argNames = lambda : argNames(VideoROIWidget)

    def submit(self, name=None):
        """
        Record food circles and submit.
        """
        handles = self.rw.scaledHandles()
        if len(handles) % 2 != 0:
            raise Error("Can't happen: odd number of handles " + 'from Ellipse Widget.')
        ells = []
        for i in range(0, len(handles), 2):
            c = handles[i:i + 2].mean(axis=0)
            r = np.linalg.norm(handles[i] - c)
            ells.append([float(c[0]), float(c[1]), float(r)])

        self.value['foodCircles'] = ells
        super(FoodRegionWidget, self).submit(name)


def circleToRegion(circle, regions):
    """
    Find the region containing a circle

    Parameters:
    -----------
    circle: a tuple (x, y, r) defining the circle 
    regions: a list of WormVideoRegions to be searched. Falsy elements
        are ignored.

    Return:
    -------
    The index of the best matching region, or None

    Exceptions:
    -----------
    No region is found that contains the center of the circle
    """
    x, y, r = circle
    matches = [ i for i, reg in enumerate(regions) if reg and x - r >= reg.cropRegion[0] and x + r <= reg.cropRegion[0] + reg.cropRegion[2] and y - r >= reg.cropRegion[1] and y + r <= reg.cropRegion[1] + reg.cropRegion[3]
              ]
    if not matches:
        matches = [ i for i, reg in enumerate(regions) if reg and x >= reg.cropRegion[0] and x <= reg.cropRegion[0] + reg.cropRegion[2] and y >= reg.cropRegion[1] and y <= reg.cropRegion[1] + reg.cropRegion[3]
                  ]
    if not matches:
        raise Error('No region found matching circle')
    if 1 == len(matches):
        return matches[0]
    best = min(matches, key=lambda i: (x - regions[i].cropRegion[0] - regions[i].cropRegion[2] / 2.0) ** 2 + (y - regions[i].cropRegion[1] - regions[i].cropRegion[3] / 2.0) ** 2)
    return best


def assignCirclesToRegions(circles, regions):
    """
    Assign each circle to a region

    Parameters:
    -----------
    circles: a list of circles, each in (x, y, r) form regions: the
        list of WormVideoRegions to be searched. Each circle is
        assigned to one WormVideoRegion as its .foodCircle
        attribute. No region is assigned more than one circle.
    regions: A list of WormVideoRegions to which the circles are to be
        assigned.

    Return:
    -------
    regions (which has been modified in place)

    Exceptions:
    -----------
    If one or more circles can't be assigned, consistent with these
    constraints.

    This function is designed on the assumption that WormVideoRegions
    don't overlap. If this is not so, dysfunctional behavior may
    result.
    """
    rs = regions[:]
    for c in circles:
        index = circleToRegion(c, rs)
        rs[index].foodCircle = c
        rs[index] = None

    return regions


class VideoParameterWidget(ContainerWidget):
    """
    VideoParameterWidget is an all-purpose tool for editing the values
    of miscellaneous parameters used in the video analysis. The bottom
    half of the widget consists of a list of text fields, one for
    each parameter. However, it is somewhat specialized for image
    processing. The top half shows either the entire video frame being
    processed or the part of it corresponding to a single region,
    depending on whether the "Region" checkbox is checked. The region
    can be selected with a slider widget. To the left of this is a
    radiobutton widget used to select the stage of processing to be
    visualized. As usual, a "Done" and "Cancel" buttons signal
    completion.
    """
    description = Unicode(sync=True)
    value = Instance(object, sync=True)
    widgetTypes = {int: IntTextWidget, 
       float: FloatTextWidget, 
       str: TextWidget, 
       'filename': FileChoiceWidget}

    def __init__(self, params, cropRegions=None, image=None, videoFile=None, scratchDir=None, description='', pixelsPerMicron=None, **kwargs):
        """
        Create a VideoParameterWidget.

        Parameters:
        -----------
        params: a list of the user-settable parameters. Each element
            of the list is a dict with at least the keys 'name',
            'value', and 'description'. 'name' is the internal symbol
            by which this parameter is known (e.g. 'wormDiskRadius')
            and usually also the name of the corresponding
            WormImageProcessor attribute. (There are currently two
            exceptions: 'wormAreaThresholdLB'and
            'wormAreaThresholdUB' correspond to
            WormImageProcessor.wormAreaThresholdRange[0] and
            WormImageProcessor.wormAreaThresholdRange[1].)
            'description' is a user-friendly text description of the
            parameter. 'value' is the initial value. There may also be
            a 'type' key, which if present should be int, float, str,
            or the string 'filename'. If not provided,
            type(params[i]['value']) is used. is the initial value of
            this parameter.
            The 'filename' type is handled specially (of course). A
            FileChoiceWidget is presented, and 'value' should be a
            dict of keyword args to be passed to the constructor. 
        cropRegions: a list of the regions to be analyzed.
        image: an image used to illustrate processing
        videoFile: the videofile to be processed. At least one of
            image or videoFile must be specified. If a videoFile is
            supplied but not an image, the first frame of the video is
            used.
        scratchDir: the scratch directory in which to store images for
            web retrieval. Defaults to <static_dir>/scratch. 
        description=u'': Widget description.
        pixelsPerMicron: Scale calibration. If not supplied,
            cropRegions[0].imageProcessor.pixelSize is used. 
        """
        super(VideoParameterWidget, self).__init__(description=description, **kwargs)
        self.description = description
        if image is not None and image.any():
            self.image = image
        else:
            if not videoFile:
                raise Error('Either image or videoFile must be specified')
            self.image = firstFrame(videoFile)
        self.videoFile = videoFile
        self.image = PIL.Image.fromarray(self.image)
        self.image = self.image.convert('L')
        self.image = np.array(self.image)
        self.regions = cropRegions
        self.wip = WormImageProcessor2()
        if pixelsPerMicron:
            self.wip.pixelSize = pixelsPerMicron
        else:
            self.wip.pixelSize = self.regions[0].imageProcessor.pixelSize
        self.params = copy.deepcopy(params)
        self.value = {p['name']:p['value'] for p in self.params}
        children = []
        for p in self.params:
            html = '<div '
            html += 'style="min-width:40ex;padding-right:0px;padding-top:9px;text-align:right;vertical-align:text-top"'
            html += '>'
            html += p['description'] + ':'
            html += '</div>'
            p['label'] = HTMLWidget(value=html)
            t = p.get('type', None) or type(p['value']) or float
            widgetType = self.widgetTypes[t]
            if t == 'filename':
                p['field'] = widgetType(**p['value'])
            else:
                p['field'] = widgetType(value=p['value'])
                p['field'].on_trait_change(self.testChange, name='value')
            child = ContainerWidget(children=(p['label'], p['field']))
            children.append(child)

        self.submissionCallbacks = CallbackDispatcher()
        self.cancelCallbacks = CallbackDispatcher()
        self.insw = HTMLWidget(value=self.toHTML(''))
        self.donew = ButtonWidget(description='Done')
        self.donew.on_click(self.submit)
        self.cancelw = ButtonWidget(description='Cancel')
        self.cancelw.on_click(self.cancel)
        self.cancelw.visible = False
        self.testrbw = RadioButtonsWidget(description='Processing:', values=OrderedDict([
         (
          'Original', self.showOrig),
         (
          'Background Filter', self.testBkgd),
         (
          'Threshold', self.testThrs),
         (
          'Cleaning', self.testClean),
         (
          'Worm ID', self.testID)]), value=self.showOrig)
        self.testrbw.on_trait_change(self.testChange, name='value')
        self.regioncbw = CheckboxWidget(description='Region?')
        self.regionnw = IntSliderWidget(description='Number:', min=0, max=len(self.regions) - 1)
        self.testrbw.on_trait_change(self.testChange, name='value')
        self.regioncbw.on_trait_change(self.testChange, name='value')
        self.regionnw.on_trait_change(self.testChange, name='value')
        self.testw = ContainerWidget(children=[
         self.testrbw, self.regioncbw, self.regionnw])
        self.binsw = ContainerWidget()
        self.binsw.on_displayed(self.sideBySide)
        self.binsw.children = [self.insw, self.donew, self.cancelw]
        self.alertw = AlertWidget()
        self.imagew = HTMLImageWidget(self.image)
        self.descw = HTMLWidget(value=self.toHTML(''), visible=False)
        children[:0] = [
         self.imagew, self.descw, self.testw, self.binsw]
        self.children = children
        self.setInstructions('Set Parameter Values:')
        self.on_displayed(self.onDisplay)
        return

    __init__.argNames = lambda : argNames(ContainerWidget)

    def testChange(self, name=None):
        """
        testChange is triggered whenever the state of the widget
        changes. It updates the display of the processed image.
        """
        value = self.testrbw.value
        self.descw.visible = value == self.testID
        value()

    def cropToRegion(self):
        """
        Return the cropped or uncropped image to be processed
        """
        if not self.regioncbw.value:
            return self.image
        r = self.regions[self.regionnw.value].cropRegion
        return cropImageToRegion(self.image, r)

    def showOrig(self, name=None):
        """Show the original image"""
        orig = self.cropToRegion()
        self.imagew.setImage(orig)

    def testBkgd(self, name=None):
        """Apply background filtering."""
        self.applyParams()
        orig = self.cropToRegion()
        filtered = self.wip.applyBackgroundFilter(orig)
        self.imagew.setImage(filtered)

    def testThrs(self, name=None):
        """Background filtering + thresholding."""
        self.applyParams()
        orig = self.cropToRegion()
        filtered = self.wip.applyBackgroundFilter(orig)
        thresholded = self.wip.applyThreshold(filtered)
        self.imagew.setImage(thresholded)

    def testClean(self, name=None):
        """Background filtering + thresholding + morphological cleaning."""
        self.applyParams()
        orig = self.cropToRegion()
        filtered = self.wip.applyBackgroundFilter(orig)
        thresholded = self.wip.applyThreshold(filtered)
        cleaned = self.wip.applyMorphologicalCleaning(thresholded)
        self.imagew.setImage(cleaned)

    def testID(self, name=None):
        """Identify a worm. This also forces region viewing."""
        self.applyParams()
        if self.regioncbw.value:
            self.testIDRegion(name)
        else:
            self.testIDWhole(name)

    def testIDRegion(self, name=None):
        region = self.regions[self.regionnw.value]
        orig = self.cropToRegion()
        wip = region.imageProcessor
        self.applyParams(wip)
        filtered = wip.applyBackgroundFilter(orig)
        thresholded = wip.applyThreshold(filtered)
        cleaned = wip.applyMorphologicalCleaning(thresholded)
        possibleWorms = wip.identifyPossibleWorms(cleaned)
        desc = 'worm not found'
        success = False
        if len(possibleWorms) > 0:
            likelyWorm = max(possibleWorms, key=lambda worm: worm[1])
            if likelyWorm is not None:
                with PlotToImage(plt.figure()) as (pti):
                    wormImage = wt.WormImage(region, filtered, cleaned, likelyWorm[0])
                    wormImage.measureWorm()
                    wormImage.plot(bodyPtMarkerSize=30)
                    desc = ('{0} {1}: worm {2} um long, {3} um wide').format(region.strainName, region.wormName, wormImage.length, wormImage.width)
                    success = True
        identified = success and pti.image or cleaned
        self.descw.value = self.toHTML(desc)
        self.imagew.setImage(identified)
        return

    def testIDWhole(self, name=None):
        video = wt.WormVideo(videoFile=self.videoFile, numberOfRegions=len(self.regions))
        self.applyParams()
        for r in self.regions:
            r.imageProcessor = self.wip

        video.imageProcessor = self.wip
        video.pixelsPerMicron = self.wip.pixelSize
        video.regions = self.regions
        video.firstFrame = self.image
        with PlotToImage() as (pti):
            with Capturing() as (output):
                video.testWormIdentification()
        identified = pti.image
        self.descw.value = ''
        self.imagew.setImage(identified)

    def applyParams(self, wip=None):
        """
        Apply current parameter values to WormImageProcessor2
        """
        wip = wip or self.wip
        for p in self.params:
            setattr(wip, p['name'], p['field'].value)

    def onDisplay(self, name=None):
        """Triggered when the widget is displayed."""
        self.sideBySide(name)

    def sideBySide(self, name=None):
        """Arrange children horizontally."""
        self.binsw.remove_class('vbox')
        self.binsw.add_class('hbox')
        self.binsw.add_class('center')
        self.testw.remove_class('vbox')
        self.testw.add_class('hbox')
        self.testw.add_class('center')
        self.testrbw.remove_class('vbox')
        self.testrbw.add_class('hbox')
        self.testrbw.add_class('center')
        for w in self.children:
            w.remove_class('vbox')
            w.add_class('hbox')
            w.add_class('center')

    def toHTML(self, text):
        """Convert text to HTML."""
        html = '<table><tr height=40><th width=15 />\n'
        html += '<th style="vertical-align: center;"><b>' + text + '</b></th>'
        html += '<th width=15 /></tr></table>'
        return html

    def setInstructions(self, text):
        """Set or change the instructions."""
        self.insw.value = self.toHTML(text)

    def submit(self, name=None):
        """
        Calculate and submit results when Done button clicked.
        """
        for p in self.params:
            t = p.get('type', float)
            if t == 'filename':
                self.value[p['name']] = str(p['field'].value)
            else:
                self.value[p['name']] = t(p['field'].value)

        self.send('value')
        self.applyParams()
        for r in self.regions:
            self.applyParams(r.imageProcessor)

        self.submissionCallbacks(self)

    def cancel(self, name=None):
        """Fire cancel callbacks."""
        self.cancelCallbacks(self)

    def alert(self, text):
        """Pop up an alert to the user."""
        self.alertw.value = text

    def on_submit(self, callback, remove=False):
        """
        (Un)Register a callback to handle result submission.

        Triggered when the user clicks the Done button.

        Parameters
        ----------
        callback: callable
            Will be called with exactly one argument: the Widget instance
        remove: bool (optional)
            Whether to unregister the callback
        """
        self.submissionCallbacks.register_callback(callback, remove=remove)

    def on_cancel(self, callback, remove=False):
        """
        (Un)Register a callback to cancel calibration.

        Triggered when the user clicks the Cancel button. (The Cancel
        button will not appear until a callback is registered.)

        Parameters
        ----------
        callback: callable
            Will be called with exactly one argument: the Widget instance
        remove: bool (optional)
            Whether to unregister the callback
        """
        self.cancelw.visible = True
        self.cancelCallbacks.register_callback(callback, remove=remove)