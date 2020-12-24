# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/yaco/applyfun/httplogger.py
# Compiled at: 2008-06-13 07:08:02
"""
This has been extracted from the excellent ZSyncer product, by Paul M. Winkler and contributors.
It basically allows to send log messages from the server to the browser.
"""
import time, logging
from DocumentTemplate.DT_Util import html_quote
color_200 = 'green'
color_error = 'red'

class TextMsg:
    """For logging & output of arbitrary text.
    """
    __module__ = __name__
    color = 'black'
    status = 200

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)

    def html(self):
        return '<div style="color: %s">%s</div>\n' % (self.color, html_quote(self.msg))


class StatusMsg(TextMsg):
    """For logging & output of remote call results.
    """
    __module__ = __name__

    def __init__(self, msg, status, color=None):
        """msg may be a text string or a TextMsg.
        """
        status = int(status)
        if isinstance(msg, TextMsg):
            msg = msg.msg
        self.status = status
        if color:
            self.color = color
            self.msg = msg
        elif status == 200:
            self.color = color_200
            if not msg.startswith('OK'):
                msg = 'OK: %s' % msg
            self.msg = msg
        else:
            self.color = color_error
            self.msg = msg

    def __eq__(self, other):
        return other.msg == self.msg and other.status == self.status

    def __repr__(self):
        return '%s("%s", %s)' % (self.__class__.__name__, self.msg, self.status)


from Products.PythonScripts.Utility import allow_class
allow_class(StatusMsg)
allow_class(TextMsg)

class HTTPLogger(object):
    __module__ = __name__

    def __init__(self, context=None, REQUEST=None):
        self.REQUEST = REQUEST
        self.log = logging
        self.context = context
        self.remote = REQUEST and True or False

    def get_time(self):
        return time.asctime(time.localtime(time.time()))

    def make_msg(self, msg, status=200, color=None):
        """
        From a string, make a StatusMsg
        """
        if isinstance(msg, StatusMsg):
            return msg
        return StatusMsg(msg, status, color)

    def do_messages(self, msgs):
        """Log a list of messages, and if there is a REQUEST, do an
        html display.
        """
        self.msg_header()
        processed_msgs = []
        for m in msgs:
            if isinstance(m, StatusMsg):
                processed_msgs.append(m)
            else:
                processed_msgs.append(StatusMsg(m))

        for m in processed_msgs:
            self.do_one_msg(m)

        self.msg_footer()
        return processed_msgs

    def msg_header(self):
        """Writes log and/or html info at beginning of a sync.
        """
        if self.remote:
            self.REQUEST.RESPONSE.setHeader('content-type', 'text/html')
            head = '<html><body>'
            self.REQUEST.RESPONSE.write(head)
        self.log.info(' -------  Started logging  -------')

    def msg_footer(self):
        if self.remote:
            url_back = self.context and self.context.absolute_url() or 'javascript:history.back(2)'
            foot = '<div>\n                <a href="%s">BACK TO CONTEXT</a>\n                </div>\n                </body></html>\n            ' % url_back
            self.REQUEST.RESPONSE.write(foot)
        self.log.info(' -------  Done logging  -------  ')

    def do_one_msg(self, msg):
        """Log and/or display a single Msg.
        """
        msg = self.make_msg(msg)
        if self.remote:
            html = msg.html()
            self.REQUEST.RESPONSE.write(str(html))
            self.REQUEST.RESPONSE.flush()
        self.log.info(msg.msg)