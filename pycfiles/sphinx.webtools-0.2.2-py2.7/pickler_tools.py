# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sphinx/webtools/pickler_tools.py
# Compiled at: 2012-06-03 20:14:59
import os, shutil, sys
from cPickle import Unpickler
from pkg_resources import resource_filename
from sphinx.application import Sphinx
from genshi import XML
from genshi.filters.transform import Transformer

def update_docs(source_dir, doc_dir):
    """Build the Sphinx documentation from the source_dir to the doc_dir. The
    doc_dir is previously remove. We use the *web* builder by default to obtain
    the pickle files in the doc_dir.

    @param source_dir: Sphinx source folder of the project
    @type source_dir: str

    @param doc_dir: Plugin Sphinx web folder for output
    @type doc_dir: str
    """
    try:
        if not os.path.exists(source_dir):
            msg = '<div><b>Source directory not found:</b>'
            msg += ' %s</div>' % source_dir
            return XML(msg)
    except Exception as e:
        msg = '<div><b>Source dir error:</b> %s</div>' % e
        return XML(msg)

    try:
        if os.path.exists(doc_dir):
            shutil.rmtree(doc_dir)
        os.mkdir(doc_dir)
    except Exception as e:
        msg = '<div><b>Doc dir error:</b> %s</div>' % e
        return XML(msg)

    doctree_dir = os.path.join(doc_dir, '.doctrees')
    builder_name = 'web'
    conf_overrides = {}
    fresh_env = False
    try:
        app = Sphinx(source_dir, source_dir, doc_dir, doctree_dir, builder_name, conf_overrides, sys.stdout, sys.stderr, fresh_env)
    except Exception as e:
        msg = '<div><b>Sphinx error:</b> %s</div>' % e
        return XML(msg)

    try:
        app.builder.build_all()
    except Exception as e:
        msg = '<div><b>Build error:</b> %s</div>' % e
        return XML(msg)

    return


def get_pickler(doc_dir, filename):
    """Returns the pickler object corresponding to a file from the the
    documentation source directory. Return None in case of error.

    @param doc_dir: web documention directory
    @type doc_dir: str

    @param filename: filename of the pickle file to load
    @type filename: str
    """
    try:
        pickler_path = os.path.join(doc_dir, filename)
        pickler_file = open(pickler_path, 'rb')
        pickler_obj = Unpickler(pickler_file).load()
        pickler_file.close()
        return pickler_obj
    except:
        return

    return


def reformat_xml_content(text, id_):
    """Returns text as valid XML and removes junk characters.
    """
    text = '<div class="%s">%s</div>' % (id_, text)
    text = text.replace('&#8217;', "'")
    return text


class PicklerContentManager(object):
    """Manage contents (relative links, table of content, body) from a pickler
    source. Returns content as str or XML for web integration.
    """

    def __init__(self, base_url, doc_dir, pickler_url):
        """Init the manager with given variables about documentation source and
        web base url.

        @param base_url: project base url
        @type base_url: str

        @param doc_dir: web documention directory
        @type doc_dir: str

        @param pickler_url: path to the current page pickler source
        @type pickler_url: str
        """
        self.__base_url = base_url
        pickler_filename = '%s.fpickle' % pickler_url
        self.__content_pickler = get_pickler(doc_dir, pickler_filename)

    def get_rellinks(self):
        """Returns list of relative links in the current page as XML Stream.
        """
        if not self.__content_pickler:
            return
        rellinks = self.__content_pickler['rellinks']
        result = list()
        for link in rellinks:
            try:
                link = map(str, link)
            except Exception:
                link = map(lambda v: getattr(v, '_args', (v,))[0], link)

            title = link[1].replace('&#8217;', "'")
            url = '%s?action=%s&item=%s' % (self.__base_url, link[(-1)], link[0])
            result.append({'category': link[(-1)], 
               'title': title, 
               'url': url})

        return result

    def get_toc(self):
        """Returns the table of content part of a pickler file as XML Stream.
        """
        if not self.__content_pickler:
            return
        toc = self.__content_pickler['toc']
        result = reformat_xml_content(toc, 'toc')
        return result

    def get_body(self):
        """Returns the body part of a pickler file as str.
        """
        if not self.__content_pickler:
            return
        body = self.__content_pickler['body']
        result = reformat_xml_content(body, 'body')
        return result


class ContentLinkReformatter(object):
    """XML reformatter for content sphhinx link reformatting. Transforms
    relative sphinx generated links into valid sphinx plugin url with params.
    """

    def __init__(self, base_url, doc_dir):
        """Reformatter init, set a list of the current valid documentation
        project url.

        @param base_url: project base url
        @type base_url: str

        @param doc_dir: web documention directory
        @type doc_dir: str
        """
        self.__base_url = base_url
        self.__links = None
        links_pickler = get_pickler(doc_dir, 'searchindex.pickle')
        if links_pickler:
            self.__links = links_pickler['filenames']
        return

    def __get_absolute_link(self, relative_url):
        """Build an absolute path form a relative link, ex.: '../test' ->
        'content/test' if 'content/test' exists in the previously __links list.

        @param relative_url: relative url to enhance
        @type relative_url: str
        """
        result_key = relative_url.split('../')[(-1)]
        page_in_index = None
        if not result_key.find('/#') == -1:
            key_parts = result_key.split('/#')
            result_key = key_parts[0]
            page_in_index = '#%s' % key_parts[1]
        for project_link in self.__links:
            if not project_link.find(result_key) == -1:
                if page_in_index:
                    return '%s%s' % (project_link, page_in_index)
                else:
                    return project_link

        return ''

    def __reformat_sphinx_links(self, link):
        """Builds a valid plugin link from a sphinx link, ex.: '../test/#1' ->
        'sphinx?action=view&item=content/test#1'

        @param link: relative url to reformat
        @type link: str
        """
        if link.find('http://') == 0:
            return link
        if link.startswith('#'):
            return link
        split_content = link.split('/')
        while '' in split_content:
            split_content.remove('')

        result = ('/').join(split_content)
        if not result.find('../') == -1:
            result = self.__get_absolute_link(result)
        result = '%s?action=view&item=%s' % (self.__base_url, result)
        return result.replace('/#', '#')

    def replace_sphinx_links(self, name, event):
        """Finds and replaces links in a matched tag.
        """
        attrs = event[1][1]
        if attrs.get('class') == 'reference external':
            link = attrs.get('href')
            return self.__reformat_sphinx_links(link)
        else:
            if attrs.get('class') in ('reference', 'reference internal'):
                link = attrs.get('href')
                return self.__reformat_sphinx_links(link)
            return attrs.get(name)


def reformat_content_links(base_url, doc_dir, content_xml):
    """Use genshi Transformer function to replace sphinx links in valid plugin
    links.

    @param base_url: project base url
    @type base_url: str

    @param doc_dir: web documention directory
    @type doc_dir: str

    @param content_xml: XML content to parse, using genshi Transformer function
    @type content_xml: genshi.XML
    """
    reformatter = ContentLinkReformatter(base_url, doc_dir)
    return content_xml | Transformer('.//a').attr('href', reformatter.replace_sphinx_links)


def format_entry_url(base_url, url_src):
    """Simple url reformat for plugin compliance.

    @param base_url: project base url
    @type base_url: str

    @param url_src: url to enhance
    @type url_src: str
    """
    if not len(url_src):
        return None
    else:
        base_url = '%s?action=view&item=' % base_url
        url = url_src.replace('../', base_url)
        url = url.replace('/#', '#')
        return url


def get_genentries(base_url, doc_dir):
    """Returns a list of the sphinx index entries of the project documentation.

    @param base_url: project base url
    @type base_url: str

    @param doc_dir: web documention directory
    @type doc_dir: str
    """
    content_pickler = get_pickler(doc_dir, 'genindex.fpickle')
    if not content_pickler:
        return
    entries = content_pickler['genindexentries']
    result = list()
    for entry in entries:
        links = list()
        for item in entry[1]:
            link = {'title': item[0], 
               'url': format_entry_url(base_url, item[1][0][0][1])}
            links.append(link)

        entry = {'letter': entry[0], 
           'links': links}
        result.append(entry)

    return result


def get_modentries(base_url, doc_dir):
    """Returns a list of the sphinx modules index entries of the project
    documentation.

    @param base_url: project base url
    @type base_url: str

    @param doc_dir: web documention directory
    @type doc_dir: str
    """
    content_pickler = get_pickler(doc_dir, 'py-modindex.fpickle')
    if not content_pickler:
        return
    content = content_pickler['content']
    result = list()
    for letter, entries in content:
        item = dict()
        item['letter'] = letter
        item['links'] = list()
        result.append(item)
        for entry in entries:
            link = {'title': entry[0], 
               'url': format_entry_url(base_url, '../' + entry[2])}
            item['links'].append(link)

    return result


def get_links(base_url, doc_dir):
    """Returns simple list of links to all the document pages found during the
    documentation generation.

    @param base_url: project base url
    @type base_url: str

    @param doc_dir: web documention directory
    @type doc_dir: str
    """
    menu_pickler = get_pickler(doc_dir, 'searchindex.pickle')
    if not menu_pickler:
        return
    links = list()
    for index, item in enumerate(menu_pickler[0]):
        title = menu_pickler[1][index].replace('&#8217;', "'")
        url = '%s?action=view&item=%s' % (base_url, item)
        link = {'url': url, 
           'title': title}
        links.append(link)

    return links