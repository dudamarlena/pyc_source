# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bogglesolver\boggle_board.py
# Compiled at: 2014-08-30 13:51:56
# Size of source mod 2**32: 4987 bytes
"""Classes that keep track of the board."""
from bogglesolver.twl06 import WORD_LIST
import random

class Boggle:
    __doc__ = '\n    The boggle board.\n\n    This represents the physical board and where each letter is.\n    '

    def __init__(self, num_columns=5, num_rows=5):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.boggle_array = [None] * (self.num_columns * self.num_rows)

    def __str__(self):
        string = ''
        if self.is_full():
            for i, letter in enumerate(self.boggle_array):
                if i % self.num_columns is 0:
                    if i is not 0:
                        string += ' |\n'
                string += ' | ' + letter

            string += ' |\n'
        return string

    def generate_boggle_board(self):
        """Generate a boggle board by randomly selecting letters from valid words."""
        combined_words = ''.join(WORD_LIST)
        self.boggle_array = []
        for i in range(0, self.num_columns * self.num_rows):
            random_number = random.randint(0, len(combined_words) - 1)
            self.boggle_array.append(combined_words[random_number])

    def get_adjacent(self, index, ignore=None, normal_adj=True):
        """
        Get all adjacent indexes.

        Ignore is meant to be the disabled or previously traversed indexes.
        Normal_adj is to toggle between finding words in a boggle board
            and finding all possible words for scrabble.
            True is find words in boggle board. False is to find scrabble
            words.

        :param int index: index to get all adjacent indexes of.
        :param list ignore: optional list of indexes to ignore.
        :param bool normal_adj: whether to use the normal is adjacent
               or ignore it.
        :returns: True if adjacent. False otherwise.
        """
        if ignore is None:
            ignore = []
        if normal_adj:
            row = index // self.num_columns
            column = index % self.num_columns
            if column != 0:
                one_less = index - 1
                if one_less not in ignore:
                    yield one_less
                if row != 0:
                    if one_less - self.num_columns not in ignore:
                        yield one_less - self.num_columns
                if row != self.num_rows - 1:
                    if one_less + self.num_columns not in ignore:
                        yield one_less + self.num_columns
                if column != self.num_columns - 1:
                    one_more = index + 1
                    if one_more not in ignore:
                        yield one_more
                    if row != 0:
                        if one_more - self.num_columns not in ignore:
                            yield one_more - self.num_columns
                    if row != self.num_rows - 1:
                        if one_more + self.num_columns not in ignore:
                            yield one_more + self.num_columns
                    if row != 0:
                        if index - self.num_columns not in ignore:
                            yield index - self.num_columns
                    if row != self.num_rows - 1:
                        if index + self.num_columns not in ignore:
                            yield index + self.num_columns
        else:
            for i in range(0, self.num_rows * self.num_columns):
                if i not in ignore and i is not index:
                    yield i
                    continue

    def insert(self, character, index):
        """
        Insert a character into the boggle array.

        :param str character: character to insert.
        :param int index: index to insert the character at.
        """
        if index < len(self.boggle_array):
            self.boggle_array[index] = character

    def is_full(self):
        """
        If the boggle board has been completely filled.

        :returns: True if full. False otherwise.
        """
        ret_val = True
        size = self.num_rows * self.num_columns
        if len(self.boggle_array) == size:
            for i in range(0, size):
                if self.boggle_array[i] is None:
                    ret_val = False
                    print('Found element of array that was None.')
                    continue

        else:
            print('Boggle array len: %s does not equal size: %s.' % (len(self.boggle_array), size))
            ret_val = False
        return ret_val

    def set_array(self, array):
        """
        Set the boggle array with the one provided.

        :param list array: list to set the boggle array to.
        """
        self.boggle_array = array