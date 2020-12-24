# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/contrib/libs/markdown/mdx_macros.py
# Compiled at: 2012-03-17 12:42:14
import markdown, re

class PreprocessorMacro(object):
    pass


class MacrosExtension(markdown.Extension):

    def __init__(self, configs):
        self.config = {'macros': [{}, 'hehe']}
        for (key, value) in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        self.md = md
        MACROS_RE = '{(?P<macroName>\\w+?)(?P<macroParams> .*)?}'
        md.inlinePatterns.append(Macros(MACROS_RE, self.config, md))
        md.preprocessors.append(MacrosPreProcessor(MACROS_RE, self.config, md))


class MacrosBase(object):

    def __init__(self, pattern, config, md):
        self.config = config
        self.macros = self.config['macros'][0]
        self.md = md

    def handleMatch(self, m, doc):
        macroName = m.group('macroName')
        if self.macros.has_key(macroName):
            macroParams = m.group('macroParams')
            allParams = dict()
            if macroParams is not None:
                paramRe = re.compile('(?P<name>\\w+?)=(?:"(?P<escapedValue>.*?)"|(?P<value>.+?))(?=\\s|$)', re.S)
                for param in paramRe.finditer(macroParams):
                    if param.group('escapedValue') is None:
                        value = param.group('value')
                    else:
                        value = param.group('escapedValue')
                    allParams[param.group('name')] = value

            allParams['__md'] = self.md
            macro = self.macros[macroName]
            if isinstance(macro, PreprocessorMacro):
                if doc == None:
                    return macro.handlePreprocessorMacroCall(allParams)
            elif doc != None:
                return macro.handleMacroCall(doc, allParams)
        if doc == None:
            return
        else:
            a = doc.createTextNode(m.group())
            return a


class MacrosPreProcessor(markdown.Preprocessor, MacrosBase):

    def __init__(self, pattern, config, md):
        MacrosBase.__init__(self, pattern, config, md)
        self.pattern = pattern
        self.compiled_re = re.compile(pattern, re.DOTALL)

    def run(self, lines):
        newlines = []
        for i in range(len(lines)):
            line = lines[i]
            m = self.compiled_re.match(line)
            if not m:
                newlines.append(line)
                continue
            ret = self.handleMatch(m, None)
            if ret != None:
                newline = ret
                for l in newline.splitlines():
                    newlines.append(l)

            else:
                newlines.append(line)

        return newlines


class Macros(markdown.BasePattern, MacrosBase):

    def __init__(self, pattern, config, md):
        markdown.BasePattern.__init__(self, pattern)
        MacrosBase.__init__(self, pattern, config, md)


class Macro(object):
    pass


def makeExtension(configs=None):
    return MacrosExtension(configs=configs)