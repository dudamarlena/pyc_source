# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/OpenGL/Interactor.py
# Compiled at: 2008-10-19 12:19:52
"""==================
General Interactor
==================

This component implements the basic functionality of an Interactor. An
Interactor listens to events of another component and tranlates them
into movement which is applied to the target component. It provides
methods to be overridden for adding functionality.

Example Usage
-------------
A very simple Interactor could look like this::

    class VerySimpleInteractor(Interactor):
        def makeInteractorLinkages(self):
            self.link( (self,"outbox"), (self.target, "rel_rotation") )
        
        def setup(self):
            self.addListenEvents([pygame.MOUSEBUTTONDOWN])
        
        def handleEvents(self):
            while self.dataReady("events"):
                event = self.recv("events")
                if self.identifier in event.hitobjects:
                    self.send((0,90,0))
            

For examples of how to create Interactors have a look at the files
XXXInteractor.py.

A MatchedInteractor and a RotationInteractor each interacting with a
SimpleCube::

    CUBE1 = SimpleCube(size=(1,1,1), position=(1,0,0)).activate()
    CUBE2 = SimpleCube(size=(1,1,1), position=(-1,0,0)).activate()
    INTERACTOR1 = MatchedTranslationInteractor(target=CUBE1).activate()
    INTERACTOR2 = SimpleRotationInteractor(target=CUBE2).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  

How does it work?
-----------------
Interactor provides functionality for interaction with the OpenGL
display service and OpenGL components. It is designed to be subclassed.
The following methods are provided to be overridden:

- makeInteractorLinkages() -- make linkages to and from targets needed
- setup()                  -- set up the component
- handleEvents()           -- handle input events ("events" inbox)
- frame()                  -- called every frame, to add additional functionality

Stubs method are provided, so missing these out does not result in
broken code. The methods get called from the main method, the following
code shows in which order::

    def main(self):
        # create and send eventspy request
        ...
        # setup function from derived objects
        self.setup()        
        ...
        while 1:
            yield 1
            # handle events function from derived objects
            self.handleEvents()
            # frame function from derived objects
            self.frame()

If you need to override the __init__() method, e.g. to get
initialisation parameters, make sure to pass on all keyword arguments to
__init__(...) of the superclass, e.g.::

    def __init__(self, **argd):
        super(ClassName, self).__init__(**argd)
        # get an initialisation parameter
        myparam = argd.get("myparam", defaultvalue)
        
The following methods are provided to be used by inherited objects:

- addListenEvents(list of events) -- Request reception of a list of events
- removeListenEvents(list of events) -- Stop reveiving events

The are inteded to simplify component handling. For their functionality
see their description.

The event identifier of the target component gets saved in
self.identifier. Use this variable in event handling to determine if the
target component has been hit.

Interactor components terminate if a producerFinished or
shutdownMicroprocess message is received on their "control" inbox. The
received message is also forwarded to the "signal" outbox. Upon
termination, this component does *not* unbind itself from the
OpenGLDisplay service and does not free any requested resources.

"""
import pygame
from pygame.locals import *
from OpenGLDisplay import *
import Axon

class Interactor(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """    Interactor(...) -> A new Interactor object (not very useful, designed to be subclassed)
    
    This component implements the basic functionality of an Interactor. An
    Interactor listens to events of another component and tranlates them
    into movement which is applied to the target component. It provides
    methods to be overridden for adding functionality.
    
    Keyword arguments:
    
    - target    -- OpenGL component to interact with
    - nolink    -- if True, no linkages are made (default=False)
    """
    Inboxes = {'inbox': 'not used', 
       'control': 'For shutdown messages', 
       'events': 'Input events', 
       'callback': 'for the response after a displayrequest'}
    Outboxes = {'outbox': 'used for sending relative tranlational movement', 
       'signal': 'For shutdown messages', 
       'display_signal': 'Outbox used for communicating to the display surface'}

    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Interactor, self).__init__()
        displayservice = OpenGLDisplay.getDisplayService()
        self.link((self, 'display_signal'), displayservice)
        self.target = argd.get('target')
        self.nolink = argd.get('nolink', False)

    def main(self):
        self.eventspyrequest = {'EVENTSPYREQUEST': True, 'objectid': id(self), 
           'target': id(self.target), 
           'callback': (
                      self, 'callback'), 
           'events': (
                    self, 'events')}
        self.send(self.eventspyrequest, 'display_signal')
        self.setup()
        while not self.dataReady('callback'):
            yield 1

        self.identifier = self.recv('callback')
        while 1:
            yield 1
            while self.dataReady('control'):
                cmsg = self.recv('control')
                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                    self.send(cmsg, 'signal')
                    return

            self.handleEvents()
            self.frame()

    def addListenEvents(self, events):
        """        Sends listening request for pygame events to the display service.
        The events parameter is expected to be a list of pygame event constants.
        """
        for event in events:
            self.send({'ADDLISTENEVENT': event, 'objectid': id(self)}, 'display_signal')

    def removeListenEvents(self, events):
        """        Sends stop listening request for pygame events to the display service.
        The events parameter is expected to be a list of pygame event constants.
        """
        for event in events:
            self.send({'REMOVELISTENEVENT': event, 'objectid': id(self)}, 'display_signal')

    def makeInteractorLinkages(self):
        """ Method stub """
        pass

    def handleEvents(self):
        """
        Method stub
        
        Override this method to do event handling inside.
        Should look like this::

            while self.dataReady("events"):
                event = self.recv("events")
                # handle event ...
        
        """
        pass

    def setup(self):
        """
        Method stub
        
        Override this method for component setup.
        It will be called on the first scheduling of the component.
        """
        pass

    def frame(self):
        """
        Method stub
        
        Override this method for operations you want to do every frame.
        It will be called every time the component is scheduled. Do not
        include infinite loops, the method has to return every time it
        gets called.
        """
        pass


__kamaelia_components__ = (
 Interactor,)