# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/highlight.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = 'The highlight module contains classes and functions for displaying short\nexcerpts from hit documents in the search results you present to the user, with\nquery terms highlighted.\n'
from __future__ import division
from heapq import nlargest
from cgi import escape as htmlescape

class Fragment(object):
    """Represents a fragment (extract) from a hit document. This object is
    mainly used to keep track of the start and end points of the fragment; it
    does not contain the text of the fragment or do much else.
    """

    def __init__(self, tokens, charsbefore=0, charsafter=0, textlen=999999):
        """
        :param tokens: list of the Token objects in the fragment. 
        :param charsbefore: approx. how many characters before the start of the
            first matched term to include in the fragment.
        :param charsafter: approx. how many characters after the end of the
            last matched term to include in the fragment.
        :param textlen: length in characters of the document text.
        """
        self.startchar = max(0, tokens[0].startchar - charsbefore)
        self.endchar = min(textlen, tokens[(-1)].endchar + charsafter)
        self.matches = [ t for t in tokens if t.matched ]
        self.matched_terms = frozenset(t.text for t in self.matches)

    def __len__(self):
        return self.endchar - self.startchar

    def overlaps(self, fragment):
        sc = self.startchar
        ec = self.endchar
        fsc = fragment.startchar
        fec = fragment.endchar
        return fsc > sc and fsc < ec or fec > sc and fec < ec

    def overlapped_length(self, fragment):
        sc = self.startchar
        ec = self.endchar
        fsc = fragment.startchar
        fec = fragment.endchar
        return max(ec, fec) - min(sc, fsc)

    def has_matches(self):
        return any(t.matched for t in self.tokens)


def copyandmatchfilter(termset, tokens):
    for t in tokens:
        t = t.copy()
        t.matched = t.text in termset
        yield t


def NullFragmenter(text, tokens):
    """Doesn't fragment the token stream. This object just returns the entire
    stream as one "fragment". This is useful if you want to highlight the
    entire text.
    """
    tokens = list(tokens)
    before = after = 0
    if tokens:
        before = tokens[0].startchar
        after = len(text) - tokens[(-1)].endchar
    return [Fragment(tokens, charsbefore=before, charsafter=after)]


class SimpleFragmenter(object):
    """Simply splits the text into roughly equal sized chunks.
    """

    def __init__(self, size=70):
        """
        :param size: size (in characters) to chunk to. The chunking is based on
            tokens, so the fragments will usually be smaller.
        """
        self.size = size

    def __call__(self, text, tokens):
        size = self.size
        first = None
        frag = []
        for t in tokens:
            if first is None:
                first = t.startchar
            if t.endchar - first > size:
                first = None
                if frag:
                    yield Fragment(frag)
                frag = []
            frag.append(t)

        if frag:
            yield Fragment(frag)
        return


class SentenceFragmenter(object):
    """Breaks the text up on sentence end punctuation characters
    (".", "!", or "?"). This object works by looking in the original text for a
    sentence end as the next character after each token's 'endchar'.
    
    When highlighting with this fragmenter, you should use an analyzer that
    does NOT remove stop words, for example::
    
        sa = StandardAnalyzer(stoplist=None)
    """

    def __init__(self, maxchars=200, sentencechars='.!?'):
        """
        :param maxchars: The maximum number of characters allowed in a fragment.
        """
        self.maxchars = maxchars
        self.sentencechars = frozenset(sentencechars)

    def __call__(self, text, tokens):
        maxchars = self.maxchars
        sentencechars = self.sentencechars
        textlen = len(text)
        first = None
        frag = []
        for t in tokens:
            if first is None:
                first = t.startchar
            endchar = t.endchar
            if endchar - first > maxchars:
                first = None
                if frag:
                    yield Fragment(frag)
                frag = []
            frag.append(t)
            if frag and endchar < textlen and text[endchar] in sentencechars:
                if endchar + 1 < textlen and text[(endchar + 1)] in sentencechars:
                    continue
                yield Fragment(frag, charsafter=0)
                frag = []
                first = None

        if frag:
            yield Fragment(frag)
        return


class ContextFragmenter(object):
    """Looks for matched terms and aggregates them with their surrounding
    context.
    
    This fragmenter only yields fragments that contain matched terms.
    """

    def __init__(self, termset, maxchars=200, surround=20):
        """
        :param termset: A collection (probably a set or frozenset) containing
            the terms you want to match to token.text attributes.
        :param maxchars: The maximum number of characters allowed in a
            fragment.
        :param surround: The number of extra characters of context to add both
            before the first matched term and after the last matched term.
        """
        self.maxchars = maxchars
        self.charsbefore = self.charsafter = surround

    def __call__(self, text, tokens):
        maxchars = self.maxchars
        charsbefore = self.charsbefore
        charsafter = self.charsafter
        current = []
        currentlen = 0
        countdown = -1
        for t in tokens:
            if t.matched:
                countdown = charsafter
            current.append(t)
            length = t.endchar - t.startchar
            currentlen += length
            if countdown >= 0:
                countdown -= length
                if countdown < 0 or currentlen >= maxchars:
                    yield Fragment(current)
                    current = []
                    currentlen = 0
            else:
                while current and currentlen > charsbefore:
                    t = current.pop(0)
                    currentlen -= t.endchar - t.startchar

        if countdown >= 0:
            yield Fragment(current)


def BasicFragmentScorer(f):
    score = sum(t.boost for t in f.matches)
    score *= len(f.matched_terms) * 100
    return score


def SCORE(fragment):
    """Sorts higher scored passages first."""
    return


def FIRST(fragment):
    """Sorts passages from earlier in the document first."""
    return fragment.startchar


def LONGER(fragment):
    """Sorts longer passages first."""
    return 0 - len(fragment)


def SHORTER(fragment):
    """Sort shorter passages first."""
    return len(fragment)


class UppercaseFormatter(object):
    """Returns a string in which the matched terms are in UPPERCASE.
    """

    def __init__(self, between='...'):
        """
        :param between: the text to add between fragments.
        """
        self.between = between

    def _format_fragment(self, text, fragment):
        output = []
        index = fragment.startchar
        for t in fragment.matches:
            if t.startchar > index:
                output.append(text[index:t.startchar])
            ttxt = text[t.startchar:t.endchar]
            if t.matched:
                ttxt = ttxt.upper()
            output.append(ttxt)
            index = t.endchar

        output.append(text[index:fragment.endchar])
        return ('').join(output)

    def __call__(self, text, fragments):
        return self.between.join(self._format_fragment(text, fragment) for fragment in fragments)


class HtmlFormatter(object):
    """Returns a string containing HTML formatting around the matched terms.
    
    This formatter wraps matched terms in an HTML element with two class names.
    The first class name (set with the constructor argument ``classname``) is
    the same for each match. The second class name (set with the constructor
    argument ``termclass`` is different depending on which term matched. This
    allows you to give different formatting (for example, different background
    colors) to the different terms in the excerpt.
    
    >>> hf = HtmlFormatter(tagname="span", classname="match", termclass="term")
    >>> hf(mytext, myfragments)
    "The <span class="match term0">template</span> <span class="match term1">geometry</span> is..."
    
    This object maintains a dictionary mapping terms to HTML class names (e.g.
    ``term0`` and ``term1`` above), so that multiple excerpts will use the same
    class for the same term. If you want to re-use the same HtmlFormatter
    object with different searches, you should call HtmlFormatter.clear()
    between searches to clear the mapping.
    """
    template = '<%(tag)s class=%(q)s%(cls)s%(tn)s%(q)s>%(t)s</%(tag)s>'

    def __init__(self, tagname='strong', between='...', classname='match', termclass='term', maxclasses=5, attrquote='"'):
        """
        :param tagname: the tag to wrap around matching terms.
        :param between: the text to add between fragments.
        :param classname: the class name to add to the elements wrapped around
            matching terms.
        :param termclass: the class name prefix for the second class which is
            different for each matched term.
        :param maxclasses: the maximum number of term classes to produce. This
            limits the number of classes you have to define in CSS by recycling
            term class names. For example, if you set maxclasses to 3 and have
            5 terms, the 5 terms will use the CSS classes ``term0``, ``term1``,
            ``term2``, ``term0``, ``term1``.
        """
        self.between = between
        self.tagname = tagname
        self.classname = classname
        self.termclass = termclass
        self.attrquote = attrquote
        self.maxclasses = maxclasses
        self.seen = {}

    def _format_fragment(self, text, fragment, seen):
        htmlclass = (' ').join((self.classname, self.termclass))
        output = []
        index = fragment.startchar
        for t in fragment.matches:
            if t.startchar > index:
                output.append(text[index:t.startchar])
            ttxt = htmlescape(text[t.startchar:t.endchar])
            if t.matched:
                if t.text in seen:
                    termnum = seen[t.text]
                else:
                    termnum = len(seen) % self.maxclasses
                    seen[t.text] = termnum
                ttxt = self.template % {'tag': self.tagname, 'q': self.attrquote, 
                   'cls': htmlclass, 
                   't': ttxt, 
                   'tn': termnum}
            output.append(ttxt)
            index = t.endchar

        if index < fragment.endchar:
            output.append(text[index:fragment.endchar])
        return ('').join(output)

    def __call__(self, text, fragments):
        seen = self.seen
        return self.between.join(self._format_fragment(text, fragment, seen) for fragment in fragments)

    def clear(self):
        """Clears the dictionary mapping terms to HTML classnames.
        """
        self.seen = {}


class GenshiFormatter(object):
    """Returns a Genshi event stream containing HTML formatting around the
    matched terms.
    """

    def __init__(self, qname='strong', between='...'):
        """
        :param qname: the QName for the tag to wrap around matched terms.
        :param between: the text to add between fragments.
        """
        self.qname = qname
        self.between = between
        from genshi.core import START, END, TEXT, Attrs, Stream
        self.START, self.END, self.TEXT = START, END, TEXT
        self.Attrs, self.Stream = Attrs, Stream

    def _add_text(self, text, output):
        if output and output[(-1)][0] == self.TEXT:
            output[-1] = (
             self.TEXT, output[(-1)][1] + text, output[(-1)][2])
        else:
            output.append((self.TEXT, text, (None, -1, -1)))
        return

    def _format_fragment(self, text, fragment):
        START, TEXT, END, Attrs = (self.START, self.TEXT, self.END, self.Attrs)
        qname = self.qname
        output = []
        index = fragment.startchar
        lastmatched = False
        for t in fragment.matches:
            if t.startchar > index:
                if lastmatched:
                    output.append((END, qname, (None, -1, -1)))
                    lastmatched = False
                self._add_text(text[index:t.startchar], output)
            ttxt = text[t.startchar:t.endchar]
            if not lastmatched:
                output.append((START, (qname, Attrs()), (None, -1, -1)))
                lastmatched = True
            output.append((TEXT, ttxt, (None, -1, -1)))
            index = t.endchar

        if lastmatched:
            output.append((END, qname, (None, -1, -1)))
        return output

    def __call__(self, text, fragments):
        output = []
        first = True
        for fragment in fragments:
            if not first:
                self._add_text(self.between, output)
            first = False
            output += self._format_fragment(text, fragment)

        return self.Stream(output)


def top_fragments(text, terms, analyzer, fragmenter, top=3, scorer=BasicFragmentScorer, minscore=1):
    termset = frozenset(terms)
    tokens = copyandmatchfilter(termset, analyzer(text, chars=True, keeporiginal=True))
    scored_frags = nlargest(top, ((scorer(f), f) for f in fragmenter(text, tokens)))
    return [ sf for score, sf in scored_frags if score > minscore ]


def highlight(text, terms, analyzer, fragmenter, formatter, top=3, scorer=BasicFragmentScorer, minscore=1, order=FIRST):
    fragments = top_fragments(text, terms, analyzer, fragmenter, top=top, minscore=minscore)
    fragments.sort(key=order)
    return formatter(text, fragments)


if __name__ == '__main__':
    pass