# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/dev-p5qc/workspace/python/team_reset/ninecms/templatetags/ninecms_extras.py
# Compiled at: 2015-04-06 08:32:29
""" NineCMS custom template filters and tags """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings
from subprocess import check_output, call
import os
register = template.Library()

@register.filter
@stringfilter
def image_style(url, style):
    """ Return the url of different image style
    Construct appropriately if not exist
    See 9cms-crop.odt

    Assumptions:
    - Works only for Linux OS; double slashes are anyway ignored
    - MEDIA_URL is local (url is in form MEDIA_URL.. (eg /media/..) and this is in BASE_DIR
      Anyway if in remote, how to create images

    :param url: An image url
    :param style: Specify style to return image
    :return: image url of specified style
    """
    path_file_name = settings.BASE_DIR + url
    style_url_path = ('/').join((os.path.dirname(url), style))
    style_url = ('/').join((style_url_path, os.path.basename(url)))
    style_path = settings.BASE_DIR + style_url_path
    style_path_file_name = settings.BASE_DIR + style_url
    style_def = settings.IMAGE_STYLES[style]
    if not os.path.exists(style_path_file_name):
        if not os.path.exists(style_path):
            os.makedirs(style_path)
        by = chr(120)
        plus = chr(43)
        source_size_str = str(check_output(['identify', path_file_name])).split(' ')[2]
        source_size_array = source_size_str.split(by)
        source_size_x = int(source_size_array[0])
        source_size_y = int(source_size_array[1])
        target_size_x = style_def['size'][0]
        target_size_y = style_def['size'][1]
        target_size_str = str(target_size_x) + by + str(target_size_y)
        if style_def['type'] == 'thumbnail':
            if target_size_x > source_size_x and target_size_y > source_size_y:
                target_size_str = source_size_str
            call(['convert', path_file_name, '-thumbnail', target_size_str, '-antialias', style_path_file_name])
        elif style_def['type'] == 'thumbnail-upscale':
            call(['convert', path_file_name, '-thumbnail', target_size_str, '-antialias', style_path_file_name])
        elif style_def['type'] == 'crop-thumbnail':
            source_ratio = float(source_size_x) / float(source_size_y)
            target_ratio = float(target_size_x) / float(target_size_y)
            if source_ratio > target_ratio:
                crop_target_size_x = int(source_size_y * target_ratio)
                crop_target_size_y = source_size_y
                offset = (source_size_x - crop_target_size_x) / 2
                crop_size_str = str(crop_target_size_x) + by + str(crop_target_size_y) + plus + str(offset) + plus + '0'
            else:
                crop_target_size_x = source_size_x
                crop_target_size_y = int(source_size_x / target_ratio)
                offset = (source_size_y - crop_target_size_y) / 2
                crop_size_str = str(crop_target_size_x) + by + str(crop_target_size_y) + plus + '0' + plus + str(offset)
            call(['convert', path_file_name, '-crop', crop_size_str, style_path_file_name])
            call(['convert', style_path_file_name, '-thumbnail', target_size_str, '-antialias', style_path_file_name])
    return style_url


@register.filter
@stringfilter
def image_style_form(url, style):
    """ Return the url of an image style when given url is form image field value
    :param url: An image url from form image field value
    :param style: Specify style to return image
    :return: image url of specified style
    """
    return image_style(settings.MEDIA_URL + url, style)


@register.filter
def library(name):
    """ Check if a library is enabled in settings
    :param name: the library name to check
    :return: a boolean value
    """
    return name in settings.LIBRARIES