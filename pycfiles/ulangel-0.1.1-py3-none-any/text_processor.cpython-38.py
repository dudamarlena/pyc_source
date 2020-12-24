# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./ulangel/data/text_processor.py
# Compiled at: 2020-03-05 08:23:54
# Size of source mod 2**32: 3063 bytes
import html, re, emoji
UNK = 'xxunk'
PAD = 'xxpad'
BOS = 'xxbos'
EOS = 'xxeos'
TK_REP = 'xxrep'
TK_WREP = 'xxwrep'
TK_UP = 'xxup'
TK_MAJ = 'xxmaj'
BOS = 'xbos'
FLD = 'xfld'

def toLowercase(matchobj):
    return matchobj.group(1).lower()


def lower_tw(tweet):
    tweet_with_lower_tw = re.sub('(@\\S+){1}', toLowercase, tweet)
    return tweet_with_lower_tw


def fixup(x):
    re1 = re.compile('  +')
    x = x.replace('#39;', "'").replace('&amp;', '&').replace('#146;', "'").replace('nbsp;', ' ').replace('#36;', '$').replace('\\n', '\n').replace('quot;', "'").replace('<br />', '\n').replace('\\"', '"').replace('<unk>', 'u_n').replace(' @.@ ', '.').replace(' @-@ ', '-').replace('\\', ' \\ ').replace('\xa0', '')
    x = re.sub('[h][t][t][p]\\S+', '', x)
    x = emoji.demojize(x)
    return re1.sub(' ', html.unescape(x))


def spec_add_spaces(x):
    """Add spaces around / and #"""
    x = re.sub('([/#@])', ' \\1 ', x)
    x = re.sub('([:][\\S]+[:])', ' \\1 ', x.replace('::', ': :'))
    return x


def rm_useless_spaces(x):
    """Remove multiple spaces"""
    return re.sub(' {2,}', ' ', x)


def replace_all_caps(x):
    """Replace tokens in ALL CAPS by their lower version and add `TK_UP` ahead."""
    res = []
    for t in x:
        if t.isupper() and len(t) > 1:
            res.append(TK_UP)
            res.append(t.lower())
        else:
            res.append(t)
    else:
        return res


def deal_caps(x):
    """Replace all Capitalized tokens in by their lower version and add `TK_MAJ` ahead."""
    res = []
    for t in x:
        if t == '':
            pass
        else:
            if t[0].isupper():
                if len(t) > 1:
                    if t[1:].islower():
                        res.append(TK_MAJ)
            res.append(t.lower())
    else:
        return res


def replace_rep(x):
    """Replace repetitions at the character level: cccc -> TK_REP 4 c"""

    def _replace_rep(m):
        c, cc = m.groups()
        return f" {TK_REP} {len(cc) + 1} {c} "

    re_rep = re.compile('(\\S)(\\1{3,})')
    return re_rep.sub(_replace_rep, x)


def replace_wrep(x):
    """Replace word repetitions: word word word -> TK_WREP 3 word"""

    def _replace_wrep(m):
        c, cc = m.groups()
        return f" {TK_WREP} {len(cc.split()) + 1} {c} "

    re_wrep = re.compile('(\\b\\w+\\W+)(\\1{3,})')
    return re_wrep.sub(_replace_wrep, x)


def text_proc(txts, tokenizer):
    texts = fixup(txts)
    texts = replace_wrep(texts)
    texts = replace_rep(texts)
    texts = spec_add_spaces(texts)
    texts = rm_useless_spaces(texts)
    tok = [t.text for t in tokenizer(texts)]
    tok = replace_all_caps(tok)
    tok = deal_caps(tok)
    tok = [BOS] + tok + [EOS]
    return [tok]