# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/greg/Dropbox/code/dealertrack/flake8-diff/flake8diff/utils.py
# Compiled at: 2015-07-06 16:58:51
from __future__ import unicode_literals, print_function
import logging, subprocess
logger = logging.getLogger(__name__)

def _execute(cmd, strict=False, log_errors=True):
    """
    Make executing a command locally a little less painful
    """
    logger.debug((b'executing {0}').format(cmd))
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return_code = process.wait()
    if return_code != 0 and (err or strict):
        if log_errors:
            logger.error(err)
        if strict:
            raise subprocess.CalledProcessError(return_code, cmd)
    return out.decode(b'utf-8')