# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/paginator.py
# Compiled at: 2016-11-29 15:20:13
# Size of source mod 2**32: 3095 bytes
from django.http.request import HttpRequest
from django.utils import six
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger
from ginger import utils
from ginger import ui
__all__ = [
 'GingerPaginator', 'GingerPage', 'paginate']

class GingerPage(Page):

    def create_link(self, request, number):
        param = self.paginator.parameter_name
        url = utils.get_url_with_modified_params(request, {param: number})
        return ui.Link(url=url, content=(six.text_type(number)), is_active=(number == self.number))

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
        (super(GingerPaginator, self).__init__)(object_list, per_page, **kwargs)

    def validate_number--- This code section failed: ---

 L.  50         0  SETUP_EXCEPT         14  'to 14'

 L.  51         2  LOAD_GLOBAL              int
                4  LOAD_FAST                'number'
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  STORE_FAST               'number'
               10  POP_BLOCK        
               12  JUMP_FORWARD         46  'to 46'
             14_0  COME_FROM_EXCEPT      0  '0'

 L.  52        14  DUP_TOP          
               16  LOAD_GLOBAL              TypeError
               18  LOAD_GLOBAL              ValueError
               20  BUILD_TUPLE_2         2 
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    44  'to 44'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  53        32  LOAD_GLOBAL              PageNotAnInteger
               34  LOAD_STR                 'That page number is not an integer'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  RAISE_VARARGS_1       1  'exception'
               40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'
             46_1  COME_FROM            12  '12'

 L.  54        46  LOAD_FAST                'number'
               48  LOAD_CONST               1
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L.  55        54  LOAD_GLOBAL              EmptyPage
               56  LOAD_STR                 'That page number is less than 1'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  RAISE_VARARGS_1       1  'exception'
             62_0  COME_FROM            52  '52'

 L.  56        62  LOAD_FAST                'number'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                num_pages
               68  COMPARE_OP               >
               70  POP_JUMP_IF_FALSE   102  'to 102'

 L.  57        72  LOAD_FAST                'self'
               74  LOAD_ATTR                allow_empty
               76  POP_JUMP_IF_TRUE    102  'to 102'
               78  LOAD_FAST                'number'
               80  LOAD_CONST               1
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    94  'to 94'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                allow_empty_first_page
             90_0  COME_FROM            76  '76'
               90  POP_JUMP_IF_FALSE    94  'to 94'

 L.  58        92  JUMP_FORWARD        102  'to 102'
             94_0  COME_FROM            84  '84'

 L.  60        94  LOAD_GLOBAL              EmptyPage
               96  LOAD_STR                 'That page contains no results'
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  RAISE_VARARGS_1       1  'exception'
            102_0  COME_FROM            92  '92'
            102_1  COME_FROM            70  '70'

 L.  61       102  LOAD_FAST                'number'
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 90

    def page(self, value):
        """
        Returns a Page object for the given 1-based page number.
        """
        if isinstance(value, HttpRequest):
            value = value.GET.get(self.parameter_name, 1)
        else:
            if isinstance(value, dict):
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