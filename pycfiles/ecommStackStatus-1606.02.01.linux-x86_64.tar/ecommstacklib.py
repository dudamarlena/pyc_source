# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ecommstackstatus/ecommstacklib.py
# Compiled at: 2016-06-02 16:49:34
"""
Magento is a trademark of Varien. Neither I nor these scripts are affiliated with or endorsed by the Magento Project or its trademark owners.

"""
STACK_LIB_VERSION = 2016051601
import re, glob, subprocess, sys, os, fnmatch
try:
    import xml.etree.ElementTree as ET
except ImportError:
    import cElementTree as ET

import pprint, socket, collections
try:
    import json
    JSON = True
except ImportError:
    JSON = False

try:
    import argparse
    ARGPARSE = True
except ImportError:
    ARGPARSE = False
    sys.stderr.write('This program is more robust if python argparse installed.\n')

try:
    import mysql.connector
    MYSQL = True
except ImportError:
    MYSQL = False

class argsAlt(object):
    pass


class apacheCtl(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if 'exe' not in self.kwargs:
            self.kwargs['exe'] = 'httpd'

    def figlet(self):
        print "\n    _                     _          \n   / \\   _ __   __ _  ___| |__   ___ \n  / _ \\ | '_ \\ / _` |/ __| '_ \\ / _ \\\n / ___ \\| |_) | (_| | (__| | | |  __/\n/_/   \\_\\ .__/ \\__,_|\\___|_| |_|\\___|\n        |_|         \n"

    def get_version(self):
        """
        Discovers installed apache version
        """
        version = self.kwargs['exe'] + ' -v'
        p = subprocess.Popen(version, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if p.returncode > 0:
            return ()
        else:
            return output

    def get_conf_parameters(self):
        conf = self.kwargs['exe'] + ' -V 2>&1'
        p = subprocess.Popen(conf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if p.returncode > 0:
            return ()
        dict = {}
        compiled = 0
        for i in output.splitlines():
            if i.strip() == 'Server compiled with....':
                compiled = 1
                continue
            if compiled == 0:
                result = re.match('\\s*([^:]+):\\s*(.+)', i.strip())
                if result:
                    dict[result.group(1)] = result.group(2)
            else:
                result = re.match('\\s*-D\\s*([^=]+)=?"?([^"\\s]*)"?', i.strip())
                if result:
                    dict[result.group(1)] = result.group(2)

        return dict

    def get_root(self):
        try:
            return self.get_conf_parameters()['HTTPD_ROOT']
        except KeyError:
            sys.exit(1)

    def get_conf(self):
        """
        :returns: configuration path location
        HTTPD_ROOT/SERVER_CONFIG_FILE
        """
        try:
            return os.path.join(self.get_conf_parameters()['HTTPD_ROOT'], self.get_conf_parameters()['SERVER_CONFIG_FILE'])
        except KeyError:
            sys.exit(1)

    def get_mpm(self):
        try:
            return self.get_conf_parameters()['Server MPM']
        except KeyError:
            sys.exit(1)

    def parse_config(self, wholeconfig):
        """
        list structure
        { line : { listen: [ ], server_name : [ ], root : path } }
    
        <VirtualHost *:80>
        DocumentRoot /var/www/vhosts/example.com/httpdocs
        ServerName example.com
        ServerAlias www.example.com
        <Directory /var/www/vhosts/example.com/httpdocs>
        </Directory>
        CustomLog /var/log/httpd/example.com-access_log combined
        ErrorLog /var/log/httpd/example.com-error_log
        </VirtualHost>
        <VirtualHost _default_:443>
        ErrorLog logs/ssl_error_log
        TransferLog logs/ssl_access_log
        LogLevel warn
        SSLEngine on
        SSLProtocol all -SSLv2 -SSLv3 -TLSv1
        SSLCipherSuite DEFAULT:!EXP:!SSLv2:!DES:!IDEA:!SEED:+3DES
        SSLCertificateFile /etc/pki/tls/certs/localhost.crt
        SSLCertificateKeyFile /etc/pki/tls/private/localhost.key
        </VirtualHost>
        """
        stanza_chain = []
        stanza_count = 0
        vhost_start = -1
        location_start = 0
        linenum = 0
        filechain = []
        stanza_flags = []
        stanzas = {}
        base_keywords = ['serverroot', 'startservers', 'minspareservers', 'maxspareservers', 'maxclients', 'maxrequestsperchild', 'listen']
        vhost_keywords = ['documentroot', 'servername', 'serveralias', 'customlog', 'errorlog', 'transferlog', 'loglevel', 'sslengine', 'sslprotocol', 'sslciphersuite', 'sslcertificatefile', 'sslcertificatekeyfile', 'sslcacertificatefile', 'sslcertificatechainfile']
        prefork_keywords = ['startservers', 'minspareservers', 'maxspareservers', 'maxclients', 'maxrequestsperchild', 'listen', 'serverlimit']
        worker_keywords = ['startservers', 'maxclients', 'minsparethreads', 'maxsparethreads', 'threadsperchild', 'maxrequestsperchild']
        event_keywords = ['startservers', 'minspareservers', 'maxspareservers', 'serverlimit', 'threadsperchild', 'maxrequestworkers', 'maxconnectionsperchild', 'minsparethreads', 'maxsparethreads']
        lines = iter(wholeconfig.splitlines())
        for line in lines:
            linenum += 1
            linecomp = line.strip().lower()
            while linecomp.endswith('\\'):
                linecomp = linecomp.strip('\\').strip()
                line = lines.next()
                linenum += 1
                linecomp += ' '
                linecomp += line.strip().lower()

            filechange = re.match('## START (.*)', line)
            if filechange:
                filechain.append(filechange.group(1))
                if vhost_start == -1:
                    if 'config_file' not in stanzas:
                        stanzas['config_file'] = []
                    stanzas['config_file'].append(filechange.group(1))
                continue
            filechange = re.match('## END (.*)', line)
            if filechange:
                filechain.pop()
                continue
            result = re.match('<[^/]\\s*(\\S+)', linecomp)
            if result:
                stanza_count += 1
                stanza_chain.append({'linenum': linenum, 'title': result.group(1)})
            result = re.match('</', linecomp)
            if result:
                stanza_count -= 1
                stanza_chain.pop()
            if stanza_count == 0:
                keywords = base_keywords + vhost_keywords
                if 'config' not in stanzas:
                    stanzas['config'] = {}
                update(stanzas['config'], kwsearch(keywords, linecomp))
            result = re.match('<ifmodule\\s+prefork.c', linecomp, re.IGNORECASE)
            if result:
                stanza_flags.append({'type': 'prefork', 'linenum': linenum, 'stanza_count': stanza_count})
                continue
            result = re.match('</ifmodule>', linecomp, re.IGNORECASE)
            if result:
                if len(stanza_flags) > 0:
                    if stanza_flags[(-1)]['type'] == 'prefork' and stanza_flags[(-1)]['stanza_count'] == stanza_count + 1:
                        stanza_flags.pop()
                        continue
            if len(stanza_flags) > 0:
                if stanza_flags[(-1)]['type'] == 'prefork' and stanza_flags[(-1)]['stanza_count'] == stanza_count:
                    if 'prefork' not in stanzas:
                        stanzas['prefork'] = {}
                    update(stanzas['prefork'], kwsearch(prefork_keywords, line, single_value=True))
                    continue
            result = re.match('<ifmodule\\s+worker.c', linecomp, re.IGNORECASE)
            if result:
                stanza_flags.append({'type': 'worker', 'linenum': linenum, 'stanza_count': stanza_count})
            result = re.match('</ifmodule>', linecomp, re.IGNORECASE)
            if result:
                if len(stanza_flags) > 0:
                    if stanza_flags[(-1)]['type'] == 'worker' and stanza_flags[(-1)]['stanza_count'] == stanza_count + 1:
                        stanza_flags.pop()
            if len(stanza_flags) > 0:
                if stanza_flags[(-1)]['type'] == 'worker' and stanza_flags[(-1)]['stanza_count'] == stanza_count:
                    if 'worker' not in stanzas:
                        stanzas['worker'] = {}
                    update(stanzas['worker'], kwsearch(worker_keywords, linecomp, single_value=True))
                    continue
            result = re.match('<ifmodule\\s+mpm_event', linecomp, re.IGNORECASE)
            if result:
                stanza_flags.append({'type': 'event', 'linenum': linenum, 'stanza_count': stanza_count})
            result = re.match('</ifmodule>', linecomp, re.IGNORECASE)
            if result:
                if len(stanza_flags) > 0:
                    if stanza_flags[(-1)]['type'] == 'event' and stanza_flags[(-1)]['stanza_count'] == stanza_count + 1:
                        stanza_flags.pop()
            if len(stanza_flags) > 0:
                if stanza_flags[(-1)]['type'] == 'event' and stanza_flags[(-1)]['stanza_count'] == stanza_count:
                    if 'event' not in stanzas:
                        stanzas['event'] = {}
                    update(stanzas['event'], kwsearch(event_keywords, linecomp, single_value=True))
                    continue
            result = re.match('<virtualhost\\s+([^>]+)', linecomp, re.IGNORECASE)
            if result:
                server_line = str(linenum)
                vhost_start = stanza_count
                if server_line not in stanzas:
                    stanzas[server_line] = {}
                stanzas[server_line]['virtualhost'] = result.group(1)
                if 'config_file' not in stanzas[server_line]:
                    stanzas[server_line]['config_file'] = []
                if filechain[(-1)] not in stanzas[server_line]['config_file']:
                    stanzas[server_line]['config_file'].append(filechain[(-1)])
                continue
            if vhost_start == stanza_count:
                keywords = vhost_keywords
                update(stanzas[server_line], kwsearch(keywords, line.strip()))
            result = re.match('</virtualhost', linecomp, re.IGNORECASE)
            if result:
                vhost_start = -1
                continue

        configuration = {}
        configuration['sites'] = []
        for i in stanzas.keys():
            if 'documentroot' in stanzas[i] or 'servername' in stanzas[i] or 'serveralias' in stanzas[i] or 'virtualhost' in stanzas[i]:
                configuration['sites'].append({})
                if 'servername' in stanzas[i]:
                    if 'domains' not in configuration['sites'][(-1)]:
                        configuration['sites'][(-1)]['domains'] = []
                    configuration['sites'][(-1)]['domains'] += stanzas[i]['servername']
                if 'serveralias' in stanzas[i]:
                    if 'domains' not in configuration['sites'][(-1)]:
                        configuration['sites'][(-1)]['domains'] = []
                    configuration['sites'][(-1)]['domains'] += stanzas[i]['serveralias']
                if 'virtualhost' in stanzas[i]:
                    if 'listening' not in configuration['sites'][(-1)]:
                        configuration['sites'][(-1)]['listening'] = []
                    configuration['sites'][(-1)]['listening'] += [stanzas[i]['virtualhost']]
                if 'documentroot' in stanzas[i]:
                    configuration['sites'][(-1)]['doc_root'] = stanzas[i]['documentroot'][0]
                if 'config_file' in stanzas[i]:
                    configuration['sites'][(-1)]['config_file'] = stanzas[i]['config_file'][0]
                if 'customlog' in stanzas[i]:
                    configuration['sites'][(-1)]['access_log'] = stanzas[i]['customlog'][0]
                if 'errorlog' in stanzas[i]:
                    configuration['sites'][(-1)]['error_log'] = stanzas[i]['errorlog'][0]

        update(stanzas, configuration)
        if 'maxprocesses' not in stanzas:
            mpm = self.get_mpm().lower()
            if mpm == 'prefork':
                if stanzas.get('prefork', {}).get('maxclients'):
                    stanzas['maxprocesses'] = int(stanzas['prefork']['maxclients'])
            elif mpm == 'event':
                if 'event' in stanzas:
                    if stanzas.get('event', {}).get('serverlimit'):
                        event_limit_one = int(stanzas['event']['serverlimit'])
                    else:
                        event_limit_one = None
                    if stanzas.get('event', {}).get('maxrequestworkers') and stanzas.get('event', {}).get('threadsperchild'):
                        event_limit_two = int(stanzas['event']['maxrequestworkers']) / int(stanzas['event']['threadsperchild'])
                    else:
                        event_limit_two = None
                    if event_limit_one is not None and event_limit_two is not None:
                        if event_limit_one < event_limit_two:
                            stanzas['maxprocesses'] = event_limit_one
                        else:
                            stanzas['maxprocesses'] = event_limit_two
                    elif event_limit_one is not None:
                        stanzas['maxprocesses'] = event_limit_one
                    elif event_limit_two is not None:
                        stanzas['maxprocesses'] = event_limit_two
            elif mpm == 'worker':
                if 'worker' in stanzas:
                    if stanzas.get('worker', {}).get('maxclients'):
                        stanzas['maxprocesses'] = int(stanzas['worker']['maxclients'])
            else:
                sys.stderr.write('Could not identify mpm in use.\n')
                error_collection.append('apache error: Could not identify mpm in use.\n')
                sys.exit(1)
        return stanzas


class nginxCtl(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if 'exe' not in self.kwargs:
            self.kwargs['exe'] = 'nginx'

    def figlet(self):
        print "\n             _            \n _ __   __ _(_)_ __ __  __\n| '_ \\ / _` | | '_ \\\\ \\/ /\n| | | | (_| | | | | |>  < \n|_| |_|\\__, |_|_| |_/_/\\_\\\n       |___/      \n\n"

    def get_version(self):
        """
        Discovers installed nginx version
        """
        version = self.kwargs['exe'] + ' -v 2>&1'
        p = subprocess.Popen(version, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if p.returncode > 0:
            return ()
        else:
            return output

    def get_conf_parameters(self):
        """
        Finds nginx configuration parameters

        :returns: list of nginx configuration parameters
        """
        conf = self.kwargs['exe'] + " -V 2>&1 | grep 'configure arguments:'"
        p = subprocess.Popen(conf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if p.returncode > 0:
            return ()
        output = re.sub('configure arguments:', '', output)
        dict = {}
        for item in output.split(' '):
            if len(item.split('=')) == 2:
                dict[item.split('=')[0]] = item.split('=')[1]

        return dict

    def get_conf(self):
        """
        :returns: nginx configuration path location
        """
        try:
            return self.get_conf_parameters()['--conf-path']
        except KeyError:
            sys.exit(1)

    def get_bin(self):
        """
        :returns: nginx binary location
        """
        if True:
            return self.get_conf_parameters()['--sbin-path']

    def get_pid(self):
        """
        :returns: nginx pid location which is required by nginx services
        """
        if True:
            return self.get_conf_parameters()['--pid-path']

    def get_lock(self):
        """
        :returns: nginx lock file location which is required for nginx services
        """
        if True:
            return self.get_conf_parameters()['--lock-path']

    def parse_config(self, wholeconfig):
        """
        list structure
        { line : { listen: [ ], server_name : [ ], root : path } }
        """
        stanza_chain = []
        stanza_count = 0
        server_start = -1
        location_start = 0
        linenum = 0
        filechain = []
        stanzas = {}
        server_keywords = [
         'listen', 'root', 'ssl_prefer_server_ciphers', 'ssl_protocols', 'ssl_ciphers', 'access_log', 'error_log']
        server_keywords_split = ['server_name']
        for line in wholeconfig.splitlines():
            linenum += 1
            linecomp = line.strip().lower()
            filechange = re.match('## START (.*)', line)
            if filechange:
                filechain.append(filechange.group(1))
            filechange = re.match('## END (.*)', line)
            if filechange:
                filechain.pop()
            if len(re.findall('{', line)) > 0 and len(re.findall('}', line)) > 0:
                if 'error' not in stanzas:
                    stanzas['error'] = 'nginx config file: This script does not consistently support opening { and closing } stanzas on the same line.\n'
                    error_collection.append('nginx config file: This script does not consistently support opening { and closing } stanzas on the same line.\n')
                stanzas['error'] += 'line %d: %s\n' % (linenum, line.strip())
                error_collection.append('line %d: %s\n' % (linenum, line.strip()))
            stanza_count += len(re.findall('{', line))
            stanza_count -= len(re.findall('}', line))
            result = re.match('(\\S+)\\s*{', linecomp)
            if result:
                stanza_chain.append({'linenum': linenum, 'title': result.group(1)})
            if len(re.findall('}', line)) and len(stanza_chain) > 0:
                stanza_chain.pop()
            result = re.match('^\\s*server\\s', linecomp, re.IGNORECASE)
            if result:
                server_start = stanza_count
                server_line = str(linenum)
                if server_line not in stanzas:
                    stanzas[server_line] = {}
                if 'config_file' not in stanzas[server_line]:
                    stanzas[server_line]['config_file'] = []
                if filechain[(-1)] not in stanzas[server_line]['config_file']:
                    stanzas[server_line]['config_file'].append(filechain[(-1)])
            if server_start == stanza_count:
                keywords = server_keywords
                if server_line not in stanzas:
                    stanzas[server_line] = {}
                update(stanzas[server_line], kwsearch(keywords, line))
                keywords = server_keywords_split
                if server_line not in stanzas:
                    stanzas[server_line] = {}
                if 'server_name' not in stanzas[server_line]:
                    stanzas[server_line]['server_name'] = []
                if kwsearch(['server_name'], line):
                    stanzas[server_line]['server_name'] += kwsearch(['server_name'], line)['server_name'][0].split()
            elif stanza_count < server_start:
                server_start = -1
            keywords = [
             'worker_processes']
            update(stanzas, kwsearch(keywords, line))

        configuration = {}
        configuration['sites'] = []
        for i in stanzas.keys():
            if type(stanzas[i]) is not list and type(stanzas[i]) is not dict:
                continue
            if 'root' in stanzas[i] or 'server_name' in stanzas[i] or 'listen' in stanzas[i]:
                configuration['sites'].append({})
                if 'server_name' in stanzas[i]:
                    if 'domains' not in configuration['sites'][(-1)]:
                        configuration['sites'][(-1)]['domains'] = []
                    configuration['sites'][(-1)]['domains'] += stanzas[i]['server_name']
                if 'listen' in stanzas[i]:
                    if 'listening' not in configuration['sites'][(-1)]:
                        configuration['sites'][(-1)]['listening'] = []
                    configuration['sites'][(-1)]['listening'] += stanzas[i]['listen']
                if 'root' in stanzas[i]:
                    configuration['sites'][(-1)]['doc_root'] = stanzas[i]['root'][0]
                if 'config_file' in stanzas[i]:
                    configuration['sites'][(-1)]['config_file'] = stanzas[i]['config_file'][0]
                if 'access_log' in stanzas[i]:
                    configuration['sites'][(-1)]['access_log'] = stanzas[i]['access_log'][0]
                if 'error_log' in stanzas[i]:
                    configuration['sites'][(-1)]['error_log'] = stanzas[i]['error_log'][0]

        update(stanzas, configuration)
        if 'worker_processes' in stanzas:
            stanzas['maxprocesses'] = int(stanzas['worker_processes'][0])
        return stanzas


class phpfpmCtl(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if 'exe' not in self.kwargs:
            self.kwargs['exe'] = 'php-fpm'

    def figlet(self):
        print "\n       _                  __                 \n _ __ | |__  _ __        / _|_ __  _ __ ___  \n| '_ \\| '_ \\| '_ \\ _____| |_| '_ \\| '_ ` _ \\ \n| |_) | | | | |_) |_____|  _| |_) | | | | | |\n| .__/|_| |_| .__/      |_| | .__/|_| |_| |_|\n|_|         |_|             |_|\n"

    def get_version(self):
        """
        Discovers installed nginx version
        """
        version = self.kwargs['exe'] + ' -v'
        p = subprocess.Popen(version, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if p.returncode > 0:
            return ()
        else:
            return output

    def get_conf_parameters(self):
        conf = self.kwargs['exe'] + ' -V 2>&1'
        p = subprocess.Popen(conf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        if p.returncode > 0:
            return ()
        dict = {}
        compiled = 0
        for i in output.splitlines():
            if i.strip() == 'Server compiled with....':
                compiled = 1
                continue
            if compiled == 0:
                result = re.match('\\s*([^:]+):\\s*(.+)', i.strip())
                if result:
                    dict[result.group(1)] = result.group(2)
            else:
                result = re.match('\\s*-D\\s*([^=]+)=?"?([^"\\s]*)"?', i.strip())
                if result:
                    dict[result.group(1)] = result.group(2)

        return dict

    def get_conf(self):
        """
        :returns: configuration path location
        HTTPD_ROOT/SERVER_CONFIG_FILE
        """
        phpfpm_process = daemon_exe(['php-fpm'])
        if phpfpm_process:
            result = re.search('\\((\\S+)\\)', phpfpm_process['php-fpm']['cmd'])
            if result:
                return result.group(1)
        sys.exit(1)

    def parse_config(self, wholeconfig):
        stanza_chain = []
        linenum = 0
        filechain = []
        stanzas = {}
        server_keywords = ['listen', 'root', 'ssl_prefer_server_ciphers', 'ssl_protocols', 'ssl_cipherspm',
         'pm.max_children', 'pm.start_servers', 'pm.min_spare_servers', 'pm.max_spare_servers']
        server_keywords_split = [
         'server_name']
        for line in wholeconfig.splitlines():
            linenum += 1
            linecomp = line.strip().lower()
            filechange = re.match('## START (.*)', line)
            if filechange:
                filechain.append(filechange.group(1))
            filechange = re.match('## END (.*)', line)
            if filechange:
                filechain.pop()
            result = re.match('[;#]', linecomp)
            if result:
                continue
            result = re.match('\\[(\\S+)\\]', linecomp)
            if result:
                if len(stanza_chain) > 0:
                    stanza_chain.pop()
                stanza_chain.append({'linenum': linenum, 'title': result.group(1)})
            else:
                result = re.match('([^=\\s]+)\\s*=\\s*(\\S+)', linecomp)
                if result:
                    key = result.group(1)
                    value = result.group(2)
                    if stanza_chain[(-1)]['title'] not in stanzas:
                        stanzas[stanza_chain[(-1)]['title']] = {}
                    stanzas[stanza_chain[(-1)]['title']][key] = value

        stanzas['maxprocesses'] = 0
        for one in stanzas:
            if type(stanzas[one]) is dict:
                if stanzas.get(one, {}).get('pm.max_children'):
                    stanzas['maxprocesses'] += int(stanzas[one]['pm.max_children'])

        return stanzas


class MagentoCtl(object):

    def figlet(self):
        print "\n __  __                        _        \n|  \\/  | __ _  __ _  ___ _ __ | |_ ___  \n| |\\/| |/ _` |/ _` |/ _ \\ '_ \\| __/ _ \\ \n| |  | | (_| | (_| |  __/ | | | || (_) |\n|_|  |_|\\__,_|\\__, |\\___|_| |_|\\__\\___/ \n              |___/\n"

    def parse_version(self, mage_php_file):
        mage = {}
        file_handle = open(mage_php_file, 'r')
        for line in file_handle:
            result = re.match('static\\s+private\\s+\\$_currentEdition\\s*=\\s*self::([^\\s;]+);', line.strip(), re.IGNORECASE)
            if result:
                mage['edition'] = result.group(1)
            if 'public static function getVersionInfo()' in line:
                line = file_handle.next()
                line = file_handle.next()
                while ');' not in line:
                    line = file_handle.next()
                    result = re.match("'([^']+)'\\s*=>\\s*'([^']*)'", line.strip())
                    if result:
                        mage[result.group(1)] = result.group(2)

        file_handle.close()
        mage['version'] = ('.').join(filter(None, [
         mage.get('major'),
         mage.get('minor'),
         mage.get('revision'),
         mage.get('patch'),
         mage.get('stability'),
         mage.get('number')]))
        if 'edition' not in mage:
            mage['edition'] = ''
        return mage

    def localxml(self, local_xml_file):
        pass

    def find_mage_php(self, doc_roots):
        return_dict = {}
        for doc_root_path in doc_roots:
            mage_php_matches = []
            for root, dirnames, filenames in os.walk(doc_root_path):
                for filename in fnmatch.filter(filenames, 'Mage.php'):
                    mage_php_matches.append(os.path.join(root, filename))

            if len(mage_php_matches) > 1:
                sys.stderr.write('There are multiple Mage.php files in the Document Root %s. Choosing the shortest path.\n' % doc_root_path)
                error_collection.append('Magento error: There are multiple Mage.php files in the Document Root %s. Choosing the shortest path.\n' % doc_root_path)
                smallest_size = 0
                smallest_line = ''
                for i in mage_php_matches:
                    num_slashes = len(re.findall('/', i))
                    if smallest_size == 0:
                        smallest_size = num_slashes
                        smallest_line = i
                    elif num_slashes < smallest_size:
                        smallest_size = num_slashes
                        smallest_line = i

                mage_php_matches[0] = smallest_line
            if mage_php_matches:
                return_dict[doc_root_path] = mage_php_matches[0]

        return return_dict

    def mage_file_info(self, mage_files):
        return_dict = {}
        for doc_root_path, mage_php_match in mage_files.iteritems():
            return_dict[doc_root_path] = {}
            mage = self.parse_version(mage_php_match)
            head, tail = os.path.split(os.path.dirname(mage_php_match))
            return_dict[doc_root_path]['Mage.php'] = mage_php_match
            return_dict[doc_root_path]['magento_path'] = head
            return_dict[doc_root_path]['local_xml'] = {}
            return_dict[doc_root_path]['local_xml']['filename'] = os.path.join(head, 'app', 'etc', 'local.xml')
            return_dict[doc_root_path]['magento_version'] = '%s' % mage['version']
            if mage['edition']:
                return_dict[doc_root_path]['magento_version'] += ' %s' % mage['edition']
            return_dict[doc_root_path]['mage_version'] = mage

        return return_dict

    def open_local_xml(self, doc_root, config_node):
        """
        provide the filename (absolute or relative) of local.xml
        
        This function opens the file as an XML ElementTree
        
        returns: dict with db and cache information
        """
        filename = config_node['local_xml']['filename']
        try:
            tree = ET.ElementTree(file=filename)
        except IOError:
            sys.stderr.write('Could not open file %s\n' % filename)
            return ()

        local_xml = {}
        section = 'db'
        xml_parent_path = 'global/resources'
        xml_config_node = 'db/table_prefix'
        xml_config_section = 'default_setup/connection'
        update(local_xml, self.parse_local_xml(tree, section, xml_parent_path, xml_config_node, xml_config_section))
        section = 'session_cache'
        xml_parent_path = 'global'
        xml_config_node = 'session_save'
        xml_config_section = 'redis_session'
        xml_config_single = 'session_save_path'
        update(local_xml, self.parse_local_xml(tree, section, xml_parent_path, xml_config_node, xml_config_section, xml_config_single='session_save_path'))
        resources = tree.find('global/redis_session')
        if resources is not None or local_xml.get(section, {}).get(xml_config_node, '').lower() == 'redis' and 'tcp://' in local_xml.get(section, {}).get(xml_config_single, ''):
            local_xml[section]['engine'] = 'redis'
            redis_module_xml = os.path.join(doc_root, 'app', 'etc', 'modules', 'Cm_RedisSession.xml')
            try:
                redis_tree = ET.ElementTree(file=redis_module_xml)
                Cm_RedisSession = redis_tree.find('modules/Cm_RedisSession/active')
                if Cm_RedisSession is not None:
                    if Cm_RedisSession.text is not None:
                        local_xml[section]['Cm_RedisSession.xml active'] = Cm_RedisSession.text
                    else:
                        local_xml[section]['Cm_RedisSession.xml active'] = 'Cm_RedisSession is present but the value is empty'
                else:
                    local_xml[section]['Cm_RedisSession.xml active'] = 'Cm_RedisSession is not present'
            except IOError:
                error_collection.append('The file %s could not be opened.' % redis_module_xml)
                local_xml[section]['Cm_RedisSession.xml active'] = 'File not found'

        elif local_xml.get(section, {}).get(xml_config_node, '').lower() == 'memcache':
            local_xml[section]['engine'] = 'memcache'
        else:
            local_xml[section]['engine'] = 'unknown'
        section = 'object_cache'
        xml_parent_path = 'global/cache'
        xml_config_node = 'backend'
        xml_config_section = 'backend_options'
        update(local_xml, self.parse_local_xml(tree, section, xml_parent_path, xml_config_node, xml_config_section))
        if local_xml.get(section, {}).get(xml_config_node, '').lower() == 'mage_cache_backend_redis':
            local_xml[section]['engine'] = 'redis'
        elif local_xml.get(section, {}).get(xml_config_node, '').lower() == 'cm_cache_backend_redis':
            local_xml[section]['engine'] = 'redis'
        elif local_xml.get(section, {}).get(xml_config_node, '').lower() == 'memcached':
            xml_parent_path = 'global/cache'
            xml_config_node = 'backend'
            xml_config_section = 'memcached/servers/server'
            update(local_xml, self.parse_local_xml(tree, section, xml_parent_path, xml_config_node, xml_config_section))
            local_xml[section]['engine'] = 'memcache'
        else:
            local_xml[section]['engine'] = 'unknown'
        section = 'full_page_cache'
        xml_parent_path = 'global/full_page_cache'
        xml_config_node = 'backend'
        xml_config_section = 'backend_options'
        xml_config_single = 'slow_backend'
        update(local_xml, self.parse_local_xml(tree, section, xml_parent_path, xml_config_node, xml_config_section, xml_config_single='slow_backend'))
        if local_xml.get(section, {}).get(xml_config_node, '').lower() == 'mage_cache_backend_redis':
            local_xml[section]['engine'] = 'redis'
        elif local_xml.get(section, {}).get(xml_config_node, '').lower() == 'cm_cache_backend_redis':
            local_xml[section]['engine'] = 'redis'
        elif local_xml.get(section, {}).get(xml_config_node, '').lower() == 'memcached':
            local_xml[section]['engine'] = 'memcache'
        else:
            local_xml[section]['engine'] = 'unknown'
        return local_xml

    def parse_local_xml(self, tree, section, xml_parent_path, xml_config_node, xml_config_section, **kwargs):
        """
        provide:
            tree, ElementTree object
            section, string, name of section
            xml_parent_path, string, section of xml where information is
            xml_config_node, string, node name that describes the type
            xml_config_section, section of additional nodes and text contents
            xml_config_single, string of a single additional node under parent
    
        returns a dict with key named "section"
        """
        local_xml = {}
        if 'xml_config_single' in kwargs:
            xml_config_single = kwargs['xml_config_single']
        else:
            xml_config_single = ''
        if section not in local_xml:
            local_xml[section] = {}
        resources = tree.find(xml_parent_path)
        if resources is not None:
            i = resources.find(xml_config_node)
            if i is not None:
                if i.text is not None:
                    local_xml[section][xml_config_node] = i.text
            if resources.find(xml_config_section) is not None:
                for i in resources.find(xml_config_section):
                    local_xml[section][i.tag] = i.text

            if xml_config_single:
                if resources.find(xml_config_single) is not None:
                    i = resources.find(xml_config_single)
                    local_xml[section][i.tag] = i.text
        return local_xml

    def db_cache_table(self, doc_root, value):
        mysql = MysqlCtl()
        var_table_prefix = value.get('db/table_prefix', '')
        var_dbname = value.get('dbname', '')
        var_host = value.get('host', '')
        var_username = value.get('username', '')
        var_password = value.get('password', '')
        output = mysql.db_query(value, 'select * FROM `%s`.`%score_cache_option`;' % (var_dbname, var_table_prefix))
        return_config = {}
        if not return_config.get('cache', {}).get('cache_option_table'):
            return_config = {'cache': {'cache_option_table': ''}}
        return_config['cache']['cache_option_table'] = output
        return return_config


class RedisCtl(object):

    def figlet(self):
        print "\n              _ _     \n _ __ ___  __| (_)___ \n| '__/ _ \\/ _` | / __|\n| | |  __/ (_| | \\__ \\\n|_|  \\___|\\__,_|_|___/\n                     \n"

    def get_status(self, ip, port, **kwargs):
        if not ip or not port:
            sys.stderr.write('ERROR, one of these is none, ip: %s port: %s\n' % (ip, port))
            sys.exit(1)
        port = int(port)
        if kwargs.get('password') is not None:
            reply = socket_client(ip, port, ['AUTH %s\n' % kwargs['password'], 'INFO\n'])
        else:
            reply = socket_client(ip, port, 'INFO\n')
        if reply:
            return reply
        else:
            return
            return

    def parse_status(self, reply):
        return_dict = {}
        section = ''
        for i in reply.splitlines():
            if len(i.strip()) == 0:
                continue
            if i.lstrip()[0] == '#':
                section = i.lstrip(' #').rstrip()
                if section not in return_dict:
                    return_dict[section] = {}
                continue
            try:
                key, value = i.split(':', 2)
            except ValueError:
                key = None
                value = None

            if key and value:
                key = key.strip()
                value = value.strip()
                return_dict[section][key] = value

        return return_dict

    def get_all_statuses(self, instances, **kwargs):
        return_dict = {}
        for i in instances:
            host = instances[i]['host']
            port = instances[i]['port']
            password = instances.get(i, {}).get('password')
            if not return_dict.get(i):
                return_dict[i] = {}
            if password and host and port:
                reply = self.get_status(host, port, password=password)
            elif host and port:
                reply = self.get_status(host, port)
            else:
                reply = None
            if reply:
                return_dict[i] = self.parse_status(reply)

        return return_dict

    def instances(self, doc_roots):
        """
        With a list of doc_roots, examine the local xml we already parsed
        Make a list of redis instances, return the IP or hostname, port and password (password as applicable)
        
        Returns a dict of "host:port" : {"host": "", "port": "", "password":""}
        Value is None if it is undefined
        
        Previously, a list of "host:port" was returned.
        You could iterate for i in instances().
        The return was changed to a dict, and the key is "host:port" so for i in instances() will still work,
        With the added benefit that you can now get to the values directly.
        """
        redis_dict = {}
        for key, value in doc_roots.iteritems():
            if value.get('local_xml'):
                local_xml = value.get('local_xml', {})
            if local_xml.get('session_cache', {}).get('engine') == 'redis':
                if local_xml.get('session_cache', {}).get('host') and local_xml.get('session_cache', {}).get('port'):
                    stanza = '%s:%s' % (
                     local_xml.get('session_cache', {}).get('host'),
                     local_xml.get('session_cache', {}).get('port'))
                    redis_dict[stanza] = {}
                    redis_dict[stanza]['host'] = local_xml.get('session_cache', {}).get('host')
                    redis_dict[stanza]['port'] = local_xml.get('session_cache', {}).get('port')
                    redis_dict[stanza]['password'] = local_xml.get('session_cache', {}).get('password')
                elif 'tcp://' in local_xml.get('session_cache', {}).get('session_save_path'):
                    result = re.match('tcp://([^:]+):(\\d+)', local_xml.get('session_cache', {}).get('session_save_path'))
                    if result:
                        host = result.group(1)
                        port = result.group(2)
                        stanza = '%s:%s' % (host, port)
                        redis_dict[stanza] = {}
                        redis_dict[stanza]['host'] = host
                        redis_dict[stanza]['port'] = port
                        redis_dict[stanza]['password'] = None
            if local_xml.get('object_cache', {}).get('engine') == 'redis':
                stanza = '%s:%s' % (
                 local_xml.get('object_cache', {}).get('server'),
                 local_xml.get('object_cache', {}).get('port'))
                redis_dict[stanza] = {}
                redis_dict[stanza]['host'] = local_xml.get('object_cache', {}).get('server')
                redis_dict[stanza]['port'] = local_xml.get('object_cache', {}).get('port')
                redis_dict[stanza]['password'] = local_xml.get('object_cache', {}).get('password')
            if local_xml.get('full_page_cache', {}).get('engine') == 'redis':
                stanza = '%s:%s' % (
                 local_xml.get('full_page_cache', {}).get('server'),
                 local_xml.get('full_page_cache', {}).get('port'))
                redis_dict[stanza] = {}
                redis_dict[stanza]['host'] = local_xml.get('session_cache', {}).get('host')
                redis_dict[stanza]['port'] = local_xml.get('session_cache', {}).get('port')
                redis_dict[stanza]['password'] = local_xml.get('session_cache', {}).get('password')

        return redis_dict


class MemcacheCtl(object):

    def figlet(self):
        print "\n                                         _          \n _ __ ___   ___ _ __ ___   ___ __ _  ___| |__   ___ \n| '_ ` _ \\ / _ \\ '_ ` _ \\ / __/ _` |/ __| '_ \\ / _ \\\n| | | | | |  __/ | | | | | (_| (_| | (__| | | |  __/\n|_| |_| |_|\\___|_| |_| |_|\\___\\__,_|\\___|_| |_|\\___|\n"

    def get_status(self, ip, port):
        port = int(port)
        reply = socket_client(ip, port, 'stats\n')
        return reply

    def parse_status(self, reply):
        return_dict = {}
        section = ''
        for i in reply.splitlines():
            if len(i.strip()) == 0:
                continue
            try:
                STAT, key, value = i.split(' ', 3)
            except ValueError:
                STAT = None
                key = None
                value = None

            if key and value:
                key = key.strip()
                value = value.strip()
                return_dict[key] = value

        return return_dict

    def get_all_statuses(self, instances):
        return_dict = {}
        for instance in instances:
            ip, port = instance.split(':')
            if not return_dict.get(instance):
                return_dict[instance] = {}
            reply = self.get_status(ip, port)
            return_dict[instance] = self.parse_status(reply)

        return return_dict

    def instances(self, doc_roots):
        memcache_dict = {}
        memcache_instances = set()
        for key, doc_root_dict in doc_roots.iteritems():
            if doc_root_dict.get('local_xml', {}).get('session_cache', {}).get('engine') == 'memcache':
                result = re.match('tcp://([^:]+):(\\d+)', doc_root_dict['local_xml'].get('session_cache', {}).get('session_save_path'))
                if result:
                    host = result.group(1)
                    port = result.group(2)
                    stanza = '%s:%s' % (host, port)
                    memcache_dict[stanza] = {'host': host, 'port': port}
                    memcache_instances.add(stanza)
            if doc_root_dict.get('local_xml', {}).get('object_cache', {}).get('engine') == 'memcache':
                host = doc_root_dict.get('local_xml', {}).get('object_cache', {}).get('host')
                port = doc_root_dict.get('local_xml', {}).get('object_cache', {}).get('port')
                stanza = '%s:%s' % (host, port)
                memcache_dict[stanza] = {'host': host, 'port': port}
                memcache_instances.add(stanza)

        return list(memcache_instances)


class MysqlCtl(object):

    def figlet(self):
        print '\n __  __       ____   ___  _     \n|  \\/  |_   _/ ___| / _ \\| |    \n| |\\/| | | | \\___ \\| | | | |    \n| |  | | |_| |___) | |_| | |___ \n|_|  |_|\\__, |____/ \\__\\_\\_____|\n        |___/\n'

    def get_status(self, ip, port):
        port = int(port)
        reply = socket_client(ip, port, 'stats\n')
        return reply

    def db_query(self, dbConnInfo, sqlquery):
        output = ''
        var_table_prefix = dbConnInfo.get('db/table_prefix', '')
        var_dbname = dbConnInfo.get('dbname', '')
        var_host = dbConnInfo.get('host', '')
        var_username = dbConnInfo.get('username', '')
        var_password = dbConnInfo.get('password', '')
        if var_dbname and var_host and var_username and var_password:
            conf = "mysql --table --user='%s' --password='%s' --host='%s' --execute='%s' 2>&1 " % (
             var_username,
             var_password,
             var_host,
             sqlquery)
            p = subprocess.Popen(conf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, err = p.communicate()
            if p.returncode > 0 or not output:
                sys.stderr.write('MySQL cache table query failed\n')
                error_collection.append('MySQL cache table query failed: %s\n' % conf)
                if err:
                    sys.stderr.write('err %s\n' % err)
                    error_collection.append('err %s\n' % err)
                sys.stderr.write('command: %s\n' % conf)
                error_collection.append('command: %s\n' % conf)
        return output

    def parse_key_value(self, queried_table):
        lines = queried_table.splitlines()
        lines = input.splitlines()
        counter = 0
        for line in lines:
            return_dict = {}
            if counter < 3:
                counter += 1
                continue
            counter += 1
            result = re.search('\\|\\s*([^\\|]+)\\|\\s*([^\\|]+)', line)
            if not result:
                print 'done'
                break
            return_dict[result.group(1).strip()] = result.group(2).strip()

        return return_dict

    def not_used_instances(self, doc_roots):
        """
        With a list of doc_roots, examine the local xml we already parsed
        Make a list of mysql instances, return the "db/table_prefix", "dbname", "host", "username", "password" 
        
        Returns a dict
        Value is None if it is undefined
        
        globalconfig[
            "magento": {
                "doc_root": {
                    "/var/www/vhosts/www.example.com/html": {
                        "local_xml": {
                            "db": {
                                "dbname": "databasename", 
                                "host": "172.24.16.2", 
                                "password": "password", 
                                "username": "someuser"
                            }
                        }
                    }
                }
            }
        ]

        """
        return_dict = {}
        for doc_root in doc_roots:
            if globalconfig.get('magento', {}).get('doc_root', {}).get(doc_root, {}).get('local_xml'):
                xml_db = globalconfig.get('magento', {}).get('doc_root', {}).get(doc_root, {}).get('local_xml', {}).get('db', {})
            return_dict[xml_db['host']]['credentials'].add(xml_db)

        return return_dict


def socket_client(host, port, string, **kwargs):
    if 'TIMEOUT' in kwargs:
        timeout = int(kwargs['TIMEOUT'])
    else:
        timeout = 5
    if isinstance(string, basestring):
        strings = [
         string]
    else:
        strings = string
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, int(port)))
        for string in strings:
            sock.send(string)
            reply = sock.recv(16384)

        sock.close()
    except socket.error:
        sys.stderr.write('socket connect error host: %s port: %s' % (host, port))
        error_collection.append('socket connect error host: %s port: %s' % (host, port))
        return

    return reply


def daemon_exe(match_exe):
    r"""
    var_filter = "text to search with"
    using this as the filter will find an executable by name whether it was call by absolute path or bare
    "^(\S*/bash|bash)"
    """
    daemons = {}
    pids = [ pid for pid in os.listdir('/proc') if pid.isdigit() ]
    for pid in pids:
        psexe = ''
        ppid = ''
        pscmd = ''
        pserror = ''
        try:
            ppid = open(os.path.join('/proc', pid, 'stat'), 'rb').read().split()[3]
            pscmd = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read().replace('\x00', ' ').rstrip()
            psexe = os.path.realpath(os.path.join('/proc', pid, 'exe'))
        except TypeError:
            e = ''
            sys.stderr.write('TypeError %s\n' % os.path.join('/proc', pid, 'exe'))
            continue
        except (IOError, OSError):
            continue
        else:
            if psexe:
                if re.search('\\(deleted\\)', psexe):
                    pserror = psexe
                    result = re.match('([^\\(]+)', psexe)
                    psexe = result.group(1).rstrip()
                if os.path.basename(psexe) in match_exe:
                    if ppid == '1' or os.path.basename(psexe) not in daemons:
                        daemons[os.path.basename(psexe)] = {'exe': '', 'cmd': '', 'basename': ''}
                        daemons[os.path.basename(psexe)]['exe'] = psexe
                        daemons[os.path.basename(psexe)]['cmd'] = pscmd
                        daemons[os.path.basename(psexe)]['basename'] = os.path.basename(psexe)
                        if pserror:
                            daemons[os.path.basename(psexe)]['error'] = 'Process %s, %s is in (deleted) status. It may not exist, or may have been updated.' % (pid, pserror)
                            pserror = ''

    return daemons


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def importfile(filename, keyword_regex, **kwargs):
    r"""
    pass the filename of the base config file, and a keyword regular expression to identify the include directive.
    The regexp should include parantheses ( ) around the filename part of the match
    
    keywords: base_path = "/some/path"
    trailing / will be stripped
    kwargs["base_path"] will be added to filename that do not include and absolute path. i.e. Apache includes
    
    Examples (the regexp is case insensitive):
    nginx
        wholeconfig = importfile(conffile,'\s*include\s+(\S+)')
    httpd
        wholeconfig = importfile(conffile,'\s*include\s+(\S+)', base_path="/etc/httpd")
    """
    if 'base_path' in kwargs:
        base_path = kwargs['base_path'].rstrip('/')
    else:
        base_path = ''
    if 'recurse_count' in kwargs:
        kwargs['recurse_count'] += 1
    else:
        kwargs['recurse_count'] = 0
    if kwargs['recurse_count'] > 20:
        sys.stderr.write('Too many recursions while importing %s, the config is probably a loop.\n' % filename)
        error_collection.append('Too many recursions while importing %s, the config is probably a loop.\n' % filename)
        sys.exit(1)

    def full_file_path(right_file, base_path):
        if right_file[0] not in '/':
            return os.path.join(base_path, right_file)
        else:
            return right_file

    files = glob.glob(full_file_path(filename, base_path))
    combined = ''
    for onefile in files:
        onefile_handle = open(onefile, 'r')
        if os.path.isfile(onefile):
            combined += '## START ' + onefile + '\n'
        for line in onefile_handle:
            result = re.match(keyword_regex, line.strip(), re.IGNORECASE)
            if result:
                combined += '#' + line + '\n'
                nestedfile = full_file_path(result.group(1), base_path)
                combined += importfile(nestedfile, keyword_regex, **kwargs)
            else:
                combined += line

        if os.path.isfile(onefile):
            combined += '## END ' + onefile + '\n'
        onefile_handle.close()

    return combined


def kwsearch(keywords, line, **kwargs):
    """
    pass:
        a list of keywords
        a string to check for keywords and extract a value (the value is everything right of the keyword)
        optional: single_value=True returns a list of the values found, unless single_value is True
    """
    line = line.lower()
    stanza = {}
    for word in keywords:
        result = re.match('(%s)\\s*(.*)' % word, line.strip(), re.IGNORECASE)
        if result:
            if 'single_value' not in kwargs:
                if result.group(1).lower() not in stanza:
                    stanza[result.group(1).lower()] = []
                if result.group(2).strip('\'"') not in stanza[result.group(1).lower()]:
                    if 'split_list' not in kwargs:
                        stanza[result.group(1).lower()] += [result.group(2).strip(';"\'')]
                    else:
                        stanza[result.group(1).lower()] += [result.group(2).strip(';"\'').split()]
            else:
                stanza[result.group(1)] = result.group(2).strip('"\'')

    return stanza


def memory_estimate(process_name, **kwargs):
    """
    line_count 16
    biggest 17036
    free_mem 1092636
    line_sum 61348
    """
    status = {'line_sum': 0, 'line_count': 0, 'biggest': 0, 'free_mem': 0, 'buffer_cache': 0, 'php_vsz-rss_sum': 0}
    conf = 'free'
    p = subprocess.Popen(conf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    if not output:
        raise NameError('Fail: %s' % err)
    lines = output.splitlines()
    for line in lines:
        result = re.match('(Mem:)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)', line)
        if result:
            status['free_mem'] = int(result.group(4))
            continue
        result = re.match('(\\+/-\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)', line)
        if result:
            status['buffer_cache'] = int(result.group(4))
            break

    conf = 'ps aux | grep %s' % process_name
    p = subprocess.Popen(conf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    if not output:
        raise NameError('Fail: %s' % err)
    for line in output.splitlines():
        status['line_count'] += 1
        result = re.match('\\s*(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+', line)
        if result:
            status['line_sum'] += int(result.group(6))
            status['php_vsz-rss_sum'] += int(result.group(5)) - int(result.group(6))
            if int(result.group(6)) > status['biggest']:
                status['biggest'] = int(result.group(6))

    return status


def memory_print(result, proc_name, proc_max):
    print '%d %s processes are currently using %d KB of memory, and there is %d KB of free memory.' % (result['line_count'], proc_name, result['line_sum'], result['free_mem'])
    print 'Average memory per process: %d KB will use %d KB if max processes %d is reached.' % (result['line_sum'] / result['line_count'], int(result['line_sum'] / result['line_count'] * proc_max), proc_max)
    print 'Largest process: %d KB will use %d KB if max processes is reached.\n' % (result['biggest'], result['biggest'] * proc_max)
    print 'What should I set max processes to?'
    print 'The safe value would be to use the largest process, and commit 80%% of memory: %d' % int((result['line_sum'] + result['free_mem']) / result['biggest'] * 0.8)
    print
    print 'Current maximum processes: %d' % proc_max
    print 'avg 100% danger   avg 80% warning   lrg 100% cautious   lrg 80% safe'
    print '     %3d                %3d                %3d              %3d' % (
     int((result['line_sum'] + result['free_mem']) / (result['line_sum'] / result['line_count'])),
     int((result['line_sum'] + result['free_mem']) / (result['line_sum'] / result['line_count']) * 0.8),
     int((result['line_sum'] + result['free_mem']) / result['biggest']),
     int((result['line_sum'] + result['free_mem']) / result['biggest'] * 0.8))


def print_sites(localconfig):
    for one in sorted(localconfig):
        if 'domains' in one:
            print 'Domains: %s' % ('  ').join(one['domains'])
        if 'listening' in one:
            print 'listening: %s' % (', ').join(one['listening'])
        if 'doc_root' in one:
            print 'Doc root: %s' % one['doc_root']
        if 'config_file' in one:
            print 'Config file: %s' % one['config_file']
        if 'access_log' in one:
            print 'Access log: %s' % one['access_log']
        if 'error_log' in one:
            print 'Error log: %s' % one['error_log']
        print


def update(d, u):
    """
    update dictionary d with updated dictionary u recursively
    """
    for k in u:
        if isinstance(u[k], dict):
            r = update(d.get(k, {}), u[k])
            d[k] = r
        else:
            d[k] = u[k]

    return d