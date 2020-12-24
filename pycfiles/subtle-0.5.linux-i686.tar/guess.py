# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/guess.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import UnicodeMixin, s, u, base_text_type
from guessit.language import Language
from guessit.country import Country
import json, datetime, logging
log = logging.getLogger(__name__)

class Guess(UnicodeMixin, dict):
    """A Guess is a dictionary which has an associated confidence for each of
    its values.

    As it is a subclass of dict, you can use it everywhere you expect a
    simple dict."""

    def __init__(self, *args, **kwargs):
        try:
            confidence = kwargs.pop(b'confidence')
        except KeyError:
            confidence = 0

        dict.__init__(self, *args, **kwargs)
        self._confidence = {}
        for prop in self:
            self._confidence[prop] = confidence

    def to_dict(self):
        data = dict(self)
        for prop, value in data.items():
            if isinstance(value, datetime.date):
                data[prop] = value.isoformat()
            elif isinstance(value, (Language, Country, base_text_type)):
                data[prop] = u(value)
            elif isinstance(value, list):
                data[prop] = [ u(x) for x in value ]

        return data

    def nice_string(self):
        data = self.to_dict()
        parts = json.dumps(data, indent=4).split(b'\n')
        for i, p in enumerate(parts):
            if p[:5] != b'    "':
                continue
            prop = p.split(b'"')[1]
            parts[i] = b'    [%.2f] "' % self.confidence(prop) + p[5:]

        return (b'\n').join(parts)

    def __unicode__(self):
        return u(self.to_dict())

    def confidence(self, prop):
        return self._confidence.get(prop, -1)

    def set(self, prop, value, confidence=None):
        self[prop] = value
        if confidence is not None:
            self._confidence[prop] = confidence
        return

    def set_confidence(self, prop, value):
        self._confidence[prop] = value

    def update(self, other, confidence=None):
        dict.update(self, other)
        if isinstance(other, Guess):
            for prop in other:
                self._confidence[prop] = other.confidence(prop)

        if confidence is not None:
            for prop in other:
                self._confidence[prop] = confidence

        return

    def update_highest_confidence(self, other):
        """Update this guess with the values from the given one. In case
        there is property present in both, only the one with the highest one
        is kept."""
        if not isinstance(other, Guess):
            raise ValueError(b'Can only call this function on Guess instances')
        for prop in other:
            if prop in self and self.confidence(prop) >= other.confidence(prop):
                continue
            self[prop] = other[prop]
            self._confidence[prop] = other.confidence(prop)


def choose_int(g1, g2):
    """Function used by merge_similar_guesses to choose between 2 possible
    properties when they are integers."""
    v1, c1 = g1
    v2, c2 = g2
    if v1 == v2:
        return (v1, 1 - (1 - c1) * (1 - c2))
    else:
        if c1 > c2:
            return (v1, c1 - c2)
        return (v2, c2 - c1)


def choose_string(g1, g2):
    """Function used by merge_similar_guesses to choose between 2 possible
    properties when they are strings.

    If the 2 strings are similar, or one is contained in the other, the latter is returned
    with an increased confidence.

    If the 2 strings are dissimilar, the one with the higher confidence is returned, with
    a weaker confidence.

    Note that here, 'similar' means that 2 strings are either equal, or that they
    differ very little, such as one string being the other one with the 'the' word
    prepended to it.

    >>> s(choose_string(('Hello', 0.75), ('World', 0.5)))
    ('Hello', 0.25)

    >>> s(choose_string(('Hello', 0.5), ('hello', 0.5)))
    ('Hello', 0.75)

    >>> s(choose_string(('Hello', 0.4), ('Hello World', 0.4)))
    ('Hello', 0.64)

    >>> s(choose_string(('simpsons', 0.5), ('The Simpsons', 0.5)))
    ('The Simpsons', 0.75)

    """
    v1, c1 = g1
    v2, c2 = g2
    if not v1:
        return g2
    else:
        if not v2:
            return g1
        v1, v2 = v1.strip(), v2.strip()
        v1l, v2l = v1.lower(), v2.lower()
        combined_prob = 1 - (1 - c1) * (1 - c2)
        if v1l == v2l:
            return (v1, combined_prob)
        if v1l == b'the ' + v2l:
            return (v1, combined_prob)
        if v2l == b'the ' + v1l:
            return (v2, combined_prob)
        if v2l in v1l:
            return (v2, combined_prob)
        if v1l in v2l:
            return (v1, combined_prob)
        if c1 > c2:
            return (v1, c1 - c2)
        return (v2, c2 - c1)


def _merge_similar_guesses_nocheck(guesses, prop, choose):
    """Take a list of guesses and merge those which have the same properties,
    increasing or decreasing the confidence depending on whether their values
    are similar.

    This function assumes there are at least 2 valid guesses."""
    similar = [ guess for guess in guesses if prop in guess ]
    g1, g2 = similar[0], similar[1]
    other_props = set(g1) & set(g2) - set([prop])
    if other_props:
        log.debug(b'guess 1: %s' % g1)
        log.debug(b'guess 2: %s' % g2)
        for prop in other_props:
            if g1[prop] != g2[prop]:
                log.warning(b'both guesses to be merged have more than one different property in common, bailing out...')
                return

    v1, v2 = g1[prop], g2[prop]
    c1, c2 = g1.confidence(prop), g2.confidence(prop)
    new_value, new_confidence = choose((v1, c1), (v2, c2))
    if new_confidence >= c1:
        msg = b"Updating matching property '%s' with confidence %.2f"
    else:
        msg = b"Updating non-matching property '%s' with confidence %.2f"
    log.debug(msg % (prop, new_confidence))
    g2[prop] = new_value
    g2.set_confidence(prop, new_confidence)
    g1.update(g2)
    guesses.remove(g2)


def merge_similar_guesses(guesses, prop, choose):
    """Take a list of guesses and merge those which have the same properties,
    increasing or decreasing the confidence depending on whether their values
    are similar."""
    similar = [ guess for guess in guesses if prop in guess ]
    if len(similar) < 2:
        return
    if len(similar) == 2:
        _merge_similar_guesses_nocheck(guesses, prop, choose)
    if len(similar) > 2:
        log.debug(b'complex merge, trying our best...')
        before = len(guesses)
        _merge_similar_guesses_nocheck(guesses, prop, choose)
        after = len(guesses)
        if after < before:
            merge_similar_guesses(guesses, prop, choose)


def merge_all(guesses, append=None):
    """Merge all the guesses in a single result, remove very unlikely values,
    and return it.
    You can specify a list of properties that should be appended into a list
    instead of being merged.

    >>> s(merge_all([ Guess({'season': 2}, confidence=0.6),
    ...               Guess({'episodeNumber': 13}, confidence=0.8) ]))
    {'season': 2, 'episodeNumber': 13}

    >>> s(merge_all([ Guess({'episodeNumber': 27}, confidence=0.02),
    ...               Guess({'season': 1}, confidence=0.2) ]))
    {'season': 1}

    >>> s(merge_all([ Guess({'other': 'PROPER'}, confidence=0.8),
    ...               Guess({'releaseGroup': '2HD'}, confidence=0.8) ],
    ...             append=['other']))
    {'releaseGroup': '2HD', 'other': ['PROPER']}

    """
    if not guesses:
        return Guess()
    else:
        result = guesses[0]
        if append is None:
            append = []
        for g in guesses[1:]:
            for prop in append:
                if prop in g:
                    result.set(prop, result.get(prop, []) + [g[prop]], confidence=g.confidence(prop))
                    del g[prop]

            dups = set(result) & set(g)
            if dups:
                log.warning(b'duplicate properties %s in merged result...' % dups)
            result.update_highest_confidence(g)

        for p in list(result.keys()):
            if result.confidence(p) < 0.05:
                del result[p]

        for prop in append:
            try:
                value = result[prop]
                if isinstance(value, list):
                    result[prop] = list(set(value))
                else:
                    result[prop] = [
                     value]
            except KeyError:
                pass

        return result