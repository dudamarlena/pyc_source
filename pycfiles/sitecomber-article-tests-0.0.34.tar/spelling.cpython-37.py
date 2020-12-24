# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nina/Documents/Sites/sitecomber-article-tests/sitecomber_article_tests/utils/spelling.py
# Compiled at: 2019-07-30 02:20:04
# Size of source mod 2**32: 14173 bytes
import logging, re
from string import punctuation
import unicodedata
from nltk.corpus import stopwords
import contractions
from spellchecker import SpellChecker
from .article import get_article
from .dictionary import get_extended_dictionary, valid_one_letter_words
logger = logging.getLogger('django')

def check_spelling(page, settings):
    language = 'en' if 'lang' not in settings else settings['lang']
    article = get_article(page, settings)
    custom_known_words = [] if 'known_words' not in settings else settings['known_words']
    dictionary = set(list(get_extended_dictionary()) + list(custom_known_words))
    if article.text:
        raw_text = '%s. %s' % (article.title, article.text)
        misspelled = get_misspelled_words(raw_text, language, dictionary)
        found_misspellings = len(misspelled) > 0
        message = 'No misspellings found' if not found_misspellings else 'Found %s misspelling(s): "%s"' % (len(misspelled), '", "'.join(misspelled))
        return (found_misspellings, message, {'misspelled_words': misspelled})
    return (False, 'No article found', {})


def is_in_dictionary(word, dictionary):
    if len(word) == 1:
        if word.lower() in valid_one_letter_words:
            return True
    else:
        return word in dictionary


def get_simplification_options(word):
    suffixes = [
     {'able': ''},
     {'acy': ''},
     {'ant': ''},
     {'al': ''},
     {'ance': ''},
     {'ate': ''},
     {'bed': ''},
     {'bility': ''},
     {'bility': 'ble'},
     {'bio': ''},
     {'dom': ''},
     {'cced': 'c'},
     {'cces': 'c'},
     {'ccing': 'c'},
     {'dded': 'd'},
     {'ddes': 'd'},
     {'dding': 'd'},
     {'ed': ''},
     {'ed': 'e'},
     {'ee': ''},
     {'en': ''},
     {'en': 'e'},
     {'ence': ''},
     {'ence': 'e'},
     {'ent': ''},
     {'er': ''},
     {'er': 'e'},
     {'erizer': ''},
     {'es': ''},
     {'es': 'e'},
     {'esque': ''},
     {'est': ''},
     {'ffed': 'f'},
     {'ffes': 'f'},
     {'ffing': 'f'},
     {'ful': ''},
     {'fy': ''},
     {'gged': 'g'},
     {'gges': 'g'},
     {'gging': 'g'},
     {'hood': ''},
     {'ible': ''},
     {'ic': ''},
     {'ical': ''},
     {'ied': ''},
     {'ied': 'y'},
     {'ier': ''},
     {'ier': 'y'},
     {'ies': ''},
     {'ies': 'y'},
     {'iest': ''},
     {'iest': 'y'},
     {'ify': ''},
     {'ily': ''},
     {'iness': ''},
     {'iness': 'y'},
     {'ing': ''},
     {'ing': 'e'},
     {'ious': ''},
     {'ise': ''},
     {'ish': ''},
     {'ism': ''},
     {'ist': ''},
     {'ity': ''},
     {'ity': 'y'},
     {'ive': ''},
     {'ize': ''},
     {'izer': ''},
     {'jjed': 'j'},
     {'jjes': 'j'},
     {'jjing': 'j'},
     {'kked': 'k'},
     {'kkes': 'k'},
     {'kking': 'k'},
     {'less': ''},
     {'like': ''},
     {'lled': 'l'},
     {'lles': 'l'},
     {'lling': 'l'},
     {'long': ''},
     {'ly': ''},
     {'mate': ''},
     {'ment': ''},
     {'mmed': 'm'},
     {'mmes': 'm'},
     {'mming': 'm'},
     {'ness': ''},
     {'nned': 'n'},
     {'nnes': 'n'},
     {'nning': 'n'},
     {'ologist': ''},
     {'ologist': 'ology'},
     {'ous': ''},
     {'ped': ''},
     {'pped': 'p'},
     {'ppes': 'p'},
     {'pping': 'p'},
     {'qqed': 'q'},
     {'qqes': 'q'},
     {'qqing': 'q'},
     {'red': ''},
     {'red': 're'},
     {'rred': 'r'},
     {'rres': 'r'},
     {'rring': 'r'},
     {'s': ''},
     {'sion': ''},
     {'ssed': 's'},
     {'sses': 's'},
     {'ssing': 's'},
     {'tion': ''},
     {'tion': 'te'},
     {'tize': ''},
     {'tize': 'ty'},
     {'tize': 't'},
     {'tted': 't'},
     {'ttes': 't'},
     {'tting': 't'},
     {'ty': ''},
     {'vved': 'v'},
     {'vves': 'v'},
     {'vving': 'v'},
     {'ward': ''},
     {'wards': ''},
     {'wide': ''},
     {'wise': ''},
     {'worthy': ''},
     {'y': ''},
     {'zzed': 'z'},
     {'zzes': 'z'},
     {'zzing': 'z'}]
    prefixes = [
     {'ante': ''},
     {'anti': ''},
     {'auto': ''},
     {'bi': ''},
     {'bio': ''},
     {'bis': ''},
     {'co': ''},
     {'de': ''},
     {'dis': ''},
     {'en': ''},
     {'ex': ''},
     {'extra': ''},
     {'hyper': ''},
     {'ig': ''},
     {'im': ''},
     {'in': ''},
     {'inter': ''},
     {'ir': ''},
     {'macro': ''},
     {'mal': ''},
     {'mega': ''},
     {'micro': ''},
     {'mini': ''},
     {'mis': ''},
     {'mono': ''},
     {'multi': ''},
     {'neo': ''},
     {'neuro': ''},
     {'non': ''},
     {'omni': ''},
     {'over': ''},
     {'penta': ''},
     {'per': ''},
     {'poly': ''},
     {'post': ''},
     {'pre': ''},
     {'pro': ''},
     {'quad': ''},
     {'re': ''},
     {'retro': ''},
     {'semi': ''},
     {'socio': ''},
     {'sub': ''},
     {'super': ''},
     {'tran': ''},
     {'tri': ''},
     {'un': ''},
     {'under': ''},
     {'uni': ''}]
    suffixes.sort(key=(lambda s: len(next(iter(s)))))
    suffixes.reverse()
    prefixes.sort(key=(lambda s: len(next(iter(s)))))
    prefixes.reverse()
    output = []
    for prefix_item in prefixes:
        prefix = next(iter(prefix_item))
        if word.startswith(prefix):
            output.append({'type':'prefix', 
             'search':prefix, 
             'replace':prefix_item[prefix]})

    for suffix_item in suffixes:
        suffix = next(iter(suffix_item))
        if word.endswith(suffix):
            output.append({'type':'suffix', 
             'search':suffix, 
             'replace':suffix_item[suffix]})

    return output


def apply_simplification(word, simplification):
    if simplification['type'] == 'prefix':
        if word.startswith(simplification['search']):
            word = simplification['replace'] + word[len(simplification['search']):]
    if simplification['type'] == 'suffix':
        if word.endswith(simplification['search']):
            word = word[:-len(simplification['search'])] + simplification['replace']
    return word


def simplify_word(word, dictionary, debug=False):
    log_level = logging.WARNING if debug else logging.DEBUG
    logger.log(log_level, '\n--------- Simplifying %s ---------' % word)
    possible_simplifications = get_simplification_options(word)
    logger.log(log_level, 'Possible simplifications: %s ' % possible_simplifications)
    if len(possible_simplifications) == 0:
        logger.log(log_level, 'No more simplification options found, returning %s' % word)
        return word
    for simplification in possible_simplifications:
        applied = apply_simplification(word, simplification)
        logger.log(log_level, 'Applied simplification %s replaced --> %s' % (simplification, applied))
        if is_in_dictionary(applied, dictionary):
            logger.log(log_level, 'Simplification yielded valid word %s' % applied)
            return applied
            drilled_down = simplify_word(applied, dictionary, debug)
            if is_in_dictionary(drilled_down, dictionary):
                logger.log(log_level, 'Drilled down yielded valid word %s' % drilled_down)
                return drilled_down

    return word


def remove_emails(input):
    return re.sub('\\S*@\\S*\\s?', ' ', input)


def remove_hashes(input):
    return re.sub('#(\\w+)', ' ', input)


def remove_phonenumbers(input):
    intl_removed = re.sub('(\\d{1,3}[-\\.\\s]??\\d{3}[-\\.\\s]??\\d{3}[-\\.\\s]??\\d{4}|\\(\\d{3}\\)\\s*\\d{3}[-\\.\\s]??\\d{4}|\\d{3}[-\\.\\s]??\\d{4})', ' ', input)
    us_removed = re.sub('(\\d{1,3}[-\\.\\s]??\\d{3}[-\\.\\s]??\\d{3}[-\\.\\s]??\\d{4}|\\(\\d{3}\\)\\s*\\d{3}[-\\.\\s]??\\d{4}|\\d{3}[-\\.\\s]??\\d{4})', ' ', intl_removed)
    return us_removed


def remove_urls(input):
    removed_full_links = re.sub('(http|https|ftp|telnet):\\/\\/[\\w\\-_]+(\\.[\\w\\-_]+)+([\\w\\-\\.,@?^=%&amp;:/~\\+#]*[\\w\\-\\@?^=%&amp;/~\\+#])?', ' ', input)
    remove_partial_links = re.sub('([\\w\\.]+\\.(?:com|org|net|us|co|edu|gov|uk)[^,\\s]*)', ' ', removed_full_links)
    remove_mailtos = re.sub('((mailto\\:|(news|(ht|f)tp(s?))\\://){1}\\S+)', ' ', remove_partial_links)
    ips_removed = re.sub('\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b', ' ', remove_mailtos)
    intl_removed = re.sub('(tel):(\\+[0-9]+\\s*)?(\\([0-9]+\\))?[\\s0-9\\-]+[0-9]+', ' ', ips_removed)
    us_removed = re.sub('(tel):(\\d{3}[-\\.\\s]??\\d{3}[-\\.\\s]??\\d{4}|\\(\\d{3}\\)\\s*\\d{3}[-\\.\\s]??\\d{4}|\\d{3}[-\\.\\s]??\\d{4})', ' ', intl_removed)
    filenames_removed = re.sub('([\\w\\d\\-.]+\\.(pdf|PDF|doc|DOC|docx|DOCX|zip|ZIP|xlsx|XLSX|csv|CSV))', ' ', us_removed)
    return filenames_removed


def remove_acronyms(input):
    return re.sub('\\b[A-Z\\.]{2,}s?\\b', '', input)


def remove_direct_quotation_brackets(input):
    return input.replace('[', '').replace(']', '')


def get_misspelled_words(raw_text, language, dictionary, debug=False):
    log_level = logging.WARNING if debug else logging.DEBUG
    logger.log(log_level, '>> raw_text:')
    logger.log(log_level, raw_text)
    urls_removed = remove_urls(raw_text)
    emails_removed = remove_emails(urls_removed)
    hashes_removed = remove_hashes(emails_removed)
    phonenumbers_removed = remove_phonenumbers(hashes_removed)
    logger.log(log_level, '>> after email, hashes, urls, phone numbers removed:')
    logger.log(log_level, phonenumbers_removed)
    typographic_translation_table = dict([(ord(x), ord(y)) for x, y in zip("‘’´'“”–-—⁃‐…●•∙©", '\'\'\'\'""-----.----')])
    typography_removed = phonenumbers_removed.translate(typographic_translation_table)
    hyphens_removed = typography_removed.replace('-', ' ').replace('/', ' ')
    newlines_removed = hyphens_removed.replace('\n', ' ').replace('\r', ' ')
    logger.log(log_level, '>> after fancy typographic characters and newlines removed:')
    logger.log(log_level, newlines_removed)
    contractions_removed = contractions.fix(newlines_removed)
    possessives_removed = re.sub("'s ", ' ', contractions_removed)
    hyphens_removed = possessives_removed.replace('-', ' ')
    acronyms_removed = remove_acronyms(hyphens_removed)
    whitespace_condensed = re.sub('[ \t]+', ' ', acronyms_removed.replace('\u200b', ' '))
    logger.log(log_level, '>> after contractions, posessives, hyphens and acronyms removed:')
    logger.log(log_level, whitespace_condensed)
    check_words_raw = whitespace_condensed.split(' ')
    logger.log(log_level, '>> check_words_raw:')
    logger.log(log_level, check_words_raw)
    stop_words = set(stopwords.words('english'))
    stopwords_removed = [word for word in check_words_raw if word.lower() not in stop_words]
    logger.log(log_level, '>> stopwords_removed:')
    logger.log(log_level, stopwords_removed)
    normalzized_words = [unicodedata.normalize('NFKC', word) for word in stopwords_removed]
    punctuation_removed = [remove_direct_quotation_brackets(word.strip(punctuation)) for word in normalzized_words if word if not word[0].isdigit()]
    punctuation_removed = [remove_direct_quotation_brackets(word.strip(punctuation)) for word in punctuation_removed if word if not word[0].isdigit()]
    logger.log(log_level, '>> punctuation_removed:')
    logger.log(log_level, punctuation_removed)
    remove_empty_words = [word for word in punctuation_removed if word]
    proper_nouns = []
    for word in remove_empty_words:
        if word[0].isupper():
            is_in_dictionary(simplify_word(word.lower(), dictionary), dictionary) or proper_nouns.append(word.strip(punctuation))

    proper_nouns_lower = [word.lower() for word in proper_nouns]
    logger.log(log_level, '>> proper_nouns:')
    logger.log(log_level, proper_nouns)
    remove_proper_nounds = [item for item in remove_empty_words if item.lower() not in proper_nouns_lower]
    check_words = list(set(remove_proper_nounds))
    logger.log(log_level, '>> check_words:')
    logger.log(log_level, check_words)
    words_not_in_dict = [word for word in check_words if not is_in_dictionary(word.lower(), dictionary)]
    logger.log(log_level, '>> words_not_in_dict:')
    logger.log(log_level, words_not_in_dict)
    spell = SpellChecker(language=language, distance=1)
    unknown = [item for item in list(spell.unknown(words_not_in_dict))]
    logger.log(log_level, '>> unknown:')
    logger.log(log_level, unknown)
    misspelled = []
    for word in unknown:
        simplified_word = simplify_word(word, dictionary)
        if not is_in_dictionary(simplified_word, dictionary):
            misspelled.append(simplified_word)

    logger.log(log_level, '>> misspelled:')
    logger.log(log_level, misspelled)
    return misspelled