# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/repositories/base.py
# Compiled at: 2017-06-18 15:44:17
# Size of source mod 2**32: 3434 bytes
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _
from moneta.repository.models import Element
from moneta.utils import import_path
__author__ = 'flanker'

class RepositoryModelsClasses(object):
    _models = None

    @classmethod
    def get_model(cls, cls_name):
        return cls.get_models()[cls_name]

    @classmethod
    def get_models(cls):
        if cls._models is None:
            cls._models = {}
            for mw_path in settings.REPOSITORY_CLASSES:
                modelcls = import_path(mw_path)()
                cls._models[modelcls.archive_type] = modelcls

        return cls._models

    def __iter__(self):
        for x, y in self.get_models().items():
            yield (x, str(y))


class RepositoryModel(object):
    verbose_name = _('Repository')
    archive_type = 'RepositoryModel'

    def __str__(self):
        """
        returns a unicode representation of this repository
        :return: unicode representation
        """
        return self.verbose_name

    def is_file_valid(self, uploaded_file):
        """ Evaluate if the uploaded file is valid for this repository model

        The main attributes of `uploaded_file` are `name` and `file`

        :param uploaded_file:
        :type uploaded_file: :class:`dango.core.uploadedfile.UploadedFile`
        :return: True if this element is acceptable for this model, else False
        :raise:
        """
        return True

    def delete_element(self, rel):
        pass

    def update_element(self, element):
        """
        Extract some informations from element to prepare the repository
        :param element: Element to add to the repository
        :return: Unicode string containing meta-data
        """
        return ''

    def finish_element(self, element: Element, states: list):
        """
        Called after the .save() operations, with all states associated to this new element.
        Currently, only add all states to this element.
        :param element: Element
        :param states: list of ArchiveState
        """
        (element.states.add)(*states)

    def url_list(self):
        """
        Return a list of URL patterns specific to this repository
        :return: a patterns as expected by django
        """
        return []

    def public_url_list(self):
        return []

    def get_index_view(self, repo):
        return repo.model + ':index'

    def wrap_view(self, view, csrf_exempt=False):

        def wrapper(request, *args, **kwargs):
            try:
                return (getattr(self, view))(request, *args, **kwargs)
            except AttributeError:
                return HttpResponseBadRequest()

        if csrf_exempt:
            wrapper.csrf_exempt = True
        return wrapper

    def extra_index_urls(self, request, rid):
        """ Provides an iterable of tuples (URL, name), to add on the main index
        :param request: HttpRequest
        :param rid: Repository id
        """
        return []

    @property
    def urls(self):
        """
        Provides URLconf details for the ``Api`` and all registered
        ``Resources`` beneath it.
        """
        return [x for x in self.url_list()]

    @property
    def public_urls(self):
        return [x for x in self.public_url_list()]