# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/re/chomp.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand

class ChompTextAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'chomp-text'
    __aliases__ = ['chompText', 'chompTextAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        tof = False
        counter = 0

        def write_line(self, text):
            if self._right_chomp:
                self.wfile.write(text[self._left_chomp:self._right_chomp * -1])
            else:
                self.wfile.write(text[self._left_chomp:])

        for text in self.rfile.readlines():
            counter += 1
            if counter > self._skip_at_top:
                if len(text) > 2:
                    if chr(12) in text[-3:]:
                        self.log.debug(('chomper detected form feed near end of line {0}').format(counter))
                        text = text[self._left_chomp:text.find(chr(12))]
                        self.wfile.write(text)
                        self.wfile.write(chr(10))
                        while counter < self._page_length + self._skip_at_top:
                            counter += 1
                            self.log.debug(('chomper injecting blank padding line for line {0}').format(counter))
                            self.wfile.write(chr(10))

                        if self._do_form_feed:
                            self.log.debug(('chomper injecting form feed at line {0}').format(counter))
                            self.wfile.write(chr(12))
                        counter = 0
                    else:
                        write_line(self, text)
                else:
                    self.log.debug(('chomper short line at line {0} - no chomping').format(counter))
                    write_line(self, text)
            else:
                self.log.debug(('chomper skipping line {0}').format(counter))

    def parse_action_parameters(self):
        self._skip_at_top = self.process_label_substitutions(self.action_parameters.get('skipAtTop', '0'))
        self._left_chomp = self.process_label_substitutions(self.action_parameters.get('leftChomp', '0'))
        self._right_chomp = self.process_label_substitutions(self.action_parameters.get('rightChomp', '0'))
        self._page_length = self.process_label_substitutions(self.action_parameters.get('pageLength', '66'))
        self._do_form_feed = self.process_label_substitutions(self.action_parameters.get('doFormFeeds', 'NO'))
        self._skip_at_top = int(self._skip_at_top)
        self._left_chomp = int(self._left_chomp)
        self._right_chomp = int(self._right_chomp)
        self._page_length = int(self._page_length)
        if self._do_form_feed.upper() == 'YES':
            self._do_form_feed = True
        else:
            self._do_form_feed = False