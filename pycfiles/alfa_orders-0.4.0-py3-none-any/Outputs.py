# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Outputs.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = '\nThe programming interface, responsible of the output of all results\n\n'
import json, re
from pyparsing import ParseException
from alfanous.main import QuranicSearchEngine, FuzzyQuranicSearchEngine
from alfanous.main import TraductionSearchEngine, WordSearchEngine
from alfanous.dynamic_resources.arabicnames_dyn import ara2eng_names as Fields
from alfanous.dynamic_resources.std2uth_dyn import std2uth_words
from alfanous.dynamic_resources.vocalizations_dyn import vocalization_dict
from alfanous.dynamic_resources.synonymes_dyn import syndict
from alfanous.dynamic_resources.derivations_dyn import derivedict
from alfanous.TextProcessing import QArabicSymbolsFilter
from alfanous.Data import *
from alfanous.Romanization import transliterate
from alfanous.Misc import LOCATE, FIND, FILTER_DOUBLES
from alfanous.Constants import LANGS
STANDARD2UTHMANI = lambda x: std2uth_words[x] if std2uth_words.has_key(x) else x
FALSE_PATTERN = '^false|no|off|0$'

def IS_FLAG(flags, key):
    default = Raw.DEFAULTS['flags'][key]
    val = flags.get(key, default)
    if val is None or val == '':
        return default
    if not val or re.match(FALSE_PATTERN, str(val), re.IGNORECASE):
        return False
    return True


def SCAN_SUPERJOKERS(query):
    """
        a function to detect SuperJokers such as  *, ????, 
        a "*" query is a superjoker if it contains less then 3 letters
        a "?" query is a superjoker if it contains less then 2 letters
        a mixed query has the same conditions of a "?" query
        
        TODO that's a quick fix, the problem of superjokers must be fixed in 
                        the query parser or by time delay 
        """
    myreg = re.compile('\\*+|[\\؟\\?]{2,9}|[ \t\n\r\\(\\)\\+\\-\\|]+|[^ ]+:|')
    filtred_query = myreg.sub('', query)
    super_joker = True if len(filtred_query) < 3 and '*' in query or len(filtred_query) < 2 and ('?' in query or '؟' in query) or query.count('*') > 2 else False
    if query in ('?', '؟', '???????????', '؟؟؟؟؟؟؟؟؟؟؟؟'):
        super_joker = False
    return super_joker


def FREEZE_XRANGE(d):
    new_d = dict(d)
    for k, v in d.items():
        if v.__class__ == xrange:
            new_d[k] = str(v)

    return new_d


def DEFREEZE_XRANGE(d):
    """ TODO reversing the operation of freezing xranges done by module alfanous.output """
    pass


class Raw():
    """ Basic format for output, as  structures of python

        TODO Add word annotations to results
        FIXME terms are standard and Qurany corpus are uthmani   # resolve with uthmani mapping of Taha , + domains + errors
        
        """
    DEFAULTS = {'minrange': 1, 
       'maxrange': 25, 
       'maxkeywords': 100, 
       'results_limit': {'aya': 6236, 
                         'translation': 1000, 
                         'word': 1000}, 
       'flags': {'action': 'search', 
                 'unit': 'aya', 
                 'ident': 'undefined', 
                 'platform': 'undefined', 
                 'domain': 'undefined', 
                 'query': '', 
                 'script': 'standard', 
                 'vocalized': True, 
                 'highlight': 'css', 
                 'view': 'custom', 
                 'recitation': '1', 
                 'translation': None, 
                 'romanization': None, 
                 'prev_aya': True, 
                 'next_aya': True, 
                 'sura_info': True, 
                 'sura_stat_info': False, 
                 'word_info': True, 
                 'word_synonyms': False, 
                 'word_derivations': True, 
                 'word_vocalizations': True, 
                 'aya_position_info': True, 
                 'aya_theme_info': True, 
                 'aya_stat_info': True, 
                 'aya_sajda_info': True, 
                 'annotation_word': False, 
                 'annotation_aya': False, 
                 'sortedby': 'score', 
                 'offset': 1, 
                 'range': 10, 
                 'page': 1, 
                 'perpage': 10, 
                 'fuzzy': False, 
                 'aya': True}}
    ERRORS = {-1: 'fail, reason unknown', 
       0: 'success', 
       1: 'no action is chosen or action undefined', 
       2: 'SuperJokers are not permitted, you have to add  3 letters \n\t           or more to use * (only two are permitted) and 2 letters or more to use ? (؟)\n\n\t     \t-- Exceptions: ? (1),  ??????????? (11)\n\t     \t', 
       3: 'Parsing Query failed, please reformulate  the query', 
       4: "One of specified fields doesn't exist"}
    DOMAINS = {'action': [
                'search', 'suggest', 'show'], 
       'unit': [
              'aya', 'word', 'translation'], 
       'ident': [
               'undefined'], 
       'platform': [
                  'undefined', 'wp7', 's60', 'android', 'ios', 'linux', 'window'], 
       'domain': [], 'query': [], 'highlight': [
                   'css', 'html', 'genshi', 'bold', 'bbcode'], 
       'script': [
                'standard', 'uthmani'], 
       'vocalized': [
                   True, False], 
       'view': [
              'minimal', 'normal', 'full', 'statistic', 'linguistic', 'recitationcustom'], 
       'recitation': [], 'translation': [], 'romanization': [
                      'none', 'buckwalter', 'iso', 'arabtex'], 
       'prev_aya': [
                  True, False], 
       'next_aya': [
                  True, False], 
       'sura_info': [
                   True, False], 
       'sura_stat_info': [
                        True, False], 
       'word_info': [
                   True, False], 
       'word_synonyms': [
                       True, False], 
       'word_derivations': [
                          True, False], 
       'word_vocalizations': [
                            True, False], 
       'aya_position_info': [
                           True, False], 
       'aya_theme_info': [
                        True, False], 
       'aya_stat_info': [
                       True, False], 
       'aya_sajda_info': [
                        True, False], 
       'annotation_word': [
                         True, False], 
       'annotation_aya': [
                        True, False], 
       'sortedby': [
                  'score', 'relevance', 'mushaf', 'tanzil', 'subject', 'ayalength'], 
       'offset': [], 'range': [], 'page': [], 'perpage': [], 'fuzzy': [
               True, False], 
       'aya': [
             True, False]}
    HELPMESSAGES = {'action': 'action to perform', 
       'unit': 'search unit', 
       'ident': 'identifier of requester', 
       'platform': 'platform used by requester', 
       'domain': 'web domain of requester if applicable', 
       'query': 'query attached to action', 
       'highlight': 'highlight method', 
       'script': 'script of aya text', 
       'vocalized': 'enable vocalization of aya text', 
       'view': 'pre-defined configuration for what information to retrieve', 
       'recitation': 'recitation id', 
       'translation': 'translation id', 
       'romanization': 'type of romanization', 
       'prev_aya': 'enable previous aya retrieving', 
       'next_aya': 'enable next aya retrieving', 
       'sura_info': 'enable sura information retrieving (override sura_stat_info if False)', 
       'sura_stat_info': 'enable sura stats retrieving (has no effect if sura_info is False)', 
       'word_info': 'enable word information retrieving', 
       'word_synonyms': 'enable  retrieving of keyword synonyms', 
       'word_derivations': 'enable  retrieving of keyword derivations', 
       'word_vocalizations': 'enable  retrieving of keyword vocalizations', 
       'aya_position_info': 'enable aya position information retrieving', 
       'aya_theme_info': 'enable aya theme information retrieving', 
       'aya_stat_info': 'enable aya stat information retrieving', 
       'aya_sajda_info': 'enable aya sajda information retrieving', 
       'annotation_word': 'enable query terms annotations retrieving', 
       'annotation_aya': 'enable aya words annotations retrieving', 
       'sortedby': 'sorting order of results', 
       'offset': 'starting offset of results', 
       'range': 'range of results', 
       'page': 'page number  [override offset]', 
       'perpage': 'results per page  [override range]', 
       'fuzzy': 'fuzzy search [exprimental]', 
       'aya': 'enable retrieving of aya text in the case of translation search'}
    IDS = [
     'ALFANOUS_WUI_2342R52']

    def __init__(self, QSE_index=Paths.QSE_INDEX, TSE_index=Paths.TSE_INDEX, WSE_index=Paths.WSE_INDEX, Recitations_list_file=Paths.RECITATIONS_LIST_FILE, Translations_list_file=Paths.TRANSLATIONS_LIST_FILE, Hints_file=Paths.HINTS_FILE, Stats_file=Paths.STATS_FILE, Information_file=Paths.INFORMATION_FILE):
        """
                initialize the search engines
                """
        self.QSE = Indexes.QSE(QSE_index)
        self.FQSE = Indexes.FQSE(QSE_index)
        self.TSE = Indexes.TSE(TSE_index)
        self.WSE = Indexes.WSE(WSE_index)
        self._recitations = Configs.recitations(Recitations_list_file)
        self._translations = Configs.translations(Translations_list_file)
        self._hints = Configs.hints(Hints_file)
        self._information = Resources.information(Information_file)
        self._surates = {'Arabic': [ item for item in self.QSE.list_values('sura_arabic') if item ], 'English': [ item for item in self.QSE.list_values('sura_english') if item ], 'Romanized': [ item for item in self.QSE.list_values('sura') if item ]}
        self._chapters = [ item for item in self.QSE.list_values('chapter') if item ]
        self._defaults = self.DEFAULTS
        self._flags = self.DEFAULTS['flags'].keys()
        self._fields = Fields
        self._fields_reverse = dict((v, k) for k, v in Fields.iteritems())
        self._roots = sorted(filter(bool, set(derivedict['root'])))
        self._errors = self.ERRORS
        self._domains = self.DOMAINS
        self._helpmessages = self.HELPMESSAGES
        self._ids = self.IDS
        self._all = {'translations': self._translations, 
           'recitations': self._recitations, 
           'information': self._information, 
           'hints': self._hints, 
           'surates': self._surates, 
           'chapters': self._chapters, 
           'defaults': self._defaults, 
           'flags': self._flags, 
           'fields': self._fields, 
           'fields_reverse': self._fields_reverse, 
           'errors': self._errors, 
           'domains': self._domains, 
           'help_messages': self._helpmessages, 
           'roots': self._roots}

    def do(self, flags):
        return self._do(flags)

    def _do(self, flags):
        action = flags['action'] if flags.has_key('action') else self._defaults['flags']['action']
        unit = flags['unit'] if flags.has_key('unit') else self._defaults['flags']['unit']
        ident = flags['ident'] if flags.has_key('ident') else self._defaults['flags']['ident']
        platform = flags['platform'] if flags.has_key('platform') else self._defaults['flags']['platform']
        domain = flags['domain'] if flags.has_key('domain') else self._defaults['flags']['domain']
        output = self._check(0, flags)
        if action == 'search':
            if SCAN_SUPERJOKERS(flags['query']):
                output = self._check(2, flags)
            else:
                output.update(self._search(flags, unit))
        elif action == 'suggest':
            output.update(self._suggest(flags, unit))
        elif action == 'show':
            output.update(self._show(flags))
        else:
            output.update(self._check(1, flags))
        return output

    def _check(self, error_code, flags):
        """ prepare the error messages """
        return {'error': {'code': error_code, 'msg': self._errors[error_code] % flags}}

    def _init_stats(self):
        stats = {}
        for ident in ['TOTAL']:
            stats[ident] = {}
            stats[ident]['total'] = 0
            stats[ident]['other'] = {}
            stats[ident]['other']['total'] = 0
            for action in self.DOMAINS['action']:
                stats[ident][action] = {}
                stats[ident][action]['total'] = 0
                stats[ident][action]['other'] = {}
                stats[ident][action]['other']['total'] = 0
                for flag, domain in self.DOMAINS.items():
                    stats[ident][action][flag] = {}
                    stats[ident][action][flag]['total'] = 0
                    stats[ident][action][flag]['other'] = 0
                    for val in domain:
                        stats[ident][action][flag][str(val)] = 0

        stats.update(self._stats)
        self._stats = stats

    def _process_stats(self, flags):
        """ process flags for statistics """
        stats = self._stats
        for ident in ['TOTAL']:
            stats[ident]['total'] += 1
            if flags.has_key('action'):
                action = flags['action']
                if action in self._domains['action']:
                    stats[ident][action]['total'] += 1
                    for flag, val in flags.items():
                        if flag in self._domains.keys():
                            stats[ident][action][flag]['total'] += 1
                            if val in self._domains[flag]:
                                stats[ident][action][flag][str(val)] += 1
                            else:
                                stats[ident][action][flag]['other'] += 1
                        else:
                            stats[ident][action]['other']['total'] += 1

                else:
                    stats[ident]['other']['total'] += 1

        self._stats = stats
        f = open(Paths.STATS_FILE, 'w')
        f.write(json.dumps(self._stats))

    def _show(self, flags):
        """  show metadata"""
        query = flags['query'] if flags.has_key('query') else self._defaults['flags']['query']
        if query == 'all':
            return {'show': self._all}
        else:
            if self._all.has_key(query):
                return {'show': {query: self._all[query]}}
            else:
                return {'show': None}

            return

    def _suggest(self, flags, unit):
        """ return suggestions for any search unit """
        if unit == 'aya':
            suggestions = self._suggest_aya(flags)
        elif unit == 'translation':
            suggestions = None
        else:
            suggestions = {}
        return {'suggest': suggestions}

    def _suggest_aya(self, flags):
        """ return suggestions for aya words """
        query = flags['query'] if flags.has_key('query') else self._defaults['flags']['query']
        query = query.replace('\\', '')
        if not isinstance(query, unicode):
            query = unicode(query, 'utf8')
        try:
            output = self.QSE.suggest_all(query)
        except Exception:
            output = {}

        return output

    def _search(self, flags, unit):
        """ return the results of search for any unit """
        try:
            if unit == 'aya':
                search_results = self._search_aya(flags)
            elif unit == 'translation':
                search_results = self._search_translation(flags)
            elif unit == 'word':
                search_results = self._search_word(flags)
            else:
                search_results = {}
            output = {'search': search_results}
        except ParseException:
            output = {'error': {'code': 3, 'msg': self.ERRORS[3]}}
        except Exception as E:
            output = {'error': {'code': -1, 'msg': self.ERRORS[(-1)] + '\n' + str(E) + '\n\n please submit that as a bug here: feedback.alfanous.org!'}}

        return output

    def _search_aya(self, flags):
        """
                return the results of aya search as a dictionary data structure
                """
        query = flags['query'] if flags.has_key('query') else self._defaults['flags']['query']
        sortedby = flags['sortedby'] if flags.has_key('sortedby') else self._defaults['flags']['sortedby']
        range = int(flags['perpage']) if flags.has_key('perpage') else flags['range'] if flags.has_key('range') else self._defaults['flags']['range']
        offset = (int(flags['page']) - 1) * range + 1 if flags.has_key('page') else int(flags['offset']) if flags.has_key('offset') else self._defaults['flags']['offset']
        recitation = flags['recitation'] if flags.has_key('recitation') else self._defaults['flags']['recitation']
        translation = flags['translation'] if flags.has_key('translation') else self._defaults['flags']['translation']
        romanization = flags['romanization'] if flags.has_key('romanization') else self._defaults['flags']['romanization']
        highlight = flags['highlight'] if flags.has_key('highlight') else self._defaults['flags']['highlight']
        script = flags['script'] if flags.has_key('script') else self._defaults['flags']['script']
        vocalized = IS_FLAG(flags, 'vocalized')
        fuzzy = IS_FLAG(flags, 'fuzzy')
        view = flags['view'] if flags.has_key('view') else self._defaults['flags']['view']
        if view == 'minimal':
            vocalized = False
            recitation = None
            translation = None
            prev_aya = next_aya = False
            sura_info = False
            word_info = False
            word_synonyms = False
            word_derivations = False
            word_vocalizations = False
            aya_position_info = aya_theme_info = aya_sajda_info = False
            aya_stat_info = False
            sura_stat_info = False
            annotation_aya = annotation_word = False
        else:
            if view == 'normal':
                prev_aya = next_aya = False
                sura_info = True
                word_info = True
                word_synonyms = False
                word_derivations = True
                word_vocalizations = True
                aya_position_info = aya_theme_info = aya_sajda_info = True
                aya_stat_info = True
                sura_stat_info = False
                annotation_aya = annotation_word = False
            elif view == 'full':
                prev_aya = next_aya = True
                sura_info = True
                word_info = True
                word_synonyms = True
                word_derivations = True
                word_vocalizations = True
                aya_position_info = aya_theme_info = aya_sajda_info = True
                aya_stat_info = sura_stat_info = True
                annotation_aya = annotation_word = True
                romanization = 'iso'
            elif view == 'statistic':
                prev_aya = next_aya = False
                sura_info = True
                word_info = True
                word_synonyms = False
                word_derivations = True
                word_vocalizations = True
                aya_position_info = True
                aya_theme_info = aya_sajda_info = False
                aya_stat_info = True
                sura_stat_info = True
                annotation_aya = False
                annotation_word = False
            elif view == 'linguistic':
                prev_aya = next_aya = False
                sura_info = False
                word_info = True
                word_synonyms = True
                word_derivations = True
                word_vocalizations = True
                aya_position_info = False
                aya_theme_info = aya_sajda_info = True
                aya_stat_info = False
                sura_stat_info = False
                annotation_aya = True
                annotation_word = True
                romanization = 'buckwalter'
            elif view == 'recitation':
                script = 'uthmani'
                prev_aya = next_aya = True
                sura_info = True
                word_info = False
                word_synonyms = False
                word_derivations = False
                word_vocalizations = False
                aya_position_info = True
                aya_theme_info = False
                aya_sajda_info = True
                aya_stat_info = False
                sura_stat_info = False
                annotation_aya = False
                annotation_word = False
            else:
                prev_aya = IS_FLAG(flags, 'prev_aya')
                next_aya = IS_FLAG(flags, 'next_aya')
                sura_info = IS_FLAG(flags, 'sura_info')
                sura_stat_info = IS_FLAG(flags, 'sura_stat_info')
                word_info = IS_FLAG(flags, 'word_info')
                word_synonyms = IS_FLAG(flags, 'word_synonyms')
                word_derivations = IS_FLAG(flags, 'word_derivations')
                word_vocalizations = IS_FLAG(flags, 'word_vocalizations')
                aya_position_info = IS_FLAG(flags, 'aya_position_info')
                aya_theme_info = IS_FLAG(flags, 'aya_theme_info')
                aya_stat_info = IS_FLAG(flags, 'aya_stat_info')
                aya_sajda_info = IS_FLAG(flags, 'aya_sajda_info')
                annotation_aya = IS_FLAG(flags, 'annotation_aya')
                annotation_word = IS_FLAG(flags, 'annotation_word')
            query = query.replace('\\', '')
            if not isinstance(query, unicode):
                query = unicode(query, 'utf8')
            if ':' not in query:
                query = unicode(transliterate('buckwalter', query, ignore='\'_"%*?#~[]{}:>+-|'))
            SE = self.FQSE if fuzzy else self.QSE
            res, termz, searcher = SE.search_all(query, self._defaults['results_limit']['aya'], sortedby=sortedby)
            terms = [ term[1] for term in list(termz)[:self._defaults['maxkeywords']] ]
            terms_uthmani = map(STANDARD2UTHMANI, terms)
            offset = 1 if offset < 1 else offset
            range = self._defaults['minrange'] if range < self._defaults['minrange'] else range
            range = self._defaults['maxrange'] if range > self._defaults['maxrange'] else range
            interval_end = offset + range - 1
            end = interval_end if interval_end < len(res) else len(res)
            start = offset if offset <= len(res) else -1
            reslist = [] if end == 0 or start == -1 else list(res)[start - 1:end]
            searcher.close()
            output = {}
            if annotation_aya and len(res) > 1:
                annotation_aya = False
            V = QArabicSymbolsFilter(shaping=False, tashkil=not vocalized, spellerrors=False, hamza=False).normalize_all
            strip_vocalization = QArabicSymbolsFilter(shaping=False, tashkil=True, spellerrors=False, hamza=False).normalize_all
            H = --- This code section failed: ---

 L. 619         0  LOAD_DEREF            0  'highlight'
                3  LOAD_CONST               'none'
                6  COMPARE_OP            3  !=
                9  POP_JUMP_IF_FALSE    40  'to 40'
               12  LOAD_FAST             0  'X'
             15_0  COME_FROM             9  '9'
               15  POP_JUMP_IF_FALSE    40  'to 40'
               18  LOAD_DEREF            1  'self'
               21  LOAD_ATTR             0  'QSE'
               24  LOAD_ATTR             1  'highlight'
               27  LOAD_FAST             0  'X'
               30  LOAD_DEREF            2  'terms'
               33  LOAD_DEREF            0  'highlight'
               36  CALL_FUNCTION_3       3  None
               39  RETURN_END_IF_LAMBDA
             40_0  COME_FROM            15  '15'
               40  LOAD_FAST             0  'X'
               43  POP_JUMP_IF_FALSE    50  'to 50'
               46  LOAD_FAST             0  'X'
               49  RETURN_END_IF_LAMBDA
             50_0  COME_FROM            43  '43'
               50  LOAD_CONST               '-----'
               53  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
            N = lambda X: X if X else 0
            kword = re.compile('[^,،]+')
            keywords = lambda phrase: kword.findall(phrase)
            extend_runtime = res.runtime
            words_output = {'individual': {}}
            if word_info:
                matches = 0
                docs = 0
                nb_vocalizations_globale = 0
                cpt = 1
                annotation_word_query = '( 0 '
                for term in termz:
                    if term[0] == 'aya' or term[0] == 'aya_':
                        if term[2]:
                            matches += term[2]
                        docs += term[3]
                        if term[0] == 'aya_':
                            annotation_word_query += ' OR word:%s ' % term[1]
                        else:
                            annotation_word_query += ' OR normalized:%s ' % STANDARD2UTHMANI(term[1])
                        if word_vocalizations:
                            vocalizations = vocalization_dict[strip_vocalization(term[1])] if vocalization_dict.has_key(strip_vocalization(term[1])) else []
                            nb_vocalizations_globale += len(vocalizations)
                        if word_synonyms:
                            synonyms = syndict[term[1]] if syndict.has_key(term[1]) else []
                        if word_derivations:
                            lemma = LOCATE(derivedict['word_'], derivedict['lemma'], term[1])
                            if lemma:
                                derivations = FILTER_DOUBLES(FIND(derivedict['lemma'], derivedict['word_'], lemma))
                            else:
                                derivations = []
                            root = LOCATE(derivedict['word_'], derivedict['root'], term[1])
                            if root:
                                derivations_extra = list(set(FILTER_DOUBLES(FIND(derivedict['root'], derivedict['word_'], lemma))) - set(derivations))
                            else:
                                derivations_extra = []
                        words_output['individual'][cpt] = {'word': term[1], 
                           'romanization': transliterate(romanization, term[1], ignore='', reverse=True) if romanization in self.DOMAINS['romanization'] else None, 
                           'nb_matches': term[2], 
                           'nb_ayas': term[3], 
                           'nb_vocalizations': len(vocalizations) if word_vocalizations else 0, 
                           'vocalizations': vocalizations if word_vocalizations else [], 
                           'nb_synonyms': len(synonyms) if word_synonyms else 0, 
                           'synonyms': synonyms if word_synonyms else [], 
                           'lemma': lemma if word_derivations else '', 
                           'root': root if word_derivations else '', 
                           'nb_derivations': len(derivations) if word_derivations else 0, 
                           'derivations': derivations if word_derivations else [], 
                           'nb_derivations_extra': len(derivations_extra), 
                           'derivations_extra': derivations_extra}
                        cpt += 1

                annotation_word_query += ' ) '
                words_output['global'] = {'nb_words': cpt - 1, 'nb_matches': matches, 'nb_vocalizations': nb_vocalizations_globale}
            output['words'] = words_output
            if prev_aya or next_aya or translation or annotation_aya:
                adja_query = trad_query = annotation_aya_query = '( 0'
                for r in reslist:
                    if prev_aya:
                        adja_query += ' OR gid:%s ' % unicode(r['gid'] - 1)
                    if next_aya:
                        adja_query += ' OR gid:%s ' % unicode(r['gid'] + 1)
                    if translation:
                        trad_query += ' OR gid:%s ' % unicode(r['gid'])
                    if annotation_aya:
                        annotation_aya_query += ' OR  ( aya_id:%s AND  sura_id:%s ) ' % (unicode(r['aya_id']), unicode(r['sura_id']))

                adja_query += ' )'
                trad_query += ' )' + ' AND id:%s ' % unicode(translation)
                annotation_aya_query += ' )'
            if prev_aya or next_aya:
                adja_res, searcher = self.QSE.find_extended(adja_query, 'gid')
                adja_ayas = {0: {'aya_': '----', 'uth_': '----', 'sura': '---', 'aya_id': 0, 'sura_arabic': '---'}, 6237: {'aya_': '----', 'uth_': '----', 'sura': '---', 'aya_id': 9999, 'sura_arabic': '---'}}
                for adja in adja_res:
                    adja_ayas[adja['gid']] = {'aya_': adja['aya_'], 'uth_': adja['uth_'], 'aya_id': adja['aya_id'], 'sura': adja['sura'], 'sura_arabic': adja['sura_arabic']}
                    extend_runtime += adja_res.runtime

                searcher.close()
            if translation:
                trad_res, searcher = self.TSE.find_extended(trad_query, 'gid')
                extend_runtime += trad_res.runtime
                trad_text = {}
                for tr in trad_res:
                    trad_text[tr['gid']] = tr['text']

                searcher.close()
            if annotation_aya or annotation_word and word_info:
                annotation_word_query = annotation_word_query if annotation_word and word_info else '()'
                annotation_aya_query = annotation_aya_query if annotation_aya else '()'
                annotation_query = annotation_aya_query + ' OR  ' + annotation_word_query
                annot_res, searcher = self.WSE.find_extended(annotation_query, 'gid')
                extend_runtime += annot_res.runtime
                annotations_by_word = {}
                annotations_by_position = {}
                for annot in annot_res:
                    if annotation_word and word_info:
                        if annot['normalized'] in terms_uthmani:
                            if annotations_by_word.has_key(annot['normalized']):
                                if annotations_by_word[annot['normalized']].has_key(annot['word']):
                                    annotations_by_word[annot['normalized']][annot['word']].append(annot)
                                else:
                                    annotations_by_word[annot['normalized']][annot['word']] = [
                                     annot]
                            else:
                                annotations_by_word[annot['normalized']] = {annot['word']: [annot]}
                    if annotation_aya:
                        if annotations_by_position.has_key((annot['sura_id'], annot['aya_id'])):
                            annotations_by_position[(annot['sura_id'], annot['aya_id'])][annot['word_id']] = annot
                        else:
                            annotations_by_position[(annot['sura_id'], annot['aya_id'])] = {annot['word_id']: annot}

                searcher.close()
            if annotation_word and word_info:
                for cpt in xrange(1, len(output['words']['individual']) + 1):
                    current_word = STANDARD2UTHMANI(output['words']['individual'][cpt]['word'])
                    if annotations_by_word.has_key(current_word):
                        current_word_annotations = annotations_by_word[current_word]
                        output['words']['individual'][cpt]['annotations'] = current_word_annotations
                        output['words']['individual'][cpt]['nb_annotations'] = len(current_word_annotations)

            output['runtime'] = round(extend_runtime, 5)
            output['interval'] = {'start': start, 
               'end': end, 
               'total': len(res), 
               'page': (start - 1) / range + 1, 
               'nb_pages': (len(res) - 1) / range + 1}
            output['translation_info'] = {}
            cpt = start - 1
            output['ayas'] = {}
            for r in reslist:
                cpt += 1
                output['ayas'][cpt] = {'identifier': {'gid': r['gid'], 'aya_id': r['aya_id'], 
                                  'sura_id': r['sura_id'], 
                                  'sura_name': keywords(r['sura'])[0], 
                                  'sura_arabic_name': keywords(r['sura_arabic'])[0]}, 
                   'aya': {'id': r['aya_id'], 
                           'text': H(V(r['aya_'])) if script == 'standard' else H(r['uth_']), 
                           'text_no_highlight': r['aya'] if script == 'standard' else r['uth_'], 
                           'translation': trad_text[r['gid']] if translation != 'None' and translation and trad_text.has_key(r['gid']) else None, 
                           'recitation': None if not recitation or not self._recitations.has_key(recitation) else 'http://www.everyayah.com/data/' + self._recitations[recitation]['subfolder'].encode('utf-8') + '/%03d%03d.mp3' % (r['sura_id'], r['aya_id']), 
                           'prev_aya': {'id': adja_ayas[(r['gid'] - 1)]['aya_id'], 'sura': adja_ayas[(r['gid'] - 1)]['sura'], 'sura_arabic': adja_ayas[(r['gid'] - 1)]['sura_arabic'], 'text': V(adja_ayas[(r['gid'] - 1)]['aya_']) if script == 'standard' else adja_ayas[(r['gid'] - 1)]['uth_']} if prev_aya else None, 
                           'next_aya': {'id': adja_ayas[(r['gid'] + 1)]['aya_id'], 'sura': adja_ayas[(r['gid'] + 1)]['sura'], 'sura_arabic': adja_ayas[(r['gid'] + 1)]['sura_arabic'], 'text': V(adja_ayas[(r['gid'] + 1)]['aya_']) if script == 'standard' else adja_ayas[(r['gid'] + 1)]['uth_']} if next_aya else None}, 
                   'sura': {} if not sura_info else {'name': keywords(r['sura'])[0], 
                            'arabic_name': keywords(r['sura_arabic'])[0], 
                            'english_name': keywords(r['sura_english'])[0], 
                            'id': r['sura_id'], 
                            'type': r['sura_type'], 
                            'arabic_type': r['sura_type_arabic'], 
                            'order': r['sura_order'], 
                            'ayas': r['s_a'], 
                            'stat': {} if not sura_stat_info else {'words': N(r['s_w']), 
                                     'godnames': N(r['s_g']), 
                                     'letters': N(r['s_l'])}}, 
                   'position': {} if not aya_position_info else {'manzil': r['manzil'], 
                                'juz': r['juz'], 
                                'hizb': r['hizb'], 
                                'rub': r['rub'] % 4, 
                                'page': r['page'], 
                                'page_IN': r['page_IN'], 
                                'ruku': r['ruku']}, 
                   'theme': {} if not aya_theme_info else {'chapter': r['chapter'], 
                             'topic': r['topic'], 
                             'subtopic': r['subtopic']}, 
                   'stat': {} if not aya_stat_info else {'words': N(r['a_w']), 
                            'letters': N(r['a_l']), 
                            'godnames': N(r['a_g'])}, 
                   'sajda': {} if not aya_sajda_info else {'exist': r['sajda'] == 'نعم', 
                             'type': r['sajda_type'] if r['sajda'] == 'نعم' else None, 
                             'id': N(r['sajda_id']) if r['sajda'] == 'نعم' else None}, 
                   'annotations': {} if not annotation_aya or not annotations_by_position.has_key((r['sura_id'], r['aya_id'])) else annotations_by_position[(r['sura_id'], r['aya_id'])]}

        return output

    def _search_translation(self, flags):
        """
                return the results of translation search as a dictionary data structure
                """
        query = flags['query'] if flags.has_key('query') else self._defaults['flags']['query']
        range = int(flags['perpage']) if flags.has_key('perpage') else flags['range'] if flags.has_key('range') else self._defaults['flags']['range']
        offset = (int(flags['page']) - 1) * range + 1 if flags.has_key('page') else int(flags['offset']) if flags.has_key('offset') else self._defaults['flags']['offset']
        highlight = flags['highlight'] if flags.has_key('highlight') else self._defaults['flags']['highlight']
        view = flags['view'] if flags.has_key('view') else self._defaults['flags']['view']
        if view == 'minimal':
            aya = False
        else:
            if view == 'normal':
                pass
            elif view == 'full':
                aya = True
            else:
                aya = IS_FLAG(flags, 'aya')
            query = query.replace('\\', '')
            if not isinstance(query, unicode):
                query = unicode(query, 'utf8')
            SE = self.TSE
            res, termz, searcher = SE.search_all(query, self._defaults['results_limit']['translation'])
            terms = [ term[1] for term in list(termz)[:self._defaults['maxkeywords']] ]
            offset = 1 if offset < 1 else offset
            range = self._defaults['minrange'] if range < self._defaults['minrange'] else range
            range = self._defaults['maxrange'] if range > self._defaults['maxrange'] else range
            interval_end = offset + range - 1
            end = interval_end if interval_end < len(res) else len(res) if len(res) < self._defaults['results_limit']['translation'] else self._defaults['results_limit']['translation']
            start = offset if offset <= len(res) else -1
            total = len(res)
            limited_total = total if total < self._defaults['results_limit']['translation'] else self._defaults['results_limit']['translation']
            reslist = [] if end == 0 or start == -1 else list(res)[start - 1:end]
            searcher.close()
            output = {}
            H = --- This code section failed: ---

 L. 922         0  LOAD_DEREF            1  'highlight'
                3  LOAD_CONST               'none'
                6  COMPARE_OP            3  !=
                9  POP_JUMP_IF_FALSE    37  'to 37'
               12  LOAD_FAST             0  'X'
             15_0  COME_FROM             9  '9'
               15  POP_JUMP_IF_FALSE    37  'to 37'
               18  LOAD_DEREF            0  'SE'
               21  LOAD_ATTR             0  'highlight'
               24  LOAD_FAST             0  'X'
               27  LOAD_DEREF            2  'terms'
               30  LOAD_DEREF            1  'highlight'
               33  CALL_FUNCTION_3       3  None
               36  RETURN_END_IF_LAMBDA
             37_0  COME_FROM            15  '15'
               37  LOAD_FAST             0  'X'
               40  POP_JUMP_IF_FALSE    47  'to 47'
               43  LOAD_FAST             0  'X'
               46  RETURN_END_IF_LAMBDA
             47_0  COME_FROM            40  '40'
               47  LOAD_CONST               '-----'
               50  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
            N = lambda X: X if X else 0
            extend_runtime = res.runtime
            if aya:
                aya_query = '( 0'
                for r in reslist:
                    if aya:
                        aya_query += ' OR gid:%s ' % unicode(r['gid'])

                aya_query += ' )'
            if aya:
                aya_res, searcher = self.QSE.find_extended(aya_query, 'gid')
                extend_runtime += aya_res.runtime
                aya_info = {}
                for ay in aya_res:
                    aya_info[ay['gid']] = {'text': ay['aya_'], 'aya_id': ay['aya_id'], 'sura_name': ay['sura'], 
                       'sura_arabic_name': ay['sura_arabic']}

                searcher.close()
            output['runtime'] = round(extend_runtime, 5)
            output['interval'] = {'start': start, 
               'end': end, 
               'total': total, 
               'page': (start - 1) / range + 1, 
               'nb_pages': (limited_total - 1) / range + 1}
            output['terms'] = terms
            cpt = start - 1
            output['translations'] = {}
            for r in reslist:
                cpt += 1
                output['translations'][cpt] = {'identifier': {'gid': r['gid'], 'id': r['id']}, 
                   'text': H(r['text']), 
                   'aya': None if not aya else aya_info[r['gid']], 
                   'info': {'language': LANGS[r['lang']], 
                            'language_short': r['lang'], 
                            'author': r['author'], 
                            'country': r['country']}}

        return output

    def _search_word(self, flags):
        """
                return the results of word search as a dictionary data structure
                """
        query = flags['query'] if flags.has_key('query') else self._defaults['flags']['query']
        sortedby = flags['sortedby'] if flags.has_key('sortedby') else self._defaults['flags']['sortedby']
        range = int(flags['perpage']) if flags.has_key('perpage') else flags['range'] if flags.has_key('range') else self._defaults['flags']['range']
        offset = (int(flags['page']) - 1) * range + 1 if flags.has_key('page') else int(flags['offset']) if flags.has_key('offset') else self._defaults['flags']['offset']
        romanization = flags['romanization'] if flags.has_key('romanization') else self._defaults['flags']['romanization']
        highlight = flags['highlight'] if flags.has_key('highlight') else self._defaults['flags']['highlight']
        script = flags['script'] if flags.has_key('script') else self._defaults['flags']['script']
        vocalized = IS_FLAG(flags, 'vocalized')
        view = flags['view'] if flags.has_key('view') else self._defaults['flags']['view']
        if view == 'minimal':
            vocalized = False
            aya = False
        else:
            if view == 'normal':
                pass
            elif view == 'full':
                romanization = 'iso'
                aya = True
            elif view == 'statistic':
                pass
            elif view == 'linguistic':
                romanization = 'buckwalter'
            elif view == 'recitation':
                script = 'uthmani'
            else:
                aya = IS_FLAG(flags, 'aya')
            query = query.replace('\\', '')
            if not isinstance(query, unicode):
                query = unicode(query, 'utf8')
            if ':' not in query:
                query = unicode(transliterate('buckwalter', query, ignore='\'_"%*?#~[]{}:>+-|'))
            SE = self.WSE
            res, termz, searcher = SE.search_all(query, self._defaults['results_limit']['word'], sortedby=sortedby)
            terms = [ term[1] for term in list(termz)[:self._defaults['maxkeywords']] ]
            offset = 1 if offset < 1 else offset
            range = self._defaults['minrange'] if range < self._defaults['minrange'] else range
            range = self._defaults['maxrange'] if range > self._defaults['maxrange'] else range
            interval_end = offset + range - 1
            end = interval_end if interval_end < len(res) else len(res)
            start = offset if offset <= len(res) else -1
            reslist = [] if end == 0 or start == -1 else list(res)[start - 1:end]
            searcher.close()
            output = {}
            V = QArabicSymbolsFilter(**{'shaping': True, 
               'tashkil': not vocalized, 
               'spellerrors': False, 
               'hamza': False, 
               'uthmani_symbols': True}).normalize_all
            V_shadda = QArabicSymbolsFilter(**{'shaping': False, 
               'tashkil': False, 
               'spellerrors': False, 
               'hamza': False, 
               'shadda': True, 
               'uthmani_symbols': True}).normalize_all
            H = --- This code section failed: ---

 L.1068         0  LOAD_DEREF            1  'highlight'
                3  LOAD_CONST               'none'
                6  COMPARE_OP            3  !=
                9  POP_JUMP_IF_FALSE    37  'to 37'
               12  LOAD_FAST             0  'X'
             15_0  COME_FROM             9  '9'
               15  POP_JUMP_IF_FALSE    37  'to 37'
               18  LOAD_DEREF            0  'SE'
               21  LOAD_ATTR             0  'highlight'
               24  LOAD_FAST             0  'X'
               27  LOAD_DEREF            2  'terms'
               30  LOAD_DEREF            1  'highlight'
               33  CALL_FUNCTION_3       3  None
               36  RETURN_END_IF_LAMBDA
             37_0  COME_FROM            15  '15'
               37  LOAD_FAST             0  'X'
               40  POP_JUMP_IF_FALSE    47  'to 47'
               43  LOAD_FAST             0  'X'
               46  RETURN_END_IF_LAMBDA
             47_0  COME_FROM            40  '40'
               47  LOAD_CONST               '-----'
               50  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
            N = lambda X: X if X else 0
            kword = re.compile('[^,،]+')
            keywords = lambda phrase: kword.findall(phrase)
            extend_runtime = res.runtime
            words_output = {'individual': {}}
            if True:
                matches = 0
                docs = 0
                cpt = 1
                for term in termz:
                    if True:
                        if term[2]:
                            matches += term[2]
                        docs += term[3]
                        words_output['individual'][cpt] = {'field': term[0], 
                           'word': term[1], 
                           'romanization': transliterate(romanization, term[1], ignore='', reverse=True) if romanization in self.DOMAINS['romanization'] else None, 
                           'nb_matches': term[2], 
                           'nb_docs': term[3]}
                        cpt += 1

                words_output['global'] = {'nb_words': cpt - 1, 'nb_matches': matches}
            output['keywords'] = words_output
            if aya:
                aya_query = '( 0'
                for r in reslist:
                    if aya:
                        aya_query += ' OR ( sura_id:%s AND aya_id:%s )  ' % (unicode(r['sura_id']), unicode(r['aya_id']))

                aya_query += ' )'
            if aya:
                aya_res = self.QSE.find_extended(aya_query, 'gid')
                extend_runtime += aya_res.runtime
                aya_info = {}
                for ay in aya_res:
                    if aya_info.has_key(ay['sura_id']):
                        aya_info[ay['sura_id']][ay['aya_id']] = ay
                    else:
                        aya_info[ay['sura_id']] = {ay['aya_id']: ay}

            output['runtime'] = round(extend_runtime, 5)
            output['interval'] = {'start': start, 
               'end': end, 
               'total': len(res), 
               'page': (start - 1) / range + 1, 
               'nb_pages': (len(res) - 1) / range + 1}
            cpt = start - 1
            output['words'] = {}
            for r in reslist:
                cpt += 1
                output['words'][cpt] = {'identifier': {'gid': r['gid'], 
                                  'word_gid': r['word_gid'], 
                                  'aya_id': r['aya_id'], 
                                  'sura_id': r['sura_id'], 
                                  'word_id': r['word_id']}, 
                   'word': {'text': r['word'], 
                            'part': 'جذع', 
                            'part_order': r['order'], 
                            'token': r['arabictoken'], 
                            'prefixes': r['prefix'], 
                            'suffixes': r['suffix'], 
                            'POS': {'english': r['pos'], 
                                    'arabic': r['arabicpos']}, 
                            'mood': {'english': r['mood'], 
                                     'arabic': r['arabicmood']}, 
                            'case': {'english': r['case'], 
                                     'arabic': r['arabiccase']}, 
                            'root': {'arabic': r['arabicroot']}, 
                            'lemma': {'arabic': r['arabiclemma']}, 
                            'special': {'arabic': r['arabicspecial']}, 
                            'derivation': r['derivation'], 
                            'form': r['form'], 
                            'gender': r['gender'], 
                            'person': r['person'], 
                            'number': r['number'], 
                            'voice': r['voice'], 
                            'state': r['state'], 
                            'aspect': r['aspect']}, 
                   'aya': None if not aya else {'text': SE.highlight(aya_info[r['sura_id']][r['aya_id']]['uth_'], [r['word']], highlight, False), 
                           'aya_id': aya_info[r['sura_id']][r['aya_id']]['aya_id'], 
                           'sura_name': aya_info[r['sura_id']][r['aya_id']]['sura'], 
                           'sura_arabic_name': aya_info[r['sura_id']][r['aya_id']]['sura_arabic']}}

        return output


class Json(Raw):
    """ JSON output format """

    def do(self, flags):
        return json.dumps(self._do(flags), sort_keys=False, indent=4)


class Xml(Raw):
    """ XML output format

        @deprecated: Why Xml and CompleXity?! Use jSon and Simplicity!
        """