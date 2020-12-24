# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/action/record.py
# Compiled at: 2019-12-18 16:13:39
# Size of source mod 2**32: 2749 bytes
"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from asciinema.commands.record import RecordCommand
from asciinema.commands.command import Command
import asciinema.asciicast.v2 as v2
import asciinema.asciicast.raw as raw
import tempfile, os

class HelpMeRecord(RecordCommand):

    def __init__(self, api, filename=None, quiet=False, env=None, env_whitelist='', record_stdin=False, command=None, title='HelpMe Recording', append=False, overwrite=False, record_raw=False):
        if filename is None:
            filename = self.generate_temporary_file()
        Command.__init__(self, quiet=quiet)
        self.api = api
        self.filename = filename
        self.rec_stdin = record_stdin
        self.command = command or os.environ['SHELL']
        self.env_whitelist = ''
        self.title = title
        self.assume_yes = quiet
        self.idle_time_limit = 10
        self.append = append
        self.overwrite = overwrite
        self.raw = record_raw
        self.recorder = raw.Recorder() if record_raw else v2.Recorder()
        self.env = env if env is not None else os.environ

    def generate_temporary_file(self, folder='/tmp', prefix='helpme', ext='json'):
        """write a temporary file, in base directory with a particular extension.
      
           Parameters
           ==========
           folder: the base directory to write in. 
           prefix: the prefix to use
           ext: the extension to use.

        """
        tmp = next(tempfile._get_candidate_names())
        return '%s/%s.%s.%s' % (folder, prefix, tmp, ext)


def record_asciinema():
    """a wrapper around generation of an asciinema.api.Api and a custom 
       recorder to pull out the input arguments to the Record from argparse.
       The function generates a filename in advance and a return code
       so we can check the final status. 
    """
    import asciinema.config as aconfig
    from asciinema.api import Api
    cfg = aconfig.load()
    api = Api(cfg.api_url, os.environ.get('USER'), cfg.install_id)
    recorder = HelpMeRecord(api)
    code = recorder.execute()
    if code == 0:
        if os.path.exists(recorder.filename):
            return recorder.filename
    print('Problem generating %s, return code %s' % (recorder.filename, code))