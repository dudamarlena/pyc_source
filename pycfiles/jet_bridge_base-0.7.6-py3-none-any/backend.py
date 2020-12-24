# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/utils/backend.py
# Compiled at: 2019-10-07 13:58:39
from datetime import datetime, tzinfo, timedelta
import logging, requests
from jet_bridge_base import settings, VERSION
from jet_bridge_base.models.token import Token
try:
    from datetime import timezone
    utc = timezone.utc
except ImportError:

    class UTC(tzinfo):

        def utcoffset(self, dt):
            return timedelta(0)

        def tzname(self, dt):
            return 'UTC'

        def dst(self, dt):
            return timedelta(0)


    utc = UTC()

def api_method_url(method):
    return ('{}/{}').format(settings.API_BASE_URL, method)


def get_token(session):
    token = session.query(Token).first()
    if token:
        return token.token
    else:
        return


def register_token(session):
    token = session.query(Token).first()
    if token:
        return (token, False)
    else:
        url = api_method_url('project_tokens/')
        headers = {'User-Agent': 'Jet Django'}
        data = {'bridge_type': 'jet_bridge', 
           'bridge_version': VERSION}
        r = requests.request('POST', url, headers=headers, data=data)
        success = 200 <= r.status_code < 300
        if not success:
            logging.error('Register Token request error', r.status_code, r.reason)
            return (
             None, False)
        result = r.json()
        token = result['token'].replace('-', '')
        date_add = datetime.strptime(result['date_add'][:-6], '%Y-%m-%dT%H:%M:%S.%f')
        token = Token(token=token, date_add=date_add)
        session.add(token)
        session.commit()
        return (
         token, True)


def is_token_activated(session):
    token = session.query(Token).first()
    if not token:
        return False
    url = api_method_url(('project_tokens/{}/').format(token.token))
    headers = {'User-Agent': 'Jet Django'}
    r = requests.request('GET', url, headers=headers)
    success = 200 <= r.status_code < 300
    if not success:
        return False
    result = r.json()
    return bool(result.get('activated'))


def reset_token(session):
    session.query(Token).delete()
    session.commit()
    return register_token(session)


def set_token(session, token):
    project_token = session.query(Token).first()
    token_clean = str(token).replace('-', '')
    now = datetime.now().replace(tzinfo=utc)
    if project_token:
        if project_token.token == token_clean:
            logging.info('This token is already set, ignoring')
            return
        project_token.token = token_clean
        project_token.date_add = now
        session.commit()
        logging.info(('Token changed to {}').format(project_token.token))
    else:
        project_token = Token(token=token_clean, date_add=now)
        session.add(project_token)
        session.commit()
        logging.info(('Token created {}').format(project_token.token))


def project_auth(session, token, permission=None):
    project_token = session.query(Token).first()
    if not project_token:
        return {'result': False}
    url = api_method_url('project_auth/')
    data = {'project_token': project_token.token, 
       'token': token}
    headers = {'User-Agent': 'Jet Django'}
    if permission:
        data.update(permission)
    r = requests.request('POST', url, data=data, headers=headers)
    success = 200 <= r.status_code < 300
    if not success:
        logging.error('Project Auth request error', r.status_code, r.reason)
        return {'result': False}
    result = r.json()
    if result.get('access_disabled'):
        return {'result': False, 
           'warning': result.get('warning')}
    return {'result': True, 
       'warning': result.get('warning')}