# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/pip/pip/_internal/commands/hash.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 1735 bytes
from __future__ import absolute_import
import hashlib, logging, sys
from pip._internal.cli.base_command import Command
from pip._internal.cli.status_codes import ERROR
from pip._internal.utils.hashes import FAVORITE_HASH, STRONG_HASHES
from pip._internal.utils.misc import read_chunks, write_output
logger = logging.getLogger(__name__)

class HashCommand(Command):
    __doc__ = '\n    Compute a hash of a local package archive.\n\n    These can be used with --hash in a requirements file to do repeatable\n    installs.\n    '
    usage = '%prog [options] <file> ...'
    ignore_require_venv = True

    def __init__(self, *args, **kw):
        (super(HashCommand, self).__init__)(*args, **kw)
        self.cmd_opts.add_option('-a',
          '--algorithm', dest='algorithm',
          choices=STRONG_HASHES,
          action='store',
          default=FAVORITE_HASH,
          help=('The hash algorithm to use: one of %s' % ', '.join(STRONG_HASHES)))
        self.parser.insert_option_group(0, self.cmd_opts)

    def run(self, options, args):
        if not args:
            self.parser.print_usage(sys.stderr)
            return ERROR
        algorithm = options.algorithm
        for path in args:
            write_output('%s:\n--hash=%s:%s', path, algorithm, _hash_of_file(path, algorithm))


def _hash_of_file(path, algorithm):
    """Return the hash digest of a file."""
    with open(path, 'rb') as (archive):
        hash = hashlib.new(algorithm)
        for chunk in read_chunks(archive):
            hash.update(chunk)

    return hash.hexdigest()