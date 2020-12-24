# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/flad/fladw.py
# Compiled at: 2016-07-25 17:17:22
"""
   Flat ASCII Database to load WIN.INI-like files.
"""
import re
from m_lib.flad import flad
from .flad import checking_error

class error(checking_error):
    pass


class section_error(checking_error):
    pass


re_section = re.compile('^ *\\[(.+)\\] *$')

class Flad_WIni(flad.Flad):
    """
      FLAD database is a list of records, where every record is
      a tuple (section_name, keys, section_dictionary).
      Sounds similary to Flad? But it is Flad! The only difference is that
      Flad_WIni has section names and keys (i.e. list of keys and comments
      in every section to preserve comments and desired order of keys).
   """

    def __init__(self):
        flad.Flad.__init__(self, key_sep='=')
        self.first_section = 1

    def __parse_line(self, record, line):
        match = re_section.match(line)
        if match:
            return match.group(1)
        if self.first_section:
            if line.strip() != '':
                raise error('non-empty line before 1st section')
        elif line.strip() == '' or line.lstrip()[0] == ';':
            record[0].append(line)
        else:
            (key, value) = self.split_key(line)
            if key in record[1].keys():
                raise KeyError('field key "' + key + '" already in record')
            record[0].append(key)
            record[1][key] = value
        return 0

    def create_new_record(self):
        return ([], {})

    def feed(self, record, line):
        if line:
            section = self.__parse_line(record, line)
            if section:
                if not self.first_section:
                    self.append((self.section, record[0], record[1]))
                    self.section = section
                    return 1
                self.first_section = 0
                self.section = section
            elif self.first_section and line.strip() != '':
                raise error('non-empty line before 1st section')
        else:
            self.append((self.section, record[0], record[1]))
            del self.section
            del self.first_section
        for record in self:
            klist = record[1]
            if klist:
                l = len(klist) - 1
                if klist[l].strip() == '':
                    del klist[l]

        return 0

    def store_to_file(self, f):
        if type(f) == type(''):
            outfile = open(f, 'w')
        else:
            outfile = f
        flush_section = 0
        for record in self:
            if flush_section:
                outfile.write('\n')
            else:
                flush_section = 1
            outfile.write('[' + record[0] + ']\n')
            if record[1]:
                for key in record[1]:
                    if key.strip() == '' or key.lstrip()[0] == ';':
                        outfile.write(key)
                    else:
                        outfile.write(key + self.key_sep + record[2][key] + '\n')

        if type(f) == type(''):
            outfile.close()

    def find_section(self, section):
        for i in range(0, len(self)):
            record = self[i]
            if record[0] == section:
                return i

        return -1

    def add_section(self, section):
        rec_no = self.find_section(section)
        if rec_no >= 0:
            raise section_error('section [%s] already exists' % section)
        self.append((section, [], {}))

    def del_section(self, section):
        rec_no = self.find_section(section)
        if rec_no < 0:
            raise section_error('section [%s] does not exists' % section)
        del self[rec_no]

    def set_keyvalue(self, section, key, value):
        rec_no = self.find_section(section)
        if rec_no < 0:
            record = (
             section, [key], {key: value})
            self.append(record)
        else:
            record = self[rec_no]
            if key not in record[1]:
                record[1].append(key)
            record[2][key] = value

    def get_keyvalue(self, section, key):
        rec_no = self.find_section(section)
        if rec_no < 0:
            raise section_error('section [%s] does not exists' % section)
        record = self[rec_no]
        if key not in record[1]:
            raise KeyError("section [%s] does not has `%s' key" % (section, key))
        return record[2][key]

    def get_keydefault(self, section, key, default):
        rec_no = self.find_section(section)
        if rec_no < 0:
            return default
        record = self[rec_no]
        if key not in record[1]:
            return default
        return record[2][key]

    def del_key(self, section, key):
        rec_no = self.find_section(section)
        if rec_no < 0:
            raise section_error('section [%s] does not exists' % section)
        record = self[rec_no]
        if key not in record[1]:
            raise KeyError("section [%s] does not has `%s' key" % (section, key))
        klist = record[1]
        del klist[klist.index(key)]
        del record[2][key]


def load_file(f):
    db = Flad_WIni()
    db.load_file(f)
    return db


def load_from_file(f):
    db = Flad_WIni()
    db.load_from_file(f)
    return db