# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/readme-renderer/readme_renderer/clean.py
# Compiled at: 2020-01-10 16:25:27
# Size of source mod 2**32: 2540 bytes
from __future__ import absolute_import, division, print_function
import functools, bleach, bleach.callbacks, bleach.linkifier, bleach.sanitizer
ALLOWED_TAGS = [
 'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol',
 'strong', 'ul',
 'br', 'caption', 'cite', 'col', 'colgroup', 'dd', 'del', 'details', 'div',
 'dl', 'dt', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'img', 'p', 'pre',
 'span', 'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'th', 'thead',
 'tr', 'tt', 'kbd', 'var']
ALLOWED_ATTRIBUTES = {'a':[
  'href', 'title'], 
 'abbr':[
  'title'], 
 'acronym':[
  'title'], 
 '*':[
  'id'], 
 'hr':[
  'class'], 
 'img':[
  'src', 'width', 'height', 'alt', 'align', 'class'], 
 'span':[
  'class'], 
 'th':[
  'align'], 
 'td':[
  'align'], 
 'code':[
  'class'], 
 'p':[
  'align']}
ALLOWED_STYLES = []

def clean(html, tags=None, attributes=None, styles=None):
    if tags is None:
        tags = ALLOWED_TAGS
    else:
        if attributes is None:
            attributes = ALLOWED_ATTRIBUTES
        if styles is None:
            styles = ALLOWED_STYLES
    cleaner = bleach.sanitizer.Cleaner(tags=tags,
      attributes=attributes,
      styles=styles,
      filters=[
     functools.partial((bleach.linkifier.LinkifyFilter),
       callbacks=[
      lambda attrs, new: attrs if not new else None,
      bleach.callbacks.nofollow],
       skip_tags=[
      'pre'],
       parse_email=False)])
    try:
        cleaned = cleaner.clean(html)
        return cleaned
    except ValueError:
        return