# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pretty_print_dictionary/pretty_dictionary.py
# Compiled at: 2014-09-06 17:58:43
import sys, collections, random, time, re

class Colors(object):

    def __init__(self, order='auto'):
        """
         A class represents colors for the console text.

        :type order : str
        :param order : A string that shows the way that dictionary content is displayed. possible values are<br/>

        'random': randomly choose colors for keys and values.(8 colors)
        'full': choose colors by a predefined order
        'even': choose two colors for keys and values
        """
        random.seed(time.time())
        self.order = order
        if order == 'full':
            self.colors_list = self.__get_full_foreground_color()
            self.__MAX_SIZE = len(self.colors_list)
        if order == 'even':
            self.colors_list = [
             35, 33]
            self.__MAX_SIZE = len(self.colors_list)

    def get_color(self, level):
        """
        Returns a color with respect of a level.

        :type level: int
        :param level: level that the dictionary exists
        """
        if self.order == 'even':
            return '\x1b[' + str(self.colors_list[((level - 1) % self.__MAX_SIZE)]) + 'm'
        else:
            if self.order == 'full':
                return '\x1b[' + str(self.colors_list[((level - 1) % self.__MAX_SIZE)]) + 'm'
            if self.order == 'random':
                return '\x1b[' + str(self.__get_random_foreground_color()) + 'm'
            return '\x1b[' + str(self.__get_random_foreground_color()) + 'm'

    @staticmethod
    def get_end_color():
        """
        Returns a string shows the end of coloring.
        """
        return '\x1b[0m'

    @staticmethod
    def __get_random_foreground_color():
        """
        Returns number represents the foreground color
        """
        return 30 + random.randint(1, 7)

    @staticmethod
    def __get_full_foreground_color():
        """
        Returns a list of numbers shows the color code
        """
        colors_code_list = []
        for i in xrange(1, 9):
            colors_code_list.append(30 + i)

        return colors_code_list


class PrettyDict(object):

    def __init__(self, mdict, fill_char_width=2, fill_char=' ', order='even', show_level='hide'):
        """
        A class prints a dictionary in a human readable manner
        :type mdict: dict
        :param mdict: dictionary to be displayed

        :type fill_char_width: int
        :param fill_char_width: length of indention for printing the key & value

        :type fill_char: str
        :param fill_char: string to be filled in the indention

        :type order: str
        :param order: 'full', 'even', 'random'

        :type show_level: str
        :param show_level: 'show': show the level string, 'hide': do not show a level string
        """
        self.mdict = mdict
        self.fill_char_width = fill_char_width
        self.fill_char = fill_char
        self.level = 0
        self.offset = 1
        self.__order = order
        self.show_level = show_level

    def ppd(self):
        """
        Prints the dictionary
        """
        self.__print(self.mdict, level=self.level)

    def __print(self, mdict, level=1):
        """
        Prepare the view of printing
        """
        color = Colors(self.__order)
        if not isinstance(mdict, dict):
            print >> sys.stderr, 'The given object is not a dictionary:'
        else:
            current_key_color = color.get_color(level=level)
            for key in mdict.keys():
                value = mdict[key]
                if isinstance(value, dict):
                    print current_key_color + self.fill_char * (level * self.fill_char_width) + str(key), ':level %d' % (level + 1) if self.show_level == 'show' else '', color.get_end_color()
                    self.__print(value, level + 1)
                elif isinstance(value, collections.Iterable) and not isinstance(value, str):
                    current_value_color = color.get_color(level=level + 1)
                    print current_key_color + self.fill_char * (level * self.fill_char_width) + str(key), ':level %d' % (level + 1) if self.show_level == 'show' else '', color.get_end_color()
                    r = re.compile('^\\s+', re.MULTILINE)
                    print_statement = []
                    for v in value:
                        v = r.sub('', str(v))
                        if v != '':
                            print_statement += str(v)

                    print_statement = (',').join(print_statement)
                    print current_value_color,
                    print self.fill_char * (level * self.fill_char_width + self.offset) + print_statement,
                    print color.get_end_color() + '\n',
                else:
                    print current_key_color + ' ' * (level * self.fill_char_width) + str(key), ':level %d' % (level + 1) if self.show_level == 'show' else '', color.get_end_color()
                    current_value_color = color.get_color(level=level + 1)
                    print current_value_color,
                    print self.fill_char * (level * self.fill_char_width + self.offset) + str(mdict[key])

    def __repr__(self):
        return 'Pretty Print Dictionary'