# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ttr\xml\csv2xml\__init__.py
# Compiled at: 2011-08-12 10:45:58
"""
    2011-07-03 by Jan Vlcinsky
    Inspired by joze nazario csv2xml.py at http://monkey.org/~jose/blog/viewpage.php?page=csv2xml
"""
import cgi, csv, sys, xml.etree.ElementTree as etree, StringIO

class Csv2Xml:

    def __init__(self, fileo, root_name='root', row_name='row', row_num_att=None, dialect=None, delimiter=None, quotechar=None, doublequote=None, skipinitialspace=None, lineterminator=None, quoting=None, encoding='utf-8'):
        self.fileo = fileo
        self.root_name = root_name
        self.row_name = row_name
        self.row_num_att = row_num_att
        self.dialect = dialect
        self.encoding = encoding
        fmttuples = [
         (
          'delimiter', delimiter),
         (
          'quotechar', quotechar),
         (
          'doublequote', doublequote),
         (
          'skipinitialspace', skipinitialspace),
         (
          'lineterminator', lineterminator),
         (
          'quoting', quoting)]
        fmttuples = [ (key, val) for (key, val) in fmttuples if val != None ]
        self.fmtparams = dict(fmttuples)
        self._init_reader_iterator(self.fileo)
        return

    def _init_reader_iterator(self, fileo):
        try:
            if self._reader:
                raise RuntimeError('_init_reader_and_result can be called only once per parser instantiation')
        except AttributeError:
            pass

        if self.dialect:
            self._reader = csv.reader(fileo, self.dialect, **self.fmtparams)
        else:
            self._reader = csv.reader(fileo, **self.fmtparams)
        self._lineno = -1

    def __iter__(self):
        return self

    def next(self):
        while True:
            line = self._reader.next()
            self._lineno += 1
            if self._lineno == 0:
                self._fields = line
                continue
            row_elem = etree.Element(self.row_name)
            if self.row_num_att:
                row_elem.set(self.row_num_att, str(self._lineno))
            for (i, field) in enumerate(self._fields):
                subelem = etree.Element(cgi.escape(field.replace(' ', '_').replace('&', 'and')))
                if i >= len(line):
                    break
                text = cgi.escape(line[i])
                subelem.text = unicode(text, self.encoding)
                row_elem.append(subelem)

            return row_elem

    def as_element(self):
        root = etree.Element(self.root_name)
        while True:
            try:
                row_elem = self.next()
                root.append(row_elem)
            except StopIteration:
                break

        return root

    def as_string(self, encoding='UTF-8'):
        return etree.tostring(self.as_element(), encoding=encoding)


def string2xml(csv_string, root_name='root', row_name='row', row_num_att=None, dialect=None, delimiter=None, quotechar=None, doublequote=None, skipinitialspace=None, lineterminator=None, quoting=None, encoding='UTF-8'):
    buff = StringIO.StringIO(csv_string)
    csv_parser = Csv2Xml(buff, root_name=root_name, row_name=row_name, row_num_att=row_num_att, dialect=dialect, delimiter=delimiter, quotechar=quotechar, doublequote=doublequote, skipinitialspace=skipinitialspace, lineterminator=lineterminator, quoting=quoting)
    res = csv_parser.as_string(encoding=encoding)
    return res


if __name__ == '__main__':
    csv_string = 'a,b,c\n1,2,3\n11,22,33\n111,222,333'
    print string2xml(csv_string, row_num_att='line', encoding='UTF-8', dialect='excel')