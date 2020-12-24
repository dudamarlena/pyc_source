# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_source_location.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 7780 bytes
import sys

class ASTSourceLocation(object):
    __doc__ = '\n    This class is used to store information regarding the source position of an element.\n    Attributes:\n        start_line = 0\n        start_column = 0\n        end_line = 0\n        end_column = 0\n    '

    def __init__(self, start_line, start_column, end_line, end_column):
        """
        Standard constructor.
        :param start_line: The start line of the object
        :type start_line: int
        :param start_column: The start column of the object
        :type start_column: int
        :param end_line: The end line of the object
        :type end_line: int
        :param end_column: The end column of the object
        :type end_column: int
        """
        self.start_line = start_line
        self.start_column = start_column
        self.end_line = end_line
        self.end_column = end_column

    @classmethod
    def make_ast_source_position(cls, start_line, start_column, end_line, end_column):
        """
        Factory method of the ASTSourceLocation class.
        :param start_line: The start line of the object
        :type start_line: int
        :param start_column: The start column of the object
        :type start_column: int
        :param end_line: The end line of the object
        :type end_line: int
        :param end_column: The end column of the object
        :type end_column: int
        :return: a new ASTSourceLocation object
        :rtype: ASTSourceLocation
        """
        return cls(start_line=start_line, start_column=start_column, end_line=end_line, end_column=end_column)

    def get_start_line(self):
        """
        Returns the start line of the element.
        :return: the start line as int
        :rtype: int
        """
        return self.start_line

    def get_start_column(self):
        """
        Returns the start column of the element.
        :return: the start column as int
        :rtype: int
        """
        return self.start_column

    def get_end_line(self):
        """
        Returns the end line of the element.
        :return: the end line as int
        :rtype: int
        """
        return self.end_line

    def get_end_column(self):
        """
        Returns the end column of the element.
        :return: the end column as int
        :rtype: int
        """
        return self.end_column

    def equals(self, source_position):
        """
        Checks if the handed over position is equal to this.
        :param source_position: a source position.
        :type source_position: ASTSourceLocation
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(source_position, ASTSourceLocation):
            return False
        return self.get_start_line() == source_position.get_start_line() and self.get_start_column() == source_position.get_start_column() and self.get_end_line() == source_position.get_end_line() and self.get_end_column() == source_position.get_end_column()

    def before(self, source_position):
        """
        Checks if the handed over position is smaller than this.
        :param source_position: a source position.
        :type source_position: ASTSourceLocation
        :return: True if smaller, otherwise False
        :rtype: bool
        """
        if not isinstance(source_position, ASTSourceLocation):
            return False
        else:
            if self.is_predefined_source_position() and source_position.is_predefined_source_position():
                return True
            if self.is_added_source_position() and source_position.is_added_source_position():
                return True
            if self.is_predefined_source_position():
                return True
            if self.is_added_source_position():
                return False
            if self.get_start_line() < source_position.get_start_line():
                return True
            if self.get_start_line() == source_position.get_start_line() and self.get_start_column() < source_position.get_start_column():
                return True
            return False

    @classmethod
    def get_predefined_source_position(cls):
        """
        Returns a source position which symbolizes that the corresponding element is predefined.
        :return: a source position
        :rtype: ASTSourceLocation
        """
        return cls(-1, -1, -1, -1)

    @classmethod
    def get_added_source_position(cls):
        """
        Returns a source position which symbolize that the corresponding element has been added by the solver.
        :return: a source position.
        :rtype: ASTSourceLocation
        """
        return cls(sys.maxsize, sys.maxsize, sys.maxsize, sys.maxsize)

    def is_predefined_source_position(self):
        """
        Indicates whether this represents a predefined source position.
        :return: True if predefined, otherwise False.
        :rtype: bool
        """
        return self.equals(ASTSourceLocation.get_predefined_source_position())

    def is_added_source_position(self):
        """
        Indicates whether this represents an artificially added source position..
        :return: a source position.
        :rtype: ASTSourceLocation
        """
        return self.equals(ASTSourceLocation.get_added_source_position())

    def encloses(self, source_position):
        """
        Checks if the handed over position is enclosed in this source position, e.g.,
            line 0 to 10 encloses lines 0 to 9 etc.
        :param source_position: a source position
        :type source_position: ASTSourceLocation
        :return: True if enclosed, otherwise False.
        :rtype: bool
        """
        if not isinstance(source_position, ASTSourceLocation):
            return False
        else:
            if self.get_start_line() <= source_position.get_start_line() and self.get_end_line() >= source_position.get_end_line() and self.get_start_column() <= source_position.get_start_column() and self.get_end_column() >= source_position.get_end_column():
                return True
            return False

    def __str__(self):
        """
        A string representation of this source position.
        :return: a string representation
        :rtype: str
        """
        if self.is_added_source_position():
            return '<ADDED_BY_SOLVER>'
        else:
            if self.is_predefined_source_position():
                return '<PREDEFINED>'
            return '[' + str(self.get_start_line()) + ':' + str(self.get_start_column()) + ';' + str(self.get_end_line()) + ':' + str(self.get_end_column()) + ']'