# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/bracket_expansion.py
# Compiled at: 2019-10-30 03:15:00
# Size of source mod 2**32: 5617 bytes


class Fragment(object):
    __doc__ = '(Abstract) empty sentence fragment'

    def __init__(self, tree):
        """
        Construct a sentence tree fragment which is merely a wrapper for
        a list of Strings
        Args:
            tree (?): Base tree for the sentence fragment, type depends on
                        subclass, refer to those subclasses
        """
        self._tree = tree

    def tree(self):
        """Return the represented sentence tree as raw data."""
        return self._tree

    def expand(self):
        """
        Expanded version of the fragment. In this case an empty sentence.
        Returns:
            List<List<str>>: A list with an empty sentence (= token/string list)
        """
        return [[]]

    def __str__(self):
        return self._tree.__str__()

    def __repr__(self):
        return self._tree.__repr__()


class Word(Fragment):
    __doc__ = '\n    Single word in the sentence tree.\n    Construct with a string as argument.\n    '

    def expand(self):
        """
        Creates one sentence that contains exactly that word.
        Returns:
            List<List<str>>: A list with the given string as sentence
                                (= token/string list)
        """
        return [
         [
          self._tree]]


class Sentence(Fragment):
    __doc__ = '\n    A Sentence made of several concatenations/words.\n    Construct with a List<Fragment> as argument.\n    '

    def expand(self):
        """
        Creates a combination of all sub-sentences.
        Returns:
            List<List<str>>: A list with all subsentence expansions combined in
                                every possible way
        """
        old_expanded = [[]]
        for sub in self._tree:
            sub_expanded = sub.expand()
            new_expanded = []
            while len(old_expanded) > 0:
                sentence = old_expanded.pop()
                for new in sub_expanded:
                    new_expanded.append(sentence + new)

            old_expanded = new_expanded

        return old_expanded


class Options(Fragment):
    __doc__ = '\n    A Combination of possible sub-sentences.\n    Construct with List<Fragment> as argument.\n    '

    def expand(self):
        """
        Returns all of its options as seperated sub-sentences.
        Returns:
            List<List<str>>: A list containing the sentences created by all
                                expansions of its sub-sentences
        """
        options = []
        for option in self._tree:
            options.extend(option.expand())

        return options


class SentenceTreeParser(object):
    __doc__ = "\n    Generate sentence token trees from a list of tokens\n    ['1', '(', '2', '|', '3, ')'] -> [['1', '2'], ['1', '3']]\n    "

    def __init__(self, tokens):
        self.tokens = tokens

    def _parse(self):
        """
        Generate sentence token trees
        ['1', '(', '2', '|', '3, ')'] -> ['1', ['2', '3']]
        """
        self._current_position = 0
        return self._parse_expr()

    def _parse_expr(self):
        """
        Generate sentence token trees from the current position to
        the next closing parentheses / end of the list and return it
        ['1', '(', '2', '|', '3, ')'] -> ['1', [['2'], ['3']]]
        ['2', '|', '3'] -> [['2'], ['3']]
        """
        sentence_list = []
        cur_sentence = []
        sentence_list.append(Sentence(cur_sentence))
        while self._current_position < len(self.tokens):
            cur = self.tokens[self._current_position]
            self._current_position += 1
            if cur == '(':
                subexpr = self._parse_expr()
                normal_brackets = False
                if len(subexpr.tree()) == 1:
                    normal_brackets = True
                    cur_sentence.append(Word('('))
                cur_sentence.append(subexpr)
                if normal_brackets:
                    cur_sentence.append(Word(')'))
                elif cur == '|':
                    cur_sentence = []
                    sentence_list.append(Sentence(cur_sentence))
                else:
                    if cur == ')':
                        break
            else:
                cur_sentence.append(Word(cur))

        return Options(sentence_list)

    def _expand_tree(self, tree):
        """
        Expand a list of sub sentences to all combinated sentences.
        ['1', ['2', '3']] -> [['1', '2'], ['1', '3']]
        """
        return tree.expand()

    def expand_parentheses(self):
        tree = self._parse()
        return self._expand_tree(tree)