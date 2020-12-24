# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tuvok/Desktop/projects/packages/flask_optional_routes/flask_optional_routes/optional_routes/route_branch_manager.py
# Compiled at: 2018-03-04 16:51:20
# Size of source mod 2**32: 1052 bytes
import copy
from .route_branch import RouteBranch

class RouteBranchManager:

    def __init__(self):
        first_branch = RouteBranch()
        self.route_branches = [first_branch]

    def get_copy_of_preexisting_branches(self):
        return copy.deepcopy(self.route_branches)

    def add_segment_to_all_branches(self, segment):
        for route_branch in self.route_branches:
            route_branch.append_new_route_segment(segment)

    def add_new_branches_to_route_branches(self, new_branches):
        self.route_branches.extend(new_branches)

    def add_segment_to_a_copy_of_all_branches(self, segment):
        copy_of_preexisting_route_branches = self.get_copy_of_preexisting_branches()
        for route_branch in copy_of_preexisting_route_branches:
            route_branch.append_new_route_segment(segment)

        self.add_new_branches_to_route_branches(copy_of_preexisting_route_branches)

    def get_route_strings(self):
        routes = [route_branch.string for route_branch in self.route_branches]
        return routes