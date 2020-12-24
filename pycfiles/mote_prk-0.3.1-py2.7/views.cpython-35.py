# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/views.py
# Compiled at: 2017-04-24 04:30:52
# Size of source mod 2**32: 5263 bytes
from django.conf import settings
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.templatetags.static import PrefixNode
from django.utils.functional import cached_property
from django.utils.six.moves.urllib.parse import urljoin
from django.views.generic.base import TemplateView
from mote import PROJECT_PATHS
from mote.models import Project, Aspect, Pattern, Element, Variation

class HomeView(TemplateView):
    template_name = 'mote/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        li = []
        for id, pth in PROJECT_PATHS.items():
            li.append(Project(id))

        context['projects'] = sorted(li, key=lambda item: item.metadata.get('position'))
        return context


class ProjectView(TemplateView):
    __doc__ = 'Detail view for a project'
    template_name = 'mote/project.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['project'] = Project(kwargs['project'])
        context['__mote_project_id__'] = context['project'].id
        return context


class AspectView(TemplateView):
    __doc__ = 'Detail view for an aspect'
    template_name = 'mote/aspect.html'

    def get_context_data(self, **kwargs):
        context = super(AspectView, self).get_context_data(**kwargs)
        project = Project(kwargs['project'])
        context['__mote_project_id__'] = project.id
        context['aspect'] = Aspect(kwargs['aspect'], project)
        return context


class PatternView(TemplateView):
    __doc__ = 'Detail view for a pattern'
    template_name = 'mote/pattern.html'

    def get_context_data(self, **kwargs):
        context = super(PatternView, self).get_context_data(**kwargs)
        project = Project(kwargs['project'])
        aspect = Aspect(kwargs['aspect'], project)
        pattern = Pattern(kwargs['pattern'], aspect)
        context['__mote_project_id__'] = project.id
        context['pattern'] = pattern
        template_names = (
         '%s/%s/src/patterns/%s/mote/intro.html' % (
          project.id, aspect.id, pattern.id),
         'mote/pattern/intros/%s.html' % pattern.id)
        intro = None
        for template_name in template_names:
            try:
                intro = render_to_string(template_name, {})
                break
            except TemplateDoesNotExist:
                pass

        context['intro'] = intro
        return context


class ElementBaseView(TemplateView):

    @cached_property
    def element(self):
        project = Project(self.kwargs['project'])
        aspect = Aspect(self.kwargs['aspect'], project)
        pattern = Pattern(self.kwargs['pattern'], aspect)
        element = Element(self.kwargs['element'], pattern)
        return element

    def get_context_data(self, **kwargs):
        context = super(ElementBaseView, self).get_context_data(**kwargs)
        context['__mote_project_id__'] = self.element.project.id
        context['element'] = self.element
        context['static_root'] = urljoin(PrefixNode.handle_simple('STATIC_URL'), self.element.aspect.relative_path)
        return context


class ElementIndexView(ElementBaseView):
    __doc__ = 'Index view for an element. Provides common UI around an element.'

    def get_template_names(self):
        return self.element.index_template_names


class ElementPartialView(ElementBaseView):
    __doc__ = 'Element view with no wrapping html and body tags'

    def get_template_names(self):
        return self.element.template_names

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ElementIframeView(ElementBaseView):
    __doc__ = 'Element view suitable for rendering in an iframe'

    def get_template_names(self):
        return [
         '%s/mote/element/iframe.html' % self.element.project.id,
         'mote/element/iframe.html']


class VariationBaseView(ElementBaseView):

    @cached_property
    def variation(self):
        return Variation(self.kwargs['variation'], self.element)

    def get_context_data(self, **kwargs):
        context = super(VariationBaseView, self).get_context_data(**kwargs)
        context['original_element'] = self.element
        context['element'] = self.variation
        return context


class VariationPartialView(VariationBaseView):

    def get_template_names(self):
        return self.variation.template_names

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class VariationIframeView(VariationBaseView):
    __doc__ = 'Element view suitable for rendering in an iframe'

    def get_template_names(self):
        return [
         '%s/mote/element/iframe.html' % self.element.project.id,
         'mote/element/iframe.html']