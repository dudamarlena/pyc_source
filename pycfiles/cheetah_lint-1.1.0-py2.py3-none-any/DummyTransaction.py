# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/DummyTransaction.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = '\nProvides dummy Transaction and Response classes is used by Cheetah in place\nof real Webware transactions when the Template obj is not used directly as a\nWebware servlet.\n\nWarning: This may be deprecated in the future, please do not rely on any\nspecific DummyTransaction or DummyResponse behavior\n'
import logging
from Cheetah.compat import unicode

class DummyResponseFailure(Exception):
    pass


class DummyResponse(object):
    """
    A dummy Response class is used by Cheetah in place of real Webware
    Response objects when the Template obj is not used directly as a Webware
    servlet
    """

    def __init__(self):
        self._outputChunks = []

    def flush(self):
        pass

    def safeConvert(self, chunk):
        if not chunk:
            return ''
        if isinstance(chunk, unicode):
            return chunk
        try:
            return chunk.decode('utf-8', 'strict')
        except UnicodeDecodeError:
            try:
                return chunk.decode('latin-1', 'strict')
            except UnicodeDecodeError:
                return chunk.decode('ascii', 'ignore')

        except AttributeError:
            return unicode(chunk, errors='ignore')

        return chunk

    def write(self, value):
        self._outputChunks.append(value)

    def writeln(self, txt):
        self.write(txt)
        self.write('\n')

    def getvalue(self, outputChunks=None):
        chunks = outputChunks or self._outputChunks
        try:
            return ('').join(chunks)
        except UnicodeDecodeError:
            logging.debug('Trying to work around a UnicodeDecodeError in getvalue()')
            logging.debug('...perhaps you could fix "%s" while you\'re debugging')
            return ('').join(self.safeConvert(c) for c in chunks)

    def writelines(self, *lines):
        [ self.writeln(ln) for ln in lines ]


class DummyTransaction(object):
    """
        A dummy Transaction class is used by Cheetah in place of real Webware
        transactions when the Template obj is not used directly as a Webware
        servlet.

        It only provides a response object and method.  All other methods and
        attributes make no sense in this context.
    """

    def __init__(self, *args, **kwargs):
        self._response = None
        return

    def response(self, resp=None):
        if self._response is None:
            self._response = resp or DummyResponse()
        return self._response


class TransformerResponse(DummyResponse):

    def __init__(self, *args, **kwargs):
        super(TransformerResponse, self).__init__(*args, **kwargs)
        self._filter = None
        return

    def getvalue(self, **kwargs):
        output = super(TransformerResponse, self).getvalue(**kwargs)
        if self._filter:
            _filter = self._filter
            if isinstance(_filter, type):
                _filter = _filter()
            return _filter.filter(output)
        return output


class TransformerTransaction(object):

    def __init__(self, *args, **kwargs):
        self._response = None
        return

    def response(self):
        if self._response:
            return self._response
        return TransformerResponse()