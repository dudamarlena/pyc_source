# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syfilebrowser/views.py
# Compiled at: 2016-04-18 13:43:03
from __future__ import unicode_literals
from json import dumps
import os, re
from django.conf import settings as django_settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.dispatch import Signal
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext as Context
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text

from syfilebrowser.settings import *
from syfilebrowser.functions import get_path, get_breadcrumbs, get_filterdate, get_settings_var, get_directory, convert_filename
from syfilebrowser.templatetags.fb_tags import query_helper
from syfilebrowser.base import FileObject
from syfilebrowser.decorators import flash_login_required
from shuyucms.utils.importing import import_dotted_path
storage_class_name = django_settings.DEFAULT_FILE_STORAGE.split(b'.')[(-1)]
mixin_class_name = b'syfilebrowser.storage.%sMixin' % storage_class_name
if django_settings.DEFAULT_FILE_STORAGE == b's3_folder_storage.s3.DefaultStorage':
    mixin_class_name = b'syfilebrowser.storage.S3BotoStorageMixin'
try:
    mixin_class = import_dotted_path(mixin_class_name)
    storage_class = import_dotted_path(django_settings.DEFAULT_FILE_STORAGE)
except ImportError:
    pass

if mixin_class not in storage_class.__bases__:
    storage_class.__bases__ += (mixin_class,)
filter_re = []
for exp in EXCLUDE:
    filter_re.append(re.compile(exp))

for k, v in VERSIONS.items():
    exp = b'_%s.(%s)' % (k, (b'|').join(EXTENSION_LIST))
    filter_re.append(re.compile(exp))

def remove_thumbnails(file_path):
    """
    Cleans up previous shuyucms thumbnail directories when
    a new file is written (upload or rename).
    """
    from shuyucms.conf import settings
    dir_name, file_name = os.path.split(file_path)
    path = os.path.join(dir_name, settings.THUMBNAILS_DIR_NAME, file_name)
    try:
        default_storage.rmtree(path)
    except:
        pass


def browse(request):
    """
    Browse Files/Directories.
    """
    query = request.GET.copy()
    path = get_path(query.get(b'dir', b''))
    directory = get_path(b'')
    if path is None:
        msg = _(b'The requested Folder does not exist.')
        messages.add_message(request, messages.ERROR, msg)
        if directory is None:
            raise ImproperlyConfigured(_(b'Error finding Upload-Folder. Maybe it does not exist?'))
        redirect_url = reverse(b'fb_browse') + query_helper(query, b'', b'dir')
        return HttpResponseRedirect(redirect_url)
    else:
        abs_path = os.path.join(get_directory(), path)
        results_var = {b'results_total': 0, b'results_current': 0, b'delete_total': 0, b'images_total': 0, b'select_total': 0}
        counter = {}
        for k, v in EXTENSIONS.items():
            counter[k] = 0

        dir_list, file_list = default_storage.listdir(abs_path)
        files = []
        for file in dir_list + file_list:
            filtered = not file or file.startswith(b'.')
            for re_prefix in filter_re:
                if re_prefix.search(file):
                    filtered = True

            if filtered:
                continue
            results_var[b'results_total'] += 1
            url_path = (b'/').join([ s.strip(b'/') for s in [
             get_directory(), path, file] if s.strip(b'/')
                                   ])
            fileobject = FileObject(url_path)
            append = False
            if fileobject.filetype == request.GET.get(b'filter_type', fileobject.filetype) and get_filterdate(request.GET.get(b'filter_date', b''), fileobject.date):
                append = True
            if request.GET.get(b'q') and not re.compile(request.GET.get(b'q').lower(), re.M).search(file.lower()):
                append = False
            if append:
                try:
                    if fileobject.filetype == b'Image':
                        results_var[b'images_total'] += 1
                    if fileobject.filetype != b'Folder':
                        results_var[b'delete_total'] += 1
                    elif fileobject.filetype == b'Folder' and fileobject.is_empty:
                        results_var[b'delete_total'] += 1
                    if query.get(b'type') and query.get(b'type') in SELECT_FORMATS and fileobject.filetype in SELECT_FORMATS[query.get(b'type')]:
                        results_var[b'select_total'] += 1
                    elif not query.get(b'type'):
                        results_var[b'select_total'] += 1
                except OSError:
                    continue
                else:
                    files.append(fileobject)
                    results_var[b'results_current'] += 1

            if fileobject.filetype:
                counter[fileobject.filetype] += 1

        query[b'o'] = request.GET.get(b'o', DEFAULT_SORTING_BY)
        query[b'ot'] = request.GET.get(b'ot', DEFAULT_SORTING_ORDER)
        files = sorted(files, key=lambda f: getattr(f, request.GET.get(b'o', DEFAULT_SORTING_BY)))
        if not request.GET.get(b'ot') and DEFAULT_SORTING_ORDER == b'desc' or request.GET.get(b'ot') == b'desc':
            files.reverse()
        p = Paginator(files, LIST_PER_PAGE)
        try:
            page_nr = request.GET.get(b'p', b'1')
        except:
            page_nr = 1

        try:
            page = p.page(page_nr)
        except (EmptyPage, InvalidPage):
            page = p.page(p.num_pages)

        return render_to_response(b'syfilebrowser/index.html', {b'dir': path, 
           b'p': p, 
           b'page': page, 
           b'results_var': results_var, 
           b'counter': counter, 
           b'query': query, 
           b'title': _(b'Media Library'), 
           b'settings_var': get_settings_var(), 
           b'breadcrumbs': get_breadcrumbs(query, path), 
           b'breadcrumbs_title': b''}, context_instance=Context(request))


browse = staff_member_required(never_cache(browse))
syfilebrowser_pre_createdir = Signal(providing_args=[b'path', b'dirname'])
syfilebrowser_post_createdir = Signal(providing_args=[b'path', b'dirname'])

def mkdir(request):
    """
    Make Directory.
    """
    from syfilebrowser.forms import MakeDirForm
    query = request.GET
    path = get_path(query.get(b'dir', b''))
    if path is None:
        msg = _(b'The requested Folder does not exist.')
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse(b'fb_browse'))
    else:
        abs_path = os.path.join(get_directory(), path)
        if request.method == b'POST':
            form = MakeDirForm(abs_path, request.POST)
            if form.is_valid():
                server_path = os.path.join(abs_path, form.cleaned_data[b'dir_name'])
                try:
                    syfilebrowser_pre_createdir.send(sender=request, path=path, dirname=form.cleaned_data[b'dir_name'])
                    default_storage.makedirs(server_path)
                    syfilebrowser_post_createdir.send(sender=request, path=path, dirname=form.cleaned_data[b'dir_name'])
                    msg = _(b'The Folder %s was successfully created.') % form.cleaned_data[b'dir_name']
                    messages.add_message(request, messages.SUCCESS, msg)
                    redirect_url = reverse(b'fb_browse') + query_helper(query, b'ot=desc,o=date', b'ot,o,filter_type,filter_date,q,p')
                    return HttpResponseRedirect(redirect_url)
                except OSError as xxx_todo_changeme:
                    errno, strerror = xxx_todo_changeme.args
                    if errno == 13:
                        form.errors[b'dir_name'] = forms.util.ErrorList([_(b'Permission denied.')])
                    else:
                        form.errors[b'dir_name'] = forms.util.ErrorList([_(b'Error creating folder.')])

        else:
            form = MakeDirForm(abs_path)
        return render_to_response(b'syfilebrowser/makedir.html', {b'form': form, 
           b'query': query, 
           b'title': _(b'New Folder'), 
           b'settings_var': get_settings_var(), 
           b'breadcrumbs': get_breadcrumbs(query, path), 
           b'breadcrumbs_title': _(b'New Folder')}, context_instance=Context(request))


mkdir = staff_member_required(never_cache(mkdir))

def upload(request):
    """
    Multiple File Upload.
    """
    from django.http import parse_cookie
    query = request.GET
    path = get_path(query.get(b'dir', b''))
    if path is None:
        msg = _(b'The requested Folder does not exist.')
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse(b'fb_browse'))
    else:
        cookie_dict = parse_cookie(request.META.get(b'HTTP_COOKIE', b''))
        engine = __import__(settings.SESSION_ENGINE, {}, {}, [b''])
        session_key = cookie_dict.get(settings.SESSION_COOKIE_NAME, None)
        return render_to_response(b'syfilebrowser/upload.html', {b'query': query, 
           b'title': _(b'Select files to upload'), 
           b'settings_var': get_settings_var(), 
           b'session_key': session_key, 
           b'breadcrumbs': get_breadcrumbs(query, path), 
           b'breadcrumbs_title': _(b'Upload')}, context_instance=Context(request))


upload = staff_member_required(never_cache(upload))

@csrf_exempt
def _check_file(request):
    """
    Check if file already exists on the server.
    """
    folder = request.POST.get(b'folder')
    fb_uploadurl_re = re.compile(b'^.*(%s)' % reverse(b'fb_upload'))
    folder = fb_uploadurl_re.sub(b'', folder)
    fileArray = {}
    if request.method == b'POST':
        for k, v in list(request.POST.items()):
            if k != b'folder':
                if default_storage.exists(os.path.join(get_directory(), folder, v)):
                    fileArray[k] = v

    return HttpResponse(dumps(fileArray))


syfilebrowser_pre_upload = Signal(providing_args=[b'path', b'file'])
syfilebrowser_post_upload = Signal(providing_args=[b'path', b'file'])

@csrf_exempt
@flash_login_required
@staff_member_required
def _upload_file(request):
    """
    Upload file to the server.

    Implement unicode handlers - https://github.com/sehmaschine/django-syfilebrowser/blob/master/syfilebrowser/sites.py#L471
    """
    if request.method == b'POST':
        folder = request.POST.get(b'folder')
        fb_uploadurl_re = re.compile(b'^.*(%s)' % reverse(b'fb_upload'))
        folder = fb_uploadurl_re.sub(b'', folder)
        if request.FILES:
            filedata = request.FILES[b'Filedata']
            directory = get_directory()
            syfilebrowser_pre_upload.send(sender=request, path=request.POST.get(b'folder'), file=filedata)
            file_path = os.path.join(directory, folder, filedata.name)
            remove_thumbnails(file_path)
            filedata.name = convert_filename(filedata.name)
            file_path = os.path.join(directory, folder, filedata.name)
            remove_thumbnails(file_path)
            uploadedfile = default_storage.save(file_path, filedata)
            if default_storage.exists(file_path) and file_path != uploadedfile:
                default_storage.move(smart_text(uploadedfile), smart_text(file_path), allow_overwrite=True)
            syfilebrowser_post_upload.send(sender=request, path=request.POST.get(b'folder'), file=FileObject(smart_text(file_path)))
        get_params = request.POST.get(b'get_params')
        if get_params:
            return HttpResponseRedirect(reverse(b'fb_browse') + get_params)
    return HttpResponse(b'True')


syfilebrowser_pre_delete = Signal(providing_args=[b'path', b'filename'])
syfilebrowser_post_delete = Signal(providing_args=[b'path', b'filename'])

def delete(request):
    """
    Delete existing File/Directory.

    When trying to delete a Directory, the Directory has to be empty.
    """
    if request.method != b'POST':
        return HttpResponseRedirect(reverse(b'fb_browse'))
    else:
        query = request.GET
        path = get_path(query.get(b'dir', b''))
        filename = query.get(b'filename', b'')
        if path is None or filename is None:
            if path is None:
                msg = _(b'The requested Folder does not exist.')
            else:
                msg = _(b'The requested File does not exist.')
            messages.add_message(request, messages.ERROR, msg)
            return HttpResponseRedirect(reverse(b'fb_browse'))
        abs_path = os.path.join(get_directory(), path)
        if request.GET.get(b'filetype') != b'Folder':
            relative_server_path = os.path.join(get_directory(), path, filename)
            try:
                syfilebrowser_pre_delete.send(sender=request, path=path, filename=filename)
                default_storage.delete(os.path.join(abs_path, filename))
                syfilebrowser_post_delete.send(sender=request, path=path, filename=filename)
                msg = _(b'The file %s was successfully deleted.') % filename.lower()
                messages.add_message(request, messages.SUCCESS, msg)
            except OSError:
                msg = _(b'An error occurred')
                messages.add_message(request, messages.ERROR, msg)

        else:
            try:
                syfilebrowser_pre_delete.send(sender=request, path=path, filename=filename)
                default_storage.rmtree(os.path.join(abs_path, filename))
                syfilebrowser_post_delete.send(sender=request, path=path, filename=filename)
                msg = _(b'The folder %s was successfully deleted.') % filename.lower()
                messages.add_message(request, messages.SUCCESS, msg)
            except OSError:
                msg = _(b'An error occurred')
                messages.add_message(request, messages.ERROR, msg)

        qs = query_helper(query, b'', b'filename,filetype')
        return HttpResponseRedirect(reverse(b'fb_browse') + qs)


delete = staff_member_required(never_cache(delete))
syfilebrowser_pre_rename = Signal(providing_args=[b'path', b'filename', b'new_filename'])
syfilebrowser_post_rename = Signal(providing_args=[b'path', b'filename', b'new_filename'])

def rename(request):
    """
    Rename existing File/Directory.

    Includes renaming existing Image Versions/Thumbnails.
    """
    from syfilebrowser.forms import RenameForm
    query = request.GET
    path = get_path(query.get(b'dir', b''))
    filename = query.get(b'filename', b'')
    if path is None or filename is None:
        if path is None:
            msg = _(b'The requested Folder does not exist.')
        else:
            msg = _(b'The requested File does not exist.')
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse(b'fb_browse'))
    else:
        abs_path = os.path.join(MEDIA_ROOT, get_directory(), path)
        file_extension = os.path.splitext(filename)[1].lower()
        if request.method == b'POST':
            form = RenameForm(abs_path, file_extension, request.POST)
            if form.is_valid():
                relative_server_path = os.path.join(get_directory(), path, filename)
                new_filename = form.cleaned_data[b'name'] + file_extension
                new_relative_server_path = os.path.join(get_directory(), path, new_filename)
                try:
                    syfilebrowser_pre_rename.send(sender=request, path=path, filename=filename, new_filename=new_filename)
                    remove_thumbnails(new_relative_server_path)
                    default_storage.move(relative_server_path, new_relative_server_path)
                    syfilebrowser_post_rename.send(sender=request, path=path, filename=filename, new_filename=new_filename)
                    msg = _(b'Renaming was successful.')
                    messages.add_message(request, messages.SUCCESS, msg)
                    redirect_url = reverse(b'fb_browse') + query_helper(query, b'', b'filename')
                    return HttpResponseRedirect(redirect_url)
                except OSError as xxx_todo_changeme1:
                    errno, strerror = xxx_todo_changeme1.args
                    form.errors[b'name'] = forms.util.ErrorList([_(b'Error.')])

        else:
            form = RenameForm(abs_path, file_extension)
        return render_to_response(b'syfilebrowser/rename.html', {b'form': form, 
           b'query': query, 
           b'file_extension': file_extension, 
           b'title': _(b'Rename "%s"') % filename, 
           b'settings_var': get_settings_var(), 
           b'breadcrumbs': get_breadcrumbs(query, path), 
           b'breadcrumbs_title': _(b'Rename')}, context_instance=Context(request))


rename = staff_member_required(never_cache(rename))