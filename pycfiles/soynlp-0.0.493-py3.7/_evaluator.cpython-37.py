# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/postagger/_evaluator.py
# Compiled at: 2018-10-01 03:38:35
# Size of source mod 2**32: 4611 bytes


class BaseEvaluator:

    def evaluate(self, candidate):
        return 0

    def select_best(self, candidates):
        if not candidates:
            return
        scored = [(c, self.evaluate(c)) for c in candidates]
        best = sorted(scored, key=(lambda x: -x[1]))[0][0]
        return best


class SimpleEojeolEvaluator(BaseEvaluator):

    def __init__(self, weights=None):
        if not weights:
            weights = (('num_nouns', -0.1), ('num_words', -0.15), ('has_noun', 0.2),
                       ('has_unknown', -0.3), ('is_adverb_repeat', 0.1), ('is_compound_noun', -0.05),
                       ('is_noun_josa', 0.1), ('is_a_noun', 0.2))
        self.weights = weights

    def evaluate(self, candidate):
        num_nouns = len([True for lr in candidate if lr.l_tag == 'Noun'])
        num_words = len(candidate)
        has_noun = num_nouns > 0
        has_unknown = len([True for lr in candidate if lr.l_tag is None])
        is_adverb_repeat = num_words > 1 and num_words == len([True for lr in candidate if lr.l_tag == 'Adverb'])
        is_compound_noun = num_words > 1 and num_words == len([True for lr in candidate if lr.l_tag == 'Noun'])
        is_noun_josa = num_words == 1 and candidate[0].l_tag == 'Noun' and candidate[0].r_tag == 'Josa'
        is_a_noun = num_words == 1 and candidate[0].l_tag == 'Noun' and not candidate[0].r
        score = num_nouns * self.weights[0][1] + num_words * self.weights[1][1] + has_noun * self.weights[2][1] + has_unknown * self.weights[3][1] + is_adverb_repeat * self.weights[4][1] + is_compound_noun * self.weights[5][1] + is_noun_josa * self.weights[6][1] + is_a_noun * self.weights[7][1]
        return score


class LREvaluator(BaseEvaluator):

    def __init__(self, weights=None, preference=None):
        """
        Arguments
        ---------
        preference: dict[str][str] = float
            Word preference. dict[tag][word] = preference_score
        """
        if not weights:
            weights = (('is_noun_phrase', 0.3), ('lr_are_known', 0.15), ('is_verb', 0.2),
                       ('is_adjective', 0.1), ('l_len', 0.1), ('r_len', 0.1), ('l_is_a_syllable', -0.2))
        self.weights = weights
        if not preference:
            preference = {}
        self.preference = preference

    def select_best(self, candidates):
        scored_candidates = [(c, self.evaluate(c)) for c in candidates]
        best = self._remove_overlapped(scored_candidates)
        return sorted(best, key=(lambda x: x[2]))

    def evaluate(self, candidate):
        is_noun_phrase = candidate.l_tag == 'Noun'
        lr_are_known = candidate.l_tag is not None and candidate.r_tag is not None
        is_verb = candidate.l_tag == 'Adverb'
        is_adjective = candidate.l_tag == 'Adjective'
        l_len = candidate.m - candidate.b
        r_len = candidate.e - candidate.m
        l_is_a_syllable = l_len == 1
        preference = 0
        if self.preference:
            preference += self.preference.get(candidate.l_tag, {}).get(candidate.l, 0)
            preference += self.preference.get(candidate.r_tag, {}).get(candidate.r, 0)
        score = is_noun_phrase * self.weights[0][1] + lr_are_known * self.weights[1][1] + is_verb * self.weights[2][1] + is_adjective * self.weights[3][1] + l_len * self.weights[4][1] + r_len * self.weights[5][1] + l_is_a_syllable * self.weights[6][1] + preference
        return score

    def _remove_overlapped(self, scored_candidates):
        best = []
        sorted_ = sorted(scored_candidates, key=(lambda x: -x[1]))
        while sorted_:
            best.append(sorted_.pop(0)[0])
            b, e = best[(-1)].b, best[(-1)].e
            removals = [i for i, (c, _) in enumerate(sorted_) if b < c.e if e > c.b]
            for idx in reversed(removals):
                del sorted_[idx]

        return sorted(best, key=(lambda x: x[2]))