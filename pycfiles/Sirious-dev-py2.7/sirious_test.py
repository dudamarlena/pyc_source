# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sirious/plugins/sirious_test.py
# Compiled at: 2011-11-28 10:49:50
from sirious import SiriPlugin

class SiriousTest(SiriPlugin):

    def sirious(self, phrase, plist):
        self.logger.info('sirious() triggered by phrase "%s"' % phrase)
        self.respond("You're damn right I am. Sirious is up and running!")

    sirious.triggers = ['are you serious']

    def ask_test(self, phrase, plist):
        self.logger.info('ask_test() triggered by phrase "%s"' % phrase)
        self.ask(self.ask_test_response, 'Do you think this is a test?')

    ask_test.triggers = ['is this a test']

    def ask_test_response(self, phrase, plist):
        self.logger.info('Got answer for test question')
        self.respond("Well, you've failed.")