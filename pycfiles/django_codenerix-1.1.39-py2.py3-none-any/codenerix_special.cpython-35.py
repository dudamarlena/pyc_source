# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/templatetags/codenerix_special.py
# Compiled at: 2017-12-18 07:03:26
# Size of source mod 2**32: 3912 bytes
import hashlib
from PIL import Image, ImageDraw, ImageFont
from os import path
from django.template import Library
from django.conf import settings
from django import template
from django.template import Variable, NodeList
from django.contrib.auth.models import Group
register = Library()

@register.filter
def txt2img(text, FontSize=14, bg='#ffffff', fg='#000000', font='FreeMono.ttf'):
    font_dir = settings.MEDIA_ROOT + '/txt2img/'
    img_name_temp = text + '-' + bg.strip('#') + '-' + fg.strip('#') + '-' + str(FontSize)
    try:
        img_name_encode = hashlib.md5(img_name_temp).hexdigest()
    except TypeError:
        img_name_temp = bytes(img_name_temp, encoding='utf-8')
        img_name_encode = hashlib.md5(img_name_temp).hexdigest()

    img_name = '%s.jpg' % img_name_encode
    if path.exists(font_dir + img_name):
        pass
    else:
        font_size = FontSize
        fnt = ImageFont.truetype(font_dir + font, font_size)
        w, h = fnt.getsize(text)
        img = Image.new('RGBA', (w, h), bg)
        draw = ImageDraw.Draw(img)
        draw.fontmode = '0'
        draw.text((0, 0), text, font=fnt, fill=fg)
        img.save(font_dir + img_name, 'JPEG', quality=100)
    imgtag = '<img src="' + settings.MEDIA_URL + 'txt2img/' + img_name + '" alt="' + text + '" />'
    return imgtag


@register.tag
def ifusergroup(parser, token):
    """ Check to see if the currently logged in user belongs to a specific
    group. Requires the Django authentication contrib app and middleware.

    Usage: {% ifusergroup Admins %} ... {% endifusergroup %}, or
           {% ifusergroup Admins Clients Sellers %} ... {% else %} ... {% endifusergroup %}

    """
    try:
        tokensp = token.split_contents()
        groups = []
        groups += tokensp[1:]
    except ValueError:
        raise template.TemplateSyntaxError("Tag 'ifusergroup' requires at least 1 argument.")

    nodelist_true = parser.parse(('else', 'endifusergroup'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(tuple(['endifusergroup']))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return GroupCheckNode(groups, nodelist_true, nodelist_false)


class GroupCheckNode(template.Node):

    def __init__(self, groups, nodelist_true, nodelist_false):
        self.groups = groups
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        user = Variable('user').resolve(context)
        if not user.is_authenticated:
            return self.nodelist_false.render(context)
        else:
            allowed = False
            for checkgroup in self.groups:
                try:
                    group = Group.objects.get(name=checkgroup)
                except Group.DoesNotExist:
                    break

                if group in user.groups.all():
                    allowed = True
                    break

            if allowed:
                return self.nodelist_true.render(context)
            return self.nodelist_false.render(context)