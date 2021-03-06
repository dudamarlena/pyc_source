# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/views/panel_views.py
# Compiled at: 2020-04-21 05:34:59
# Size of source mod 2**32: 10547 bytes
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

    def dispatch--- This code section failed: ---

 L.  29         0  LOAD_FAST                'self'
                2  LOAD_METHOD              parse_request_post_to_data
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  30         8  SETUP_FINALLY        52  'to 52'

 L.  31        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _dispatch
               14  LOAD_FAST                'request'
               16  BUILD_TUPLE_1         1 
               18  LOAD_FAST                'args'
               20  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               22  LOAD_FAST                'kwargs'
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  STORE_FAST               'result'

 L.  32        28  LOAD_FAST                'result'
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE    46  'to 46'

 L.  33        36  LOAD_FAST                'self'
               38  LOAD_METHOD              render
               40  CALL_METHOD_0         0  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM            34  '34'

 L.  34        46  LOAD_FAST                'result'
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY     8  '8'

 L.  35        52  DUP_TOP          
               54  LOAD_GLOBAL              AvishanException
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE   128  'to 128'
               60  POP_TOP          
               62  STORE_FAST               'e'
               64  POP_TOP          
               66  SETUP_FINALLY       116  'to 116'

 L.  36        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'e'
               72  LOAD_GLOBAL              AuthException
               74  CALL_FUNCTION_2       2  ''
               76  POP_JUMP_IF_FALSE   112  'to 112'
               78  LOAD_FAST                'e'
               80  LOAD_ATTR                error_kind
               82  LOAD_GLOBAL              AuthException
               84  LOAD_METHOD              get_login_required_errors
               86  CALL_METHOD_0         0  ''
               88  COMPARE_OP               in
               90  POP_JUMP_IF_FALSE   112  'to 112'

 L.  37        92  LOAD_GLOBAL              redirect
               94  LOAD_GLOBAL              AvishanPanelLoginPage
               96  LOAD_ATTR                template_url
               98  LOAD_CONST               ('to',)
              100  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              102  ROT_FOUR         
              104  POP_BLOCK        
              106  POP_EXCEPT       
              108  CALL_FINALLY        116  'to 116'
              110  RETURN_VALUE     
            112_0  COME_FROM            90  '90'
            112_1  COME_FROM            76  '76'
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM           108  '108'
            116_1  COME_FROM_FINALLY    66  '66'
              116  LOAD_CONST               None
              118  STORE_FAST               'e'
              120  DELETE_FAST              'e'
              122  END_FINALLY      
              124  POP_EXCEPT       
              126  JUMP_FORWARD        172  'to 172'
            128_0  COME_FROM            58  '58'

 L.  38       128  DUP_TOP          
              130  LOAD_GLOBAL              Exception
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   170  'to 170'
              136  POP_TOP          
              138  STORE_FAST               'e'
              140  POP_TOP          
              142  SETUP_FINALLY       158  'to 158'

 L.  39       144  LOAD_GLOBAL              AvishanException
              146  LOAD_FAST                'e'
              148  LOAD_CONST               ('wrap_exception',)
              150  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              152  POP_TOP          
              154  POP_BLOCK        
              156  BEGIN_FINALLY    
            158_0  COME_FROM_FINALLY   142  '142'
              158  LOAD_CONST               None
              160  STORE_FAST               'e'
              162  DELETE_FAST              'e'
              164  END_FINALLY      
              166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM           134  '134'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM           126  '126'

 L.  40       172  LOAD_GLOBAL              redirect
              174  LOAD_GLOBAL              AvishanPanelErrorPage
              176  LOAD_ATTR                template_url
              178  LOAD_STR                 '?from='
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                template_url
              184  FORMAT_VALUE          0  ''
              186  BUILD_STRING_2        2 
              188  BINARY_ADD       
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                template_url
              194  LOAD_CONST               ('to', 'felan')
              196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              198  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 104

    def _dispatch(self, request, *args, **kwargs):
        return (super().dispatch)(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render


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
        if issubclassself.login_classKeyValueAuthentication:
            if issubclassself.login_classEmailPasswordAuthenticate:
                self.form.add_item(IconAddedInputFormElement(name='key',
                  input_type='email',
                  fa_icon='fa-envelope',
                  label='ایمیل'))
            else:
                if issubclassself.login_classPhonePasswordAuthenticate:
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
            if issubclassself.login_classOtpAuthentication:
                self.context['login_type'] = 'otp'
                raise NotImplementedError
            else:
                raise NotImplementedError

    def post(self, request, *args, **kwargs):
        if issubclassself.login_classOtpAuthentication:
            raise NotImplementedError
        else:
            if issubclassself.login_classKeyValueAuthentication:
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
        return self.render


class AvishanPanelPage(AvishanPanelWrapperView):
    template_url = f"/{get_avishan_config().PANEL_ROOT}"
    page_header_text = ''
    page_header_text: str
    track_it = True
    contents = []
    contents: List[DivComponent]

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.clean_class
        self.sidebar = Sidebar().add_item(SidebarItem(text='داشبورد',
          link=f"/{get_avishan_config().PANEL_ROOT}",
          icon='fa-dashboard'))
        for sub_class in sorted((all_subclasses(AvishanModelPanelEnabled)), key=(lambda x: x.sidebar_order)):
            if not sub_class._meta.abstract:
                if not sub_class.sidebar_visible:
                    pass
                else:
                    self.sidebar.add_item(SidebarItem(text=(sub_class.panel_plural_name),
                      link=f"/{get_avishan_config().PANEL_ROOT}/{sub_class.class_plural_snake_case_name}",
                      icon=(sub_class.sidebar_fa_icon)))
            self.navbar = Navbar(background_color=(Color('white')))
            self.navbar.navbar_items.append(NavbarItem(link=(AvishanPanelLogoutPage.template_url), icon='fa-sign-out'))

    def clean_class(self):
        self.page_header_text = ''
        self.contents = []

    def get(self, request, *args, **kwargs):
        pass


class AvishanPanelDashboardPage(AvishanPanelPage):
    template_url = f"/{get_avishan_config().PANEL_ROOT}"

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.dashboard_items = []
        self.page_header_text = 'داشبورد'
        for model in all_subclasses(AvishanModelPanelEnabled):
            self.dashboard_items.extend(model.panel_dashboard_items)

    def rows(self) -> List[Row]:
        rows = {}
        created = []
        for item in sorted((self.dashboard_items), key=(lambda x: x.row)):
            if item.row not in rows.keys:
                rows[item.row] = []
            rows[item.row].append(item)
        else:
            for row_key in sorted(rows.keys):
                row = Row()
                for item in sorted((rows[row_key]), key=(lambda x: x.order)):
                    row.add_item(item.col.add_item(item.item))
                else:
                    created.append(row)

            else:
                return created

    def get(self, request, *args, **kwargs):
        self.contents.extend(self.rows)
        return (super().get)(request, *args, **kwargs)


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
        self.clean_class
        self.populate_from_url
        if self.model is None:
            raise ErrorMessageException(AvishanTranslatable(EN='Model not found'))
        if not issubclassself.modelAvishanModelPanelEnabled:
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
            else:
                if self.item_function:
                    return self.item.call_panel_item_function(self.item_function)
                return redirect((self.request.path + '/detail'), permanent=True)
        return self.model.call_panel_model_function('list')

    @property
    def template_url(self) -> str:
        return f"/{get_avishan_config().PANEL_ROOT}/{self.model.class_plural_snake_case_name}"

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
        super().clean_class
        self.model = None
        self.item = None
        self.model_function = None
        self.item_id = None
        self.item_function = None


class AvishanPanelTestPage(AvishanTemplateView):
    authenticate = False
    template_file_address = 'avishan/panel/test_page.html'

    def get(self, request, *args, **kwargs):
        return self.render