# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/quizdrill/builder.py
# Compiled at: 2007-05-21 10:31:05
from SaDrill import SaDrill
from xml import sax
from xml.sax.handler import ContentHandler
import re, sys, os.path
from pkg_resources import resource_filename
import locale, gettext
_ = gettext.gettext
APP = 'quizdrill'
DIR = resource_filename(__name__, 'data/locale')
if not os.path.exists(DIR):
    DIR = '/usr/share/locale'
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

class AbstractQuizBuilder:
    """
    Implements the appending of the Quiz-data to the .drill-file.
    """
    __module__ = __name__

    def __init__(self, category_filter=None, question_filter=None, answer_filter=None):
        self.quiz_dict = {}
        filter_dict = {'brackets': self.filter_brackets, None: self.filter_echo}
        self.category_filter = filter_dict[category_filter]
        self.question_filter = filter_dict[question_filter]
        self.answer_filter = filter_dict[answer_filter]
        return

    def write_quiz_data(self):
        """
        Append the quiz-data to the .drill-file.
        """
        str = ''
        for cat in self.quiz_dict.keys():
            str += '\n\n\n[' + self.category_filter(cat) + ']\n'
            for question in self.quiz_dict[cat]:
                str += '\n' + self.question_filter(question[0]) + ' = ' + self.answer_filter(question[1])

        self.append_file.write(str)

    def filter_echo(self, text):
        """
        Simple pass-through filter.
        """
        return text

    def filter_brackets(self, text):
        """
        Remove brackets as they often contain extra information, that isn't
        provided on all articles (so the user can't know when to type it and
        when not) and often not what the user wants to be tested on (e.g. 
        city name in a different language, which might not be (easily) typable.
        """
        text = re.compile('\\(.*?\\)').sub('', text)
        text = re.compile('\\{.*?\\}').sub('', text)
        text = re.compile('\\[.*?\\]').sub('', text)
        return text


class AbstractMediaWikiHandler(ContentHandler):
    """
    Processes a MediaWiki pages-articles.xml Database Backup dump[1] and 
    passes the article and title to separate_article implemented by a child.

    [1]: http://meta.wikimedia.org/wiki/Data_dumps
    """
    __module__ = __name__

    def __init__(self, encoding='utf-8'):
        self.encoding = 'utf-8'
        self.DATA_FIELD = 'text'
        self.TITLE_FIELD = 'title'
        self.in_data_field = False
        self.in_title_field = False
        self.content = ''
        self.title = ''

    def parse(self, file):
        sax.parse(file, self)
        self.write_quiz_data()

    def startElement(self, name, attr):
        """
        Remember if we are in an xml-element of interest (title_field or
        data_field).
        """
        if name == self.DATA_FIELD:
            self.in_data_field = True
            self.content = ''
        if name == self.TITLE_FIELD:
            self.in_title_field = True
            self.title = ''

    def endElement(self, name):
        """
        Tracks whether we leave our xml-element of interest (title_field or 
        data_field) and processes the article if we leave data_field.
        """
        if name == self.DATA_FIELD:
            self.in_data_field = False
            if self.content:
                self.separate_article(self.content)
        if name == self.TITLE_FIELD:
            self.in_title_field = False

    def characters(self, content):
        """
        Records the content if we are in an xml-element of interest
        (title_field or data_field).
        """
        if self.in_data_field:
            self.content += unicode.encode(content, self.encoding)
        if self.in_title_field:
            self.title += unicode.encode(content, self.encoding)

    def separate_article(self, content):
        """
        Needs to be implemented by the child. Processes the actual article.
        """
        print 'Warning: "separate_article" should not be called on AbstractWikipediaHandler.'


class WikipediaArticleHandler(AbstractMediaWikiHandler, AbstractQuizBuilder):
    """
    Processes a MediaWiki database_dump (see class AbstractMediaWikiHandler),
    extracts data from the categories and named-templates (e.g. infoboxes
    and personendaten) and generates a .drill-file from it.
    """
    __module__ = __name__

    def __init__(self, append_file, template_tag, category_tag, question_tag, answer_tag, category_filter=None, question_filter=None, answer_filter=None, one_of_categories=[], encoding='utf-8', wiki_cat_namespace=['category']):
        AbstractMediaWikiHandler.__init__(self, encoding)
        AbstractQuizBuilder.__init__(self, category_filter, question_filter, answer_filter)
        self.append_file = open(append_file, 'a')
        self.re_flags = re.DOTALL | re.IGNORECASE
        self.template_tag = re.compile(' ').sub('[\\s_]', template_tag)
        self.wiki_cat_namespace = wiki_cat_namespace
        self.category_tag = category_tag
        self.question_tag = question_tag
        self.answer_tag = answer_tag
        self.one_of_categories = one_of_categories

    def separate_article(self, text):
        """
        Extract data out of a given article. Currently templates and categories
        are supported.
        """
        template_start = '\\{\\{\\S*:?' + self.template_tag
        template_body = '[^{]*'
        template_end = '\\}\\}'
        nested_template_body = '[^}]*'
        dict = {'_article': self.title.strip(), '_cat': []}
        for cat in self.wiki_cat_namespace:
            cat_re = re.compile('\\[\\[' + cat + ':([^|\\]]*)\\|?.*?\\]\\]', self.re_flags)
            dict['_cat'].extend([ cat for cat in cat_re.findall(text) ])

        self.select_one_of_categories(dict)
        unnested_template_re = re.compile(template_start + template_body + template_end, self.re_flags)
        nested_template_re = re.compile(template_start + nested_template_body + template_start, self.re_flags)
        comments_re = re.compile('<!--.*?-->', self.re_flags)
        text = comments_re.sub('', text)
        if nested_template_re.search(text):
            print _('Warning: Skipping nested templates in "%s".') % self.title
        for infobox in unnested_template_re.findall(text):
            infobox_dict = self.separate_infobox(infobox)
            infobox_dict.update(dict)
            self.append_template_to_quiz_data(infobox_dict)

    def select_one_of_categories(self, article_dict):
        """
        Generate the 'select_one_categories' values from the dictionary of
        the current wikipedia-page beeing processed.
        """
        categories = article_dict['_cat']
        for cat_list in self.one_of_categories:
            for cat in cat_list[1:]:
                if cat in categories:
                    article_dict[cat_list[0]] = cat
                    break
            else:
                article_dict[cat_list[0]] = '_None_of' + cat_list[0]

    def separate_infobox(self, infobox):
        """
        Extract data out of a template (e.g. a infobox or personendaten).
        """
        text = self.remove_links(infobox)
        text = re.compile('\\|*[\\s_]*\\}\\}').sub('', text)
        text = re.compile('\n').sub('', text)
        tag_list = text.split('|')
        dict = {'_head': tag_list[0].strip()[3:]}
        for tag in tag_list[1:]:
            L = tag.split('=', 1)
            if len(L) == 2:
                dict[L[0].strip()] = self.simple_white_spaces(L[1]).strip()
            elif len(L) == 1 and not L[0].strip():
                pass
            else:
                print _('Warning: No parameter name in Infobox row "%(para)s" in article "%(article)s".') % {'para': L, 'article': self.title}

        return dict

    def remove_links(self, text):
        """
        Removes wikistructures, which often cause problems beacause they 
        contain "|" or "=": Weblinks (URLs sometimes have a "="), Images,
        Wikilinks, Sources (ref-sections) and XML tags (assigning attributes 
        have "=") as well as '' '' (kursiv) and ''' ''' (bold).
        """
        text = re.compile('<ref>[^|<>]*?</ref>', self.re_flags).sub('', text)
        text = re.compile('<include>[^|<>]*?</include>', self.re_flags).sub('', text)
        text = re.compile('<[^|]*?>', self.re_flags).sub('', text)
        text = re.compile('\\[\\[([^|\\]]*\\|){2,}[^|\\]]*\\]\\]', self.re_flags).sub('', text)
        text = re.compile('\\[\\[[^|\\]]*?\\|?([^|\\]]*)\\]\\]', self.re_flags).sub('\\1', text)
        text = re.compile('\\[[^ |\\]]+ ?([^|\\]]*?)\\]').sub('\\1', text)
        text = re.compile("'''(.*?)'''").sub('\\1', text)
        text = re.compile("''(.*?)''").sub('\\1', text)
        return text

    def simple_white_spaces(self, text):
        """
        Convert wiki-white-spaces into " ".
        """
        return re.compile('([\\s_\\n]|&nbsp;)+').sub(' ', text)

    def append_template_to_quiz_data(self, dict):
        """
        Generate the quiz_data from a mediawiki-template (as a dictionary) and 
        append it to self.quiz_dict.
        """
        if self.category_tag in dict:
            cat = dict[self.category_tag]
        else:
            cat = ''
            if self.category_tag != '':
                print _('Warning: Parameter "%(para)s" missing in a template in article "%(article)s", using "" instead.') % {'para': self.category_tag, 'article': dict['_article']}
        if self.question_tag in dict:
            question = dict[self.question_tag]
        else:
            print _('Warning: Parameter "%(para)s" missing in a template in article "%(article)s", skipping.') % {'para': self.question_tag, 'article': dict['_article']}
            return
        if self.answer_tag in dict:
            answer = dict[self.answer_tag]
        else:
            print _('Warning: Parameter "%(para)s" missing in a template in article "%(article)s", skipping.') % {'para': self.answer_tag, 'article': dict['_article']}
            return
        if cat not in self.quiz_dict:
            self.quiz_dict[cat] = [
             [
              question, answer]]
        else:
            self.quiz_dict[cat].append([question, answer])


class DrillBuilder(SaDrill):
    """
    Processes a .drill.builder-file and outputs a .drill-file.

    Note: Still too specific to WikipediaArtikel builder-tags.
    """
    __module__ = __name__

    def __init__(self):
        tag_dict = {'build_to': self.on_tag_build_to, 'builder': self.on_tag_builder, 'filter': self.on_tag_filter, 'one_of_categories': self.on_tag_one_of_categories, 'wiki_cat_namespace': self.on_tag_wiki_cat_namespace}
        mandatory_tags = [
         'build_to', 'builder']
        SaDrill.__init__(self, {}, tag_dict, {}, mandatory_tags)
        self.encoding = 'utf-8'
        self.one_of_categories = []

    def convert_drill_file(self, file, database):
        """
        Build a .drill-file from a .builder discription-file and a wikipedia-
        xml-dumpfile.
        """
        file_out = file.replace('.builder', '') + '.original'
        self._fout = open(file_out, 'w')
        self._init_default_values()
        self.parse(file)
        self._fout.close()
        builder = self.builder_class(file_out, self.template_tag, self.category_tag, self.question_tag, self.answer_tag, self.category_filter, self.question_filter, self.answer_filter, self.one_of_categories, self.encoding, self.wiki_cat_namespace)
        builder.parse(database)

    def _init_default_values(self):
        """
        Set default values for tags that don't have to be listed in a 
        .builder-file.
        """
        self.category_tag = [
         'category']
        self.category_filter = self.question_filter = self.answer_filter = None
        self.one_of_categories = []
        self.encoding = 'utf-8'
        self.wiki_cat_namespace = ['category']
        return

    def on_default_head_tag(self, as_text, word_pair=None, tag=None, type='#'):
        """
        Writes header-lines unfiltered to the new .drill-file.
        """
        self._fout.write(as_text + '\n')

    def on_tag_builder(self, as_text, word_pair, tag='builder', type='$'):
        builder_dict = {'WikipediaArticle': WikipediaArticleHandler}
        assert len(word_pair) == 2, _('Error: Tag $builder does not have exactly one "=".')
        assert word_pair[0] in builder_dict, _('Error: Unknown builder "%s".') % tag
        self.builder_class = builder_dict[word_pair[0]]
        self.template_tag = word_pair[1]

    def on_tag_build_to(self, as_text, word_pair, tag='build_to', type='$'):
        assert len(word_pair) == 3, _('Error: Tag $build_to does not have exactly two "=".')
        self.category_tag = word_pair[0]
        self.question_tag = word_pair[1]
        self.answer_tag = word_pair[2]

    def on_tag_filter(self, as_text, word_pair, tag='filter', type='$'):
        while len(word_pair) > 3:
            word_pair.append(None)

        self.category_filter = word_pair[0]
        self.question_filter = word_pair[1]
        self.answer_filter = word_pair[2]
        return

    def on_tag_wiki_cat_namespace(self, as_text, word_pair, tag='wiki_cat_namespace', type='$'):
        self.wiki_cat_namespace = word_pair

    def on_tag_one_of_categories(self, as_text, word_pair, tag='one_of_categories', type='$'):
        self.one_of_categories.append(word_pair)


def build():
    """
    A console script for our endusers. 
    """
    builder = DrillBuilder()
    if len(sys.argv) == 3:
        builder.convert_drill_file(sys.argv[1], sys.argv[2])
    else:
        print _('Usage: %s [.drill.builder-file] [wikipedia.xml-file]') % sys.argv[0]


if __name__ == '__main__':
    build()