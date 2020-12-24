# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vanessa/Documents/Dropbox/Code/share/containershare-python/containershare/validator/library.py
# Compiled at: 2018-07-30 07:34:11
# Size of source mod 2**32: 5751 bytes
"""

validators/library.py: python functions to validate library

Copyright (c) 2018, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
import os, re, sys
from containershare.logger import bot
from glob import glob
from .utils import notvalid
import json

class LibraryValidator:

    def __init__(self, quiet=False):
        if quiet is True:
            bot.level = 0

    def __str__(self):
        return 'containershare.LibraryValidator'

    def validate(self, expfile):
        bot.test('CONTAINER: %s' % os.path.basename(expfile))
        if expfile.endswith('json'):
            return self._validate_json(expfile) or False
        else:
            if expfile.endswith('md'):
                if not self._validate_markdown(expfile):
                    return False
            return True

    def _print_valid(self, result):
        options = {True:'yes', 
         False:'no'}
        return options[result]

    def _validate_markdown(self, expfile):
        """ensure that fields are present in markdown file"""
        try:
            import yaml
        except:
            bot.error('Python yaml is required for testing yml/markdown files.')
            sys.exit(1)

        self.metadata = {}
        uid = os.path.basename(expfile).strip('.md')
        if os.path.exists(expfile):
            with open(expfile, 'r') as (stream):
                docs = yaml.load_all(stream)
                for doc in docs:
                    if isinstance(doc, dict):
                        for k, v in doc.items():
                            print('%s: %s' % (k, v))
                            self.metadata[k] = v

            self.metadata['uid'] = uid
            fields = [
             'github', 'docker', 'web', 'name',
             'tags', 'uid', 'maintainer']
            for field in fields:
                if field not in self.metadata:
                    return False
                if self.metadata[field] in ('', None):
                    return False

            if 'github' not in self.metadata['github']:
                return notvalid('%s: not a valid github repository' % name)
            return isinstance(self.metadata['tags'], list) or notvalid('%s: tags must be a list' % name)
        else:
            if not re.search('(\\w+://)(.+@)*([\\w\\d\\.]+)(:[\\d]+){0,1}/*(.*)', self.metadata['github']):
                return notvalid('%s is not a valid URL.' % content['github'])
            return True

    def _validate_json(self, jsonfile):
        valids = []
        valid = jsonfile.endswith('.json')
        valids.append(valid)
        bot.test('...extension json: %s' % self._print_valid(valid))
        with open(jsonfile, 'r') as (filey):
            content = json.load(filey)
        valid = isinstance(content, dict)
        valids.append(valid)
        bot.test('...json loadable: %s' % self._print_valid(valid))
        if not all(valids):
            return False
        bot.test('Content:')
        name = os.path.basename(jsonfile)
        exp_id = name.replace('.json', '')
        if 'name' not in content:
            return notvalid('"name" not found in %s' % name)
        if exp_id != content['name']:
            return notvalid('"name" not found in %s' % name)
        bot.test('        Name: %s' % content['name'])
        if not re.match('^[a-z0-9_-]*$', content['name']):
            return notvalid('invalid characters in %s, only \n                               lowercase and "-" or "_" allowed.' % content['name'])
        if 'github' not in content:
            return notvalid('"github" not found in %s' % name)
        if not re.search('(\\w+://)(.+@)*([\\w\\d\\.]+)(:[\\d]+){0,1}/*(.*)', content['github']):
            return notvalid('%s is not a valid URL.' % content['github'])
        if not isinstance(content['github'], str):
            return notvalid('%s must be a string' % content['github'])
        else:
            bot.test('        Github: %s' % content['github'])
            if 'maintainer' not in content:
                return notvalid('"maintainer" missing in %s' % name)
            bot.test('        Maintainer: %s' % content['maintainer'])
            return True