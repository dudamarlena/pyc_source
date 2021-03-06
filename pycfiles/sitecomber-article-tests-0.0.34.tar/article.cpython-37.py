# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nina/Documents/Sites/sitecomber-article-tests/sitecomber_article_tests/utils/article.py
# Compiled at: 2019-07-29 16:20:21
# Size of source mod 2**32: 3172 bytes
import re, logging
from newspaper import Article
from newspaper.utils import get_available_languages
import readtime
logger = logging.getLogger('django')

def get_article(page, settings):
    url = page.url
    html = page.last_text_content
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
        if not article.authors:
            messages.append('WARNING: Aricle missing authors.')
            status = 'warning'
        if not article.publish_date:
            messages.append('WARNING: Aricle missing publish date.')
            status = 'warning'
        data = {'article': {'text':article.text, 
                     'title':article.title, 
                     'authors':article.authors, 
                     'publish_date':None if not article.publish_date else article.publish_date.isoformat(), 
                     'top_image':article.top_image, 
                     'imgs':list(article.imgs)}}
    else:
        messages.append('Page missing a structured article.')
        status = 'error'
    message = ' '.join(messages)
    return (reader_view_enabled, status, message, data)


def get_placeholder_words(input_text, placeholder_words):
    placeholder_words_found = []
    for placeholder_string in placeholder_words:
        matches = re.finditer('\\b%s\\b' % placeholder_string, input_text, re.IGNORECASE)
        for match in matches:
            placeholder_words_found.append(match.group(0))

    return placeholder_words_found


def contains_placeholder_text(page, settings, placeholder_words):
    article = get_article(page, settings)
    data = {'placeholder_words_searched':placeholder_words, 
     'placeholder_words_found':[]}
    placeholder_words_found = get_placeholder_words('%s %s' % (article.title, article.text), placeholder_words)
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