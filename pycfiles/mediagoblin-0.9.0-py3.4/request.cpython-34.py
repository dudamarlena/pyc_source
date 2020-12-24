# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/request.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 2460 bytes
import json, logging, six
from werkzeug.http import parse_options_header
from mediagoblin.db.models import User, AccessToken
from mediagoblin.oauth.tools.request import decode_authorization_header
_log = logging.getLogger(__name__)
form_encoded = 'application/x-www-form-urlencoded'
json_encoded = 'application/json'

def setup_user_in_request(request):
    """
    Examine a request and tack on a request.user parameter if that's
    appropriate.
    """
    authorization = decode_authorization_header(request.headers)
    if authorization.get('access_token'):
        token = authorization['oauth_token']
        token = AccessToken.query.filter_by(token=token).first()
        if token is not None:
            request.user = token.user
            return
    if 'user_id' not in request.session:
        request.user = None
        return
    request.user = User.query.get(request.session['user_id'])
    if not request.user:
        _log.warn('Killing session for user id %r', request.session['user_id'])
        request.session.delete()


def decode_request(request):
    """ Decodes a request based on MIME-Type """
    data = request.data
    content_type, _ = parse_options_header(request.content_type)
    if content_type == json_encoded:
        data = json.loads(six.text_type(data, 'utf-8'))
    else:
        if content_type == form_encoded or content_type == '':
            data = request.form
        else:
            data = ''
    return data