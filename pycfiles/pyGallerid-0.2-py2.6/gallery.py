# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyGallerid/views/gallery.py
# Compiled at: 2012-01-31 11:29:51
"""
Provides views for the gallery resources of pyGallerid.
"""
import datetime, json, urllib, itertools, logging
from pyramid.location import lineage
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.traversal import find_resource, find_root, find_interface, resource_path
from pyramid.security import authenticated_userid, remember, forget
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from ..models import retrieve_about, retrieve_gallery, retrieve_user
from ..models.user import User
from ..models.gallery import GalleryContainer, GalleryAlbum, GalleryPicture, GalleryDocument
logger = logging.getLogger(__name__)

def picture_item(method):

    def new_method(item):
        if isinstance(item, GalleryContainer):
            item = item.preview_picture
        return method(item)

    return new_method


def picture_request_item(method):

    def new_method(request, item):
        if isinstance(item, GalleryContainer):
            item = item.preview_picture
        return method(request, item)

    return new_method


@picture_request_item
def big_url(request, item):
    url = request.static_url(item.big_image_path)
    url = urllib.unquote(url)
    return url


@picture_item
def big_width(item):
    return item.big_image_view.width


@picture_item
def big_height(item):
    return item.big_image_view.height


@picture_request_item
def regular_url(request, item):
    url = request.static_url(item.regular_image_path)
    url = urllib.unquote(url)
    return url


@picture_item
def regular_width(item):
    return item.regular_image_view.width


@picture_item
def regular_height(item):
    return item.regular_image_view.height


@picture_request_item
def small_url(request, item):
    url = request.static_url(item.small_image_path)
    url = urllib.unquote(url)
    return url


@picture_item
def small_width(item):
    return item.small_image_view.width


@picture_item
def small_height(item):
    return item.small_image_view.height


def render_resource(resource):
    name = resource.name
    name = name[0].upper() + name[1:]
    return unicode(name)


def find_gallery_resource(resource):
    user = itertools.ifilter(lambda r: isinstance(r, User), lineage(resource)).next()
    return retrieve_gallery(user)


def find_about_resource(resource):
    user = itertools.ifilter(lambda r: isinstance(r, User), lineage(resource)).next()
    return retrieve_about(user)


@view_config(context=GalleryContainer, xhr=True, name='update', renderer='json', permission='update', request_param='pg-type=order-list')
def update_gallery_order_list(context, request):
    result = {'pg-status': 'failed'}
    pg_context = find_resource(context, request.params['pg-context'])
    pg_ids = json.loads(request.params['pg-value'])
    children = pg_context.children
    new_children = []
    for pg_id in pg_ids:
        new_children.append(children[pg_id])

    pg_context.children = new_children
    result['pg-status'] = 'success'
    result['pg-redirect-url'] = request.resource_url(context, '@@edit')
    return result


@view_config(context=GalleryContainer, xhr=True, name='update', renderer='json', permission='update', request_param='pg-type=select-picture')
def update_gallery_select_picture(context, request):
    result = {'pg-status': 'failed'}
    pg_context = find_resource(context, request.params['pg-context'])
    pg_resource = find_resource(pg_context, json.loads(request.params['pg-value']))
    print 'selected picture %s' % pg_resource.name
    pg_context.preview_picture = pg_resource
    result['pg-status'] = 'success'
    result['pg-redirect-url'] = request.resource_url(context, '@@edit')
    return result


@view_config(context=GalleryDocument, xhr=True, name='update', renderer='json', permission='update', request_param='pg-type=attribute-multiline-text')
@view_config(context=GalleryContainer, xhr=True, name='update', renderer='json', permission='update', request_param='pg-type=attribute-multiline-text')
@view_config(context=GalleryDocument, xhr=True, name='update', renderer='json', permission='update', request_param='pg-type=attribute-text')
@view_config(context=GalleryContainer, xhr=True, name='update', renderer='json', permission='update', request_param='pg-type=attribute-text')
def update_gallery_attribute_text(context, request):
    result = {'pg-status': 'failed'}
    pg_context = find_resource(context, request.params['pg-context'])
    pg_name = request.params['pg-name']
    pg_text = json.loads(request.params['pg-value'])
    if find_gallery_resource(pg_context) == pg_context and pg_name == 'name':
        logger.info('Attempt to change name of gallery resource: %s' % pg_context)
        return result
    if find_about_resource(pg_context) == pg_context and pg_name == 'name':
        logger.info('Attempt to change name of about resource: %s' % pg_context)
        return result
    pg_context.__setattr__(pg_name, pg_text)
    if pg_context == context and pg_name == 'name':
        result['pg-redirect-url'] = request.resource_url(context, '@@edit')
    result['pg-status'] = 'success'
    return result


@view_config(context=GalleryContainer, xhr=True, name='update', renderer='json', permission='update', request_param='pg-type=attribute-date')
def update_gallery_attribute_date(context, request):
    result = {'pg-status': 'failed'}
    pg_context = find_resource(context, request.params['pg-context'])
    pg_name = request.params['pg-name']
    pg_value = json.loads(request.params['pg-value'])
    date = datetime.datetime.strptime(pg_value, '%Y-%m-%d').date()
    pg_context.__setattr__(pg_name, date)
    result['pg-date'] = '%d %s %d' % (date.day, date.strftime('%B'), date.year)
    result['pg-status'] = 'success'
    return result


@view_config(context=GalleryContainer, xhr=True, name='update', renderer='json', permission='update', request_param='pg-type=attribute-date-from-to')
def update_gallery_attribute_date_from_to(context, request):
    result = {'pg-status': 'failed'}
    pg_context = find_resource(context, request.params['pg-context'])
    pg_name = request.params['pg-name']
    pg_value = json.loads(request.params['pg-value'])
    (date_from, date_to) = [ datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in (
     pg_value['from'], pg_value['to'])
                           ]
    if date_to < date_from:
        raise AssertionError('date_to < date_from')
    if pg_name == '__date_from_to':
        pg_context.date_from = date_from
        pg_context.date_to = date_to
    else:
        pg_context.__setattr__(pg_name, (date_from, date_to))
    date_str = '%d' % date_from.day
    if date_from.month != date_to.month:
        date_str += ' %s' % date_from.strftime('%B')
    if date_from.year != date_to.year:
        date_str += ' %d' % date_from.year
    date_str += ' - %d %s %d' % (date_to.day, date_to.strftime('%B'),
     date_to.year)
    result['pg-date-from-to'] = date_str
    result['pg-status'] = 'success'
    return result


@view_config(context=GalleryContainer, xhr=True, name='retrieve', renderer='json', request_param='pg-type=pictures', permission='view')
def retrieve_pictures(context, request):
    result = {'pg-status': 'failed'}
    pg_context = find_resource(context, request.params['pg-context'])
    if 'pg-slice' in request.params:
        pg_slice = [ int(x) for x in request.params['pg-slice'].split(':') ]
        pg_slice = slice(*pg_slice)
    else:
        pg_slice = slice(None)
    indices = range(len(pg_context))[pg_slice]
    pg_pictures = []
    for (index, child) in enumerate(pg_context.itervalues()):
        if index not in indices:
            continue
        if isinstance(child, GalleryContainer):
            thumbnail = child.preview_picture
        elif isinstance(child, GalleryPicture):
            thumbnail = child
        else:
            raise Exception("Can't retrieve thumbnails for this kind of object")
        pg_pictures.append({'index': index, 
           'name': child.name, 
           'big_url': big_url(request, thumbnail), 
           'regular_url': regular_url(request, thumbnail), 
           'width': regular_width(thumbnail), 
           'height': regular_height(thumbnail)})

    result['pg-pictures'] = json.dumps(pg_pictures)
    result['pg-status'] = 'success'
    return result


@view_config(context=GalleryContainer, xhr=True, name='retrieve', renderer='json', request_param='pg-type=thumbnails', permission='view')
def retrieve_thumbnails(context, request):
    result = {'pg-status': 'failed'}
    pg_context = find_resource(context, request.params['pg-context'])
    pg_thumbnails = []
    for (index, child) in enumerate(pg_context.itervalues()):
        if isinstance(child, GalleryContainer):
            thumbnail = child.preview_picture
        elif isinstance(child, GalleryPicture):
            thumbnail = child
        else:
            raise Exception("Can't retrieve thumbnails for this kind of object")
        pg_thumbnails.append({'index': index, 
           'name': child.name, 
           'url': small_url(request, thumbnail), 
           'width': small_width(thumbnail), 
           'height': small_height(thumbnail)})

    result['pg-thumbnails'] = json.dumps(pg_thumbnails)
    result['pg-status'] = 'success'
    return result


def convert_resource_to_json(resource, state='closed'):
    json_resource = {}
    json_resource['state'] = state
    if resource == find_root(resource):
        json_resource['data'] = '<root>'
    else:
        json_resource['data'] = str(resource)
    json_resource['attr'] = {'pg-path': resource_path(resource)}
    metadata = {}
    if hasattr(resource, '__attributes__'):
        for attr_name in resource.__attributes__:
            metadata[attr_name] = str(getattr(resource, attr_name))

    json_resource['metadata'] = metadata
    return json_resource


@view_config(context=GalleryDocument, name='retrieve', renderer='json', request_param='pg-type=resource-lineage', permission='edit')
@view_config(context=GalleryContainer, name='retrieve', renderer='json', request_param='pg-type=resource-lineage', permission='edit')
def retrieve_resource_lineage(context, request):
    result = {'pg-status': 'failed'}

    def convert_lineage_to_json(resource, descendants):
        json_resource = convert_resource_to_json(resource, state='open')
        if isinstance(resource, PersistentDict):
            iterator = resource.itervalues()
        elif isinstance(resource, PersistentList):
            iterator = resource.__iter__()
        else:
            iterator = (()).__iter__()
        children = []
        for child in iterator:
            if len(descendants) > 0 and child == descendants[0]:
                json_child = convert_lineage_to_json(child, descendants[1:])
            else:
                json_child = convert_resource_to_json(child, state='closed')
            children.append(json_child)

        json_resource['children'] = children
        return json_resource

    descendants = list(lineage(context))[::-1]
    root = descendants[0]
    pg_lineage = convert_lineage_to_json(root, descendants[1:])
    result['pg-data'] = json.dumps(pg_lineage)
    result['pg-status'] = 'success'
    return result


@view_config(context=GalleryDocument, name='retrieve', renderer='json', request_param='pg-type=resource-children', permission='edit')
@view_config(context=GalleryContainer, name='retrieve', renderer='json', request_param='pg-type=resource-children', permission='edit')
def retrieve_resource_children(context, request):
    result = {'pg-status': 'failed'}
    resource = find_resource(find_root(context), request.params['pg-path'])
    if isinstance(resource, PersistentDict):
        pg_children = [ convert_resource_to_json(child) for child in resource.itervalues()
                      ]
    elif isinstance(resource, PersistentList):
        pg_children = [ convert_resource_to_json(child) for child in resource
                      ]
    else:
        pg_children = []
    result['pg-data'] = json.dumps(pg_children)
    result['pg-status'] = 'success'
    return result


@view_config(context=GalleryContainer, name='login', permission='login')
@view_config(context=GalleryDocument, name='login', permission='login')
def login(context, request):
    username = request.params['username']
    password = request.params['password']
    root = find_root(context)
    user = retrieve_user(root, username)
    if user is not None and user.authenticate(password):
        headers = remember(request, username)
        request.session.flash('Logged in successfully')
    else:
        headers = None
        request.session.flash('Login failed')
    url = request.resource_url(context)
    return HTTPFound(location=url, headers=headers)


@view_config(context=GalleryContainer, name='logout', permission='logout')
def logout(context, request):
    headers = forget(request)
    request.session.flash('Logged out')
    url = request.resource_url(context)
    return HTTPFound(location=url, headers=headers)


def allow_editing(context, request):
    user = find_interface(context, User)
    if user is not None and authenticated_userid(request) == user.name:
        return True
    else:
        return False
        return


def about_url(context, request):
    about_resource = find_about_resource(context)
    if about_resource != context:
        about_url = request.resource_url(about_resource, '@@' + request.view_name)
    else:
        about_url = None
    return about_url


@view_config(context=GalleryContainer, name='edit', renderer='view_gallery.html.mako', permission='edit')
def edit_gallery(context, request):
    d = view_gallery(context, request)
    d.update({'editing': True})
    return d


@view_config(context=GalleryContainer, renderer='view_gallery.html.mako', permission='view')
def view_gallery(context, request):
    items = []
    for item in context.itervalues():
        if len(item) > 0:
            items.append(item)

    items = list(enumerate(items))
    local_small_url = lambda item: small_url(request, item)
    return {'messages': request.session.pop_flash(), 
       'user': request.user, 
       'gallery': context, 
       'items': items, 
       'allow_editing': allow_editing(context, request), 
       'editing': False, 
       'lineage_list': list(lineage(context))[:-2], 
       'about_url': about_url(context, request), 
       'render_resource': render_resource, 
       'small_url': local_small_url, 
       'small_width': small_width, 
       'small_height': small_height}


@view_config(context=GalleryAlbum, name='edit', renderer='view_album.html.mako', permission='edit')
def edit_album(context, request):
    d = view_album(context, request)
    d.update({'editing': True})
    return d


@view_config(context=GalleryAlbum, renderer='view_album.html.mako', permission='view')
def view_album(context, request):
    display_mode = request.params.get('display_mode', 'list')
    if display_mode == 'list':
        pictures_per_page = 10
    elif display_mode == 'grid':
        pictures_per_page = 20
    else:
        pictures_per_page = -1
    if pictures_per_page > 0:
        num_of_pages = len(context) / pictures_per_page + 1
        try:
            page = int(request.params.get('page', 1))
        except ValueError:
            page = 1
        else:
            if page < 1 or page > num_of_pages:
                page = 1
            pictures_start_index = (page - 1) * pictures_per_page
            pictures_end_index = pictures_start_index + pictures_per_page
    else:
        page = 1
        num_of_pages = 1
        pictures_start_index = 0
        pictures_end_index = len(context.pictures)
    pictures = context.pictures[pictures_start_index:pictures_end_index]
    pictures = zip(xrange(pictures_start_index, pictures_end_index), pictures)
    local_big_url = lambda item: big_url(request, item)
    local_regular_url = lambda item: regular_url(request, item)
    local_small_url = lambda item: small_url(request, item)
    return {'messages': request.session.pop_flash(), 
       'user': request.user, 
       'album': context, 
       'allow_editing': allow_editing(context, request), 
       'editing': False, 
       'lineage_list': list(lineage(context))[:-2], 
       'about_url': about_url(context, request), 
       'render_resource': render_resource, 
       'pictures': pictures, 
       'display_mode': display_mode, 
       'page': page, 
       'num_of_pages': num_of_pages, 
       'total_num_of_pictures': len(context), 
       'small_url': local_small_url, 
       'small_width': small_width, 
       'small_height': small_height, 
       'regular_url': local_regular_url, 
       'regular_width': regular_width, 
       'regular_height': regular_height, 
       'big_url': local_big_url}


@view_config(context=GalleryDocument, name='edit', renderer='view_document.html.mako', permission='edit')
def edit_document(context, request):
    d = view_document(context, request)
    d.update({'editing': True})
    return d


@view_config(context=GalleryDocument, renderer='view_document.html.mako', permission='view')
def view_document(context, request):
    lineage_list = [context, find_gallery_resource(context)]
    return {'messages': request.session.pop_flash(), 
       'user': request.user, 
       'document': context, 
       'allow_editing': allow_editing(context, request), 
       'editing': False, 
       'lineage_list': lineage_list, 
       'about_url': about_url(context, request), 
       'render_resource': render_resource}