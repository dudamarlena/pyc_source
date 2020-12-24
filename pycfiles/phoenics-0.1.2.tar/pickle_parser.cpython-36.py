# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/flo/Phoenics/master/src/phoenics/utilities/pickle_parser.py
# Compiled at: 2019-11-24 12:43:13
# Size of source mod 2**32: 1528 bytes
"""
Licensed to the Apache Software Foundation (ASF) under one or more 
contributor license agreements. See the NOTICE file distributed with this 
work for additional information regarding copyright ownership. The ASF 
licenses this file to you under the Apache License, Version 2.0 (the 
"License"); you may not use this file except in compliance with the 
License. You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
License for the specific language governing permissions and limitations 
under the License.

The code in this file was developed at Harvard University (2018) and 
modified at ChemOS Inc. (2019) as stated in the NOTICE file.
"""
__author__ = 'Florian Hase'
import pickle

class ParserPickle(object):

    def __init__(self, pickle_file=None):
        self.pickle_file = pickle_file

    def parse(self, pickle_file=None):
        if pickle_file is not None:
            self.pickle_file = pickle_file
        if self.pickle_file is not None:
            with open(self.pickle_file, 'rb') as (content):
                self.parsed_pickle = pickle.load(content)
        return self.parsed_pickle