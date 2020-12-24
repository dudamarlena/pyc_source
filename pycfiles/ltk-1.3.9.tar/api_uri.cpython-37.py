# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek/lib/python3.7/site-packages/ltk/api_uri.py
# Compiled at: 2020-04-15 14:10:55
# Size of source mod 2**32: 1433 bytes
API_URI = {'community':'/api/community', 
 'project':'/api/project', 
 'project_id':'/api/project/%(project_id)s', 
 'project_translation':'/api/project/%(project_id)s/translation', 
 'project_translation_locale':'/api/project/%(project_id)s/translation/%(locale)s', 
 'project_status':'/api/project/%(project_id)s/status', 
 'document':'/api/document', 
 'document_id':'/api/document/%(document_id)s', 
 'document_translation':'/api/document/%(document_id)s/translation', 
 'document_status':'/api/document/%(document_id)s/status', 
 'document_content':'/api/document/%(document_id)s/content', 
 'document_translation_locale':'/api/document/%(document_id)s/translation/%(locale)s', 
 'document_latest_version':'/api/document/%(document_id)s/latest-version', 
 'document_format':'/api/document/format', 
 'workflow':'/api/workflow', 
 'filter':'/api/filter', 
 'filter_id':'/api/filter/%(filter_id)s', 
 'filter_content':'/api/filter/%(filter_id)s/content', 
 'document_cancel':'/api/document/%(document_id)s/cancel', 
 'document_cancel_locale':'/api/document/%(document_id)s/translation/%(locale)s/cancel', 
 'process':'/api/process/%(process_id)s', 
 'reference':'/api/document/%(document_id)s/reference-material', 
 'reference_id':'/api/document/%(document_id)s/reference-material/%(reference_id)s'}