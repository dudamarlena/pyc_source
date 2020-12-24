# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/DATA/Proyectos en Python/django-unsplash/unsplash/templatetags/unsplash_tags.py
# Compiled at: 2018-12-31 10:28:08
# Size of source mod 2**32: 2448 bytes
from django import template
from django.shortcuts import get_object_or_404
from ..models import UnsplashPhoto, Slideshow, Separator
from collections import namedtuple
import os
register = template.Library()

@register.inclusion_tag('includes/image.html')
def uphoto(alias):
    Image = namedtuple('Image', 'src alt classes')
    photo = get_object_or_404(UnsplashPhoto, photo_alias=alias)
    i = Image(src=photo.url, alt=photo.photo_alias, classes='')
    return {'image': i}


@register.inclusion_tag('includes/slideshow.html')
def uslideshow(slideshow_name):
    slideshow = get_object_or_404(Slideshow, name=slideshow_name)
    return {'slideshow': slideshow, 
     'slides': slideshow.slides.order_by('slideshowslide')}


@register.inclusion_tag('includes/parallax.html')
def uparallax(photo_alias, fixed=False, top_separator_name=None, bot_separator_name=None):
    photo = get_object_or_404(UnsplashPhoto, photo_alias=photo_alias)
    return {'photo': photo, 
     'fixed': fixed, 
     'top_separator_name': top_separator_name, 
     'bot_separator_name': bot_separator_name}


@register.simple_tag
def random_photo(size):
    return UnsplashPhoto.random(size)


@register.inclusion_tag('includes/separator.html')
def useparator(separator_name, top=True):
    sep = get_object_or_404(Separator, name=separator_name)
    sep_f = sep.svg_file.svg_file
    return {'separator_name': sep.name, 
     'separator_svg': sep_f.read().decode(), 
     'separator_style': sep.css, 
     'top': top}


@register.filter
def subtract(value, arg):
    return value - arg