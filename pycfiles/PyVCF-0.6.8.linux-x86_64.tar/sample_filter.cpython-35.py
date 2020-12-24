# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/vcf/sample_filter.py
# Compiled at: 2016-03-18 12:18:31
# Size of source mod 2**32: 4023 bytes
import logging, sys, warnings
from .parser import Reader, Writer

class SampleFilter(object):
    __doc__ = '\n    Modifies the vcf Reader to filter each row by sample as it is parsed.\n\n    '

    def __init__(self, infile, outfile=None, filters=None, invert=False):

        def get_filter(self):
            return self._samp_filter

        def set_filter(self, filt):
            self._samp_filter = filt
            if filt:
                self.samples = [val for idx, val in enumerate(self.samples) if idx not in set(filt)]

        def filter_samples(fn):
            """Decorator function to filter sample parameter"""

            def filt(self, samples, *args):
                samples = [val for idx, val in enumerate(samples) if idx not in set(self.sample_filter)]
                return fn(self, samples, *args)

            return filt

        Reader.sample_filter = property(get_filter, set_filter)
        Reader._samp_filter = []
        self._orig_parse_samples = Reader._parse_samples
        Reader._parse_samples = filter_samples(Reader._parse_samples)
        self.parser = Reader(filename=infile)
        self.samples = self.parser.samples
        self.smp_idx = dict([(v, k) for k, v in enumerate(self.samples)])
        self.outfile = outfile
        self.invert = invert
        self.filters = filters
        if filters is not None:
            self.set_filters()
            self.write()

    def __del__(self):
        try:
            self._undo_monkey_patch()
        except AttributeError:
            pass

    def set_filters(self, filters=None, invert=False):
        """Convert filters from string to list of indices, set on Reader"""
        if filters is not None:
            self.filters = filters
        if invert:
            self.invert = invert
        filt_l = self.filters.split(',')
        filt_s = set(filt_l)
        if len(filt_s) < len(filt_l):
            warnings.warn('Non-unique filters, ignoring', RuntimeWarning)

        def filt2idx(item):
            """Convert filter to valid sample index"""
            try:
                item = int(item)
            except ValueError:
                return self.smp_idx.get(item)
            else:
                if item < len(self.samples):
                    return item

        filters = set([x for x in map(filt2idx, filt_s) if x is not None])
        if len(filters) < len(filt_s):
            warnings.warn('Invalid filters, ignoring', RuntimeWarning)
        if self.invert:
            filters = set(range(len(self.samples))).difference(filters)
        self.parser.sample_filter = filters
        if len(self.parser.samples) == 0:
            warnings.warn('Number of samples to keep is zero', RuntimeWarning)
        logging.info('Keeping these samples: {0}\n'.format(self.parser.samples))
        return self.parser.samples

    def write(self, outfile=None):
        if outfile is not None:
            self.outfile = outfile
        if self.outfile is None:
            _out = sys.stdout
        else:
            if hasattr(self.outfile, 'write'):
                _out = self.outfile
            else:
                _out = open(self.outfile, 'wb')
        logging.info("Writing to '{0}'\n".format(self.outfile))
        writer = Writer(_out, self.parser)
        for row in self.parser:
            writer.write_record(row)

    def _undo_monkey_patch(self):
        Reader._parse_samples = self._orig_parse_samples
        delattr(Reader, 'sample_filter')