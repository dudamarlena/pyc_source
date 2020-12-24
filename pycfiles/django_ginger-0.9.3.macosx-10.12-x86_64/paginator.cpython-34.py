# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/paginator.py
# Compiled at: 2015-10-05 16:22:09
# Size of source mod 2**32: 3134 bytes
from django.http.request import HttpRequest
from django.utils import six
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger
from ginger import utils
from ginger import ui
__all__ = [
 'GingerPaginator', 'GingerPage', 'paginate']

class GingerPage(Page):

    def create_link(self, request, number):
        base_url = request.get_full_path()
        param = self.paginator.parameter_name
        url = utils.get_url_with_modified_params(request, {param: number})
        return ui.Link(url=url, content=six.text_type(number), is_active=url == base_url)

    def build_links(self, request):
        for i in utils.generate_pages(self.number, self.paginator.page_limit, self.paginator.num_pages):
            yield self.create_link(request, i)

    def previous_link(self, request):
        number = self.previous_page_number()
        return self.create_link(request, number)

    def next_link(self, request):
        number = self.next_page_number()
        return self.create_link(request, number)


class GingerPaginator(Paginator):
    parameter_name = 'page'
    page_limit = 10
    allow_empty = False

    def __init__(self, object_list, per_page, **kwargs):
        self.parameter_name = kwargs.pop('parameter_name', self.parameter_name)
        self.allow_empty = kwargs.pop('allow_empty', self.allow_empty)
        self.page_limit = kwargs.pop('page_limit', self.page_limit)
        super(GingerPaginator, self).__init__(object_list, per_page, **kwargs)

    def validate_number--- This code section failed: ---

 L.  51         0  SETUP_EXCEPT         19  'to 19'

 L.  52         3  LOAD_GLOBAL              int
                6  LOAD_FAST                'number'
                9  CALL_FUNCTION_1       1  '1 positional, 0 named'
               12  STORE_FAST               'number'
               15  POP_BLOCK        
               16  JUMP_FORWARD         55  'to 55'
             19_0  COME_FROM_EXCEPT      0  '0'

 L.  53        19  DUP_TOP          
               20  LOAD_GLOBAL              TypeError
               23  LOAD_GLOBAL              ValueError
               26  BUILD_TUPLE_2         2 
               29  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    54  'to 54'
               35  POP_TOP          
               36  POP_TOP          
               37  POP_TOP          

 L.  54        38  LOAD_GLOBAL              PageNotAnInteger
               41  LOAD_STR                 'That page number is not an integer'
               44  CALL_FUNCTION_1       1  '1 positional, 0 named'
               47  RAISE_VARARGS_1       1  'exception'
               50  POP_EXCEPT       
               51  JUMP_FORWARD         55  'to 55'
               54  END_FINALLY      
             55_0  COME_FROM            51  '51'
             55_1  COME_FROM            16  '16'

 L.  55        55  LOAD_FAST                'number'
               58  LOAD_CONST               1
               61  COMPARE_OP               <
               64  POP_JUMP_IF_FALSE    82  'to 82'

 L.  56        67  LOAD_GLOBAL              EmptyPage
               70  LOAD_STR                 'That page number is less than 1'
               73  CALL_FUNCTION_1       1  '1 positional, 0 named'
               76  RAISE_VARARGS_1       1  'exception'
               79  JUMP_FORWARD         82  'to 82'
             82_0  COME_FROM            79  '79'

 L.  57        82  LOAD_FAST                'number'
               85  LOAD_FAST                'self'
               88  LOAD_ATTR                num_pages
               91  COMPARE_OP               >
               94  POP_JUMP_IF_FALSE   145  'to 145'

 L.  58        97  LOAD_FAST                'self'
              100  LOAD_ATTR                allow_empty
              103  POP_JUMP_IF_TRUE    142  'to 142'
              106  LOAD_FAST                'number'
              109  LOAD_CONST               1
              112  COMPARE_OP               ==
              115  POP_JUMP_IF_FALSE   130  'to 130'
              118  LOAD_FAST                'self'
              121  LOAD_ATTR                allow_empty_first_page
            124_0  COME_FROM           115  '115'
            124_1  COME_FROM           103  '103'
              124  POP_JUMP_IF_FALSE   130  'to 130'

 L.  59       127  JUMP_ABSOLUTE       145  'to 145'
              130  ELSE                     '142'

 L.  61       130  LOAD_GLOBAL              EmptyPage
              133  LOAD_STR                 'That page contains no results'
              136  CALL_FUNCTION_1       1  '1 positional, 0 named'
              139  RAISE_VARARGS_1       1  'exception'
              142  JUMP_FORWARD        145  'to 145'
            145_0  COME_FROM           142  '142'

 L.  62       145  LOAD_FAST                'number'
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 142

    def page(self, value):
        """
        Returns a Page object for the given 1-based page number.
        """
        if isinstance(value, HttpRequest):
            value = value.GET.get(self.parameter_name, 1)
        elif isinstance(value, dict):
            value = value.get(self.parameter_name, 1)
        number = self.validate_number(value)
        if number > self.num_pages:
            result = self.object_list.none() if hasattr(self.object_list, 'none') else []
        else:
            bottom = (number - 1) * self.per_page
            top = bottom + self.per_page
            if top + self.orphans >= self.count:
                top = self.count
            result = self.object_list[bottom:top]
        return self._get_page(result, number, self)

    def _get_page(self, *args, **kwargs):
        return GingerPage(*args, **kwargs)


def paginate(object_list, page, **kwargs):
    return GingerPaginator(object_list, **kwargs).page(page)