# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/cli/ftmap/cmd_submit.py
# Compiled at: 2018-10-15 19:16:31
# Size of source mod 2**32: 2116 bytes
import logging, click, requests, json
from sblu import CONFIG
from sblu.cli import make_sig
logger = logging.getLogger(__name__)
URL_SCHEME = 'http'
API_ENDPOINT = '/api.php'
CP_CONFIG = CONFIG['ftmap']
FORM_KEYS = [
 'username', 'prot', 'protpdb', 'jobname', 'protchains', 'keep_metals']

@click.command('submit', short_help='Submit a job to FTMap.')
@click.option('--username', default=(CP_CONFIG['username']))
@click.option('--secret', default=(CP_CONFIG['api_secret']))
@click.option('--server', default=(CP_CONFIG['server']))
@click.option('-j', '--jobname')
@click.option('-k', '--keep_metals', is_flag=True, default=False)
@click.option('--prot', type=click.Path(exists=True))
@click.option('--protpdb')
@click.option('--protchains')
def cli(username, secret, server, jobname, keep_metals, prot, protpdb, protchains):
    if username is None or username == 'None' or secret is None or secret == 'None':
        if username is None or username == 'None':
            username = click.prompt('Please enter your ftmap username')
            CP_CONFIG['username'] = username
        if secret is None or secret == 'None':
            secret = click.prompt('Please enter your ftmap api secret')
            CP_CONFIG['api_secret'] = secret
        CONFIG.write()
    elif prot is None:
        if protpdb is None:
            raise click.BadOptionUsage('One of --prot or --protpdb is required')
    else:
        form = {k:v for k, v in locals().items() if k in FORM_KEYS if v is not None if v is not None}
        files = {}
        if form.get('prot') is not None:
            files['prot'] = open(form['prot'], 'rb')
            form['useprotpdbid'] = '0'
        form['sig'] = make_sig(form, secret)
        api_address = '{0}://{1}{2}'.format(URL_SCHEME, server, API_ENDPOINT)
        try:
            r = requests.post(api_address, data=form, files=files)
            result = json.loads(r.text)
            if result['status'] == 'success':
                print(result['id'])
            else:
                print(result['errors'])
                click.exit(1)
        except Exception as e:
            logger.error('Error submitting job: {}'.format(e))