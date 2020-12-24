# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bschumacher/anircbot_venv/lib/python2.7/site-packages/variance/util.py
# Compiled at: 2015-12-27 17:15:53
"""
    Variance - A python configuration manager

    Author: Bill Schumacher <bill@servernet.co>
    License: LGPLv3
    Copyright: 2015 Bill Schumacher, Cerebral Power
** GNU Lesser General Public License Usage
** This file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPLv3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl.html.
"""
import os

def safe_path(file_path):
    if '/' in file_path or '\\' in file_path:
        if file_path.startswith(os.getcwd()) and '..' not in file_path and '~' not in file_path and ';' not in file_path and '&' not in file_path and './' not in file_path:
            return True
    else:
        return True
    return False