# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/LeslieZhu/.pyenv/versions/2.7.15/Python.framework/Versions/2.7/lib/python2.7/site-packages/orgnote/parser.py
# Compiled at: 2019-11-27 20:06:24
"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""
from __future__ import print_function
from __future__ import absolute_import
import re, sys, os, time, datetime, calendar, json, http.server
from bs4 import BeautifulSoup, Comment
from multiprocessing import Process
from functools import partial
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from orgnote import config
from orgnote import util
from orgnote.colorsrc import get_hightlight_src
if sys.version_info.major == 3:
    from imp import reload
    reload(sys)
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')

class OrgNoteFileSystemEventHander(FileSystemEventHandler):

    def __init__(self, fn, port=''):
        super(OrgNoteFileSystemEventHander, self).__init__()
        self.restart = fn
        self.port = port
        self.orglist = ['calendar.org', 'links.org', 'nopublic.org', 'public.org', 'slinks.org']

    def on_any_event(self, event):
        if event.src_path.endswith('.html') or os.path.basename(event.src_path) in self.orglist:
            print('orgnote source file changed: %s' % event.src_path)
            self.restart(self.port)


class OrgNote(object):

    def __init__(self):
        self.cfg = config.Config()
        self.emacs_version = [ int(i) for i in util.get_emacs_version() ]
        self.refresh_config()

    def refresh_config(self, homepage=''):
        self.notes_db = {}
        self.notes = []
        self.localnotes = []
        self.archives = []
        self.keywords = []
        self.tags = {}
        self.page_tags = {}
        self.timetags = {}
        self.slinks = []
        self.links = []
        self.job_today = []
        self.job_week = []
        self.job_prev = []
        self.__pagenames__ = {}
        self.title = self.cfg.cfg.get('title', 'OrgNote')
        self.subtitle = self.cfg.cfg.get('subtitle', 'OrgNote')
        self.author = self.cfg.cfg.get('author', 'OrgNote')
        self.email = self.cfg.cfg.get('email', '')
        self.description = self.cfg.cfg.get('description', '')
        self._keywords = self.cfg.cfg.get('keywords', 'OrgNote')
        self.language = self.cfg.cfg.get('language', 'zh-CN')
        self.homepage = (homepage or self.cfg.cfg.get)('url', 'https://github.com/LeslieZhu/OrgNote') if 1 else homepage
        self.blogroot = self.cfg.cfg.get('root', '/')
        self.source_dir = './' + self.cfg.cfg.get('source_dir', 'notes') + '/'
        self.images_dir = self.cfg.cfg.get('images_dir', 'images')
        self.files_dir = self.cfg.cfg.get('files_dir', 'data')
        self.public_dir = './' + self.cfg.cfg.get('public_dir', 'public') + '/'
        self.tags_dir = self.public_dir + '/tags'
        self.deploy_type = self.cfg.cfg.get('deploy_type', 'git')
        self.deploy_url = self.cfg.cfg.get('deploy_url', '')
        self.deploy_branch = self.cfg.cfg.get('deploy_branch', 'master')
        self.theme = self.cfg.cfg.get('theme', 'freemind')
        self.css_highlight = self.cfg.cfg.get('css_highlight', 'default')
        self.duoshuo_shortname = self.cfg.cfg.get('duoshuo_shortname', None)
        self.weibo_shortname = self.cfg.cfg.get('weibo_shortname', None)
        self.utteranc_repo = self.cfg.cfg.get('utteranc_repo', None)
        self.weixin_name = self.cfg.cfg.get('weixin_name', None)
        self.weixin_public = self.cfg.cfg.get('weixin_public', None)
        self.donate_name = self.cfg.cfg.get('donate_name', '赞赏支持')
        self.donate_alipay = self.cfg.cfg.get('donate_alipay', '')
        self.donate_wechatpay = self.cfg.cfg.get('donate_wechatpay', '')
        self.rss_type = self.cfg.cfg.get('rss_type', 'ReadMore')
        if self.rss_type not in ('ReadMore', 'ReadAll'):
            self.rss_type = 'ReadMore'
        self.default_tag = self.cfg.cfg.get('default_tag', '默认')
        self.nopublic_tag = self.cfg.cfg.get('nopublic_tag', '暂不公开')
        self.rdmode_keyword = self.cfg.cfg.get('reading_mode_keyword', '随笔')
        self.per_page = self.cfg.cfg.get('per_page', 6)
        self.sidebar_show = self.cfg.cfg.get('sidebar_show', 0)
        self.sidebar_show_page = self.cfg.cfg.get('sidebar_show_page', 0)
        self._sidebar_contact = self.cfg.cfg.get('sidebar_contact', '')
        self._sidebar_contact_name = self.cfg.cfg.get('sidebar_contact_name', '联系/反馈')
        self.sidebar_list = self.cfg.cfg.get('sidebar', list())
        self.dirs = [
         self.source_dir + 'public.org', self.source_dir + 'nopublic.org']
        self.menu_list = self.cfg.cfg.get('menu_list', dict())
        self.slinks_name = self.cfg.cfg.get('slinks_name', '友情链接')
        self.slinks_file = self.cfg.cfg.get('slinks_file', '')
        if self.slinks_file:
            self.slinks_file = self.source_dir + self.slinks_file
        self.links_name = self.cfg.cfg.get('links_name', '觅链')
        self.links_file = self.cfg.cfg.get('links_file', '')
        if self.links_file:
            self.links_file = self.source_dir + self.links_file
        self.shift_hour = self.cfg.cfg.get('shift_hour', 0)
        self.calendar_name = self.cfg.cfg.get('calendar_name', '')
        self.calendar_jobfile = self.cfg.cfg.get('calendar_jobfile', '')
        if self.calendar_jobfile:
            self.calendar_jobfile = self.source_dir + self.calendar_jobfile
        if self.sidebar_show == 1:
            self.col_md_index = 'col-md-9'
            self.col_md_index_r = 'col-md-3'
        else:
            self.col_md_index = 'col-md-12'
            self.col_md_index_r = ''
        if self.sidebar_show_page == 1:
            self.col_md_page = 'col-md-9'
            self.col_md_page_r = 'col-md-3'
        else:
            self.col_md_page = 'col-md-12'
            self.col_md_page_r = ''
        self.public_url = self.homepage + re.sub('//*', '/', self.blogroot + '/')
        self.search_path = 'search.json'
        self.menus = [
         [
          self.public_url + 'links.html', self.links_name, 'fa fa-sitemap', self.links_name],
         [
          self.public_url + 'archive.html', '归档', 'fa fa-archive', '归档'],
         [
          self.public_url + 'tags.html', '标签', 'fa fa-tags', '标签'],
         [self.public_url + 'calendar.html', self.calendar_name, 'fa fa-calendar', self.calendar_name] if self.calendar_name else None,
         [
          self.public_url + 'about.html', '说明', 'fa fa-user', '说明'],
         [
          self.public_url + 'rss.xml', '订阅', 'fa fa-rss', '订阅'],
         [
          self.public_url + self.search_path, '搜索', 'fa fa-search fa-fw', '搜索']]
        self.menus_map = {self.links_name: 'links.html', 
           '归档': 'archive.html', 
           '说明': 'about.html', 
           '标签': 'tags.html', 
           '订阅': 'rss.xml'}
        if self.calendar_name:
            self.menus_map[self.calendar_name] = 'calendar.html'
        for _menu in self.menu_list:
            menu = self.menu_list[_menu]
            if menu['url'].endswith('.html'):
                _url = menu['url']
            else:
                _url = menu['url'] + '.html'
            _item = [self.public_url + _url, menu['title'], menu['icon'], menu['title']]
            if _item not in self.menus:
                self.menus.append(_item)
                self.menus_map[menu['title']] = _url.strip('.html')

        if os.path.exists(self.links_file):
            for link in open(self.links_file, 'r').readlines():
                link = link.strip()
                if not link:
                    continue
                if link.startswith('#'):
                    continue
                link = [ i.strip() for i in link.split(',') ]
                if len(link) >= 3:
                    url, name, icon = link[:3]
                elif len(link) == 2:
                    url, name = link
                    icon = 'fa fa-link'
                else:
                    url = name = link[0]
                    icon = 'fa fa-link'
                item = [url, icon, name]
                if item not in self.links:
                    self.links.append(item)

        nopublic_link = [
         self.public_url + 'tags/' + self.nopublic_tag + '.html', 'fa fa-link', self.nopublic_tag]
        if nopublic_link not in self.links:
            self.links.append(nopublic_link)
        return

    def header_prefix(self, deep=1, title=''):
        """
        gen the header of each html
        """
        if deep == 1:
            path = '.'
        elif deep == 2:
            path = '..'
        if not title:
            title = self.title
        return '\n        <!DOCTYPE HTML>\n        <html>\n        <head>\n        <meta charset="utf-8">\n        %s\n        <title>%s</title>\n        <meta name="author" content="%s">\n        <meta name="email" content="%s">\n        <meta name="description" content="%s">\n        <meta property="og:site_name" content="%s"/>\n        <meta name="Keywords" content="%s">\n        \n        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">\n        <meta property="og:image" content="undefined"/>\n\n        <link href="%sfavicon.ico" rel="icon">\n        \n        <link rel="stylesheet" href="%stheme/%s/css/bootstrap.min.css" media="screen" type="text/css">\n        <link rel="stylesheet" href="%stheme/%s/css/font-awesome.css" media="screen" type="text/css">\n        <link rel="stylesheet" href="%stheme/%s/css/style.css" media="screen" type="text/css">\n        <link rel="stylesheet" href="%stheme/%s/css/highlight.css" media="screen" type="text/css">\n        <link rel="stylesheet" href="%stheme/%s/css/%s-highlight.css" media="screen" type="text/css">\n        <script type="text/javascript" src="%stheme/%s/js/jquery-2.0.3.min.js"></script>\n        <script type="text/javascript" src="%stheme/%s/js/local-search.js?v=7.4.1"></script>\n        </head>\n        ' % (self.js_config(), title, self.author, self.email, self.description, self.title, self._keywords,
         self.blogroot,
         self.blogroot, self.theme,
         self.blogroot, self.theme,
         self.blogroot, self.theme,
         self.blogroot, self.theme,
         self.blogroot, self.theme, self.css_highlight,
         self.blogroot, self.theme,
         self.blogroot, self.theme)

    def body_prefix(self):
        return '\n        <body>  \n        <nav id="main-nav" class="navbar navbar-inverse navbar-fixed-top" role="navigation">\n        \n        <div class="container">\n        \n        <button type="button" class="navbar-header navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">\n        <span class="sr-only">Toggle navigation</span>\n        <span class="icon-bar"></span>\n        <span class="icon-bar"></span>\n        <span class="icon-bar"></span>\n        </button>\n    \n        <a class="navbar-brand" href="%sindex.html">%s</a>\n        ' % (self.blogroot, self.title)

    def gen_tag_href(self, name=''):
        if name not in self.menus_map.keys():
            return '<a href="%stags/%s.html"><i class="%s"></i>%s</a>' % (self.public_url, name, name, name)
        else:
            return '<a href="%s%s"><i class="%s"></i>%s</a>' % (self.public_url, self.menus_map[name], name, name)

    def gen_href(self, line=list()):
        if len(line) == 4:
            if 'rss' in line[0]:
                return '<li><a href="%s" title="%s" target="_blank"><i class="%s"></i>%s</a></li>' % (line[0], line[1], line[2], line[3])
            else:
                if 'search' in line[0]:
                    return '<li>\n                <a role="button" class="popup-trigger">\n                <i class="%s"></i>%s\n                </a>\n                </li>\n                ' % (line[2], line[3])
                return '<li><a href="%s" title="%s"><i class="%s"></i>%s</a></li>' % (line[0], line[1], line[2], line[3])

        else:
            if len(line) == 3:
                return '<li><a href="%s" target="_blank"><i class="%s"></i>%s</a></li>' % (line[0], line[1], line[2])
            else:
                return ''

    def body_menu(self, menus=list()):
        """
        each menu's layout: link,title,fa-name,name
        """
        output = ''
        output += '\n        <div class="collapse navbar-collapse nav-menu">\n        \n        <ul class="nav navbar-nav">\n        '
        for menu in menus:
            if not menu:
                continue
            output += self.gen_href(menu)

        output += '\n        <div class="site-search">\n          <div class="popup search-popup">\n            <div class="search-header">\n              <span class="search-icon">\n                <i class="fa fa-search"></i>\n              </span>\n            <div class="search-input-container">\n              <input autocomplete="off" autocorrect="off" autocapitalize="none"\n                     placeholder="Searching..." spellcheck="false"\n                     type="text" id="search-input">\n            </div>\n            <span class="popup-btn-close">\n                <i class="fa fa-times-circle"></i>\n            </span>\n          </div>\n          <div id="search-result"></div>\n        </div>\n        <div class="search-pop-overlay"></div>\n        '
        output += '\n        </ul>\n        \n        </div> <!-- navbar -->\n        </div> <!-- container -->\n        </nav>\n        '
        return output

    def contain_prefix(self, tags=[], name='', header_title='', ispage=False):
        """
        ispage: False

        - True: it's in each note page, use self.col_md_page
        - False: it's in index page, use self.col_md_index
        """
        col_md = self.col_md_page if ispage else self.col_md_index
        if header_title == '':
            _header_title = self.subtitle
        else:
            if header_title in self.__pagenames__.keys():
                _header_title = self.__pagenames__[header_title]
            else:
                _header_title = header_title
            output = '\n        <div class="clearfix"></div>\n        <div class="container">\n        <div class="content">\n        \n        <div class="page-header">                   <!-- page-header begin -->\n        <h1>%s</h1>\n        </div>                                      <!-- page-header end -->\n        \n        <div class="row page">                      <!-- row-page begin -->\n        <div class="%s">                            <!-- col-md-9/12 begin -->\n        <div class="mypage">                        <!-- mypage begin -->\n        \n        <div class="slogan">                        <!-- slogan begin -->\n        <i class="fa fa-heart"></i>\n        ' % (_header_title, col_md)
            if not tags:
                output += '主页君: ' + self.author
            elif len(tags) == 1 and tags[0] in self.tags:
                output += name
                output += self.gen_tag_href(tags[0])
            else:
                output += name
                for tag in tags:
                    output += self.gen_tag_href(tag)
                    if tag != tags[(-1)]:
                        output += ' , '

        return output

    def contain_prefix_end(self, link=''):
        output = ''
        if link.endswith('.html'):
            output += "<span class='date'>文|<a href='%s'><i class='%s'></i>%s</a></span>" % (self.public_url + 'about.html',
             self.public_url + 'about.html',
             self.author)
        output += '\n        </div>                                     <!-- slogan end -->\n        '
        return output

    def gen_notes(self, dirs=list()):
        """
        gen each note from blog list
        """
        import os
        for i, notedir in enumerate(dirs):
            for line in open(notedir):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                public = False
                local = False
                public = True if i == 0 else False
                local = not public
                if line.endswith('.org'):
                    link = line.replace('.org', '.html')
                elif line.endswith('.md'):
                    link = line.replace('.md', '.html')
                else:
                    link = line
                name = util.gen_title(link)
                if public:
                    self.notes += [[link, name]]
                if local:
                    self.localnotes += [[link, name]]

    def contain_notes(self, data=list(), num=0, lastone=0):
        output = ''
        for item in data:
            output += '\n            <h3 class="title">\n            <a href="%s">%s</a>\n            <span class="date">%s </span>\n            </h3>\n            ' % (self.gen_public_link(item[0], self.public_url), item[1], self.gen_date(item[0]))
            if self.emacs_version[0] >= 24:
                output += '<div class="%s">' % 'col-md-12'
            else:
                output += '            \n                <div class="entry">\n                <div class="row">\n                <div class="%s">\n                ' % self.col_md_index
            output += self.contain_note(item[0])
            sub_title = sub_title = '<h1 class="title">%s</h1>' % util.gen_title(item[0])
            output = output.replace(sub_title, '')
            if self.emacs_version[0] >= 24:
                output += '\n                </div> <!-- %s -->\n                ' % 'col-md-12'
            else:
                output += '\n                </div> <!-- %s -->\n                </div> <!-- row -->\n                </div> <!-- entry -->\n                ' % 'col-md-12'

        if num == 0:
            prev_page = '<li class="prev disabled"><a><i class="fa fa-arrow-circle-o-left"></i>Newer</a></li>'
        elif num == 1:
            prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>Newer</a></li>' % (self.blogroot + 'index.html')
        else:
            prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>Newer</a></li>' % (self.public_url + 'page' + str(num - 1) + '.html')
        if lastone == len(self.notes):
            next_page = '<li class="next disabled"><a><i class="fa fa-arrow-circle-o-right"></i>Older</a></li>'
        else:
            next_page = '<li class="next"><a href="%s" class="alignright next">Older<i class="fa fa-arrow-circle-o-right"></i></a></li>' % (self.public_url + 'page' + str(num + 1) + '.html')
        output += '\n        <div>\n        <center>\n        <div class="pagination">\n        <ul class="pagination">\n        %s\n        <li><a href="%sarchive.html" target="_blank"><i class="fa fa-archive"></i>Archive</a></li>\n        %s\n        </ul>\n        </div>\n        </center>\n        </div>\n        ' % (prev_page, self.public_url, next_page)
        output += self.duosuo()
        output += '\n        </div> <!-- mypage -->\n        </div> <!-- %s -->\n        ' % 'col-md-12'
        return output

    def gen_prev(self, num=0):
        if num == 0:
            return ''
        else:
            return self.gen_public_link(self.notes[(num - 1)][0], self.public_url)

    def gen_next(self, num=0):
        if num == len(self.notes) - 1:
            return ''
        else:
            if self.notes:
                return self.gen_public_link(self.notes[(num + 1)][0], self.public_url)
            return ''

    def gen_tag_list(self, public=True):
        """
        - self.keywords is a list of all keywords
        - self.tags is a dict, a keyword's value is a list, each item is a [notefile,notetitle]
        """
        if not public:
            return
        for num, link in enumerate(self.notes):
            keywords = self.gen_category(link[0])
            self.page_tags[link[0]] = keywords
            for key in keywords:
                if key not in self.keywords:
                    self.keywords.append(key)
                if key not in self.tags.keys():
                    self.tags[key] = list()
                self.tags[key].append([link[0], link[1].strip()])

    def gen_timetag_list(self, public=True):
        if not public:
            return
        for num, link in enumerate(self.notes):
            yyyymm = ('').join(self.gen_date(link[0]).split('-')[:2])
            if yyyymm not in self.timetags.keys():
                self.timetags[yyyymm] = list()
            self.timetags[yyyymm].append(link)

    def copyright(self, num=''):
        if not self.notes:
            return ''
        if self.weixin_name:
            if self.weixin_public:
                wx = "<li><strong>微信搜索：</strong> <span>「 <a href='%s%s'>%s</a> 」</span>, 关注公众号!<li>" % (self.public_url, self.weixin_public, self.weixin_name)
            else:
                wx = "<li><strong>微信搜索：</strong> <span style='color:red'>「 %s 」</span>, 关注公众号!<li>" % self.weixin_name
        else:
            wx = ''
        output = '\n        <hr>\n        <div id="post-copyright">\n        <ul class="post-copyright">\n        <li class="post-copyright-author">\n        <strong>本文作者：</strong>「\n        <a href="%s" title="%s">%s</a> 」创作于%s\n        </li>\n        %s\n        <li class="post-copyright-link">\n        <strong>本文链接：</strong>\n        <a href="%s" title="%s">%s</a>\n        </li>\n        <li class="post-copyright-license">\n        <strong>版权声明：</strong>\n        原创文章，如需转载请注明文章作者和出处。谢谢！\n        </li>\n        </ul>\n        </div>\n        ' % (self.public_url + 'about.html',
         self.author, self.author,
         self.gen_date(self.notes[num][0]),
         wx,
         self.gen_public_link(self.notes[num][0], self.public_url),
         self.notes[num][1],
         self.gen_public_link(self.notes[num][0], self.public_url))
        return output

    def contain_page(self, link='', num=0, public=True):
        output = ''
        html_data = BeautifulSoup(open(link, 'r').read(), 'html.parser')
        _title = html_data.find('h1', {'class': 'title'}).text
        content_data = html_data.find('div', {'id': 'content'})
        content_data_text = str(content_data)
        keywordtext = html_data.find(attrs={'name': 'keywords'})['content']
        if self.rdmode_keyword in keywordtext:
            content_data_text = content_data_text.replace('id="content"', 'id="content-reading"')
        content_data_text += self.copyright(num)
        image_file = 'file:///%s/' % self.images_dir
        image_path = '%s%s/' % (self.public_url, self.images_dir)
        if image_file in content_data_text:
            content_data_text = content_data_text.replace(image_file, image_path)
        data_file = 'file:///%s/' % self.files_dir
        data_path = '%s%s/' % (self.public_url, self.files_dir)
        if data_file in content_data_text:
            content_data_text = content_data_text.replace(data_file, data_path)
        src_data = content_data.find_all('div', {'class': 'org-src-container'})
        for src_tag in src_data:
            src_lang = src_tag.find('pre').attrs['class'][(-1)].split('-')[(-1)]
            src_code = src_tag.text
            new_src = get_hightlight_src(src_code, src_lang)
            content_data_text = content_data_text.replace(str(src_tag), new_src)

        if public:
            new_archive = [self.gen_public_link(self.notes[num][0], self.public_url), 'fa fa-file-o', self.notes[num][1].strip()] if self.notes else []
            if new_archive not in self.archives:
                self.archives.append(new_archive)
            if num == 0:
                prev_page = '<li class="prev disabled"><a><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>'
            else:
                prev_page = '<li class="prev"><a href="%s" class=alignright prev"><i class="fa fa-arrow-circle-o-left"></i>上一页</a></li>' % self.gen_prev(num)
            if num == len(self.notes) - 1:
                next_page = '<li class="next disabled"><a><i class="fa fa-arrow-circle-o-right"></i>下一页</a></li>'
            else:
                next_page = '<li class="next"><a href="%s" class="alignright next">下一页<i class="fa fa-arrow-circle-o-right"></i></a></li>' % self.gen_next(num)
            page_order = '\n            <div>\n            <center>\n            <div class="pagination">\n            <ul class="pagination">\n            %s\n            <li><a href="%sarchive.html" target="_blank"><i class="fa fa-archive"></i>Archive</a></li>\n            %s\n            </ul>\n            </div>\n            </center>\n            </div>\n            ' % (prev_page, self.public_url, next_page)
        else:
            page_order = ''
        without_title_data = content_data_text.replace('<h1 class="title">%s</h1>' % _title, '')
        new_data = without_title_data + page_order + self.donate() + self.duosuo() + self.utteranc()
        output += new_data
        output += '</div> <!-- my-page -->'
        output += '</div> <!-- col-md -->'
        return output

    def contain_note(self, link=''):
        import re
        output = ''
        html_data = BeautifulSoup(open(link, 'r').read(), 'html.parser')
        _title = html_data.find('h1', {'class': 'title'}).text
        content_data = html_data.find('div', {'id': 'content'})
        if 'table-of-contents' in str(content_data):
            content_data_text = str(html_data.find('div', {'id': 'table-of-contents'}))
        else:
            content_data_text = str(content_data)
        content_data_text = content_data_text.replace('<h1 class="title">%s</h1>' % _title, '')
        src_data = content_data.find_all('div', {'class': 'org-src-container'})
        for src_tag in src_data:
            src_lang = src_tag.find('pre').attrs['class'][(-1)].split('-')[(-1)]
            src_code = src_tag.text
            new_src = get_hightlight_src(src_code, src_lang)
            content_data_text = content_data_text.replace(str(src_tag), new_src)

        if 'table-of-contents' in content_data_text:
            new_data = content_data_text
        else:
            new_data = content_data_text.split('</p>')
            p_num = len(new_data)
            if p_num > 5:
                new_data = ('</p>').join(new_data[:5])
                new_data += '\n                </p>\n                </div>\n                '
            else:
                new_data = ('</p>').join(new_data)
        new_data = new_data.replace('content', 'content-index')
        output += new_data
        output += '\n        <footer>\n        <div class="alignleft">\n        <a href="%s#more" class="more-link">阅读全文</a>\n        </div>\n        <div class="clearfix"></div>\n        </footer>\n        ' % self.gen_public_link(link, self.public_url)
        return output

    def contain_archive(self, data=list()):
        output = ''
        output += '\n        <!-- display as entry -->\n        <div class="entry">\n        <div class="row">\n        <div class="%s">\n        ' % self.col_md_index
        for archive in data:
            if len(archive) == 2:
                newarchive = [
                 self.public_url + ('/').join(archive[0].split('/')[2:]), 'fa fa-file-o', archive[1]]
                output += self.gen_href(newarchive)
            else:
                output += self.gen_href(archive)

        output += '\n        </div>\n        </div>\n        </div>\n        '
        output += '\n        </div> <!-- mypage -->\n        </div> <!-- %s -->\n        ' % self.col_md_index
        return output

    def contain_archive_tag(self):
        output = ''
        '\n        <!-- display as entry -->\n        <div class="entry"> \n        <div class="row">\n        <div class="%s">\n        ' % self.col_md_index
        output += '<ul>'
        from functools import cmp_to_key
        key = cmp_to_key(lambda x, y: len(self.tags[x]) - len(self.tags[y]))
        for key in sorted(self.keywords, key=key, reverse=True):
            output += '<a href="javascript:showul(\'%s\');"><h3>%s(%d)</h3></a>' % (key, key, len(self.tags[key]))
            output += "<ul id='%s' style='display:none'>" % key
            for link in self.tags[key]:
                newarchive = [
                 self.gen_public_link(link[0], self.public_url), 'fa fa-file-o', link[1]]
                output += self.gen_href(newarchive)

            output += '</ul>'

        output += '</ul>'
        output += '\n        </div> <!-- mypage -->\n        </div> <!-- %s -->\n        ' % self.col_md_index
        return output

    def contain_about(self):
        """about me page"""
        output = ''
        output += '\n        <!-- display as entry -->\n        <div class="entry">\n        <div class="row">\n        <div class="%s">\n        ' % self.col_md_index
        if self.description:
            output += '<p>%s</p>' % self.description
        else:
            output += '\n            <p>这是一个建立在<code><a class="i i1 fc01 h" hidefocus="true" href="https://www.github.com/LeslieZhu/OrgNote" target="_blank">OrgNote</a></code>上的博客.</p>\n            '
        output += '\n        </div>\n        </div>\n        </div>             \n        '
        output += self.duosuo()
        output += '\n        </div> <!-- mypage -->\n        </div> <!-- %s -->\n        ' % self.col_md_index
        return output

    def contain_calendar(self):
        output = ''
        if not self.calendar_name or not self.calendar_jobfile:
            return output
        if not os.path.exists(self.calendar_jobfile):
            print('Can not found jobfile: ', self.calendar_jobfile)
            return output
        by_types = {'by_once': '一次性事情', 'by_day': '每天一次', 
           'by_week': '每周一次', 
           'by_month': '每月一次', 
           'by_quarter': '每季一次', 
           'by_year': '每年一次'}
        for job in open(self.calendar_jobfile, 'r').readlines():
            job = job.strip()
            if not job:
                continue
            if job.startswith('#'):
                continue
            job = [ i.strip() for i in job.strip().split(',') ]
            if len(job) < 3:
                print('Bad format calendar job(time,name,job type,url):', job)
                continue
            jtype, jtime = job[:2]
            hasurl = False
            for p in ['http://', 'https://', 'www.']:
                if job[(-1)].startswith(p):
                    hasurl = True
                    continue

            if hasurl:
                jurl = job[(-1)]
                jname = (',').join(job[2:-1]) if len(job) > 3 else jurl
            else:
                jurl = ''
                jname = (',').join(job[2:])
            if jtype not in by_types:
                print('Bad job type in', job)
                print('job type must be on of ', by_types.keys())
                continue
            try:
                jtime = datetime.datetime.strptime(jtime, '%Y/%m/%d %H:%M')
            except ValueError as e:
                print('Bad job format:', job)
                print(str(e))
                continue

            quarter_list = [ j for j in [ i + jtime.month for i in range(-9, 10, 3) ] if j >= 1 and j <= 12 ]
            today = datetime.datetime.now() + datetime.timedelta(hours=self.shift_hour)
            monthrange = calendar.monthrange(today.year, today.month)
            if monthrange[1] < jtime.day:
                jtime.replace(day=monthrange[1])
            today = today.replace(hour=jtime.hour, minute=jtime.minute)
            is_today_job = False
            is_week_job = False
            is_prev_job = False
            if jtype == 'by_day' or (today.year, today.month, today.day) == (jtime.year, jtime.month, jtime.day):
                is_today_job = True
            elif jtype == 'by_once':
                delta = jtime - today
                if delta.days in range(0, 8):
                    is_week_job = True
                elif delta.days in range(-8, 0):
                    is_prev_job = True
            elif jtype == 'by_week':
                if jtime.weekday() == today.weekday():
                    is_today_job = True
                else:
                    is_week_job = True
                    is_prev_job = True
            elif jtype == 'by_month':
                if today.day == jtime.day:
                    is_today_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day > jtime.day:
                    is_prev_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day < jtime.day:
                    is_week_job = True
            elif jtype == 'by_quarter':
                if today.month not in quarter_list:
                    continue
                if today.day == jtime.day:
                    is_today_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day > jtime.day:
                    is_prev_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day < jtime.day:
                    is_week_job = True
            elif jtype == 'by_year':
                if today.year < jtime.year:
                    continue
                if today.month != jtime.month:
                    continue
                if today.day == jtime.day:
                    is_today_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day > jtime.day:
                    is_prev_job = True
                elif abs(today.day - jtime.day) <= 7 and today.day < jtime.day:
                    is_week_job = True
            else:
                continue
            weekday = jtime.weekday() + 1
            t_weekday = today.weekday() + 1
            if is_today_job:
                today_str = today.strftime('%Y/%m/%d %H:%M')
                self.job_today.append([today_str, jname, jtype, jurl])
            elif is_week_job:
                if t_weekday >= weekday:
                    days = 7 - t_weekday + weekday
                else:
                    days = weekday - t_weekday
                today = today + datetime.timedelta(days=days)
                today_str = today.strftime('%Y/%m/%d %H:%M')
                self.job_week.append([today_str, jname, jtype, jurl])
            elif is_prev_job:
                if t_weekday <= weekday:
                    days = 7 - weekday + t_weekday
                else:
                    days = t_weekday - weekday
                days *= -1
                today = today + datetime.timedelta(days=days)
                today_str = today.strftime('%Y/%m/%d %H:%M')
                self.job_prev.append([today_str, jname, jtype, jurl])

        for jobs in [self.job_today, self.job_week, self.job_prev]:
            if not jobs:
                continue
            if jobs == self.job_today:
                output += '<h3>今日行程</h3>'
            else:
                if jobs == self.job_week:
                    output += '<h3>下周行程</h3>'
                else:
                    output += '<h3>上周行程</h3>'
                output += '<ul>'
                for job in sorted(jobs):
                    if not job[3]:
                        output += '<li><strong>时间</strong>: %s , <strong>(%s)</strong>: %s </li>' % (job[0], by_types[job[2]], job[1])
                    else:
                        output += "<li><strong>时间</strong>: %s , <strong>(%s)</strong>: <a href='%s'>%s</a> </li>" % (job[0], by_types[job[2]], job[3], job[1])

            output += '</ul>'

        output += '\n        </div> <!-- mypage -->\n        </div> <!-- %s -->\n        ' % self.col_md_index
        return output

    def donate(self):
        if not self.donate_name or not self.donate_wechatpay and not self.donate_alipay:
            return ''
        output = ''
        if self.donate_name:
            output += '\n            <div class="post-reward">\n            <input type="checkbox" name="reward" id="reward" hidden />\n            <label id="reward-button" class="reward-button" for="reward">%s</label>\n            <div class="qr-code">\n            ' % self.donate_name
            if self.donate_wechatpay:
                output += '\n                <label id="qr-code-image-w" class="qr-code-image" for="reward" hidden>\n                <img class="image" src="%s/%s">\n                <span>微信打赏</span>\n                </label>\n                ' % (self.public_url, self.donate_wechatpay)
            if self.donate_alipay:
                output += '\n                <label id="qr-code-image-a" class="qr-code-image" for="reward" hidden>\n                <img class="image" src="%s/%s">\n                <span>支付宝打赏</span>\n                </label>\n                ' % (self.public_url, self.donate_alipay)
            if self.weixin_public:
                output += '\n                <label id="qr-code-image-p" class="qr-code-image" for="reward" hidden>\n                <img class="image" src="%s/%s">\n                <span>微信公众号</span>\n                </label>\n                ' % (self.public_url, self.weixin_public)
            output += '\n            </div>\n            </div>\n            '
        return output

    def utteranc(self):
        if not self.utteranc_repo:
            return ''
        else:
            return '\n            <script src="https://utteranc.es/client.js"\n            repo="%s"\n            issue-term="title"\n            theme="github-light"\n            crossorigin="anonymous"\n            async>\n            </script>\n            ' % self.utteranc_repo

    def duosuo(self):
        if not self.duoshuo_shortname:
            return '\n            '
        else:
            return '\n            <!-- Duoshuo Comment BEGIN -->\n            <div class="ds-thread"></div>\n            <script type="text/javascript">\n            var duoshuoQuery = {short_name:"%s"};\n            (function() {\n            var ds = document.createElement(\'script\');\n            ds.type = \'text/javascript\';ds.async = true;\n            ds.src = \'http://static.duoshuo.com/embed.js\';\n            ds.charset = \'UTF-8\';\n            (document.getElementsByTagName(\'head\')[0]\n            || document.getElementsByTagName(\'body\')[0]).appendChild(ds);\n            })();\n            </script>\n            <!-- Duoshuo Comment END -->\n            ' % self.duoshuo_shortname

    def contain_sidebar(self):
        return '\n        <div class="%s">\n        <div id="sidebar">\n        ' % (self.col_md_index_r if self.col_md_index_r else self.col_md_page_r)

    def sidebar_contact(self):
        return '\n        <div class="widget">\n        <h4>%s</h4>\n        <ul class="entry list-unstyled">\n        <li>%s</li>\n        </ul>\n        </div>\n        ' % (self._sidebar_contact_name, self._sidebar_contact)

    def sidebar_weixin(self):
        if not self.weixin_name and not self.weixin_public:
            return ''
        else:
            if not self.weixin_public:
                return '\n            <div class="widget">\n            <h4>%s</h4>\n            <ul class="entry list-unstyled">\n            <li>%s</li>\n            </ul>\n            </div>\n            ' % ('微信公众号', self.weixin_name)
            return '\n            <div class="widget">\n            <h4>%s</h4>\n            <ul class="entry list-unstyled">\n            <li><img class="image" src="%s/%s"></li>\n            </ul>\n            </div>\n            ' % ('微信公众号', self.public_url, self.weixin_public)

    def sidebar_duoshuo(self):
        return '\n        <div class="widget">\n        <h4>最新评论</h4>\n        <ul class="entry list-unstyled">\n\n        <!-- 多说最新评论 start -->\n        <div class="ds-recent-comments" data-num-items="5" data-show-avatars="1" data-show-time="1" data-show-title="1" data-show-admin="1" data-excerpt-length="170"></div>\n        <!-- 多说最新评论 end -->\n        <!-- 多说公共JS代码 start (一个网页只需插入一次) -->\n        <script type="text/javascript">\n        var duoshuoQuery = {short_name:"%s"};\n        (function() {\n        var ds = document.createElement(\'script\');\n        ds.type = \'text/javascript\';ds.async = true;\n        ds.src = (document.location.protocol == \'https:\' ? \'https:\' : \'http:\') + \'//static.duoshuo.com/embed.js\';\n        ds.charset = \'UTF-8\';\n        (document.getElementsByTagName(\'head\')[0]\n        || document.getElementsByTagName(\'body\')[0]).appendChild(ds);\n        })();\n        </script>\n        <!-- 多说公共JS代码 end -->\n        </ul>\n        </div>\n        ' % self.duoshuo_shortname

    def sidebar_tags(self):
        output = ''
        output += '\n        <div class="widget">\n        <h4>标签云</h4>\n        <ul class="tag_box inline list-unstyled">\n        '
        from functools import cmp_to_key
        key = cmp_to_key(lambda x, y: len(self.tags[x]) - len(self.tags[y]))
        for key in sorted(self.keywords, key=key, reverse=True):
            output += '<li><a href="%stags/%s.html">%s<span>%s</span></a></li>' % (self.public_url, key, key, len(self.tags[key]))

        output += '\n        </ul>\n        </div>\n        '
        return output

    def contain_tags(self):
        output = ''
        output += '\n        <div class="tag-cloud-tags" style="padding: 5px 15px">\n        '
        from functools import cmp_to_key
        key = cmp_to_key(lambda x, y: len(self.tags[x]) - len(self.tags[y]))
        for key in sorted(self.keywords, key=key, reverse=True):
            nums = len(self.tags[key])
            size = nums / 5.0
            if size < 1:
                size = 1
            elif size > 4:
                size = 4
            output += '<a href="%stags/%s.html" style="font-size:%srem">%s</a>' % (self.public_url, key, size, key)

        output += '\n        </div>\n        '
        return output

    def sidebar_date(self):
        output = ''
        output += '\n        <div class="widget">\n        <h4>时间机器</h4>\n        <ul class="tag_box inline list-unstyled">\n        '
        tot = 0
        for key in sorted(self.timetags.keys(), reverse=True):
            output += '<li><a href="%stags/%s.html">%s<span>%s</span></a></li>' % (self.public_url, key, key, len(self.timetags[key]))
            tot += len(self.timetags[key])

        output += '<li><a href="%sarchive.html">All<span>%s</span></a></li>' % (self.public_url, tot)
        output += '\n        </ul>\n        </div>\n        '
        return output

    def sidebar_latest(self, notes=list(), num=6):
        """
        each note layout: link,name
        """
        output = ''
        output += '\n        <div class="widget">\n        <h4>最新文章</h4>\n        <ul class="entry list-unstyled">\n        '
        for note in notes[:num]:
            output += '<li><a href="%s"><i class="fa fa-file-o"></i>%s</a></li>' % (self.gen_public_link(note[0].replace('"', ''), self.public_url), note[1])

        output += '\n        </ul>   \n        </div> \n        '
        return output

    def sidebar_weibo(self):
        return '\n        '

    def sidebar_link(self):
        output = '\n        <div class="widget">\n        <h4>%s</h4>\n        <ul class="entry list-unstyled">\n        ' % self.slinks_name
        if os.path.exists(self.slinks_file):
            for link in open(self.slinks_file, 'r').readlines():
                link = link.strip()
                if not link:
                    continue
                if link.startswith('#'):
                    continue
                link = [ i.strip() for i in link.split(',') ]
                if len(link) >= 3:
                    url, name, icon = link[:3]
                elif len(link) == 2:
                    icon = 'fa fa-link'
                else:
                    url = name = link[0]
                    icon = 'fa fa-link'
                item = (url, name, icon)
                if item not in self.slinks:
                    self.slinks.append(item)

        for link in sorted(self.slinks):
            url, name, icon = link
            output += '\n            <li><a href="%s" title="%s" target="_blank"><i class="%s"></i>%s</a></li>\n            ' % (url, name, icon, name)

        output += '\n        </ul>\n        </div>\n        '
        return output

    def end_sidebar(self):
        return '\n        </div> <!-- sidebar -->\n        </div> <!-- %s -->\n        ' % self.col_md_index_r

    def contain_suffix(self):
        return '\n        </div> <!-- row-fluid -->\n        </div>\n        </div>\n        '

    def header_suffix(self):
        return '\n        <div class="container-narrow">\n        <footer>\n        <p>&copy; 2014 %s\n        with help from <a href="https://github.com/LeslieZhu/OrgNote" target="_blank">OrgNote</a>. Theme by <a href="https://github.com/LeslieZhu/orgnote-theme-freemind">orgnote-theme-freemind</a>.  Published with GitHub Pages. \n        </p> </footer>\n        </div> <!-- container-narrow -->\n        \n        <a id="gotop" href="#">   \n        <span>▲</span> \n        </a>\n        \n        %s\n\n        </body>\n        </html>\n        ' % (self.author, self.gen_jscripts())

    def js_config(self):
        return '\n        <script>\n        var CONFIG = {\n        root: \'/\',\n        localsearch: {"enable":true,"trigger":"auto","top_n_per_article":1,"preload":true},\n        path: \'%s\',\n        };\n        </script>\n        ' % self.search_path

    def gen_jscripts(self):
        return '\n\n        <script type="text/javascript">\n        \n        <!-- donate script -->\n        var reward = document.getElementById(\'reward\');\n        if(reward){\n            reward.onclick = function() {\n              $(\'#reward-button\').addClass(\'hidden\');\n              $(\'#qr-code-image-w\').show();\n              $(\'#qr-code-image-a\').show();\n              $(\'#qr-code-image-p\').show();\n            }\n        }\n        <!-- /donate script -->\n\n        \n        function showul(name){\n            var uls = document.getElementById(name);\n            if(uls.style.display == "none"){\n               uls.style.display = "block";\n            } else {\n               uls.style.display = "none";\n            } \n        }\n        </script>\n        '

    def gen_public_link(self, link='', prefix=None):
        if prefix == None:
            prefix = ''
        return prefix + ('/').join(link.split('/')[2:])

    def gen_sidebar(self):
        """
        if the sidebar enable, then display each sidebar by order
        """
        if self.sidebar_show == 1:
            output = self.contain_sidebar()
            if self._sidebar_contact:
                output += self.sidebar_contact()
            for _sidebar in self.sidebar_list:
                if _sidebar == 'sidebar_latest':
                    output += self.sidebar_latest(self.notes)
                elif _sidebar == 'sidebar_tags':
                    output += self.sidebar_tags()
                elif _sidebar == 'sidebar_time':
                    output += self.sidebar_date()
                elif _sidebar == 'sidebar_link':
                    output += self.sidebar_link()
                elif _sidebar == 'sidebar_weibo' and self.weibo_shortname:
                    output += self.sidebar_weibo()
                elif self.duoshuo_shortname and _sidebar == 'sidebar_duoshuo' and self._sidebar_contact:
                    output += self.sidebar_duoshuo()
                elif self.weixin_name or self.weixin_public:
                    output += self.sidebar_weixin()

            output += self.end_sidebar()
        else:
            output = ''
        return output

    def gen_sidebar_page(self):
        output = ''
        if self.sidebar_show_page == 0:
            output += ''
        else:
            output += self.contain_sidebar()
            if self._sidebar_contact:
                output += self.sidebar_contact()
            for _sidebar in self.sidebar_list:
                if _sidebar == 'sidebar_latest':
                    output += self.sidebar_latest(self.notes)
                elif _sidebar == 'sidebar_tags':
                    output += self.sidebar_tags()
                elif _sidebar == 'sidebar_time':
                    output += self.sidebar_date()
                elif _sidebar == 'sidebar_link':
                    output += self.sidebar_link()
                elif _sidebar == 'sidebar_weibo' and self.weibo_shortname:
                    output += self.sidebar_weibo()
                elif self.duoshuo_shortname and _sidebar == 'sidebar_duoshuo' and self._sidebar_contact:
                    output += self.sidebar_duoshuo()
                elif self.weixin_name or self.weixin_public:
                    output += self.sidebar_weixin()

            output += self.end_sidebar()
        return output

    def gen_archive(self):
        output = open('./' + self.public_dir + 'archive.html', 'w')
        print(self.header_prefix(title='归档'), file=output)
        print(self.body_prefix(), file=output)
        print(self.body_menu(self.menus), file=output)
        print(self.contain_prefix(['归档'], '', '归档(%d)' % sum([ len(self.tags[k]) for k in self.keywords ])), file=output)
        print(self.contain_prefix_end(), file=output)
        print(self.contain_archive_tag(), file=output)
        print(self.gen_sidebar(), file=output)
        print(self.contain_suffix(), file=output)
        print(self.header_suffix(), file=output)
        output.close()

    def gen_rss(self):
        output = open('./' + self.public_dir + 'rss.xml', 'w')
        print(self.gen_rss_xml(), file=output)
        output.close()

    def gen_search(self):
        output = open('./' + self.public_dir + self.search_path, 'w')
        print(self.gen_search_json(), file=output)
        output.close()

    def gen_search_json(self):
        searchdb = []
        for note in self.notes:
            link, name = note
            item = {}
            item['title'] = name
            item['url'] = self.gen_public_link(link, '/')
            item['content'] = self.gen_content(link)
            searchdb.append(item)

        return json.dumps(searchdb)

    def gen_search_xml(self):
        output = ''
        output += '<?xml version="1.0" encoding="UTF-8" ?>\n        <item>\n        '
        for note in self.notes:
            link, name = note
            output += '\n            <entry>\n            <title> %s </title>\n            <url> %s </link>\n            <description>%s </description>\n            </entry>\n            ' % (name,
             self.gen_public_link(link, self.public_url),
             self.gen_content(link))

        output += '\n        </item>\n        </xml>\n        '
        return output

    def gen_rss_xml(self):
        output = ''
        output += '<?xml version="1.0" encoding="UTF-8" ?>\n        <rss version="2.0">\n        <channel>\n\n        <title>%s</title>\n\n        <link>%s</link>\n\n        <description>\n           <![CDATA[%s]]>\n        </description>\n\n        <language>zh-CN</language>\n        <generator>OrgNote: A simple org-mode blog, write blog by org-mode in Emacs</generator>\n        <webMaster><![CDATA[%s]]></webMaster>\n        <ttl>120</ttl>\n        \n        <image>\n        <title><![CDATA[%s]]></title>\n        <url>%s/favicon.ico</url>\n        <link>%s</link>\n        </image>        \n        ' % (self.title, self.homepage, self.subtitle,
         self.author, self.title, self.homepage, self.homepage)
        for note in self.notes:
            link, name = note
            output += '\n            <item>\n            <title> %s </title>\n            <link> %s </link>\n            <author><![CDATA[%s]]></author>\n            <guid isPermaLink="true">%s</guid>\n            ' % (name, self.gen_public_link(link, self.public_url),
             self.author, self.gen_public_link(link, self.public_url))
            for tag in self.gen_category(link):
                output += '<category><![CDATA[%s]]></category>' % tag

            output += '\n            <pubDate>%s</pubDate>\n            <description><![CDATA[%s]]></description>\n            <comments>%s</comments>\n            </item>\n            ' % (self.gen_date(link),
             self.gen_content(link) if self.rss_type == 'ReadAll' else self.contain_note(link),
             self.gen_public_link(link, self.public_url))

        output += '\n        </channel>\n        </rss>\n        '
        return output

    def gen_content(self, link):
        html_data = BeautifulSoup(open(link, 'r').read(), 'html.parser')
        content_data = html_data.find('div', {'id': 'content'})
        return str(content_data)

    def gen_tags_menu_page(self):
        output = open('./' + self.public_dir + 'tags.html', 'w')
        print(self.header_prefix(title='标签'), file=output)
        print(self.body_prefix(), file=output)
        print(self.body_menu(self.menus), file=output)
        print(self.contain_prefix(['标签'], '', '标签'), file=output)
        print(self.contain_prefix_end(), file=output)
        print(self.contain_tags(), file=output)
        print(self.contain_suffix(), file=output)
        print(self.header_suffix(), file=output)
        output.close()

    def gen_page(self, note=list(), num=0, public=True):
        import os, os.path
        page_file = './' + self.gen_public_link(note[0], self.public_dir)
        page_dir = os.path.dirname(page_file)
        if not os.path.exists(page_dir):
            os.makedirs(page_dir)
        output = open(page_file, 'w')
        print(self.header_prefix(2, note[1].strip()), file=output)
        print(self.body_prefix(), file=output)
        print(self.body_menu(self.menus), file=output)
        if public:
            print(self.contain_prefix(self.page_tags[note[0]], '标签: ', util.gen_title(note[0]), True), file=output)
        else:
            print(self.contain_prefix([self.nopublic_tag], '标签: ', util.gen_title(note[0]), True), file=output)
        print(self.contain_prefix_end(note[0]), file=output)
        print(self.contain_page(note[0], num, public), file=output)
        print(self.gen_sidebar_page(), file=output)
        print(self.contain_suffix(), file=output)
        print(self.header_suffix(), file=output)
        output.close()

    def gen_public(self):
        for i, note in enumerate(self.notes):
            self.gen_page(note, i, True)

        for i, note in enumerate(self.localnotes):
            self.gen_page(note, i, False)

    def split_index(self, num, b_index, e_index):
        """
        split index.html as page1,page2,page3...,so do not need display all notes in homepage
        """
        if num == 0:
            output = open('./' + self.public_dir + 'index.html', 'w')
        else:
            output = open('./' + self.public_dir + 'page' + str(num) + '.html', 'w')
        print(self.header_prefix(title=self.title), file=output)
        print(self.body_prefix(), file=output)
        print(self.body_menu(self.menus), file=output)
        print(self.contain_prefix(), file=output)
        print(self.contain_prefix_end(), file=output)
        print(self.contain_notes(self.notes[b_index:e_index], num, e_index), file=output)
        print(self.gen_sidebar(), file=output)
        print(self.contain_suffix(), file=output)
        print(self.header_suffix(), file=output)
        output.close()

    def gen_index(self, note_num=None):
        """
        each split page hold `num` notes
        """
        if note_num == None:
            note_num = self.per_page
        num = 0
        b_index = 0
        e_index = b_index + note_num
        tot = len(self.notes)
        while num <= tot:
            if b_index > tot:
                break
            elif b_index <= tot and e_index > tot:
                self.split_index(num, b_index, tot)
            else:
                self.split_index(num, b_index, e_index)
            num += 1
            b_index += note_num
            e_index = b_index + note_num

        return

    def gen_about(self):
        about_file = '%sabout.html' % self.source_dir
        output = open(self.public_dir + 'about.html', 'w')
        print(self.header_prefix(title='说明'), file=output)
        print(self.body_prefix(), file=output)
        print(self.body_menu(self.menus), file=output)
        print(self.contain_prefix(['说明'], '', '说明'), file=output)
        print(self.contain_prefix_end(), file=output)
        if os.path.exists(about_file):
            print(self.contain_page(about_file, 0, True), file=output)
        else:
            print(self.contain_about(), file=output)
        print(self.gen_sidebar(), file=output)
        print(self.contain_suffix(), file=output)
        print(self.header_suffix(), file=output)
        output.close()

    def gen_links(self):
        output = open('./' + self.public_dir + 'links.html', 'w')
        print(self.header_prefix(title=self.links_name), file=output)
        print(self.body_prefix(), file=output)
        print(self.body_menu(self.menus), file=output)
        print(self.contain_prefix([self.links_name], '', self.links_name), file=output)
        print(self.contain_prefix_end(), file=output)
        print(self.contain_archive(self.links), file=output)
        print(self.gen_sidebar(), file=output)
        print(self.contain_suffix(), file=output)
        print(self.header_suffix(), file=output)
        output.close()

    def gen_tags(self):
        for key in self.keywords:
            output = open('./' + self.public_dir + 'tags/' + key + '.html', 'w')
            print(self.header_prefix(title=key), file=output)
            print(self.body_prefix(), file=output)
            print(self.body_menu(self.menus), file=output)
            print(self.contain_prefix([key], '分类: ', key), file=output)
            print(self.contain_prefix_end(), file=output)
            print(self.contain_archive(self.tags[key]), file=output)
            print(self.gen_sidebar(), file=output)
            print(self.contain_suffix(), file=output)
            print(self.header_suffix(), file=output)
            output.close()

    def gen_timetags(self):
        for key in sorted(self.timetags.keys(), reverse=True):
            output = open('./' + self.public_dir + 'tags/' + key + '.html', 'w')
            print(self.header_prefix(title=key), file=output)
            print(self.body_prefix(), file=output)
            print(self.body_menu(self.menus), file=output)
            print(self.contain_prefix([key], '月份: ', key), file=output)
            print(self.contain_prefix_end(), file=output)
            print(self.contain_archive(self.timetags[key]), file=output)
            print(self.gen_sidebar(), file=output)
            print(self.contain_suffix(), file=output)
            print(self.header_suffix(), file=output)
            output.close()

    def gen_nopublic(self):
        output = open('./' + self.public_dir + 'tags/' + self.nopublic_tag + '.html', 'w')
        print(self.header_prefix(title=self.nopublic_tag), file=output)
        print(self.body_prefix(), file=output)
        print(self.body_menu(self.menus), file=output)
        print(self.contain_prefix([self.nopublic_tag], '分类: ', self.nopublic_tag), file=output)
        print(self.contain_prefix_end(), file=output)
        print(self.contain_archive(self.localnotes), file=output)
        print(self.contain_suffix(), file=output)
        print(self.header_suffix(), file=output)
        output.close()

    def gen_calendar(self):
        output = open(self.public_dir + 'calendar.html', 'w')
        print(self.header_prefix(title=self.calendar_name), file=output)
        print(self.body_prefix(), file=output)
        print(self.body_menu(self.menus), file=output)
        print(self.contain_prefix([self.calendar_name], '', self.calendar_name), file=output)
        print(self.contain_prefix_end(), file=output)
        print(self.contain_calendar(), file=output)
        print(self.gen_sidebar(), file=output)
        print(self.contain_suffix(), file=output)
        print(self.header_suffix(), file=output)
        output.close()

    def gen_date(self, link=''):
        """ Filter Publish data from HTML metadata>"""
        html_data = BeautifulSoup(open(link, 'r').read(), 'html.parser')
        date_tag = html_data.find('p', {'class': 'date'})
        if not date_tag:
            date_tag = html_data.find('meta', {'name': 'generated'})
        if date_tag:
            pubdate = date_tag.contents[0].split(':')[(-1)].strip()
        if '/' in pubdate:
            try:
                pubdate = time.strptime(pubdate, '%m/%d/%Y')
            except ValueError:
                pubdate = time.strptime(pubdate, '%Y/%m/%d')
            except Exception as e:
                print(e)
                sys.exit(-1)

        elif '-' in pubdate:
            try:
                pubdate = time.strptime(pubdate, '%Y-%m-%d')
            except ValueError:
                pubdate = time.strptime(pubdate, '%m-%d-%Y')
            except Exception as e:
                print(e)
                sys.exit(-1)

        else:
            print(link, pubdate)
            pubdate = time.strptime(pubdate, '%Y%m%d')
        pubdate = time.strftime('%Y-%m-%d %a', pubdate)
        return pubdate

    def gen_category(self, link=''):
        """ Filter Keywords from HTML metadata """
        html_data = BeautifulSoup(open(link, 'r').read(), 'html.parser')
        keywords_list = html_data.findAll('meta', {'name': 'keywords'})
        if keywords_list and 'content' in keywords_list[0].attrs.keys():
            keywords = keywords_list[0].attrs['content']
            return [ i.strip() for i in keywords.split(',') ]
        else:
            return [
             self.default_tag]

    def monitor_log(self, s=''):
        print('[Monitor] %s' % s)

    def monitor_kill(self):
        if self.process and self.process.is_alive():
            self.monitor_log('Kill process [%s]...' % self.process.pid)
            self.process.terminate()
            self.monitor_log('Process ended with code %s.' % self.process.exitcode)
            self.process = None
        return

    def monitor_restart(self, port='8080', filename=''):
        print('Watch: re-generate pages')
        self.homepage = 'http://localhost:' + port
        self.do_generate(self.homepage)

    def do_server(self, port='8080'):
        self.port = port
        self.monitor_path = self.source_dir
        observer = Observer()
        observer.schedule(OrgNoteFileSystemEventHander(self.monitor_restart, self.port), self.monitor_path, recursive=True)
        observer.start()
        self.monitor_log('Watching directory %s' % self.monitor_path)
        self.process = Process(target=self.monitor_start, args=(self.port,))
        self.process.daemon = True
        self.process.start()
        self.process.join()
        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            observer.stop()

        observer.join()

    def monitor_start(self, port):
        import sys
        if not os.path.exists(self.tags_dir):
            os.makedirs(self.tags_dir)
        self.port = port
        self.homepage = 'http://localhost:' + self.port
        self.do_generate(self.homepage)
        try:
            server_address = ('', int(self.port))
            if sys.version_info.major == 2:
                import SimpleHTTPServer, BaseHTTPServer
                server_class = BaseHTTPServer.HTTPServer
                handler_class = SimpleHTTPServer.SimpleHTTPRequestHandler
                curdir = os.getcwd()
                os.chdir(self.public_dir)
                BaseHTTPServer.test(handler_class, server_class)
                os.chdir(curdir)
            elif sys.version_info.major == 3:
                if sys.version_info >= (3, 7):
                    curdir = os.getcwd()
                    os.chdir(self.public_dir)
                    server_class = http.server.ThreadingHTTPServer
                    handler_class = partial(http.server.SimpleHTTPRequestHandler, directory=os.getcwd())
                    handler_class.protocol_version = 'HTTP/1.0'
                    with server_class(server_address, handler_class) as (httpd):
                        sa = httpd.socket.getsockname()
                        serve_message = 'Serving HTTP on {host} port {port} (http://{host}:{port}/) ...'
                        print(serve_message.format(host=sa[0], port=sa[1]))
                        try:
                            httpd.serve_forever()
                        except KeyboardInterrupt:
                            print('\nKeyboard interrupt received, exiting.')
                            os.chdir(curdir)
                            sys.exit(0)

                else:
                    server_class = http.server.HTTPServer
                    handler_class = http.server.SimpleHTTPRequestHandler
                    handler_class.protocol_version = 'HTTP/1.0'
                    curdir = os.getcwd()
                    os.chdir(self.public_dir)
                    httpd = server_class(server_address, handler_class)
                    sa = httpd.socket.getsockname()
                    print('Serving HTTP on', sa[0], 'port', sa[1], '...')
                    try:
                        httpd.serve_forever()
                    except KeyboardInterrupt:
                        print('\nKeyboard interrupt received, exiting.')
                        httpd.server_close()
                        os.chdir(curdir)
                        sys.exit(0)

        except Exception as ex:
            print(str(ex))
            usage()

    def public_theme(self):
        if not os.path.exists(self.public_dir):
            os.makedirs(self.public_dir)
        if os.path.exists('./theme'):
            os.system('rsync --quiet -av ./theme ./%s/' % self.public_dir)

    def public_images(self):
        if not os.path.exists(self.public_dir):
            os.makedirs(self.public_dir)
        if os.path.exists('%s%s' % (self.source_dir, self.images_dir)):
            os.system('rsync --quiet -av %s%s ./%s/' % (self.source_dir, self.images_dir, self.public_dir))
        if os.path.exists('%s%s' % (self.source_dir, self.files_dir)):
            os.system('rsync --quiet -av %s%s ./%s/' % (self.source_dir, self.files_dir, self.public_dir))

    def public_cname(self):
        if not os.path.exists(self.public_dir):
            os.makedirs(self.public_dir)
        if os.path.exists('%sCNAME' % self.source_dir):
            os.system('rsync --quiet -av %sCNAME ./%s/' % (self.source_dir, self.public_dir))

    def public_favicon(self):
        if not os.path.exists(self.public_dir):
            os.makedirs(self.public_dir)
        if os.path.exists('%sfavicon.ico' % self.source_dir):
            os.system('rsync --quiet -av %sfavicon.ico ./%s/' % (self.source_dir, self.public_dir))

    def do_deploy(self, branch='master'):
        if not self.deploy_url or self.deploy_type != 'git':
            print('Please add deploy repo git config info')
            return False
        import os, shutil
        if not os.path.exists(self.tags_dir):
            os.makedirs(self.tags_dir)
        os.system('rm -r %s/2*/' % self.public_dir)
        self.do_generate()
        curdir = os.getcwd()
        repodir = './%s/.repo' % self.public_dir
        if not os.path.exists(repodir):
            os.makedirs(repodir)
            os.chdir(repodir)
            os.system('git init && git remote add origin %s && git fetch && git pull origin %s' % (self.deploy_url, self.deploy_branch))
        else:
            os.chdir(repodir)
            os.system('git fetch && git pull origin %s' % self.deploy_branch)
        os.system("rsync -a --exclude='.repo/' ../ ./")
        os.system("git add . && git commit -m 'update' && git push origin %s" % self.deploy_branch)
        os.chdir(curdir)

    def do_generate(self, homepage='', batch=''):
        self.cfg.update()
        self.refresh_config(homepage)
        if not os.path.exists(self.tags_dir):
            os.makedirs(self.tags_dir)
        self.public_images()
        self.public_theme()
        self.public_cname()
        self.public_favicon()
        self.gen_notes(self.dirs)
        if batch == 'all':
            notes = [ note[0].replace('.html', '.org') for note in self.notes ]
            for note in notes:
                self.do_page(note)

        elif batch.endswith('.org') or batch.endswith('.md'):
            self.do_page(batch)
        elif batch.isdigit():
            notes = [ note[0].replace('.html', '.org') for note in self.notes ]
            for note in notes[:int(batch)]:
                self.do_page(note)

        self.gen_tag_list()
        self.gen_timetag_list()
        self.gen_public()
        self.gen_index()
        self.gen_about()
        self.gen_links()
        self.gen_archive()
        self.gen_tags()
        self.gen_tags_menu_page()
        self.gen_rss()
        self.gen_search()
        self.gen_timetags()
        self.gen_nopublic()
        self.gen_calendar()
        print('notes generate done')

    def do_new(self, notename=''):
        return util.add_note(notename, self.source_dir)

    def do_page(self, notename=''):
        if notename.endswith('.org') and not os.path.exist(notename):
            notename = notename.replace('.org', '.md')
        else:
            if notename.endswith('.md') and not os.path.exist(notename):
                notename = notename.replace('.md', '.org')
            print('working on :', notename)
            if notename.endswith('.org'):
                return util.to_page(notename)
            if notename.endswith('.md'):
                return util.to_page_mk2(notename)

    def do_recall(self, notename=''):
        import os.path
        publish_list = self.dirs[0]
        nopublish_list = self.dirs[1]
        publish_line = util.publish_note(notename, self.source_dir)
        if not publish_line:
            return
        else:
            link = publish_line.replace('.org', '.html').replace('.md', '.html')
            if publish_line == None:
                print('\x1b[31m[ERROR]\x1b[0m: Can not cancel note: %s, are you sure it exists?' % notename)
                return
            print(publish_line)
            if not os.path.exists(publish_list):
                data = []
            else:
                data = open(publish_list, 'r').readlines()
                data = [ i.strip() for i in data if not i.startswith('#') ]
            nopublish_data = open(nopublish_list, 'r').readlines()
            nopublish_data = [ i.strip() for i in nopublish_data if not i.startswith('#') ]
            if publish_line in data:
                data.remove(publish_line)
                output = open(publish_list, 'w')
                for line in data:
                    if line in nopublish_data:
                        continue
                    print(line, file=output)

                output.close()
            if publish_line in nopublish_data:
                nopublish_data.remove(publish_line)
                output = open(nopublish_list, 'w')
                for line in nopublish_data:
                    print(line, file=output)

                output.close()
            page_file = self.gen_public_link(link, self.public_dir)
            curdir = os.getcwd()
            repodir = './%s/.repo/' % self.public_dir
            repo_file = self.gen_public_link(link, repodir)
            filename = os.path.basename(repo_file)
            if not os.path.exists(self.tags_dir):
                os.makedirs(self.tags_dir)
            if os.path.exists(page_file):
                os.remove(page_file)
                print('\x1b[34m[Warning]\x1b[0m: delete %s done!' % page_file)
            if os.path.exists(repo_file):
                os.remove(repo_file)
                print('\x1b[34m[Warning]\x1b[0m: delete %s done!' % repo_file)
                os.chdir(repodir)
                os.system("git  commit -am 'recall %s' >/dev/null;git push origin %s >/dev/null" % (filename, self.deploy_branch))
                os.chdir(curdir)
            print('\x1b[34m[Info]\x1b[0m: Recall %s done!' % notename)
            return

    def do_publish(self, notename=''):
        import os.path
        publish_list = self.dirs[0]
        nopublish_list = self.dirs[1]
        publish_line = util.publish_note(notename, self.source_dir)
        if publish_line == None:
            print('\x1b[31m[ERROR]\x1b[0m: Can not publish note: %s, are you sure the html file exists?' % notename)
            return
        else:
            print(publish_line)
            nopublish_data = open(nopublish_list, 'r').readlines()
            nopublish_data = [ i.strip() for i in nopublish_data if not i.startswith('#') ]
            if not os.path.exists(publish_list):
                output = open(publish_list, 'w')
                print(publish_line, file=output)
                output.close()
            else:
                data = open(publish_list, 'r').readlines()
                data = [ i.strip() for i in data if not i.startswith('#') ]
                if publish_line in data or publish_line in nopublish_data:
                    print(' publish done')
                    return
                output = open(publish_list, 'w')
                print(publish_line, file=output)
                for line in data:
                    if line in nopublish_data:
                        continue
                    print(line, file=output)

                output.close()
            print('publish done')
            return

    def scan(self, note_dir=None):
        """
        scan the note_dir, build a dict with notes
        """
        if note_dir == None:
            note_dir = self.source_dir
        for path, dirs, files in os.walk(note_dir):
            if dirs:
                continue
            for _file in files:
                if not _file.endswith('.org') and not _file.endswith('.md'):
                    continue
                _path = path + '/' + _file
                if _path in [self.source_dir + 'public.org', self.source_dir + 'nopublic.org', self.source_dir + 'about.org']:
                    continue
                if _path.endswith('.html'):
                    continue
                self.notes_db[_path] = _path

        return

    def do_list(self):
        """
        list all notes
        """
        self.scan()
        for _note in reversed(sorted(self.notes_db.keys())):
            print(_note)

    def do_status(self):
        publish_list = self.dirs[0]
        nopublish_list = self.dirs[1]
        publish_data = open(publish_list, 'r').readlines()
        publish_data = [ i.strip() for i in publish_data if not i.startswith('#') ]
        nopublish_data = open(nopublish_list, 'r').readlines()
        nopublish_data = [ i.strip() for i in nopublish_data if not i.startswith('#') ]
        all_publish = True
        self.scan()
        for _note in reversed(sorted(self.notes_db.keys())):
            if _note.endswith('.org'):
                _html = _note.replace('.org', '.html')
            elif _note.endswith('.md'):
                _html = _note.replace('.md', '.html')
            else:
                _html = _note
            publish_line = util.publish_note(self.notes_db[_note], self.source_dir)
            if publish_line not in publish_data and publish_line not in nopublish_data:
                print('\x1b[34m[Warning]\x1b[0m: %s not publish yet!' % _note)
                all_publish = False

        if all_publish:
            print('all notes published!')


def usage():
    import sys
    print('\nUsage: orgnote <command>\n\nCommands:\n  init       Create a new OrgNote folder\n  new        Create a new .org post\n  list       List this blog notes\n  status     Status of those notes\n  publish    Publish a note\n  recall     Cancel publish a note\n  generate   Generate static files\n  server     Start the server\n  deploy     Deploy your website\n  help       Get help on a command\n  version    Display version information\n    \nFor more help, you can check the docs:  http://orgnote.readthedocs.org/zh_CN/latest/\n    ')
    sys.exit()


def main(args=None):
    import sys, os, orgnote, orgnote.parser, orgnote.init
    blog = orgnote.parser.OrgNote()
    if len(sys.argv) == 2:
        if sys.argv[1] == 'server':
            blog.do_server()
        elif sys.argv[1] == 'init':
            print('init....')
            orgnote.init.main()
        elif sys.argv[1] == 'deploy':
            blog.do_deploy()
        elif sys.argv[1] == 'version':
            print(orgnote.__version__)
        elif sys.argv[1] == 'generate':
            blog.do_generate()
        elif sys.argv[1] == 'list':
            blog.do_list()
        elif sys.argv[1] == 'status':
            blog.do_status()
        else:
            usage()
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'server':
            blog.do_server(sys.argv[2])
        elif sys.argv[1] == 'new':
            blog.do_new(sys.argv[2])
        elif sys.argv[1] == 'publish':
            blog.do_publish(sys.argv[2])
        elif sys.argv[1] == 'generate':
            blog.do_generate('http://localhost:' + sys.argv[2])
        elif sys.argv[1] == 'deploy':
            blog.do_deploy(sys.argv[2])
        elif sys.argv[1] == 'recall':
            blog.do_recall(sys.argv[2])
        else:
            usage()
    else:
        usage()


if __name__ == '__main__':
    import sys
    sys.exit(main())