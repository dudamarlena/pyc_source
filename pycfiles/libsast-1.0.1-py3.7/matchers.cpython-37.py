# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/libsast/core_matcher/matchers.py
# Compiled at: 2020-04-13 00:00:20
# Size of source mod 2**32: 4119 bytes
"""
Alogrithms for Matching Pattern.

Severity - It defines severity of the finding.

   1. error - Critical Security vulnerability
   2. warning - Possible Security vulnerability
   3. info - Informational findings

Input Case - Defines the case of data before pattern matching

   1. upper - Convert data to upper case before matching
   2. lower - Convert data to lower case before matching
   3. exact - No conversion

Match Type - Types of pattern matchers supported

   1. Regex - if re.findall(regex1, input)
   2. RegexAnd - if re.findall(regex1, input) and re.findall(regex2, input)
   3. RegexOr - if re.findall(regex1, input) or re.findall(regex2, input)
   4. RegexAndOr -  if (string1 in input)
                    and ((string2 in input) or (string3 in input))
   5. RegexAndNot - if(string1 in input and string2 not in input)
"""
import re
from abc import ABC, abstractclassmethod
from libsast.logger import init_logger
logger = init_logger(__name__)

class MatchCommand:

    def __init__(self):
        self.patterns = {}

    def _find_match(self, pattern_name, content, rule):
        if pattern_name not in self.patterns:
            pattern_class = globals()[pattern_name]
            self.patterns[pattern_name] = pattern_class()
        return self.patterns[pattern_name]._perform_search(content, rule)


class MatchStrategy(ABC):

    @abstractclassmethod
    def _perform_search(self, content, rule):
        """Search for instance of match in content."""
        pass


class Regex(MatchStrategy):

    def _perform_search(self, content, rule):
        matches = set()
        for match in re.compile(rule['pattern']).finditer(content):
            if match.group():
                matches.add((match.group(), match.span()))

        return matches


class RegexAnd(MatchStrategy):

    def _perform_search(self, content, rule):
        if isinstance(rule['pattern'], str):
            logger.debug('wrong regex type, switching to single regex')
            return Regex().perform_search(content, rule)
        matches = set()
        for regex in rule['pattern']:
            for match in re.compile(regex).finditer(content):
                if not match.group():
                    return False
                    matches.add((match.group(), match.span()))

        return matches


class RegexOr(MatchStrategy):

    def _perform_search(self, content, rule):
        if isinstance(rule['pattern'], str):
            logger.debug('wrong regex type, switching to single regex')
            return Regex().perform_search(content, rule)
        matches = set()
        for regex in rule['pattern']:
            for match in re.compile(regex).finditer(content):
                if match.group():
                    matches.add((match.group(), match.span()))

        return matches


class RegexAndNot(MatchStrategy):

    def _perform_search(self, content, rule):
        matches = set()
        regex_present = re.compile(rule['pattern'][0]).finditer(content)
        regex_not = re.compile(rule['pattern'][1]).finditer(content)
        for match in regex_not:
            if match.group():
                return False

        for match in regex_present:
            if match.group():
                matches.add((match.group(), match.span()))

        return matches


class RegexAndOr(MatchStrategy):

    def _perform_search(self, content, rule):
        matches = set()
        or_matches = set()
        or_list = rule['pattern'][1]
        break_parent_loop = False
        for regex in or_list:
            for match in re.compile(regex).finditer(content):
                if match.group():
                    or_matches.add((match.group(), match.span()))
                    break_parent_loop = True
                    break

            if break_parent_loop:
                break

        for match in re.compile(rule['pattern'][0]).finditer(content):
            if match.group():
                matches.add((match.group(), match.span()))

        if matches and or_matches:
            matches.update(or_matches)
        else:
            return False
            return matches