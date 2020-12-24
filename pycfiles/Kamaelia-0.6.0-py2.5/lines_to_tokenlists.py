# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Visualisation/PhysicsGraph/lines_to_tokenlists.py
# Compiled at: 2008-10-19 12:19:52
r"""=============================
Simple line-of-text tokeniser
=============================

This component takes a line of text and splits it into space character
separated tokens. Tokens can be encapsulated with single or double quote marks,
allowing spaces to appear within a token.

Example Usage
-------------

A simple pieline that takes each line you type and splits it into a list of tokens,
showing you the result::
    
    Pipeline( ConsoleReader(),
              lines_to_tokenlists(),
              ConsoleEchoer()
            ).run()

At runtime::
    >>> Hello world "how are you" 'john said "hi"' "i replied "hi"" "c:\windows" end
    [ 'Hello',
      'world',
      'how are you',
      'john said "hi"', 
      'i replied "hi"',
      'c:\windows',
      'end' ]
            
            
            
How does it work?
-----------------
                 
lines_to_tokenlists receives individual lines of text on its "inbox" inbox. A 
line is converted to a list of tokens, which is sent out of its "outbox"
outbox.

Space characters are treated as the token separator, however a token can be
encapsulated in single or double quotes allowing space characters to appear
within it.

If you need to use a quote mark or backslash within a token encapsulated by 
quote marks, it must be escaped by prefixing it with a backslash. Only do
this if the token is encapsulated.

encapsulating quote marks are removed when the line is tokenised. Escaped
backslashes and quote marks are converted to plain backslashes and quote marks.

If a producerFinished() or shutdownMicroprocess() message is received on this
component's "control" inbox, then it will send it on out of its "signal" outbox
and immediately terminate. It will not flush any whole lines of text that may
still be buffered.
"""
import re
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class lines_to_tokenlists(component):
    """    lines_to_tokenlists() -> new lines_to_tokenlists component.
    
    Takes individual lines of text and separates them into white
    space separated tokens. Tokens can be enclosed with single or 
    double quote marks.
    """
    Inboxes = {'inbox': 'Individual lines of text', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'list of tokens making up the line of text', 'signal': 'Shutdown signalling'}

    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(lines_to_tokenlists, self).__init__()
        doublequoted = '(?:"((?:(?:\\\\.)|[^\\\\"])*)")'
        singlequoted = "(?:'((?:(?:\\\\.)|[^\\\\'])*)')"
        unquoted = '([^"\\\'][^\\s]*)'
        self.tokenpat = re.compile('\\s*(?:' + unquoted + '|' + singlequoted + '|' + doublequoted + ')(?:\\s+(.*))?$')

    def main(self):
        """Main loop."""
        while not self.shutdown():
            while self.dataReady('inbox'):
                line = self.recv('inbox')
                tokens = self.lineToTokens(line)
                if tokens != []:
                    self.send(tokens, 'outbox')

            self.pause()
            yield 1

    def lineToTokens(self, line):
        """        linesToTokens(line) -> list of tokens.
        
        Splits a line into individual white-space separated tokens.
        Tokens can be enclosed in single or double quotes to allow spaces
        to be used in them.
        
        Escape backslash and single or double quotes by prefixing them
        with a backslash *only* if used within an quote encapsulated string.
        """
        tokens = []
        while line != None and line.strip() != '':
            match = self.tokenpat.match(line)
            if match != None:
                (uq, sq, dq, line) = match.groups()
                if uq != None:
                    tokens += [uq]
                elif sq != None:
                    tokens += [re.sub('\\\\(.)', '\\1', sq)]
                elif dq != None:
                    tokens += [re.sub('\\\\(.)', '\\1', dq)]
            else:
                return []

        return tokens

    def shutdown(self):
        """        Returns True if a shutdownMicroprocess or producerFinished message was received.
        """
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send(msg, 'signal')
                return True

        return False


__kamaelia_components__ = (
 lines_to_tokenlists,)