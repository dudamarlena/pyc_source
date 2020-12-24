# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastachar/fasta_logic.py
# Compiled at: 2020-02-27 14:36:42
# Size of source mod 2**32: 8052 bytes
from collections import UserList, defaultdict
import re

class Char(set):
    __doc__ = ' A character object representation a nucleotide in a sequence\n\n    The object is initialised with a character from the IUPAC list. Ambiguous characters, \n    such as Y and W are expanded into their base nucleotides.\n\n    Parameters\n    ----------\n    c : str \n         IUPAC character\n    subst_c : str\n         IUPAC character substitute for logical operations.\n\n    Attributes\n    ----------\n    _value : str\n        (non-expanded) character representation of nucleotide character.\n \n    Notes\n    -----\n    \n    The (IUPAC) characters supported are::\n\n        A\n        T\n        C\n        G\n        - (gap)\n\n    The ambiguous characters and their expansions::\n\n        Y -> C and T\n        R -> A and G\n        W -> A and T\n        S -> G and C\n        K -> T and G\n        M -> C and A\n\n        D -> A, G and T\n        V -> A, G and C\n        H -> A, C and T\n        B -> C, G and T\n\n    The masking characters X and N expand to A, G, T and G.\n    '
    IUPAC = {'A':'A',  'T':'T',  'C':'C',  'G':'G',  'Y':'CT',  'R':'AG',  'W':'AT',  'S':'GC', 
     'K':'TG',  'M':'CA',  'D':'AGT',  'V':'AGC',  'H':'ACT',  'B':'CGT',  'X':'ACTG', 
     'N':'ACTG',  '-':'-'}

    def __init__(self, c, masked):
        s = Char.IUPAC[c]
        super().__init__(s[0])
        for _s in s[1:]:
            self.add(_s)

        self._value = c
        self._masked = masked

    @property
    def is_masked(self):
        """ Evaluates to True if this character is a masked character."""
        return self._masked


class State(set):
    __doc__ = " The class' purpose is to hold a number of Char objects\n        and treat these as a set.\n\n    Parameters\n    ----------\n    chars : iterable of :obj: Char\n\n    Attributes\n    ----------\n    _value : list of str\n        ascii representation of characters.\n    "

    def __init__(self, chars):
        super().__init__()
        self._value = []
        self._chars = []
        for _char in chars:
            if not _char.is_masked:
                self.update(_char)
                self._value.append(_char._value)
            else:
                self._value.append(' ')

    def update(self, s):
        self._chars.append(s)
        super().update(s)

    def intersection_of_subsets(self):
        return (set.intersection)(*self._chars)

    def __repr__(self):
        m = '{} ({})'.format(super().__repr__(), ''.join(self._value))
        return m


class Sequence(UserList):
    __doc__ = ' A class to hold the information of a single sequence \n    \n    Parameters\n    ----------\n    ID : str\n        ID or lab code\n    species : str\n        species name\n    sequences_chars : str\n        ascii representation of the sequence\n\n    '
    PATTERNS = (re.compile('^[N]+'), re.compile('[N]+$'),
     re.compile('^[X]+'), re.compile('[X]+$'),
     re.compile('^[-]+'), re.compile('[-]+$'))

    def __init__(self, ID, species, sequence_chars):
        super().__init__()
        self.ID, self.species = ID, species
        self.sequence_chars = sequence_chars
        self.masked_positions = self.get_masked_positions(sequence_chars)
        for s, m in zip(sequence_chars, self.masked_positions):
            self.append(Char(s, m))

    def __repr__(self):
        return 'Sequence {}({}) {}'.format(self.species, self.ID, self.sequence_chars)

    def get_masked_positions(self, sequence_chars):
        """ Get masked positions

        Returns the positions where this sequences has a continuous block of N, X or - characters,
        either leading, or trailing.

        Parameters
        ----------
        sequence_chars : str
            string of sequence characters
        
        Returns
        -------
        m : list of int
            True where masked N appears.
        """
        m = [
         False] * len(sequence_chars)
        for p in Sequence.PATTERNS:
            match = p.search(sequence_chars)
            if match:
                for i in range(*match.span()):
                    m[i] = True

        return m


class SequenceLogic(object):
    __doc__ = ' Class for state comparison\n    '

    def mark_unit_length_states_within_set(self, aset):
        """ marks for each position whether this position has a unique character
        
        Parameters
        ----------
        aset : list of :obj: Char

        Returns
        -------
        list of tuple of (bool, :class:`State`)
            a list of tuples with first element True for unique character, and 
            second element the character(s) on this position of :class:`State`.
        """
        selection = []
        for j, c in enumerate(zip(*aset)):
            s = State(c)
            condition = len(s) == 1
            selection.append((condition, s))

        return selection

    def list_non_unique_characters_in_set(self, aset):
        """ 
        list non-unique characters in set.

        Parameters
        ----------
        aset: list of :class:`Char`
            list of sequences

        Returns
        -------
        list of tuple of (int, :class:`State`)
            Returns list of tuples of position and characters, for which more 
            than one different characters were found.
        """
        r = self.mark_unit_length_states_within_set(aset)
        return [(j, s) for j, (c, s) in enumerate(r) if not c]

    def list_unique_characters_in_set(self, aset):
        """ list where aset has unique characters

        Parameters
        ----------
        aset: list of :class:`Char`
            list of sequences

        Returns
        -------
        list of tuple of (int, :class:`State`)
            Returns list of tuples of position and characters, for which only 
            one characeter was found.
        """
        r = self.mark_unit_length_states_within_set(aset)
        return [(j, s) for j, (c, s) in enumerate(r) if c]

    def compute_mdcs(self, set_A, set_B, method='MDC'):
        """Computes molecular diagnostic characters
        
        Parameters
        ----------
        set_A: list of :class:`Char`
            list of sequences in list A
        set_B: list of :class:`Char`
            list of sequence in list B
        
        method: {"MDC", "potential_MDC_only"}
            method of comparison.

        Returns
        -------
        list of tuples of (int, :class:`State`, :class:`State`)
            Each tuple contains the position, its state for list A, and its state for list B
            sequences.

        
        This method computes molecular diagnostic characters by comparing the sequences in list 
        set_A and set_B. Two different criteria for comparison can be selected: return molecular 
        diagnostic characters, or only the potential modlecular diagnostic characters.

        Method determining the comparison method:
             * "MDC" returns Molecular Diagnostic Characters only
                conditions 1 and 2 are honoured
             * "potential_MDC_only" return MDCs only
                condition 2 is honoured, condition 1 is violated. 
        """
        if method not in 'MDC potential_MDC_only'.split():
            raise ValueError('Invalid method specified. Use either MDC or potential_MDC_only.')
        selection = []
        potential_CAs = self.mark_unit_length_states_within_set(set_A)
        for j, ((is_unique, state_a), b) in enumerate(zip(potential_CAs, zip(*set_B))):
            if method == 'MDC':
                if is_unique or method == 'potential_MDC_only':
                    state_b = is_unique or State(b)
            if state_a:
                if not state_b:
                    continue
                state_a.intersection(state_b) or selection.append((j, state_a, state_b))

        return selection