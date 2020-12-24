# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/oneline/modules/StreamMod.py
# Compiled at: 2015-03-28 13:51:27
"""
Stream Module will take the output
from oneline and compose with another
scripting language's input. In other words

{ScriptingLanguage} [input]
"""
from oneline import ol

class StreamMod(ol.module):

    def start(self):
        print 'Starting Stream Module using language: PHP'
        self.pipeline = ol.stream()

    def receiver(self, message):
        self.pipeline.run(message)

    def end(self):
        print 'Ending Stream module'