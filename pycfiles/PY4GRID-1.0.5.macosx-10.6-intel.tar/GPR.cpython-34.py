# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/org/py4grid/GPR.py
# Compiled at: 2014-08-31 03:22:40
# Size of source mod 2**32: 2723 bytes
"""
PY4GRID : a little framework to simule multiprocessing over a lot of computers
Copyright (C) 2014  João Jorge Pereira Farias Junior
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import threading as trd, socketserver, org.py4grid.GP as gp

class ProcessRemoteClient(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            ser = gp.Serializer(self.request)
            dic = ser.read()
            print('Process client...', self.client_address)
            print('Process function:', "'" + dic['function'] + "'", 'on module:', "'" + dic['filename'] + "'")
            ret = gp.ProcessRemoteWork(dic)
            ser.send(ret)
        except EOFError as eof:
            print('EOFError', ':', eof, ':', 'Final de arquivo encontrado...')
        except Exception as ex:
            raise