# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hgwebproxy/views.py
# Compiled at: 2009-08-03 02:54:01
"""
hgwebproxy.py

Simple Django view code that proxies requests through
to `hgweb` and handles authentication on `POST` up against
Djangos own built in authentication layer.

This code is largely equivalent to the code powering Bitbucket.org.
"""
__docformat__ = 'restructedtext'
import os
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from hgwebproxy.proxy import HgRequestWrapper
from hgwebproxy.utils import is_mercurial, basic_auth
from hgwebproxy.models import Repository
from hgwebproxy.settings import *
from mercurial.hgweb import hgwebdir, hgweb
from mercurial import hg, ui

def repo_list(request):
    repos = Repository.objects.all()
    context = {'repos_list': repos}
    return render_to_response('admin/hgwebproxy/repo_list.html', context, RequestContext(request))


def repo(request, slug, *args):
    response = HttpResponse()
    repo = get_object_or_404(Repository, slug=slug)
    hgr = HgRequestWrapper(request, response, reponame=repo.slug, repourl=repo.get_repo_url())
    realm = AUTH_REALM
    if is_mercurial(request):
        authed = basic_auth(request, realm, repo.slug)
    else:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('%s?next=%s' % (
             settings.LOGIN_URL, request.path))
        authed = request.user.username
    if not authed:
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        return response
    hgr.set_user(authed)
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    hgserve = hgweb(str(repo.location))
    hgserve.reponame = repo.slug
    hgserve.templatepath = (
     template_dir, '/usr/share/mercurial/templates')
    hgserve.repo.ui.setconfig('web', 'description', repo.description)
    hgserve.repo.ui.setconfig('web', 'name', hgserve.reponame)
    hgserve.repo.ui.setconfig('web', 'contact', repo.owner.get_full_name().encode('utf-8'))
    hgserve.repo.ui.setconfig('web', 'allow_archive', repo.allow_archive)
    hgserve.repo.ui.setconfig('web', 'style', 'monoblue_plain')
    hgserve.repo.ui.setconfig('web', 'baseurl', repo.get_repo_url())
    hgserve.repo.ui.setconfig('web', 'staticurl', STATIC_URL)
    try:
        response.write(('').join([ each for each in hgserve.run_wsgi(hgr) ]))
    except KeyError:
        response['content-type'] = 'text/html'
        response.write('hgweb crashed.')

    context = {'content': response.content, 
       'reponame': hgserve.reponame, 
       'static_url': STATIC_URL, 
       'slugpath': request.path.replace(repo.get_repo_url(), ''), 
       'is_root': request.path == repo.get_repo_url(), 
       'repo': repo}
    if response.has_header('content-type'):
        if not response['content-type'].startswith('text/html'):
            return response
    return render_to_response('admin/hgwebproxy/repo.html', context, RequestContext(request))