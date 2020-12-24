# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cinje/inline/flush.py
# Compiled at: 2019-03-06 14:24:28
# Size of source mod 2**32: 1710 bytes
from ..util import Line, ensure_buffer

def flush_template(context, declaration=None, reconstruct=True):
    """Emit the code needed to flush the buffer.
                
        Will only emit the yield and clear if the buffer is known to be dirty.
        """
    if declaration is None:
        declaration = Line(0, '')
    if {'text', 'dirty'}.issubset(context.flag):
        yield declaration.clone(line='yield "".join(_buffer)')
        context.flag.remove('text')
        context.flag.remove('dirty')
        if reconstruct:
            for i in ensure_buffer(context):
                yield i

    if declaration.stripped == 'yield':
        yield declaration


class Flush(object):
    __doc__ = 'Allow mid-stream flushing of the template buffer.\n\t\n\tThis is generally used to flush sections of a page to the client to allow for content pre-loading of CSS,\n\tJavaScript, images, etc., as well as to provide a more responsive experience for a user during longer operations.\n\t\n\tSyntax:\n\t\n\t\t: flush\n\t\n\tNote: this will only emit the code needed to flush and clear the buffer if there is a buffer to flush, and the\n\tbuffer is known to be "dirty" by the translator.  I.e. following ": use" or ": uses", or after some template\n\ttext has been defined.  Unlike most other commands involving the buffer, this one will not create a buffer if\n\tmissing.\n\t\n\tThis also handles flushing prior to yielding, for wrapper templates.\n\t'
    priority = 25

    def match(self, context, line):
        """Match exact "flush" command usage."""
        return line.kind == 'code' and line.stripped in ('flush', 'yield')

    def __call__(self, context):
        try:
            line = context.input.next()
        except StopIteration:
            return
        else:
            return flush_template(context, line)