#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from setuptools import setup, find_packages

__updated__ = "2019-04-11"
__author__ = "Aurélien Moreau"
__copyright__ = "Copyright 2019, Angus.ai"
__credits__ = ["Aurélien Moreau"]
__license__ = "Apache v2.0"
__maintainer__ = "Aurélien Moreau"
__status__ = "Production"

__version__ = "1.0.0"

setup(name='timedeltaparser',
      version=__version__,
      description='Parse a string that represents a timedelta',
      author=__author__,
      author_email='aurelien.moreau@angus.ai',
      url='http://www.angus.ai/',
      install_requires=[
      ],
      license=__license__,
      packages=find_packages(exclude=['tests']),
      )
