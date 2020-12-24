# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/DH/prosodic/dicts/en/english.py
# Compiled at: 2018-11-13 19:02:36
import sys, codecs, os, subprocess
from ipa import sampa2ipa
import pyphen
Pyphen = None
DIR_ROOT = os.path.split(globals()['__file__'])[0]
CMU_DICT_FN = os.path.join(DIR_ROOT, 'english.tsv')
CMU_DICT = {}
CACHE_DICT_FN = os.path.join(DIR_ROOT, 'english.tts-cache.tsv')
CACHE_DICT_F = None

def load_cmu(fn=CMU_DICT_FN, config={}):
    global CMU_DICT
    fns = [
     fn]
    if config.get('en_TTS_cache', False):
        fns += [CACHE_DICT_FN]
    for fn in fns:
        if os.path.exists(fn):
            with codecs.open(fn, encoding='utf-8') as (f):
                for ln in f:
                    ln = ln.strip()
                    if not ln or ln.count('\t') != 1:
                        continue
                    word, ipa = ln.split('\t')[:2]
                    word = word.strip()
                    ipa = ipa.strip().split()[0]
                    if word not in CMU_DICT:
                        CMU_DICT[word] = []
                    CMU_DICT[word] += [ipa]


def write_to_cache(token, ipa):
    global CACHE_DICT_F
    tokenl = token.lower()
    if not CACHE_DICT_F:
        CACHE_DICT_F = codecs.open(CACHE_DICT_FN, 'a', encoding='utf-8')
    CACHE_DICT_F.write(tokenl + '\t' + ipa + '\n')
    if tokenl not in CMU_DICT:
        CMU_DICT[tokenl] = []
    CMU_DICT[tokenl] += [ipa]


def get(token, config={}, toprint=False):
    if not CMU_DICT:
        load_cmu(config=config)
    tokenl = word_l = token.lower()
    ipas = CMU_DICT.get(tokenl, [])
    if not ipas:
        for contr, add_ipa in [("'d", 'd')]:
            if word_l.endswith(contr):
                word_l_unc = word_l[:-2]
                if word_l_unc in CMU_DICT:
                    for wipa in CMU_DICT[word_l_unc]:
                        wipa += add_ipa
                        ipas += [wipa]

    if not ipas:
        TTS_ENGINE = config.get('en_TTS_ENGINE', '')
        if TTS_ENGINE == 'espeak':
            ipa = espeak2ipa(token)
            cmu = espeak2cmu(ipa)
            cmu_sylls = syllabify_cmu(cmu)
            if toprint:
                print ipa
            if toprint:
                print cmu
            if toprint:
                print cmu_sylls
            ipa = cmusylls2ipa(cmu_sylls)
            if toprint:
                print ipa
        elif TTS_ENGINE == 'openmary':
            ipa = openmary2ipa(token)
        else:
            return
        ipas = [
         ipa]
        if config.get('en_TTS_cache', False):
            for ipa in ipas:
                write_to_cache(token, ipa)

    results = []
    iselision = []
    for ipa in ipas:
        num_sylls = ipa.count('.') + 1
        sylls_text = syllabify_orth(token, num_sylls=num_sylls)
        res = (ipa, sylls_text)
        if res not in results:
            results += [res]
            iselision += [False]
        if config.get('add_elided_pronunciations', 0):
            for ipa2 in add_elisions(ipa):
                num_sylls2 = ipa2.count('.') + 1
                sylls_text2 = syllabify_orth(token, num_sylls=num_sylls2)
                res = (ipa2, sylls_text2)
                if res not in results:
                    results += [res]
                    iselision += [True]

    toreturn = [ (a, b, {'is_elision': c}) for (a, b), c in zip(results, iselision) ]
    return toreturn


def add_elisions(_ipa):
    """
        Add alternative pronunciations: those that have elided syllables
        """
    replace = {}
    replace['aʊ.ɛː'] = 'aʊr'
    replace['ə.nəs'] = 'nəs'
    replace['ɛː.əs'] = 'rəs'
    replace['iː.ə'] = 'jə'
    replace['iː.ɛː'] = 'ɪr'
    replace['ɛː.ɪŋ'] = 'rɪŋ'
    replace['ə.nɪŋ'] = 'nɪŋ'
    replace['ə.nɛː'] = 'nɛː'
    replace['ɪ.ɛː'] = 'ɪr'
    replace['uː.əl'] = 'uːl'
    replace['ɛ.vən'] = 'ɛvn'
    replace['eɪ.ʌ'] = 'eɪʌ'
    new = [
     _ipa]
    for k, v in replace.items():
        if k in _ipa:
            new += [_ipa.replace(k, v)]

    return new


def espeak2ipa(token):
    CMD = 'espeak -q -x ' + token.replace("'", "\\'").replace('"', '\\"')
    try:
        res = subprocess.check_output(CMD.split()).strip()
        return res
    except (OSError, subprocess.CalledProcessError) as e:
        return

    return


def tts2ipa(token, TTS_ENGINE=None):
    if TTS_ENGINE == 'espeak':
        return espeak2ipa(token)
    else:
        if TTS_ENGINE == 'openmary':
            return openmary2ipa(token)
        else:
            return

        return


def espeak2cmu(tok):
    import lexconvert
    return lexconvert.convert(tok, 'espeak', 'cmu')


def ipa2cmu(tok):
    import lexconvert
    return lexconvert.convert(tok, 'unicode-ipa', 'cmu')


def cmu2ipa(tok):
    import lexconvert
    res = lexconvert.convert(tok, 'cmu', 'unicode-ipa')
    if tok.endswith(' T') and not res.endswith('t'):
        res = res + 't'
    return res


def syllabify_cmu(cmu_token):
    import syllabify as sy
    cmu_token = cmu_token.replace(' 2', '2').replace(' 1', '1')
    sylls = sy.syllabify(sy.English, cmu_token)
    return sylls


def cmusylls2ipa(sylls):
    new_cmu = []
    for syl in sylls:
        stress, onset, nucleus, coda = syl
        if stress:
            nucleus = [
             nucleus[0] + ' ' + str(stress)] + nucleus[1:]
        _newcmu = (' ').join(onset + nucleus + coda).strip().replace('  ', ' ')
        new_cmu += [_newcmu]

    new_cmu = (' 0 ').join(new_cmu)
    ipa = cmu2ipa(new_cmu)
    ipa_sylls = ipa.split('.')
    for i, syl in enumerate(ipa_sylls):
        if 'ˈ' in syl:
            syl = "'" + syl.replace('ˈ', '')
        if 'ˌ' in syl:
            syl = '`' + syl.replace('ˌ', '')
        ipa_sylls[i] = syl

    ipa = ('.').join(ipa_sylls)
    return ipa


def syllabify_orth_with_hyphenate(token, num_sylls=None):
    from hyphenate import hyphenate_word
    l = hyphenate_word(token)
    if not num_sylls or len(l) == num_sylls:
        return l
    return []


def syllabify_orth_with_pyphen(token, num_sylls=None):
    global Pyphen
    if not Pyphen:
        Pyphen = pyphen.Pyphen(lang='en_US')
    sylls = Pyphen.inserted(token, hyphen='||||').split('||||')
    if len(sylls) == num_sylls:
        return sylls
    return []


def syllabify_orth(token, num_sylls=None):
    return syllabify_orth_with_pyphen(token, num_sylls=num_sylls)


def openmary2ipa(word):
    import urllib2
    try:
        wordxml = openmary(word)
    except urllib2.URLError:
        return

    sylls = []
    for syll in wordxml.find_all('syllable'):
        syllstr = "'" if syll.get('stress', None) else ''
        for ph in syll['ph'].split():
            syllstr += sampa2ipa(ph)

        sylls += [syllstr]

    from Phoneme import Phoneme
    if len(sylls) > 1 and True not in [ Phoneme(phon).isVowel() for phon in sylls[0] ]:
        sylls = [
         sylls[0] + sylls[1]] + (sylls[2:] if len(sylls) > 2 else [])
    pronounc = ('.').join(sylls)
    return pronounc


def openmary(line):
    import re, urlparse, urllib2
    try:
        from unidecode import unidecode
    except ImportError:
        raise Exception('\n\t\t\tIn order to use OpenMary, you need to install the unidecode python module. Run:\n\t\t\tpip install unidecode\n\t\t\t')

    try:
        import bs4
    except ImportError:
        raise Exception('\n\t\t\tIn order to use OpenMary, you need to install the bs4 python module. Run:\n\t\t\tpip install bs4\n\t\t\t')

    line = line.replace("'", '')
    line = unidecode(line)

    def urlEncodeNonAscii(b):
        return re.sub(b'[\x80-\xff]', lambda c: '%%%02x' % ord(c.group(0)), b)

    def iriToUri(iri):
        parts = urlparse.urlparse(iri)
        return urlparse.urlunparse((part.encode('idna') if parti == 1 else urlEncodeNonAscii(part.encode('utf-8'))) for parti, part in enumerate(parts))

    def bigrams(l):
        return ngram(l, 2)

    def ngram(l, n=3):
        grams = []
        gram = []
        for x in l:
            gram.append(x)
            if len(gram) < n:
                continue
            g = tuple(gram)
            grams.append(g)
            gram.reverse()
            gram.pop()
            gram.reverse()

        return grams

    line = line.replace(' ', '+')
    link = ('http://localhost:59125/process?INPUT_TEXT={0}&INPUT_TYPE=TEXT&OUTPUT_TYPE=ALLOPHONES&LOCALE=en_US').format(line)
    f = urllib2.urlopen(iriToUri(link))
    t = f.read()
    f.close()
    xml = bs4.BeautifulSoup(t, 'html.parser')
    for word in xml.find_all('t'):
        word['token'] = word.text.strip()

    for para in xml.find_all('p'):
        for phrase in para.find_all('phrase'):
            wordlist = [ word for word in phrase.find_all('t') if len(list(word.find_all('syllable'))) ]
            for word1, word2 in bigrams(wordlist):
                w2text = word2.text.strip().lower()
                if w2text.startswith("'"):
                    phones2add = word2.find_all('syllable')[(-1)]['ph'].strip()
                    word1.find_all('syllable')[(-1)]['ph'] += ' ' + phones2add
                    word1['token'] += w2text
                    word2.decompose()

    return xml