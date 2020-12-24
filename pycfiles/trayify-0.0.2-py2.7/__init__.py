# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.openbsd-5.1-i386/egg/trayify/__init__.py
# Compiled at: 2012-09-02 18:58:34
import gtk_icon, qt_icon
LICENSE = '\n Copyright (c) 2012, Kristofer M White\n All rights reserved.\n\n Redistribution and use in source and binary forms, with or without\n modification, are permitted provided that the following conditions are\n met:\n\n * Redistributions of source code must retain the above copyright\n   notice, this list of conditions and the following disclaimer.\n * Redistributions in binary form must reproduce the above copyright\n   notice, this list of conditions and the following disclaimer in the\n   documentation and/or other materials provided with the distribution.\n * Neither the name of the software nor the names of its\n   contributors may be used to endorse or promote products derived from\n   this software without specific prior written permission.\n\n THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\n LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A\n PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT\n HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,\n SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT\n LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,\n DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY\n THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\n OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'

class TrayifyError(Exception):
    """ Exception Class for Trayify Errors """

    def __init__(self, value='No value provided'):
        """ Create a TrayifyError instance """
        self.value = value

    def __str__(self):
        """ Define a textual representation of the Instance """
        return ('{0}: {1}').format(self.__class__.__name__, self.value)


class InvalidUserInterfaceError(TrayifyError):
    """ Exception: A bad UI type was passed to Trayify """

    def __init__(self, message='Invalid UI Type'):
        """ Create a new BadUserInterfaceType Exception """
        super(InvalidUserInterfaceError, self).__init__(message)


def initialize(ui_type, *args, **kwargs):
    """ Start-up Trayify """
    if ui_type == 'appindicator':
        return gtk_icon.NotificationIcon('appindicator')
    if ui_type == 'gtk':
        return gtk_icon.NotificationIcon()
    if ui_type == 'qt':
        return qt_icon.NotificationIcon()
    msg = ('{0} is not a valid UI type').format(ui_type)
    raise InvalidUserInterfaceError(msg)