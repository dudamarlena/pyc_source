# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\LTTL\Segment.py
# Compiled at: 2016-09-02 09:02:46
# Size of source mod 2**32: 16254 bytes
"""Module Segment.py
Copyright 2012-2016 LangTech Sarl (info@langtech.ch)
---------------------------------------------------------------------------
This file is part of the LTTL package v2.0.

LTTL v2.0 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LTTL v2.0 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LTTL v2.0. If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from operator import itemgetter
from itertools import groupby
import numpy as np, operator
from .Segmentation import Segmentation
from builtins import range
__version__ = '1.0.4'

class Segment(object):
    __doc__ = 'A class for representing a Segmentation, with Numpy constructor'
    __slots__ = [
     'str_index', 'start', 'end', 'annotations']

    def __init__(self, str_index, start=None, end=None, annotations=None):
        """Initialize a Segment instance"""
        if isinstance(str_index, (np.ndarray, list)):
            self.str_index = str_index[0]
            if str_index[1] == np.iinfo(np.int32).max:
                self.start = None
            else:
                self.start = str_index[1]
            if str_index[2] == np.iinfo(np.int32).max:
                self.end = None
            else:
                self.end = str_index[2]
            if start is None:
                self.annotations = dict()
            else:
                self.annotations = start
        else:
            self.str_index = str_index
            self.start = start
            self.end = end
            if annotations is None:
                self.annotations = dict()
            else:
                self.annotations = annotations

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.str_index == other.str_index and self.start == (other.start or 0) and self.end == (other.end or None)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str([getter(self) for getter in [operator.attrgetter(attr) for attr in self.__slots__]])

    def get_real_str_index(self):
        """Return the index of the string which this segment refers to."""
        str_index = self.str_index
        if isinstance(Segmentation.data[str_index], int):
            str_index = Segmentation.data[str_index]
        return str_index

    def to_string(self, formatting=None, humanize_addresses=False, segment_count=0, default_dict=None, progress_callback=None):
        """Stringify a segmentation

        :param formatting: format string for each segment (default None)

        :param humanize_addresses: boolean indicating whether string indices as
        well as start positions in strings should be numbered from 1, rather
        than from 0 as usual (default False)

        :return: formatted string

        In format string, it is possible to use the %(variable_name) format
        notation to insert variable element in each segment's formatted string,
        cf. https://orange-textable.readthedocs.org/en/latest/display.html.
        """
        offset = 1 if humanize_addresses else 0
        str_index = self.str_index + offset
        start = (self.start or 0) + offset
        end = self.end or len(Segmentation.get_data(self.str_index))
        if progress_callback:
            progress_callback()
        if formatting is not None:
            segment_dict = default_dict.copy()
            segment_dict.update(self.annotations)
            segment_dict['__num__'] = segment_count
            segment_dict['__content__'] = self.get_content()
            segment_dict['__str_index__'] = str_index
            segment_dict['__start__'] = start
            segment_dict['__end__'] = end
            segment_dict['__str_index_raw__'] = str_index - offset
            segment_dict['__start_raw__'] = start - offset
            segment_dict['__end_raw__'] = end
            return formatting % segment_dict
        else:
            a = 'segment number %i\n\tcontent:\t"%s"\n\tstr_index:\t%i\n\tstart:\t%i\n\tend:\t%i' % (
             segment_count,
             self.get_content(),
             str_index,
             start,
             end)
            if len(self.annotations):
                a += '\n\tannotations:\n'
                a += '\n'.join(['\t\t%-20s %s' % (k, v) for k, v in sorted(self.annotations.items())])
            return a

    def to_html(self, offset=0, counter=0, progress_callback=None):
        """Stringify a segment in HTML format and returns an iterator.
        Useful when the actual string doesn't fit in memory.

        :param offset: an int that will be added to address element (default 0)

        :param counter: the segment index within a segmentation (default 0)

        :param progress_callback: callback for monitoring progress ticks
        (1 tick per call to this method)

        :return: HTML formatted string
        """
        if progress_callback:
            progress_callback()
        html_string = '<a name="%i"/>\n' % counter
        html_string += '<table width="100%">\n<tr><td class="h" colspan="2">Segment #' + '%s&nbsp;&nbsp;[%s:%s-%s]</td></tr>' % (
         counter,
         self.str_index + offset,
         (self.start or 0) + offset,
         self.end or len(Segmentation.get_data(self.str_index)))
        if len(self.annotations):
            html_string += ''.join('<tr><td class="k">%s</td><td class="v" width="100%%">%s</td></tr>\n' % (k, v) for k, v in sorted(self.annotations.items()))
        content = self.get_content().replace('<', '&lt;')
        content = content.replace('>', '&gt;')
        content = content.replace('\n', '<br/>')
        html_string += '<tr><td colspan="2">%s</td></tr></table>' % content
        return html_string

    def get_content(self):
        """Stringify the content of a Segment

        :return: a string with the segment's content.
        """
        return Segmentation.get_data(self.str_index)[self.start:self.end]

    def deepcopy(self, annotations=None, update=True):
        """Return a deep copy of the segment

        :param annotations: unless set to None (default), a dictionary of
        annotation key-value pairs to be assigned to the new copy of the segment

        :param update: a boolean indicating whether the annotations specified
        in parameter 'annotations' should be added to existing annotations
        (True, default) or replace them (False); if 'annotations' is set to None
        and 'update' is False, the new segment copy will have no annotations.

        :return: a deep copy of the segment
        """
        if update:
            if self.annotations is not None:
                new_annotations = self.annotations.copy()
            else:
                new_annotations = None
            if annotations is not None:
                new_annotations.update(annotations)
        else:
            if annotations is None:
                new_annotations = dict()
            else:
                new_annotations = annotations.copy()
        return Segment(self.str_index, self.start, self.end, new_annotations)

    def contains(self, other_segment):
        """Test if another segment (or segment sequence) is contained in
        this one

        :param other_segment: the segment whose inclusion in this one is being
        tested.

        :return: boolean
        """
        if self.str_index != other_segment.str_index:
            return False
        else:
            if (self.start or 0) > (other_segment.start or 0):
                return False
            string_length = len(Segmentation.get_data(self.str_index))
            if (self.end or string_length) < (other_segment.end or string_length):
                return False
            return True

    def get_contained_segments(self, segmentation):
        """Return segments from another segmentation that are contained in
        this segment

        :param segmentation: the segmentation whose segments will be returned if
        they are contained in the segments of this one.

        :return: a list of segments
        """
        str_index = self.str_index
        start = self.start or 0
        string_length = len(Segmentation.get_data(str_index))
        end = self.end or string_length
        ret = list()
        try:
            start_search = segmentation.str_index_ptr[str_index]
            end_search = min([x for x in segmentation.str_index_ptr.values() if x > start_search] + [
             len(segmentation)])
            while end_search - start_search > 1:
                middle = segmentation[((end_search + start_search) // 2)]
                if (middle.start or 0) >= start:
                    end_search = (end_search + start_search) // 2
                else:
                    start_search = (end_search + start_search) // 2

            if (segmentation[start_search].start or 0) >= start:
                start_search -= 1
            for segment in segmentation[start_search + 1:]:
                if str_index != segment.str_index or (segment.start or 0) > end:
                    break
                if end >= (segment.end or string_length):
                    ret.append(segment)

            return ret
        except:
            return list()

    def get_contained_segment_indices(self, segmentation):
        """Return indices of segments from another segmentation that are
        contained in this segment

        :param segmentation: the segmentation whose segment indices will be
        returned if they are contained in the segments of this one.

        :return: a list of segment indices
        """
        str_index = self.str_index
        start = self.start or 0
        string_length = len(Segmentation.get_data(str_index))
        end = self.end or string_length
        ret = list()
        try:
            start_search = segmentation.str_index_ptr[str_index]
            end_search = min([x for x in segmentation.str_index_ptr.values() if x > start_search] + [
             len(segmentation)])
            while end_search - start_search > 1:
                middle = segmentation[((end_search + start_search) // 2)]
                if (middle.start or 0) >= start:
                    end_search = (end_search + start_search) // 2
                else:
                    start_search = (end_search + start_search) // 2

            if (segmentation[start_search].start or 0) >= start:
                start_search -= 1
            for i, segment in enumerate(segmentation[start_search + 1:]):
                if str_index != segment.str_index or (segment.start or 0) > end:
                    break
                if end >= (segment.end or string_length):
                    ret.append(i + (start_search + 1))

            return ret
        except:
            return list()

    def get_contained_sequence_indices(self, segmentation, length):
        """Return indices of first position of sequences of segments from
        another segmentation that are contained in this segment

        :param segmentation: the segmentation whose segment indices will be
        returned if they are contained in the segments of this one.

        :param length: the length of segment sequences.

        :return: a list of segment indices
        """
        contained_indices = self.get_contained_segment_indices(segmentation)
        contained_idx_sequences = [list(map(itemgetter(1), g)) for _, g in groupby(enumerate(contained_indices), lambda args: args[0] - args[1])]
        fixed_length_idx_sequences = list()
        for contained_idx_sequence in contained_idx_sequences:
            fixed_length_idx_sequences.extend([contained_idx_sequence[idx] for idx in range(len(contained_idx_sequence) - length + 1)])

        return fixed_length_idx_sequences