# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/action/submit.py
# Compiled at: 2019-12-18 16:16:41
# Size of source mod 2**32: 1781 bytes
"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from helpme.logger import bot
import os, re

def upload_asciinema(filename):
    """a wrapper around generation of an asciinema.api.Api to call the 
       upload command given an already existing asciinema file. 

       Parameters
       ==========
       filename: the asciinema file to upload, can be generated with 
                 function record_asciinema in record.py

    """
    if os.path.exists(filename):
        try:
            from asciinema.commands.upload import UploadCommand
            import asciinema.config as aconfig
            from asciinema.api import Api
        except:
            bot.exit('The asciinema module is required to submit an asciinema recording. Try pip install helpme[asciinema]')

        cfg = aconfig.load()
        api = Api(cfg.api_url, os.environ.get('USER'), cfg.install_id)
        uploader = UploadCommand(api, filename)
        try:
            url, warn = uploader.api.upload_asciicast(filename)
            if warn:
                uploader.print_warning(warn)
            if url:
                match = re.search('https://.+', url)
                if match:
                    url = match.group()
            return url
        except:
            bot.error('Problem with upload, skipping')

    else:
        bot.warning('Cannot find %s, skipping submission.' % filename)