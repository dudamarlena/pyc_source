# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simplystatic/s2page.py
# Compiled at: 2014-01-31 13:49:30
"""This module provides functionality to manage a Page entity.

Classes included:

    - Page: Manages creation, loading, rendering, writing, etc. of
            a "page" in a site. This structure refers to the "source"
            page.

"""
import os, datetime, glob, shutil, codecs
from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO
import markdown, mdx_mathjax, util

class Page(object):
    """Represent a Page and provide tools for creation, management, etc.

    When an object of this class is created, it's necessary to pass a
    reference to a site, since a Page is created/managed/rendered in the
    context of a site.

    If a page name is passed on creation, the program will check whether
    it exists in the site. If it does, it loads the page source and
    parses it (setting the instance variables accordingly.) If it does
    not exist, it only creates the instance variables that it can.

    """

    def __init__(self, site, ptitle, isslug=False):
        """Initialize the page object created.

        Arguments:

            - ptitle: A string with the page title.

            - isslug: Boolean that indicates whether the title is a
                         "real" title (with spaces, etc.) or if it is
                         the "sanitized" version (lower case, no spaces,
                         underscores, no punctuation)

        This way of encoding the initialization parameters makes it
        easy to automatically initialize the object whether it is for
        creation of a new page, or it is to load an existing page.

        If "isslug" is omitted or false, the program assumes that we
        want to create a new page with that title (although it will
        check). It "sanitized" is true, it's supposed to be the
        reference to an existing page, and the program will try to load
        the pertinent information.

        """
        self.site = site
        self._config = None
        self._exists_on_disk = None
        self._slug = None
        self._title = None
        self._content = None
        self._dirs = {'www_dir': None, 'www_filename': None, 
           'source_dir': None, 
           'source_filename': None}
        if not isslug:
            self._create(ptitle)
        elif self.site.page_exists_on_disk(ptitle):
            self._exists_on_disk = True
            self._load(ptitle)
        else:
            raise ValueError
        return

    def __repr__(self):
        return ('\n').join([str(self._slug), str(self._title),
         str(self._content)])

    def _create(self, rawtitle):
        """Create a page with this title, if it doesn't exist.

        This method first checks whether a page with the same slug
        (sanitized name) exists_on_disk. If it does, it doesn't do anthing.
        Otherwise, the relevant attributes are created.
        Nothing is written to disc (to the source file). You must call
        the write_page method to do that. Doing it this way, after
        creation you can call a method to add random text, for example,
        before committing the page to disk.

        """
        slug = util.make_slug(rawtitle)
        if self.site.page_exists_on_disk(slug):
            raise ValueError
        self._title = rawtitle
        self._slug = slug
        self._dirs['source_dir'] = os.path.join(self.site.dirs['source'], slug)
        self._dirs['source_filename'] = os.path.join(self._dirs['source_dir'], slug + '.md')
        self._dirs['www_dir'] = os.path.join(self.site.dirs['www'], slug)
        self._dirs['www_filename'] = os.path.join(self._dirs['www_dir'], 'index.html')
        self._config = self._create_config()
        return True

    def write(self):
        """Write the s2 page to the corresponding source file.

        It always writes the (serialized) config first, and then the
        content (normally markdown). The destination file is in the
        source_dir of the site.

        """
        if not os.path.isdir(self._dirs['source_dir']):
            os.mkdir(self._dirs['source_dir'])
        fout = open(self._dirs['source_filename'], 'w')
        fout.write(self._config_to_text())
        if self._content:
            fout.write('\n')
            fout.write(self._content)
            fout.write('\n')
        fout.close()

    def rename(self, new_title):
        """Rename an existing s2 page.

        For an existing s2 page, updates the directory and file name,
        as well as the internal configuration information (since it
        contains the title and the slug)

        """
        if not isinstance(new_title, str) and not isinstance(new_title, unicode):
            raise TypeError
        new_slug = util.make_slug(new_title)
        if self.site.page_exists_on_disk(new_slug):
            raise ValueError
        shutil.rmtree(self._dirs['source_dir'])
        self._title = new_title
        self._slug = new_slug
        self._config['title'] = [self._title]
        self._config['slug'] = [self._slug]
        self._dirs['source_dir'] = os.path.join(self.site.dirs['source'], new_slug)
        self._dirs['source_filename'] = os.path.join(self._dirs['source_dir'], new_slug + '.md')
        self._dirs['www_dir'] = os.path.join(self.site.dirs['www'], new_slug)
        self.write()

    def render(self):
        """Render this page and return the rendition.

        Converts the markdown content to html, and then renders the
        (mako) template specified in the config, using that html.

        The task of writing of the rendition to a real file is
        responsibility of the generate method.

        """
        pthemedir, ptemplatefname = self._theme_and_template_fp()
        makotemplate = Template(filename=ptemplatefname, module_directory=self.site._makodir)
        md = markdown.Markdown(extensions=['meta', 'fenced_code', 'codehilite'], output_format='html5')
        page_html = md.convert(self._content)
        themepath = '../themes/' + os.path.split(pthemedir)[1] + '/'
        commonpath = '../common/'
        rendition = makotemplate.render(pageContent=page_html, isFrontPage=False, themePath=themepath, commonPath=commonpath, pageTitle=self.title)
        return rendition

    def generate(self):
        """Generate the page html file.

        Just open the destination file for writing and write the result
        of rendering this page.

        """
        generated_content = ''
        if self._config['status'][0].lower() == 'published':
            if os.path.isdir(self.dirs['www_dir']):
                shutil.rmtree(self.dirs['www_dir'])
            os.mkdir(self.dirs['www_dir'])
            sfl = glob.glob(os.path.join(self.dirs['source_dir'], '*'))
            dirlist = [ f for f in sfl if os.path.isdir(f) ]
            filelist = [ f for f in sfl if os.path.isfile(f) ]
            for f in filelist:
                if '.md' not in os.path.split(f)[1]:
                    shutil.copy(f, self.dirs['www_dir'])

            for d in dirlist:
                rfn = os.path.split(d)[1]
                if rfn != 'nowww':
                    shutil.copytree(d, os.path.join(self.dirs['www_dir'], rfn))

            generated_content = self.render()
            fout = codecs.open(self.dirs['www_filename'], 'w', encoding='utf-8', errors='xmlcharrefreplace')
            fout.write(generated_content)
            fout.close()
        return generated_content

    def set_published(self):
        """Change the page configuration to make the page 'published' """
        self._config['status'][0] = 'published'

    def _create_config(self):
        """Create the default configuration dictionary for this page."""
        configinfo = {'creation_date': [datetime.datetime.now().date().isoformat()], 'author': [
                    self.site.site_config['default_author']], 
           'status': [
                    'draft'], 
           'lang': [
                  ''], 
           'tags': [
                  ''], 
           'title': [
                   self._title], 
           'slug': [
                  self._slug], 
           'theme': [
                   ''], 
           'template': [
                      '']}
        return configinfo

    def _load(self, slug):
        """Load the page. The _file_name param is known, because this
        method is only called after having checked that the page exists.

        """
        self._slug = slug
        page_dir = os.path.join(self.site.dirs['source'], self._slug)
        page_file_name = os.path.join(page_dir, self._slug + '.md')
        self._dirs['source_dir'] = page_dir
        self._dirs['source_filename'] = page_file_name
        self._dirs['www_dir'] = os.path.join(self.site.dirs['www'], slug)
        self._dirs['www_filename'] = os.path.join(self._dirs['www_dir'], 'index.html')
        pf = codecs.open(self._dirs['source_filename'], mode='r', encoding='utf-8')
        page_text = pf.read()
        pf.close()
        self._parse_text(page_text)
        if not self._check_config():
            raise ValueError
        self._title = self._config['title'][0]

    def _check_config(self):
        """Verify that the configuration is correct."""
        required_data = [
         'creation_date',
         'author',
         'status',
         'lang',
         'tags',
         'title',
         'slug',
         'theme',
         'template']
        isok = True
        for e in self._config.keys():
            if e not in required_data:
                print "The configuration in page '" + self._slug + "' is corrupt."
                isok = False

        pthemedir, ptemplatefname = self._theme_and_template_fp()
        if not os.path.isdir(pthemedir):
            print 'Theme ' + self._config['theme'][0] + " specified in page '" + self._slug + "' does not exist."
            isok = False
        if not os.path.isfile(ptemplatefname):
            print 'Template ' + self._config['template'][0] + " specified in page '" + self._slug + "' does not exist."
            isok = False
        return isok

    def _theme_and_template_fp(self):
        """Return the full paths for theme and template in this page"""
        ptheme = self._config['theme'][0]
        if ptheme == '':
            ptheme = self.site.site_config['default_theme']
        pthemedir = os.path.join(self.site.dirs['themes'], ptheme)
        ptemplate = self._config['template'][0]
        if ptemplate == '':
            ptemplate = self.site.site_config['default_template']
        ptemplatefname = os.path.join(pthemedir, ptemplate)
        return (pthemedir, ptemplatefname)

    def _parse_text(self, page_text):
        """Extract the s2config and the content from the raw page text."""
        lines = page_text.split('\n')
        i = 0
        while lines[i].strip() == '':
            i += 1

        if i > 0:
            lines = lines[i:]
        i = 0
        while lines[i].strip() != '':
            i += 1

        cfg_lines = ('\n').join(lines[0:i + 1])
        md = markdown.Markdown(extensions=['meta', 'fenced_code', 'codehilite'], output_format='html5')
        md.convert(cfg_lines)
        self._config = md.Meta
        self._content = ('\n').join(lines[i + 1:])

    def _config_to_text(self):
        """Render the configuration as text."""
        r = ''
        for k in self._config:
            r += k + ': ' + ('\n        ').join(self._config[k]) + '\n'

        r += '\n'
        return r

    @property
    def content(self):
        """Return the content for the page (getter)"""
        return self._content

    @content.setter
    def content(self, value):
        """Set the content of the page (setter)"""
        self._content = value

    @property
    def dirs(self):
        """Return the directory information for the page (getter)"""
        return self._dirs

    @property
    def slug(self):
        """Return the slug for the page (getter)"""
        return self._slug

    @property
    def title(self):
        """Return the title for the page (getter)"""
        return self._title

    @property
    def published(self):
        """Return if the page is published or not"""
        return self._config['status'][0].lower() == 'published'

    @property
    def creation_date(self):
        """Return the date from the configuration (getter)"""
        return self._config['creation_date'][0]

    @creation_date.setter
    def creation_date(self, value):
        """Set the date in the configuraton (setter)"""
        if not isinstance(value, datetime.date):
            raise TypeError
        self._config['creation_date'][0] = value.isoformat()

    @property
    def tags(self):
        """Return the tags from the configuration (getter)"""
        return self._config['tags']

    @tags.setter
    def tags(self, value):
        """Set the tags in the configuraton (setter)"""
        if not isinstance(value, list):
            raise TypeError
        self._config['tags'] = value

    @property
    def theme_path(self):
        """Return the full path of the theme used by this page."""
        return self._theme_and_template_fp()[0]

    @property
    def author(self):
        """Return the full path of the theme used by this page."""
        r = self.site.site_config['default_author']
        if 'author' in self._config:
            r = self._config['author']
        return r