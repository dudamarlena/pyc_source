# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/neil/Scripts/random_name/build/lib/censusname/censusname.py
# Compiled at: 2015-02-15 14:17:20
# Size of source mod 2**32: 6432 bytes
from pkg_resources import resource_stream, resource_exists
import codecs, random, csv
from . import formatters
SURNAME2000 = 'data/dist.all.last.2000.csv'
SURNAME1990 = 'data/dist.all.last.1990.csv'
MALEFIRST1990 = 'data/dist.male.first.1990.csv'
FEMALEFIRST1990 = 'data/dist.female.first.1990.csv'
MAX_FREQUENCIES = {SURNAME2000: 89.75356, 
 SURNAME1990: 90.483, 
 MALEFIRST1990: 90.04, 
 FEMALEFIRST1990: 90.024}
GIVENNAMEFILES = {'male': MALEFIRST1990, 
 'female': FEMALEFIRST1990}
SURNAMEFILES = {'2000': SURNAME2000}
NAMEFILES = {'given': GIVENNAMEFILES, 
 'surname': SURNAMEFILES}
FORMATTERS = {'surname': [
             formatters.recapitalize_surnames]}

class Censusname(object):
    __doc__ = 'Generate a random name from an arbitrary set of files'

    def __init__(self, nameformat='{given} {surname}', namefiles=None, max_frequencies=None, **kwargs):
        self.namefiles = namefiles or NAMEFILES
        if self.namefiles == NAMEFILES:
            self.max_frequencies = MAX_FREQUENCIES
        if max_frequencies is None:
            max_frequencies = dict((self.namefiles[k][x], 100) for k in list(self.namefiles.keys()) for x in self.namefiles[k])
        self.nameformat = nameformat
        if 'csv_args' in kwargs:
            self.csv_args = kwargs['csv_args']
        else:
            self.csv_args = {'delimiter': ','}
        if 'formatters' in kwargs:
            if type(kwargs['formatters']) is not dict:
                raise TypeError("Keyword argument 'formatters' for censusname() must be a dict.")
            self.formatters = kwargs['formatters']
        else:
            self.formatters = FORMATTERS
        if 'capitalize' in kwargs:
            self.capitalize = kwargs['capitalize']
        else:
            self.capitalize = True

    def generate(self, nameformat=None, capitalize=None, formatters={}, **kwargs):
        """Pick a random name form a specified list of name parts"""
        if nameformat is None:
            nameformat = self.nameformat
        if capitalize is None:
            capitalize = self.capitalize
        lines = self._get_lines(kwargs)
        names = dict((k, v['name']) for k, v in list(lines.items()))
        if capitalize:
            names = dict((k, n.capitalize()) for k, n in list(names.items()))
        merged_formatters = dict()
        try:
            merged_formatters = dict((k, self.formatters.get(k, []) + formatters.get(k, [])) for k in set(list(self.formatters.keys()) + list(formatters.keys())))
        except AttributeError:
            raise TypeError("keyword argument 'formatters' for Censusname.generate() must be a dict")

        if merged_formatters:
            for key, functions in list(merged_formatters.items()):
                for func in functions:
                    names[key] = func(names[key])

        return nameformat.format(**names)

    def _get_lines(self, nametypes):
        datafile, frequency, lines = '', 0.0, {}
        for namepart in list(self.namefiles.keys()):
            datafile = self._pick_file(namepart, nametypes.get(namepart, None))
            frequency = random.uniform(0, self.max_frequencies[datafile])
            lines[namepart] = self.pick_frequency_line(datafile, frequency)

        return lines

    def _pick_file(self, namepart, namekeys=None):
        result = None
        if type(namekeys) is not list:
            namekeys = [
             namekeys]
        if namekeys:
            key = random.choice(namekeys)
            result = self.namefiles[namepart].get(key)
        if result is None:
            return random.choice(list(self.namefiles[namepart].values()))
        else:
            return result

    def pick_frequency_line(self, filename, frequency, cumulativefield='cumulative_frequency'):
        """Given a numeric frequency, pick a line from a csv with a cumulative frequency field"""
        if resource_exists('censusname', filename):
            with resource_stream('censusname', filename) as (b):
                g = codecs.iterdecode(b, 'ascii')
                return self._pick_frequency_line(g, frequency, cumulativefield)
        else:
            with open(filename, encoding='ascii') as (g):
                return self._pick_frequency_line(g, frequency, cumulativefield)

    def _pick_frequency_line(self, handle, frequency, cumulativefield):
        reader = csv.DictReader(handle, **self.csv_args)
        for line in reader:
            if float(line[cumulativefield]) >= frequency:
                return line


_C = Censusname()

def generate(*args, **kwargs):
    return _C.generate(*args, **kwargs)


def main():
    cn = Censusname('{given} {surname}', NAMEFILES, MAX_FREQUENCIES, csv_args={'delimiter': ','})
    print(cn.generate())


if __name__ == '__main__':
    main()