# -*- coding: utf-8 -*-
 
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
 
#     http://www.opensource.org/licenses/osl-3.0.php
 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
 
from setuptools import setup, find_packages
from simplexml import __version__
 
setup(
    name = 'Very SimpleXML',
    version = __version__,
    description = "SimpleXML is a simple and fast XML encoder/decoder for Python",
    long_description = """SimpleXML is a simple and fast XML encoder/decoder for Python.""",
    keywords = 'simplexml xml',
    author = 'Marcel Nicolay',
    author_email = 'marcel.nicolay@gmail.com',
    url = 'http://www.python-simplexml.org',
    license = 'OSI',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Natural Language :: English',
                   'Natural Language :: Portuguese (Brazilian)',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Topic :: Software Development :: Libraries',
                   ],
    packages = find_packages(),
    package_dir = {"simplexml": "simplexml"},
    include_package_data = True,
)