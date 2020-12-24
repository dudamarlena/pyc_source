# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mindmeister/connections.py
# Compiled at: 2012-05-17 15:30:03
"""
Copyright 2012 Alexey Kravets  <mr.kayrick@gmail.com>

This file is part of PythonMindmeister.

PythonMindmeister is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PythonMindmeister is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PythonMindmeister.  If not, see <http://www.gnu.org/licenses/>.

This file contains MindMeister API calls for connections. Additional
information can be found by this URL:
http://www.mindmeister.com/developers/explore

This product uses the MindMeister API but is not endorsed or certified
by MindMeister.
"""
import common, parser
from diagnostic import MindException

def add(token, from_id, map_id, to_id):
    """
    Adds connection.

    Arguments:
    from_id
    map_id
    to_id
    Optional (keyword) Arguments:

    This function calls mm.connections.add MindMeister API method
    More documentation can be found by this URL:
    http://www.mindmeister.com/developers/explore_method?method=mm.connections.add
    """
    rawResult = common.performRequest('rest', token, method='mm.connections.add', from_id=from_id, map_id=map_id, to_id=to_id)
    root = parser.parse('mm.connections.add', rawResult)
    if root.attrib['stat'] != 'ok':
        raise MindException('mm.connections.add', root[0])


def changeColor(token, color, from_id, map_id, to_id):
    """
    Changes color of the connection.

    Arguments:
    color
    from_id
    map_id
    to_id
    Optional (keyword) Arguments:

    This function calls mm.connections.changeColor MindMeister API method
    More documentation can be found by this URL:
    http://www.mindmeister.com/developers/explore_method?method=mm.connections.changeColor
    """
    rawResult = common.performRequest('rest', token, method='mm.connections.changeColor', color=color, from_id=from_id, map_id=map_id, to_id=to_id)
    root = parser.parse('mm.connections.changeColor', rawResult)
    if root.attrib['stat'] != 'ok':
        raise MindException('mm.connections.changeColor', root[0])


def delete(token, from_id, map_id, to_id):
    """
    Deletes connection.

    Arguments:
    from_id
    map_id
    to_id
    Optional (keyword) Arguments:

    This function calls mm.connections.delete MindMeister API method
    More documentation can be found by this URL:
    http://www.mindmeister.com/developers/explore_method?method=mm.connections.delete
    """
    rawResult = common.performRequest('rest', token, method='mm.connections.delete', from_id=from_id, map_id=map_id, to_id=to_id)
    root = parser.parse('mm.connections.delete', rawResult)
    if root.attrib['stat'] != 'ok':
        raise MindException('mm.connections.delete', root[0])