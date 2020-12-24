# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_mce_spellcheck/views.py
# Compiled at: 2016-09-12 17:31:13
import enchant, json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def spellcheck(request):
    """
Returns a HttpResponse that implements the TinyMCE spellchecker protocol.
"""
    try:
        raw = request.raw_post_data
        input = json.loads(raw)
        id = input['id']
        method = input['method']
        params = input['params']
        lang = params[0]
        arg = params[1]
        if not enchant.dict_exists(str(lang)):
            raise RuntimeError("dictionary not found for language '%s'" % lang)
        checker = enchant.Dict(str(lang))
        if method == 'checkWords':
            result = [ word for word in arg if word and not checker.check(word) ]
        elif method == 'getSuggestions':
            result = checker.suggest(arg)
        else:
            raise RuntimeError("Unkown spellcheck method: '%s'" % method)
        output = {'id': id, 'result': result, 
           'error': None}
    except Exception:
        return HttpResponse('Error running spellchecker')

    return HttpResponse(json.dumps(output), content_type='application/json')


try:
    spellcheck = csrf_exempt(spellcheck)
except NameError:
    pass