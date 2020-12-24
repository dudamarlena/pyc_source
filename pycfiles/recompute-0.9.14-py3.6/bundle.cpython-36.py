# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/recompute/bundle.py
# Compiled at: 2019-03-23 11:20:30
# Size of source mod 2**32: 3601 bytes
"""bundle.py

Bundle encapsulates the local repository in the current directory.
Dependencies are resolved and added to a local database (`.recompute/resync.db`).
pypi package requirements are resolved and added to `requirements.txt`.
Inclusion/Exclusion rules are read from the local configuration files `.recompute/include` and `.recompute/exclude`.

"""
import os
from recompute import process
from recompute import cmd
from recompute import utils
logger = utils.get_logger(__name__)
RSYNC_DB = '.recompute/rsync.db'
REQS = 'requirements.txt'
INCLUDE = '.recompute/include'
EXCLUDE = '.recompute/exclude'

class Bundle(object):
    __doc__ = 'Bundle encapsulates local repository in current folder.'

    def __init__(self, name=None):
        """
    Parameters
    ----------
    name : str, optional
      The name (parent) of current directory (default None)
    """
        self.path = os.path.abspath('.')
        self.name = name if name else self.path.split('/')[(-1)]
        self.db = RSYNC_DB
        self.init_include_exclude()
        self.update_dependencies()

    def update_dependencies(self):
        """Update dependencies including local files and pypi packages."""
        self.files = list(self.get_local_deps())
        self.files = self.inclusion_exclusion()
        logger.info(' '.join(self.files))
        self.populate_requirements()
        self.requirements = self.get_requirements()
        self.populate_local_deps()

    def init_include_exclude(self):
        """Create include/exclude local configuration files."""
        if not os.path.exists(INCLUDE):
            open(INCLUDE, 'w').close()
        if not os.path.exists(EXCLUDE):
            open(EXCLUDE, 'w').close()

    def inclusion_exclusion(self):
        """Read from include/exclude configuration files and update database."""
        include = [f for f in open(INCLUDE).readlines() if f.strip()]
        exclude = [f for f in open(EXCLUDE).readlines() if f.strip()]
        self.files = [f for f in self.files if f not in exclude]
        self.files.extend(include)
        return list(set(self.files))

    def get_local_deps(self):
        """Resolve local dependencies.

    Run a search for *.py files in current directory.
    """
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in [f for f in filenames if f.endswith('.py')]:
                yield os.path.join(dirpath, filename)

    def populate_local_deps(self):
        """ Write local dependencies to file (local database)."""
        with open(self.db, 'w') as (db):
            for filename in self.files:
                logger.info(filename)
                db.write(filename)
                db.write('\n')

    def populate_requirements(self):
        """Resolve pypi package dependencies and populate requirement.txt."""
        assert process.execute(cmd.REDIRECT_STDOUT_NULL.format(command=(cmd.PIP_REQS)))

    def get_requirements(self):
        """Read from requirements.txt."""
        reqs = [line.replace('\n', '') for line in open(REQS).readlines() if line.replace('\n', '').strip()]
        logger.info(reqs)
        return reqs