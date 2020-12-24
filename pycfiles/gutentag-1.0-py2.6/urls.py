# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tagbase\urls.py
# Compiled at: 2009-08-06 01:21:29
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', ('^gutentag/$', 'tagbase.gutentag.views.main'), ('^gutentag/add/$',
                                                                            'tagbase.gutentag.views.add'), ('^gutentag/doblast/$',
                                                                                                            'tagbase.gutentag.views.doblast'), ('^gutentag/blastSearch/$',
                                                                                                                                                'tagbase.gutentag.views.blastSearch'), ('^gutentag/upload/$',
                                                                                                                                                                                        'tagbase.gutentag.views.upload'), ('^gutentag/go/(?P<go_id>\\d+)/$',
                                                                                                                                                                                                                           'tagbase.gutentag.views.go'), ('^gutentag/goSeq/(?P<go_id>\\d+)/$',
                                                                                                                                                                                                                                                          'tagbase.gutentag.views.goSeq'), ('^gutentag/mainSearch/$',
                                                                                                                                                                                                                                                                                            'tagbase.gutentag.views.mainSearch'), ('^gutentag/getSeq/$',
                                                                                                                                                                                                                                                                                                                                   'tagbase.gutentag.views.getSeq'), ('^gutentag/getTags/(?P<gene_id>\\w+)/$',
                                                                                                                                                                                                                                                                                                                                                                      'tagbase.gutentag.views.getTags'), ('^gutentag/getThisSeq/(?P<seq_id>\\w+)/$',
                                                                                                                                                                                                                                                                                                                                                                                                          'tagbase.gutentag.views.getThisSeq'), ('^gutentag/(?P<tag_name>\\w.+)/(?P<tag_type>\\w+)/tag/$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                 'tagbase.gutentag.views.tagCloudSearch'), (
 '^admin/', include(admin.site.urls)), (
 '^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}))