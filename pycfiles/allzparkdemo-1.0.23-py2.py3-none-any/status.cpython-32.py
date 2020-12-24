# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/impl/processor/status.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 1, 2013\n\n@package: ally core http\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the status and status text population based on codes.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed

class Response(Context):
    """
    The response context.
    """
    code = requires(str)
    status = defines(int)
    text = defines(str)


@injected
class StatusHandler(HandlerProcessorProceed):
    """
    Provides the code to status handler.
    """
    codeToStatus = dict
    codeToText = dict

    def __init__(self):
        """
        Construct the encoder.
        """
        assert isinstance(self.codeToStatus, dict), 'Invalid code to status mapping %s' % self.codeToStatus
        assert isinstance(self.codeToText, dict), 'Invalid code to text mapping %s' % self.codeToText
        for code, status in self.codeToStatus.items():
            assert isinstance(code, str), 'Invalid code %s' % code
            if not isinstance(status, int):
                raise AssertionError('Invalid status %s' % status)

        for code, text in self.codeToText.items():
            assert isinstance(code, str), 'Invalid code %s' % code
            if not isinstance(text, str):
                raise AssertionError('Invalid text %s' % text)

        super().__init__()

    def process(self, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Process the status.
        """
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(response.code, str), 'Invalid response code %s' % response.code
        status = self.codeToStatus.get(response.code)
        if response.status is None:
            if status is None:
                ValueError("Cannot produce a status for code '%s'" % response.code)
            response.status = status
        elif status is not None:
            response.status = status
        text = self.codeToText.get(response.code)
        if text:
            response.text = text
        return