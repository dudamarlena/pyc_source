# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: metricaltree/deptree.py
# Compiled at: 2017-04-23 13:38:12
from __future__ import unicode_literals
import tempfile, os, re
from subprocess import PIPE
import nltk, nltk.data
from nltk import compat
from nltk import Tree
from nltk.internals import find_jar, find_jar_iter, config_java, java, _java_options
from nltk.parse.api import ParserI
_stanford_url = b'http://nlp.stanford.edu/software/lex-parser.shtml'

class DependencyTree(Tree):
    """"""
    _contractables = ('m', 's', 'll', 'd', 'nt', 're', 've', "'m", "'s", "'ll", "'d",
                      "n't", "'re", "'ve")
    _punctTags = ('.', ',', ':')

    def __init__(self, node, children=None, dep=None):
        """"""
        self._cat = node
        self._dep = dep
        self._preterm = False
        self._label = None
        super(DependencyTree, self).__init__(node, children)
        if len(self) == 1 and isinstance(self[0], compat.string_types):
            self._preterm = True
        self.set_label()
        return

    def preterminal(self):
        """"""
        return self._preterm

    def category(self):
        """"""
        return self._cat

    def dependency(self):
        """"""
        return self._dep

    def preterminals(self, leaves=True):
        """"""
        if self._preterm:
            if leaves:
                yield self
            else:
                yield self._label
        else:
            for child in self:
                for preterminal in child.preterminals(leaves=leaves):
                    yield preterminal

    def categories(self, leaves=True):
        """"""
        for preterminal in self.preterminals(leaves=True):
            if leaves:
                yield (
                 preterminal._cat, preterminal[0])
            else:
                yield preterminal._cat

    def dependencies(self, leaves=True):
        """"""
        for preterminal in self.preterminals(leaves=True):
            if leaves:
                yield (
                 preterminal._dep, preterminal[0])
            else:
                yield preterminal._dep

    def set_label(self):
        """"""
        if self._dep is None:
            self._label = self._cat
        else:
            self._label = b'%s/%s' % (self._cat, self._dep)
        return

    def set_category(self, cat):
        """"""
        self._cat = cat
        self.set_label()

    def set_dep(self, dep):
        """"""
        self._dep = dep
        self.set_label()

    def set_deps(self, deps):
        """"""
        preterminals = self.preterminals()
        for preterminal in preterminals:
            if re.match(b'\\w', preterminal._cat[0]):
                preterminal.set_dep(deps.pop(0))

    def to_tuples(self):
        """"""
        for preterminal in self.preterminals():
            yield (
             preterminal[0], preterminal.category(), preterminal.dependency())

    def _get_last_preterm(self):
        """"""
        if self._preterm:
            return self
        else:
            return self[(-1)]._get_last_preterm()

    def _pop_first_contractable(self):
        """"""
        if self._preterm:
            if self[0] in _contractables:
                return self
            else:
                return

        else:
            first_contractable = self[0]._pop_first_contractable()
            if self[0] == first_contractable or len(self[0]) == 0:
                self.children.pop(0)
                self.pop(0)
            return first_contractable
        return

    def contract(self):
        """"""
        for child in self:
            if isinstance(child, DependencyTree):
                child.contract()

        i = len(self) - 2
        while i >= 0:
            child = self[i]
            last_preterm = child._get_last_preterm()
            j = i + 1
            while j < len(self):
                next_child = self[j]
                first_contractable = next_child._pop_first_contractable()
                if first_contractable is not None:
                    last_preterm._cat += b'+' + first_contractable.category()
                    last_preterm[0] += first_goeswith[0]
                    last_preterm.children[0] += first_goeswith.children[0]
                    if len(next_child) == 0:
                        self.pop(j)
                    else:
                        break
                else:
                    break

            i -= 1

        return

    @classmethod
    def fromstring(cls, s):
        """"""
        cTree, dGraph = s.split(b'\n\n')
        dTree = Tree.fromstring(cTree)
        dTree = DependencyTree.convert(dTree)
        deps = []
        dGraph = dGraph.split(b'\n')
        lastWord = b''
        for dep in dGraph:
            try:
                dep, thisWord = re.match(b'(.+?)\\(.*?, (.*?)\\)', dep).groups()
                if thisWord != lastWord:
                    deps.append(dep)
                    lastWord = thisWord
            except:
                print b''

        dTree.set_deps(deps)
        return dTree

    @classmethod
    def convert(cls, tree):
        """
        Convert a tree between different subtypes of Tree.  ``cls`` determines
        which class will be used to encode the new tree.

        :type tree: Tree
        :param tree: The tree that should be converted.
        :return: The new Tree.
        """
        if isinstance(tree, Tree):
            children = [ cls.convert(child) for child in tree ]
            if isinstance(tree, DependencyTree):
                return cls(tree._cat, children, tree._dep)
            return cls(tree._label, children)
        else:
            return tree

    def copy(self, deep=False):
        """"""
        if not deep:
            return type(self)(self._cat, self, dep=self._dep)
        else:
            return type(self).convert(self)


class DependencyTreeParser(ParserI):
    """"""
    _MODEL_JAR_PATTERN = b'stanford-parser-(\\d+)(\\.(\\d+))+-models\\.jar'
    _EJML_JAR_PATTERN = b'ejml-(\\d+)(\\.(\\d+))+\\.jar'
    _JAR = b'stanford-parser.jar'

    def __init__(self, path_to_jar=None, path_to_models_jar=None, path_to_ejml_jar=None, model_path=b'edu/stanford/nlp/models/parser/lexparser/englishPCFG.ser.gz', encoding=b'utf8', verbose=False, java_options=b'-mx3G'):
        """"""
        self._stanford_jar = find_jar(self._JAR, path_to_jar, env_vars=('STANFORD_PARSER', ), searchpath=(), url=_stanford_url, verbose=verbose)
        self._model_jar = max(find_jar_iter(self._MODEL_JAR_PATTERN, path_to_models_jar, env_vars=('STANFORD_MODELS', ), searchpath=(), url=_stanford_url, verbose=verbose, is_regex=True), key=lambda model_name: re.match(self._MODEL_JAR_PATTERN, model_name))
        self._ejml_jar = max(find_jar_iter(self._EJML_JAR_PATTERN, path_to_ejml_jar, env_vars=('STANFORD_EJML', ), searchpath=(), url=_stanford_url, verbose=verbose, is_regex=True), key=lambda ejml_name: re.match(self._EJML_JAR_PATTERN, ejml_name))
        self.model_path = model_path
        self._encoding = encoding
        self.java_options = java_options

    @staticmethod
    def _parse_trees_output(output_):
        """"""
        res = []
        cur_lines = []
        finished_tree = False
        for line in output_.splitlines(False):
            if line == b'' and finished_tree:
                res.append(iter([DependencyTree.fromstring((b'\n').join(cur_lines))]))
                cur_lines = []
                finished_tree = False
            else:
                cur_lines.append(line)
                if line == b'' and not finished_tree:
                    finished_tree = True

        return iter(res)

    def parse_sents(self, sentences, verbose=False):
        """"""
        cmd = [
         b'edu.stanford.nlp.parser.lexparser.LexicalizedParser',
         b'-model', self.model_path,
         b'-sentences', b'newline',
         b'-outputformat', b'penn,typedDependencies',
         b'-tokenized',
         b'-escaper', b'edu.stanford.nlp.process.PTBEscapingProcessor']
        return self._parse_trees_output(self._execute(cmd, (b'\n').join((b' ').join(sentence) for sentence in sentences), verbose))

    def raw_parse(self, sentence, verbose=False):
        """"""
        return next(self.raw_parse_sents([sentence], verbose))

    def raw_parse_sents(self, sentences, verbose=False):
        """"""
        cmd = [
         b'edu.stanford.nlp.parser.lexparser.LexicalizedParser',
         b'-model', self.model_path,
         b'-sentences', b'newline',
         b'-outputFormat', b'penn,typedDependencies']
        return self._parse_trees_output(self._execute(cmd, (b'\n').join(sentences), verbose))

    def tagged_parse(self, sentence, verbose=False):
        """"""
        return next(self.tagged_parse_sents([sentence], verbose))

    def tagged_parse_sents(self, sentences, verbose=False):
        """"""
        tag_separator = b'/'
        cmd = [
         b'edu.stanford.nlp.parser.lexparser.LexicalizedParser',
         b'-model', self.model_path,
         b'-sentences', b'newline',
         b'-outputFormat', b'penn,typedDependencies',
         b'-tokenized',
         b'-tagSeparator', tag_separator,
         b'-tokenizerFactory', b'edu.stanford.nlp.process.WhitespaceTokenizer',
         b'-tokenizerMethod', b'newCoreLabelTokenizerFactory']
        return self._parse_trees_output(self._execute(cmd, (b'\n').join((b' ').join(tag_separator.join(tagged) for tagged in sentence) for sentence in sentences), verbose))

    def _execute(self, cmd, input_, verbose=False):
        """"""
        encoding = self._encoding
        cmd.extend([b'-encoding', encoding])
        default_options = (b' ').join(_java_options)
        config_java(options=self.java_options, verbose=verbose)
        with tempfile.NamedTemporaryFile(mode=b'wb', delete=False) as (input_file):
            if isinstance(input_, compat.text_type) and encoding:
                input_ = input_.encode(encoding)
            input_file.write(input_)
            input_file.flush()
            cmd.append(input_file.name)
            stdout, stderr = java(cmd, classpath=(self._stanford_jar, self._model_jar, self._ejml_jar), stdout=PIPE, stderr=PIPE)
            stdout = stdout.decode(encoding)
        os.unlink(input_file.name)
        config_java(options=default_options, verbose=False)
        return stdout


def setup_module(module):
    """"""
    from nose import SkipTest
    try:
        StanfordParser(model_path=b'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
    except LookupError:
        raise SkipTest(b"doctests from nltk.parse.stanford are skipped because the stanford parser jar doesn't exist")


if __name__ == b'__main__':
    import doctest, os
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    import nltk.data
    sent_splitter = nltk.data.load(b'tokenizers/punkt/english.pickle')
    import codecs, cPickle as pkl, time, sys
    DATE = b'2015-04-20'
    MODELS_VERSION = b'3.5.2'
    EJML_VERSION = b'0.23'
    os.environ[b'STANFORD_PARSER'] = b'Stanford Library/stanford-parser-full-%s/stanford-parser.jar' % DATE
    os.environ[b'STANFORD_MODELS'] = b'Stanford Library/stanford-parser-full-%s/stanford-parser-%s-models.jar' % (DATE, MODELS_VERSION)
    os.environ[b'STANFORD_EJML'] = b'Stanford Library/stanford-parser-full-%s/ejml-%s.jar' % (DATE, EJML_VERSION)
    parser = DependencyTreeParser(model_path=b'Stanford Library/stanford-parser-full-%s/edu/stanford/nlp/models/lexparser/englishRNN.ser.gz' % DATE)
    basename = sys.argv[1].decode(b'utf-8')
    tuples = []
    i = 0
    lps = 0
    t_0 = time.time()
    lines = sum(1 for line in codecs.open(b'Text Book/Tolkien/%s.txt' % basename, encoding=b'utf-8'))
    try:
        with codecs.open(b'Text Book/Tolkien/%s.txt' % basename, encoding=b'utf-8') as (f):
            for line in f:
                i += 1
                for sent in sent_splitter.tokenize(line.strip()):
                    trees = parser.raw_parse(sent)
                    for tree in trees:
                        tuples.append(list(tree.to_tuples()))

                t_i = time.time()
                lps = i / (t_i - t_0)
                lpm = lps * 60
                lph = lpm * 60
                etc = (lines - i) / lph
                etc_h = int(etc)
                etc_m = (etc - etc_h) * 60
                print b'Line %d/%d: %.1f lpm, %dh %.1fm left         \r' % (i, lines, lpm, etc_h, etc_m),
                sys.stdout.flush()

    except:
        print b'Stopped while parsing line %d   ' % i

    pkl.dump(tuples, open(b'Pickle Jar/%s.pkl' % basename, b'w'), protocol=pkl.HIGHEST_PROTOCOL)