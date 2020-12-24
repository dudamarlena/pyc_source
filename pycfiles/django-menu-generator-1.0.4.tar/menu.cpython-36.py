# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/miltonln/Proyectos/django-menu-generator/menu_generator/menu.py
# Compiled at: 2018-01-31 10:30:52
# Size of source mod 2**32: 5150 bytes
import copy, django
from django.core.exceptions import ImproperlyConfigured
from .utils import get_callable
if django.VERSION >= (1, 10):
    from django.urls import reverse, NoReverseMatch
else:
    from django.core.urlresolvers import reverse, NoReverseMatch

class MenuBase(object):
    __doc__ = '\n    Base class that generates menu list.\n    '

    def __init__(self):
        self.path = ''
        self.request = None

    def save_user_state(self, request):
        """
        Given a request object, store the current user attributes
        :param request: HttpRequest
        """
        self.request = request
        self.path = request.path

    def _is_validated(self, item_dict):
        """
        Given a menu item dictionary, it returns true if the user passes all the validator's conditions, it means,
        if the user passes all the conditions, the user can see the menu
        """
        validators = item_dict.get('validators')
        if not validators:
            return True
        else:
            if not isinstance(validators, (list, tuple)):
                raise ImproperlyConfigured('validators must be a list')
            result_validations = []
            for validator in validators:
                if isinstance(validator, tuple):
                    if len(validator) <= 1:
                        raise ImproperlyConfigured('You are passing a tuple validator without args %s' % str(validator))
                    func = get_callable(validator[0])
                    args = validator[1:]
                    result_validations.append(func(self.request, *args))
                else:
                    func = get_callable(validator)
                    result_validations.append(func(self.request))

            return all(result_validations)

    def _has_attr(self, item_dict, attr):
        """
        Given a menu item dictionary, it returns true if an attr is set.
        """
        if item_dict.get(attr, False):
            return True
        else:
            return False

    def _get_icon(self, parent_dict):
        """
        Given a menu item dictionary, this returns an icon class if one exist, or
        returns an empty string.
        """
        return parent_dict.get('icon_class', '')

    def _get_url(self, item_dict):
        """
        Given a menu item dictionary, it returns the URL or an empty string.
        """
        url = item_dict.get('url', '')
        try:
            final_url = reverse(**url) if type(url) is dict else reverse(url)
        except NoReverseMatch:
            final_url = url

        return final_url

    def _is_selected(self, item_dict):
        """
        Given a menu item dictionary, it returns true if `url` is on path.
        """
        url = self._get_url(item_dict)
        return url == self.path

    def _process_breadcrums(self, menu_list):
        """
        Given a menu list, it marks the items on the current path as selected, which
        can be used as breadcrumbs
        """
        for item in menu_list:
            if item['submenu']:
                item['selected'] = self._process_breadcrums(item['submenu'])
            if item['selected']:
                return True

        return False

    def _get_submenu_list(self, parent_dict):
        """
        Given a menu item dictionary, it returns a submenu if one exist, or
        returns None.
        """
        submenu = parent_dict.get('submenu', None)
        if submenu:
            for child_dict in submenu:
                child_dict['validators'] = list(set(list(parent_dict.get('validators', [])) + list(child_dict.get('validators', []))))

            submenu = self.generate_menu(submenu)
            if not submenu:
                submenu = None
        return submenu

    def _get_menu_list(self, list_dict):
        """
        A generator that returns only the visible menu items.
        """
        for item in list_dict:
            if self._has_attr(item, 'name') and self._has_attr(item, 'url') and self._is_validated(item):
                yield copy.copy(item)

    def generate_menu(self, list_dict):
        """
        Given a list of dictionaries, returns a menu list.
        """
        visible_menu = []
        for item in self._get_menu_list(list_dict):
            item['url'] = self._get_url(item)
            item['selected'] = self._is_selected(item)
            item['submenu'] = self._get_submenu_list(item)
            item['icon_class'] = self._get_icon(item)
            visible_menu.append(item)

        self._process_breadcrums(visible_menu)
        return visible_menu


class Menu(MenuBase):
    __doc__ = '\n    Class that generates menu list.\n    '

    def __call__(self, request, list_dict):
        self.save_user_state(request)
        return self.generate_menu(list_dict)


generate_menu = Menu()