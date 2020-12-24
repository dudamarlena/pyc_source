# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slack_print/slack_print.py
# Compiled at: 2018-05-02 08:42:42
# Size of source mod 2**32: 848 bytes
from slacker import Slacker
import os, sys

class SlackPrint:

    def __init__(self, access_token, channel):
        self.access_token = access_token
        self.channel = channel
        self.slacker = Slacker(access_token)

    def print(self, *objects, sep=' ', end='\n', file=sys.stdout, flush=False):
        print(*objects, sep=sep, end=end, file=file, flush=flush)
        text = sep.join([str(x) for x in objects])
        try:
            self.slacker.chat.post_message(channel=(self.channel),
              text=text)
        except:
            pass

    def upload(self, path):
        try:
            self.slacker.files.upload(file_=path,
              filename=(os.path.basename(path)),
              channels=(self.channel))
        except:
            pass