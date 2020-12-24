# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/reedmuller/reedmuller.py
# Compiled at: 2018-05-19 10:57:57
"""reedmuller.py

Implementation of Reed-Muller codes for Python.
See the class ReedMuller for the documentation."""
import operator, itertools
from functools import reduce

def _binom(n, k):
    """Binomial coefficienct (n-k)!/k!."""
    return reduce(operator.mul, range(n - k + 1, n + 1)) // reduce(operator.mul, range(1, k + 1))


def _construct_vector(m, i):
    """Construct the vector for x_i of length 2^m, which has form:
    A string of 2^{m-i-1} 1s followed by 2^{m-i-1} 0s, repeated
    2^m / (2*2^{m-i-1}) = 2^{m-1}/2^{m-i-1} = 2^i times.
    NOTE: we must have 0 <= i < m."""
    return ([
     1] * 2 ** (m - i - 1) + [0] * 2 ** (m - i - 1)) * 2 ** i


def _vector_mult(*vecs):
    """For any number of length-n vectors, pairwise multiply the entries, e.g. for
    x = (x_0, ..., x_{n-1}), y = (y_0, ..., y_{n-1}),
    xy = (x_0y_0, x_1y_1, ..., x_{n-1}y{n-1})."""
    assert len(set(map(len, vecs))) == 1
    return list(map(lambda a: reduce(operator.mul, a, 1), list(zip(*vecs))))


def _vector_add(*vecs):
    """For any number of length-n vectors, pairwise add the entries, e.g. for
    x = (x_0, ..., x_{n-1}), y = (y_0, ..., y_{n-1}),
    xy = (x_0+y_0, x_1+y_1, ..., x_{n-1}+y{n-1})."""
    assert len(set(map(len, vecs))) == 1
    return list(map(lambda a: reduce(operator.add, a, 0), list(zip(*vecs))))


def _vector_neg(x):
    """Take the negation of a vector over Z_2, i.e. swap 1 and 0."""
    return list(map(lambda a: 1 - a, x))


def _vector_reduce(x, modulo):
    """Reduce each entry of a vector modulo the value supplied."""
    return list(map(lambda a: a % modulo, x))


def _dot_product(x, y):
    """Calculate the dot product of two vectors."""
    assert len(x) == len(y)
    return sum(_vector_mult(x, y))


def _generate_all_rows(m, S):
    """Generate all rows over the monomials in S, e.g. if S = {0,2}, we want to generate
    a list of four rows, namely:
    phi(x_0) * phi(x_2)
    phi(x_0) * !phi(x_2)
    !phi(x_0) * phi(x_2)
    !phi(x_0) * !phi(x_2).

    We do this using recursion on S."""
    if not S:
        return [[1] * 2 ** m]
    i, Srest = S[0], S[1:]
    Srest_rows = _generate_all_rows(m, Srest)
    xi_row = _construct_vector(m, i)
    not_xi_row = _vector_neg(xi_row)
    return [ _vector_mult(xi_row, row) for row in Srest_rows ] + [ _vector_mult(not_xi_row, row) for row in Srest_rows ]


class ReedMuller:
    """A class representing a Reed-Muller code RM(r,m), which encodes words of length:
    k = C(m,0) + C(m,1) + ... + C(m,r)
    to words of length n = 2^m.
    Note that C(m,0) + ... + C(m,m) = 2^m, so k <= n in all cases, as expected.
    The code RM(r,m) has weight 2^{m-r}, and thus, can correct up to 2^{m-r-1}-1 errors."""

    def __init__(self, r, m):
        """Create a Reed-Muller coder / decoder for RM(r,m)."""
        self.r, self.m = r, m
        self._construct_matrix()
        self.k = len(self.M[0])
        self.n = 2 ** m

    def strength(self):
        """Return the strength of the code, i.e. the number of errors we can correct."""
        return 2 ** (self.m - self.r - 1) - 1

    def message_length(self):
        """The length of a message to be encoded."""
        return self.k

    def block_length(self):
        """The length of a coded message."""
        return self.n

    def _construct_matrix(self):
        x_rows = [ _construct_vector(self.m, i) for i in range(self.m) ]
        self.matrix_by_row = [ reduce(_vector_mult, [ x_rows[i] for i in S ], [1] * 2 ** self.m) for s in range(self.r + 1) for S in itertools.combinations(range(self.m), s)
                             ]
        self.voting_rows = [ _generate_all_rows(self.m, [ i for i in range(self.m) if i not in S ]) for s in range(self.r + 1) for S in itertools.combinations(range(self.m), s)
                           ]
        self.row_indices_by_degree = [
         0]
        for degree in range(1, self.r + 1):
            self.row_indices_by_degree.append(self.row_indices_by_degree[(degree - 1)] + _binom(self.m, degree))

        self.M = list(zip(*self.matrix_by_row))

    def encode(self, word):
        """Encode a length-k vector to a length-n vector."""
        assert len(word) == self.k
        return [ _dot_product(word, col) % 2 for col in self.M ]

    def decode(self, eword):
        """Decode a length-n vector back to its original length-k vector using majority logic."""
        row = self.k - 1
        word = [-1] * self.k
        for degree in range(self.r, -1, -1):
            upper_r = self.row_indices_by_degree[degree]
            lower_r = 0 if degree == 0 else self.row_indices_by_degree[(degree - 1)] + 1
            for pos in range(lower_r, upper_r + 1):
                votes = [ _dot_product(eword, vrow) % 2 for vrow in self.voting_rows[pos] ]
                if votes.count(0) == votes.count(1):
                    return None
                word[pos] = 0 if votes.count(0) > votes.count(1) else 1

            s = [ _dot_product(word[lower_r:upper_r + 1], column[lower_r:upper_r + 1]) % 2 for column in self.M ]
            eword = _vector_reduce(_vector_add(eword, s), 2)

        return word

    def __repr__(self):
        return '<Reed-Muller code RM(%s,%s), strength=%s>' % (self.r, self.m, self.strength())


def _generate_all_vectors(n):
    """Generator to yield all possible length-n vectors in Z_2."""
    v = [
     0] * n
    while True:
        yield v
        v[n - 1] = v[(n - 1)] + 1
        pos = n - 1
        while pos >= 0 and v[pos] == 2:
            v[pos] = 0
            pos = pos - 1
            if pos >= 0:
                v[pos] += 1

        if v == [0] * n:
            break


def _characteristic_vector(n, S):
    """Return the characteristic vector of the subset S of an n-set."""
    return [ 0 if i not in S else 1 for i in range(n) ]


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: %s r m\n' % (sys.argv[0],))
        sys.exit(1)
    r, m = map(int, sys.argv[1:])
    if m <= r:
        sys.stderr.write('We require r > m.\n')
        sys.exit(2)
    rm = ReedMuller(r, m)
    strength = rm.strength()
    message_length = rm.message_length()
    block_length = rm.block_length()
    error_vectors = [ _characteristic_vector(block_length, S) for numerrors in range(strength + 1) for S in itertools.combinations(range(block_length), numerrors)
                    ]
    success = True
    for word in _generate_all_vectors(message_length):
        codeword = rm.encode(word)
        for error in error_vectors:
            error_codeword = _vector_reduce(_vector_add(codeword, error), 2)
            error_word = rm.decode(error_codeword)
            if error_word != word:
                print 'ERROR: encode(%s) => %s, decode(%s+%s=%s) => %s' % (word, codeword, codeword,
                 error, error_codeword, error_word)
                success = False

    if success:
        print 'RM(%s,%s): success.' % (r, m)