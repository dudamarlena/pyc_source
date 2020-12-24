# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/placeholder.py
# Compiled at: 2019-12-09 07:12:30
# Size of source mod 2**32: 7128 bytes


class Placeholder(object):
    __doc__ = '\n    Table placeholder\n\n    A Placeholder object represents a table in your data model without\n    containing any actual data. They exist to provide a convenient way to\n    define your data model. If the data is loaded directly into a\n    :class:`~getml.engine.DataFrame` there is no need to specify the role of\n    each column.\n\n    Args:\n        name (str): Name of the table, as it will appear in the generated SQL code.\n        categorical (List[str], optional): Names of the columns that you want to be\n            interpreted as categorical variables.\n        discrete (List[str], optional): Names of the columns that you want to be\n            interpreted as discrete variables. \n        numerical (List[str], optional): Names of the columns that you want to\n            be interpreted as numerical variables.\n        join_keys (List[str], optional): Names of the columns that \n            you want to be interpreted as join keys. \n        time_stamps (List[str], optional): Names of the columns that \n            you want to be interpreted as time stamps.\n        targets (List[str], optional): Names of the target variables.\n    '

    def __init__(self, name, categorical=None, discrete=None, numerical=None, join_keys=None, time_stamps=None, targets=None):
        self.thisptr = dict()
        self.thisptr['name_'] = name
        self.thisptr['join_keys_used_'] = []
        self.thisptr['other_join_keys_used_'] = []
        self.thisptr['time_stamps_used_'] = []
        self.thisptr['other_time_stamps_used_'] = []
        self.thisptr['upper_time_stamps_used_'] = []
        self.thisptr['joined_tables_'] = []
        self.thisptr['categorical_'] = categorical or []
        self.thisptr['discrete_'] = discrete or []
        self.thisptr['numerical_'] = numerical or []
        self.thisptr['join_keys_'] = join_keys or []
        self.thisptr['targets_'] = targets or []
        self.thisptr['time_stamps_'] = time_stamps or []
        self.num = Placeholder.num_placeholders
        Placeholder.num_placeholders += 1

    num_placeholders = 0

    def __find_peripheral(self, name):
        for table in self.thisptr['joined_tables_']:
            if table['name_'] == name:
                return table

        for table in self.thisptr['joined_tables_']:
            temp = Placeholder(table['name_'])
            temp.thisptr = table
            subtable = temp._Placeholder__find_peripheral(name)
            if subtable is not None:
                return subtable

    def __replace_empty_strings(self):
        """
        C++ will represent empty arrays as empty strings. We need to fix that.
        """
        for key, value in self.thisptr.items():
            if key == 'name_':
                continue
            if value == '':
                self.thisptr[key] = []

    def __repr__(self):
        return self.thisptr.__repr__()

    def join(self, other, join_key, time_stamp, other_join_key=None, other_time_stamp=None, upper_time_stamp=None):
        """
        LEFT JOINS another Placeholder object onto this Placeholder object.

        Args:
            other (:class:`~getml.placeholder.Placeholder`): The other Placeholder.
            join_key (str): The name of the join key used for this Placeholder object.
            time_stamp (str): The name of the time stamp used for this Placeholder object.
            other_join_key (str, optional): The name of the join key used for
                the other Placeholder object. If None, then it will be assumed
                to be equal to *join_key*. Default: None.
            other_time_stamp (str): The name of the time stamp used for the
                other Placeholder object. If None, then it will be assumed to
                be equal to *time_stamp*. Default: None.
            upper_time_stamp (str): Optional additional time stamp in the
                joined table that will be used as an upper bound. This is
                useful for data that can cease to be relevant, such as address
                data after people have moved. Technically, this will add the
                condition (t1.time_stamp < t2.upper_time_stamp OR
                t2.upper_time_stamp IS NULL) to the feature. Default: None.
        """
        if other.num <= self.num:
            raise Exception("You cannot join a placeholder that was created before the placeholder it is joined to. This is to avoid circular dependencies. Please reverse the order in which the placeholders '" + other.thisptr['name_'] + "' and '" + self.thisptr['name_'] + "' are created!")
        other_join_key = other_join_key or join_key
        other_time_stamp = other_time_stamp or time_stamp
        upper_time_stamp = upper_time_stamp or ''
        self.thisptr['join_keys_used_'].append(join_key)
        self.thisptr['other_join_keys_used_'].append(other_join_key)
        self.thisptr['time_stamps_used_'].append(time_stamp)
        self.thisptr['other_time_stamps_used_'].append(other_time_stamp)
        self.thisptr['upper_time_stamps_used_'].append(upper_time_stamp)
        self.thisptr['joined_tables_'].append(other.thisptr)