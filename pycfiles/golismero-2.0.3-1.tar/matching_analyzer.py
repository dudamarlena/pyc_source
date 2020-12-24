# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/text/matching_analyzer.py
# Compiled at: 2013-11-20 12:43:31
"""
Text diff/match analyzer API.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'get_diff_ratio', 'MatchingAnalyzer']
from difflib import SequenceMatcher

def get_diff_ratio(text1, text2):
    """
    Compare two texts and return a floating point value between 0 and 1 with
    the difference ratio, with 0 being absolutely different and 1 being
    absolutely equal - the more similar the two texts are, the closer the ratio
    will be to 1.

    :param text1: First text to compare.
    :type text1: str

    :param text2: Second text to compare.
    :type text2: str

    :returns: Floating point value between 0 and 1.
    :rtype: float
    """
    if not text1:
        text1 = ''
    if not text2:
        text2 = ''
    if not isinstance(text1, basestring):
        raise TypeError('Expected string, got %r instead' % type(text1))
    if not isinstance(text2, basestring):
        raise TypeError('Expected string, got %r instead' % type(text2))
    if text1 == text2:
        return 1.0
    m = SequenceMatcher(a=text1, b=text2)
    return m.ratio()


class MatchingAnalyzerElement(object):
    """
    Match element of the :ref:`MatchingAnalyzer`.

    :ivar text: Text.
    :type text: str

    :ivar ratio: Difference ratio against the base text.
    :type ratio: float
    """

    def __init__(self, text, ratio, attrs):
        r"""
        :param text: Text.
        :type text: str

        :param ratio: Difference ratio against the base text.
        :type ratio: float

        :param attrs: Custom attributes dictionary.
        :type attrs: dict(str -> \*)
        """
        self.text = text
        self.ratio = ratio
        self.__attrs = attrs

    def __getattr__(self, name):
        return self.__attrs[name]


class MatchingAnalyzer(object):
    """
    Text matching analyzer.

    Compares any number of texts from a base text and generates
    an iterator with those that are sufficiently different.
    """

    def __init__(self, base_text, min_ratio=0.52, min_deviation=1.15):
        """
        :param base_text: Base text to be used for comparisons.
        :type base_text: str

        :param min_ratio: Minimum diff ratio to consider two texts as different.
        :type min_ratio: float

        :param min_deviation: Minimum deviation from the average to consider
            texts to be unique.
        :type min_deviation: float
        """
        if not base_text:
            raise ValueError('Base text cannot be empty')
        if not isinstance(base_text, basestring):
            raise TypeError('Expected string , got %r instead' % type(base_text))
        if not isinstance(min_ratio, float):
            raise TypeError('Expected float, got %r instead' % type(min_ratio))
        if not isinstance(min_deviation, float):
            raise TypeError('Expected float, got %r instead' % type(min_deviation))
        self.__base_text = base_text
        self.__min_ratio = min_ratio
        self.__min_deviation = min_deviation
        self.__matches = []
        self.__unique_strings = None
        self.__average_ratio = None
        return

    @property
    def base_text(self):
        """
        :returns: Base text to be used for comparisons.
        :rtype: str
        """
        return self.__base_text

    @property
    def min_ratio(self):
        """
        :returns: Minimum diff ratio to consider two texts as different.
        :rtype: float
        """
        return self.__min_ratio

    @property
    def min_deviation(self):
        """
        :returns: Minimum deviation from the average to consider
            texts to be unique.
        :rtype: float
        """
        return self.__min_deviation

    def analyze(self, text, **kwargs):
        r"""
        If the matching level of text var is sufficient similar
        to the base_text, then, store the text, and anything vars as
        \*\*kargs associated with this text.

        :param text: Text to compare with the base text.
        :type text: str

        :returns: True if the text is accepted as equal, False otherwise.
        :rtype: bool
        """
        if text:
            ratio = get_diff_ratio(self.__base_text, text)
            if ratio > self.__min_ratio:
                self.__clear_caches()
                match = MatchingAnalyzerElement(text, ratio, kwargs)
                self.__matches.append(match)
                return True
        return False

    def __clear_caches(self):
        self.__average_ratio = None
        self.__unique_strings = None
        return

    @property
    def average_ratio(self):
        """
        :returns: Average diff ratio.
        :rtype: float
        """
        if self.__average_ratio is None:
            if self.__matches:
                ratios = sum(match.ratio for match in self.__matches)
                count = len(self.__matches)
                self.__average_ratio = float(ratios) / float(count)
            else:
                self.__average_ratio = 0.0
        return self.__average_ratio

    @property
    def unique_texts(self):
        """
        :returns: List of unique texts.
        :rtype: list(str)
        """
        if self.__unique_strings is None:
            self.__calculate_unique_texts()
        return list(self.__unique_strings)

    def __calculate_unique_texts(self):
        self.__unique_strings = []
        average = self.average_ratio
        if average:
            append = self.__unique_strings.append
            deviation = self.__min_deviation
            for match in self.__matches:
                ratio = match.ratio
                deviated = ratio * deviation
                if not ratio < average < deviated:
                    append(match)