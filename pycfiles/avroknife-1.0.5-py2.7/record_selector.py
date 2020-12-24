# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/record_selector.py
# Compiled at: 2015-09-04 08:27:04
import sys
from collections import namedtuple
from avroknife.error import error

class EqualitySelection:
    """Specification of a desired value assigned to a key"
    
    The key can be nested, e.g. 'opt1.opt2'.
    """

    def __init__(self, string_):
        """
        Args:
            string_: a string in a form of "opt1.opt2=val"
        """
        key, value = string_.split('=')
        self.__key = key
        self.__value = value

    def get_key_parts(self):
        """Returns:
            a list of all nesting components of the key
        """
        return self.__key.split('.')

    def get_value(self):
        """Returns:
            value assigned to the key
        """
        return self.__value


class PositionWrtRange(object):
    SMALLER = 1
    INSIDE = 2
    LARGER = 3


class Range:
    """Numerical range"""

    def __init__(self, string):
        """
        Args:
            string: range given in format, e.g., 1-6, -6, 1-. The string
                can be also set to None, which means that range is 
                (-infinity, infinity). """
        self.range_ = [
         None, None]
        if string is not None:
            parts = string.split('-')
            if len(parts) > 2:
                raise Exception(("Too many elements in range specification '{}'.").format(string))
            elif len(parts) == 1:
                number = int(parts[0])
                self.range_ = [number, number]
            else:
                self.range_ = [
                 None, None]
                for i in range(2):
                    if len(parts[i]) != 0:
                        self.range_[i] = int(parts[i])

        return

    def get_position(self, number):
        """@return position of given number with respect to the range"""
        if self.range_[0] is not None:
            if number < self.range_[0]:
                return PositionWrtRange.SMALLER
            if self.range_[1] is not None:
                if number > self.range_[1]:
                    return PositionWrtRange.LARGER
                else:
                    return PositionWrtRange.INSIDE

            else:
                return PositionWrtRange.INSIDE
        elif self.range_[1] is not None:
            if number <= self.range_[1]:
                return PositionWrtRange.INSIDE
            else:
                return PositionWrtRange.LARGER

        else:
            return PositionWrtRange.INSIDE
        return


Record = namedtuple('Record', ['index', 'content'], verbose=False)

class RecordSelector:
    """Allows to iterate over records according to certain selection criteria
    """

    def __init__(self, range_=None, selection=None, limit=None):
        """
        Args:
            range_: a Range object. It defines range of accepted record 
                indexes.
            selection: an EqualitySelection object. It defines values of
                accepted properties of records.
            limit: specifies that only this number of records matching all other 
                constraints should be returned.
        """
        if range_ is None:
            range_ = Range(None)
        self.__range = range_
        self.__selection = selection
        if limit is None:
            limit = sys.maxint
        self.__limit = limit
        return

    @staticmethod
    def __records_in_range(data_store, range_):
        """
        Generates records in the specified range from the given data store
    
        Args:
            data_store: a DataStore object with records
            range_: a Range object specifying the desired records
        Returns:
            records from the given range
        """
        for index, content in enumerate(data_store):
            position = range_.get_position(index)
            if position == PositionWrtRange.SMALLER:
                pass
            elif position == PositionWrtRange.INSIDE:
                yield Record(index, content)
            else:
                raise StopIteration

    @staticmethod
    def __record_fulfills_condition(record, selection):
        """Checks whether a field in Avro records fulfills a condition
    
        Args:
            record: an Avro record as a Python dictionary
            selection: an EqualitySelection object (optional)
        Returns:
            True if a record fulfill the condition
            False otherwise
        """
        if selection is None:
            return True
        else:
            key_parts = selection.get_key_parts()
            value = selection.get_value()
            content = record.content
            try:
                for key_part in key_parts:
                    content = content[key_part]

            except KeyError:
                error(('Specified key not found in the schema: {}').format(('.').join(key_parts)))
                raise

            if content is None and value == 'null':
                return True
            if unicode(content) == unicode(value):
                return True
            return False
            return

    def get_records(self, data_store):
        """
        Args:
            data_store: a DataStore object with records
        Returns:
            Record objects.
        """
        records = self.__records_in_range(data_store, self.__range)
        count = 0
        for record in records:
            if count < self.__limit:
                if self.__record_fulfills_condition(record, self.__selection):
                    count = count + 1
                    yield record
            else:
                raise StopIteration