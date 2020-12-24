# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/scripts/create.py
# Compiled at: 2009-02-26 01:43:18
"""
Скрипт создания каталога для инсталляции СпамоБорца.
"""
import sys, os, subprocess, stat
from optparse import OptionParser
from spamfighter.utils import terminal

def guess_prefix():
    prefix = sys.prefix
    try:
        from pkg_resources import Requirement, resource_filename, DistributionNotFound
        try:
            resource_prefix = resource_filename(Requirement.parse('spamfighter'), '.')
            if os.path.exists(os.path.join(resource_prefix, 'share/spamfighter')):
                prefix = resource_prefix
        except DistributionNotFound:
            pass

    except ImportError:
        pass

    return prefix


def main():
    usage = 'usage: %prog [options] dir'
    parser = OptionParser(usage)
    parser.add_option('--prefix', dest='prefix', default=guess_prefix(), help='prefix of SpamFighter install [default: %default]')
    parser.add_option('--no-https', dest='https', action='store_false', default=True, help='disable HTTPS (no certificate generation, no OpenSSL)')
    parser.add_option('--http-port', dest='http_port', action='store', type='int', default=8000, help='Port for incoming HTTP connections [default: %default]')
    parser.add_option('--https-port', dest='https_port', action='store', type='int', default=8001, help='Port for incoming HTTPS connections [default: %default]')
    parser.add_option('--uid', dest='uid', action='store', type='string', default=None, help='The uid to run as')
    parser.add_option('--gid', dest='gid', action='store', type='string', default=None, help='The gid to run as')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of arguments')
    base_dir = os.path.realpath(args[0])
    print terminal.render('%(WHITE)s%(BOLD)sChecking directory ' + base_dir + '...%(NORMAL)s')
    if os.path.exists(base_dir):
        if not os.path.isdir(base_dir):
            print terminal.render('%(RED)sPath ' + base_dir + " exists, but it isn't a directory!%(NORMAL)s")
            sys.exit(1)
        if os.listdir(base_dir):
            print terminal.render('%(RED)sDirectory ' + base_dir + " isn't empty!%(NORMAL)s")
            sys.exit(1)
    else:
        os.mkdir(base_dir)
    options.prefix = os.path.realpath(options.prefix)
    print terminal.render('%(WHITE)s%(BOLD)sChecking SpamFighter in ' + options.prefix + '...%(NORMAL)s')
    if not os.path.exists(os.path.join(options.prefix, 'share/spamfighter/config.xml')):
        print terminal.render("%(RED)sCan't find SpamFighter installation at " + options.prefix + ', maybe --prefix is wrong?%(NORMAL)s')
        sys.exit(1)
    print terminal.render('%(WHITE)s%(BOLD)sGenerating configuration...%(NORMAL)s')
    config_params = {'CONFIG_FILE': os.path.join(options.prefix, 'share/spamfighter/config.xml'), 
       'MANUAL': os.path.join(options.prefix, 'share/spamfighter/manual/'), 
       'SOURCE_DOCS': os.path.join(options.prefix, 'share/spamfighter/apidocs/'), 
       'ADMIN_PATH': os.path.join(options.prefix, 'share/spamfighter/admin/'), 
       'JSDOCS_PATH': os.path.join(options.prefix, 'share/spamfighter/jsdocs/'), 
       'HTTPS_ENABLED': 'yes' if options.https else 'no', 
       'HTTP_PORT': options.http_port, 
       'HTTPS_PORT': options.https_port, 
       'BASE_DIR': base_dir, 
       'PIDFILE': 'spamfighter.pid', 
       'LOGFILE': 'spamfighter.log', 
       'TWISTD': os.path.join(sys.prefix, 'bin', 'twistd')}
    user_spec = []
    if options.uid:
        user_spec.extend(['-u', options.uid])
    if options.gid:
        user_spec.extend(['-g', options.gid])
    config_params['USER_SPEC'] = (' ').join(user_spec)
    config = config_template % config_params
    print os.path.join(base_dir, 'config.xml')
    f = open(os.path.join(base_dir, 'config.xml'), 'wb')
    f.write(config)
    f.close()
    print terminal.render('%(WHITE)s%(BOLD)sSetting up symlinks...%(NORMAL)s')
    print os.path.join(base_dir, 'html') + ' -> ' + os.path.join(options.prefix, 'share/spamfighter/public_html')
    os.symlink(os.path.join(options.prefix, 'share/spamfighter/public_html'), os.path.join(base_dir, 'html'))
    print terminal.render('%(WHITE)s%(BOLD)sCreating DB directory...%(NORMAL)s')
    print os.path.join(base_dir, 'db')
    os.mkdir(os.path.join(base_dir, 'db'))
    if options.https:
        print terminal.render('%(WHITE)s%(BOLD)sGenerating HTTPS certificate...%(NORMAL)s')
        os.mkdir(os.path.join(base_dir, 'cert'))
        print terminal.render('%(WHITE)s%(BOLD)sPlease, answer questions below:%(NORMAL)s')
        print os.path.join(options.prefix, 'share/spamfighter/cert/scripts/generateLocal.sh')
        if subprocess.call(['/bin/sh', os.path.join(options.prefix, 'share/spamfighter/cert/scripts/generateLocal.sh'), os.path.join(base_dir, 'cert')]) != 0:
            print terminal.render('%(RED)sFailed to execute certificate generation.%(NORMAL)s')
    print terminal.render('%(WHITE)s%(BOLD)sGenerating start scripts...%(NORMAL)s')
    print os.path.join(base_dir, 'start.sh')
    f = open(os.path.join(base_dir, 'start.sh'), 'wb')
    f.write(start_script_template % config_params)
    f.close()
    os.chmod(os.path.join(base_dir, 'start.sh'), stat.S_IREAD | stat.S_IEXEC | stat.S_IWUSR)
    print os.path.join(base_dir, 'stop.sh')
    f = open(os.path.join(base_dir, 'stop.sh'), 'wb')
    f.write(stop_script_template % config_params)
    f.close()
    os.chmod(os.path.join(base_dir, 'stop.sh'), stat.S_IREAD | stat.S_IEXEC | stat.S_IWUSR)
    print terminal.render('%(WHITE)s%(BOLD)sDONE.%(NORMAL)s')
    print terminal.render('%(YELLOW)s' + '-' * 70 + '%(NORMAL)s')
    print terminal.render('  SpamFighter configured in ' + base_dir + '\n')
    print terminal.render('  In order to start SpamFighter:')
    print terminal.render('     cd ' + base_dir)
    print terminal.render('     ./start.sh\n')
    print terminal.render('  Check console and %(LOGFILE)s for errors.\n' % config_params)
    print terminal.render('  Once started, please point your browser to:')
    print terminal.render('    http://localhost:%(HTTP_PORT)d/' % config_params)
    if options.https:
        print terminal.render('    or https://localhost:%(HTTPS_PORT)d/' % config_params)
    print terminal.render('\n  API (JSON-RPC) is available at:')
    print terminal.render('    http://localhost:%(HTTP_PORT)d/api/json/' % config_params)
    print terminal.render('  API (XML-RPC) is available at:')
    print terminal.render('    http://localhost:%(HTTP_PORT)d/api/xml/' % config_params)
    print terminal.render('%(YELLOW)s' + '-' * 70 + '%(NORMAL)s')
    return


config_template = '<?xml version="1.0" encoding="UTF-8"?>\n<config>\n    <global>\n        <include>%(CONFIG_FILE)s</include>\n    </global>\n    <local>\n        <docs>\n            <manual>\n                <path>%(MANUAL)s</path>\n            </manual>\n            <source>\n                <path>%(SOURCE_DOCS)s</path>\n            </source>\n        </docs>\n        <manage>\n            <interface>\n                <path>%(ADMIN_PATH)s</path>\n            </interface>\n            <js_api>\n                <path>%(JSDOCS_PATH)s</path>\n            </js_api>\n        </manage>\n        <http>\n            <port type="int">%(HTTP_PORT)d</port>\n        </http>\n        <https>\n            <enabled>%(HTTPS_ENABLED)s</enabled>\n            <port type="int">%(HTTPS_PORT)d</port>\n        </https>\n    </local>\n</config>'
start_script_template = '#!/bin/sh\n\ncd "%(BASE_DIR)s"\n%(TWISTD)s %(USER_SPEC)s --pidfile="%(PIDFILE)s" --logfile="%(LOGFILE)s" --reactor=poll spamfighter\n'
stop_script_template = '#!/bin/sh\n\ncd "%(BASE_DIR)s"\nkill `cat "%(PIDFILE)s"`\nrm -f "%(PIDFILE)s"\n'
if __name__ == '__main__':
    main()