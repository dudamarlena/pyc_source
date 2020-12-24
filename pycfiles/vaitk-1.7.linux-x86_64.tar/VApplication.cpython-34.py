# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/gui/VApplication.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 13135 bytes
from .. import FocusPolicy
from .. import KeyModifier, Key
from .. import core
from . import events
from .VPalette import VPalette
from .VScreen import VScreen
from .events import VFocusEvent
from .VGraphicElements import VGraphicElements
import threading, queue, logging, time

class _VExceptionEvent:

    def __init__(self, exception):
        self.exception = exception


class _KeyEventThread(threading.Thread):
    __doc__ = "\n    Separate thread class to handle keyboard events\n    extracted from ncurses.\n    It communicates to the main thread in three ways:\n    - with a queue, where it puts all the key events\n    - and with an event flag, which is set when key events are available\n    - with the stop_thread flag, which stops the loop\n\n    the reason why we use the event_available_flag is because we have two\n    queues, one for the key events, and the other for the other events (timer etc).\n    We can't check the queues without altering them, so we need a flag to communicate\n    when either of the queues has something to fetch. (to be verified, I remember\n    I had to devise this solution due to limits of the queue object)\n\n    Important thing (for future resolution): the stop_event is pretty useless\n    since the thread stay stopped in getKeyCode and can't check the flag until\n    it leaves. Either I need to add a timer, or come up with a better solution.\n    In any case, the self.daemon flag should solve the problem, since the main\n    thread is free to quit even if the secondary daemon thread is still running.\n    "

    def __init__(self, screen, key_event_queue, event_available_flag):
        super().__init__()
        self.daemon = True
        self.stop_event = threading.Event()
        self.exception = None
        self._screen = screen
        self._key_event_queue = key_event_queue
        self.throttle = threading.Event()
        self._event_available_flag = event_available_flag

    def run(self):
        """
        Runs on the separate thread. Fetches key events from ncurses,
        converts them into vaitk key events, and post them into the key
        event queue for further processing from the main thread.
        """
        while not self.stop_event.is_set():
            last_event = (
             None, time.time())
            try:
                c = self._screen.getKeyCode()
                last_event = (
                 c, time.time())
                event = events.VKeyEvent.fromNativeKeyCode(c)
                if event is not None:
                    self._key_event_queue.put(event)
                    self._event_available_flag.set()
                    self.throttle.wait()
                    self.throttle.clear()
            except Exception as e:
                event = _VExceptionEvent(e)
                self._key_event_queue.put(event)
                self._event_available_flag.set()

    def registerTimer(self, timer):
        pass


class VApplication(core.VCoreApplication):

    def __init__(self, argv, screen=None):
        from . import VWidget
        super().__init__(argv)
        if screen is not None:
            self._screen = screen
        else:
            self._screen = VScreen()
        self._root_widget = None
        self._root_widget = VWidget()
        self._focus_widget = None
        self._palette = self.defaultPalette()
        self._event_available_flag = threading.Event()
        self._event_queue = queue.Queue()
        self._key_event_queue = queue.Queue()
        self._key_event_thread = _KeyEventThread(self._screen, self._key_event_queue, self._event_available_flag)
        self._delete_later_queue = []
        self._exit_flag = False
        self.lastWindowClosed = core.VSignal(self)
        self.focusChanged = core.VSignal(self)
        self._default_graphic_elements = VGraphicElements.ASCII

    def exec_(self):
        """
        Starts the event loop.
        """
        self._root_widget.show()
        self.processEvents(True)
        self._key_event_thread.start()
        while self._exit_flag != True:
            self.logger.info('Waiting for events')
            self._event_available_flag.wait()
            self._event_available_flag.clear()
            self.logger.info('Event available')
            self.processEvents(True)
            self._key_event_thread.throttle.set()

        self._exitCleanup()

    def processEvents(self, native=False):
        self.logger.info('++++---- %s processing events ---+++++' % ('Native' if native else 'Forced'))
        self._processKeyEvents()
        self._processRemainingEvents()
        self._sendPaintEvents()
        self._deleteScheduled()
        self.logger.info('===================================')
        self._screen.refresh()

    def postEvent(self, receiver, event):
        """
        Add an event to the event queue, to be delivered at a later time to receiver.

        Arguments:
            receiver: the intended receiver of the event
            event: a VEvent object
        """
        self.logger.info(' <posted ' + str(receiver) + ' ' + str(event))
        self._event_queue.put((receiver, event))
        self._event_available_flag.set()

    def exit(self):
        self._exit_flag = True

    def addTopLevelWidget(self, widget):
        self._root_widget.addChild(widget)

    def deleteLater(self, widget):
        self.logger.info('Added widget %s to deleteLater queue' % str(widget))
        self._delete_later_queue.append(widget)

    def screen(self):
        return self._screen

    def focusWidget(self):
        return self._focus_widget

    def setFocusWidget(self, widget):
        """
        Gives focus to the specified widget.
        Focused widgets are the one that will receive Key events.

        Arguments:
            widget: the widget to set as focused
        """
        if self._focus_widget is widget:
            return
        self.logger.info('Setting focus on widget %s.' % widget)
        if self._focus_widget is not None:
            self.logger.info('Focus out on widget %s.' % self._focus_widget)
            VApplication.vApp.postEvent(self._focus_widget, VFocusEvent(core.VEvent.EventType.FocusOut))
        self._focus_widget = None
        if widget is not None:
            if widget.focusPolicy() == FocusPolicy.NoFocus:
                self.logger.info('Focus not accepted on widget %s due to its focus policy.' % self._focus_widget)
                return
            self._focus_widget = widget
            VApplication.vApp.postEvent(self._focus_widget, VFocusEvent(core.VEvent.EventType.FocusIn))

    def defaultPalette(self):
        """
        Returns:
            the default palette of the application.
        """
        palette = VPalette()
        palette.setDefaults()
        return palette

    def palette(self):
        """
        Returns:
            the current palette of the application
        """
        return self._palette

    def defaultGraphicElements(self):
        return self._default_graphic_elements

    def setDefaultGraphicElements(self, graphic_elements):
        self._default_graphic_elements = graphic_elements

    def rootWidget(self):
        return self._root_widget

    def resetScreen(self):
        self._screen.reset()

    def topLevelWidgets(self):
        raise NotImplementedError()

    def allWidgets(self):
        raise NotImplementedError()

    def activeWindow(self):
        raise NotImplementedError()

    def setActiveWindow(self, window):
        raise NotImplementedError()

    def closeAllWindows(self):
        raise NotImplementedError()

    def event(self, event):
        raise NotImplementedError()

    def clipboard(self):
        raise NotImplementedError()

    def keyboardModifiers(self):
        raise NotImplementedError()

    def notify(self):
        raise NotImplementedError()

    def eventFilter(self, event):
        """
        Default event filter that is used when no other event interceptor catches the event.
        By default, this event filter reacts to Ctrl+C keyevents, quitting the application.

        Arguments:
            event: the VEvent

        """
        if event.key() == Key.Key_C:
            if event.modifiers() & KeyModifier.ControlModifier:
                self.exit()

    def _hideScheduled(self):
        self.logger.info('Widget scheduled for deletion: %s' % str(self._delete_later_queue))
        for w in self._delete_later_queue:
            self.logger.info('Posting hide events for deleted widget %s' % str(w))
            w.hide()

    def _deleteScheduled(self):
        for w in self._delete_later_queue:
            w.parent().removeChild(w)

        self._delete_later_queue.clear()

    def _processKeyEvents(self):
        while 1:
            self.logger.info('key queue %d' % self._key_event_queue.qsize())
            try:
                event = self._key_event_queue.get_nowait()
            except queue.Empty:
                event = None

            if event is None:
                return
            if isinstance(event, events.VKeyEvent):
                self._processSingleKeyEvent(event)
            elif isinstance(event, _VExceptionEvent):
                raise event.exception
                continue

    def _processSingleKeyEvent(self, key_event):
        self.logger.info('Key event %d %x' % (key_event.key(), key_event.modifiers()))
        key_event.setAccepted(False)
        focus_widget = self.focusWidget()
        if focus_widget:
            for widget in focus_widget.traverseToRoot():
                self.logger.info('KeyEvent attempting delivery to ' + str(widget))
                stop_event = False
                for event_filter in reversed(widget.installedEventFilters()):
                    stop_event = stop_event | event_filter.eventFilter(key_event)
                    if key_event.isAccepted():
                        self.logger.info('KeyEvent accepted by filter ' + str(event_filter))
                        return

                if not stop_event:
                    self.logger.info('KeyEvent not stopped. Sending to widget ' + str(widget))
                    widget.keyEvent(key_event)
                    if key_event.isAccepted():
                        self.logger.info('KeyEvent accepted by ' + str(widget))
                        return
                    continue

        self.eventFilter(key_event)

    def _processRemainingEvents(self):
        previous_data = None
        while 1:
            try:
                receiver, event = self._event_queue.get_nowait()
            except queue.Empty:
                receiver, event = (None, None)

            if event is None:
                break
            if previous_data is not None:
                prev_receiver, prev_event = previous_data
                if event.eventType() == prev_event.eventType():
                    if receiver == prev_receiver:
                        continue
                    self.logger.info('Data queue %d. Processing %s -> %s.' % (self._event_queue.qsize(), str(event), str(receiver)))
                    receiver.event(event)
                    previous_data = (receiver, event)

    def _sendPaintEvents(self):
        for w in self.rootWidget().depthFirstFullTree():
            if w.needsUpdate():
                for w2 in w.depthFirstRightTree():
                    if core.VRect.tuple.intersects(w.absoluteRect(), w2.absoluteRect()):
                        w2.update()
                        continue

                continue

        for w in self.rootWidget().depthFirstFullTree():
            if w.needsUpdate():
                w.event(events.VPaintEvent())
                continue

    def _exitCleanup(self):
        self._key_event_thread.stop_event.set()
        self._screen.reset()
        super().exit()