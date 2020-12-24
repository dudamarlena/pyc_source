# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/utils/desktop.py
# Compiled at: 2016-08-15 07:59:19
r"""Simple desktop integration for Python. This module provides desktop
environment detection and resource opening support for a selection of common
and standardised desktop environments.

Copyright (C) 2005, 2006, 2007 Paul Boddie <paul@boddie.org.uk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

--------

Desktop Detection
-----------------

To detect a specific desktop environment, use the get_desktop function.
To detect whether the desktop environment is standardised (according to the
proposed DESKTOP_LAUNCH standard), use the is_standard function.

Opening URLs
------------

To open a URL in the current desktop environment, relying on the automatic
detection of that environment, use the desktop.open function as follows:

desktop.open("http://www.python.org")

To override the detected desktop, specify the desktop parameter to the open
function as follows:

desktop.open("http://www.python.org", "KDE") # Insists on KDE
desktop.open("http://www.python.org", "GNOME") # Insists on GNOME

Without overriding using the desktop parameter, the open function will attempt
to use the "standard" desktop opening mechanism which is controlled by the
DESKTOP_LAUNCH environment variable as described below.

The DESKTOP_LAUNCH Environment Variable
---------------------------------------

The DESKTOP_LAUNCH environment variable must be shell-quoted where appropriate,
as shown in some of the following examples:

DESKTOP_LAUNCH="kdialog --msgbox"       Should present any opened URLs in
                                        their entirety in a KDE message box.
                                        (Command "kdialog" plus parameter.)
DESKTOP_LAUNCH="my\ opener"             Should run the "my opener" program to
                                        open URLs.
                                        (Command "my opener", no parameters.)
DESKTOP_LAUNCH="my\ opener --url"       Should run the "my opener" program to
                                        open URLs.
                                        (Command "my opener" plus parameter.)

Details of the DESKTOP_LAUNCH environment variable convention can be found
here: http://lists.freedesktop.org/archives/xdg/2004-August/004489.html

"""
__version__ = '0.2.4'
import os, sys
try:
    import subprocess

    def _run(cmd, shell, wait):
        opener = subprocess.Popen(cmd, shell=shell)
        if wait:
            opener.wait()
        return opener.pid


    def _readfrom(cmd, shell):
        opener = subprocess.Popen(cmd, shell=shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        opener.stdin.close()
        return opener.stdout.read()


    def _status(cmd, shell):
        opener = subprocess.Popen(cmd, shell=shell)
        opener.wait()
        return opener.returncode == 0


except ImportError:
    import popen2

    def _run(cmd, shell, wait):
        opener = popen2.Popen3(cmd)
        if wait:
            opener.wait()
        return opener.pid


    def _readfrom(cmd, shell):
        opener = popen2.Popen3(cmd)
        opener.tochild.close()
        opener.childerr.close()
        return opener.fromchild.read()


    def _status(cmd, shell):
        opener = popen2.Popen3(cmd)
        opener.wait()
        return opener.poll() == 0


import commands

def _is_xfce():
    """Return whether XFCE is in use."""
    try:
        if not os.environ.get('DISPLAY', '').strip():
            vars = 'DISPLAY=:0.0 '
        else:
            vars = ''
        return _readfrom(vars + 'xprop -root _DT_SAVE_MODE', shell=1).strip().endswith(' = "xfce4"')
    except OSError:
        return 0


def get_desktop():
    """
    Detect the current desktop environment, returning the name of the
    environment. If no environment could be detected, None is returned.
    """
    if 'KDE_FULL_SESSION' in os.environ or 'KDE_MULTIHEAD' in os.environ:
        return 'KDE'
    if 'GNOME_DESKTOP_SESSION_ID' in os.environ or 'GNOME_KEYRING_SOCKET' in os.environ:
        return 'GNOME'
    if sys.platform == 'darwin':
        return 'Mac OS X'
    else:
        if hasattr(os, 'startfile'):
            return 'Windows'
        else:
            if _is_xfce():
                return 'XFCE'
            if 'DISPLAY' in os.environ:
                return 'X11'
            return

        return


def use_desktop(desktop):
    """Decide which desktop should be used, based on the detected desktop and a
    supplied 'desktop' argument (which may be None). Return an identifier
    indicating the desktop type as being either "standard" or one of the
    results from the 'get_desktop' function.
    """
    detected = get_desktop()
    if (desktop is None or desktop == 'standard') and is_standard():
        return 'standard'
    else:
        if (desktop is None or desktop == 'Windows') and detected == 'Windows':
            return 'Windows'
        else:
            if (desktop or detected) == 'KDE':
                return 'KDE'
            if (desktop or detected) == 'GNOME':
                return 'GNOME'
            if (desktop or detected) == 'XFCE':
                return 'XFCE'
            if (desktop or detected) == 'Mac OS X':
                return 'Mac OS X'
            if (desktop or detected) == 'X11':
                return 'X11'
            return

        return


def is_standard():
    """
    Return whether the current desktop supports standardised application
    launching.
    """
    return 'DESKTOP_LAUNCH' in os.environ


def open(url, desktop=None, wait=0, dialog_on_error=False):
    """
    Open the 'url' in the current desktop's preferred file browser. If the
    optional 'desktop' parameter is specified then attempt to use that
    particular desktop environment's mechanisms to open the 'url' instead of
    guessing or detecting which environment is being used.

    Suggested values for 'desktop' are "standard", "KDE", "GNOME", "XFCE",
    "Mac OS X", "Windows" where "standard" employs a DESKTOP_LAUNCH environment
    variable to open the specified 'url'. DESKTOP_LAUNCH should be a command,
    possibly followed by arguments, and must have any special characters
    shell-escaped.

    The process identifier of the "opener" (ie. viewer, editor, browser or
    program) associated with the 'url' is returned by this function. If the
    process identifier cannot be determined, None is returned.

    An optional 'wait' parameter is also available for advanced usage and, if
    'wait' is set to a true value, this function will wait for the launching
    mechanism to complete before returning (as opposed to immediately returning
    as is the default behaviour).
    """
    import bauble.utils as utils
    desktop_in_use = use_desktop(desktop)
    cmd = None
    if desktop_in_use == 'standard':
        arg = ('').join([os.environ['DESKTOP_LAUNCH'], commands.mkarg(url)])
        return _run(arg, 1, wait)
    else:
        if desktop_in_use == 'Windows':
            return os.startfile(url)
        if desktop_in_use == 'KDE':
            cmd = [
             'kfmclient', 'exec', url]
        else:
            if desktop_in_use == 'GNOME':
                cmd = [
                 'xdg-open', url]
            elif desktop_in_use == 'XFCE':
                cmd = [
                 'exo-open', url]
            elif desktop_in_use == 'Mac OS X':
                cmd = [
                 'open', url]
            elif desktop_in_use == 'X11' and 'BROWSER' in os.environ:
                cmd = [
                 os.environ['BROWSER'], url]
            if not cmd:
                exe = utils.which('xdg-open')
                if exe:
                    cmd = [
                     exe, url]
            try:
                if not cmd:
                    raise OSError, _('Could not open %(url)s\n\nUnknown desktop environment: %(desktop)s\n\n') % dict(url=url, desktop=desktop_in_use)
            except Exception as e:
                if dialog_on_error:
                    utils.message_dialog(utils.utf8(e))
                else:
                    raise

        return _run(cmd, 0, wait)