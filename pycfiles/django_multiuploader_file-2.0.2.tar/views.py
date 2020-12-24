# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matheus/Documents/projects/enki/Admin-Django/msk/multiuploader/views.py
# Compiled at: 2013-06-28 17:44:23
from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files import File as FileWrapper
from models import File
from django.core.files.uploadedfile import UploadedFile
from django.utils import simplejson
from sorl.thumbnail import get_thumbnail
from django.views.decorators.csrf import csrf_exempt
import logging
log = logging

@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
        log.info('Called delete image. image id=' + str(pk))
        image = get_object_or_404(File, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id=' + str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')


@csrf_exempt
def multiuploader(request):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')
        file = request.FILES['files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info('Got file: "%s"' % filename)
        image = File()
        image.filename = filename
        image.image = file
        image.key_data = image.key_generate
        image.save()
        log.info('File saving done')
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL + '/'
        except AttributeError:
            file_delete_url = 'multi_delete/'

        file_url = image.image.url
        result = []
        context = {'name': filename, 'size': file_size, 
           'url': file_url, 
           'file_id': image.id, 
           'delete_url': file_delete_url + str(image.pk) + '/', 
           'delete_type': 'POST'}
        if image.is_image:
            im = get_thumbnail(image, '80x80', quality=50)
            context['thumbnail_url'] = im.url
        else:
            context['thumbnail_url'] = settings.FILE_IMAGE_URL
        result.append(context)
        response_data = simplejson.dumps(result)
        if 'application/json' in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else:
        return HttpResponse('Only POST accepted')
        return


def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(File, key_data=key)
    url = settings.MEDIA_URL + image.image.name
    return render_to_response('multiuploader/one_image.html', {'multi_single_url': url})