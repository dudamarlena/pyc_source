# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/views/delete.py
# Compiled at: 2018-10-06 08:17:06
# Size of source mod 2**32: 1227 bytes
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
__all__ = [
 'Delete', 'ModalDelete']

class Delete(generic.DeleteView):

    def get_success_message(self, obj):
        return f"{obj} supprimé"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk = self.object.pk
        self.object.delete()
        return JsonResponse(self.get_json_data())

    def get_success_message_json_notice(self):
        return {'content':self.get_success_message(self.object), 
         'classes':'success'}

    def get_json_data(self):
        json = {'notice': self.get_success_message_json_notice()}
        messages.success(self.request, self.get_success_message(self.object))
        json['redirect'] = self.request.META['HTTP_REFERER']
        return json


class ModalDelete(Delete):
    template_name = 'workon/views/delete/_modal.html'