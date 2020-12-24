# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/ResultsProcessing.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = '\n\n\n@author: Assem Chelli\n@contact: assem.ch [at] gmail.com\n@license: AGPL\n\n\n'
from alfanous.Support.whoosh.scoring import BM25F
from alfanous.Support.whoosh.highlight import highlight, BasicFragmentScorer, Fragment, GenshiFormatter, HtmlFormatter
from alfanous.TextProcessing import QHighLightAnalyzer, QDiacHighLightAnalyzer, Gword_tamdid

def QScore(methode=None):
    """ chooose the methode of score
        - Cosine
        - BM25F
        - TF_IDF
        - Frequency

    """
    if not methode:
        methode = BM25F(B=0.75, K1=1.2)
    return methode


def QSort(sortedby):
    """  Controls the results sorting options    """
    if sortedby == 'mushaf':
        sortedby = 'gid'
    elif sortedby == 'tanzil':
        sortedby = ('sura_order', 'aya_id')
    elif sortedby == 'subject':
        sortedby = ('chapter', 'topic', 'subtopic')
    elif sortedby == 'ayalength':
        sortedby = ('a_l', 'a_w')
    elif sortedby == 'relevance' or sortedby == 'score':
        sortedby = None
    else:
        sortedby = sortedby
    return sortedby


def QFilter(results, new_results):
    """ Filter give results with new results"""
    results.filter(new_results)
    return results


def QExtend():
    pass


def QPaginate(results, pagelen=10):
    """generator of pages"""
    l = len(results)
    minimal = lambda x, y: y if x > y else x
    for i in range(0, l, 10):
        yield (
         i / pagelen, results[i:minimal(i + pagelen, l)])


def Qhighlight(text, terms, type='css', strip_vocalization=True):
    """ highlight terms in text

    @param type: the type of formatting , html or css or genchi

    """
    if type == 'html':
        formatter = QHtmlFormatter()
    elif type == 'genshi':
        formatter = GenshiFormatter()
    elif type == 'bold':
        formatter = QBoldFormatter()
    elif type == 'bbcode':
        formatter = QBBcodeFormatter()
    else:
        formatter = HtmlFormatter(tagname='span', classname='match', termclass='term', maxclasses=8)
    h = highlight(text, terms, analyzer=QHighLightAnalyzer if strip_vocalization else QDiacHighLightAnalyzer, fragmenter=QFragmenter(), formatter=formatter, top=3, scorer=BasicFragmentScorer, minscore=1)
    if h:
        return h
    else:
        return text


class QFragmenter:
    """ TO DO """

    def __init__(self):
        pass

    def __call__(self, text, tokens):
        return [
         Fragment(list(tokens))]


class QHtmlFormatter(object):
    """ add the style tags to the text """

    def __init__(self, change_size=True, color_cycle=['red', 'green', 'orange', 'blue']):
        self._change_size = True
        self._color_cycle = color_cycle

    def _format(self, text, color, score=1):
        if self._change_size:
            ration = 100 + (score - 1) * 0.25
        else:
            ration = 100
        return '<span style="color:' + color + ';font-size:' + str(ration) + '%"><b>' + Gword_tamdid(text) + '</b></span>'

    def _format_fragment(self, text, fragment):
        output = []
        index = fragment.startchar
        CC = self._color_cycle
        CPT = 0
        MAX = len(CC)
        for t in fragment.matches:
            if t.startchar > index:
                output.append(text[index:t.startchar])
            ttxt = text[t.startchar:t.endchar]
            if t.matched:
                ttxt = self._format(ttxt, color=CC[CPT])
                CPT = (CPT + 1) % MAX
            output.append(ttxt)
            index = t.endchar

        output.append(text[index:fragment.endchar])
        return ('').join(output)

    def __call__(self, text, fragments):
        return ('').join(self._format_fragment(text, fragment) for fragment in fragments)


class QBBcodeFormatter(object):
    """ format to bbcode(forums syntax) """

    def __init__(self, change_size=True, color_cycle=['red', 'green', 'orange', 'blue']):
        self._change_size = True
        self._color_cycle = color_cycle

    def _format(self, text, color, score=1):
        return '[color=' + color + ']' + '[B]' + Gword_tamdid(text) + '[/B][/color]'

    def _format_fragment(self, text, fragment):
        output = []
        index = fragment.startchar
        CC = self._color_cycle
        CPT = 0
        MAX = len(CC)
        for t in fragment.matches:
            if t.startchar > index:
                output.append(text[index:t.startchar])
            ttxt = text[t.startchar:t.endchar]
            if t.matched:
                ttxt = self._format(ttxt, color=CC[CPT])
                CPT = (CPT + 1) % MAX
            output.append(ttxt)
            index = t.endchar

        output.append(text[index:fragment.endchar])
        return ('').join(output)

    def __call__(self, text, fragments):
        return ('').join(self._format_fragment(text, fragment) for fragment in fragments)


class QBoldFormatter(object):
    """ add the style tags to the text """

    def _format(self, text):
        return '<b>' + Gword_tamdid(text) + '</b>'

    def _format_fragment(self, text, fragment):
        output = []
        index = fragment.startchar
        for t in fragment.matches:
            if t.startchar > index:
                output.append(text[index:t.startchar])
            ttxt = text[t.startchar:t.endchar]
            if t.matched:
                ttxt = self._format(ttxt)
            output.append(ttxt)
            index = t.endchar

        output.append(text[index:fragment.endchar])
        return ('').join(output)

    def __call__(self, text, fragments):
        return ('').join(self._format_fragment(text, fragment) for fragment in fragments)