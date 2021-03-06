# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/tinymce/compressor.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 4786 bytes
"""
Based on "TinyMCE Compressor PHP" from MoxieCode.

http://tinymce.moxiecode.com/

Copyright (c) 2008 Jason Davies
Licensed under the terms of the MIT License (see LICENSE.txt)
"""
from datetime import datetime
import os, re
from django.conf import settings
import django.core.cache as cache
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers, patch_response_headers
import tendenci.libs.tinymce.settings as tinymce_settings
safe_filename_re = re.compile('^[a-zA-Z][a-zA-Z0-9_/-]*$')

def get_file_contents(filename):
    if 'staticfiles' in settings.INSTALLED_APPS or 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
        from django.contrib.staticfiles import finders
        file_path = finders.find(os.path.join('tiny_mce', filename))
    else:
        file_path = os.path.join(tinymce_settings.JS_ROOT, filename)
    try:
        f = open(file_path)
        try:
            return f.read()
        finally:
            f.close()

    except IOError:
        return ''


def split_commas(str):
    if str == '':
        return []
    return str.split(',')


def gzip_compressor(request):
    plugins = split_commas(request.GET.get('plugins', ''))
    languages = split_commas(request.GET.get('languages', ''))
    themes = split_commas(request.GET.get('themes', ''))
    isJS = request.GET.get('js', '') == 'true'
    compress = request.GET.get('compress', 'true') == 'true'
    suffix = request.GET.get('suffix', '') == '_src' and '_src' or ''
    content = []
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    if not isJS:
        response.write(render_to_string(template_name='tinymce/tiny_mce_gzip.js', context={'base_url': tinymce_settings.JS_BASE_URL},
          request=request))
        return response
    patch_vary_headers(response, ['Accept-Encoding'])
    now = datetime.utcnow()
    response['Date'] = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    cacheKey = '|'.join(plugins + languages + themes)
    cacheData = cache.get(cacheKey)
    if cacheData is not None:
        if 'ETag' in cacheData:
            if_none_match = request.META.get('HTTP_IF_NONE_MATCH', None)
            if if_none_match == cacheData['ETag']:
                response.status_code = 304
                response.content = ''
                response['Content-Length'] = '0'
                return response
        if 'Last-Modified' in cacheData:
            if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE', None)
            if if_modified_since == cacheData['Last-Modified']:
                response.status_code = 304
                response.content = ''
                response['Content-Length'] = '0'
                return response
    content.append("var tinyMCEPreInit={base:'%s',suffix:''};" % tinymce_settings.JS_BASE_URL)
    files = [
     'tiny_mce']
    for lang in languages:
        files.append('langs/%s' % lang)

    for plugin in plugins:
        files.append('plugins/%s/editor_plugin%s' % (plugin, suffix))
        for lang in languages:
            files.append('plugins/%s/langs/%s' % (plugin, lang))

    for theme in themes:
        files.append('themes/%s/editor_template%s' % (theme, suffix))
        for lang in languages:
            files.append('themes/%s/langs/%s' % (theme, lang))

    for f in files:
        if not safe_filename_re.match(f):
            continue
        content.append(get_file_contents('%s.js' % f))

    content.append('tinymce.each("%s".split(","), function(f){tinymce.ScriptLoader.markDone(tinyMCE.baseURL+"/"+f+".js");});' % ','.join(files))
    unicode_content = []
    for i, c in enumerate(content):
        try:
            unicode_content.append(c.decode('latin-1'))
        except UnicodeDecodeError:
            try:
                unicode_content.append(c.decode('utf-8'))
            except:
                print('%s is nor latin-1 nor utf-8.' % files[i])
                raise

    if compress:
        content = compress_string(''.join([c.encode('utf-8') for c in unicode_content]))
        response['Content-Encoding'] = 'gzip'
        response['Content-Length'] = str(len(content))
    response.write(content)
    timeout = 864000
    patch_response_headers(response, timeout)
    cache.set(cacheKey, {'Last-Modified':response['Last-Modified'], 
     'ETag':response.get('ETag', '')})
    return response