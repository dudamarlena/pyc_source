# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/utils/loadFile.py
# Compiled at: 2014-07-07 11:20:25
from protoLib.utilsWeb import JsonError
from protoLib.protoActions import protoExecuteAction
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt
def loadFiles(request):
    if not request.user.is_authenticated():
        return JsonError('readOnly User')
    if request.method != 'POST':
        return JsonError('invalid message')
    from django.conf import settings
    import os
    fileroot = request.user.__str__() + datetime.datetime.now().strftime('_%y%m%d%H%M%S_')
    actionFiles = {}
    try:
        for key, fileObj in request.FILES.items():
            path = os.path.join(settings.MEDIA_ROOT, fileroot + fileObj.name)
            actionFiles[key] = path
            dest = open(path, 'w')
            if fileObj.multiple_chunks:
                for c in fileObj.chunks():
                    dest.write(c)

            else:
                dest.write(fileObj.read())
            dest.close()

        request.POST['actionFiles'] = actionFiles
    except:
        return JsonError('fileLoad error: ' + fileObj.name)

    return protoExecuteAction(request)