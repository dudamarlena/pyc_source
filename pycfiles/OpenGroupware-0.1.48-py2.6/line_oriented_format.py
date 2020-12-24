# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/formats/line_oriented_format.py
# Compiled at: 2012-10-12 07:02:39
from format import Format
from format import COILS_FORMAT_DESCRIPTION_OK
from format import COILS_FORMAT_DESCRIPTION_INCOMPLETE

class LineOrientedFormat(Format):

    def __init__(self):
        Format.__init__(self)
        self.in_counter = 0
        self.out_counter = 0

    def set_description(self, fd):
        code = Format.set_description(self, fd)
        if code[0] == 0:
            self.description = fd
            self._definition = self.description.get('data')
            for field in self.description['data']['fields']:
                if 'kind' not in field:
                    return (COILS_FORMAT_DESCRIPTION_INCOMPLETE,
                     ('Incomplete Description: kind missing from <{0}> field').format(field['name']))

            self._skip_comment = bool(self._definition.get('skipCommentedLines', False))
            self._skip_lines = int(self._definition.get('skipLeadingLines', 0))
            self._skip_blanks = bool(self._definition.get('skipBlankLines', False))
            self._line_delimiter = self._definition.get('lineDelimiter', (13, 10))
            self._discard_on_error = self._definition.get('discardMalformedRecords', False)
            self._allowed_ords = self._definition.get('allowedNonprintableOrdinals', (9,
                                                                                      10,
                                                                                      13))
            return (
             COILS_FORMAT_DESCRIPTION_OK, 'OK')
        else:
            return code

    def next_record_in(self):
        """ Read a single line of input, return None if no more lines are available. """
        x = self._input.readline()
        if len(x) == 0:
            return None
        else:
            return x