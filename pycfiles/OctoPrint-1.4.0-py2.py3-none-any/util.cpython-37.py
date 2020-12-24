# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\util.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 1212 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__author__ = 'Gina Häußge <osd@foosel.net>'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License'
from .exceptions import ScriptError
import logging

def execute(command, cwd=None, evaluate_returncode=True, **kwargs):
    do_async = kwargs.get('do_async', kwargs.get('async', False))
    import sarge
    p = None
    try:
        p = sarge.run(command, cwd=cwd, stdout=(sarge.Capture()), stderr=(sarge.Capture()), async_=do_async)
    except Exception:
        logging.getLogger(__name__).exception('Error while executing command: {}'.format(command))
        returncode = p.returncode if p is not None else None
        stdout = p.stdout.text if (p is not None and p.stdout is not None) else ''
        stderr = p.stderr.text if (p is not None and p.stderr is not None) else ''
        raise ScriptError(returncode, stdout, stderr)

    if evaluate_returncode:
        if p.returncode != 0:
            raise ScriptError(p.returncode, p.stdout.text, p.stderr.text)
    else:
        return do_async or (
         p.returncode, p.stdout.text, p.stderr.text)