# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/lamson/mail.py
# Compiled at: 2011-05-21 19:39:14
"""
The lamson.mail module contains nothing more than wrappers around the big work
done in lamson.encoding.  These are the actual APIs that you'll interact with
when doing email, and they mostly replicate the lamson.encoding.MailBase 
functionality.

The main design criteria is that MailRequest is mostly for reading email 
that you've received, so it doesn't have functions for attaching files and such.
MailResponse is used when you are going to write an email, so it has the
APIs for doing attachments and such.
"""
import mimetypes
from lamson import encoding, bounce
from email.utils import parseaddr
import os, warnings
ROUTABLE_TO_HEADER = 'to'

def _decode_header_randomness(addr):
    """
    This fixes the given address so that it is *always* a set() of 
    just email addresses suitable for routing.
    """
    if not addr:
        return set()
    if isinstance(addr, list):
        return set(parseaddr(a.lower())[1] for a in addr)
    if isinstance(addr, basestring):
        return set([parseaddr(addr.lower())[1]])
    raise encoding.EncodingError('Address must be a string or a list not: %r', type(addr))


class MailRequest(object):
    """
    This is what's handed to your handlers for you to process.  The information
    you get out of this is *ALWAYS* in Python unicode and should be usable 
    by any API.  Modifying this object will cause other handlers that deal
    with it to get your modifications, but in general you don't want to do
    more than maybe tag a few headers.
    """

    def __init__(self, Peer, From, To, Data):
        """
        Peer is the remote peer making the connection (sometimes the queue
        name).  From and To are what you think they are.  Data is the raw
        full email as received by the server.

        NOTE:  It does not handle multiple From headers, if that's even
        possible.  It will parse the From into a list and take the first
        one.
        """
        self.original = Data
        self.base = encoding.from_string(Data)
        self.Peer = Peer
        self.From = From or self.base['from']
        self.To = To or self.base[ROUTABLE_TO_HEADER]
        if 'from' not in self.base:
            self.base['from'] = self.From
        if 'to' not in self.base:
            self.base['to'] = self.To
        self.route_to = _decode_header_randomness(self.To)
        self.route_from = _decode_header_randomness(self.From)
        if self.route_from:
            self.route_from = self.route_from.pop()
        else:
            self.route_from = None
        self.bounce = None
        return

    def all_parts(self):
        """Returns all multipart mime parts.  This could be an empty list."""
        return self.base.parts

    def body(self):
        """
        Always returns a body if there is one.  If the message
        is multipart then it returns the first part's body, if
        it's not then it just returns the body.  If returns
        None then this message has nothing for a body.
        """
        if self.base.parts:
            return self.base.parts[0].body
        else:
            return self.base.body

    def __contains__(self, key):
        return self.base.__contains__(key)

    def __getitem__(self, name):
        return self.base.__getitem__(name)

    def __setitem__(self, name, val):
        self.base.__setitem__(name, val)

    def __delitem__(self, name):
        del self.base[name]

    def __str__(self):
        """
        Converts this to a string usable for storage into a queue or 
        transmission.
        """
        return encoding.to_string(self.base)

    def __repr__(self):
        return 'From: %r' % [self.Peer, self.From, self.To]

    def keys(self):
        return self.base.keys()

    def to_message(self):
        """
        Converts this to a Python email message you can use to
        interact with the python mail APIs.
        """
        return encoding.to_message(self.base)

    def walk(self):
        """Recursively walks all attached parts and their children."""
        for x in self.base.walk():
            yield x

    def is_bounce(self, threshold=0.3):
        """
        Determines whether the message is a bounce message based on 
        lamson.bounce.BounceAnalzyer given threshold.  0.3 is a good
        conservative base.
        """
        if not self.bounce:
            self.bounce = bounce.detect(self)
        if self.bounce.score > threshold:
            return True
        else:
            return False

    @property
    def msg(self):
        warnings.warn('The .msg attribute is deprecated, use .base instead.  This will be gone in Lamson 1.0', category=DeprecationWarning, stacklevel=2)
        return self.base


class MailResponse(object):
    """
    You are given MailResponse objects from the lamson.view methods, and
    whenever you want to generate an email to send to someone.  It has
    the same basic functionality as MailRequest, but it is designed to
    be written to, rather than read from (although you can do both).

    You can easily set a Body or Html during creation or after by
    passing it as __init__ parameters, or by setting those attributes.

    You can initially set the From, To, and Subject, but they are headers so
    use the dict notation to change them:  msg['From'] = 'joe@test.com'.

    The message is not fully crafted until right when you convert it with
    MailResponse.to_message.  This lets you change it and work with it, then
    send it out when it's ready.
    """

    def __init__(self, To=None, From=None, Subject=None, Body=None, Html=None):
        self.Body = Body
        self.Html = Html
        self.base = encoding.MailBase([('To', To), ('From', From), ('Subject', Subject)])
        self.multipart = self.Body and self.Html
        self.attachments = []

    def __contains__(self, key):
        return self.base.__contains__(key)

    def __getitem__(self, key):
        return self.base.__getitem__(key)

    def __setitem__(self, key, val):
        return self.base.__setitem__(key, val)

    def __delitem__(self, name):
        del self.base[name]

    def attach--- This code section failed: ---

 L. 205         0  LOAD_FAST             1  'filename'
                3  POP_JUMP_IF_TRUE     21  'to 21'
                6  LOAD_FAST             3  'data'
                9  POP_JUMP_IF_TRUE     21  'to 21'
               12  LOAD_ASSERT              AssertionError
               15  LOAD_CONST               'You must give a filename or some data to attach.'
               18  RAISE_VARARGS_2       2  None

 L. 206        21  LOAD_FAST             3  'data'
               24  POP_JUMP_IF_TRUE     54  'to 54'
               27  LOAD_GLOBAL           1  'os'
               30  LOAD_ATTR             2  'path'
               33  LOAD_ATTR             3  'exists'
               36  LOAD_FAST             1  'filename'
               39  CALL_FUNCTION_1       1  None
               42  POP_JUMP_IF_TRUE     54  'to 54'
               45  LOAD_ASSERT              AssertionError
               48  LOAD_CONST               "File doesn't exist, and no data given."
               51  RAISE_VARARGS_2       2  None

 L. 208        54  LOAD_GLOBAL           4  'True'
               57  LOAD_FAST             0  'self'
               60  STORE_ATTR            5  'multipart'

 L. 210        63  LOAD_FAST             1  'filename'
               66  POP_JUMP_IF_FALSE   100  'to 100'
               69  LOAD_FAST             2  'content_type'
               72  UNARY_NOT        
             73_0  COME_FROM            66  '66'
               73  POP_JUMP_IF_FALSE   100  'to 100'

 L. 211        76  LOAD_GLOBAL           6  'mimetypes'
               79  LOAD_ATTR             7  'guess_type'
               82  LOAD_FAST             1  'filename'
               85  CALL_FUNCTION_1       1  None
               88  UNPACK_SEQUENCE_2     2 
               91  STORE_FAST            2  'content_type'
               94  STORE_FAST            5  'encoding'
               97  JUMP_FORWARD          0  'to 100'
            100_0  COME_FROM            97  '97'

 L. 213       100  LOAD_FAST             2  'content_type'
              103  POP_JUMP_IF_TRUE    119  'to 119'
              106  LOAD_ASSERT              AssertionError
              109  LOAD_CONST               "No content type given, and couldn't guess from the filename: %r"
              112  LOAD_FAST             1  'filename'
              115  BINARY_MODULO    
              116  RAISE_VARARGS_2       2  None

 L. 215       119  LOAD_FAST             0  'self'
              122  LOAD_ATTR             8  'attachments'
              125  LOAD_ATTR             9  'append'
              128  BUILD_MAP_4           4  None
              131  LOAD_FAST             1  'filename'
              134  LOAD_CONST               'filename'
              137  STORE_MAP        

 L. 216       138  LOAD_FAST             2  'content_type'
              141  LOAD_CONST               'content_type'
              144  STORE_MAP        

 L. 217       145  LOAD_FAST             3  'data'
              148  LOAD_CONST               'data'
              151  STORE_MAP        

 L. 218       152  LOAD_FAST             4  'disposition'
              155  LOAD_CONST               'disposition'
              158  STORE_MAP        
              159  CALL_FUNCTION_1       1  None
              162  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 159

    def attach_part(self, part):
        """
        Attaches a raw MailBase part from a MailRequest (or anywhere)
        so that you can copy it over.
        """
        self.multipart = True
        self.attachments.append({'filename': None, 'content_type': None, 
           'data': None, 
           'disposition': None, 
           'part': part})
        return

    def attach_all_parts(self, mail_request):
        """
        Used for copying the attachment parts of a mail.MailRequest
        object for mailing lists that need to maintain attachments.
        """
        for part in mail_request.all_parts():
            self.attach_part(part)

        self.base.content_encoding = mail_request.base.content_encoding.copy()

    def clear(self):
        """
        Clears out the attachments so you can redo them.  Use this to keep the
        headers for a series of different messages with different attachments.
        """
        del self.attachments[:]
        del self.base.parts[:]
        self.multipart = False

    def update(self, message):
        """
        Used to easily set a bunch of heading from another dict
        like object.
        """
        for k in message.keys():
            self.base[k] = message[k]

    def __str__(self):
        """
        Converts to a string.
        """
        return self.to_message().as_string()

    def _encode_attachment(self, filename=None, content_type=None, data=None, disposition=None, part=None):
        """
        Used internally to take the attachments mentioned in self.attachments
        and do the actual encoding in a lazy way when you call to_message.
        """
        if part:
            self.base.parts.append(part)
        elif filename:
            if not data:
                data = open(filename).read()
            self.base.attach_file(filename, data, content_type, disposition or 'attachment')
        else:
            self.base.attach_text(data, content_type)
        ctype = self.base.content_encoding['Content-Type'][0]
        if ctype and not ctype.startswith('multipart'):
            self.base.content_encoding['Content-Type'] = (
             'multipart/mixed', {})

    def to_message(self):
        """
        Figures out all the required steps to finally craft the
        message you need and return it.  The resulting message
        is also available as a self.base attribute.

        What is returned is a Python email API message you can
        use with those APIs.  The self.base attribute is the raw
        lamson.encoding.MailBase.
        """
        del self.base.parts[:]
        if self.Body and self.Html:
            self.multipart = True
            self.base.content_encoding['Content-Type'] = ('multipart/alternative', {})
        if self.multipart:
            self.base.body = None
            if self.Body:
                self.base.attach_text(self.Body, 'text/plain')
            if self.Html:
                self.base.attach_text(self.Html, 'text/html')
            for args in self.attachments:
                self._encode_attachment(**args)

        elif self.Body:
            self.base.body = self.Body
            self.base.content_encoding['Content-Type'] = ('text/plain', {})
        elif self.Html:
            self.base.body = self.Html
            self.base.content_encoding['Content-Type'] = ('text/html', {})
        return encoding.to_message(self.base)

    def all_parts(self):
        """
        Returns all the encoded parts.  Only useful for debugging
        or inspecting after calling to_message().
        """
        return self.base.parts

    def keys(self):
        return self.base.keys()

    @property
    def msg(self):
        warnings.warn('The .msg attribute is deprecated, use .base instead.  This will be gone in Lamson 1.0', category=DeprecationWarning, stacklevel=2)
        return self.base