# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/generic/templatetags/disqus_tags.py
# Compiled at: 2016-05-20 23:42:06
from __future__ import unicode_literals
import base64, hashlib, hmac, json, time
from future.builtins import bytes, int
from wenlincms import template
register = template.Library()

@register.simple_tag
def disqus_id_for(obj):
    """
    Returns a unique identifier for the object to be used in
    DISQUS JavaScript.
    """
    return b'%s-%s' % (obj._meta.object_name, obj.id)


@register.inclusion_tag(b'generic/includes/disqus_sso.html', takes_context=True)
def disqus_sso_script(context):
    """
    Provides a generic context variable which adds single-sign-on
    support to DISQUS if ``COMMENTS_DISQUS_API_PUBLIC_KEY`` and
    ``COMMENTS_DISQUS_API_SECRET_KEY`` are specified.
    """
    settings = context[b'settings']
    public_key = getattr(settings, b'COMMENTS_DISQUS_API_PUBLIC_KEY', b'')
    secret_key = getattr(settings, b'COMMENTS_DISQUS_API_SECRET_KEY', b'')
    user = context[b'request'].user
    if public_key and secret_key and user.is_authenticated():
        context[b'public_key'] = public_key
        context[b'sso_data'] = _get_disqus_sso(user, public_key, secret_key)
    return context


def _get_disqus_sso(user, public_key, secret_key):
    data = json.dumps({b'id': b'%s' % user.id, 
       b'username': user.username, 
       b'email': user.email})
    message = base64.b64encode(bytes(data, encoding=b'utf8'))
    timestamp = int(time.time())
    sig = hmac.HMAC(bytes(secret_key, encoding=b'utf8'), bytes(b'%s %s' % (message, timestamp), encoding=b'utf8'), hashlib.sha1).hexdigest()
    return b'%s %s %s' % (message, sig, timestamp)