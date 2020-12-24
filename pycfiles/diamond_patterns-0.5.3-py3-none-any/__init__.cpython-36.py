# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./diamond_patterns/__init__.py
# Compiled at: 2019-07-27 09:03:29
# Size of source mod 2**32: 3395 bytes
import os, glob, json, arrow, requests
master_config = {'manifest_file':'~/.diamond-patterns-manifest.json', 
 'docs_html_url':'https://diamond-patterns.readthedocs.io/en/latest/patterns', 
 'docs_rst_url':'https://raw.githubusercontent.com/iandennismiller/diamond-patterns/master/docs/patterns', 
 'manifest_url':'https://raw.githubusercontent.com/iandennismiller/diamond-patterns/master/patterns/manifest.json', 
 'archive_url':'https://github.com/iandennismiller/diamond-patterns/archive/master.zip#diamond-patterns-master/patterns'}

class Pattern:

    def __init__(self):
        self.config_file = '~/.diamond-patterns.json'
        self.config_file = os.path.expanduser(self.config_file)
        self.ensure_config()
        with open(self.config_file, 'r') as (f):
            self.config = json.load(f)
        self.config['manifest_file'] = os.path.expanduser(self.config['manifest_file'])
        self.ensure_manifest()
        with open(self.config['manifest_file'], 'r') as (f):
            self.manifest = json.load(f)
        self.patterns = self.manifest['patterns']

    def ensure_config(self):
        if not os.path.isfile(self.config_file):
            print('WARNING: {} not found'.format(self.config_file))
            with open(self.config_file, 'w') as (f):
                f.write(json.dumps(master_config, indent=2, sort_keys=True))

    def open_docs(self, pattern, web):
        if pattern not in self.patterns:
            print('unrecognized pattern: {0}'.format(pattern))
            return
        html_url = '{}/{}.html'.format(self.config['docs_html_url'], pattern)
        rst_url = '{}/{}.rst'.format(self.config['docs_rst_url'], pattern)
        print('URL: {}\n'.format(html_url))
        if web:
            try:
                os.system("open '{}'".format(html_url))
            except:
                print("WARNING: could not open browser with 'open'")

        else:
            r = requests.get(rst_url)
        if r.status_code == 200:
            print(r.text)

    def run_scaffold(self, pattern, interactive=True):
        if pattern not in self.patterns:
            print('unrecognized pattern: {0}'.format(pattern))
            return
        else:
            pattern_url = '{}/{}'.format(self.config['archive_url'], pattern)
            if interactive:
                cmd = 'mrbob -w -O . {}'.format(pattern_url)
            else:
                cmd = 'mrbob -w -n -O . {}'.format(pattern_url)
        os.system(cmd)

    def download_manifest(self):
        r = requests.get(self.config['manifest_url'])
        if r.status_code == 200:
            with open(self.config['manifest_file'], 'w') as (f):
                f.write(r.text)
        else:
            print('ERROR: failed to download {}'.format(self.config['manifest_url']))

    def ensure_manifest(self):
        if not os.path.isfile(self.config['manifest_file']):
            print('WARNING: {} not found'.format(self.config['manifest_file']))
            self.download_manifest()

    def write_manifest(self):
        h = {'timestamp':arrow.utcnow().timestamp, 
         'patterns':[f.split('/')[1] for f in glob.glob('patterns/*/')]}
        with open('patterns/manifest.json', 'w') as (f):
            f.write(json.dumps(h, indent=2, sort_keys=True))