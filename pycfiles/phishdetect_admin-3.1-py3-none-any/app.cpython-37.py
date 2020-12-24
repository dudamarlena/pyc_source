# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-admin/phishdetectadmin/app.py
# Compiled at: 2020-02-14 05:35:34
# Size of source mod 2**32: 13758 bytes
import io, datetime, phishdetect
from flask import Flask, render_template, request, redirect, url_for, send_file
from .config import load_config, save_config, load_archived_events, archive_event
from .utils import get_indicator_type, clean_indicator, extract_domain, send_email
from . import session
app = Flask(__name__)

@app.route('/conf/', methods=['GET'])
def conf():
    return render_template('conf.html', page='Configuration', config=(load_config()))


@app.route('/conf/node/', methods=['POST'])
def conf_node():
    host = request.form.get('host')
    key = request.form.get('key')
    if host == '' or key == '':
        return redirect(url_for('conf'))
    config = load_config()
    if not config:
        config = {'nodes': []}
    config['nodes'].append({'host':host.rstrip('/'), 
     'key':key})
    save_config(config)
    return redirect(url_for('index'))


@app.route('/conf/smtp/', methods=['POST'])
def conf_smtp():
    smtp_host = request.form.get('smtp_host')
    smtp_user = request.form.get('smtp_user')
    smtp_pass = request.form.get('smtp_pass')
    if smtp_host == '' or smtp_user == '' or smtp_pass == '':
        return redirect(url_for('conf'))
    config = load_config()
    if not config:
        config = {'node': []}
    config['smtp_host'] = smtp_host
    config['smtp_user'] = smtp_user
    config['smtp_pass'] = smtp_pass
    save_config(config)
    return redirect(url_for('conf'))


@app.route('/node/', methods=['GET', 'POST'])
def node():
    config = load_config()
    if request.method == 'GET':
        if not config:
            return redirect(url_for('conf'))
        nodes = config['nodes']
        return render_template('node.html', page='Node Selection', nodes=nodes)
    if request.method == 'POST':
        host = request.form.get('host')
        key = ''
        for node in config['nodes']:
            if node['host'] == host:
                key = node['key']
                break

        session.__node__ = {'host':host,  'key':key}
        return redirect(url_for('index'))


@app.route('/')
def index():
    if not session.__node__:
        return redirect(url_for('node'))
    return redirect(url_for('events'))


@app.route('/events/archive')
def events_archive():
    if not session.__node__:
        return redirect(url_for('node'))
    else:
        uuid = request.args.get('uuid', None)
        return uuid or redirect(url_for('events'))
    archive_event(uuid)
    return redirect(url_for('events'))


@app.route('/events/')
def events():
    if not session.__node__:
        return redirect(url_for('node'))
    try:
        pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
        results = pd.events.fetch()
    except Exception as e:
        try:
            return render_template('error.html', msg=('The connection to the PhishDetect Node failed: {}'.format(e)))
        finally:
            e = None
            del e

    if results:
        if 'error' in results:
            return render_template('error.html', msg=('Unable to fetch events: {}'.format(results['error'])))
    archived = request.args.get('archived', None)
    archived_events = load_archived_events()
    final = []
    for result in results:
        patterns = ['%Y-%m-%dT%H:%M:%S.%f%z',
         '%Y-%m-%dT%H:%M:%S.%f%Z',
         '%Y-%m-%dT%H:%M:%S.%fZ']
        date = None
        for pattern in patterns:
            try:
                date = datetime.datetime.strptime(result['datetime'], pattern)
            except ValueError:
                continue
            else:
                break

        if date:
            result['datetime'] = date.strftime('%Y-%m-%d %H:%M:%S %Z')
        if archived:
            if result['uuid'] in archived_events:
                final.append(result)
            elif result['uuid'] not in archived_events:
                final.append(result)

    return render_template('events.html', node=(session.__node__['host']),
      page='Events',
      events=final,
      archived=archived)


@app.route('/indicators/', methods=['GET', 'POST'])
def indicators():
    if not session.__node__:
        return redirect(url_for('node'))
    else:
        if request.method == 'GET':
            ioc = request.args.get('ioc', None)
            if ioc:
                ioc = extract_domain(ioc)
            return render_template('indicators.html', indicators=ioc, page='Indicators')
            if request.method == 'POST':
                indicators_string = request.form.get('indicators', '')
                tags_string = request.form.get('tags', '')
                indicators_string = indicators_string.strip()
                tags_string = tags_string.strip()
                if indicators_string == '':
                    return render_template('indicators.html', page='Indicators',
                      error="You didn't provide a valid list of indicators")
                if tags_string == '':
                    tags = []
        else:
            tags = [t.lower().strip() for t in tags_string.split(',')]
        domain_indicators = []
        email_indicators = []
        for indicator in indicators_string.split():
            indicator_clean = clean_indicator(indicator)
            if get_indicator_type(indicator_clean) == 'email':
                email_indicators.append(indicator_clean)
            elif get_indicator_type(indicator_clean) == 'domain':
                domain_indicators.append(indicator_clean)

        domain_results = {}
        email_results = {}
        total = 0
        try:
            pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
            if domain_indicators:
                domain_results = pd.indicators.add(domain_indicators, 'domain', tags)
                total += domain_results['counter']
            if email_indicators:
                email_results = pd.indicators.add(email_indicators, 'email', tags)
                total += email_results['counter']
        except Exception as e:
            try:
                return render_template('error.html', msg=('The connection to the PhishDetect Node failed: {}'.format(e)))
            finally:
                e = None
                del e

        if 'error' in domain_results or 'error' in email_results:
            return render_template('indicators.html', page='Indicators',
              error=(results['error']),
              tags=tags_string,
              indicators=indicators_string)
        msg = 'Added {} new indicators successfully!'.format(total)
        return render_template('success.html', msg=msg)


@app.route('/indicators/<string:sha256>/', methods=['GET'])
def indicator(sha256):
    if not session.__node__:
        return redirect(url_for('node'))
    pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
    details = pd.indicators.details(sha256)
    return render_template('indicator.html', node=(session.__node__['host']),
      page='Indicator Details',
      details=details)


@app.route('/reports/', methods=['GET'])
def reports():
    if not session.__node__:
        return redirect(url_for('node'))
    pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
    results = pd.reports.fetch()
    if 'error' in results:
        return render_template('error.html', msg=('Unable to fetch reports: {}'.format(results['error'])))
    return render_template('reports.html', node=(session.__node__['host']),
      page='Reports',
      messages=results)


@app.route('/reports/<string:uuid>/', methods=['GET'])
def report(uuid):
    if not session.__node__:
        return redirect(url_for('node'))
    pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
    results = pd.reports.details(uuid=uuid)
    if 'error' in results:
        return render_template('error.html', msg=('Unable to fetch report details: {}'.format(results['error'])))
    return render_template('report.html', node=(session.__node__['host']),
      page='Report',
      message=results)


@app.route('/download/<string:uuid>/', methods=['GET'])
def report_download(uuid):
    if not session.__node__:
        return redirect(url_for('node'))
        pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
        results = pd.reports.details(uuid=uuid)
        if 'error' in results:
            return render_template('error.html', msg=('Unable to fetch report details: {}'.format(results['error'])))
        content = results['content']
        if content.strip() == '':
            return render_template('error.html', msg='The fetched message seems empty')
        mem = io.BytesIO()
        mem.write(content.encode('utf-8'))
        mem.seek(0)
        if results['type'] == 'email':
            mimetype = 'message/rfc822'
            filename = '{}.eml'.format(results['uuid'])
    else:
        mimetype = 'text/plain'
        filename = '{}.txt'.format(results['uuid'])
    return send_file(mem, mimetype=mimetype,
      as_attachment=True,
      attachment_filename=filename)


@app.route('/users/', methods=['GET'])
def users_pending():
    if not session.__node__:
        return redirect(url_for('node'))
    pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
    results = pd.users.get_pending()
    if 'error' in results:
        return render_template('error.html', msg=('Unable to fetch pending users: {}'.format(results['error'])))
    return render_template('users_pending.html', node=(session.__node__['host']),
      page='Users',
      users=results)


@app.route('/users/active/', methods=['GET'])
def users_active():
    if not session.__node__:
        return redirect(url_for('node'))
    pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
    results = pd.users.get_active()
    if 'error' in results:
        return render_template('error.html', msg=('Unable to fetch users: {}'.format(results['error'])))
    return render_template('users_active.html', node=(session.__node__['host']),
      page='Users',
      users=results)


@app.route('/users/activate/<string:api_key>/', methods=['GET'])
def users_activate(api_key):
    if not session.__node__:
        return redirect(url_for('node'))
        pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
        results = pd.users.get_pending()
        if 'error' in results:
            return render_template('error.html', msg=('Unable to fetch pending users: {}'.format(users['error'])))
        result = pd.users.activate(api_key)
        if 'error' in result:
            return render_template('error.html', msg=('Unable to activate user: {}'.format(result['error'])))
        email = None
        for user in results:
            if api_key == user['key']:
                email = user['email']
                break

        if not email:
            return render_template('error.html', msg='User not found')
    else:
        message = 'Your PhishDetect secret token has been activated!'
        try:
            send_email(email, 'Your PhishDetect secret token has been activated', message)
        except Exception as e:
            try:
                return render_template('error.html', msg=('Failed to send email to user: {}'.format(e)))
            finally:
                e = None
                del e

    return render_template('success.html', msg='The user has been activated successfully')


@app.route('/users/deactivate/<string:api_key>/', methods=['GET'])
def users_deactivate(api_key):
    if not session.__node__:
        return redirect(url_for('node'))
        pd = phishdetect.PhishDetect(host=(session.__node__['host']), api_key=(session.__node__['key']))
        results = pd.users.get_active()
        if 'error' in results:
            return render_template('error.html', msg=('Unable to fetch pending users: {}'.format(users['error'])))
        result = pd.users.deactivate(api_key)
        if 'error' in result:
            return render_template('error.html', msg=('Unable to deactivate user: {}'.format(result['error'])))
        email = None
        for user in results:
            if api_key == user['key']:
                email = user['email']
                break

        if not email:
            return render_template('error.html', msg='User not found')
    else:
        message = 'Your PhishDetect secret token has been deactivated!\nIf you have any questions, please contact your PhishDetect Node administrator.'
        try:
            send_email(email, 'Your PhishDetect secret token has been deactivated', message)
        except Exception as e:
            try:
                return render_template('error.html', msg=('Failed to send email to user: {}'.format(e)))
            finally:
                e = None
                del e

    return render_template('success.html', msg='The user has been deactivated successfully')