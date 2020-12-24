# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_internal/commands/uninstall.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 2983 bytes
from __future__ import absolute_import
from pip._vendor.packaging.utils import canonicalize_name
from pip._internal.cli.base_command import Command
from pip._internal.cli.req_command import SessionCommandMixin
from pip._internal.exceptions import InstallationError
from pip._internal.req import parse_requirements
from pip._internal.req.constructors import install_req_from_line
from pip._internal.utils.misc import protect_pip_from_modification_on_windows

class UninstallCommand(Command, SessionCommandMixin):
    __doc__ = '\n    Uninstall packages.\n\n    pip is able to uninstall most installed packages. Known exceptions are:\n\n    - Pure distutils packages installed with ``python setup.py install``, which\n      leave behind no metadata to determine what files were installed.\n    - Script wrappers installed by ``python setup.py develop``.\n    '
    usage = '\n      %prog [options] <package> ...\n      %prog [options] -r <requirements file> ...'

    def __init__(self, *args, **kw):
        (super(UninstallCommand, self).__init__)(*args, **kw)
        self.cmd_opts.add_option('-r',
          '--requirement', dest='requirements',
          action='append',
          default=[],
          metavar='file',
          help='Uninstall all the packages listed in the given requirements file.  This option can be used multiple times.')
        self.cmd_opts.add_option('-y',
          '--yes', dest='yes',
          action='store_true',
          help="Don't ask for confirmation of uninstall deletions.")
        self.parser.insert_option_group(0, self.cmd_opts)

    def run(self, options, args):
        session = self.get_default_session(options)
        reqs_to_uninstall = {}
        for name in args:
            req = install_req_from_line(name,
              isolated=(options.isolated_mode))
            if req.name:
                reqs_to_uninstall[canonicalize_name(req.name)] = req

        for filename in options.requirements:
            for req in parse_requirements(filename,
              options=options,
              session=session):
                if req.name:
                    reqs_to_uninstall[canonicalize_name(req.name)] = req

        if not reqs_to_uninstall:
            raise InstallationError('You must give at least one requirement to %(name)s (see "pip help %(name)s")' % dict(name=(self.name)))
        protect_pip_from_modification_on_windows(modifying_pip=('pip' in reqs_to_uninstall))
        for req in reqs_to_uninstall.values():
            uninstall_pathset = req.uninstall(auto_confirm=(options.yes),
              verbose=(self.verbosity > 0))
            if uninstall_pathset:
                uninstall_pathset.commit()