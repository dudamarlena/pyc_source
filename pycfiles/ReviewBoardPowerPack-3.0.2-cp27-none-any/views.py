# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/reports/views.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import json
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils import six
from reviewboard.accounts.decorators import check_login_required
from reviewboard.site.decorators import check_local_site_access
from reviewboard.site.urlresolvers import local_site_reverse
from rbpowerpack.reports.decorators import check_reporting_enabled
from rbpowerpack.reports.forms import LIST_SPLIT_RE
from rbpowerpack.reports.queries import UserQuery
from rbpowerpack.reports.reports import get_report_classes, get_report

@check_login_required
@check_local_site_access
@check_reporting_enabled
def report_list(request, local_site=None, extension=None):
    reports = _get_report_classes(request, local_site, extension)
    return render(request, b'powerpack/reports/report_list.html', {b'extension': extension, 
       b'reports': reports})


@check_login_required
@check_local_site_access
@check_reporting_enabled
def report(request, report_id, local_site=None, extension=None):
    try:
        reports = _get_report_classes(request, local_site, extension)
        report = get_report(report_id)
        return report.render(extension, request, local_site, {b'reports': reports})
    except KeyError:
        raise Http404


@check_login_required
@check_local_site_access
@check_reporting_enabled
def report_data(request, report_id, local_site=None, extension=None):
    try:
        report = get_report(report_id)
    except KeyError:
        raise Http404

    get_params = request.GET.copy()
    try:
        if get_params.pop(b'csv', None):
            return HttpResponse(report.get_csv(extension, request, get_params, local_site), content_type=b'text/csv')
        else:
            return HttpResponse(json.dumps({b'stat': b'ok', 
               b'result': report.get_data(extension, request, get_params, local_site)}), content_type=b'application/json')

    except ValueError as e:
        return HttpResponseBadRequest(json.dumps({b'stat': b'fail', 
           b'error': six.text_type(e)}))

    return


@check_login_required
@check_local_site_access
@check_reporting_enabled
def query_users(request, local_site=None, extension=None):
    everyone = request.GET.get(b'everyone', b'0') == b'1'

    def get_list(field):
        return [ name for name in LIST_SPLIT_RE.split(request.GET.get(field, b'').strip()) if name
               ]

    usernames = get_list(b'users')
    group_names = get_list(b'groups')
    users = list(UserQuery(local_site=local_site, everyone=everyone, usernames=usernames, group_names=group_names).get_objects().values(b'username', b'email', b'first_name', b'last_name'))
    return HttpResponse(json.dumps(users), content_type=b'application/json')


def _get_report_classes(request, local_site, extension):
    reports = []
    local_site_name = None
    if local_site:
        local_site_name = local_site.name
    for cls in get_report_classes():
        report = cls()
        report.thumbnail_image_url = static(b'ext/%s/%s' % (extension.id, report.thumbnail_image))
        report.url = local_site_reverse(b'powerpack-reports-report', request, local_site_name, kwargs={b'report_id': report.id})
        reports.append(report)

    return reports