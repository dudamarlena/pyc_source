# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/uploader/uploader.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 5021 bytes
import os, shutil, json
from django.conf import settings
from .fine_uploader import utils
from fine_uploader.views import make_response
from fine_uploader.forms import UploadFileForm
settings.UPLOAD_DIRECTORY = os.path.join(settings.MEDIA_ROOT, 'uploads')

class CallbackError(Exception):
    pass


def post(request, callback):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        file_attrs = form.cleaned_data
        dest_path = os.path.join(settings.UPLOAD_DIRECTORY, file_attrs['qquuid'])
        dest_file = os.path.join(dest_path, file_attrs['qqfilename'])
        chunk = False
        if file_attrs['qqtotalparts'] is not None:
            if int(file_attrs['qqtotalparts']) > 1:
                dest_file = os.path.join(dest_file + '.chunks', str(file_attrs['qqpartindex']))
                chunk = True
        utils.save_upload(file_attrs['qqfile'], dest_file)
        if chunk:
            if file_attrs['qqtotalparts'] - 1 == file_attrs['qqpartindex']:
                dest_file = os.path.join(dest_path, file_attrs['qqfilename'])
                utils.combine_chunks((file_attrs['qqtotalparts']), (file_attrs['qqtotalfilesize']), source_folder=(dest_file + '.chunks'),
                  dest=dest_file)
                shutil.rmtree(dest_file + '.chunks')
                chunk = False
        if not chunk:
            try:
                try:
                    callback(file_path=dest_file, uuid=(file_attrs['qquuid']))
                except CallbackError as e:
                    try:
                        return make_response(status=400, content=(json.dumps({'success':False, 
                         'error':'%s' % repr(e)})))
                    finally:
                        e = None
                        del e

                except Exception as e:
                    try:
                        return make_response(status=500, content=(json.dumps({'success':False, 
                         'error':'Exception thrown by callback'})))
                    finally:
                        e = None
                        del e

            finally:
                shutil.rmtree(dest_path)

        return make_response(content=(json.dumps({'success': True})))
    return make_response(status=400, content=(json.dumps({'success':False, 
     'error':'%s' % repr(form.errors)})))


def delete(request, callback, *args, **kwargs):
    uuid = kwargs.get('qquuid', '')
    if uuid:
        try:
            callback(uuid=uuid)
        except CallbackError as e:
            try:
                return make_response(status=400, content=(json.dumps({'success':False, 
                 'error':'%s' % repr(e)})))
            finally:
                e = None
                del e

        except Exception as e:
            try:
                return make_response(status=500, content=(json.dumps({'success':False, 
                 'error':'Exception thrown by callback'})))
            finally:
                e = None
                del e

        return make_response(content=(json.dumps({'success': True})))
    return make_response(status=404, content=(json.dumps({'success':False, 
     'error':'File not present'})))