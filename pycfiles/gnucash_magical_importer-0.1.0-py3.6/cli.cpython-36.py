# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gnucash_importer/cli.py
# Compiled at: 2018-11-28 19:46:12
# Size of source mod 2**32: 864 bytes
"""Main Module responsibility for all command line fuctions."""
import logging
from termcolor import colored
from util import Util
from ledger import Ledger

class Cli:
    __doc__ = 'This class will coordinate all actions.'

    def import_data(account, currency, dry_run, gnucash_file):
        """
        Import data from a given file into a given gnucash file.

        Must have an account and a gnucash file defined.
        Is optional define the currency (default can setted in seupt.cfg - usiing BRL).
        Also, is optional define dry_run (default is **true**).
        """
        logging.info(Util.info('Importing data to ') + colored('{a}'.format(a=(account.name)), 'yellow', attrs=['bold', 'underline']) + Util.info("'s account"))
        Ledger(account, currency, dry_run, gnucash_file).write()