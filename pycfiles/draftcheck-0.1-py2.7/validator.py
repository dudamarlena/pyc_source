# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/draftcheck/validator.py
# Compiled at: 2014-08-08 05:59:32
"""This modules contains code to find rule violations in text."""
import rules, itertools, re
LATEX_ENVS = {'math': [
          'math', 'array', 'eqnarray', 'equation', 'align'], 
   'paragraph': [
               'abstract', 'document', 'titlepage']}
LATEX_ENVS = dict((k, env) for env in LATEX_ENVS for k in LATEX_ENVS[env])

class Validator(object):
    env_begin_regex = re.compile('\\\\begin{(\\w+)}')
    env_end_regex = re.compile('\\\\end{(\\w+)}')
    math_env_regex = re.compile('((?:\\$\\$|\\$|\\\\\\[).+?(?:\\$\\$|\\$|\\\\\\]))')

    def __init__(self):
        self._envs = [
         'paragraph']

    def validate(self, line):
        """Validate a particular line of text.

        This function finds rules that are violated by the text. The validation
        is performed in a stateful manner, with past calls to validate possibly
        affecting the results of future calls.

        Parameters
        ----------
        line : string
            The line of text to validate.

        Yields
        ------
        rule, span : (rule, (start, end))
            The first element is the rule that is violated. The second element
            is the tuple pair representing the start and end indices of the
            substring which violates that rule.
        """
        match = Validator.env_begin_regex.match(line)
        if match:
            self._envs.append(LATEX_ENVS.get(match.group(1), 'unknown'))
        match = Validator.env_end_regex.match(line)
        if match:
            self._envs.pop()
        if self._envs[(-1)] == 'math':
            chunks = [
             '', line]
        else:
            chunks = Validator.math_env_regex.split(line)
        chunk_envs = itertools.cycle([self._envs[(-1)], 'math'])
        offset = 0
        for chunk, chunk_env in zip(chunks, chunk_envs):
            for rule in rules.RULES_LIST:
                for span in rule(chunk, chunk_env):
                    offsetted_span = (
                     span[0] + offset, span[1] + offset)
                    yield (rule, offsetted_span)

            offset += len(chunk)