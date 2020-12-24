# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/Tokenisation/Simple.py
# Compiled at: 2008-10-19 12:19:52
from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.Support.Data.Escape import escape, unescape
substitutions = '\x009\n\r []'
from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller

def tokenlists_to_lines():
    return Marshaller(EscapedListMarshalling)


def lines_to_tokenlists():
    return DeMarshaller(EscapedListMarshalling)


class EscapedListMarshalling:

    def marshall(lst, term='\n'):
        out = ''
        for item in lst:
            if isinstance(item, (list, tuple)):
                out = out + '[ ' + EscapedListMarshalling.marshall(item, term='] ')
            else:
                out = out + escape(item, substitutions) + ' '

        return out + term

    marshall = staticmethod(marshall)

    def demarshall(string):
        out = []
        outstack = []
        for item in string.split(' '):
            if len(item) and item != '\n':
                if item == '[':
                    outstack.append(out)
                    newout = []
                    out.append(newout)
                    out = newout
                elif item == ']':
                    out = outstack.pop(-1)
                else:
                    out.append(unescape(item, substitutions))

        return out

    demarshall = staticmethod(demarshall)


__kamaelia_prefabs__ = (
 tokenlists_to_lines, lines_to_tokenlists)
if __name__ == '__main__':
    tests = [
     [
      'hello', 'world'],
     [
      [
       'hello', 'world']],
     [
      [
       'hello world']],
     [
      'hello', ' world', ['1', '2', [['7', 'alpha beta'], ['5', '6']], 'n']],
     [
      'hello\nworld\\today']]
    for test in tests:
        marshalled = EscapedListMarshalling.marshall(test)
        demarshalled = EscapedListMarshalling.demarshall(marshalled)
        if test == demarshalled:
            for char in marshalled[:-1]:
                if ord(char) < 32:
                    raise '\nFAILED (LOWCHAR) : ' + str(test)

            if marshalled[(-1)] != '\n':
                raise '\nFAILED (ENDTERM) : ' + str(test)
            print '.'
        else:
            raise '\nFAILED (MISMATCH) : ' + str(test) + '\nIt was : ' + str(demarshalled) + '\n'