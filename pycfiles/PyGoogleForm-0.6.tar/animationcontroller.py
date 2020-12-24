# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pygoogleearth\animationcontroller.py
# Compiled at: 2009-09-26 22:10:50
import getime

class AnimationController(object):
    """
    This contains animation options and controls.
    
    Use this interface to control animation. To get an instance 
    of IAnimationControllerGE, call IApplicationGE::AnimationController.
    
    Note:
    This interface always reflects the current state of the application's 
    animation, even if changes occur after creation.
    """

    def __init__(self, comobject):
        self.ge_fc = comobject

    def __getattr__(self, name):
        if name == 'slider_time_interval':
            return self.ge_fc.SliderTimeInterval
        if name == 'current_time_interval':
            return self.gc_fc.CurrentTimeInterval
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'slider_time_interval':
            self.ge_fc.SliderTimeInterval = value
        elif name == 'current_time_interval':
            self.ge_fc.CurrentTimeInterval = value
        else:
            raise AttributeError

    def play(self):
        """
        Starts playing animation.

        Plays animation with current settings if available.
        """
        self.ge_fc.Play()

    def pause(self):
        """
        Pauses current animation.
        
        Pauses animation if one is playing.
        """
        self.ge_fc.Pause()