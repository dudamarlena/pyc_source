# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pypeerassets/voting.py
# Compiled at: 2018-10-29 16:32:13
# Size of source mod 2**32: 18480 bytes
from typing import Iterable, Generator, List, Optional, Callable, cast
from enum import Enum
from decimal import Decimal
from hashlib import sha256
from operator import itemgetter
from pypeerassets.kutil import Kutil
from pypeerassets.protocol import Deck
from pypeerassets.provider import Provider
from pypeerassets.pavoteproto_pb2 import Vote as pavoteproto
from pypeerassets.protocol import DeckState
from pypeerassets.pautils import read_tx_opreturn, find_tx_sender, tx_serialization_order
from pypeerassets.networks import net_query
from pypeerassets.exceptions import OverSizeOPReturn, InvalidVoteVersion, InvalidVoteEndBlock, EmptyP2THDirectory
from pypeerassets.transactions import tx_output, p2pkh_script, nulldata_script, Transaction, make_raw_transaction, Locktime

class CountMode(Enum):
    NONE = 0
    SIMPLE = 1
    WEIGHT_CARD_BALANCE = 3
    WEIGHT_CARD_DAYS = 7


def deck_vote_tag(deck: Deck) -> Kutil:
    """deck vote tag address"""
    if deck.id is None:
        raise Exception('deck.id is required')
    return Kutil(network=(deck.network), privkey=(sha256(bytearray.fromhex(deck.id) + 'vote_init'.encode()).digest()))


class VoteInit:

    def __init__(self, version: int, description: str, count_mode: int, start_block: int, end_block: int, deck: Deck, choices: List[str]=(), vote_metainfo: str='', id: str=None, sender: str=None, tx_confirmations=None) -> None:
        """initialize vote object"""
        self.version = version
        self.description = description
        self.choices = choices
        self.count_mode = count_mode
        self.start_block = start_block
        self.end_block = end_block
        self.id = id
        self.vote_metainfo = vote_metainfo
        self.sender = sender
        self.tx_confirmations = tx_confirmations
        self.deck = deck

    @property
    def p2th_address(self) -> Optional[str]:
        """P2TH address for the deck vote"""
        if self.deck.id:
            return deck_vote_tag(self.deck).address
        else:
            return

    @property
    def p2th_wif(self) -> Optional[str]:
        """P2TH privkey in WIF format"""
        if self.id:
            return deck_vote_tag(self.deck).wif
        else:
            return

    def metainfo_to_protobuf(self) -> bytes:
        """encode vote into protobuf"""
        vote = pavoteproto()
        vote.version = self.version
        vote.description = self.description
        vote.count_mode = self.count_mode
        vote.start_block = self.start_block
        vote.end_block = self.end_block
        vote.choices.extend(self.choices)
        if not isinstance(self.vote_metainfo, bytes):
            vote.vote_metainfo = self.vote_metainfo.encode()
        else:
            vote.vote_metainfo = self.vote_metainfo
        if vote.ByteSize() > net_query(self.deck.network).op_return_max_bytes:
            raise OverSizeOPReturn('\n                        Metainfo size exceeds maximum of {max} bytes supported by this network.'.format(max=(net_query(self.deck.network).op_return_max_bytes)))
        return vote.SerializeToString()

    def metainfo_to_dict(self) -> dict:
        """vote info as dict"""
        r = {'version':self.version, 
         'count_mode':self.count_mode, 
         'start_block':self.start_block, 
         'end_block':self.end_block, 
         'choices':self.choices, 
         'choice_address':self.vote_choice_address, 
         'description':self.description}
        if self.vote_metainfo:
            r.update({'vote_metainfo': self.vote_metainfo})
        return r

    @property
    def vote_choice_address(self) -> List[str]:
        """calculate the addresses on which the vote is casted."""
        if self.id is None:
            raise Exception('vote id is required')
        addresses = []
        for choice in self.choices:
            addresses.append(Kutil(network=(self.deck.network), privkey=(sha256(bytearray.fromhex(self.id) + bytearray(self.choices.index(choice))).digest())).address)

        return addresses

    def to_json(self) -> dict:
        """export the VoteInit object to json-ready format"""
        d = self.__dict__
        d['p2th_address'] = self.p2th_address
        d['p2th_wif'] = self.p2th_wif
        d['vote_choice_address'] = self.vote_choice_address
        d['deck'] = self.deck.to_json()
        return d

    @classmethod
    def from_json(cls, json: dict):
        """load the VoteInit object from json"""
        return cls(version=json['version'], 
         description=json['description'], 
         choices=json['choices'], 
         count_mode=json['count_mode'], 
         start_block=json['start_block'], 
         end_block=json['end_block'], 
         id=json['id'], 
         vote_metainfo=json['vote_metainfo'], 
         sender=json['sender'], 
         deck=Deck.from_json(json['deck']))

    def __str__(self) -> str:
        r = []
        for key in self.__dict__:
            r.append("{key}='{value}'".format(key=key, value=(self.__dict__[key])))

        return ', '.join(r)


def parse_vote_init(protobuf: bytes) -> dict:
    """decode vote init tx op_return protobuf message and validate it."""
    vote = pavoteproto()
    vote.ParseFromString(protobuf)
    if not vote.version > 0:
        raise InvalidVoteVersion({'error': "Vote info incomplete, version can't be 0."})
    if vote.start_block > vote.end_block:
        raise InvalidVoteEndBlock({'error': "vote can't end in the past."})
    return {'version':vote.version, 
     'description':vote.description, 
     'count_mode':vote.MODE.Name(vote.count_mode), 
     'choices':vote.choices, 
     'start_block':vote.start_block, 
     'end_block':vote.end_block, 
     'vote_metainfo':vote.vote_metainfo}


def vote_init(vote_init: VoteInit, inputs: dict, change_address: str, locktime: int=0) -> Transaction:
    """initialize vote transaction, must be signed by the deck_issuer privkey"""
    print(vote_init.deck)
    network_params = net_query(vote_init.deck.network)
    p2th = vote_init.p2th_address
    change_sum = Decimal(inputs['total'] - network_params.min_tx_fee - Decimal(0.01))
    txouts = [
     tx_output(network=(vote_init.deck.network), value=(Decimal(0.01)), n=0,
       script=p2pkh_script(address=p2th, network=(vote_init.deck.network))),
     tx_output(network=(vote_init.deck.network), value=(Decimal(0)), n=1,
       script=(nulldata_script(vote_init.metainfo_to_protobuf()))),
     tx_output(network=(vote_init.deck.network), value=change_sum, n=2,
       script=p2pkh_script(address=change_address, network=(vote_init.deck.network)))]
    unsigned_tx = make_raw_transaction(network=(vote_init.deck.network), inputs=(inputs['utxos']),
      outputs=txouts,
      locktime=(Locktime(locktime)))
    return unsigned_tx


def find_vote_inits(provider: Provider, deck: Deck) -> Iterable[VoteInit]:
    """find vote_inits on this deck"""
    vote_ints = provider.listtransactions(deck_vote_tag(deck).address)
    for txid in vote_ints:
        try:
            raw_vote = provider.getrawtransaction(txid, 1)
            vote = parse_vote_init(read_tx_opreturn(raw_vote['vout'][1]))
            vote['id'] = txid
            vote['sender'] = find_tx_sender(provider, raw_vote)
            vote['tx_confirmations'] = raw_vote['confirmations']
            vote['deck'] = deck.to_json()
            yield VoteInit.from_json(vote)
        except (InvalidVoteVersion,
         InvalidVoteEndBlock) as e:
            pass


def vote_cast(vote: VoteInit, choice_index: int, inputs: dict, change_address: str, locktime: int=0) -> Transaction:
    """vote cast transaction"""
    network_params = net_query(vote.deck.network)
    p2th = vote.vote_choice_address[choice_index]
    change_sum = Decimal(inputs['total'] - network_params.min_tx_fee - Decimal(0.01))
    txouts = [
     tx_output(network=(vote.deck.network), value=(Decimal(0.01)), n=0,
       script=p2pkh_script(address=p2th, network=(vote.deck.network))),
     tx_output(network=(vote.deck.network), value=change_sum, n=1,
       script=p2pkh_script(address=change_address, network=(vote.deck.network)))]
    unsigned_tx = make_raw_transaction(network=(vote.deck.network), inputs=(inputs['utxos']),
      outputs=txouts,
      locktime=(Locktime(locktime)))
    return unsigned_tx


class Vote:
    """Vote"""

    def __init__(self, vote_init: VoteInit, id: str, blocknum: int, blockseq: int, confirmations: int, timestamp: int, sender: str=None) -> None:
        self.vote_init = vote_init
        self.sender = sender
        self.id = id
        self.blocknum = blocknum
        self.blockseq = blockseq
        self.confirmations = confirmations
        self.timestamp = timestamp

    @property
    def is_valid(self) -> bool:
        """check if VoteCast is valid"""
        if not (self.blocknum >= self.vote_init.start_block and self.blocknum <= self.vote_init.end_block):
            return False
        else:
            return True

    def to_json(self) -> dict:
        """export the Vote object to json-ready format"""
        d = self.__dict__
        d['is_valid'] = self.is_valid
        return d

    @property
    def uid(self):
        return self.id + str(self.blocknum) + str(self.blockseq)

    def __str__(self) -> str:
        r = []
        for key in self.__dict__:
            r.append("{key}='{value}'".format(key=key, value=(self.__dict__[key])))

        return ', '.join(r)


def find_vote_casts(provider: Provider, vote_init: VoteInit, choice_index: int) -> Iterable[Vote]:
    """find and verify vote_casts on this vote_choice_address"""
    vote_casts = provider.listtransactions(vote_init.vote_choice_address[choice_index])
    if vote_casts is None:
        return
    for tx in vote_casts:
        raw_tx = provider.getrawtransaction(tx, 1)
        sender = find_tx_sender(provider, raw_tx)
        confirmations = raw_tx['confirmations']
        blocknum = provider.getblock(raw_tx['blockhash'])['height']
        blockseq = tx_serialization_order(provider, raw_tx['blockhash'], raw_tx['txid'])
        yield Vote(vote_init=vote_init, id=(raw_tx['txid']),
          sender=sender,
          blocknum=blocknum,
          blockseq=blockseq,
          confirmations=confirmations,
          timestamp=(raw_tx['blocktime']))


class VoteState:
    """VoteState"""

    def __init__(self, provider: Provider, vote_init: VoteInit, deck_state: DeckState) -> None:
        self.provider = provider
        self.vote_init = vote_init
        self.deck_state = deck_state
        self.balances = deck_state.balances
        self.count_mode = vote_init.count_mode

    def _sort_votes(self, votes: Generator) -> list:
        """sort votes by blocknum and blockseq"""
        return sorted([v.to_json() for v in votes], key=(itemgetter('blocknum', 'blockseq')))

    def _validate_against_count_mode(self, votes: list) -> list:
        """validate votes against vote_init count mode"""
        supported_mask = 7
        if not bool(self.count_mode & supported_mask):
            return []
        else:
            parser_fn = self.parsers[CountMode(self.count_mode).name]
            parsed_votes = parser_fn(votes=(self._sort_votes(votes)))
            return parsed_votes

    def _none_vote_parser(self, votes: list) -> None:
        """
        parser for NONE [0] count method
        """
        pass

    def _simple_vote_parser(self, votes: dict) -> list:
        """
        parser for SIMPLE [1] count method
        https://github.com/PeerAssets/peerassets-rfcs/blob/master/0005-on-chain-voting-protocol-proposal.md#simple-vote-counting
        """
        v = votes[0]
        if v['sender'] not in self.balances.keys():
            return []
        else:
            return v

    def _weight_card_balance_vote_parser(self, votes: list) -> list:
        raise NotImplementedError

    def _weight_card_days_vote_parser(self, votes: list):
        raise NotImplementedError

    parsers = {'NONE':_none_vote_parser, 
     'SIMPLE':_simple_vote_parser, 
     'WEIGHT_CARD_BALANCE':_weight_card_balance_vote_parser, 
     'WEIGHT_CARD_DAYS':_weight_card_days_vote_parser}

    def all_vote_casts(self) -> dict:
        """find all the votes related to this vote_init"""
        choices = self.vote_init.choices
        return {choices.index(c):find_vote_casts(self.provider, self.vote_init, choices.index(c)) for c in choices}

    def all_valid_vote_casts(self) -> dict:
        """filter out the invalid votes"""
        return {k:(i for i in v if i.is_valid) for k, v in self.all_vote_casts().items()}

    def __len__(self) -> int:
        """count the valid votes"""
        return sum([len(list(v)) for v in self.all_vote_casts().values()])

    def calculate_state(self) -> dict:
        """do the final calculation"""
        all_votes = self.all_valid_vote_casts()
        return {k:self._validate_against_count_mode(v) for k, v in all_votes.items()}