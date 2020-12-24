# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/metadata.py
# Compiled at: 2019-10-27 19:02:52
# Size of source mod 2**32: 463 bytes
from rest_framework.metadata import SimpleMetadata

class CustomMetadata(SimpleMetadata):

    def determine_actions(self, request, view):
        actions = {}
        for method, action in view.action_map.items():
            if method.lower() == 'delete':
                continue
            view.action = action
            serializer = view.get_serializer()
            actions[method.upper()] = self.get_serializer_info(serializer)

        return actions