# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bdgt/commands/importer.py
# Compiled at: 2014-10-31 03:15:09
import logging, os
from collections import defaultdict
from StringIO import StringIO
import asciitable, yaml
from colorama import Fore
from sqlalchemy.orm.exc import NoResultFound
from bdgt import get_data_dir
from bdgt.commands import ParseIdMixin
from bdgt.importer.parsers import TxParserFactory
from bdgt.models import Account, Category, Transaction
from bdgt.storage.database import session_scope
from bdgt.storage.gateway import save_objects
_log = logging.getLogger(__name__)
_IMPORT_YAML_PATH = os.path.join(get_data_dir(), 'import.yaml')

class BaseCmdImport(object):

    @classmethod
    def _load_parsed_txs(cls, file_obj):
        return yaml.load(file_obj)

    @classmethod
    def _save_parsed_txs(cls, parsed_txs, file_obj):
        yaml.dump(parsed_txs, file_obj)


class CmdAdd(BaseCmdImport, ParseIdMixin):

    def __init__(self, tx_ids):
        if not os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError('You must import transactions first.')
        self.tx_ids = self._parse_tx_ids(tx_ids)

    def __call__(self):
        with open(_IMPORT_YAML_PATH, 'r') as (f):
            i_txs = self._load_parsed_txs(f)
        num_processed = 0
        for i, i_tx in enumerate(i_txs, start=1):
            with session_scope() as (session):
                try:
                    session.query(Account).filter_by(number=i_tx.parsed_tx.account).one()
                except NoResultFound:
                    raise ValueError(("Account number '{}' does not exist.").format(i_tx.parsed_tx.account))

            if i in self.tx_ids:
                i_tx.processed = True
                num_processed += 1

        assert num_processed == len(self.tx_ids)
        with open(_IMPORT_YAML_PATH, 'w+') as (f):
            self._save_parsed_txs(i_txs, f)
        return ('{} transactions added to the staging area.').format(num_processed)


class CmdCommit(BaseCmdImport):
    """
    Either all parsed transactions are committed, or non at all.
    """

    def __init__(self):
        if not os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError('You must import transactions first.')

    def __call__(self):
        with open(_IMPORT_YAML_PATH, 'r') as (f):
            i_txs = self._load_parsed_txs(f)
        txs = []
        cats = []
        for i_tx in i_txs:
            with session_scope() as (session):
                account = session.query(Account).filter_by(number=i_tx.parsed_tx.account).one()
            with session_scope() as (session):
                try:
                    category = session.query(Category).filter_by(name=i_tx.category).one()
                except NoResultFound:
                    category = Category(i_tx.category)
                    cats.append(category)

            if not i_tx.processed:
                raise ValueError('All transactions must be in the staging ' + 'area')
            tx = Transaction(account, i_tx.parsed_tx.date, i_tx.parsed_tx.description, i_tx.parsed_tx.amount, False)
            tx.category = category
            txs.append(tx)

        save_objects(cats)
        save_objects(txs)
        os.remove(_IMPORT_YAML_PATH)
        return ('{} transactions imported.').format(len(txs))


class CmdImport(BaseCmdImport):

    def __init__(self, file_type, file_path, commit):
        if os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError('A previous import has not been processed.')
        self.file_type = file_type
        self.file_path = file_path
        self.commit = commit

    def __call__(self):
        parser = TxParserFactory.create(self.file_type)
        parsed_txs = parser.parse(self.file_path)
        _log.info(("Parsed {} transactions from '{}'").format(len(parsed_txs), self.file_path))
        with open(_IMPORT_YAML_PATH, 'w+') as (f):
            self._save_parsed_txs(parsed_txs, f)
        if self.commit:
            num_txs = len(parsed_txs)
            CmdAdd(('1-{}').format(num_txs))()
            output = CmdCommit()()
        else:
            output = ('Parsed {} transactions from {}.').format(len(parsed_txs), self.file_path)
        return output


class CmdRemove(BaseCmdImport, ParseIdMixin):

    def __init__(self, tx_ids):
        if not os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError('You must import transactions first.')
        self.tx_ids = self._parse_tx_ids(tx_ids)

    def __call__(self):
        with open(_IMPORT_YAML_PATH, 'r') as (f):
            i_txs = self._load_parsed_txs(f)
        num_processed = 0
        for i, i_tx in enumerate(i_txs, start=1):
            if i in self.tx_ids:
                i_tx.processed = False
                num_processed += 1

        assert num_processed == len(self.tx_ids)
        with open(_IMPORT_YAML_PATH, 'w+') as (f):
            self._save_parsed_txs(i_txs, f)
        return ('{} transactions removed from the staging area.').format(num_processed)


class CmdReset(BaseCmdImport):

    def __call__(self):
        os.remove(_IMPORT_YAML_PATH)
        return 'Import process reset successfully.'


class CmdSet(BaseCmdImport, ParseIdMixin):

    def __init__(self, field, value, tx_ids):
        if not os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError('You must import transactions first.')
        self.field = field
        self.value = value
        self.tx_ids = self._parse_tx_ids(tx_ids)

    def __call__(self):
        with open(_IMPORT_YAML_PATH, 'r') as (f):
            i_txs = self._load_parsed_txs(f)
        num_processed = 0
        for i, i_tx in enumerate(i_txs, start=1):
            if i in self.tx_ids:
                if i_tx.processed:
                    raise ValueError('Transaction must not be in the ' + 'staging area.')
                if self.field in ('category', ):
                    with session_scope() as (session):
                        try:
                            session.query(Category).filter_by(name=self.value).one()
                        except NoResultFound:
                            raise ValueError(("Category '{}' not found.").format(self.value))

                    setattr(i_tx, self.field, self.value)
                    num_processed += 1
                elif self.field in ('account', ):
                    setattr(i_tx.parsed_tx, self.field, self.value)
                    num_processed += 1
                else:
                    raise ValueError(("Field '{}' cannot be changed.").format(self.field))

        assert num_processed == len(self.tx_ids)
        with open(_IMPORT_YAML_PATH, 'w+') as (f):
            self._save_parsed_txs(i_txs, f)
        return ('{} transactions updated.').format(num_processed)


class CmdStatus(BaseCmdImport):

    def __init__(self):
        if not os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError('You must import transactions first.')

    def __call__(self):
        with open(_IMPORT_YAML_PATH, 'r') as (f):
            i_txs = self._load_parsed_txs(f)
        processed_output = defaultdict(list)
        unprocessed_output = defaultdict(list)
        for i, i_tx in enumerate(i_txs, start=1):
            if i_tx.processed:
                output = processed_output
            else:
                output = unprocessed_output
            output['id'].append(i)
            output['date'].append(str(i_tx.parsed_tx.date))
            output['account'].append(str(i_tx.parsed_tx.account))
            output['description'].append(i_tx.parsed_tx.description[:130].replace('\n', ' '))
            output['amount'].append(float(i_tx.parsed_tx.amount))
            output['category'].append(i_tx.category)

        output_io = StringIO()

        def format_amount(x):
            if x < 0:
                color = Fore.RED
            else:
                color = Fore.GREEN
            output = ('{}{:.2f}{}').format(color, x, Fore.RESET)
            return output

        if processed_output:
            output_io.write('Transactions ready to commit:\n\n')
            asciitable.write(processed_output, output_io, Writer=asciitable.FixedWidthNoHeader, names=[
             'id', 'date', 'account', 'description', 'category',
             'amount'], formats={'amount': lambda x: format_amount(x)})
            if unprocessed_output:
                output_io.write('\n')
        if unprocessed_output:
            output_io.write('Transactions ready for processing:\n\n')
            asciitable.write(unprocessed_output, output_io, Writer=asciitable.FixedWidthNoHeader, names=[
             'id', 'date', 'account', 'description', 'category',
             'amount'], formats={'amount': lambda x: format_amount(x)})
        return output_io.getvalue()