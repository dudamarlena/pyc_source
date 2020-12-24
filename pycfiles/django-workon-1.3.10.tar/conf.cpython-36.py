# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/conf.py
# Compiled at: 2018-08-29 05:22:37
# Size of source mod 2**32: 1671 bytes
from django.apps import AppConfig
from django.conf import settings
import workon.utils

class WorkonConfig(AppConfig):
    name = 'workon'


WORKON = getattr(settings, 'WORKON', dict())
LIST_LAYOUT_TEMPLATE = WORKON.get('LIST_LAYOUT_TEMPLATE', 'workon/views/list/layout.html')
LIST_TEMPLATE = WORKON.get('LIST_TEMPLATE', 'workon/views/list/list.html')
LIST_RESULTS_TEMPLATE = WORKON.get('LIST_RESULTS_TEMPLATE', 'workon/views/list/_list.html')
LIST_ROW_TEMPLATE = WORKON.get('LIST_ROW_TEMPLATE', 'workon/views/list/_row.html')
LIST_DEFAULT_METHOD = WORKON.get('LIST_DEFAULT_METHOD', 'data-modal')
LIST_ROW_CREATE_METHOD = WORKON.get('LIST_ROW_CREATE_METHOD', LIST_DEFAULT_METHOD)
LIST_ROW_VIEW_METHOD = WORKON.get('LIST_ROW_VIEW_METHOD', LIST_DEFAULT_METHOD)
LIST_ROW_UPDATE_METHOD = WORKON.get('LIST_ROW_UPDATE_METHOD', LIST_DEFAULT_METHOD)
LIST_ROW_UPDATE_ON_DOUBLE_CLICK = WORKON.get('LIST_ROW_UPDATE_ON_DOUBLE_CLICK', True)
LIST_ROW_UPDATE_ON_DOUBLE_CLICK_METHOD = WORKON.get('LIST_ROW_UPDATE_ON_DOUBLE_CLICK_METHOD', 'data-dblclick-modal')
LIST_ROW_DELETE_METHOD = WORKON.get('LIST_ROW_DELETE_METHOD', LIST_DEFAULT_METHOD)
LIST_FLOATING_ACTIONS_TEMPLATE = WORKON.get('LIST_FLOATING_ACTIONS_TEMPLATE', None)
SAVE_LAYOUT_TEMPLATE = WORKON.get('SAVE_LAYOUT_TEMPLATE', 'workon/save/layout.html')
SAVE_TEMPLATE = WORKON.get('SAVE_TEMPLATE', 'workon/views/save/save.html')
SAVE_MODAL_ACTIONS_TEMPLATE = WORKON.get('SAVE_MODAL_ACTIONS_TEMPLATE', 'workon/views/save/_modal_actions.html')
SELECT2_CACHE_BACKEND = WORKON.get('SELECT2_CACHE_BACKEND', 'default')
SELECT2_CACHE_PREFIX = WORKON.get('SELECT2_CACHE_PREFIX', 'select2_')