# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/utils/lint_helpers.py
# Compiled at: 2019-10-28 10:52:21
# Size of source mod 2**32: 1907 bytes
""" MultiQC lint helpers. Simple additional tests to run when
--lint is specified (outside scope of normal functions) """
from __future__ import print_function
import os, yaml
from multiqc.utils import config, report
logger = config.logger

def run_tests():
    """ Run all lint tests """
    if config.lint:
        check_mods_docs_readme()


def check_mods_docs_readme():
    """ Check that all modules are listed in the YAML index
    at the top of docs/README.md """
    docs_mods = []
    readme_fn = os.path.join(os.path.dirname(config.MULTIQC_DIR), 'docs', 'README.md')
    if not os.path.isfile(readme_fn):
        if os.environ.get('TRAVIS_BUILD_DIR') is not None:
            readme_fn = os.path.join(os.environ.get('TRAVIS_BUILD_DIR'), 'docs', 'README.md')
        else:
            logger.warn("Can't check docs readme in lint test as file doesn't exist: {}".format(readme_fn))
            return
    with open(readme_fn) as (f):
        fm = next(yaml.load_all(f, Loader=(yaml.SafeLoader)))
    for section in fm['MultiQC Modules']:
        for name, fn in fm['MultiQC Modules'][section].items():
            docs_mods.append(fn[8:-3])

    for m in config.avail_modules.keys():
        if m not in docs_mods and m != 'custom_content':
            errmsg = "LINT: Module '{}' found in installed modules, but not docs/README.md".format(m)
            logger.error(errmsg)
            report.lint_errors.append(errmsg)

    for m in docs_mods:
        if m not in config.avail_modules.keys() and m != 'custom_content':
            errmsg = "LINT: Module '{}' found in docs/README.md, but not installed modules".format(m)
            logger.error(errmsg)
            report.lint_errors.append(errmsg)