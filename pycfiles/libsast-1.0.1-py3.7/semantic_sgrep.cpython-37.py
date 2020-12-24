# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/libsast/core_sgrep/semantic_sgrep.py
# Compiled at: 2020-04-16 20:08:45
# Size of source mod 2**32: 2220 bytes
"""Semantic Grep Core."""
import functools
from argparse import Namespace
from semgrep import sgrep_main
from libsast.logger import init_logger
logger = init_logger(__name__)

def wrap_function(oldfunction, newfunction):

    @functools.wraps(oldfunction)
    def run(*args, **kwargs):
        return newfunction(oldfunction, *args, **kwargs)

    return run


class SemanticGrep:

    def __init__(self, options: dict) -> None:
        self.scan_rules = options.get('sgrep_rules')
        if options.get('match_extensions'):
            self.exts = options.get('match_extensions')
        else:
            self.exts = []
        if options.get('ignore_extensions'):
            self.ignore_extensions = options.get('ignore_extensions')
        else:
            self.ignore_extensions = []
        if options.get('ignore_filenames'):
            self.ignore_filenames = options.get('ignore_filenames')
        else:
            self.ignore_filenames = []
        if options.get('ignore_paths'):
            self.ignore_paths = options.get('ignore_paths')
        else:
            self.ignore_paths = []
        sgrep_main.build_normal_output = wrap_function(sgrep_main.build_normal_output, self._patch)

    def _patch(self, oldfunc, *args, **kwargs):
        return []

    def scan(self, paths: list) -> dict:
        """Do sgrep scan."""
        args = Namespace(autofix=False,
          config=(self.scan_rules),
          dangerously_allow_arbitrary_code_execution_from_rules=False,
          dump_ast=False,
          error=False,
          exclude=[],
          exclude_tests=False,
          generate_config=False,
          json=False,
          lang=None,
          no_rewrite_rule_ids=False,
          output=None,
          pattern=None,
          precommit=False,
          quiet=False,
          r2c=False,
          skip_pattern_validation=False,
          strict=False,
          target=paths,
          test=False,
          test_ignore_todo=False,
          validate=False,
          verbose=False,
          version=False)
        return sgrep_main.main(args)