# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redturtle/maps/portlet/browser/map.py
# Compiled at: 2009-01-06 06:49:26
from Products.Maps.browser.map import BaseMapView as BaseView
from Products.Maps.interfaces import IMapView
from zope.interface import implements
from zope.component._api import getMultiAdapter

class DefaultMapView(BaseView):
    __module__ = __name__
    implements(IMapView)

    @property
    def enabled--- This code section failed: ---

 L.  11         0  LOAD_GLOBAL           0  'getMultiAdapter'
                3  LOAD_FAST             0  'self'
                6  LOAD_ATTR             2  'context'
                9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             3  'request'
               15  BUILD_TUPLE_2         2 
               18  LOAD_CONST               'name'
               21  LOAD_CONST               'plone_context_state'
               24  CALL_FUNCTION_257   257  None
               27  STORE_FAST            3  'plone'

 L.  12        30  LOAD_FAST             0  'self'
               33  LOAD_ATTR             5  'map'
               36  LOAD_CONST               None
               39  COMPARE_OP            8  is
               42  JUMP_IF_FALSE         8  'to 53'
             45_0  THEN                     54
               45  POP_TOP          

 L.  13        46  LOAD_GLOBAL           7  'False'
               49  RETURN_VALUE     
               50  JUMP_FORWARD          1  'to 54'
             53_0  COME_FROM            42  '42'
               53  POP_TOP          
             54_0  COME_FROM            50  '50'

 L.  14        54  LOAD_FAST             3  'plone'
               57  LOAD_ATTR             8  'is_view_template'
               60  CALL_FUNCTION_0       0  None
               63  JUMP_IF_FALSE        65  'to 131'
             66_0  THEN                     132
               66  POP_TOP          
               67  BUILD_LIST_0          0 
               70  DUP_TOP          
               71  STORE_FAST            2  '_[1]'
               74  LOAD_FAST             0  'self'
               77  LOAD_ATTR             5  'map'
               80  LOAD_ATTR            10  'getMarkers'
               83  CALL_FUNCTION_0       0  None
               86  GET_ITER         
               87  FOR_ITER             27  'to 117'
               90  STORE_FAST            1  'm'
               93  LOAD_FAST             1  'm'
               96  LOAD_ATTR            12  'lon'
               99  JUMP_IF_FALSE        11  'to 113'
              102  POP_TOP          
              103  LOAD_FAST             2  '_[1]'
              106  LOAD_FAST             1  'm'
              109  LIST_APPEND      
              110  JUMP_BACK            87  'to 87'
            113_0  COME_FROM            99  '99'
              113  POP_TOP          
              114  JUMP_BACK            87  'to 87'
              117  DELETE_FAST           2  '_[1]'
              120  JUMP_IF_FALSE         8  'to 131'
            123_0  THEN                     128
              123  POP_TOP          

 L.  15       124  LOAD_GLOBAL          13  'True'
              127  RETURN_VALUE     
              128  JUMP_FORWARD          1  'to 132'
            131_0  COME_FROM           120  '120'
            131_1  COME_FROM            63  '63'
              131  POP_TOP          
            132_0  COME_FROM           128  '128'

 L.  16       132  LOAD_GLOBAL           7  'False'
              135  RETURN_VALUE     

Parse error at or near `LOAD_GLOBAL' instruction at offset 132