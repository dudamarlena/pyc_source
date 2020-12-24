# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbtools.py
# Compiled at: 2017-12-21 16:23:41
# Size of source mod 2**32: 32521 bytes
import psycopg2, psycopg2.extras
from schemes import schemes
from copy import deepcopy
import utils
from utils import dictionify
import exceptions, api

class DbConnection:

    def __init__(self, user, password, host='localhost', database='ark_mainnet'):
        self._conn = psycopg2.connect(host=host,
          database=database,
          user=user,
          password=password)

    def connection(self):
        return self._conn


class DbCursor:

    def __init__(self, user, password, host='localhost', database='ark_mainnet', dbconnection=None):
        if not dbconnection:
            dbconnection = DbConnection(host=host,
              database=database,
              user=user,
              password=password)
        self._cur = dbconnection.connection().cursor()
        self._dict_cur = dbconnection.connection().cursor(cursor_factory=(psycopg2.extras.DictCursor))

    def description(self):
        return self._cur.description

    def execute(self, qry, *args, cur_type=None):
        if not cur_type:
            return (self._cur.execute)(qry, *args)
        if cur_type == 'dict':
            return (self._dict_cur.execute)(qry, *args)

    def fetchall(self, cur_type=None):
        if not cur_type:
            return self._cur.fetchall()
        if cur_type == 'dict':
            self._dict_cur.fetchall()

    def fetchone(self, cur_type=None):
        if not cur_type:
            return self._cur.fetchone()
        if cur_type == 'dict':
            self._dict_cur.fetchone()

    def execute_and_fetchall(self, qry, *args, cur_type=None):
        (self.execute)(qry, *args, **{'cur_type': cur_type})
        return self.fetchall(cur_type=cur_type)

    def execute_and_fetchone(self, qry, *args, cur_type=None):
        (self.execute)(qry, *args, **{'cur_type': cur_type})
        return self.fetchone(cur_type=cur_type)


class DposNode:

    def __init__(self, user, password, host='localhost', database='ark_mainnet'):
        self._cursor = DbCursor(user=user,
          password=password,
          host=host,
          database=database)
        self.scheme = schemes['base']
        self.num_delegates = self.scheme['coin_specific_info']['number_of_delegates']
        self.network = 'ark'

    def account_details(self, address):
        resultset = self._cursor.execute_and_fetchone(' \n        SELECT mem."{mem_accounts[address]}",     mem."{mem_accounts[username]}", \n               mem."{mem_accounts[is_delegate]}", mem."{mem_accounts[second_signature]}", \n               ENCODE(mem."{mem_accounts[public_key]}"::BYTEA, \'hex\'),  ENCODE(mem."{mem_accounts[second_public_key]}"::BYTEA, \'hex\'), \n               mem."{mem_accounts[balance]}",     mem."{mem_accounts[vote]}", \n               mem."{mem_accounts[rate]}",        mem."{mem_accounts[multi_signatures]}"\n        FROM {mem_accounts[table]} as mem\n        WHERE mem."{mem_accounts[address]}" = \'{address}\';\n        '.format(mem_accounts=(self.scheme['mem_accounts']),
          address=address))
        labelset = [
         'address', 'username', 'is_delegate', 'second_signature', 'public_key', 'second_public_key',
         'balance', 'vote', 'rate', 'multisignatures']
        return dictionify(resultset, labelset, single=True)

    def node_height_details(self):
        resultset = self._cursor.execute_and_fetchone('\n        SELECT blocks."{blocks[id]}", blocks."{blocks[timestamp]}",\n        blocks."{blocks[height]}", ENCODE(blocks."{blocks[generator_public_key]}"::BYTEA, \'hex\')\n        FROM {blocks[table]} AS blocks\n        ORDER BY blocks."{blocks[height]}" DESC\n        LIMIT 1;\n        '.format(blocks=(self.scheme['blocks'])))
        labelset = [
         'block_id', 'timestamp', 'height', 'generator_public_key']
        return dictionify(resultset, labelset, single=True)

    def check_node_height(self, max_difference):
        if api.Network(network=(self.network)).status()['height'] - self.node_height_details()['height'] > max_difference:
            return False
        else:
            return True

    def all_delegates(self):
        resultset = self._cursor.execute_and_fetchall('\n        SELECT\n        mem."{mem_accounts[address]}", \n        mem."{mem_accounts[username]}",         \n        mem."{mem_accounts[is_delegate]}",\n        mem."{mem_accounts[second_signature]}", \n        ENCODE(mem."{mem_accounts[public_key]}"::BYTEA, \'hex\'), \n        ENCODE(mem."{mem_accounts[second_public_key]}"::BYTEA, \'hex\'),\n        mem."{mem_accounts[balance]}",          \n        mem."{mem_accounts[vote]}", \n        mem."{mem_accounts[rate]}",             \n        mem."{mem_accounts[multi_signatures]}"\n        FROM {mem_accounts[table]} AS mem\n        WHERE mem."{mem_accounts[is_delegate]}" = 1\n        '.format(mem_accounts=(self.scheme['mem_accounts'])))
        labelset = [
         'address', 'username', 'is_delegate', 'second_signature', 'public_key', 'second_public_key',
         'balance', 'vote', 'rate', 'multisignatures']
        return dictionify(resultset, labelset)

    def current_delegates(self):
        resultset = self._cursor.execute_and_fetchall('\n        SELECT mem."{mem_accounts[username]}",         mem."{mem_accounts[is_delegate]}",\n               mem."{mem_accounts[second_signature]}", mem."{mem_accounts[address]}", \n               ENCODE(mem."{mem_accounts[public_key]}"::BYTEA, \'hex\'), ENCODE(mem."{mem_accounts[second_public_key]}"::BYTEA, \'hex\'),\n               mem."{mem_accounts[balance]}",          mem."{mem_accounts[vote]}", \n               mem."{mem_accounts[rate]}",             mem."{mem_accounts[multi_signatures]}" \n        FROM {mem_accounts[table]} AS mem\n        WHERE mem."{mem_accounts[is_delegate]}" = 1\n        ORDER BY mem."{mem_accounts[vote]}" DESC\n        LIMIT {num_delegates}\n        '.format(mem_accounts=(self.scheme['mem_accounts']), num_delegates=(self.num_delegates)))
        labelset = [
         'username', 'is_delegate', 'second_signature', 'address', 'public_key', 'second_public_key',
         'balance', 'vote', 'rate', 'multisignatures']
        return dictionify(resultset, labelset)

    def payouts_to_address(self, address):
        resultset = self._cursor.execute_and_fetchall('\n            SELECT DISTINCT trs."{transactions[id]}", trs."{transactions[amount]}",\n                   trs."{transactions[timestamp]}", trs."{transactions[recipient_id]}",\n                   trs."{transactions[sender_id]}", trs."{transactions[type]}", \n                   trs."{transactions[fee]}", mem."{mem_accounts[username]}", \n                   ENCODE(mem."{mem_accounts[public_key]}"::BYTEA, \'hex\'), blocks."{blocks[height]}"\n            FROM {mem_accounts[table]} mem   \n              INNER JOIN {transactions[table]} trs \n              ON \n              (trs."{transuactions[sender_id]}"=mem."{mem_accounts[address]}")\n              INNER JOIN {blocks[table]} blocks\n              ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}")\n            WHERE trs."{transactions[recipient_id]}" = \'{address}\'\n            AND mem."{mem_accounts[is_delegate]}" = 1 \n            ORDER BY blocks."{blocks[height]}" ASC\n            '.format(transactions=(self.scheme['transactions']),
          mem_accounts=(self.scheme['mem_accounts']),
          address=address,
          blocks=(self.scheme['blocks'])))
        labelset = [
         'tx_id', 'amount', 'timestamp', 'recipient_id', 'sender_id',
         'type', 'fee', 'username', 'public_key', 'height']
        return dictionify(resultset, labelset)

    def transactions_from_address(self, address):
        resultset = self._cursor.execute_and_fetchall('\n            SELECT \n            trs."{transactions[id]}" AS id, \n            trs."{transactions[amount]}",\n            trs."{transactions[timestamp]}", \n            trs."{transactions[recipient_id]}",\n            trs."{transactions[sender_id]}", \n            trs."{transactions[type]}",\n            trs."{transactions[fee]}", \n            blocks."{blocks[height]}"\n            FROM \n            {transactions[table]} AS trs\n              INNER JOIN {blocks[table]} AS blocks\n                 ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}") \n            WHERE \n            trs."{transactions[sender_id]}" = \'{address}\'\n            OR \n            trs."{transactions[recipient_id]}" = \'{address}\'\n            ORDER BY \n            blocks."{blocks[height]}" ASC\n            '.format(transactions=(self.scheme['transactions']), address=address,
          blocks=(self.scheme['blocks'])))
        labelset = [
         'tx_id', 'amount', 'timestamp', 'recipient_id', 'sender_id', 'type', 'fee', 'height']
        return dictionify(resultset, labelset)

    def all_votes_by_address(self, address):
        resultset = self._cursor.execute_and_fetchall('\n            SELECT \n            trs."{transactions[timestamp]}", \n            votes."{votes[votes]}",\n            mem."{mem_accounts[username]}", \n            mem."{mem_accounts[address]}", \n            ENCODE(mem."{mem_accounts[public_key]}"::BYTEA, \'hex\'),\n            blocks."{blocks[height]}"\n            FROM {transactions[table]} AS trs \n                 INNER JOIN {blocks[table]} blocks\n                 ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}")\n                 INNER JOIN {votes[table]} AS votes\n                 ON (trs."{transactions[id]}" = votes."{votes[transaction_id]}")\n                 INNER JOIN {mem_accounts[table]} mem\n                 ON (TRIM(LEADING \'+-\' FROM votes."{votes[votes]}") = ENCODE(mem."{mem_accounts[public_key]}"::BYTEA, \'hex\'))\n            WHERE trs."{transactions[sender_id]}" = \'{address}\'\n        \n            ORDER BY blocks."{blocks[height]}" ASC;\n            '.format(transactions=(self.scheme['transactions']), votes=(self.scheme['votes']),
          mem_accounts=(self.scheme['mem_accounts']),
          address=address,
          blocks=(self.scheme['blocks'])))
        labelset = [
         'timestamp', 'vote', 'username', 'address', 'public_key', 'height']
        return dictionify(resultset, labelset)

    def calculate_balance_over_time(self, address):
        qry = '\n        SELECT * FROM (\n        SELECT \n        \'tx\' AS a,\n        trs."{transactions[id]}" AS b,\n        trs."{transactions[amount]}" AS c, \n        trs."{transactions[fee]}" AS d, \n        trs."{transactions[sender_id]}" AS e, \n        trs."{transactions[timestamp]}" AS f,\n        blocks."{blocks[height]}" AS g\n        FROM {transactions[table]} AS trs \n             INNER JOIN {blocks[table]} blocks\n             ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}")\n        WHERE trs."{transactions[sender_id]}" = \'{address}\'\n        OR trs."{transactions[recipient_id]}" = \'{address}\'\n        UNION\n        SELECT\n        \'block\' AS a, \n        blocks."{blocks[id]}" AS b, \n        blocks."{blocks[reward]}" AS c,\n        blocks."{blocks[total_fee]}" AS d,\n        NULL AS e,\n        blocks."{blocks[timestamp]}" AS f,\n        blocks."{blocks[height]}" AS g\n        FROM blocks \n        WHERE\n        blocks."{blocks[generator_public_key]}" = (\n                    SELECT mem2."{mem_accounts[public_key]}"\n                    FROM {mem_accounts[table]} mem2\n                    WHERE mem2."{mem_accounts[address]}" = \'{address}\')) total\n        \n        ORDER BY total.g ASC\n        '.format(transactions=(self.scheme['transactions']), blocks=(self.scheme['blocks']),
          address=address,
          mem_accounts=(self.scheme['mem_accounts']))
        resultset = self._cursor.execute_and_fetchall(qry)
        res = {}
        balance = 0
        for i in resultset:
            if i[0] == 'tx':
                if i[4] == address:
                    balance -= i[2] + i[3]
                else:
                    balance += i[2]
            else:
                if i[0] == 'block':
                    balance += i[2] + i[3]
            if balance < 0:
                raise exceptions.NegativeBalanceError
            res.update({i[5]: balance})

        return res

    def get_last_out_transactions(self, address):
        resultset = self._cursor.execute_and_fetchall('\n            SELECT\n            trs."{transactions[recipient_id]}",\n            trs."{transactions[timestamp]}",\n            blocks."{blocks[height]}",\n            trs."{transactions[id]}", \n            trs."{transactions[amount]}",\n            trs."{transactions[fee]}"\n            FROM {transactions[table]} trs\n              INNER JOIN {blocks[table]} blocks\n              ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}"),\n            (SELECT \n             MAX(ts."{transactions[timestamp]}") AS max_timestamp, \n             ts."{transactions[recipient_id]}"\n             FROM {transactions[table]} AS ts\n             WHERE ts."{transactions[sender_id]}" = \'{address}\'\n             GROUP BY ts."{transactions[recipient_id]}") AS maxresults\n            \n            WHERE trs."recipientId" = maxresults."recipientId"\n            AND trs."timestamp"= maxresults.max_timestamp;\n            '.format(transactions=(self.scheme['transactions']), address=address,
          blocks=(self.scheme['blocks'])))
        labelset = [
         'recipient_id', 'timestamp', 'height', 'tx_id', 'amount', 'fee']
        return dictionify(resultset, labelset)

    def get_historic_voters(self, address):
        delegate_public_key = self.account_details(address=address)['public_key']
        plusvote = '{{"votes":["+{0}"]}}'.format(delegate_public_key)
        resultset = self._cursor.execute_and_fetchall('\n            SELECT \n            trs."{transactions[sender_id]}", \n            trs."{transactions[timestamp]}",\n            trs."{transactions[id]}",\n            blocks."{blocks[height]}"\n            FROM \n            {transactions[table]} AS trs\n            INNER JOIN {blocks[table]} AS blocks\n                ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}")\n            WHERE \n            trs."{transactions[rawasset]}" = \'{plusvote}\'\n            ORDER BY {blocks[table]}."{blocks[height]}" ASC;\n               '.format(transactions=(self.scheme['transactions']), mem_accounts=(self.scheme['mem_accounts']),
          address=address,
          plusvote=plusvote,
          blocks=(self.scheme['blocks'])))
        labelset = [
         'address', 'timestamp', 'id', 'height']
        return dictionify(resultset, labelset)

    def get_current_voters(self, address):
        resultset = self._cursor.execute_and_fetchall('\n            SELECT \n            trs."{transactions[sender_id]}",\n            trs."{transactions[timestamp]}",\n            trs."{transactions[id]}",\n            blocks."{blocks[height]}" AS block,\n            trs."{transactions[id]}"\n            FROM\n            {transactions[table]} AS trs\n               INNER JOIN {blocks[table]} blocks\n                 ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}")\n            WHERE\n            trs."{transactions[type]}" = 3\n            AND\n            trs."{transactions[sender_id]}" IN (\n                 \n                 SELECT mem."{mem_accounts2delegates[account_id]}"\n                 FROM\n                 {mem_accounts2delegates[table]} AS mem\n                 WHERE\n                 mem."{mem_accounts2delegates[dependent_id]}" = (\n                 SELECT ENCODE(mem2."{mem_accounts[public_key]}"::BYTEA, \'hex\')\n                        FROM {mem_accounts[table]} AS mem2\n                        WHERE mem2."{mem_accounts[address]}" = \'{address}\'           \n              )) \n            ORDER BY block DESC\n            '.format(transactions=(self.scheme['transactions']),
          blocks=(self.scheme['blocks']),
          mem_accounts2delegates=(self.scheme['mem_accounts2delegates']),
          mem_accounts=(self.scheme['mem_accounts']),
          address=address))
        labelset = [
         'address', 'timestamp', 'id', 'height']
        return dictionify(resultset, labelset)

    def get_blocks(self, delegate_address):
        resultset = self._cursor.execute_and_fetchall('\n             SELECT \n             blocks."{blocks[height]}", \n             blocks."{blocks[timestamp]}", \n             blocks."{blocks[id]}", \n             blocks."{blocks[total_fee]}", \n             blocks."{blocks[reward]}"\n             FROM \n             {blocks[table]} AS blocks\n             WHERE \n             blocks."{blocks[generator_public_key]}" = (\n                            SELECT mem."{mem_accounts[public_key]}"\n                            FROM {mem_accounts[table]} AS mem\n                            WHERE mem."{mem_accounts[address]}" = \'{address}\')\n             ORDER BY \n             blocks."{blocks[height]}" ASC\n             '.format(blocks=(self.scheme['blocks']), mem_accounts=(self.scheme['mem_accounts']),
          address=delegate_address))
        labelset = [
         'height', 'timestamp', 'id', 'total_fee', 'reward']
        return dictionify(resultset, labelset)

    def get_events_vote_cluster(self, delegate_address):
        """ Returns all transactions and forged blocks by voters clustered around a single delegate_address"""
        delegate_pubkey = self.account_details(address=delegate_address)['public_key']
        plusvote = '+{delegate_pubkey}'.format(delegate_pubkey=delegate_pubkey)
        resultset = self._cursor.execute_and_fetchall('\n            SELECT *\n             FROM (\n            SELECT \n            trs."{transactions[id]}" AS a,\n            \'transaction\' AS b, \n            trs."{transactions[amount]}" AS c,\n            trs."{transactions[timestamp]}" AS d, \n            trs."{transactions[recipient_id]}" AS e,\n            trs."{transactions[sender_id]}" AS f, \n            trs."{transactions[rawasset]}" AS g,\n            trs."{transactions[type]}" AS h, \n            trs."{transactions[fee]}" AS i, \n            trs."{transactions[block_id]}" AS j,\n            blocks."{blocks[height]}" AS k\n            FROM {transactions[table]} AS trs\n            INNER JOIN {blocks[table]} AS blocks\n                 ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}")\n            WHERE trs."{transactions[sender_id]}" IN\n              (SELECT trs."{transactions[sender_id]}"\n               FROM {transactions[table]} AS trs, {votes[table]} AS votes\n               WHERE trs."{transactions[id]}" = votes."{votes[transaction_id]}"\n               AND votes."{votes[votes]}" = \'{plusvote}\') \n            OR trs."{transactions[recipient_id]}" IN\n              (SELECT trs."{transactions[sender_id]}"\n               FROM {transactions[table]} AS trs, {votes[table]} AS votes\n               WHERE trs."{transactions[id]}" = votes."{votes[transaction_id]}"\n               AND votes."{votes[votes]}" = \'{plusvote}\') \n            UNION\n            SELECT \n            blocks."{blocks[id]}" AS a, \n            \'block\' AS b, \n            blocks."{blocks[reward]}"as c, \n            blocks."{blocks[total_fee]}" AS d,\n            ENCODE(mem."{mem_accounts[public_key]}"::BYTEA, \'hex\') AS e,\n            mem."{mem_accounts[address]}" AS f,\n            mem."{mem_accounts[username]}" AS g,\n            NULL AS h,\n            blocks."{blocks[timestamp]}" AS i,\n            NULL AS j,\n            blocks."{blocks[height]}" AS k\n            FROM blocks\n              INNER JOIN {mem_accounts[table]} AS mem\n              ON (mem."{mem_accounts[public_key]}" = blocks."{blocks[generator_public_key]}")  \n            WHERE\n            blocks."{blocks[generator_public_key]}" IN (\n                    SELECT mem2."{mem_accounts[public_key]}"\n                    FROM {mem_accounts[table]} mem2\n                    WHERE mem2."{mem_accounts[address]}" IN \n                    (SELECT trs."{transactions[sender_id]}"\n                     FROM {transactions[table]} AS trs, {votes[table]} AS votes\n                     WHERE trs."{transactions[id]}" = votes."{votes[transaction_id]}"\n                     AND votes."{votes[votes]}" = \'{plusvote}\') \n               )) total\n               \n            ORDER BY total.k ASC;'.format(address=delegate_address,
          transactions=(self.scheme['transactions']),
          blocks=(self.scheme['blocks']),
          mem_accounts=(self.scheme['mem_accounts']),
          mem_accounts2delegates=(self.scheme['mem_accounts2delegates']),
          votes=(self.scheme['votes']),
          plusvote=plusvote))
        res = {}
        for i in resultset:
            if i[1] == 'transaction':
                res.update({i[0]: {'tx_id':i[0], 
                        'event_type':i[1], 
                        'amount':i[2], 
                        'timestamp':i[3], 
                        'recipient_id':i[4], 
                        'sender_id':i[5], 
                        'rawasset':i[6], 
                        'type':i[7], 
                        'fee':i[8], 
                        'block_id':i[9], 
                        'height':i[10]}})
            else:
                if i[1] == 'block':
                    res.update({i[0]: {'block_id':i[0], 
                            'event_type':i[1], 
                            'reward':i[2], 
                            'total_fee':i[3], 
                            'timestamp':i[8], 
                            'address':i[5], 
                            'username':i[6], 
                            'public_key':i[4], 
                            'height':i[10]}})

        return res

    def tbw(self, delegate_address, blacklist=None, share_fees=False, compound_interest=False):
        """This function doesn't work yet. Instead use legacy.trueshare() for a functional tbw script"""
        if not blacklist:
            blacklist = []
        delegate_public_key = self.account_details(address=delegate_address)['public_key']
        height_at_calculation = self.node_height_details()['height']
        minvote = '{{"votes":["-{0}"]}}'.format(delegate_public_key)
        plusvote = '{{"votes":["+{0}"]}}'.format(delegate_public_key)
        events = self.get_events_vote_cluster(delegate_address)
        votes = self.get_historic_voters(delegate_address)
        blocks = self.get_blocks(delegate_address)
        voter_dict = {}
        for voter in votes:
            voter_dict.update({voter: {'balance':0.0, 
                     'status':False, 
                     'last_payout':votes[voter]['height'], 
                     'share':0.0, 
                     'vote_height':votes[voter]['height'], 
                     'blocks_forged':[]}})

        for blacklisted_address in blacklist:
            voter_dict.pop(blacklisted_address, None)

        last_payout = self.get_last_out_transactions(delegate_address)
        for payout in last_payout:
            try:
                voter_dict[payout]['last_payout'] = last_payout[payout]['height']
            except KeyError:
                pass

        delta_state = {}
        no_state_change = False
        block_keys = sorted(list(blocks.keys()))
        block_nr = 0
        try:
            for id in events:
                if events[id]['height'] > blocks[block_keys[block_nr]]['height']:
                    block_nr += 1
                    if no_state_change:
                        for x in delta_state:
                            voter_dict[x]['share'] += delta_state[x]

                        continue
                    poolbalance = 0
                    delta_state = {}
                    for i in voter_dict:
                        if compound_interest:
                            balance = voter_dict[i]['balance'] + voter_dict[i]['share']
                        else:
                            balance = voter_dict[i]['balance']
                        if voter_dict[i]['status']:
                            poolbalance += balance

                    for i in voter_dict:
                        if compound_interest:
                            balance = voter_dict[i]['balance'] + voter_dict[i]['share']
                        else:
                            balance = voter_dict[i]['balance']
                        if voter_dict[i]['status']:
                            if voter_dict[i]['last_payout'] < blocks[block_keys[block_nr]]['height']:
                                if share_fees:
                                    share = balance / poolbalance * (blocks[block_keys[block_nr]]['reward'] + blocks[block_keys[block_nr]]['totalFee'])
                                else:
                                    share = balance / poolbalance * blocks[block_keys[block_nr]]['reward']
                            voter_dict[i]['share'] += share
                            delta_state.update({i: share})

                    no_state_change = True
                else:
                    no_state_change = False
                    if events[id]['event_type'] == 'transaction':
                        if events[id]['recipient_id'] == 'Acw2vAVA48TcV8EnoBmZKJdV8bxnW6Y4E9':
                            print(events[id]['amount'])
                    if events[id]['event_type'] == 'transaction':
                        if events[id]['recipient_id'] in voter_dict:
                            voter_dict[events[id]['recipient_id']]['balance'] += events[id]['amount']
                        else:
                            if events[id]['sender_id'] in voter_dict:
                                voter_dict[events[id]['sender_id']]['balance'] -= events[id]['amount'] + events[id]['fee']
                            if events[id]['sender_id'] in voter_dict:
                                if events[id]['type'] == 3:
                                    if plusvote in events[id]['rawasset']:
                                        voter_dict[events[id]['sender_id']]['status'] = True
                        if events[id]['sender_id'] in voter_dict:
                            if events[id]['type'] == 3:
                                if minvote in events[id]['rawasset']:
                                    voter_dict[events[id]['sender_id']]['status'] = False
                        if events[id]['event_type'] == 'block':
                            voter_dict[events[id]['address']]['balance'] += events[id]['reward'] + events[id]['total_fee']

            remaining_blocks = len(block_keys) - block_nr - 1
            for i in range(remaining_blocks):
                for x in delta_state:
                    voter_dict[x]['share'] += delta_state[x]

        except IndexError:
            raise

        return (
         voter_dict, height_at_calculation)


class ArkNode(DposNode):

    def __init__(self, user, password, host='localhost', database='ark_mainnet'):
        DposNode.__init__(self, user=user, password=password, host=host, database=database)
        self.scheme.update(schemes['ark'])
        self.num_delegates = self.scheme['coin_specific_info']['number_of_delegates']

    def payouts_to_address(self, address):
        resultset = self._cursor.execute_and_fetchall('\n        SELECT DISTINCT \n        trs."{transactions[id]}", \n        trs."{transactions[amount]}",\n        trs."{transactions[timestamp]}", \n        trs."{transactions[recipient_id]}",\n        trs."{transactions[sender_id]}", \n        trs."{transactions[type]}", \n        trs."{transactions[fee]}", \n        mem."{mem_accounts[username]}", \n        ENCODE(mem."{mem_accounts[public_key]}"::BYTEA, \'hex\'), \n        blocks."{blocks[height]}",\n        trs."{transactions[vendor_field]}"\n        FROM {mem_accounts[table]} mem   \n          INNER JOIN {transactions[table]} trs \n          ON \n          (trs."{transactions[sender_id]}"=mem."{mem_accounts[address]}")\n          INNER JOIN {blocks[table]} blocks\n          ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}")\n        WHERE trs."{transactions[recipient_id]}" = \'{address}\'\n        AND mem."{mem_accounts[is_delegate]}" = 1 \n        ORDER BY blocks."{blocks[height]}" ASC\n        '.format(transactions=(self.scheme['transactions']),
          mem_accounts=(self.scheme['mem_accounts']),
          address=address,
          blocks=(self.scheme['blocks'])))
        labelset = [
         'tx_id', 'amount', 'timestamp', 'recipient_id', 'sender_id',
         'type', 'fee', 'username', 'public_key', 'height', 'vendor_field']
        return dictionify(resultset, labelset)

    def transactions_from_address(self, address):
        resultset = self._cursor.execute_and_fetchall('\n        SELECT \n        trs."{transactions[id]}" AS tx_id, \n        trs."{transactions[amount]}",\n        trs."{transactions[timestamp]}", \n        trs."{transactions[recipient_id]}",\n        trs."{transactions[sender_id]}", \n        trs."{transactions[type]}",\n        trs."{transactions[fee]}",\n        trs."{transactions[rawasset]}",\n        blocks."{blocks[height]}",\n        trs."{transactions[vendor_field]}" \n        FROM \n        {transactions[table]} AS trs\n            INNER JOIN {blocks[table]} AS blocks\n                     ON (blocks."{blocks[id]}" = trs."{transactions[block_id]}")\n        WHERE \n        trs."{transactions[sender_id]}" = \'{address}\'\n        OR \n        trs."{transactions[recipient_id]}" = \'{address}\' \n        ORDER BY \n        blocks."{blocks[height]}" ASC\n        '.format(transactions=(self.scheme['transactions']), address=address,
          blocks=(self.scheme['blocks'])))
        labelset = [
         'tx_id', 'amount', 'timestamp', 'recipient_id', 'sender_id', 'type', 'fee', 'rawasset', 'height', 'vendor_field']
        return dictionify(resultset, labelset)


class OxycoinNode(DposNode):

    def __init__(self, user, password, host='localhost', database='oxycoin_db_main'):
        DposNode.__init__(self, user=user, password=password, host=host, database=database)
        self.scheme.update(schemes['oxycoin'])
        self.num_delegates = self.scheme['coin_specific_info']['number_of_delegates']
        self.network = 'oxy'