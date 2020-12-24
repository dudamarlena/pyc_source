# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/volunteer-coordination/volunteerhub/apps/volunteers/views.py
# Compiled at: 2014-07-14 11:53:15
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView, ListView, View
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.template.loader import render_to_string
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from .forms import VolunteerForm, ProjectForm, OrganizationForm
from .models import Opportunity, Project, Organization, Volunteer, VolunteerApplication
from braces import views

def get_nearby_opportunities(request, *args, **kwargs):
    if kwargs['lat'] and kwargs['lng']:
        if kwargs['lat'][0] == '-':
            lat = kwargs['lat'][:3] + '.' + kwargs['lat'][3:]
        else:
            lat = kwargs['lat'][:2] + '.' + kwargs['lat'][2:]
        if kwargs['lng'][0] == '-':
            lng = kwargs['lng'][:3] + '.' + kwargs['lng'][3:]
        else:
            lng = kwargs['lng'][:2] + '.' + kwargs['lng'][2:]
        current_point = GEOSGeometry('POINT(%s %s)' % (lat, lng))
        meters = 5000
        OrganizationMixin, opportunities = Opportunity.objects.filter(point__distance_lte=(
         current_point, D(m=meters)))
        if getattr(request.GET, 'json', False):
            data = serializers.serialize('json', opportunities)
            return HttpResponse(data, mimetype='application/json')
        html = render_to_string('volunteers/_opportunity_list.html', {'object_list': opportunities})
        return HttpResponse(html, mimetype='text/html')


def change_organization(request):
    if 'POST' == request.method:
        new_org = request.POST.get('new_org')
        if new_org:
            current_organization = Organization.objects.get(id=new_org)
            request.session['current_organization'] = str(current_organization.id)
            request.session[('{0}_slug').format('current_organization')] = current_organization.slug
            redirect_url = request.POST.get('redirect_to', '/dashboard')
            if redirect_url:
                return redirect(redirect_url)
            return redirect('/dashboard')


class JsonView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, views.JSONResponseMixin, View):
    pass


class ProjectDetailJSONView(JsonView, DetailView):
    model = Project
    json_dumps_kwargs = {'indent': 2}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_dict = {'title': self.object.title, 
           'description': self.object.description}
        return self.render_json_response(context_dict)


class ProjectDetailView(JsonView, DetailView):
    model = Project


class ProjectCreateView(CreateView):
    model = Project


class ProjectListJSONView(JsonView, ListView):
    model = Project
    json_dumps_kwargs = {'indent': 2}

    def get(self, request, *args, **kwargs):
        context = serializers.serialize('json', self.get_queryset().all())
        return self.render_json_response(context)


class ProjectListView(JsonView, ListView):
    model = Project
    form_class = ProjectForm


class OpportunityVolunteerView(View):
    """
    Takes a get request to a URL with a volunteer and an 
    and adds the user to the opportunities candidate list.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous():
            return redirect(reverse('account_login'))
        else:
            qs = Opportunity.open_objects.all()
            try:
                slug = kwargs['slug']
                project_slug = kwargs['project_slug']
            except AttributeError:
                slug = project_slug = None

            opp = get_object_or_404(qs, slug=slug, project__slug=project_slug)
            try:
                application = VolunteerApplication.objects.get(user=user, opportunity=opp)
            except VolunteerApplication.DoesNotExist:
                application = None

            if not application:
                application = VolunteerApplication.objects.create(user=user, opportunity=opp)
                application.save()
            return redirect(reverse('opportunity-detail', kwargs={'slug': slug, 
               'project_slug': project_slug}))


class OpportunityUnVolunteerView(View):
    """
    Takes a posted form with a volunteer and an OpportunityDetailJSONView
    and adds the user to the opportunities candidate list.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        qs = Opportunity.open_objects.all()
        try:
            slug = kwargs['slug']
            project_slug = kwargs['project_slug']
        except AttributeError:
            slug = project_slug = None

        opp = get_object_or_404(qs, slug=slug, project__slug=project_slug)
        try:
            application = VolunteerApplication.objects.get(user=user, opportunity=opp)
            application.delete()
        except VolunteerApplication.DoesNotExist:
            application = None

        return redirect(reverse('opportunity-detail', kwargs={'slug': slug, 
           'project_slug': project_slug}))


class OpportunityDetailJSONView(JsonView, DetailView):
    model = Opportunity
    json_dumps_kwargs = {'indent': 2}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_dict = {'title': self.object.title, 
           'description': self.object.description}
        self.object = self.get_object()
        return self.render_json_response(context_dict)


class OpportunityDetailView(JsonView, DetailView):
    model = Opportunity
    json_dumps_kwargs = {'indent': 2}


class CreateOpportunityView(CreateView):
    pass


class OrganizationListView(ListView):
    model = Organization


class OrganizationDetailView(DetailView):
    model = Organization


class OrganizationCreateView(CreateView):
    model = Organization


class DashboardView(DetailView):
    """ DashboardView
    """
    model = Volunteer
    template_name = 'volunteers/dashboard.html'

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        org_id = getattr(self.kwargs, 'org_id', None)
        if org_id:
            try:
                organization = Organization.objects.get(manager=self.request.user, id=self.kwargs['org_id'])
            except:
                return Http404

        try:
            organization = Organization.objects.get(id=self.kwargs['org_id'])
        except:
            organization = None

        if organization:
            context['organization'] = organization
            context['applications'] = VolunteerApplication.objects.filter(user=self.request.user, opportunity__project__organization=organization)
            context['projects'] = Project.objects.filter(organization=organization)
        else:
            return Http404
        context['org_form'] = OrganizationForm
        context['user_orgs'] = Organization.objects.filter(managers=self.request.user)
        return context


class ProfileUpdateView(UpdateView):
    model = Volunteer
    template_name = 'volunteers/profile_update.html'
    form_class = VolunteerForm

    def get_object(self, *args, **kwargs):
        return self.request.user