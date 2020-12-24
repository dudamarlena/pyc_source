# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/lex_bot_tester/aws/polly/pollyclient.py
# Compiled at: 2018-01-23 20:52:09
"""
    Lex Bot Tester
    Copyright (C) 2017  Diego Torres Milano

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import boto3

class PollyClient:
    """
    Polly Client.
    """

    def __init__(self):
        self.__client = boto3.client('polly')
        self.output_format = 'pcm'
        self.voice_id = 'Nicole'

    def synthesize_speech(self, text):
        return self.__client.synthesize_speech(Text=text, OutputFormat=self.output_format, VoiceId=self.voice_id)