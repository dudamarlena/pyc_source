# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/core/check_runner.py
# Compiled at: 2018-09-03 10:17:54
# Size of source mod 2**32: 1495 bytes
import logging, traceback
from .result import CheckResults, FailedCheckResult
logger = logging.getLogger(__name__)

def go_through_checks(target, checks):
    logger.debug('Going through checks.')
    results = _result_generator(target=target, checks=checks)
    return CheckResults(results=results)


def _result_generator(target, checks):
    try:
        for check in checks:
            logger.debug('Checking {}'.format(check.name))
            try:
                yield check.check(target)
            except Exception as ex:
                tb = traceback.format_exc()
                logger.warning('There was an error while performing check: {}'.format(tb))
                yield FailedCheckResult(check, logs=[str(ex)])

    finally:
        target.clean_up()