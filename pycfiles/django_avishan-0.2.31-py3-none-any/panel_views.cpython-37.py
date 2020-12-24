# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/parkners_new/avishan/views/panel_views.py
# Compiled at: 2020-03-23 16:20:23
# Size of source mod 2**32: 9107 bytes
from typing import Optional, List, Type, Union
from django.shortcuts import redirect
from avishan import current_request
from avishan.configure import get_avishan_config
from avishan.exceptions import AvishanException, AuthException, ErrorMessageException
from avishan.libraries.admin_lte.classes import *
from avishan.libraries.admin_lte.model import AvishanModelPanelEnabled
from avishan.misc.translation import AvishanTranslatable
from avishan.models import AvishanModel, KeyValueAuthentication, EmailPasswordAuthenticate, PhonePasswordAuthenticate, OtpAuthentication, AuthenticationType, UserGroup
from avishan.utils import all_subclasses
from avishan.views.class_based import AvishanTemplateView

class AvishanPanelWrapperView(AvishanTemplateView):
    template_file_address = 'avishan/panel/pages/panel_page.html'
    template_file_address: str
    template_url = None
    template_url: str
    sidebar_visible = False
    sidebar_visible: bool
    sidebar_title = 'Untitled'
    sidebar_title: Optional[str]
    sidebar_fa_icon = 'fa-circle-o'
    sidebar_fa_icon: Optional[str]
    sidebar_parent_view = None
    sidebar_parent_view: Optional['AvishanPanelWrapperView']
    sidebar_order = -1
    sidebar_order: int

    def dispatch(self, request, *args, **kwargs):
        self.parse_request_post_to_data()
        try:
            result = (self._dispatch)(request, *args, **kwargs)
            if result is None:
                return self.render()
            return result
        except AvishanException as e:
            try:
                if isinstance(e, AuthException):
                    if e.error_kind in AuthException.get_login_required_errors():
                        return redirect(to=(AvishanPanelLoginPage.template_url))
            finally:
                e = None
                del e

        except Exception as e:
            try:
                AvishanException(wrap_exception=e)
            finally:
                e = None
                del e

        return redirect(to=(AvishanPanelErrorPage.template_url + f"?from={self.template_url}"), felan=(self.template_url))

    def _dispatch(self, request, *args, **kwargs):
        return (super().dispatch)(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render()


class AvishanPanelLoginPage(AvishanPanelWrapperView):
    template_file_address = 'avishan/panel/pages/login_page.html'
    template_url = f"/{get_avishan_config().PANEL_ROOT}/login"
    login_class = None
    login_class: Type[AuthenticationType]
    authenticate = False

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.login_class = AvishanModel.get_model_with_class_name(get_avishan_config().PANEL_LOGIN_CLASS_NAME)
        self.form = Form(action_url=(self.template_url),
          method='post',
          button=Button(text='ورود'),
          items_margin=Margin(bottom=2),
          name='sign_in')
        if issubclass(self.login_class, KeyValueAuthentication):
            if issubclass(self.login_class, EmailPasswordAuthenticate):
                self.form.add_item(IconAddedInputFormElement(name='key',
                  input_type='email',
                  fa_icon='fa-envelope',
                  label='ایمیل'))
            else:
                if issubclass(self.login_class, PhonePasswordAuthenticate):
                    self.form.add_item(IconAddedInputFormElement(name='key',
                      input_type='tel',
                      fa_icon='fa-phone-square',
                      label='شماره همراه'))
                else:
                    raise NotImplementedError
            self.context['login_type'] = 'key_value'
            self.form.add_item(IconAddedInputFormElement(name='value',
              input_type='password',
              fa_icon='fa-lock',
              label='رمز عبور'))
        else:
            if issubclass(self.login_class, OtpAuthentication):
                self.context['login_type'] = 'otp'
                raise NotImplementedError
            else:
                raise NotImplementedError

    def post(self, request, *args, **kwargs):
        if issubclass(self.login_class, OtpAuthentication):
            raise NotImplementedError
        else:
            if issubclass(self.login_class, KeyValueAuthentication):
                self.login_class.login(key=(self.request.data['sign_in__key']),
                  password=(self.request.data['sign_in__value']),
                  user_group=UserGroup.get(title=(get_avishan_config().PANEL_LOGIN_USER_GROUP_TITLE)))
        return redirect(AvishanPanelPage.template_url)


class AvishanPanelLogoutPage(AvishanPanelWrapperView):
    template_url = f"/{get_avishan_config().PANEL_ROOT}/logout"

    def get(self, request, *args, **kwargs):
        self.current_request['add_token'] = False
        return redirect(AvishanPanelLoginPage.template_url)


class AvishanPanelErrorPage(AvishanPanelWrapperView):
    template_file_address = 'avishan/panel/pages/error_page.html'
    template_url = f"/{get_avishan_config().PANEL_ROOT}/error"
    authenticate = False

    def get(self, request, *args, **kwargs):
        self.redirected_from = self.request.GET.get('from', None)
        if self.redirected_from == self.template_url:
            self.redirected_from = get_avishan_config().PANEL_ROOT
        return self.render()


class AvishanPanelPage(AvishanPanelWrapperView):
    template_url = f"/{get_avishan_config().PANEL_ROOT}"
    page_header_text = ''
    page_header_text: str
    track_it = True
    contents = []
    contents: List[DivComponent]

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.clean_class()
        self.sidebar = Sidebar()
        for sub_class in all_subclasses(AvishanModelPanelEnabled):
            if not sub_class._meta.abstract:
                if not sub_class.sidebar_visible:
                    continue
                self.sidebar.add_item(SidebarItem(text=(sub_class.panel_plural_name()),
                  link=f"/{get_avishan_config().PANEL_ROOT}/{sub_class.class_plural_snake_case_name()}",
                  icon=(sub_class.sidebar_fa_icon)))

        self.navbar = Navbar(background_color=(Color('white')))
        self.navbar.navbar_items.append(NavbarItem(link=(AvishanPanelLogoutPage.template_url), icon='fa-sign-out'))

    def clean_class(self):
        self.page_header_text = ''
        self.contents = []

    def get(self, request, *args, **kwargs):
        pass


class AvishanPanelModelPage(AvishanPanelPage):
    model = None
    model: Optional[Type[Union[(AvishanModel, AvishanModelPanelEnabled)]]]
    item = None
    item: Optional[Union[(AvishanModel, AvishanModelPanelEnabled)]]
    model_function = None
    model_function: Optional[str]
    item_id = None
    item_id: Optional[int]
    item_function = None
    item_function: Optional[str]

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.clean_class()
        self.populate_from_url()
        if self.model is None:
            raise ErrorMessageException(AvishanTranslatable(EN='Model not found'))
        if not issubclass(self.model, AvishanModelPanelEnabled):
            raise ErrorMessageException(AvishanTranslatable(EN='Model not inherited from "AvishanPanelEnabled" class'))
        self.model.panel_view = self

    def _dispatch(self, request, *args, **kwargs):
        if self.model_function:
            return self.model.call_panel_model_function(self.model_function)
        if self.item_id:
            try:
                self.item = self.model.get(id=(self.item_id))
            except self.model.DoesNotExist:
                ErrorMessageException(AvishanTranslatable(EN=f"Item not found with id={self.item_id}"))

            if self.item_function:
                return self.item.call_panel_item_function(self.item_function)
            return redirect((self.request.path + '/detail'), permanent=True)
        return self.model.call_panel_model_function('list')

    @property
    def template_url(self) -> str:
        return f"/{get_avishan_config().PANEL_ROOT}/{self.model.class_plural_snake_case_name()}"

    def populate_from_url(self):
        url = current_request['request'].path[len(get_avishan_config().PANEL_ROOT) + 2:]
        url = url.split('/')
        self.model = AvishanModel.get_model_by_plural_snake_case_name(url[0])
        if len(url) > 1:
            try:
                self.item_id = int(url[1])
                if len(url) > 2:
                    self.item_function = url[2]
            except ValueError:
                self.model_function = url[1]

    def clean_class(self):
        super().clean_class()
        self.model = None
        self.item = None
        self.model_function = None
        self.item_id = None
        self.item_function = None


class AvishanPanelTestPage(AvishanTemplateView):
    authenticate = False
    template_file_address = 'avishan/panel/test_page.html'

    def get(self, request, *args, **kwargs):
        return self.render()