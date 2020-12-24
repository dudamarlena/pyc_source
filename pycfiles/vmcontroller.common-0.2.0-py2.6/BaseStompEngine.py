# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/common/BaseStompEngine.py
# Compiled at: 2011-03-04 15:52:41
"""
BaseStompEngine
"""
try:
    import stomper, logging, inject
    from vmcontroller.common import support
except ImportError, e:
    print 'Import error in %s : %s' % (__name__, e)
    import sys
    sys.exit()

class MsgInterpreter(object):

    @inject.param('words')
    def __init__(self, words):
        """
        @param words: A list of "words" (ie, commands represented as classes)
        """
        self.logger = logging.getLogger('%s.%s' % (self.__class__.__module__, self.__class__.__name__))
        self._words = words

    def interpret(self, msg):
        """
        @param msg: An unpacked STOMP frame
        """
        firstWord = msg['body'].split(None, 1)[0]
        self.logger.debug('Trying to interpret %s' % (firstWord,))
        try:
            word = self._words[firstWord]()
        except KeyError:
            raise NameError("Word '%s' unknown" % firstWord)

        word.listenAndAct(msg)
        return


class BaseStompEngine(stomper.Engine):
    """
    G{classtree BaseStompEngine}
    """

    @inject.param('msgInterpreter', MsgInterpreter, scope=inject.appscope)
    def __init__(self, msgInterpreter):
        super(BaseStompEngine, self).__init__()
        self.logger = logging.getLogger('%s.%s' % (self.__class__.__module__, self.__class__.__name__))
        self._msgInterpreter = msgInterpreter

    def ack(self, msg):
        """
        Called when a MESSAGE message is received
        @param msg: An unpacked frame
        """
        self._msgInterpreter.interpret(msg)
        return stomper.NO_REPONSE_NEEDED

    def react(self, msg):
        """Returns an iterable of responses"""
        rxdFrame = stomper.unpack_frame(msg)
        cmd = rxdFrame['cmd']
        self.logger.info('Received a %s message.' % cmd)
        self.logger.debug('Headers: %s ; Body: %s' % (rxdFrame['headers'], rxdFrame['body']))
        try:
            res = list(stomper.Engine.react(self, msg))
        except Exception, e:
            self.logger.error(str(e))
            res = stomper.NO_REPONSE_NEEDED

        return res