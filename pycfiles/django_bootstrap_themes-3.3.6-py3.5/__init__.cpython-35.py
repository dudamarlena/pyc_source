# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bootstrap_themes/__init__.py
# Compiled at: 2016-03-24 10:20:11
# Size of source mod 2**32: 994 bytes
from django.contrib.staticfiles.storage import staticfiles_storage
available_themes = (('default', 'Default'), ('amelia', 'Amelia'), ('cerulean', 'Cerulean'),
                    ('cosmo', 'Cosmo'), ('cyborg', 'Cyborg'), ('flatly', 'Flatly'),
                    ('journal', 'Journal'), ('readable', 'Readable'), ('simplex', 'Simplex'),
                    ('slate', 'Slate'), ('spacelab', 'SpaceLab'), ('united', 'United'),
                    ('superhero', 'Superhero'), ('lumen', 'Lumen'))

def list_themes():
    return available_themes


def get_script(use_min=True):
    minified = ''
    if use_min:
        minified = '.min'
    return staticfiles_storage.url('bootstrap/js/bootstrap%(minified)s.js' % dict(minified=minified))


def get_styles(theme='default', subdir='css', fileext='min.css'):
    if not theme or theme == '':
        theme = 'default'
    return staticfiles_storage.url('bootstrap/themes/%(theme)s/%(subdir)s/bootstrap.%(fileext)s' % dict(theme=theme, subdir=subdir, fileext=fileext))