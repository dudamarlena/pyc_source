# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wareweb/notify.py
# Compiled at: 2006-10-22 17:17:11
import event
__all__ = ['Notify']

class Notify(object):
    """
    This allows you to queue messages to be displayed to the user on
    the next page the user reads.
    
    This allows you to give messages in response to POST requests,
    then redirect to a another page and display that message (e.g,
    'event added').

    Usage::

        class SitePage(Servlet):
            message = Notify()

        class MyPage(SitePage):
            def setup(self):
                if something_done:
                    self.message.write('All good!')
                    self.redirect(...)
            def respond(self):
                write header...
                if self.message:
                    self.write('<div class="message">%s</div>
'
                               % self.message.html)

    """
    __module__ = __name__

    def __addtoclass__(self, attr, cls):
        cls.listeners.append(self.servlet_event)
        self.name = attr

    def servlet_event(self, name, servlet, *args, **kw):
        if name == 'start_awake':
            setattr(servlet, self.name, Message(servlet))
        elif name == 'end_sleep':
            if getattr(servlet, '_notify_written', False):
                if 'notify.messages' in servlet.session:
                    del servlet.session['notify.messages']
        return event.Continue


class Message(object):
    __module__ = __name__

    def __init__(self, servlet):
        self.servlet = servlet

    def write(self, message):
        session = self.servlet.session
        messages = session.get('notify.messages') or []
        messages.append(message)
        session['notify.messages'] = messages

    def __nonzero__(self):
        return bool(self.servlet.session.get('notify.messages'))

    def html__get(self):
        messages = self.servlet.session.get('notify.messages') or []
        self.servlet._notify_written = True
        return self.peek

    html = property(html__get)

    def peek__get(self):
        messages = self.servlet.session.get('notify.messages') or []
        return ('<br>').join(messages)

    peek = property(peek__get)