# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bridge_ai.py
# Compiled at: 2016-11-01 16:16:46
# Size of source mod 2**32: 36541 bytes
from bridge_util import *
point_vals = {12: 4, 11: 3, 10: 2, 9: 1}
dist_vals = {0: 3, 1: 2, 2: 1}
dum_dist_vals = {0: 5, 1: 3, 2: 1}
NT_bids = {1: (16, 18), 2: (22, 24), 3: (25, 27), 4: (28, 30), 
 5: (31, 32), 6: (33, 36), 7: (37, 40)}
NT_finals = {1: 19, 2: 23, 3: 26, 4: 30, 5: 33, 6: 33, 7: 37, 8: 41}
suit_bids = {1: 13, 2: 19, 3: 24, 4: 26, 5: 30, 6: 33, 7: 37, 8: 60}

class AI:

    def __init__(self):
        self.vul = [
         False, False]
        self.game_score = [0, 0]

    def show_game_score(self, game_score, rubber_score):
        self.game_score = game_score
        self.rub_score = rubber_score

    def show_rubber_score(self, rubber_score, vul):
        self.vul = vul
        self.rub_score = rubber_score
        self.game_score = [0, 0]

    def show_score(self, trick_score):
        pass

    def show_hand(self):
        pass

    def show_card(self, trick, card):
        if trick.cur_player != self.me:
            self.not_out.add(card)
            self.left[card.suit] -= 1
        if card.suit != trick.lead_suit:
            self.none[trick.lead_suit][trick.cur_player] = True
        if self.dummy is not None:
            self._find_none()

    def show_deal(self, hand, me, dealer):
        self.hand = hand
        self.not_out = set(hand)
        self.me = me
        if me < 2:
            self.partner = me + 2
        else:
            self.partner = me - 2
        self.dealer = dealer
        self.position = (me - dealer) % 4
        self.round = 0
        self.last_bid = [None] * 4
        self.n_bids = [0] * 4
        self.host = False
        self.chost = False
        self.opener = None
        self.hc_points = sum(v * len([c for c in hand if c.rank == i]) for i, v in point_vals.items())
        self.dist_points = sum(v * len([s for s in suit_real() if suit_count(hand, s) == i]) for i, v in dist_vals.items())
        self.dum_dist_points = sum(v * len([s for s in suit_real() if suit_count(hand, s) == i]) for i, v in dum_dist_vals.items())
        self.points = self.hc_points + self.dist_points
        self.dum_points = self.hc_points + self.dum_dist_points
        self.balanced = self.dist_points < 2
        self.suit_lengths = {s:suit_count(self.hand, s) for s in suit_real()}
        self.suit_lengths[Suit.NT] = 0
        self.eff_lengths = self.suit_lengths.copy()
        for s in suit_real():
            if max([c.rank for c in hand if c.suit is s], default=0) > 9:
                self.eff_lengths[s] += 0.5

        self.left = {s:13 - self.suit_lengths[s] for s in self.suit_lengths}
        self.none = dict()
        for s in suit_real():
            self.none[s] = [
             False] * 4

        self.none[Suit.NT] = [
         True] * 4
        self.bad = set(s for s in suit_real() if self.suit_lengths[s] < 3)
        self.max_len = max(self.suit_lengths.values())
        self.quickies = 0
        for s in suit_real():
            i = {c.rank for c in hand if c.suit is s}
            if {11, 12} <= i:
                self.quickies += 2
            else:
                if {
                 10, 12} <= i:
                    self.quickies += 1.5
                else:
                    if 12 in i or {10, 11} in i:
                        self.quickies += 1
                    elif 11 in i and len(i) > 1:
                        self.quickies += 0.5

        self.pjumped = False
        self.n = 0
        self.p = 0
        self.suit = Suit.NT
        self.shown = 0
        self.dec = None
        self.dummy = None
        self.dum_hand = set()
        self.lsuits = set()
        self.rsuits = set()
        self.psuits = set()

    def show_bid(self, who, bid):
        n = (who - self.me) % 4
        if bid is not Bids.Pass:
            self.last_bid[who] = bid
            if bid is not Bids.Double and bid is not Bids.Redouble:
                self.dec = who
                self.n_bids[who] += 1
                if self.opener is None and who in (self.me, self.partner):
                    self.opener = who
                    self.open = bid
                    if who == self.partner:
                        if bid.n == 1 and bid.suit is not Suit.NT:
                            self.quickies += 3
        elif bid.suit is Suit.NT:
            self.quickies += 4
        if who == self.partner and self.opener == self.me and self.n_bids[who] == 1:
            self.quickies += 1
        if n == 2:
            if bid.n > self.n + 1 or bid.n == self.n + 1 and bid.suit.value > self.suit.value:
                self.pjumped = True
            if bid.suit is not Suit.NT:
                self.bad.discard(bid.suit)
                self.psuits.add(bid.suit)
        else:
            if n == 1 and bid.suit is not Suit.NT:
                self.lsuits.add(bid.suit)
            else:
                if n == 3 and bid.suit is not Suit.NT:
                    self.rsuits.add(bid.suit)
                self.n, self.suit = bid.n, bid.suit
                self.chost = (who - self.me) % 2
            self.host = (who - self.me) % 2
        if (who + 1) % 4 == self.dealer:
            self.round += 1

    def ask_bid(self, con, last_bid):
        self.con = con
        if self.dec == self.me:
            return Bids.Pass
        else:
            if self.host and not con.doubled:
                q = self.quickies
                if self.suit_lengths[con.suit] > 3:
                    q += self.suit_lengths[con.suit] - 3
                if q > 9 - con.n:
                    pass
                return Bids.Double
            a = self._ask_bid()
            if self.host and a is Bids.Pass and self._is_rub(con, them=True) and not con.doubled:
                return Bids.Double
            if self.chost and self._is_neg_rub(con):
                return Bids.Pass
            return a

    def _cant_pass(self):
        return not self.chost and self._is_neg_rub(self.con)

    def _ask_bid(self):
        if self.chost and self.suit_lengths[self.con.suit] > 3:
            return Bids.Pass
        if self.round == 0:
            if self.n_bids[self.partner] == 0:
                return self._opening_bid()
                try:
                    return self._response(self.last_bid[self.partner])
                except ValueError:
                    return Bids.Pass

        if self.last_bid[self.me] is not None:
            if self.n_bids[self.partner] == 0:
                return self._open_again(self.last_bid[self.me])
            else:
                if self.n_bids[self.partner] == 1:
                    return self._rebid_opener(self.last_bid[self.me], self.last_bid[self.partner])
                if self.n_bids[self.me] == 1 and self.n_bids[self.partner] == 2:
                    return self._rebid_responder(self.open, self.last_bid[self.me], self.last_bid[self.partner])
                if self.n_bids[self.me] == 2 and self.n_bids[self.partner] == 2:
                    return self._third(self.last_bid[self.me], self.last_bid[self.partner])
                return self._rebid_extended(self.last_bid[self.me], self.last_bid[self.partner])
        else:
            if self.last_bid[self.partner] is not None:
                return self._response(self.last_bid[self.partner])
            else:
                return Bids.Pass

    def _choose_open_suit(self):
        for s in suit_real():
            if self.suit_lengths[s] == self.max_len:
                return s

    def _is_game(self, bid, them=False):
        if them:
            m = self.me % 2 - 1
        else:
            m = self.me % 2
        if bid is Bids.Pass:
            return False
        else:
            return val(bid) + self.game_score[m] >= 10

    def _is_rub(self, bid, them=False):
        if them:
            m = self.me % 2 - 1
        else:
            m = self.me % 2
        if bid is Bids.Pass or bid.n is None:
            return False
        else:
            bonus = 50 if self.vul[(m - 1)] else 70
            return self._is_game(bid, them=them) and self.vul[m] and self.game_score[m] + self.rub_score[m] + val(bid) + over_bonus(0, bid, True) + bonus > self.game_score[(m - 1)] + self.rub_score[(m - 1)]

    def _is_neg_rub(self, bid, them=False):
        if them:
            m = self.me % 2 - 1
        else:
            m = self.me % 2
        if bid is Bids.Pass or bid.n is None:
            return False
        else:
            bonus = 50 if self.vul[(m - 1)] else 70
            return self._is_game(bid, them=them) and self.vul[m] and self.game_score[m] + self.rub_score[m] + val(bid) + over_bonus(0, bid, True) + bonus < self.game_score[(m - 1)] + self.rub_score[(m - 1)]

    def _game(self, suit):
        amt = 10 - self.game_score[(self.me % 2)]
        if suit is Suit.NT:
            amt -= 1
        if suit in {Suit.Clubs, Suit.Diamonds}:
            return (amt + 1) // 2
        else:
            return (amt + 2) // 3

    def _opening_bid(self):
        if self.balanced:
            for l, p in NT_bids.items():
                if p[0] <= self.hc_points <= p[1]:
                    self.shown = p[0]
                    return self._validate(Bid(l, Suit.NT))

        if self._is_neg_rub(Bid(7, Suit.Spades)):
            cutoff = 50
        else:
            if self._is_neg_rub(Bid(6, Suit.Spades)):
                cutoff = 19
            else:
                if self._is_neg_rub(Bid(5, Suit.Spades)):
                    cutoff = 17
                else:
                    if self._is_neg_rub(Bid(4, Suit.Spades)):
                        cutoff = 15
                    else:
                        cutoff = 13
                    if self.points >= cutoff:
                        self.shown = cutoff
                        if self.max_len > 4:
                            s = self._choose_open_suit()
                            return self._validate(Bid(1, s), Bid(self.max_len - (4 if self.vul[(self.me % 2)] else 3), s))
                        else:
                            short = find_val(self.suit_lengths, min(self.suit_lengths.values()))
                            for s in suit_real(short.prev()):
                                if self.eff_lengths[s] > 4:
                                    try:
                                        return self._validate(Bid(1, s), None, safe=False)
                                    except ValueError:
                                        pass

                            return self._validate(Bid(1, Suit.Clubs))
                    else:
                        if self.points >= 10:
                            if self.max_len > 5:
                                self.shown = 10
                                s = self._choose_open_suit()
                                b = self._validate(Bid(2, s), Bid(self.max_len - (4 if self.vul[(self.me % 2)] else 3), s))
                                if not self._is_neg_rub(b):
                                    return b
                            else:
                                return Bids.Pass
                        else:
                            if self.max_len > 6:
                                s = self._choose_open_suit()
                                b = self._validate(Bid(self.max_len - (4 if self.vul[(self.me % 2)] else 3), s))
                                if not self._is_neg_rub(b):
                                    return b
                            else:
                                return Bids.Pass

    def _slam(self, suit):
        for m in range(1, 8):
            if not self._is_neg_rub(Bid(m, suit)):
                try:
                    return self._validate(Bid(m, suit), safe=False)
                except ValueError:
                    pass

    def _bid_NT(self, worst, best, to, pass_ok=False, final=False):
        if self._cant_pass():
            return self._slam(Suit.NT)
        else:
            if worst < 22 or self._game(Suit.NT) == 1 and (best < 33 or self._is_rub(Bid(1, Suit.NT))) and pass_ok:
                return self._validate(Bid(1, Suit.NT))
            if best < 26 or self._game(Suit.NT) == 1 and (best < 33 or self._is_rub(Bid(1, Suit.NT))):
                return self._validate(Bid(1, Suit.NT), Bid(2, Suit.NT))
            if worst < 26 or self._game(Suit.NT) == 2 and (best < 33 or self._is_rub(Bid(2, Suit.NT))):
                self.shown = 26 - to[1]
                return self._validate(Bid(2, Suit.NT))
            if best < 33 or self._is_rub(Bid(3, Suit.NT)) or final:
                self.shown = 26 - to[0]
                return self._validate(Bid(3, Suit.NT))
            if worst < 33 or self._is_rub(Bid(4, Suit.NT)):
                self.shown = 33 - to[1]
                return self._validate(Bid(4, Suit.NT))
            if self._is_rub(Bid(5, Suit.NT)):
                self.shown = 33 - to[1]
                return self._validate(Bid(5, Suit.NT))
            if worst < 37 or self._is_rub(Bid(6, Suit.NT)):
                self.shown = 33 - to[0]
                return self._validate(Bid(6, Suit.NT))
            self.shown = 37 - to[0]
            return self._validate(Bid(7, Suit.NT))

    def _show_suit(self, suit):
        for i in range(1, 8):
            try:
                return self._validate(Bid(i, suit), safe=False)
            except ValueError:
                pass

        return Bids.Pass

    def _jump_suit(self, suit):
        return self._show_suit(suit).plus_one()

    def _response(self, to):
        if not hasattr(to, 'suit'):
            return Bids.Pass
        if to.suit is Suit.NT:
            n = NT_bids[to.n]
            worst = n[0] + self.hc_points
            best = n[1] + self.hc_points
            if self.balanced:
                return self._bid_NT(worst, best, n, pass_ok=not self.chost)
            else:
                m = max(self.eff_lengths[Suit.Spades], self.eff_lengths[Suit.Hearts])
                if m > 4:
                    if self.eff_lengths[Suit.Spades] == m:
                        s = Suit.Spades
                    else:
                        s = Suit.Hearts
                    if m > 6:
                        return self._validate(Bid(4, s))
                    else:
                        if best < 26 and not self._cant_pass():
                            return Bids.Pass
                        if worst < 26 or best < 33 and self._game(s) < 3:
                            self.shown = 26 - n[1]
                            return self._validate(Bid(2, s))
                        if best < 33:
                            self.shown = 26 - n[0]
                            return self._validate(Bid(3, s))
                        if worst < 33:
                            self.shown = 33 - n[1]
                            return self._validate(Bid(5, s))
                        if worst < 37:
                            self.shown = 33 - n[0]
                            return self._validate(Bid(6, s))
                        self.shown = 37 - n[0]
                        return self._validate(Bid(7, s))
                elif self.max_len > 5 or self._cant_pass():
                    s = self._choose_open_suit()
                    return self._show_suit(s)
                return Bids.Pass
        else:
            if to.n > 1:
                return Bids.Pass
            if self.eff_lengths[to.suit] > 3:
                return self._bid_suit(to.suit, 13, self.dum_points)
            if self.balanced and self.hc_points >= 10:
                return self._bid_NT(self.hc_points + 13, self.hc_points + 16, (13,
                                                                               16))
            if self.points >= 10:
                s = self._choose_open_suit()
                if self.points >= 19:
                    self.shown = 19
                    return self._jump_suit(s)
                b = self._show_suit(s)
                if hasattr(b, 'n'):
                    if b.n > 1:
                        self.shown = 10
                    else:
                        self.shown = 6
                    return b
                elif self.points >= 6 or self._cant_pass():
                    for s in suit_fwd(to.suit):
                        if self.suit_lengths[s] >= 4:
                            self.shown = 6
                            try:
                                return self._validate(Bid(1, s), None, safe=False)
                            except ValueError:
                                pass

        if self.hc_points > 6:
            self.shown = 6
            return self._validate(Bid(1, Suit.NT))
        return Bids.Pass

    def _open_again(self, first):
        if not hasattr(first, 'suit') or first.suit is Suit.NT:
            return Bids.Pass
        else:
            return self._validate(Bid(self.suit_lengths[first.suit] - (4 if self.vul[(self.me % 2)] else 3), first.suit))

    def _rebid_opener(self, mine, his):
        if not hasattr(mine, 'suit'):
            return self._response(his)
        if not hasattr(his, 'suit'):
            return self._open_again(mine)
        if mine.suit is Suit.NT:
            if his.suit is Suit.NT:
                if self._cant_pass():
                    return self._NT_slam()
                if self.hc_points == NT_bids[mine.n][1]:
                    if not self._is_game(his):
                        self.shown = self.hc_points
                        return self._validate(Bid(3, Suit.NT))
                    else:
                        if his.n == 4:
                            self.shown = self.hc_points
                            return self._validate(Bid(6, Suit.NT))
                        return Bids.Pass
                else:
                    return Bids.Pass
            else:
                if his.suit in (Suit.Clubs, Suit.Diamonds) or his.n == 4:
                    if self._cant_pass():
                        return self._slam(his.suit)
                    else:
                        return Bids.Pass
                else:
                    if self.suit_lengths[his.suit] > 3:
                        if self._cant_pass():
                            return self._slam(his.suit)
                        else:
                            if his.n == 3 or his.n == 2 and self.points > 17:
                                self.shown = 18
                                return self._validate(Bid(self._game(his.suit), his.suit), Bid(4, his.suit))
                            if his.n < 4 and self._game(his.suit) < 4:
                                return self._validate(Bid(self._game(his.suit), his.suit))
                            if his.n == 5 and self.points >= NT_bids[mine.n][1]:
                                self.shown = NT_bids[mine.n][1]
                                return self._validate(Bid(6, his.suit))
                            return Bids.Pass
                    else:
                        return self._validate(Bid(his.n, Suit.NT))
        elif mine.n > 1:
            return self._validate(Bid(self.max_len - (4 if self.vul[(self.me % 2)] else 3), mine.suit))
        if mine.suit is his.suit:
            return self._bid_suit(his.suit, suit_bids[his.n] - self.shown, self.dum_points)
        if his.suit is Suit.NT:
            return self._bid_NT(self.hc_points + NT_finals[his.n] - 13, self.hc_points + NT_finals[(his.n + 1)] - 14, (
             NT_finals[his.n] - 13,
             NT_finals[(his.n + 1)] - 14), pass_ok=not self.chost)
        if self.pjumped:
            self.p = 19
        else:
            if his.n == 2:
                self.p = 10
            else:
                self.p = 6
            p = self.p
            if self.suit_lengths[his.suit] > 3:
                return self._bid_suit(his.suit, p, self.dum_points)
            else:
                if not self.bad:
                    n = self._bid_NT(p + self.hc_points, p + self.hc_points + 2, (p, p + 2))
                    if n is not Bids.Pass:
                        pass
                    return n
                if self.n != his.n or self.suit is not his.suit:
                    return Bids.Pass
                b = his.next_suit()
                while b.suit is not his.suit:
                    if self.suit_lengths[b.suit] > 4 or self.suit_lengths[b.suit] == 4 and b.suit is not mine.suit:
                        return b
                    b = b.next_suit()

                return Bids.Pass

    def _rebid_responder(self, hiso, mine, his):
        if not hasattr(his, 'suit'):
            return Bids.Pass
        if his.suit is Suit.NT:
            if mine.suit is Suit.NT:
                if self._cant_pass():
                    return self._slam(Suit.NT)
                if self.hc_points - self.shown >= 2:
                    self.shown = self.hc_points
                    if his.n == 2:
                        return self._validate(Bid(3, Suit.NT))
                    if his.n == 4:
                        pass
                    return self._validate(Bid(6, Suit.NT))
                return Bids.Pass
            else:
                return self._bid_NT(self.hc_points + NT_finals[his.n] - self.shown, self.hc_points + NT_finals[(his.n + 1)] - self.shown - 1, (
                 NT_finals[his.n] - self.shown,
                 NT_finals[(his.n + 1)] - self.shown - 1), pass_ok=not self.chost, final=True)
        else:
            if his.suit is mine.suit:
                return self._bid_suit(his.suit, suit_bids[his.n] - self.shown, self.dum_points, final=True)
            else:
                if self.suit_lengths[his.suit] >= 4 or self.suit_lengths[his.suit] == 3 and his.suit is hiso.suit:
                    if self.suit_lengths[his.suit] == 3:
                        d = self.dum_points - 1
                    else:
                        d = self.dum_points
                    return self._bid_suit(his.suit, 13, d)
                if not self.bad:
                    return self._bid_NT(13 + self.hc_points, 16 + self.hc_points, (13,
                                                                                   16), final=True)
                if self.suit_lengths[hiso.suit] == 3:
                    return self._bid_suit(hiso.suit, 13, self.dum_points - 1, m=hiso.n)
                if self.points >= 10:
                    if self.shown < 10:
                        self.shown = 10
                    return self._show_suit(mine.suit)
                if self.suit_lengths[hiso.suit] >= self.suit_lengths[his.suit]:
                    return self._validate(Bid(his.n, hiso.suit))
                if self._cant_pass():
                    return self._slam(his.suit)
                return Bids.Pass

    def _third(self, mine, his):
        if not hasattr(his, 'suit') or not hasattr(mine, 'suit') or not self._cant_pass() and (len(self.psuits) < 2 or mine.suit is his.suit):
            return Bids.Pass
        if not self.bad and self.suit_lengths[his.suit] < 4:
            return self._validate(Bid(his.n, Suit.NT))
        for s in list(self.psuits - {his.suit}):
            if self.suit_lengths[s] >= self.suit_lengths[his.suit]:
                return self._validate(Bid(his.n, s))

        if self.suit_lengths[mine.suit] > 5:
            return self._show_suit(mine.suit)
        if self.eff_lengths[his.suit] > 3:
            return self._bid_suit(his.suit, self.p, self.points, final=True)
        if self._cant_pass():
            return self._slam(his.suit)
        return Bids.Pass

    def _rebid_extended(self, mine, his):
        if self._cant_pass():
            return self._slam(his.suit)
        else:
            return Bids.Pass

    def _bid_suit(self, suit, his, points, m=1, no_pass=False, final=False):
        g = self._game(suit)
        if self._cant_pass():
            return self._slam(suit)
        for i in range(m, 8):
            if his + points < suit_bids[(i + 1)]:
                self.shown = suit_bids[i] - his
                return self._validate(Bid(i, suit))
            if (his + points < 31 or final) and i >= g or self._is_rub(Bid(i, suit)):
                self.shown = suit_bids[i] - his
                try:
                    return self._validate(Bid(i, suit), safe=False)
                except ValueError:
                    if not self.chost and not no_pass:
                        return Bids.Pass

        return Bids.Pass

    def _validate(self, desired, willing=None, safe=True):
        if outrank(desired, self.con, self.host):
            ans = desired
        else:
            if willing is not None and outrank(willing, self.con, self.host):
                ans = willing
            else:
                if safe:
                    return Bids.Pass
                raise ValueError
        return ans

    def _find_none(self):
        for s in suit_real():
            if self.left[s] == suit_count(self.dum_hand, s):
                for i in range(4):
                    if i != self.me and i != self.dummy and self.me != self.dummy:
                        self.none[s][i] = True

            if suit_count(self.dum_hand, s) == 0:
                self.none[s][self.dummy] = True

    def show_misdeal(self):
        pass

    def show_con(self, con, declarer):
        self.con = con
        self.role = (self.me - declarer) % 4
        self.dec = declarer
        self.trump = con.suit
        self.to_trump = self.role % 2 and self.suit_lengths[self.trump] < 4
        self.my_suit = None

    def show_dum(self, dum_hand, dummy):
        self.dummy = dummy
        self.dum_hand = dum_hand
        self._find_none()

    def show_trick(self, trick):
        if self.me != self.dec and trick.leader == self.partner and (self.my_suit is None or trick.lead_suit == self.trump) and suit_count(self.hand, trick.lead_suit):
            self.my_suit = trick.lead_suit
            self.short_suit = False
        if self.my_suit == self.trump and self.none[self.trump][(self.me - 3)] and self.none[self.trump][(self.me - 1)] and len(self.hand):
            self.my_suit, self.short_suit = self._choose_suit(False, False)

    def _discard(self, hand, lead_suit):
        try:
            return low_card_suit(hand, lead_suit)
        except ValueError:
            return low_card_hand(hand, self.trump)

    def _choose_suit(self, trump_ok, dum):
        if self.trump is Suit.NT:
            trump_ok = False
        if self.me == self.dec:
            lengths = {s:suit_count(self.hand, s) + suit_count(self.dum_hand, s) for s in suit_real()}
            if dum:
                loc_lengths = {s:suit_count(self.dum_hand, s) for s in suit_real()}
                hand = self.dum_hand
            else:
                loc_lengths = self.suit_lengths
                hand = self.hand
            if trump_ok and lengths[self.trump] > 6 and loc_lengths[self.trump]:
                return (self.trump, False)
            cutoff = 6
        else:
            loc_lengths = lengths = self.suit_lengths
            hand = self.hand
            if trump_ok and lengths[self.trump] > 4:
                return (self.trump, False)
            cutoff = 3
            for s in list(self.psuits) + list(self.lsuits - self.rsuits):
                if lengths[s]:
                    return (
                     s, False)

        try:
            gl = {s:lengths[s] for s in suit_real() if s is not self.trump and loc_lengths[s] and s not in self.rsuits - self.lsuits}
            max_len = max(gl.values())
            if max_len > (cutoff if trump_ok else 0):
                return (find_val(gl, max_len), False)
            else:
                gll = {s:loc_lengths[s] for s in suit_real() if s is not self.trump and loc_lengths[s] and s not in self.rsuits - self.lsuits}
                min_len = min(gll.values())
                if min_len < 3:
                    return (find_val(gll, min_len), True)
                high_cards = {s:high_card_suit(hand, s) for s in suit_real()}
                highest = max(high_cards[s] for s in suit_real() if s is not self.trump and high_cards[s] is not None)
                return (find_val(high_cards, highest), True)
        except ValueError:
            gl = {s:lengths[s] for s in suit_real() if loc_lengths[s]}
            max_len = max(gl.values())
            return (find_val(gl, max_len), False)

    def _find_higher(self, hand, to_beat):
        return min(c for c in hand if c.suit is to_beat.suit and c > to_beat)

    def _can_beat(self, hand, to_beat):
        in_suit = {c for c in hand if c.suit is to_beat.suit}
        if len(in_suit) > 0:
            return len([c for c in in_suit if c > to_beat]) > 0
        else:
            if len([c for c in hand if c.suit is self.trump]) > 0:
                return True
            return False

    def _try_overtrump(self, hand, top):
        try:
            if top.suit == self.trump:
                return self._find_higher(hand, top)
            else:
                return low_card_suit(hand, self.trump)
        except ValueError:
            pass

    def _n_higher(self, card):
        return 12 - card.rank - len([c for c in self.not_out if c.suit is card.suit and c > card])

    def ask(self, trick, who):
        pos = (who - trick.leader) % 4
        dum = who != self.me
        if dum:
            hand = self.dum_hand
        else:
            hand = self.hand
        ans = None
        if pos == 0:
            if not suit_count(hand, self.my_suit):
                trump_ok = not self.none[self.trump][(self.me - 3)] or not self.none[self.trump][(self.me - 1)]
                self.my_suit, self.short_suit = self._choose_suit(trump_ok, dum)
            if self.trump is Suit.NT:
                for s in suit_real():
                    if suit_count(hand, s) and self.none[s][(self.me - 1)] and self.none[s][(self.me - 3)]:
                        self.my_suit, self.short_suit = s, False
                        break

            ans = high_card_suit(hand, self.my_suit)
            if ans is None:
                print(self.my_suit)
            if not self.short_suit and (self.left[self.my_suit] > 5 or self._n_higher(ans)):
                ans = low_card_suit(hand, self.my_suit)
        elif pos == 1:
            if not suit_count(hand, trick.lead_suit) and self.to_trump and suit_count(hand, self.trump):
                ans = low_card_suit(hand, self.trump)
            else:
                try:
                    ans = high_card_suit(hand, trick.lead_suit)
                    if ans is None:
                        raise ValueError
                    if self.left[trick.lead_suit] > 5 or (self._can_beat(self.dum_hand, ans) if (self.dummy - self.me) % 4 == 1 else self._n_higher(ans)) or ans < trick.cards[trick.leader]:
                        ans = low_card_suit(hand, trick.lead_suit)
                except ValueError:
                    pass

        if pos == 2:
            win, top = winner(trick, self.trump)
            if win in {self.partner, self.me} and (self.none[trick.lead_suit][(who - 3)] or self._n_higher(top) == 0 or (self.dummy - self.me) % 4 == 1 and not self._can_beat(self.dum_hand, top)):
                ans = self._discard(hand, trick.lead_suit)
            else:
                try:
                    if (self.dummy - self.me) % 4 == 1:
                        ans = high_card_suit_b4d(hand, trick.lead_suit, self.dum_hand | set([top]))
                    else:
                        ans = high_card_suit(hand, trick.lead_suit)
                    if ans is None:
                        raise ValueError
                    if ans.rank < trick.cards[trick.leader].rank + 2 or ans < top or top.suit is not trick.lead_suit:
                        ans = low_card_suit(hand, trick.lead_suit)
                except ValueError:
                    ans = self._try_overtrump(hand, top)

        else:
            win, top = winner(trick, self.trump)
            if win in {self.partner, self.me}:
                ans = self._discard(hand, trick.lead_suit)
            else:
                try:
                    ans = low_card_suit(hand, trick.lead_suit)
                except ValueError:
                    ans = self._try_overtrump(hand, top)
                else:
                    if top.suit is trick.lead_suit:
                        pass
            try:
                ans = self._find_higher(hand, top)
            except ValueError:
                pass

            if ans is None:
                ans = low_card_hand(hand, self.trump)
            if not dum:
                self.suit_lengths[ans.suit] -= 1
            return ans