# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/backports/email/generator.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 19520 bytes
"""Classes to generate plain text from a message object tree."""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.builtins import super
from future.builtins import str
__all__ = [
 'Generator', 'DecodedGenerator', 'BytesGenerator']
import re, sys, time, random, warnings
from io import StringIO, BytesIO
from future.backports.email._policybase import compat32
from future.backports.email.header import Header
from future.backports.email.utils import _has_surrogates
import future.backports.email.charset as _charset
UNDERSCORE = '_'
NL = '\n'
fcre = re.compile('^From ', re.MULTILINE)

class Generator(object):
    __doc__ = 'Generates output from a Message object tree.\n\n    This basic generator writes the message to the given file object as plain\n    text.\n    '

    def __init__(self, outfp, mangle_from_=True, maxheaderlen=None, **_3to2kwargs):
        if 'policy' in _3to2kwargs:
            policy = _3to2kwargs['policy']
            del _3to2kwargs['policy']
        else:
            policy = None
        self._fp = outfp
        self._mangle_from_ = mangle_from_
        self.maxheaderlen = maxheaderlen
        self.policy = policy

    def write(self, s):
        self._fp.write(s)

    def flatten(self, msg, unixfrom=False, linesep=None):
        """Print the message object tree rooted at msg to the output file
        specified when the Generator instance was created.

        unixfrom is a flag that forces the printing of a Unix From_ delimiter
        before the first object in the message tree.  If the original message
        has no From_ delimiter, a `standard' one is crafted.  By default, this
        is False to inhibit the printing of any From_ delimiter.

        Note that for subobjects, no From_ line is printed.

        linesep specifies the characters used to indicate a new line in
        the output.  The default value is determined by the policy.

        """
        policy = msg.policy if self.policy is None else self.policy
        if linesep is not None:
            policy = policy.clone(linesep=linesep)
        if self.maxheaderlen is not None:
            policy = policy.clone(max_line_length=self.maxheaderlen)
        self._NL = policy.linesep
        self._encoded_NL = self._encode(self._NL)
        self._EMPTY = ''
        self._encoded_EMTPY = self._encode('')
        old_gen_policy = self.policy
        old_msg_policy = msg.policy
        try:
            self.policy = policy
            msg.policy = policy
            if unixfrom:
                ufrom = msg.get_unixfrom()
                if not ufrom:
                    ufrom = 'From nobody ' + time.ctime(time.time())
                self.write(ufrom + self._NL)
            self._write(msg)
        finally:
            self.policy = old_gen_policy
            msg.policy = old_msg_policy

    def clone(self, fp):
        """Clone this generator with the exact same options."""
        return self.__class__(fp, self._mangle_from_, None, policy=self.policy)

    _encoded_EMPTY = ''

    def _new_buffer(self):
        return StringIO()

    def _encode(self, s):
        return s

    def _write_lines(self, lines):
        if not lines:
            return
        lines = lines.splitlines(True)
        for line in lines[:-1]:
            self.write(line.rstrip('\r\n'))
            self.write(self._NL)

        laststripped = lines[(-1)].rstrip('\r\n')
        self.write(laststripped)
        if len(lines[(-1)]) != len(laststripped):
            self.write(self._NL)

    def _write(self, msg):
        oldfp = self._fp
        try:
            self._fp = sfp = self._new_buffer()
            self._dispatch(msg)
        finally:
            self._fp = oldfp

        meth = getattr(msg, '_write_headers', None)
        if meth is None:
            self._write_headers(msg)
        else:
            meth(self)
        self._fp.write(sfp.getvalue())

    def _dispatch(self, msg):
        main = msg.get_content_maintype()
        sub = msg.get_content_subtype()
        specific = UNDERSCORE.join((main, sub)).replace('-', '_')
        meth = getattr(self, '_handle_' + specific, None)
        if meth is None:
            generic = main.replace('-', '_')
            meth = getattr(self, '_handle_' + generic, None)
            if meth is None:
                meth = self._writeBody
        meth(msg)

    def _write_headers(self, msg):
        for h, v in msg.raw_items():
            self.write(self.policy.fold(h, v))

        self.write(self._NL)

    def _handle_text(self, msg):
        payload = msg.get_payload()
        if payload is None:
            return
        if not isinstance(payload, str):
            raise TypeError('string payload expected: %s' % type(payload))
        if _has_surrogates(msg._payload):
            charset = msg.get_param('charset')
            if charset is not None:
                del msg['content-transfer-encoding']
                msg.set_payload(payload, charset)
                payload = msg.get_payload()
        if self._mangle_from_:
            payload = fcre.sub('>From ', payload)
        self._write_lines(payload)

    _writeBody = _handle_text

    def _handle_multipart(self, msg):
        msgtexts = []
        subparts = msg.get_payload()
        if subparts is None:
            subparts = []
        elif isinstance(subparts, str):
            self.write(subparts)
            return
        if not isinstance(subparts, list):
            subparts = [subparts]
        for part in subparts:
            s = self._new_buffer()
            g = self.clone(s)
            g.flatten(part, unixfrom=False, linesep=self._NL)
            msgtexts.append(s.getvalue())

        boundary = msg.get_boundary()
        if not boundary:
            alltext = self._encoded_NL.join(msgtexts)
            boundary = self._make_boundary(alltext)
            msg.set_boundary(boundary)
        if msg.preamble is not None:
            if self._mangle_from_:
                preamble = fcre.sub('>From ', msg.preamble)
            else:
                preamble = msg.preamble
            self._write_lines(preamble)
            self.write(self._NL)
        self.write('--' + boundary + self._NL)
        if msgtexts:
            self._fp.write(msgtexts.pop(0))
        for body_part in msgtexts:
            self.write(self._NL + '--' + boundary + self._NL)
            self._fp.write(body_part)

        self.write(self._NL + '--' + boundary + '--')
        if msg.epilogue is not None:
            self.write(self._NL)
            if self._mangle_from_:
                epilogue = fcre.sub('>From ', msg.epilogue)
            else:
                epilogue = msg.epilogue
            self._write_lines(epilogue)

    def _handle_multipart_signed(self, msg):
        p = self.policy
        self.policy = p.clone(max_line_length=0)
        try:
            self._handle_multipart(msg)
        finally:
            self.policy = p

    def _handle_message_delivery_status(self, msg):
        blocks = []
        for part in msg.get_payload():
            s = self._new_buffer()
            g = self.clone(s)
            g.flatten(part, unixfrom=False, linesep=self._NL)
            text = s.getvalue()
            lines = text.split(self._encoded_NL)
            if lines and lines[(-1)] == self._encoded_EMPTY:
                blocks.append(self._encoded_NL.join(lines[:-1]))
            else:
                blocks.append(text)

        self._fp.write(self._encoded_NL.join(blocks))

    def _handle_message(self, msg):
        s = self._new_buffer()
        g = self.clone(s)
        payload = msg._payload
        if isinstance(payload, list):
            g.flatten(msg.get_payload(0), unixfrom=False, linesep=self._NL)
            payload = s.getvalue()
        else:
            payload = self._encode(payload)
        self._fp.write(payload)

    @classmethod
    def _make_boundary(cls, text=None):
        token = random.randrange(sys.maxsize)
        boundary = '===============' + _fmt % token + '=='
        if text is None:
            return boundary
        b = boundary
        counter = 0
        while True:
            cre = cls._compile_re('^--' + re.escape(b) + '(--)?$', re.MULTILINE)
            if not cre.search(text):
                break
            b = boundary + '.' + str(counter)
            counter += 1

        return b

    @classmethod
    def _compile_re(cls, s, flags):
        return re.compile(s, flags)


class BytesGenerator(Generator):
    __doc__ = 'Generates a bytes version of a Message object tree.\n\n    Functionally identical to the base Generator except that the output is\n    bytes and not string.  When surrogates were used in the input to encode\n    bytes, these are decoded back to bytes for output.  If the policy has\n    cte_type set to 7bit, then the message is transformed such that the\n    non-ASCII bytes are properly content transfer encoded, using the charset\n    unknown-8bit.\n\n    The outfp object must accept bytes in its write method.\n    '
    _encoded_EMPTY = b''

    def write(self, s):
        self._fp.write(str(s).encode('ascii', 'surrogateescape'))

    def _new_buffer(self):
        return BytesIO()

    def _encode(self, s):
        return s.encode('ascii')

    def _write_headers(self, msg):
        for h, v in msg.raw_items():
            self._fp.write(self.policy.fold_binary(h, v))

        self.write(self._NL)

    def _handle_text(self, msg):
        if msg._payload is None:
            return
        if _has_surrogates(msg._payload) and not self.policy.cte_type == '7bit':
            if self._mangle_from_:
                msg._payload = fcre.sub('>From ', msg._payload)
            self._write_lines(msg._payload)
        else:
            super(BytesGenerator, self)._handle_text(msg)

    _writeBody = _handle_text

    @classmethod
    def _compile_re(cls, s, flags):
        return re.compile(s.encode('ascii'), flags)


_FMT = '[Non-text (%(type)s) part of message omitted, filename %(filename)s]'

class DecodedGenerator(Generator):
    __doc__ = 'Generates a text representation of a message.\n\n    Like the Generator base class, except that non-text parts are substituted\n    with a format string representing the part.\n    '

    def __init__(self, outfp, mangle_from_=True, maxheaderlen=78, fmt=None):
        """Like Generator.__init__() except that an additional optional
        argument is allowed.

        Walks through all subparts of a message.  If the subpart is of main
        type `text', then it prints the decoded payload of the subpart.

        Otherwise, fmt is a format string that is used instead of the message
        payload.  fmt is expanded with the following keywords (in
        %(keyword)s format):

        type       : Full MIME type of the non-text part
        maintype   : Main MIME type of the non-text part
        subtype    : Sub-MIME type of the non-text part
        filename   : Filename of the non-text part
        description: Description associated with the non-text part
        encoding   : Content transfer encoding of the non-text part

        The default value for fmt is None, meaning

        [Non-text (%(type)s) part of message omitted, filename %(filename)s]
        """
        Generator.__init__(self, outfp, mangle_from_, maxheaderlen)
        if fmt is None:
            self._fmt = _FMT
        else:
            self._fmt = fmt

    def _dispatch(self, msg):
        for part in msg.walk():
            maintype = part.get_content_maintype()
            if maintype == 'text':
                print(part.get_payload(decode=False), file=self)
            else:
                if maintype == 'multipart':
                    pass
                else:
                    print(self._fmt % {'type': part.get_content_type(), 
                     'maintype': part.get_content_maintype(), 
                     'subtype': part.get_content_subtype(), 
                     'filename': part.get_filename('[no filename]'), 
                     'description': part.get('Content-Description', '[no description]'), 
                     
                     'encoding': part.get('Content-Transfer-Encoding', '[no encoding]')}, file=self)


_width = len(repr(sys.maxsize - 1))
_fmt = '%%0%dd' % _width
_make_boundary = Generator._make_boundary