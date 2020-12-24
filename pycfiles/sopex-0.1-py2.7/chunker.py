# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sopex/chunker.py
# Compiled at: 2013-02-13 08:34:44
import os, simplejson as json, pyparsing
from jpype import *

class PennTreebackChunker(object):

    def __init__(self):
        path = os.path.realpath(__file__)
        path = path[:path.rfind(os.sep)] + os.sep + 'jars'
        classpath = os.pathsep.join(path + os.sep + jar for jar in os.listdir(path))
        startJVM(getDefaultJVMPath(), '-Djava.class.path=%s' % classpath)
        String = JClass('java.lang.String')
        self.StringReader = JClass('java.io.StringReader')
        self.StringWriter = JClass('java.io.StringWriter')
        self.PrintWriter = JClass('java.io.PrintWriter')
        PTBTokenizer = JClass('edu.stanford.nlp.process.PTBTokenizer')
        LexicalizedParser = JClass('edu.stanford.nlp.parser.lexparser.LexicalizedParser')
        CoreLabelTokenFactory = JClass('edu.stanford.nlp.process.CoreLabelTokenFactory')
        self.TreePrint = JClass('edu.stanford.nlp.trees.TreePrint')
        self.tokenizerFactory = PTBTokenizer.factory(CoreLabelTokenFactory(), '')
        self.lp = LexicalizedParser.loadModel()
        self.penn_treebank_expr = pyparsing.nestedExpr('(', ')')

    def _nestedlist2dict(self, d, l):
        if l[0] not in d:
            d[l[0]] = {}
        for v in l[1:]:
            if type(v) == list:
                self._nestedlist2dict(d[l[0]], v)
            else:
                d[l[0]] = v

    def chunk_string(self, sentence, json_response=False):
        rawWords = self.tokenizerFactory.getTokenizer(self.StringReader(sentence)).tokenize()
        parse = self.lp.apply(rawWords)
        stringWriter = self.StringWriter()
        tp = self.TreePrint('oneline')
        tp.printTree(parse, self.PrintWriter(stringWriter))
        penn = stringWriter.toString()
        penn = self.penn_treebank_expr.parseString(penn).asList()[0]
        penn_str = {}
        self._nestedlist2dict(penn_str, penn)
        if json_response:
            return json.dumps(penn_str)
        return penn_str

    def close(self):
        shutdownJVM()