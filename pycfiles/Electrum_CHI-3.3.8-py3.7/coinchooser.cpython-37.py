# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/coinchooser.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 21080 bytes
from collections import defaultdict
from math import floor, log10
from typing import NamedTuple, List, Callable
from decimal import Decimal
from .bitcoin import sha256, COIN, TYPE_ADDRESS, is_address
from .transaction import Transaction, TxOutput
from .util import NotEnoughFunds
from .logging import Logger

class PRNG:

    def __init__(self, seed):
        self.sha = sha256(seed)
        self.pool = bytearray()

    def get_bytes(self, n):
        while len(self.pool) < n:
            self.pool.extend(self.sha)
            self.sha = sha256(self.sha)

        result, self.pool = self.pool[:n], self.pool[n:]
        return result

    def randint(self, start, end):
        n = end - start
        r = 0
        p = 1
        while p < n:
            r = self.get_bytes(1)[0] + (r << 8)
            p = p << 8

        return start + r % n

    def choice(self, seq):
        return seq[self.randint(0, len(seq))]

    def shuffle(self, x):
        for i in reversed(range(1, len(x))):
            j = self.randint(0, i + 1)
            x[i], x[j] = x[j], x[i]


class Bucket(NamedTuple):
    desc: str
    weight: int
    value: int
    effective_value: int
    coins: List[dict]
    min_height: int
    witness: bool


class ScoredCandidate(NamedTuple):
    penalty: float
    tx: Transaction
    buckets: List[Bucket]


def strip_unneeded(bkts, sufficient_funds):
    """Remove buckets that are unnecessary in achieving the spend amount"""
    if sufficient_funds([], bucket_value_sum=0):
        return []
    bkts = sorted(bkts, key=(lambda bkt: bkt.value), reverse=True)
    bucket_value_sum = 0
    for i in range(len(bkts)):
        bucket_value_sum += bkts[i].value
        if sufficient_funds((bkts[:i + 1]), bucket_value_sum=bucket_value_sum):
            return bkts[:i + 1]

    raise Exception('keeping all buckets is still not enough')


class CoinChooserBase(Logger):
    enable_output_value_rounding = False

    def __init__(self):
        Logger.__init__(self)

    def keys(self, coins):
        raise NotImplementedError

    def bucketize_coins(self, coins, *, fee_estimator_vb):
        keys = self.keys(coins)
        buckets = defaultdict(list)
        for key, coin in zip(keys, coins):
            buckets[key].append(coin)

        constant_fee = fee_estimator_vb(2000) == fee_estimator_vb(200)

        def make_Bucket(desc, coins):
            witness = any((Transaction.is_segwit_input(coin, guess_for_address=True) for coin in coins))
            weight = sum((Transaction.estimated_input_weight(coin, witness) for coin in coins))
            value = sum((coin['value'] for coin in coins))
            min_height = min((coin['height'] for coin in coins))
            if constant_fee:
                effective_value = value
            else:
                fee = fee_estimator_vb(Decimal(weight) / 4)
                effective_value = value - fee
            return Bucket(desc=desc, weight=weight,
              value=value,
              effective_value=effective_value,
              coins=coins,
              min_height=min_height,
              witness=witness)

        return list(map(make_Bucket, buckets.keys(), buckets.values()))

    def penalty_func(self, base_tx, *, tx_from_buckets) -> Callable[([List[Bucket]], ScoredCandidate)]:
        raise NotImplementedError

    def _change_amounts(self, tx, count, fee_estimator_numchange) -> List[int]:
        output_amounts = [o.value for o in tx.outputs()]
        max_change = max(max(output_amounts) * 1.25, 0.02 * COIN)
        for n in range(1, count + 1):
            change_amount = max(0, tx.get_fee() - fee_estimator_numchange(n))
            if change_amount // n <= max_change:
                break

        def trailing_zeroes(val):
            s = str(val)
            return len(s) - len(s.rstrip('0'))

        zeroes = [trailing_zeroes(i) for i in output_amounts]
        min_zeroes = min(zeroes)
        max_zeroes = max(zeroes)
        if n > 1:
            zeroes = range(max(0, min_zeroes - 1), max_zeroes + 1 + 1)
        else:
            zeroes = [min_zeroes]
        remaining = change_amount
        amounts = []
        while n > 1:
            average = remaining / n
            amount = self.p.randint(int(average * 0.7), int(average * 1.3))
            precision = min(self.p.choice(zeroes), int(floor(log10(amount))))
            amount = int(round(amount, -precision))
            amounts.append(amount)
            remaining -= amount
            n -= 1

        max_dp_to_round_for_privacy = 2 if self.enable_output_value_rounding else 0
        N = int(pow(10, min(max_dp_to_round_for_privacy, zeroes[0])))
        amount = remaining // N * N
        amounts.append(amount)
        assert sum(amounts) <= change_amount
        return amounts

    def _change_outputs(self, tx, change_addrs, fee_estimator_numchange, dust_threshold):
        amounts = self._change_amounts(tx, len(change_addrs), fee_estimator_numchange)
        assert min(amounts) >= 0
        assert len(change_addrs) >= len(amounts)
        assert all([isinstance(amt, int) for amt in amounts])
        amounts = [amount for amount in amounts if amount >= dust_threshold]
        change = [TxOutput(TYPE_ADDRESS, addr, amount) for addr, amount in zip(change_addrs, amounts)]
        return change

    def _construct_tx_from_selected_buckets(self, *, buckets, base_tx, change_addrs, fee_estimator_w, dust_threshold, base_weight):
        tx = Transaction.from_io(base_tx.inputs()[:], base_tx.outputs()[:])
        tx.add_inputs([coin for b in buckets for coin in b.coins])
        tx_weight = self._get_tx_weight(buckets, base_weight=base_weight)
        if not change_addrs:
            change_addrs = [
             tx.inputs()[0]['address']]
            assert is_address(change_addrs[0])
        output_weight = 4 * Transaction.estimated_output_size(change_addrs[0])
        fee_estimator_numchange = lambda count: fee_estimator_w(tx_weight + count * output_weight)
        change = self._change_outputs(tx, change_addrs, fee_estimator_numchange, dust_threshold)
        tx.add_outputs(change)
        return (
         tx, change)

    def _get_tx_weight(self, buckets, *, base_weight) -> int:
        """Given a collection of buckets, return the total weight of the
        resulting transaction.
        base_weight is the weight of the tx that includes the fixed (non-change)
        outputs and potentially some fixed inputs. Note that the change outputs
        at this point are not yet known so they are NOT accounted for.
        """
        total_weight = base_weight + sum((bucket.weight for bucket in buckets))
        is_segwit_tx = any((bucket.witness for bucket in buckets))
        if is_segwit_tx:
            total_weight += 2
            num_legacy_inputs = sum(((not bucket.witness) * len(bucket.coins) for bucket in buckets))
            total_weight += num_legacy_inputs
        return total_weight

    def make_tx(self, coins, inputs, outputs, change_addrs, fee_estimator_vb, dust_threshold):
        """Select unspent coins to spend to pay outputs.  If the change is
        greater than dust_threshold (after adding the change output to
        the transaction) it is kept, otherwise none is sent and it is
        added to the transaction fee.

        `inputs` and `outputs` are guaranteed to be a subset of the
        inputs and outputs of the resulting transaction.
        `coins` are further UTXOs we can choose from.

        Note: fee_estimator_vb expects virtual bytes
        """
        utxos = [c['prevout_hash'] + str(c['prevout_n']) for c in coins]
        self.p = PRNG(''.join(sorted(utxos)))
        base_tx = Transaction.from_io(inputs[:], outputs[:])
        input_value = base_tx.input_value()
        base_weight = base_tx.estimated_weight()
        spent_amount = base_tx.output_value()

        def fee_estimator_w(weight):
            return fee_estimator_vb(Transaction.virtual_size_from_weight(weight))

        def sufficient_funds(buckets, *, bucket_value_sum):
            total_input = input_value + bucket_value_sum
            if total_input < spent_amount:
                return False
            total_weight = self._get_tx_weight(buckets, base_weight=base_weight)
            return total_input >= spent_amount + fee_estimator_w(total_weight)

        def tx_from_buckets(buckets):
            return self._construct_tx_from_selected_buckets(buckets=buckets, base_tx=base_tx,
              change_addrs=change_addrs,
              fee_estimator_w=fee_estimator_w,
              dust_threshold=dust_threshold,
              base_weight=base_weight)

        all_buckets = self.bucketize_coins(coins, fee_estimator_vb=fee_estimator_vb)
        all_buckets = list(filter(lambda b: b.effective_value > 0, all_buckets))
        scored_candidate = self.choose_buckets(all_buckets, sufficient_funds, self.penalty_func(base_tx, tx_from_buckets=tx_from_buckets))
        tx = scored_candidate.tx
        self.logger.info(f"using {len(tx.inputs())} inputs")
        self.logger.info(f"using buckets: {[bucket.desc for bucket in scored_candidate.buckets]}")
        return tx

    def choose_buckets(self, buckets, sufficient_funds, penalty_func: Callable[([List[Bucket]], ScoredCandidate)]) -> ScoredCandidate:
        raise NotImplemented('To be subclassed')


class CoinChooserRandom(CoinChooserBase):

    def bucket_candidates_any(self, buckets, sufficient_funds):
        """Returns a list of bucket sets."""
        if not buckets:
            raise NotEnoughFunds()
        candidates = set()
        for n, bucket in enumerate(buckets):
            if sufficient_funds([bucket], bucket_value_sum=(bucket.value)):
                candidates.add((n,))

        attempts = min(100, (len(buckets) - 1) * 10 + 1)
        permutation = list(range(len(buckets)))
        for i in range(attempts):
            self.p.shuffle(permutation)
            bkts = []
            bucket_value_sum = 0
            for count, index in enumerate(permutation):
                bucket = buckets[index]
                bkts.append(bucket)
                bucket_value_sum += bucket.value
                if sufficient_funds(bkts, bucket_value_sum=bucket_value_sum):
                    candidates.add(tuple(sorted(permutation[:count + 1])))
                    break
            else:
                raise NotEnoughFunds()

        candidates = [[buckets[n] for n in c] for c in candidates]
        return [strip_unneeded(c, sufficient_funds) for c in candidates]

    def bucket_candidates_prefer_confirmed(self, buckets, sufficient_funds):
        """Returns a list of bucket sets preferring confirmed coins.

        Any bucket can be:
        1. "confirmed" if it only contains confirmed coins; else
        2. "unconfirmed" if it does not contain coins with unconfirmed parents
        3. other: e.g. "unconfirmed parent" or "local"

        This method tries to only use buckets of type 1, and if the coins there
        are not enough, tries to use the next type but while also selecting
        all buckets of all previous types.
        """
        conf_buckets = [bkt for bkt in buckets if bkt.min_height > 0]
        unconf_buckets = [bkt for bkt in buckets if bkt.min_height == 0]
        other_buckets = [bkt for bkt in buckets if bkt.min_height < 0]
        bucket_sets = [
         conf_buckets, unconf_buckets, other_buckets]
        already_selected_buckets = []
        already_selected_buckets_value_sum = 0
        for bkts_choose_from in bucket_sets:
            try:

                def sfunds(bkts, *, bucket_value_sum):
                    bucket_value_sum += already_selected_buckets_value_sum
                    return sufficient_funds((already_selected_buckets + bkts), bucket_value_sum=bucket_value_sum)

                candidates = self.bucket_candidates_any(bkts_choose_from, sfunds)
                break
            except NotEnoughFunds:
                already_selected_buckets += bkts_choose_from
                already_selected_buckets_value_sum += sum((bucket.value for bucket in bkts_choose_from))

        else:
            raise NotEnoughFunds()

        candidates = [already_selected_buckets + c for c in candidates]
        return [strip_unneeded(c, sufficient_funds) for c in candidates]

    def choose_buckets(self, buckets, sufficient_funds, penalty_func):
        candidates = self.bucket_candidates_prefer_confirmed(buckets, sufficient_funds)
        scored_candidates = [penalty_func(cand) for cand in candidates]
        winner = min(scored_candidates, key=(lambda x: x.penalty))
        self.logger.info(f"Total number of buckets: {len(buckets)}")
        self.logger.info(f"Num candidates considered: {len(candidates)}. Winning penalty: {winner.penalty}")
        return winner


class CoinChooserPrivacy(CoinChooserRandom):
    __doc__ = "Attempts to better preserve user privacy.\n    First, if any coin is spent from a user address, all coins are.\n    Compared to spending from other addresses to make up an amount, this reduces\n    information leakage about sender holdings.  It also helps to\n    reduce blockchain UTXO bloat, and reduce future privacy loss that\n    would come from reusing that address' remaining UTXOs.\n    Second, it penalizes change that is quite different to the sent amount.\n    Third, it penalizes change that is too big.\n    "

    def keys(self, coins):
        return [coin['address'] for coin in coins]

    def penalty_func(self, base_tx, *, tx_from_buckets):
        min_change = min((o.value for o in base_tx.outputs())) * 0.75
        max_change = max((o.value for o in base_tx.outputs())) * 1.33

        def penalty(buckets):
            badness = len(buckets) - 1
            tx, change_outputs = tx_from_buckets(buckets)
            change = sum((o.value for o in change_outputs))
            if change == 0:
                pass
            elif change < min_change:
                badness += (min_change - change) / (min_change + 10000)
                if change < COIN / 1000:
                    badness += 1
            elif change > max_change:
                badness += (change - max_change) / (max_change + 10000)
                badness += change / (COIN * 5)
            return ScoredCandidate(badness, tx, buckets)

        return penalty


COIN_CHOOSERS = {'Privacy': CoinChooserPrivacy}

def get_name(config):
    kind = config.get('coin_chooser')
    if kind not in COIN_CHOOSERS:
        kind = 'Privacy'
    return kind


def get_coin_chooser(config):
    klass = COIN_CHOOSERS[get_name(config)]
    coinchooser = klass()
    coinchooser.enable_output_value_rounding = config.get('coin_chooser_output_rounding', False)
    return coinchooser