# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/folen/Documents/Aptana Studio 3 Workspace/django_facebook_helper/django_facebook_helper/templatetags/django_facebook_helper_tags.py
# Compiled at: 2013-05-17 06:43:51
from django import template
import urllib
from django.core.urlresolvers import reverse
register = template.Library()
from django.conf import settings

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            v.decode('utf8')
        out_dict[k] = v

    return out_dict


@register.simple_tag(takes_context=True)
def facebook_feed_url(context, friend, link, picture, name, caption, description, action_name, action_link, redirect_uri):
    """
        Direct URL Example
        
        You can also bring up a Feed Dialog by explicitly directing people to the /dialog/feed endpoint:
        
        https://www.facebook.com/dialog/feed?
          app_id=458358780877780&
          link=https://developers.facebook.com/docs/reference/dialogs/&
          picture=http://fbrell.com/f8.jpg&
          name=Facebook%20Dialogs&
          caption=Reference%20Documentation&
          description=Using%20Dialogs%20to%20interact%20with%20users.&
          redirect_uri=https://mighty-lowlands-6381.herokuapp.com/
        
        Click here to try the url yourself. The user will see a dialog that looks like the following:
        
        If a person clicks "Share", the browser will redirect to
        
        https://mighty-lowlands-6381.herokuapp.com/?post_id=12345
        
        The published story will look like this:
        
        If the user clicks "Cancel", the browser will redirect to
        
        https://mighty-lowlands-6381.herokuapp.com/
    """
    facebook_app_id = settings.FACEBOOK_APP_ID
    param_dict = {'app_id': facebook_app_id, 
       'link': link, 
       'picture': picture, 
       'name': name, 
       'caption': caption, 
       'description': description, 
       'redirect_uri': redirect_uri, 
       'to': friend, 
       'display': 'popup'}
    if action_name != '' and action_link != '':
        param_dict['actions'] = "[{name:'%s',link:'%s'}]" % (action_name, action_link)
    params = urllib.urlencode(encoded_dict(param_dict))
    return 'https://www.facebook.com/dialog/feed?%s' % params


@register.simple_tag(takes_context=True)
def facebook_request_app_install(context, redirect_uri):
    """
        Este tag genera el enlace para recomendar la app a un amigo 
        
        Direct URL Example
        
        This example uses the the raw URL to render a Request Dialog for your app.
        One key difference from using this method over the JavaScript SDK is the 
        requirement of the redirect_uri parameter.
        
        https://www.facebook.com/dialog/apprequests?
          app_id=APP_ID&
          message=Facebook%20Dialogs%20are%20so%20easy!&
          redirect_uri=http://www.example.com/response
        
        After the user follows the flow and sends the request the browser will redirect to
        
        http://example.com/response?request=REQUEST_ID&to=ARRAY_OF_USER_IDS
        
        If there are errors, the browser will redirect to
        
        http://example.com/response?error_code=ERROR_CODE&error_msg=ERROR_MSG
    """
    facebook_app_id = settings.FACEBOOK_APP_ID
    facebook_app_message = settings.FACEBOOK_APP_INSTALL_MESSAGE
    params = urllib.urlencode(encoded_dict({'app_id': facebook_app_id, 
       'message': facebook_app_message, 
       'redirect_uri': redirect_uri}))
    return 'https://www.facebook.com/dialog/apprequests?%s' % params