# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/config.py
# Compiled at: 2018-10-18 17:35:13
PROJECTNAME = 'brasil.gov.portal'
LOCAL_TIME_FORMAT = '%d/%m/%Y'
TIME_FORMAT = '%Hh%M'
LOCAL_LONG_TIME_FORMAT = ('{0} {1}').format(LOCAL_TIME_FORMAT, TIME_FORMAT)
REDES = [
 {'id': 'facebook', 'title': 'Facebook', 
    'url': 'https://www.facebook.com/%s'},
 {'id': 'twitter', 'title': 'Twitter', 
    'url': 'https://www.twitter.com/%s'},
 {'id': 'youtube', 'title': 'YouTube', 
    'url': 'https://www.youtube.com/%s'},
 {'id': 'flickr', 'title': 'Flickr', 
    'url': 'https://www.flickr.com/%s'},
 {'id': 'googleplus', 'title': 'Google+', 
    'url': 'https://plus.google.com/%s'},
 {'id': 'slideshare', 'title': 'Slideshare', 
    'url': 'https://www.slideshare.net/%s'},
 {'id': 'soundcloud', 'title': 'SoundCloud', 
    'url': 'https://soundcloud.com/%s'},
 {'id': 'rss', 'title': 'RSS', 
    'url': '%s'},
 {'id': 'instagram', 'title': 'Instagram', 
    'url': 'https://www.instagram.com/%s'},
 {'id': 'tumblr', 'title': 'Thumblr', 
    'url': 'https://%s.tumblr.com'}]
TINYMCE_JSON_FORMATS = {'strikethrough': {'inline': 'span', 'classes': 'strikethrough', 
                     'exact': 'true'}, 
   'underline': {'inline': 'span', 'classes': 'underline', 
                 'exact': 'true'}}