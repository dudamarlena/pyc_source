# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/utils/corpus_helpers.py
# Compiled at: 2018-10-25 10:50:30


class CorpusData(object):
    invalid_symbols_in_colnames = list('{}[]:,;-()<>=#@?^°') + [' ']
    info = {'tagger': {'tweetnlp': {'url': 'http://www.cs.cmu.edu/~ark/TweetNLP/', 
                               'paper': 'http://www.cs.cmu.edu/~ark/TweetNLP/owoputi+etal.naacl13.pdf', 
                               'tagset': {'en': {'data': {'!': 'interjection', 
                                                          '#': 'hashtag (indicates topic/category for tweet)', 
                                                          '$': 'numeral', 
                                                          '&': 'coordinating conjunction', 
                                                          ',': 'punctuation', 
                                                          '@': 'at-mention (indicates a user as a recipient of a tweet)', 
                                                          'A': 'adjective', 
                                                          'D': 'determiner', 
                                                          'E': 'emoticon', 
                                                          'G': 'other abbreviations, foreign words, possessive endings, symbols, garbage', 
                                                          'L': 'nominal + verbal (e.g. i’m), verbal + nominal (let’s)', 
                                                          'M': 'proper noun + verbal', 
                                                          'N': 'common noun', 
                                                          'O': 'pronoun (personal/WH; not possessive)', 
                                                          'P': 'pre- or postposition, or subordinating conjunction', 
                                                          'R': 'adverb', 
                                                          'S': 'nominal + possessive', 
                                                          'T': 'verb particle', 
                                                          'U': 'URL or email address', 
                                                          'V': 'verb including copula, auxiliaries', 
                                                          'X': 'existential there, predeterminers', 
                                                          'Y': 'X + verbal', 
                                                          'Z': 'proper noun + possessive', 
                                                          '^': 'proper noun', 
                                                          '~': 'discourse marker, indications of continuation across multiple tweets'}}}}, 
                  'someweta': {'url': 'https://github.com/tsproisl/SoMeWeTa', 
                               'paper': 'http://www.lrec-conf.org/proceedings/lrec2018/pdf/49.pdf', 
                               'tagset': {'de': {'name': 'STTS IBK tagset', 
                                                 'url': [
                                                       'http://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/TagSets/stts-table.html'], 
                                                 'paper': 'https://ids-pub.bsz-bw.de/frontdoor/deliver/index/docId/5065/file/Beisswenger_Bartz_Storrer_Tagset_und_Richtlinie_fuer_das_PoS_Tagging_2015.pdf', 
                                                 'data': {'$(': 'sonstige Satzzeichen; satzintern', 
                                                          '$,': 'Komma', 
                                                          '$.': 'Satzbeendende Interpunktion', 
                                                          'ADJA': 'attributives Adjektiv', 
                                                          'ADJD': 'adverbiales oder prädikatives Adjektiv', 
                                                          'ADR': 'Adressierung', 
                                                          'ADV': 'Adverb', 
                                                          'ADVART': 'Kontraktion: Adverb + Artikel', 
                                                          'AKW': 'Aktionswort', 
                                                          'APPO': 'Postposition', 
                                                          'APPR': 'Präposition, Zirkumposition links', 
                                                          'APPRART': 'Präposition mit Artikel', 
                                                          'APZR': 'Zirkumposition rechts', 
                                                          'ART': 'bestimmter oder unbestimmter Artikel', 
                                                          'CARD': 'Kardinalzahl', 
                                                          'DM': 'Diskursmarker', 
                                                          'EML': 'E-Mail-Adresse', 
                                                          'EMOASC': 'Emoticon, als Zeichenfolge dargestellt (Typ „ASCII“)', 
                                                          'EMOIMG': 'Emoticon, als Grafik-Ikon dargestellt (Typ „Image“)', 
                                                          'FM': 'Fremdsprachliches Material', 
                                                          'HST': 'Hashtag', 
                                                          'ITJ': 'Interjektion', 
                                                          'KOKOM': 'Vergleichspartikel ohne Satz', 
                                                          'KON': 'nebenordnende Konjunktion', 
                                                          'KOUI': 'unterordnende Konjunktion mit „zu“ und Infinitiv', 
                                                          'KOUS': 'unterordnende Konjunktion mit Satz (VL-Stellung)', 
                                                          'KOUSPPER': 'Kontraktion: unterordnende Konjunk- tion mit Satz (VL-Stellung) + irreflexi- ves Personalpronomen', 
                                                          'NE': 'Eigennamen', 
                                                          'NN': 'Appellativa', 
                                                          'ONO': 'Onomatopoetikon', 
                                                          'PAV': 'Pronominaladverb', 
                                                          'PDAT': 'attributierendes Demonstrativprono- men', 
                                                          'PDS': 'substituierendes Demonstrativprono- men', 
                                                          'PIAT': 'attributierendes Indefinitpronomen ohne Determiner', 
                                                          'PIDAT': 'attributierendes Indefinitpronomen mit Determiner', 
                                                          'PIS': 'substituierendes  Indefinitpronomen', 
                                                          'PPER': 'irreflexives Personalpronomen', 
                                                          'PPERPPER': 'Kontraktion: irreflexives Personalpro- nomen + irreflexives Personalprono- men', 
                                                          'PPOSAT': 'attributierendes  Possesivpronomen', 
                                                          'PPOSS': 'substituierendes  Possesivpronomen', 
                                                          'PRELAT': 'attributierendes Relativpronomen', 
                                                          'PRELS': 'substituierendes Relativpronomen', 
                                                          'PRF': 'reflexives Personalpronomen', 
                                                          'PTKA': 'Partikel bei Adjektiv oder Adverb', 
                                                          'PTKANT': 'Antwortpartikel', 
                                                          'PTKIFG': 'Intensitäts-, Fokus- oder  Gradpartikel', 
                                                          'PTKMA': 'Modal- oder Abtönungspartikel', 
                                                          'PTKMWL': 'Partikel als Teil eines Mehrwort- Lexems', 
                                                          'PTKNEG': 'Negationspartikel', 
                                                          'PTKVZ': 'abgetrennter Verbzusatz', 
                                                          'PTKZU': '„zu“ vor Infinitiv', 
                                                          'PWAT': 'attributierendes  Interrogativpronomen', 
                                                          'PWAV': 'adverbiales Interrogativ- oder Relativ- pronomen', 
                                                          'PWS': 'substituierendes Interrogativprono- men', 
                                                          'TRUNC': 'Kompositions-Erstglied', 
                                                          'URL': 'Uniform Resource Locator', 
                                                          'VAFIN': 'finites Verb, aux', 
                                                          'VAIMP': 'Imperativ, aux', 
                                                          'VAINF': 'Infinitiv, aux', 
                                                          'VAPP': 'Partizip Perfekt, aux', 
                                                          'VAPPER': 'Kontraktion: Auxiliarverb + irreflexives Personalpronomen', 
                                                          'VMFIN': 'finites Verb, modal', 
                                                          'VMINF': 'Infinitiv, modal', 
                                                          'VMPP': 'Partizip Perfekt, modal', 
                                                          'VMPPER': 'Kontraktion: Modalverb + irreflexives Personalpronomen', 
                                                          'VVFIN': 'finites Verb, voll', 
                                                          'VVIMP': 'Imperativ, voll', 
                                                          'VVINF': 'Infinitiv, voll', 
                                                          'VVIZU': 'Infinitiv mit „zu“, voll', 
                                                          'VVPP': 'Partizip Perfekt, voll', 
                                                          'VVPPER': 'Kontraktion: Vollverb + irreflexives Personalpronomen', 
                                                          'XY': 'Nichtwort, Sonderzeichen  enthaltend'}}, 
                                          'en': {'name': 'Treebank-3', 
                                                 'url': [
                                                       'https://catalog.ldc.upenn.edu/ldc99t42'], 
                                                 'paper': 'https://catalog.ldc.upenn.edu/docs/LDC99T42/tagguid1.pdf', 
                                                 'data': {'CC': 'Coordinating conjunction', 
                                                          'CD': 'Cardinal number', 
                                                          'DT': 'Determiner', 
                                                          'EX': 'Existential there', 
                                                          'FW': 'Foreign word', 
                                                          'IN': 'Preposition or subordinating', 
                                                          'JJ': 'Adjective', 
                                                          'JJR': 'Adjective, comparative', 
                                                          'JJS': 'Adjective, superlative', 
                                                          'LS': 'List item marker', 
                                                          'MD': 'Modal', 
                                                          'NN': 'Noun, singular or mass', 
                                                          'NNP': 'Proper noun, singular', 
                                                          'NNPS': 'Proper noun, plural', 
                                                          'NNS': 'Noun, plural', 
                                                          'PDT': 'Predeterminer', 
                                                          'PEP$': 'Possessive pronoun', 
                                                          'POS': 'Possessive ending', 
                                                          'PRP': 'Personal pronoun', 
                                                          'RB': 'Adverb', 
                                                          'RBR': 'Adverb, comparative', 
                                                          'RBS': 'Adverb, superlative', 
                                                          'RP': 'Particle', 
                                                          'SYM': 'Symbol', 
                                                          'TO': 'to', 
                                                          'UH': 'Interjection', 
                                                          'VB': 'Verb, base form', 
                                                          'VBD': 'Verb, past tense', 
                                                          'VBG': 'Verb, gerund or present participle', 
                                                          'VBN': 'Verb,past participle', 
                                                          'VBP': 'Verb, non-3rd person singular present', 
                                                          'VBZ': 'Verb, 3rd person singular present', 
                                                          'WDT': 'Wh-determiner', 
                                                          'WP': 'Wh-pronoun', 
                                                          'WP$': 'Possessive wh-pronoun', 
                                                          'WRB': 'Wh-adverb', 
                                                          "''": 'punctuation'}}}}}, 
       'splitter': {'somajo': {'link': 'https://github.com/tsproisl/SoMaJo', 
                               'supported_lang': 'de, en, fr'}}, 
       'tokenizer': {'somajo': {'link': 'https://github.com/tsproisl/SoMaJo', 
                                'supported_lang': 'de, en,fr'}, 
                     'nltk': {'link': 'http://www.nltk.org', 
                              'supported_lang': 'en'}}, 
       'stemmer': {'pystemmer': {'algorithm': 'snowball', 
                                 'links': [
                                         'https://github.com/snowballstem/pystemmer', 'http://snowball.tartarus.org']}}, 
       'lang_classification': {'langid': {'link': 'https://github.com/saffsd/langid.py', 
                                          'supported_lang': 'af, am, an, ar, as, az, be, bg, bn, br, bs, ca, cs, cy, da, de, dz, el, en, eo, es, et, eu, fa, fi, fo, fr, ga, gl, gu, he, hi, hr, ht, hu, hy, id, is, it, ja, jv, ka, kk, km, kn, ko, ku, ky, la, lb, lo, lt, lv, mg, mk, ml, mn, mr, ms, mt, nb, ne, nl, nn, no, oc, or, pa, pl, ps, pt, qu, ro, ru, rw, se, si, sk, sl, sq, sr, sv, sw, ta, te, th, tl, tr, ug, uk, ur, vi, vo, wa, xh, zh, zu'}}}
    tokenizer_for_languages = {'en': [
            'somajo', 'nltk'], 
       'de': [
            'somajo'], 
       'test': [
              'somajo']}
    supported_languages_tokenizer = [ key for key in tokenizer_for_languages ]
    supported_tokenizer = set([ v for values in tokenizer_for_languages.itervalues() for v in values ])
    sent_splitter_for_languages = {'en': [
            'somajo'], 
       'de': [
            'somajo'], 
       'test': [
              'somajo']}
    supported_languages_sent_splitter = [ key for key in sent_splitter_for_languages ]
    supported_sent_splitter = set([ v for values in sent_splitter_for_languages.itervalues() for v in values ])
    pos_tagger_for_languages = {'en': [
            'someweta', 'tweetnlp'], 
       'de': [
            'someweta'], 
       'fr': [
            'someweta'], 
       'test': [
              'tweetnlp']}
    supported_languages_pos_tagger = [ key for key in pos_tagger_for_languages ]
    supported_pos_tagger = set([ v for values in pos_tagger_for_languages.itervalues() for v in values ])
    pos_tagger_models = {'tweetnlp': {'en': []}, 'someweta': {'de': [
                         'german_web_social_media_2017-12-20.model', 'german_newspaper_for_empirist_2017-12-20.model'], 
                    'en': [
                         'english_newspaper_2017-09-15.model'], 
                    'fr': [
                         'french_newspaper_2018-06-20.model'], 
                    'test': [
                           'english_newspaper_2017-09-15.model']}}
    sentiment_analyzer_for_languages = {'en': [
            'textblob'], 
       'de': [
            'textblob'], 
       'fr': [
            'textblob'], 
       'test': [
              'textblob']}
    supported_languages_sentiment_analyzer = [ key for key in sentiment_analyzer_for_languages ]
    supported_sentiment_analyzer = set([ v for values in sentiment_analyzer_for_languages.itervalues() for v in values ])
    stemmer_for_languages = {'da': [
            'pystemmer'], 
       'nl': [
            'pystemmer'], 
       'en': [
            'pystemmer'], 
       'fi': [
            'pystemmer'], 
       'fr': [
            'pystemmer'], 
       'de': [
            'pystemmer'], 
       'hu': [
            'pystemmer'], 
       'it': [
            'pystemmer'], 
       'no': [
            'pystemmer'], 
       'pt': [
            'pystemmer'], 
       'ro': [
            'pystemmer'], 
       'ru': [
            'pystemmer'], 
       'es': [
            'pystemmer'], 
       'sv': [
            'pystemmer'], 
       'tr': [
            'pystemmer'], 
       'test': [
              'pystemmer']}
    supported_languages_stemmer = [ key for key in stemmer_for_languages ]
    supported_stemmer = set([ v for values in stemmer_for_languages.itervalues() for v in values ])