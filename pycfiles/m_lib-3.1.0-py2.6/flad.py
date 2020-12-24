# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/flad/flad.py
# Compiled at: 2016-07-25 17:17:22
"""
   Flat ASCII Database.
   This module implements a very simple database on the flat ASCII files.
"""

class checking_error(Exception):
    pass


def_keysep = ': '

class Flad(list):
    """
      Class to represent memory database.
      FLAD database is a list of records,
      where every record is a dictionary.
   """

    def __init__(self, check_record_func=None, key_sep=def_keysep):
        list.__init__(self)
        self.check_record_func = check_record_func
        self.key_sep = key_sep
        self.comment = ''
        self.wait_comment = 1

    def check_record(self, record):
        if self.check_record_func:
            if callable(self.check_record_func):
                return self.check_record_func(self, record)
            raise TypeError('non-callable restriction function')
        else:
            return 1

    def checking_error(self):
        raise checking_error

    def __setitem__(self, i, item):
        if not self.check_record(item):
            self.checking_error()
        else:
            list.__setitem__(self, i, item)

    def __setslice__(self, i, j, v_list):
        if v_list:
            copy_list = v_list[:]
            for item in v_list:
                if not self.check_record(item):
                    self.checking_error()
                    del copy_list[copy_list.index(item)]

            list.__setslice__(self, i, j, copy_list)

    def append(self, item):
        if not self.check_record(item):
            self.checking_error()
        else:
            list.append(self, item)

    def insert(self, i, item):
        if not self.check_record(item):
            self.checking_error()
        else:
            list.insert(self, i, item)

    def split_key(self, line):
        """
         Split input line to key/value pair and add the pair to dictionary
      """
        if line[(-1)] == '\n':
            line = line[:-1]
        l = line.split(self.key_sep, 1)
        return tuple(l)

    def __parse_line(self, record, line):
        if line == '\n':
            if record:
                self.append(record)
                return 1
        else:
            (key, value) = self.split_key(line)
            if key in record.keys():
                raise KeyError('field key "' + key + '" already in record')
            record[key] = value
        return 0

    def create_new_record(self):
        return {}

    def feed(self, record, line):
        if line:
            if self.wait_comment:
                if line.strip() == '':
                    self.comment = self.comment + '\n'
                    self.wait_string = 0
                    return 0
                if line.lstrip()[0] == '#':
                    self.comment = self.comment + line
                    return 0
                self.wait_comment = 0
            return self.__parse_line(record, line)
        self.append(record)
        return 0

    def load_file(self, f):
        """
         Load a database from file as a list of records.
         Every record is a dictionary of key/value pairs.
         The file is reading as whole - this is much faster, but require
         more memory.
      """
        if type(f) == type(''):
            infile = open(f, 'r')
        else:
            infile = f
        try:
            lines = infile.readlines()
        finally:
            if type(f) == type(''):
                infile.close()

        record = self.create_new_record()
        for line in lines:
            if self.feed(record, line):
                record = self.create_new_record()

        if record:
            self.feed(record, None)
        return

    def load_from_file(self, f):
        """
         Load a database from file as a list of records.
         Every record is a dictionary of key/value pairs.
         The file is reading line by line - this is much slower, but do not
         require so much memory. (On systems with limited virtual memory,
         like DOS, it is even faster - for big files)
      """
        if type(f) == type(''):
            infile = open(f, 'r')
        else:
            infile = f
        record = self.create_new_record()
        try:
            line = infile.readline()
            while line:
                if self.feed(record, line):
                    record = self.create_new_record()
                line = infile.readline()

        finally:
            if type(f) == type(''):
                infile.close()

        if record:
            self.feed(record, None)
        return

    def store_to_file(self, f):
        if type(f) == type(''):
            outfile = open(f, 'w')
        else:
            outfile = f
        flush_record = 0
        if self.comment != '':
            outfile.write(self.comment)
        for record in self:
            copy_rec = record.copy()
            if flush_record:
                outfile.write('\n')
            else:
                flush_record = 1
            if copy_rec:
                for key in list(copy_rec.keys()):
                    outfile.write(key + self.key_sep + copy_rec[key] + '\n')
                    del copy_rec[key]

        if type(f) == type(''):
            outfile.close()


def load_file(f, check_record_func=None):
    """
      Create a database object and load it from file
   """
    db = Flad(check_record_func)
    db.load_file(f)
    return db


def load_from_file(f, check_record_func=None):
    """
      Create a database object and load it from file
   """
    db = Flad(check_record_func)
    db.load_from_file(f)
    return db