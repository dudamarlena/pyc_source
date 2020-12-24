# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dr/Documents/code/Python/vps-manager/web/ui.py
# Compiled at: 2019-05-28 23:31:28
# Size of source mod 2**32: 9337 bytes
import tornado.web, os
J = os.path.join
FILES = J(J(os.path.dirname(__file__), 'static'), 'files')

class Card(tornado.web.UIModule):

    def render(self, title, img_url='images/hat.png', content='...', html=None):
        return self.render_string('template/ui_templates/card.html', title=title,
          img_url=img_url,
          html=html,
          content=content)

    def embedded_css(self):
        return '\n            .card-container {\n                background: #ebebeb;\n                margin:10px;\n                border-radius: 25px;\n            }\n\n            .card-container > .card {\n                background: #fafafa;\n                border: 2px solid white;\n                border-radius: 20px;\n                margin: 2px;\n            }\n\n            .card > img {\n                width: 60px;\n                height: 60px;\n                float: left;\n                margin-right: 30px;\n                margin-bottom: 30px;\n                padding: 4px;\n                border: 2px solid #fff;\n                background: rgb(229, 229, 229);\n\n            }\n        '


class Inputs(tornado.web.UIModule):
    __doc__ = '\n    type: horizontal/ inline . this will be parse to form-horizontal/ form-inline in bootstrap\n    '
    types = ('text', 'file', 'email', 'submit', 'button', 'checkbox', 'password')

    def classify(self, name):
        res = name.split(':')
        if len(res) == 2:
            tpe, name = res
            if tpe not in Inputs.types:
                name, v = res
                return [
                 'text', name, v]
            else:
                return [
                 tpe, name, '']
        else:
            if len(res) == 3:
                tpe, name, value = res
                if tpe not in Inputs.types:
                    raise Exception('not found input type %s' % tpe)
                return [
                 tpe, name, value]
        if len(res) == 1:
            return [
             'text', res[0], '']

    def render(self, *inputs, type='normal', title=None, form_type='horizontal', action='#', method='post'):
        inputs = [self.classify(input) for input in inputs]
        return self.render_string('template/ui_templates/{t}_inputs.html'.format(t=type), inputs=inputs,
          type=form_type,
          title=title,
          action=action,
          method=method)


class Table(tornado.web.UIModule):

    def rows(self, head_num, items):
        body = [[items[(ii * head_num + i)] for i in range(head_num)] for ii in range(int(len(items) / head_num))]
        if len(items) % head_num != 0:
            yu = len(items) % head_num
            all_len = len(items)
            return body + [[items[i] for i in range(all_len - yu, all_len)]]
        else:
            return body

    def render(self, table_headers, *table_items, type='normal', title='', table_type='striped'):
        items = self.rows(len(table_headers), table_items)
        return self.render_string('template/ui_templates/{t}_table.html'.format(t=type), headers=table_headers,
          items=items,
          type=table_type,
          title=title)


class Nav(tornado.web.UIModule):
    __doc__ = "\n    items example:\n        [{\n            'txt':'xxx',\n            'link': '/index',\n            'active': '1',\n            'tq': '1'\n        },\n        {\n            'txt':'xxx',\n            'link': '/url',\n\n        },\n        {\n            'txt':'xxx',\n            'link': '/index2',\n        }]\n    "

    def render(self, items, type='normal', title='Dashboard', nav_type='stacked'):
        return self.render_string('template/ui_templates/{t}_nav.html'.format(t=type), items=items,
          type=nav_type,
          title=title)

    def embedded_css(self):
        return '\n.tq{\n    padding-left: 15px;\n    padding-right: 15px;\n    margin-bottom: 5px;\n    font-size: 85%;\n    font-weight: 100;\n    letter-spacing: 1px;\n    color: #51586a;\n    text-transform: uppercase;\n\n}\n\n.nav > li > a{\n    position: relative;\n    display: block;\n    padding: 7px 15px 7px ;\n    padding-left: 27px;\n    border-radius: 4px;\n}\n\n.nav > li.active > a {\n    color: #252830;\n    background-color: #e5e5e5;\n}\nli.divider{\n    width: 70%;\n    align-self: center;\n    align-content: center;\n    left:10%;\n    height: 1px;\n    margin: 9px 1px;*\n    margin: -5px 0 5px;\n    overflow: hidden;\n    bottom:10px;\n    background-color: #e5e5e5;\n    border-bottom: 1px solid #e5e5e5;\n}\n        '


class Files(Nav):
    __doc__ = '\n    items example:\n        Files(file_path)\n    '

    def get_len(self, f):
        l = os.stat(os.path.join(FILES, f)).st_size
        s = '%f B' % float(l)
        if l / 1024 > 1:
            s = '%2.2f KB' % float(l / 1024)
        else:
            return s
            if l / 1048576 > 1:
                s = '%2.2f MB' % float(l / 1048576)
            else:
                return s
            if l / 1073741824 > 1:
                s = '%2.2f GB' % float(l / 1073741824)
            else:
                return s

    def render(self, type='normal', title='Dashboard', nav_type='stacked'):
        ss = [{'txt':f,  'link':'/static/files/' + f,  'code':f.split('.').pop() + '[%s]' % self.get_len(f)} for f in os.listdir(FILES)]
        return super().render(ss, type=type, title=title, nav_type=nav_type)


class LMap(tornado.web.UIModule):
    __doc__ = '\n    this is a map plugin , based on leaflet\n    '

    def render(self, id, host, height=460):
        return self.render_string('template/ui_templates/plugin-map.html', id=id,
          host=host,
          height=height)


class LEarth(tornado.web.UIModule):
    __doc__ = '\n    this is a earth plugin , based on leaflet\n    '

    def render(self, id, height=360, width=760):
        return self.render_string('template/ui_templates/plugin-earth.html', id=id,
          w=width,
          h=height)


class LGeoControl(tornado.web.UIModule):
    __doc__ = '\n    this is a controller to controll geo.\n    '

    def render(self, host='localhost:8080/mapapi', earth='earth', map='lmap'):
        return self.render_string('template/ui_templates/plugin-geo-control.html', host=host,
          map=map,
          earth=earth)


class BaseUI(tornado.web.UIModule):

    def render(self, Id='', Class='', Style='', content='Hello world', Base='div', **kargs):
        if hasattr(self, 'patch'):
            content = (self.patch)(**kargs)
        if hasattr(self, 'Base'):
            Base = self.Base
        return self.render('template/ui_templates/plugin-base.html', Id=Id,
          B=Base,
          Class=Class,
          Style=Style,
          content=content)


class List(BaseUI):
    __doc__ = '\nlist for item\n    '

    def patch(self, **kargs):
        self.Base = 'ul'


class TModal(tornado.web.UIModule):

    def render(self, content, Title='Title', foot='', Id='', Class='', Style=''):
        return self.render_string('template/ui_templates/plugin-modal.html', Id=Id,
          Title=Title,
          Class=Class,
          Style=Style,
          Content=content,
          Foot=foot)


class Loading(tornado.web.UIModule):
    __doc__ = '\n    loading plugin to display\n    '

    def render(self, target):
        return self.render_string('template/ui_templates/plugin_loading_circle.html', target=target)


class Collections(tornado.web.UIModule):
    __doc__ = '\nthis is a collections by bootstrap js conponent.\n    '

    def render(self, content, Id='', Class='collapse', Style=''):
        return self.render_string('template/ui_templates/plugin-collections.html', Id=Id,
          Class=Class,
          Style=Style,
          content=content)


class SaoMenuList(tornado.web.UIModule):
    __doc__ = '\nthis is a menu of SAO theme.\n    '

    def render(self, *items, Id=''):
        for i in items:
            assert 'id' in i
            assert 'name' in i

        return self.render_string('template/ui_templates/sao-menu.html', Id=Id,
          items=items)


class SaoPanel(tornado.web.UIModule):

    def render(self, content, title='Title', Id='', Class=''):
        return self.render_string('template/ui_templates/sao-panel.html', Id=Id,
          Class=Class,
          content=content,
          title=title)