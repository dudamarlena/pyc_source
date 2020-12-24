# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpwrussell/Checkout/OME/webtagging/tagsearch/omero_webtagging_tagsearch/views.py
# Compiled at: 2019-12-15 16:33:56
from __future__ import absolute_import
from builtins import str
import json, logging
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from omeroweb.webclient.decorators import render_response, login_required
from omero.sys import Parameters
from omero.rtypes import rlong, rlist
from omeroweb.webclient.views import switch_active_group
from omeroweb.webclient.forms import GlobalSearchForm, ContainerForm
from .forms import TagSearchForm
logger = logging.getLogger(__name__)

@login_required()
@render_response()
def index(request, conn=None, **kwargs):
    request.session.modified = True
    menu = 'search'
    template = 'omero_webtagging_tagsearch/tagnav.html'
    init = {'initially_open': None, 'initially_select': []}
    first_sel = None
    initially_open_owner = None
    path = request.GET.get('path', '')
    i = path.split('|')[(-1)]
    if i.split('=')[0] in ('project', 'dataset', 'image', 'screen', 'plate', 'tag'):
        init['initially_select'].append(str(i).replace('=', '-'))
    show = request.GET.get('show', '')
    for i in show.split('|'):
        if i.split('-')[0] in ('project', 'dataset', 'image', 'screen', 'plate', 'tag',
                               'acquisition', 'run', 'well'):
            i = i.replace('run', 'acquisition')
            init['initially_select'].append(str(i))

    if len(init['initially_select']) > 0:
        init['initially_open'] = [init['initially_select'][0]]
        first_obj, first_id = init['initially_open'][0].split('-', 1)
        if first_obj == 'tag' and menu != 'usertags':
            return HttpResponseRedirect(reverse(viewname='load_template', args=['usertags']) + '?show=' + init['initially_select'][0])
        try:
            conn.SERVICE_OPTS.setOmeroGroup('-1')
            if first_obj == 'tag':
                first_sel = conn.getObject('TagAnnotation', int(first_id))
            else:
                first_sel = conn.getObject(first_obj, int(first_id))
                initially_open_owner = first_sel.details.owner.id.val
                if first_obj == 'well':
                    parentNode = first_sel.getWellSample().getPlateAcquisition()
                    ptype = 'acquisition'
                    if parentNode is None:
                        parentNode = first_sel.getParent()
                        ptype = 'plate'
                    first_sel = parentNode
                    init['initially_open'] = [
                     '%s-%s' % (ptype,
                      parentNode.getId())]
                    init['initially_select'] = init['initially_open'][:]
        except:
            pass

        if first_obj not in ('project', 'screen'):
            if first_sel is not None:
                for p in first_sel.getAncestry():
                    if first_obj == 'tag':
                        init['initially_open'].insert(0, 'tag-%s' % p.getId())
                    else:
                        init['initially_open'].insert(0, '%s-%s' % (p.OMERO_CLASS.lower(), p.getId()))
                        initially_open_owner = p.details.owner.id.val

                if init['initially_open'][0].split('-')[0] == 'image':
                    init['initially_open'].insert(0, 'orphaned-0')
    if first_sel is not None:
        switch_active_group(request, first_sel.details.group.id.val)
    global_search_form = GlobalSearchForm(data=request.GET.copy())
    if menu == 'search':
        if global_search_form.is_valid():
            init['query'] = global_search_form.cleaned_data['search_query']
    url = reverse(viewname='tagsearch')
    active_group = request.session.get('active_group') or conn.getEventContext().groupId
    s = conn.groupSummary(active_group)
    leaders = s['leaders']
    members = s['colleagues']
    userIds = [ u.id for u in leaders ]
    userIds.extend([ u.id for u in members ])
    users = []
    if len(leaders) > 0:
        users.append(('Owners', leaders))
    if len(members) > 0:
        users.append(('Members', members))
    users = tuple(users)
    user_id = request.GET.get('experimenter')
    if initially_open_owner is not None:
        if request.session.get('user_id', None) != -1:
            user_id = initially_open_owner
    try:
        user_id = int(user_id)
    except:
        user_id = None

    if user_id not in set([ x.id for x in leaders ]) | set([ x.id for x in members ]) and user_id != -1:
        user_id = None
    if user_id is None:
        user_id = request.session.get('user_id', None)
        if user_id is None or int(user_id) not in userIds:
            if user_id != -1:
                user_id = conn.getEventContext().userId
    request.session['user_id'] = user_id
    if conn.isAdmin():
        myGroups = [ g for g in conn.getObjects('ExperimenterGroup') if g.getName() not in ('user',
                                                                                            'guest')
                   ]
    else:
        myGroups = list(conn.getGroupsMemberOf())
    myGroups.sort(key=lambda x: x.getName().lower())
    new_container_form = ContainerForm()
    params = Parameters()
    qs = conn.getQueryService()
    service_opts = conn.SERVICE_OPTS.copy()
    service_opts.setOmeroGroup(active_group)

    def get_tags(obj):
        hql = '\n            SELECT DISTINCT link.child.id, link.child.textValue\n            FROM %sAnnotationLink link\n            WHERE link.child.class IS TagAnnotation\n            ORDER BY link.child.textValue\n        ' % obj
        return [ (result[0].val, result[1].val) for result in qs.projection(hql, params, service_opts)
               ]

    tags = set(get_tags('Image'))
    tags.update(get_tags('Dataset'))
    tags.update(get_tags('Project'))
    tags.update(get_tags('Plate'))
    tags.update(get_tags('PlateAcquisition'))
    tags.update(get_tags('Screen'))
    tags = list(tags)
    tags.sort(key=lambda x: x[1].lower())
    form = TagSearchForm(tags, conn, initial={'results_preview': True})
    context = {'init': init, 
       'myGroups': myGroups, 
       'new_container_form': new_container_form, 
       'global_search_form': global_search_form}
    context['groups'] = myGroups
    context['active_group'] = conn.getObject('ExperimenterGroup', int(active_group))
    for g in context['groups']:
        g.groupSummary()

    context['active_user'] = conn.getObject('Experimenter', int(user_id))
    context['isLeader'] = conn.isLeader()
    context['current_url'] = url
    context['template'] = template
    context['tagnav_form'] = form
    return context


@login_required(setGroupContext=True)
def tag_image_search(request, conn=None, **kwargs):
    import time
    start = time.time()
    if request.method == 'POST':
        selected_tags = [ int(x) for x in request.POST.getlist('selectedTags') ]
        results_preview = bool(request.POST.get('results_preview'))
        active_group = request.session.get('active_group') or conn.getEventContext().groupId
        service_opts = conn.SERVICE_OPTS.copy()
        service_opts.setOmeroGroup(active_group)

        def getObjectsWithAllAnnotations(obj_type, annids):
            hql = 'select link.parent.id from %sAnnotationLink link where link.child.id in (:oids) group by link.parent.id having count (distinct link.child) = %s' % (
             obj_type,
             len(annids))
            params = Parameters()
            params.map = {}
            params.map['oids'] = rlist([ rlong(o) for o in set(annids) ])
            qs = conn.getQueryService()
            return [ x[0].getValue() for x in qs.projection(hql, params, service_opts)
                   ]

        context = {}
        html_response = ''
        remaining = set([])
        manager = {'containers': {}}
        preview = False
        project_count = 0
        dataset_count = 0
        screen_count = 0
        plate_count = 0
        acquisition_count = 0
        image_count = 0
        if selected_tags:
            image_ids = getObjectsWithAllAnnotations('Image', selected_tags)
            context['image_count'] = len(image_ids)
            image_count = len(image_ids)
            dataset_ids = getObjectsWithAllAnnotations('Dataset', selected_tags)
            context['dataset_count'] = len(dataset_ids)
            dataset_count = len(dataset_ids)
            project_ids = getObjectsWithAllAnnotations('Project', selected_tags)
            context['project_count'] = len(project_ids)
            project_count = len(project_ids)
            screen_ids = getObjectsWithAllAnnotations('Screen', selected_tags)
            context['screen_count'] = len(screen_ids)
            screen_count = len(screen_ids)
            plate_ids = getObjectsWithAllAnnotations('Plate', selected_tags)
            context['plate_count'] = len(plate_ids)
            plate_count = len(plate_ids)
            acquisition_ids = getObjectsWithAllAnnotations('PlateAcquisition', selected_tags)
            context['acquisition_count'] = len(acquisition_ids)
            acquisition_count = len(acquisition_ids)
            if results_preview:
                if image_ids:
                    images = conn.getObjects('Image', ids=image_ids)
                    manager['containers']['image'] = list(images)
                if dataset_ids:
                    datasets = conn.getObjects('Dataset', ids=dataset_ids)
                    manager['containers']['dataset'] = list(datasets)
                if project_ids:
                    projects = conn.getObjects('Project', ids=project_ids)
                    manager['containers']['project'] = list(projects)
                if screen_ids:
                    screens = conn.getObjects('Screen', ids=screen_ids)
                    manager['containers']['screen'] = list(screens)
                if plate_ids:
                    plates = conn.getObjects('Plate', ids=plate_ids)
                    manager['containers']['plate'] = list(plates)
                if acquisition_ids:
                    acquisitions = conn.getObjects('PlateAcquisition', ids=acquisition_ids)
                    manager['containers']['acquisition'] = list(acquisitions)
                manager['c_size'] = len(image_ids) + len(dataset_ids) + len(project_ids) + len(screen_ids) + len(plate_ids) + len(acquisition_ids)
                if manager['c_size'] > 0:
                    preview = True
            context['manager'] = manager
            html_response = render_to_string('omero_webtagging_tagsearch/search_details.html', context)
            middle = time.time()

            def getAnnotationsForObjects(obj_type, oids):
                hql = 'select distinct link.child.id from %sAnnotationLink link where link.parent.id in (:oids)' % obj_type
                params = Parameters()
                params.map = {}
                params.map['oids'] = rlist([ rlong(o) for o in oids ])
                qs = conn.getQueryService()
                return [ result[0].val for result in qs.projection(hql, params, service_opts)
                       ]

            if image_ids:
                remaining.update(getAnnotationsForObjects('Image', image_ids))
            if dataset_ids:
                remaining.update(getAnnotationsForObjects('Dataset', dataset_ids))
            if project_ids:
                remaining.update(getAnnotationsForObjects('Project', project_ids))
            if acquisition_ids:
                remaining.update(getAnnotationsForObjects('PlateAcquisition', acquisition_ids))
            if plate_ids:
                remaining.update(getAnnotationsForObjects('Plate', plate_ids))
            if screen_ids:
                remaining.update(getAnnotationsForObjects('Screen', screen_ids))
            end = time.time()
            logger.info('Tag Query Times. Preview: %ss, Remaining: %ss, Total:%ss' % (
             middle - start, end - middle, end - start))
        return HttpResponse(json.dumps({'navdata': list(remaining), 'preview': preview, 
           'project_count': project_count, 
           'dataset_count': dataset_count, 
           'screen_count': screen_count, 
           'plate_count': plate_count, 
           'acquisition_count': acquisition_count, 
           'image_count': image_count, 
           'html': html_response}), content_type='application/json')