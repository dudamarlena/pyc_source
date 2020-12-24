# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/pytigon/pytigon/prj/_schwiki/schwiki/models.py
# Compiled at: 2020-04-19 16:01:02
# Size of source mod 2**32: 14131 bytes
import django
from django.db import models
from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *
import pytigon_lib.schdjangoext.fields as ext_models
import django.utils.translation as _
from django.contrib import admin
import os, os.path, sys
from pytigon_lib.schhtml.htmltools import superstrip
from django.template import RequestContext, Context, Template
import markdown2 as markdown
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schtools.wiki import wikify, wiki_from_str, make_href
from pytigon_lib.schtools.tools import norm_indent
from django.template.loader import select_template
from datetime import datetime
from collections import namedtuple
template_content = '\n{# -*- coding: utf-8 -*- #}\n{%% load exfiltry %%}\n{%% load exsyntax %%}\n%s\n'

def _get_wiki_object(page, buf, name, paragraf):
    name0 = name.split('_')[0]
    conf = None
    x = PageObjectsConf.objects.filter(name=name0)
    if len(x) > 0:
        conf = x[0]
        d = page.get_json_data()
        if name in d:
            c = d[name]
        else:
            c = ''
        inline_content = norm_indent(buf)
        if conf.inline_wiki:
            inline_content = html_from_wiki(page, inline_content)
        context = {'param':c,  'inline_content':inline_content,  'object':conf,  'page':page,  'paragraf':paragraf,  'name':name}
        if conf.view_dict:
            exec(conf.view_dict)
            context = locals()['get_view_dict'](context)
        template_name1 = (conf.app + '/' + conf.name).lower() + '_wikiobj_view.html'
        template_name2 = 'schwiki/wikiobj_view.html'
        t = select_template([template_name1, template_name2])
        return t.render(context).replace('[{', '{{').replace('}]', '}}').replace('[%', '{%').replace('%]', '%}')
    return ''


def _get_markdown_object(buf):
    return markdown.markdown(('\n'.join(buf)), extras=['tables', 'codehilite'])


def html_from_wiki--- This code section failed: ---

 L.  73         0  BUILD_LIST_0          0 
                2  STORE_DEREF              'document'

 L.  74         4  BUILD_LIST_0          0 
                6  STORE_DEREF              'paragraf'

 L.  75         8  BUILD_LIST_0          0 
               10  STORE_DEREF              'buf'

 L.  76        12  LOAD_CONST               False
               14  STORE_DEREF              'in_wiki_object'

 L.  77        16  LOAD_STR                 ''
               18  STORE_DEREF              'name'

 L.  79        20  LOAD_CONST               None
               22  STORE_DEREF              'paragraf_prefix'

 L.  80        24  LOAD_CONST               None
               26  STORE_DEREF              'paragraf_suffix'

 L.  81        28  BUILD_LIST_0          0 
               30  STORE_DEREF              'section_close_elements'

 L.  82        32  BUILD_LIST_0          0 
               34  STORE_DEREF              'document_close_elements'

 L.  84        36  LOAD_CLOSURE             'buf'
               38  LOAD_CLOSURE             'document'
               40  LOAD_CLOSURE             'in_wiki_object'
               42  LOAD_CLOSURE             'name'
               44  LOAD_CLOSURE             'page'
               46  LOAD_CLOSURE             'paragraf'
               48  LOAD_CLOSURE             'paragraf_prefix'
               50  LOAD_CLOSURE             'paragraf_suffix'
               52  BUILD_TUPLE_8         8 
               54  LOAD_CODE                <code_object write_papragraf>
               56  LOAD_STR                 'html_from_wiki.<locals>.write_papragraf'
               58  MAKE_FUNCTION_8          'closure'
               60  STORE_FAST               'write_papragraf'

 L. 114        62  LOAD_CLOSURE             'document'
               64  LOAD_CLOSURE             'section_close_elements'
               66  BUILD_TUPLE_2         2 
               68  LOAD_CODE                <code_object write_section>
               70  LOAD_STR                 'html_from_wiki.<locals>.write_section'
               72  MAKE_FUNCTION_8          'closure'
               74  STORE_FAST               'write_section'

 L. 120        76  LOAD_CLOSURE             'document'
               78  LOAD_CLOSURE             'document_close_elements'
               80  BUILD_TUPLE_2         2 
               82  LOAD_CODE                <code_object write_document>
               84  LOAD_STR                 'html_from_wiki.<locals>.write_document'
               86  MAKE_FUNCTION_8          'closure'
               88  STORE_FAST               'write_document'

 L. 126        90  LOAD_FAST                'wiki_str'
               92  LOAD_METHOD              replace
               94  LOAD_STR                 '\r'
               96  LOAD_STR                 ''
               98  CALL_METHOD_2         2  '2 positional arguments'
              100  LOAD_METHOD              split
              102  LOAD_STR                 '\n'
              104  CALL_METHOD_1         1  '1 positional argument'
              106  STORE_FAST               'lines'

 L. 127   108_110  SETUP_LOOP          528  'to 528'
              112  LOAD_FAST                'lines'
              114  GET_ITER         
          116_118  FOR_ITER            526  'to 526'
              120  STORE_FAST               'line'

 L. 128       122  LOAD_DEREF               'in_wiki_object'
          124_126  POP_JUMP_IF_FALSE   388  'to 388'

 L. 129       128  LOAD_FAST                'line'
              130  LOAD_METHOD              startswith
              132  LOAD_STR                 ' '
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_JUMP_IF_TRUE    152  'to 152'
              138  LOAD_FAST                'line'
              140  LOAD_METHOD              startswith
              142  LOAD_STR                 '\t'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  POP_JUMP_IF_TRUE    152  'to 152'
              148  LOAD_FAST                'line'
              150  POP_JUMP_IF_TRUE    166  'to 166'
            152_0  COME_FROM           146  '146'
            152_1  COME_FROM           136  '136'

 L. 130       152  LOAD_DEREF               'buf'
              154  LOAD_METHOD              append
              156  LOAD_FAST                'line'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          

 L. 131       162  CONTINUE            116  'to 116'
              164  JUMP_FORWARD        388  'to 388'
            166_0  COME_FROM           150  '150'

 L. 133       166  LOAD_GLOBAL              _get_wiki_object
              168  LOAD_DEREF               'page'
              170  LOAD_DEREF               'buf'
              172  LOAD_DEREF               'name'
              174  LOAD_DEREF               'paragraf_prefix'
              176  LOAD_DEREF               'paragraf_suffix'
              178  BUILD_LIST_2          2 
              180  CALL_FUNCTION_4       4  '4 positional arguments'
              182  STORE_FAST               'x'

 L. 135       184  LOAD_FAST                'x'
              186  LOAD_METHOD              startswith
              188  LOAD_STR                 '@@@'
              190  CALL_METHOD_1         1  '1 positional argument'
          192_194  POP_JUMP_IF_FALSE   258  'to 258'

 L. 136       196  LOAD_STR                 '|||'
              198  LOAD_FAST                'x'
              200  COMPARE_OP               in
              202  POP_JUMP_IF_FALSE   240  'to 240'

 L. 137       204  LOAD_FAST                'x'
              206  LOAD_CONST               3
              208  LOAD_CONST               None
              210  BUILD_SLICE_2         2 
              212  BINARY_SUBSCR    
              214  LOAD_METHOD              split
              216  LOAD_STR                 '|||'
              218  CALL_METHOD_1         1  '1 positional argument'
              220  STORE_FAST               'y'

 L. 138       222  LOAD_FAST                'y'
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  STORE_DEREF              'paragraf_prefix'

 L. 139       230  LOAD_FAST                'y'
              232  LOAD_CONST               1
              234  BINARY_SUBSCR    
              236  STORE_DEREF              'paragraf_suffix'
              238  JUMP_FORWARD        256  'to 256'
            240_0  COME_FROM           202  '202'

 L. 141       240  LOAD_FAST                'x'
              242  LOAD_CONST               3
              244  LOAD_CONST               None
              246  BUILD_SLICE_2         2 
              248  BINARY_SUBSCR    
              250  STORE_DEREF              'paragraf_prefix'

 L. 142       252  LOAD_STR                 ''
              254  STORE_DEREF              'paragraf_suffix'
            256_0  COME_FROM           238  '238'
              256  JUMP_FORWARD        380  'to 380'
            258_0  COME_FROM           192  '192'

 L. 144       258  LOAD_STR                 '|||'
              260  LOAD_FAST                'x'
              262  COMPARE_OP               in
          264_266  POP_JUMP_IF_FALSE   366  'to 366'

 L. 145       268  LOAD_STR                 '||||'
              270  LOAD_FAST                'x'
              272  COMPARE_OP               in
          274_276  POP_JUMP_IF_FALSE   322  'to 322'

 L. 146       278  LOAD_FAST                'x'
              280  LOAD_METHOD              split
              282  LOAD_STR                 '||||'
              284  CALL_METHOD_1         1  '1 positional argument'
              286  STORE_FAST               'y'

 L. 147       288  LOAD_DEREF               'paragraf'
              290  LOAD_METHOD              append
              292  LOAD_FAST                'y'
              294  LOAD_CONST               0
              296  BINARY_SUBSCR    
              298  LOAD_CONST               False
              300  BUILD_TUPLE_2         2 
              302  CALL_METHOD_1         1  '1 positional argument'
              304  POP_TOP          

 L. 148       306  LOAD_DEREF               'document_close_elements'
              308  LOAD_METHOD              append
              310  LOAD_FAST                'y'
              312  LOAD_CONST               1
              314  BINARY_SUBSCR    
              316  CALL_METHOD_1         1  '1 positional argument'
              318  POP_TOP          
              320  JUMP_FORWARD        364  'to 364'
            322_0  COME_FROM           274  '274'

 L. 150       322  LOAD_FAST                'x'
              324  LOAD_METHOD              split
              326  LOAD_STR                 '|||'
              328  CALL_METHOD_1         1  '1 positional argument'
              330  STORE_FAST               'y'

 L. 151       332  LOAD_DEREF               'paragraf'
              334  LOAD_METHOD              append
              336  LOAD_FAST                'y'
              338  LOAD_CONST               0
              340  BINARY_SUBSCR    
              342  LOAD_CONST               False
              344  BUILD_TUPLE_2         2 
              346  CALL_METHOD_1         1  '1 positional argument'
              348  POP_TOP          

 L. 152       350  LOAD_DEREF               'section_close_elements'
              352  LOAD_METHOD              append
              354  LOAD_FAST                'y'
              356  LOAD_CONST               1
              358  BINARY_SUBSCR    
              360  CALL_METHOD_1         1  '1 positional argument'
              362  POP_TOP          
            364_0  COME_FROM           320  '320'
              364  JUMP_FORWARD        380  'to 380'
            366_0  COME_FROM           264  '264'

 L. 154       366  LOAD_DEREF               'paragraf'
              368  LOAD_METHOD              append
              370  LOAD_FAST                'x'
              372  LOAD_CONST               False
              374  BUILD_TUPLE_2         2 
              376  CALL_METHOD_1         1  '1 positional argument'
              378  POP_TOP          
            380_0  COME_FROM           364  '364'
            380_1  COME_FROM           256  '256'

 L. 156       380  BUILD_LIST_0          0 
              382  STORE_DEREF              'buf'

 L. 157       384  LOAD_CONST               False
              386  STORE_DEREF              'in_wiki_object'
            388_0  COME_FROM           164  '164'
            388_1  COME_FROM           124  '124'

 L. 159       388  LOAD_FAST                'line'
              390  LOAD_METHOD              startswith
              392  LOAD_STR                 '@'
              394  CALL_METHOD_1         1  '1 positional argument'
          396_398  POP_JUMP_IF_FALSE   456  'to 456'

 L. 160       400  LOAD_DEREF               'buf'
          402_404  POP_JUMP_IF_FALSE   420  'to 420'

 L. 162       406  LOAD_DEREF               'paragraf'
              408  LOAD_METHOD              append
              410  LOAD_DEREF               'buf'
              412  LOAD_CONST               True
              414  BUILD_TUPLE_2         2 
              416  CALL_METHOD_1         1  '1 positional argument'
              418  POP_TOP          
            420_0  COME_FROM           402  '402'

 L. 163       420  BUILD_LIST_0          0 
              422  STORE_DEREF              'buf'

 L. 164       424  LOAD_CONST               True
              426  STORE_DEREF              'in_wiki_object'

 L. 165       428  LOAD_FAST                'line'
              430  LOAD_METHOD              split
              432  LOAD_STR                 ':'
              434  CALL_METHOD_1         1  '1 positional argument'
              436  LOAD_CONST               0
              438  BINARY_SUBSCR    
              440  LOAD_CONST               1
              442  LOAD_CONST               None
              444  BUILD_SLICE_2         2 
              446  BINARY_SUBSCR    
              448  LOAD_METHOD              strip
              450  CALL_METHOD_0         0  '0 positional arguments'
              452  STORE_DEREF              'name'
              454  JUMP_BACK           116  'to 116'
            456_0  COME_FROM           396  '396'

 L. 166       456  LOAD_FAST                'line'
              458  LOAD_METHOD              startswith
              460  LOAD_STR                 '...'
              462  CALL_METHOD_1         1  '1 positional argument'
          464_466  POP_JUMP_IF_TRUE    480  'to 480'
              468  LOAD_FAST                'line'
              470  LOAD_METHOD              startswith
              472  LOAD_STR                 '+++'
              474  CALL_METHOD_1         1  '1 positional argument'
          476_478  POP_JUMP_IF_FALSE   514  'to 514'
            480_0  COME_FROM           464  '464'

 L. 167       480  LOAD_FAST                'write_papragraf'
              482  CALL_FUNCTION_0       0  '0 positional arguments'
              484  POP_TOP          

 L. 168       486  LOAD_FAST                'line'
              488  LOAD_METHOD              startswith
              490  LOAD_STR                 '+++'
              492  CALL_METHOD_1         1  '1 positional argument'
          494_496  POP_JUMP_IF_FALSE   524  'to 524'

 L. 169       498  LOAD_FAST                'write_section'
              500  CALL_FUNCTION_0       0  '0 positional arguments'
              502  POP_TOP          

 L. 170       504  LOAD_STR                 ''
              506  STORE_DEREF              'paragraf_prefix'

 L. 171       508  LOAD_STR                 ''
              510  STORE_DEREF              'paragraf_suffix'
              512  JUMP_BACK           116  'to 116'
            514_0  COME_FROM           476  '476'

 L. 173       514  LOAD_DEREF               'buf'
              516  LOAD_METHOD              append
              518  LOAD_FAST                'line'
              520  CALL_METHOD_1         1  '1 positional argument'
              522  POP_TOP          
            524_0  COME_FROM           494  '494'
              524  JUMP_BACK           116  'to 116'
              526  POP_BLOCK        
            528_0  COME_FROM_LOOP      108  '108'

 L. 175       528  LOAD_FAST                'write_papragraf'
              530  CALL_FUNCTION_0       0  '0 positional arguments'
              532  POP_TOP          

 L. 176       534  LOAD_FAST                'write_section'
              536  CALL_FUNCTION_0       0  '0 positional arguments'
              538  POP_TOP          

 L. 177       540  LOAD_FAST                'write_document'
              542  CALL_FUNCTION_0       0  '0 positional arguments'
              544  POP_TOP          

 L. 179       546  LOAD_STR                 '\n'
              548  LOAD_METHOD              join
              550  LOAD_DEREF               'document'
              552  CALL_METHOD_1         1  '1 positional argument'
              554  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 166_0


page_type_choices = (('W', 'Wiki'), ('I', 'Indent html'), ('H', 'Html'))

class PageObjectsConf(models.Model):

    class Meta:
        verbose_name = _('Page objects configurations')
        verbose_name_plural = _('Page objects configurations')
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schwiki'
        ordering = [
         'id']

    app = models.CharField('Application', null=False, blank=False, editable=True, max_length=32)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=128)
    inline_editing = ext_models.NullBooleanField('Inline editing', null=False, blank=False, editable=True, default=False)
    inline_wiki = ext_models.NullBooleanField('Inline wiki', null=False, blank=False, editable=True, default=False)
    edit_form = models.TextField('Edit form', null=True, blank=True, editable=False)
    load_fun = models.TextField('Load function', null=True, blank=True, editable=False)
    save_fun = models.TextField('Save function', null=True, blank=True, editable=False)
    view_dict = models.TextField('Get view dict function', null=True, blank=True, editable=False)
    doc = models.TextField('Documentaction', null=True, blank=True, editable=False)

    def __str__(self):
        return self.name


admin.site.register(PageObjectsConf)

class Page(JSONModel):

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Page')
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schwiki'
        ordering = [
         'id']

    subject = models.CharField('Subject', null=False, blank=False, editable=True, max_length=64)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=64)
    content_src = models.TextField('Content source', null=True, blank=True, editable=False)
    content = models.TextField('Content', null=True, blank=True, editable=False)
    base_template = models.CharField('Base template', null=True, blank=True, editable=True, max_length=64)
    rights_group = models.CharField('Rights group', null=True, blank=True, editable=True, max_length=64)
    menu = models.CharField('Menu', null=True, blank=True, editable=True, max_length=64)
    operator = models.CharField('Operator', null=True, blank=True, editable=False, max_length=64)
    update_time = models.DateTimeField('Update time', null=False, blank=False, editable=False, default=(datetime.now))
    published = ext_models.NullBooleanField('Published', null=False, blank=False, editable=False, default=False)
    latest = ext_models.NullBooleanField('Latest', null=False, blank=False, editable=False, default=True)

    def save_from_request(self, request, view_type, param):
        if 'direct_save' in request.POST:
            super(Page, self).save()
        else:
            conf_list = WikiConf.objects.filter(subject=(self.subject))
            conf_exists = False
            if len(conf_list) > 0:
                conf = conf_list[0]
                conf_exists = True
                if conf.backup_copies > 0:
                    pages = Page.objects.filter(subject=(self.subject), name=(self.name)).update(latest=False)
                    obj_to_save = Page()
                    obj_to_save.subject = self.subject
                    obj_to_save.name = self.name
                    obj_to_save.description = self.description
                    obj_to_save.content_src = self.content_src
                    obj_to_save.content = self.content
                    obj_to_save.base_template = self.base_template
                    obj_to_save.rights_group = self.rights_group
                    obj_to_save.menu = self.menu
                    obj_to_save.operator = self.operator
                    obj_to_save.update_time = self.update_time
                    obj_to_save.jsondata = self.jsondata
                    obj_to_save.published = False
                    obj_to_save.latest = True
                    obj_to_save.operator = request.user.username
                    obj_to_save.update_time = datetime.now()
                    obj_to_save.save()
                    pages = Page.objects.filter(subject=(self.subject), name=(self.name)).order_by('update_time')
                    if len(pages) > conf.backup_copies:
                        to_delete_count = len(pages) - conf.backup_copies
                        to_delete = []
                        for pos in pages:
                            if not pos.published:
                                if not pos.latest:
                                    to_delete.append(pos)
                                    to_delete_count -= 1
                                if to_delete_count <= 0:
                                    break

                        if to_delete:
                            for pos2 in to_delete:
                                pos2.delete()

                    return
            self.operator = request.user.username
            self.update_time = datetime.now()
            self.latest = True
            if not conf_exists:
                self.published = True
            self.save()

    def save(self, *args, **kwargs):
        (super(Page, self).save)(*args, **kwargs)
        if self.content_src:
            content = html_from_wiki(self, self.content_src + '\n\n\n&nbsp;')
        else:
            content = ''
        self.content = content
        (super(Page, self).save)(*args, **kwargs)

    def transform_template_name(self, request, template_name):
        return 'schwiki/edit_wiki_content.html'

    def get_page_for_wiki(self, wiki_str, user=None):
        wiki_word = wiki_from_str(wiki_str)
        return Page.get_page(user, self.subject, wiki_word)

    def get_href(self, path=None):
        return make_href((self.description if self.description else self.name), new_win=False, section=(self.subject), path=path)

    @staticmethod
    def get_page(request_or_username, subject, name):
        if type(request_or_username) == str:
            username = request_or_username
        else:
            if request_or_username.user:
                username = request_or_username.user.username
            else:
                username = None
        objs = None
        if username:
            objs = Page.objects.filter(subject=subject, name=name, operator=username, latest=True)
        if not objs or len(objs) == 0:
            objs = Page.objects.filter(subject=subject, name=name, published=True)
        if not objs or len(objs) == 0:
            objs = Page.objects.filter(subject=subject, name=name)
        if len(objs) > 0:
            return objs[0]
        return

    def __str__(self):
        return self.name


admin.site.register(Page)

class WikiConf(JSONModel):

    class Meta:
        verbose_name = _('Wiki config')
        verbose_name_plural = _('Wiki config')
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schwiki'
        ordering = [
         'id']

    subject = models.CharField('Wiki subject', null=False, blank=False, editable=True, max_length=64)
    group_of_rights_to_view = models.CharField('A group of rights to view wiki', null=True, blank=True, editable=True, max_length=64)
    group_of_rights_to_edit = models.CharField('A group of rights to edit wiki', null=True, blank=True, editable=True, max_length=64)
    backup_copies = models.IntegerField('Number of backup copies', null=False, blank=False, editable=True)
    publish_fun = models.TextField('Function called after publishing', null=True, blank=True, editable=False)
    scss = models.TextField('Additional scss styles', null=True, blank=True, editable=False)
    css = models.TextField('Css styles', null=True, blank=True, editable=False)

    def get_css(self):
        import sass
        if self.scss:
            buf = self.scss.replace('page_class', 'wiki_' + self.subject.lower())
            style = sass.compile(string=buf, indented=True)
            return style
        return ''

    def save(self, *args, **kwargs):
        self.css = self.get_css()
        ret = (super().save)(*args, **kwargs)
        return ret


admin.site.register(WikiConf)