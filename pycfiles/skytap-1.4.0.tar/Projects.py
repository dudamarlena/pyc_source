# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/Projects.py
# Compiled at: 2016-12-16 14:55:45
"""Support for Skytap API access to projects.

If accessed via the command line (``python -m skytap.Projects``) this will
return the projects from Skytap in a JSON format.
"""
import sys
from skytap.models.Project import Project
from skytap.models.SkytapGroup import SkytapGroup

class Projects(SkytapGroup):
    """Set of Skytap projects.

    Example:

    .. code-block:: python
        p = skytap.Projects()
        print len(p)
    """

    def __init__(self):
        """Initial set of projects."""
        super(Projects, self).__init__()
        self.load_list_from_api('/v2/projects', Project)


if __name__ == '__main__':
    print Projects().main(sys.argv[1:])