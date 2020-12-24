# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/schemas/schemas_cli_message_generator.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 1353 bytes
"""
Contains message used by Schemas paginated CLI.
"""

def construct_cli_display_message_for_schemas(page_to_render, last_page_number=None):
    if last_page_number is None:
        last_page_number = 'many'
    single_page = 'Event Schemas'
    first_page = 'Event Schemas [Page %s/%s] (Enter N for next page)' % (page_to_render, last_page_number)
    middle_page = 'Event Schemas [Page %s/%s] (Enter N/P for next/previous page)' % (page_to_render, last_page_number)
    last_page = 'Event Schemas [Page %s/%s] (Enter P for previous page)' % (page_to_render, last_page_number)
    return {'single_page':single_page,  'first_page':first_page,  'middle_page':middle_page,  'last_page':last_page}


def construct_cli_display_message_for_registries(page_to_render, last_page_number=None):
    if last_page_number is None:
        last_page_number = 'many'
    single_page = 'Schema Registry'
    first_page = 'Schema Registry [Page %s/%s] (Enter N for next page)' % (page_to_render, last_page_number)
    middle_page = 'Schema Registry [Page %s/%s] (Enter N/P for next/previous page)' % (page_to_render, last_page_number)
    last_page = 'Schema Registry [Page %s/%s] (Enter P for previous page)' % (page_to_render, last_page_number)
    return {'single_page':single_page,  'first_page':first_page,  'middle_page':middle_page,  'last_page':last_page}