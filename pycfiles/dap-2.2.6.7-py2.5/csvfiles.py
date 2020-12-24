# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dap/plugins/csvfiles.py
# Compiled at: 2008-03-31 07:43:16
"""Plugin for CSV (comma separated values) files.

This plugin serves sequential data from a CSV file. It's a bit hackish and
abuses ``lambda`` and ``itertools``, but it works *very* nice. The plugin
uses the ``buildfilter()`` function to create a filter from the constraint
expression, and applies it on-the-fly on the data as it is being read.
"""
__author__ = 'Roberto De Almeida <rob@pydap.org>'
import sys, os.path, re, csv, itertools, urllib
from dap import dtypes
from dap.responses.das import typeconvert
from dap.server import BaseHandler
from dap.exceptions import OpenFileError
from dap.helper import buildfilter, parse_querystring
from dap.util.safeeval import expr_eval
extensions = '^.*\\.(csv|CSV)$'

def lazy_eval(s):
    """Try to evalute expression or fallback to string.
    
        >>> lazy_eval("1")
        1
        >>> lazy_eval("None")
        'None'
    """
    try:
        s = expr_eval(s)
    except:
        pass

    return s


class Handler(BaseHandler):

    def __init__(self, filepath, environ):
        """Handler constructor.
        """
        self.filepath = filepath
        self.environ = environ
        (dir, self.filename) = os.path.split(filepath)
        self.description = 'Comma Separated Values from file %s.' % self.filename

    def _parseconstraints(self, constraints=None):
        """Dataset builder.

        This method opens a CSV reader, extracts the variable names from
        the first line and returns an iterator to the data. Constraint
        expressions or handled by the ``get_filter()`` function and a 
        filter to return only data from the columns corresponding to the
        requested variables.
        """
        try:
            self._file = open(self.filepath)
            reader = csv.reader(self._file)
        except:
            message = 'Unable to open file %s.' % self.filepath
            raise OpenFileError(message)

        (fields, queries) = parse_querystring(constraints)
        dataset = dtypes.DatasetType(name=self.filename)
        dataset.attributes['filename'] = self.filename
        name = self.filename[:-4].split('_', 1)[0]
        seq = dataset[name] = dtypes.SequenceType(name=name)
        fieldnames = reader.next()
        ids = [ '%s.%s' % (seq.name, n) for n in fieldnames ]
        line = reader.next()
        types_ = [ lazy_eval(i) for i in line ]
        types_ = [ typeconvert[type(i)] for i in types_ ]
        if seq.id in fields.keys():
            req_ids = []
        else:
            req_ids = [ ['%s.%s' % (seq.id, var), var][(var in ids)] for var in fields.keys() ]
        if req_ids:
            indexes = []
            for id_ in req_ids:
                if id_ in ids:
                    i = ids.index(id_)
                    indexes.append(i)
                    name = fieldnames[i]
                    type_ = types_[i]
                    seq[name] = dtypes.BaseType(name=name, type=type_)

        for (name, type_) in zip(fieldnames, types_):
            seq[name] = dtypes.BaseType(name=name, type=type_)

        data = itertools.chain([line], reader)
        data = itertools.imap(lambda l: map(lazy_eval, l), data)
        if queries:
            filter1 = buildfilter(queries, ids)
            data = itertools.ifilter(filter1, data)
        if req_ids:
            filter2 = lambda x: [ x[i] for i in indexes ]
            data = itertools.imap(filter2, data)
        slice_ = fields.get(seq.id)
        if slice_:
            slice_ = slice_[0]
            data = itertools.islice(data, slice_.start or 0, slice_.stop or sys.maxint, slice_.step or 1)
        else:
            slices = []
            for var in seq.walk():
                slice_ = fields.get(var.id)
                if slice_:
                    slices.append(slice_[0])

            if slices:
                (start, step, stop) = zip(*[ (s.start or 0, s.step or 1, s.stop or sys.maxint) for s in slices ])
                data = itertools.islice(data, max(start), min(stop), max(step))
        seq.data = data
        return dataset

    def close(self):
        """Close the CSV file."""
        if hasattr(self, '_file'):
            self._file.close()


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()