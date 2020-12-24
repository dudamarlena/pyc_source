# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/daarmaan/daarmaan/server/views/profile.py
# Compiled at: 2012-10-23 10:06:56
from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.template import RequestContext
from django.shortcuts import render_to_response as rr
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from daarmaan.server.models import BasicProfile

class ProfileActions(object):
    """
    Profile related action like:
        Review user profiles
        Edit profile
        etc
    """
    view_profile_template = 'view_profile.html'
    edit_profile_template = 'edit_profile.html'

    @property
    def urls(self):
        """
        Profile Page url patterns.
        """
        urlpatterns = patterns('', url('^$', self.index, name='profile-home'), url('^edit/$', self.edit, name='edit-profile'))
        return urlpatterns

    def index(self, request):
        """
        Index view.
        """
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
        if request.method == 'POST':
            raise Http404()
        else:
            profile = self._get_user_profile(request.user)
            return rr(self.view_profile_template, {'user': request.user, 'profile': profile, 
               'global': False}, context_instance=RequestContext(request))

    def edit(self, request):
        """
        Edit view for basic user profile.
        """
        from daarmaan.server.forms import EditBasicProfile
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/?next=%s' % reverse(self.edit, args=[]))
        user = request.user
        profile = self._get_user_profile(user)
        if request.method == 'POST':
            form = EditBasicProfile(user, instance=profile, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('profile-home', args=[]))
        else:
            form = EditBasicProfile(user, instance=profile)
        return rr(self.edit_profile_template, {'form': form, 'user': user}, context_instance=RequestContext(request))

    def view_profile(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404()

        profile = self._get_user_profile(request.user)
        if not profile.is_public() and user != request.user:
            raise Http404()
        return rr(self.view_profile_template, {'user': request.user, 'profile': profile, 
           'global': True}, context_instance=RequestContext(request))

    def _get_user_profile(self, user):
        """
        Get or create a basic profile object for given user.
        """
        try:
            p = BasicProfile.objects.get(user=user)
        except BasicProfile.DoesNotExist:
            p = BasicProfile(user=user)
            p.save()

        return p


profile = ProfileActions()