# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/Pygame/Multiclick.py
# Compiled at: 2008-10-19 12:19:52
"""================================
Pygame Multi-click Button Widget
================================

A button widget for pygame display surfaces. Sends a message when clicked. The
message can be different for each mouse button.

Uses the Pygame Display service.

Example Usage
-------------
Three buttons that output messages to the console::

    msgs = [ "button 1", "button 2", "button 3", "button 4", "button 5" ]
    button1 = Button(caption="Click different mouse buttons!",msgs=msgs).activate()
    
    ce = ConsoleEchoer().activate()
    button1.link( (button1,"outbox"), (ce,"inbox") )
    

How does it work?
-----------------

The component requests a display surface from the Pygame Display service
component. This is used as the surface of the button. It also binds event
listeners to the service, as appropriate.

Arguments to the constructor configure the appearance and behaviour of the
button component:

- If "msgs" is specified, then a different message can be specified for each
  mouse button. If it is not specified, then "msg" is used instead, for all
  buttons.
  
- If an output "msg" is not specified, the default is a tuple ("CLICK", id)
  where id is the self.id attribute of the component.

- you can set the text label, colour, margin size, size and position of the
  button

- if you do not specify the size yourself, the size will default to fit the
  caption of the button.

- the button can have a transparent background

If a producerFinished or shutdownMicroprocess message is received on its
"control" inbox. It is passed on out of its "signal" outbox and the component
terminates.

Upon termination, this component does *not* unbind itself from the Pygame Display
service. It does not deregister event handlers and does not relinquish the
display surface it requested.
"""
import pygame, Axon
from Axon.Ipc import producerFinished
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class Multiclick(Axon.Component.component):
    """   Multiclick(...) -> new Multiclick component.

   Create a button widget in pygame, using the Pygame Display service. Sends a
   message out of its outbox when clicked.

   Keyword arguments (all optional):
   
   - caption      -- text (default="Button <component id>")
   - position     -- (x,y) position of top left corner in pixels
   - margin       -- pixels margin between caption and button edge (default=8)
   - bgcolour     -- (r,g,b) fill colour (default=(224,224,224))
   - fgcolour     -- (r,g,b) text colour (default=(0,0,0))
   - msg          -- sent when clicked (default=("CLICK",self.id)) of msgs is not specified
   - msgs         -- list of messages. msgs[x] is sent when button X is clicked (default=None)
   - transparent  -- draw background transparent if True (default=False)
   - size         -- (width,height) pixels size of the button (default=scaled to fit caption)
   """
    Inboxes = {'inbox': 'Receive events from Pygame Display', 'control': 'Shutdown messages: shutdownMicroprocess or producerFinished', 
       'callback': 'Receive callbacks from Pygame Display'}
    Outboxes = {'outbox': 'button click events emitted here', 'signal': 'Shutdown signalling: shutdownMicroprocess or producerFinished', 
       'display_signal': 'For sending signals to the Pygame Display'}

    def __init__(self, caption=None, position=None, margin=8, bgcolour=(224, 224, 224), fgcolour=(0, 0, 0), msg=None, msgs=None, transparent=True, size=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Multiclick, self).__init__()
        self.backgroundColour = bgcolour
        self.foregroundColour = fgcolour
        self.margin = margin
        self.size = size
        self.msgs = msgs
        if caption is None:
            caption = 'Button ' + str(self.id)
        pygame.font.init()
        self.buildCaption(caption)
        if msg is None:
            msg = (
             'CLICK', self.id)
        self.eventMsg = msg
        if transparent:
            transparency = bgcolour
        else:
            transparency = None
        self.disprequest = {'DISPLAYREQUEST': True, 'callback': (self, 'callback'), 'events': (
                    self, 'inbox'), 
           'size': self.size, 
           'transparency': transparency}
        if position is not None:
            self.disprequest['position'] = position
        return

    def buildCaption(self, text):
        """Pre-render the text to go on the button label."""
        font = pygame.font.Font(None, 14)
        self.image = font.render(text, True, self.foregroundColour)
        (w, h) = self.image.get_size()
        if self.size is None:
            self.size = (
             w + 2 * self.margin, h + 2 * self.margin)
        self.imagePosition = (
         self.margin, self.margin)
        return

    def waitBox(self, boxname):
        """Generator. yields 1 until data ready on the named inbox."""
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def main(self):
        """Main loop."""
        displayservice = PygameDisplay.getDisplayService()
        self.link((self, 'display_signal'), displayservice)
        self.send(self.disprequest, 'display_signal')
        for _ in self.waitBox('callback'):
            yield 1

        self.display = self.recv('callback')
        self.blitToSurface()
        self.send({'ADDLISTENEVENT': pygame.MOUSEBUTTONDOWN, 'surface': self.display}, 'display_signal')
        done = False
        while not done:
            if self.dataReady('control'):
                cmsg = self.recv('control')
                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                    done = True
            while self.dataReady('inbox'):
                for event in self.recv('inbox'):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bounds = self.display.get_rect()
                        if bounds.collidepoint(*event.pos):
                            try:
                                message = self.msgs[event.button]
                            except KeyError:
                                continue
                            except IndexError:
                                continue
                            except TypeError:
                                message = self.eventMsg
                            else:
                                self.send(message, 'outbox')

            yield 1

    def blitToSurface(self):
        """Clears the background and renders the text label onto the button surface."""
        try:
            self.send({'REDRAW': True, 'surface': self.display}, 'display_signal')
            self.display.fill(self.backgroundColour)
            self.display.blit(self.image, self.imagePosition)
        except:
            pass


__kamaelia_components__ = (
 Multiclick,)
if __name__ == '__main__':
    pass