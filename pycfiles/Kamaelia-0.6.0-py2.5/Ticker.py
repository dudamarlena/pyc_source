# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/Pygame/Ticker.py
# Compiled at: 2008-10-19 12:19:52
"""====================
Pygame text 'Ticker'
====================

Displays text in pygame a word at a time as a 'ticker'.

NOTE: This component is very much a work in progress. Its capabilities and API
is likely to change substantially in the near future.

Example Usage
-------------

Ticker displaying text from a file::

    Pipeline( RateControlledFileReader("textfile","lines",rate=1000),
              Ticker(position=(100,100))
            ).run()

How does it work?
-----------------

The component requests a display surface from the Pygame Display service
component. This is used as the ticker.

Send strings containing *lines of text* to the Ticker component. Do not send
strings with words split between one string and the next. It displays the
words as a 'ticker' one word at a time. Text is automatically wrapped from one
line to the next. Once the bottom of the ticker is reached, the text
automatically jump-scrolls up a line to make more room.

The text is normalised by the ticker. Multiple spaces between words are
collapsed to a single space. Linefeeds are ignored.

NOTE: 2 consecutive linefeeds currently results in a special message being
sent out of the "_displaysignal" outbox. This is work-in-progress aimed at new features.
It is only documented here for completeness and should not be relied upon.

You can set the text size, colour and line spacing. You can also set the
background colour, outline (border) colour and width. You can also specify the
size and position of the ticker

NOTE: Specifying the outline width currently does not work for any value other
than 1.

NOTE: Specify the size of the ticker with the render_right and render_bottom
arguments. Specifying render_left and render_top arguments with values other
than 1 results in parts of the ticker being obscured.

The ticker displays words at a constant rate - it self regulates its display
speed.

Whilst it is running, sending any message to the "pausebox" inbox will pause
the Ticker. It will continue to buffer incoming text. Any message sent to the
"unpausebox" inbox will cause the Ticker to resume.

Whilst running, you can change the transparency of the ticker by sending a value
to the "alphacontrol" inbox between 0 (fully transparent) and 255 (fully opaque)
inclusive.

If a producerFinished message is received on the "control" inbox, this component
will send its own producerFinished message to the "signal" outbox and will
terminate.

However, if the ticker is paused (message sent to "pausebox" inbox) then the
component will ignore messages on its "control" inbox until it is unpaused by
sending a message to its "unpausebox" inbox.
"""
import pygame, Axon
from Kamaelia.UI.GraphicDisplay import PygameDisplay
from Axon.Ipc import WaitComplete
import time

class Ticker(Axon.Component.component):
    """   Ticker(...) -> new Ticker component.

   A pygame based component that displays incoming text as a ticker.

   Keyword arguments (all optional):
   
   - text_height        -- Font size in points (default=39)
   - line_spacing       -- (default=text_height/7)
   - background_colour  -- (r,g,b) background colour of the ticker (default=(128,48,128))
   - text_colour        -- (r,g,b) colour of text (default=(232,232,48))
   - outline_colour     -- (r,g,b) colour of the outline border (default=background_colour)
   - outline_width      -- pixels width of the border (default=1)
   - position           -- (x,y) pixels location of the top left corner
   - render_left        -- pixels distance of left of text from left edge (default=1)
   - render_top         -- pixels distance of top of text from top edge (default=1)
   - render_right       -- pixels width of ticker (default=399)
   - render_bottom      -- pixels height of ticker (default=299)

   NOTE: render_left and render_top currently behave incorrectly if not set to 1
   """
    Inboxes = {'inbox': 'Specify (new) filename', 'control': 'NOT USED (yet)', 
       'alphacontrol': 'Transparency of the ticker (0=fully transparent, 255=fully opaque)', 
       'pausebox': 'Any message pauses the ticker', 
       'unpausebox': 'Any message unpauses the ticker', 
       '_displaycontrol': 'Shutdown messages & feedback from Pygame Display service'}
    Outboxes = {'outbox': 'NOT USED', 'signal': 'NOT USED (yet)', 
       '_displaysignal': 'Shutdown signalling & sending requests to Pygame Display service'}

    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Ticker, self).__init__()
        self.text_height = argd.get('text_height', 39)
        self.line_spacing = argd.get('line_spacing', self.text_height / 7)
        self.background_colour = argd.get('background_colour', (128, 48, 128))
        self.text_colour = argd.get('text_colour', (232, 232, 48))
        self.outline_colour = argd.get('outline_colour', self.background_colour)
        self.outline_width = argd.get('outline_width', 1)
        self.position = argd.get('position', (1, 1))
        self.render_area = pygame.Rect((argd.get('render_left', 1),
         argd.get('render_top', 1),
         argd.get('render_right', 399),
         argd.get('render_bottom', 299)))
        self.words_per_second = 8
        self.delay = 1.0 / self.words_per_second

    def waitBox(self, boxname):
        """Generator. yields 1 until data ready on the named inbox."""
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def clearDisplay(self):
        """Clears the ticker of any existing text."""
        self.display.fill(self.background_colour)
        self.renderBorder(self.display)
        self.send({'REDRAW': True, 'surface': self.display}, '_displaysignal')

    def renderBorder(self, display):
        """Draws a rectangle to form the 'border' of the ticker"""
        pygame.draw.rect(display, self.outline_colour, (
         self.render_area.left - self.outline_width,
         self.render_area.top - self.outline_width,
         self.render_area.width + self.outline_width,
         self.render_area.height + self.outline_width), self.outline_width)

    def requestDisplay(self, **argd):
        """      Generator. Gets a display surface from the Pygame Display service.

      Makes the request, then yields 1 until a display surface is returned.
      """
        displayservice = PygameDisplay.getDisplayService()
        self.link((self, '_displaysignal'), displayservice)
        self.send(argd, '_displaysignal')
        for _ in self.waitBox('_displaycontrol'):
            yield 1

        display = self.recv('_displaycontrol')
        self.display = display

    def handleAlpha(self):
        if self.dataReady('alphacontrol'):
            alpha = self.recv('alphacontrol')
            self.display.set_alpha(alpha)

    def main(self):
        """Main loop."""
        yield WaitComplete(self.requestDisplay(DISPLAYREQUEST=True, callback=(
         self, '_displaycontrol'), size=(
         self.render_area.width, self.render_area.height), position=self.position))
        display = self.display
        my_font = pygame.font.Font(None, self.text_height)
        initial_postition = (self.render_area.left, self.render_area.top)
        position = [self.render_area.left, self.render_area.top]
        self.clearDisplay()
        maxheight = 0
        last = time.time()
        blankcount = 0
        alpha = -1
        while 1:
            self.handleAlpha()
            if self.dataReady('control'):
                if self.dataReady('control'):
                    data = self.recv('control')
                    if isinstance(data, Axon.Ipc.producerFinished):
                        self.send(Axon.Ipc.producerFinished(message=display), 'signal')
                        return
            if self.dataReady('inbox'):
                word = self.recv('inbox')
                if word == '\n':
                    word = ''
                if '\n' in word:
                    lines = word.split('\n')[:-1]
                    word = 'BONG'
                else:
                    lines = [
                     word]
                c = len(lines)
                for line in lines:
                    word = line
                    words = line.split()
                    for word in words:
                        while time.time() - last < self.delay:
                            self.handleAlpha()
                            yield 1

                        self.handleAlpha()
                        if self.dataReady('pausebox'):
                            data = self.recv('pausebox')
                            while not self.dataReady('unpausebox'):
                                yield 1

                            self.recv('unpausebox')
                        if self.dataReady('control'):
                            if self.dataReady('control'):
                                data = self.recv('control')
                                if isinstance(data, Axon.Ipc.producerFinished):
                                    self.send(Axon.Ipc.producerFinished(message=display), 'signal')
                                    return
                        last = time.time()
                        word = ' ' + word
                        alpha = self.display.get_alpha()
                        self.display.set_alpha(255)
                        wordsize = my_font.size(word)
                        word_render = my_font.render(word, 1, self.text_colour)
                        if position[0] + wordsize[0] > self.render_area.right or c > 1:
                            position[0] = initial_postition[0]
                            if position[1] + (maxheight + self.line_spacing) * 2 > self.render_area.bottom:
                                display.set_colorkey(None)
                                display.blit(display, (
                                 self.render_area.left, self.render_area.top), (
                                 self.render_area.left, self.render_area.top + self.text_height + self.line_spacing,
                                 self.render_area.width - 1, position[1] - self.render_area.top))
                                pygame.draw.rect(display, self.background_colour, (
                                 self.render_area.left, position[1],
                                 self.render_area.width - 1, self.render_area.top + self.render_area.height - 1 - position[1]), 0)
                                if c > 1:
                                    c = c - 1
                            else:
                                position[1] += maxheight + self.line_spacing
                        display.blit(word_render, position)
                        self.send({'REDRAW': True, 'surface': self.display}, '_displaysignal')
                        position[0] += wordsize[0]
                        if wordsize[1] > maxheight:
                            maxheight = wordsize[1]
                        self.display.set_alpha(alpha)

            yield 1

        return


__kamaelia_components__ = (
 Ticker,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    text = "The lights begin to twinkle from the rocks;\nThe long day wanes; the slow moon climbs; the deep\nMoans round with many voices.  Come, my friends.\n'T is not too late to seek a newer world.Push off, and sitting well in order smite\nThe sounding furrows; for my purpose holds\nTo sail beyond the sunset, and the baths\nOf all the western stars, until I die.\nIt may be that the gulfs will wash us down;\nIt may be we shall touch the Happy Isles,\nAnd see the great Achilles, whom we knew.\nTho' much is taken, much abides; and tho'\nWe are not now that strength which in old days\nMoved earth and heaven, that which we are, we are,--\nOne equal temper of heroic hearts,\nMade weak by time and fate, but strong in will\nTo strive, to seek, to find, and not to yield.\n"

    class datasource(Axon.Component.component):

        def main(self):
            for x in text.split():
                self.send(x, 'outbox')
                yield 1


    for _ in range(6):
        Pipeline(datasource(), Ticker()).activate()

    Axon.Scheduler.scheduler.run.runThreads()