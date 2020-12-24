# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/txriak/__init__.py
# Compiled at: 2011-03-10 12:34:38
"""
txriak:
Twisted module for communicating with the Riak data store from 
Basho Technologies, Inc. http://basho.com/

Modules based on code originally disbributed by Basho:
    http://riak.basho.com/python_client_api/riak.html
"""
VERSION = '0.3.2'
COPYRIGHT = 'Copyright (c) 2010-2011 Appropriate Solutions, Inc. All right reserved.\nSee txriak.LICENSE for details.\n'
LICENSE = '\n%s\n\nThis file is provided to you under the Apache License,\nVersion 2.0 (the "License"); you may not use this file\nexcept in compliance with the License.  You may obtain\na copy of the License at\n \n  http://www.apache.org/licenses/LICENSE-2.0\n \nUnless required by applicable law or agreed to in writing,\nsoftware distributed under the License is distributed on an\n"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\nKIND, either express or implied.  See the License for the\nspecific language governing permissions and limitations\nunder the License.\n\nThis module is an almost complete copy of the original riak.py provided\nin Basho\'s standard Riak distribution. Only functional change is to use \nTwisted deferreds when communicating with Riak via http and to use \nTwisted logging.\n\nOriginal riak.py was Apache License 2.0. That license is maintained for\nthe txriak module. \n\nCopyrights from the original riak.py module are: \nCopyright 2010 Rusty Klophaus <rusty@basho.com>\nCopyright 2010 Justin Sheehy <justin@basho.com>\nCopyright 2009 Jay Baird <jay@mochimedia.com>\n\nThank you Basho for open sourcing your interface libraries. \n\n' % COPYRIGHT