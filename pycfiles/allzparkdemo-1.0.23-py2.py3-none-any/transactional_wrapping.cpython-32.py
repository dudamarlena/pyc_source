# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/sqlalchemy/processor/transactional_wrapping.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 5, 2012\n\n@package: ally core sql alchemy\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides support for SQL alchemy a processor for automatic session handling.\n'
from ally.design.processor.attribute import optional
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor
from ally.support.sqlalchemy.session import rollback, commit, setKeepAlive, endSessions

class Response(Context):
    """
    The response context.
    """
    isSuccess = optional(bool)


class TransactionWrappingHandler(HandlerProcessor):
    """
    Implementation for a processor that provides the SQLAlchemy session handling.
    """

    def process(self, chain, response: Response, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Wraps the invoking and all processors after invoking in a transaction.
        """
        assert isinstance(chain, Chain), 'Invalid processors chain %s' % chain
        assert isinstance(response, Response), 'Invalid response %s' % response
        setKeepAlive(True)

        def onFinalize():
            """
            Handle the finalization
            """
            if Response.isSuccess in response:
                if response.isSuccess is True:
                    endSessions(commit)
                else:
                    endSessions(rollback)
            else:
                endSessions(commit)

        def onError():
            """
            Handle the error.
            """
            endSessions(rollback)

        chain.callBack(onFinalize)
        chain.callBackError(onError)