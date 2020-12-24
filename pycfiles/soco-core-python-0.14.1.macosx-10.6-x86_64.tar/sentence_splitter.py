# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonyzhao/anaconda2/lib/python2.7/site-packages/soco_core/sentence_splitter.py
# Compiled at: 2020-04-17 14:36:35
import re

def split_sentence(sentence, lang='en'):
    if lang == 'en':
        return en_split_sentence(sentence)
    if lang == 'zh':
        return zh_split_sentence(sentence)
    raise Exception(('Unsupported language {}').format(lang))


def zh_split_sentence(text):
    resentencesp = re.compile('([\t﹒﹔﹖﹗．；。！？]["’”」』]{0,2}|：(?=["‘“「『]{1,2}|$))')
    s = text
    slist = []
    for i in resentencesp.split(s):
        if resentencesp.match(i) and slist:
            slist[(-1)] += i
        elif i:
            slist.append(i)

    return slist


def en_split_sentence(text):
    sentences = []
    for span in _infer_sentence_breaks(text):
        sentences.append(text[span[0]:span[1]])

    return sentences


def _infer_sentence_breaks(uni_text):
    """Generates (start, end) pairs demarking sentences in the text.

  Args:
    uni_text: A (multi-sentence) passage of text, in Unicode.

  Yields:
    (start, end) tuples that demarcate sentences in the input text. Normal
    Python slicing applies: the start index points at the first character of
    the sentence, and the end index is one past the last character of the
    sentence.
  """
    uni_text = re.sub('\\n', ' ', uni_text)
    text_with_breaks = _sed_do_sentence_breaks(uni_text)
    starts = [ m.end() for m in re.finditer('^\\s*', text_with_breaks, re.M) ]
    sentences = [ s.strip() for s in text_with_breaks.split('\n') ]
    assert len(starts) == len(sentences)
    for i in range(len(sentences)):
        start = starts[i]
        end = start + len(sentences[i])
        yield (start, end)


def _sed_do_sentence_breaks(uni_text):
    """Uses regexp substitution rules to insert newlines as sentence breaks.

  Args:
    uni_text: A (multi-sentence) passage of text, in Unicode.

  Returns:
    A Unicode string with internal newlines representing the inferred sentence
    breaks.
  """
    txt = re.sub('([.?!][)\'" %s]*)\\s(\\s*[[\'"(%s]?[A-Z0-9])' % ('\\u201D', '\\u201C'), '\\1\\n\\2', uni_text)
    txt = re.sub('([.?!][\'"]?)((\\[[a-zA-Z0-9 ?]+\\])+)\\s(\\s*[\'"(]?[A-Z0-9])', '\\1\\2\\n\\4', txt)
    txt = re.sub('(\\[\\.\\.\\.\\]\\s*)\\s(\\[?[A-Z])', '\\1\\n\\2', txt)
    txt = re.sub('\\b(Mrs?|Ms|Dr|Prof|Fr|Rev|Msgr|Sta?)\\.\\n', '\\1. ', txt)
    txt = re.sub('\\b(Lt|Gen|Col|Maj|Adm|Capt|Sgt|Rep|Gov|Sen|Pres)\\.\\n', '\\1. ', txt)
    txt = re.sub('\\b(e\\.g|i\\.?e|vs?|pp?|cf|a\\.k\\.a|approx|app|es[pt]|tr)\\.\\n', '\\1. ', txt)
    txt = re.sub('\\b(Jan|Aug|Oct|Nov|Dec)\\.\\n', '\\1. ', txt)
    txt = re.sub('\\b(Mt|Ft)\\.\\n', '\\1. ', txt)
    txt = re.sub('\\b([ap]\\.m)\\.\\n(Eastern|EST)\\b', '\\1. \\2', txt)
    txt = re.sub('\\b([A-Z]\\.)[ \\n]([A-Z]\\.)[ \\n]([A-Z]\\.)[ \\n]("?[A-Z][a-z])', '\\1 \\2 \\3 \\4', txt)
    txt = re.sub('\\b([A-Z]\\.)[ \\n]([A-Z]\\.)[ \\n]("?[A-Z][a-z])', '\\1 \\2 \\3', txt)
    txt = re.sub('\\b([A-Z]\\.[A-Z]\\.)\\n("?[A-Z][a-z])', '\\1 \\2', txt)
    txt = re.sub('\\b([A-Z]\\.)\\n("?[A-Z][a-z])', '\\1 \\2', txt)
    txt = re.sub('([.!?][\\\'")]*) (The|This|That|These|It) ', '\\1\\n\\2 ', txt)
    txt = re.sub('(\\.) (Meanwhile|However)', '\\1\\n\\2', txt)
    txt = re.sub('(\\.) (In|On|By|During|After|Under|Although|Yet|As |Several|According to) ', '\\1\\n\\2 ', txt)
    txt = re.sub('\\b([Aa]rt|[Nn]o|Opp?|ch|Sec|cl|Rec|Ecl|Cor|Lk|Jn|Vol)\\.\\n([0-9IVX]+)\\b', '\\1. \\2', txt)
    txt = re.sub('\\b([bdrc]|ca|fl)\\.\\n([A-Z0-9])', '\\1. \\2', txt)
    txt = re.sub('\\b(et al)\\.\\n(\\(?[0-9]{4}\\b)', '\\1. \\2', txt)
    txt = re.sub('\\b(H\\.R\\.)\\n([0-9])', '\\1 \\2', txt)
    txt = re.sub('(I Am\\.\\.\\.)\\n(Sasha Fierce|World Tour)', '\\1 \\2', txt)
    txt = re.sub('(Warner Bros\\.)\\n(Records|Entertainment)', '\\1 \\2', txt)
    txt = re.sub('(U\\.S\\.)\\n(\\(?\\d\\d+)', '\\1 \\2', txt)
    txt = re.sub('\\b(Rs\\.)\\n(\\d)', '\\1 \\2', txt)
    txt = re.sub('\\b(Jay Z\\.) ([A-Z])', '\\1\\n\\2', txt)
    txt = re.sub('\\b(Washington, D\\.C\\.) ([A-Z])', '\\1\\n\\2', txt)
    txt = re.sub('\\b(for 4\\.\\)) ([A-Z])', '\\1\\n\\2', txt)
    txt = re.sub('\\b(Wii U\\.) ([A-Z])', '\\1\\n\\2', txt)
    txt = re.sub('\\. (iPod|iTunes)', '.\\n\\1', txt)
    txt = re.sub(' (\\[\\.\\.\\.\\]\\n)', '\\n\\1', txt)
    txt = re.sub('(\\.Sc\\.)\\n', '\\1 ', txt)
    txt = re.sub(' (\\u2022 [A-Z])', '\\n\\1', txt)
    return txt