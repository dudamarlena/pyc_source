# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nina/Documents/Sites/sitecomber-article-tests/sitecomber_article_tests/utils.py
# Compiled at: 2019-07-24 00:48:29
# Size of source mod 2**32: 16860 bytes
import logging, re
from string import punctuation
from newspaper import Article
from newspaper.utils import get_available_languages
import nltk.data
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import SnowballStemmer
import contractions, readtime
from spellchecker import SpellChecker
from .dictionary import core_dictionary
logger = logging.getLogger('django')

def get_article(page, settings):
    url = page.url
    html = page.latest_request.response.text_content
    language = 'en' if 'lang' not in settings else settings['lang']
    if language not in get_available_languages():
        logger.error("Language %s not found. Defaulting to 'en' instead." % language)
        language = 'en'
    article = Article(url=url, language=language)
    article.download(html)
    article.parse()
    return article


def is_reader_view_enabled(page, settings):
    article = get_article(page, settings)
    reader_view_enabled = False
    messages = []
    data = {}
    if article.text and article.title:
        status = 'success'
        reader_view_enabled = True
        messages.append('Page contains properly structured article.')
        if not article.top_image:
            messages.append('WARNING: Aricle missing top image.')
            status = 'warning'
        if not article.top_image:
            messages.append('WARNING: Aricle missing authors.')
            status = 'warning'
        data = {'article': {'text':article.text, 
                     'title':article.title, 
                     'authors':article.authors, 
                     'publish_date':article.publish_date, 
                     'top_image':article.top_image, 
                     'imgs':list(article.imgs)}}
    else:
        messages.append('Page missing a structured article.')
        status = 'error'
    message = ' '.join(messages)
    return (reader_view_enabled, status, message, data)


def contains_placeholder_text(page, settings):
    article = get_article(page, settings)
    placeholder_words = ['lorem', 'ipsum'] if 'placeholder_words' not in settings else settings['placeholder_words']
    data = {'placeholder_words_searched':placeholder_words,  'placeholder_words_found':[]}
    placeholder_words_found = []
    if article.text:
        text_lower = article.text.lower() + article.title.lower()
        for placeholder_string in placeholder_words:
            if placeholder_string in text_lower:
                placeholder_words_found.append(placeholder_string)

    data['placeholder_words_found'] = placeholder_words_found
    if len(placeholder_words_found) > 0:
        return (
         True, 'Found placeholder word(s): "%s"' % '", "'.join(placeholder_words_found), data)
    message = 'No placeholder text "%s" found.' % '", "'.join(placeholder_words)
    return (False, message, data)


def get_article_readtime(page, settings):
    article = get_article(page, settings)
    if article.text:
        result = readtime.of_text(article.text)
        return (str(result.text), {'read_time': str(result.text)})
    return ('No article found', {})


def check_spelling(page, settings):
    language = 'en' if 'lang' not in settings else settings['lang']
    article = get_article(page, settings)
    custom_known_words = [] if 'known_words' not in settings else settings['known_words']
    dictionary = set(list(core_dictionary) + list(custom_known_words))
    if article.text:
        raw_text = '%s. %s' % (article.title, article.text)
        misspelled = get_misspelled_words(raw_text, language, dictionary)
        found_misspellings = len(misspelled) > 0
        message = 'No misspellings found' if not found_misspellings else 'Found %s misspelling(s): "%s"' % (len(misspelled), '", "'.join(misspelled))
        return (found_misspellings, message, {'misspelled_words': misspelled})
    return (False, 'No article found', {})


suffixes = [
 'able', 'acy', 'al', 'ance', 'ate', 'bility', 'bio', 'dom', 'ed', 'ee', 'en', 'ence', 'er', 'erizer', 'es', 'esque', 'est', 'ful', 'fy', 'hood', 'ible', 'ic', 'ical', 'ied', 'ier', 'ies', 'iest', 'ify', 'iness', 'ing', 'ious', 'ise', 'ish', 'ism', 'ist', 'ity', 'ive', 'ize', 'izer', 'less', 'like', 'long', 'ly', 'mate', 'ment', 'ness', 'ologist', 'ous', 'pping', 'red', 'sion', 'ting', 'tion', 'tize', 'tted', 'ty', 'ward', 'wards', 'wide', 'wise', 'worthy', 'y', 'zing']
suffix_replacements = {'bility':[
  'ble'], 
 'iness':[
  'y'], 
 'ied':[
  'y'], 
 'ier':[
  'y'], 
 'ies':[
  'y'], 
 'iest':[
  'y'], 
 'ity':[
  'y'], 
 'ed':[
  'e'], 
 'es':[
  'e'], 
 'er':[
  'e'], 
 'ence':[
  'e'], 
 'ing':[
  'e'], 
 'ologist':[
  'ology'], 
 'pping':[
  'p'], 
 'red':[
  're'], 
 'tize':[
  'ty', 't'], 
 'tted':[
  't'], 
 'tion':[
  'te'], 
 'ting':[
  'te', 't'], 
 'zing':[
  'ze', 'z']}
prefixes = [
 'ante', 'anti', 'auto', 'bi', 'bio', 'bis', 'co', 'de', 'dis', 'en', 'ex', 'extra', 'hyper', 'ig', 'im', 'in', 'inter', 'ir', 'macro', 'mal', 'mega', 'micro', 'mini', 'mis', 'mono', 'multi', 'neo', 'neuro', 'non', 'omni', 'over', 'penta', 'per', 'poly', 'post', 'pre', 'pro', 'quad', 're', 'retro', 'semi', 'socio', 'sub', 'super', 'tran', 'tri', 'un', 'under', 'uni']
suffixes.sort(key=(lambda s: len(s)))
suffixes.reverse()
prefixes.sort(key=(lambda s: len(s)))
prefixes.reverse()
stop_words = set(stopwords.words('english'))
lmtzr = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer('english')

def replace_prefix(word, dictionary, debug=False):
    log_level = logging.WARNING if debug else logging.DEBUG
    for prefix in prefixes:
        if word.startswith(prefix):
            word_updated = word[len(prefix):]
            logger.log(log_level, "Attempting to remove prefix '%s' from word %s.... %s" % (prefix, word, word_updated))
            return word_updated

    return word


def replace_suffix(word, dictionary, debug=False):
    log_level = logging.WARNING if debug else logging.DEBUG
    for suffix in suffixes:
        print('Does %s end with %s? %s' % (word, suffix, word.endswith(suffix)))
        if word.endswith(suffix):
            word_updated = word[0:-len(suffix)]
            logger.log(log_level, "Attempting to remove suffix '%s' from word %s....%s" % (suffix, word, word_updated))
            if word_updated in dictionary:
                logger.log(log_level, "Removing suffix '%s' from word %s: %s --> %s" % (suffix, word, word_updated, word_updated in dictionary))
                return word_updated
            if suffix in suffix_replacements:
                for suffix_replacement in suffix_replacements[suffix]:
                    replaced = word.replace(suffix, suffix_replacement)
                    logger.log(log_level, "Attempting to replace suffix '%s' with '%s' to get %s" % (suffix, suffix_replacement, replaced))
                    if replaced in dictionary:
                        logger.log(log_level, "Removing suffix '%s' from word %s: %s --> %s" % (suffix, word, replaced, replaced in dictionary))
                        return replaced

    return word


def simplify_word_pass(word, dictionary, pattern, debug=False):
    log_level = logging.WARNING if debug else logging.DEBUG
    logger.log(log_level, '---- Applying simplification pattern: %s' % pattern)
    for item in pattern:
        logger.log(log_level, '----> %s (word currently %s)' % (item, word))
        if item == 's':
            if word.endswith('s'):
                word = word[0:-1]
                if word in dictionary:
                    logger.log(log_level, 'Singularization replaced to get valid word %s' % word)
                    return word
            elif item == 'x':
                word = replace_suffix(word, dictionary, debug)
                if word in dictionary:
                    logger.log(log_level, 'Suffix replaced to get valid word %s' % word)
                    return word
            elif item == 'p':
                word = replace_prefix(word, dictionary, debug)
                if word in dictionary:
                    logger.log(log_level, 'Prefix replaced to get valid word %s' % word)
                    return word
            elif item == 'l':
                lemmatized = lmtzr.lemmatize(word)
                if lemmatized in dictionary:
                    logger.log(log_level, 'Lemmatizer returned valid word %s' % lemmatized)
                    return lemmatized
            elif item == 't':
                stemmed = snowball_stemmer.stem(word)
                if stemmed in dictionary:
                    logger.log(log_level, 'Stemmer returned valid word %s' % stemmed)
                    return stemmed

    return word


def simplify_word(word, dictionary, debug=False):
    log_level = logging.WARNING if debug else logging.DEBUG
    original_word = word
    logger.log(log_level, '\n--------- Simplifying %s ---------' % word)
    word = simplify_word_pass(original_word, dictionary, ['x', 'p', 's', 'x', 'p', 's', 'x', 'p', 's'], debug)
    if word in dictionary:
        return word
    word = simplify_word_pass(original_word, dictionary, ['s', 'x', 'p', 's', 'x', 'p', 's', 'x', 'p'], debug)
    if word in dictionary:
        return word
    word = simplify_word_pass(original_word, dictionary, ['p', 'x', 's', 'p', 'x', 's', 'p', 'x', 's'], debug)
    if word in dictionary:
        return word
    word = simplify_word_pass(original_word, dictionary, ['s', 'p', 'x', 's', 'p', 'x', 's', 'p', 'x'], debug)
    if word in dictionary:
        return word
    word = simplify_word_pass(original_word, dictionary, ['x', 'x', 'x', 's', 'p', 'p', 'p'], debug)
    if word in dictionary:
        return word
    word = simplify_word_pass(original_word, dictionary, ['l'], debug)
    if word in dictionary:
        return word
    word = simplify_word_pass(original_word, dictionary, ['t'], debug)
    if word in dictionary:
        return word
    logger.log(log_level, 'No simplified version found, return original %s' % original_word)
    return original_word


def remove_emails(input):
    return re.sub('\\S*@\\S*\\s?', ' ', input)


def remove_hashes(input):
    return re.sub('#(\\w+)', ' ', input)


def remove_phonenumbers(input):
    intl_removed = re.sub('(\\+[0-9]+\\s*)?(\\([0-9]+\\))?[\\s0-9\\-]+[0-9]+', ' ', input)
    us_removed = re.sub('(\\d{3}[-\\.\\s]??\\d{3}[-\\.\\s]??\\d{4}|\\(\\d{3}\\)\\s*\\d{3}[-\\.\\s]??\\d{4}|\\d{3}[-\\.\\s]??\\d{4})', ' ', intl_removed)
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


def get_misspelled_words(raw_text, language, dictionary, debug=False):
    log_level = logging.WARNING if debug else logging.DEBUG
    spell = SpellChecker(language=language, distance=1)
    logger.log(log_level, '>> raw_text:')
    logger.log(log_level, raw_text)
    urls_removed = remove_urls(raw_text)
    emails_removed = remove_emails(urls_removed)
    hashes_removed = remove_hashes(emails_removed)
    phonenumbers_removed = remove_phonenumbers(hashes_removed)
    logger.log(log_level, '>> after email, hashes, urls, phone numbers removed:')
    logger.log(log_level, phonenumbers_removed)
    typographic_translation_table = dict([(ord(x), ord(y)) for x, y in zip("‘’´'“”–-—⁃‐…●•∙", '\'\'\'\'""-----.---')])
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
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    proper_nouns = []
    for sentence in tokenizer.tokenize(whitespace_condensed):
        sentence_words = [word for word in sentence.split(' ') if word]
        for word in sentence_words:
            if word and word[0].isupper() and word.lower() not in dictionary:
                proper_nouns.append(word.strip(punctuation))

    proper_nouns_lower = [word.lower() for word in proper_nouns]
    check_words_raw = whitespace_condensed.split(' ')
    stopwords_removed = [word for word in check_words_raw if word.lower() not in stop_words]
    punctuation_removed = [word.strip(punctuation) for word in stopwords_removed if word if not re.search('\\d+', word)]
    remove_empty_words = [word for word in punctuation_removed if word]
    remove_proper_nounds = [item for item in remove_empty_words if item.lower() not in proper_nouns_lower]
    check_words = list(set(remove_proper_nounds))
    words_not_in_dict = [word for word in check_words if word.lower() not in dictionary]
    unknown = [item for item in list(spell.unknown(words_not_in_dict))]
    misspelled = []
    for word in unknown:
        simplified_word = simplify_word(word, dictionary)
        if simplified_word not in dictionary:
            misspelled.append(simplified_word)

    logger.log(log_level, '>> misspelled:')
    logger.log(log_level, misspelled)
    return misspelled