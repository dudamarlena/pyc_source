# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tigorc/repo/django-redactorjs/redactor/views.py
# Compiled at: 2016-01-24 05:00:54
import os, json
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import FormMixin, ProcessFormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from redactor.forms import ImageForm

def default_generate_filename(filename):
    return filename


UPLOAD_PATH = getattr(settings, 'REDACTOR_UPLOAD', 'redactor/')
GENERATE_FILENAME = getattr(settings, 'REDACTOR_GENERATE_FILENAME', default_generate_filename)

class BaseRedactorUploadView(FormMixin, ProcessFormView, View):
    http_method_names = [
     'post']
    form_class = ImageForm
    file_storage = default_storage

    def get_form_class(self):
        return self.kwargs.get('form_class') or self.form_class

    def form_valid(self, form):
        file_ = form.cleaned_data['file']
        upload_to = self.kwargs.get('upload_to')
        path = os.path.join(upload_to or UPLOAD_PATH, GENERATE_FILENAME(file_.name))
        real_path = self.file_storage.save(path, file_)
        response_data = json.dumps({'filelink': self.file_storage.url(real_path),  'filename': file_.name})
        return HttpResponse(response_data)

    def form_invalid(self, form):
        return HttpResponse(status=403)


class DefaultRedactorUploadView(BaseRedactorUploadView):

    @method_decorator(csrf_exempt)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(DefaultRedactorUploadView, self).dispatch(request, *args, **kwargs)