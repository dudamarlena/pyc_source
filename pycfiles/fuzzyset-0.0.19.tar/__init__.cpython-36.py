# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/share/AxiakDocs/fuzzyset/fuzzyset/__init__.py
# Compiled at: 2019-03-05 15:06:46
# Size of source mod 2**32: 4295 bytes
import re, math, operator, collections, Levenshtein
__version__ = (0, 0, 18)
_non_word_re = re.compile('[^\\w, ]+')
__all__ = ('FuzzySet', )

class FuzzySet(object):
    __doc__ = ' Fuzzily match a string '

    def __init__(self, iterable=(), gram_size_lower=2, gram_size_upper=3, use_levenshtein=True, rel_sim_cutoff=1):
        self.exact_set = {}
        self.match_dict = collections.defaultdict(list)
        self.items = {}
        self.use_levenshtein = use_levenshtein
        self.gram_size_lower = gram_size_lower
        self.gram_size_upper = gram_size_upper
        self.rel_sim_cutoff = rel_sim_cutoff
        for i in range(gram_size_lower, gram_size_upper + 1):
            self.items[i] = []

        for value in iterable:
            self.add(value)

    def add(self, value):
        lvalue = value.lower()
        if lvalue in self.exact_set:
            return False
        for i in range(self.gram_size_lower, self.gram_size_upper + 1):
            self._FuzzySet__add(value, i)

    def __add(self, value, gram_size):
        lvalue = value.lower()
        items = self.items[gram_size]
        idx = len(items)
        items.append(0)
        grams = _gram_counter(lvalue, gram_size)
        norm = math.sqrt(sum(x ** 2 for x in grams.values()))
        for gram, occ in grams.items():
            self.match_dict[gram].append((idx, occ))

        items[idx] = (
         norm, lvalue)
        self.exact_set[lvalue] = value

    def __getitem__(self, value):
        lvalue = value.lower()
        result = self.exact_set.get(lvalue)
        if result:
            if self.rel_sim_cutoff >= 1:
                return [
                 (
                  1, result)]
        for i in range(self.gram_size_upper, self.gram_size_lower - 1, -1):
            results = self._FuzzySet__get(value, i)
            if results is not None:
                return results

        raise KeyError(value)

    def __get(self, value, gram_size):
        lvalue = value.lower()
        matches = collections.defaultdict(float)
        grams = _gram_counter(lvalue, gram_size)
        items = self.items[gram_size]
        norm = math.sqrt(sum(x ** 2 for x in grams.values()))
        for gram, occ in grams.items():
            for idx, other_occ in self.match_dict.get(gram, ()):
                matches[idx] += occ * other_occ

        if not matches:
            return
        else:
            results = [(match_score / (norm * items[idx][0]), items[idx][1]) for idx, match_score in matches.items()]
            results.sort(reverse=True, key=(operator.itemgetter(0)))
            if self.use_levenshtein:
                results = [(_distance(matched, lvalue), matched) for _, matched in results[:50]]
                results.sort(reverse=True, key=(operator.itemgetter(0)))
            score_threshold = results[0][0] * min(1.0, self.rel_sim_cutoff)
            return [(score, self.exact_set[lval]) for score, lval in results if score >= score_threshold]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __nonzero__(self):
        return bool(self.exact_set)

    def __len__(self):
        return len(self.exact_set)


def _distance(str1, str2):
    distance = Levenshtein.distance(str1, str2)
    if len(str1) > len(str2):
        return 1 - float(distance) / len(str1)
    else:
        return 1 - float(distance) / len(str2)


def _gram_counter(value, gram_size=2):
    result = collections.defaultdict(int)
    for value in _iterate_grams(value, gram_size):
        result[value] += 1

    return result


def _iterate_grams(value, gram_size=2):
    simplified = '-' + _non_word_re.sub('', value.lower()) + '-'
    len_diff = gram_size - len(simplified)
    if len_diff > 0:
        simplified += '-' * len_diff
    for i in range(len(simplified) - gram_size + 1):
        yield simplified[i:i + gram_size]


def _other_test():
    with open('./origin_cities') as (cities):
        for line in cities:
            result = f.get(line.strip())
            if result is None:
                print('{}: Could not find'.format(line.strip()))
            else:
                if isinstance(result, list):
                    print('{}: {}'.format(line.strip(), result))


if __name__ == '__main__':
    pass