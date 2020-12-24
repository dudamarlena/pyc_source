# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sphinx/webtools/search_tools.py
# Compiled at: 2012-06-03 19:34:48
import os
from genshi import XML
from sphinx.webtools.pickler_tools import get_pickler

def highlight(content, words):
    """Tricky function to highlight search result in a page using <a> tag and
    class find. Old fashion parsing way explode the html tags and content and
    rebuild everything at the end with the tags for highlihting.

    @param content: content we want to highlight
    @type content: str

    @param words: words to be highlighted in the content
    @type words: str
    """
    try:
        content_result = ''
        content_right = content.split('>')
        for ct_r in content_right:
            content_left = ct_r.split('<')
            if len(content_left) == 2:
                content_left[0] = content_left[0].replace(words, '<a class="find">%s</a>' % words)
                content_result += content_left[0]
                content_result += '<%s>' % content_left[1]

        return content_result
    except:
        return content


def search_in_file(doc_dir, file, title, words, result):
    """Search words in a source file and update the current result.

    @param doc_dir: web documention directory
    @type doc_dir: str

    @param file: file name base to study
    @type file: str

    @param title: title of the current studied file
    @type type: str

    @param words: list of words to search in the file
    @type words: list

    @param result: current result to update
    @type: dict
    """
    file_name = '%s.txt' % file
    file_path = os.path.join(doc_dir, '_sources', file_name)
    file_ = open(file_path)
    for line in file_.readlines():
        line = line.lower()
        update = False
        if not line.find(words) == -1:
            if not update:
                line = line.replace('>', '&gt;')
                line = line.replace('<', '&lt;')
                line = '<div>%s</div>\n' % line
            line = line.replace(words, '<a class="find" id="find">%s</a>' % words)
            update = True
        if update:
            if result.has_key(file):
                result[file]['lines'].append(XML(line))
            else:
                result[file] = {'title': title, 'lines': [
                           XML(line)]}

    file_.close()


def do_search(doc_dir, words):
    """Search first path. Do search in each documentation files using the
    *search_in_file* method.

    @param doc_dir: web documention directory
    @type doc_dir: str

    @param words: list of words to search in the documentation
    @type words: list
    """
    menu_pickler = get_pickler(doc_dir, 'searchindex.pickle')
    links = list()
    result = dict()
    for index, file in enumerate(menu_pickler['filenames']):
        title = menu_pickler['titles'][index]
        title = title.replace('&#8217;', "'")
        search_in_file(doc_dir, file, title, words, result)

    if len(result) > 0:
        return result
    else:
        return
        return


def search(base_url, doc_dir, words):
    """Does search il the source file of the project documentation and format a
    result result for an HTML simple render.

    @param base_url: project base url
    @type base_url: str

    @param doc_dir: web documention directory
    @type doc_dir: str

    @param words: list of words to search in the documentation
    @type words: list
    """
    result_words = do_search(doc_dir, words)
    if not result_words:
        return None
    else:
        result = list()
        for src_key in result_words.keys():
            search_words = words.replace(' ', '+')
            url = '%s?action=view' % base_url
            url += '&item=%s' % src_key
            url += '&search_words=%s' % search_words
            result.append({'url': url, 
               'title': result_words[src_key]['title'], 
               'lines': result_words[src_key]['lines']})

        return result