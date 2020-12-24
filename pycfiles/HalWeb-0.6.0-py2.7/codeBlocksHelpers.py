# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/codeBlocksHelpers.py
# Compiled at: 2011-12-25 05:31:43
from string import Template

class BlockLocator(object):
    blockTemplate = None

    def lineIsBlockBegin(self):
        pass

    def lineIsBlockEnd(self):
        pass

    def createValidBlock(self, blockname, content=[], blIndent=0, indent=0):
        if not self.blockTemplate:
            raise NotImplementedError('Block Template was not provided')
        result = Template(self.blockTemplate).substitute(blindent=' ' * blIndent, blockname=blockname)
        if not content:
            return result.replace('#content#\n', '')
        else:
            return result.replace('#content#', ('\n').join([ ' ' * indent + line for line in content ]))


class GenericCbl(BlockLocator):
    """base class for all BlockLocators"""

    def __init__(self, blockBeginLocator, blockEndLocator, blockTemplate=None):
        self.blockTemplate = blockTemplate
        self.lineIsBlockBegin = blockBeginLocator
        self.lineIsBlockEnd = blockEndLocator


class HalCodeBlockLocator(BlockLocator):
    blockTemplate = '$blindent{%block $blockname%}\n#content#\n$blindent{%endblock%}\n'

    def lineIsBlockBegin(self, line):
        if line.replace(' ', '').find('{%block') >= 0 and line.replace(' ', '').find('%}') > 0:
            return strBetween(line.replace(' ', ''), '{%block', '%}')
        else:
            return
            return

    def lineIsBlockEnd(self, line):
        return line.replace(' ', '').find('{%endblock%}') >= 0


class InPythonBlockLocator(BlockLocator):
    blockTemplate = '$blindent#{%block $blockname%}\n#content#\n$blindent#{%endblock%}\n'

    def lineIsBlockBegin(self, line):
        if line.replace(' ', '').find('#{%block') >= 0 and line.replace(' ', '').find('%}') > 0:
            return strBetween(line.replace(' ', ''), '#{%block', '%}')
        else:
            return
            return

    def lineIsBlockEnd(self, line):
        return line.replace(' ', '').find('#{%endblock%}') >= 0


def strBetween(line, strLeft, strRigth, strip=True):
    fromIndex = line.index(strLeft) + len(strLeft)
    toIndex = fromIndex + line[fromIndex:].index(strRigth)
    result = line[fromIndex:toIndex]
    if strip:
        return result.strip()
    else:
        return result