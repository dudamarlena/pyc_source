# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/utils/misc.py
# Compiled at: 2012-02-14 23:34:00
from django.template.defaultfilters import slugify

def bookiSlugify(text):
    """
    Wrapper for default Django function. Default function does not work with unicode strings.

    @type text: C{string}
    @param: Text you want to slugify

    @rtype: C{string}
    @return: Returns slugified text
    """
    try:
        import unidecode
        text = unidecode.unidecode(text)
    except ImportError:
        pass

    return slugify(text)