# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tuvok/Desktop/projects/packages/flask_optional_routes/flask_optional_routes/optional_routes/route_branch.py
# Compiled at: 2018-03-04 15:58:44
# Size of source mod 2**32: 178 bytes


class RouteBranch:

    def __init__(self):
        self.string = ''

    def append_new_route_segment(self, segment):
        self.string = '{}/{}'.format(self.string, segment)