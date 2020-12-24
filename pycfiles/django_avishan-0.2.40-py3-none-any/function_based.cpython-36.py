# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/views/function_based.py
# Compiled at: 2020-05-09 02:48:26
# Size of source mod 2**32: 401 bytes
from avishan.decorators import AvishanTemplateViewDecorator

@AvishanTemplateViewDecorator(authenticate=False)
def avishan_doc(request):
    import json
    from avishan.libraries.openapi3.classes import OpenApi
    from django.shortcuts import render
    return render(request, 'avishan/swagger.html', context={'data': json.dumps(OpenApi('0.0.0', 'Documentation').export_json())})