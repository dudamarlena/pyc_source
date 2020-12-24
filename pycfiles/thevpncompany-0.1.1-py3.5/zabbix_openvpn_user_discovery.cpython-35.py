# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thevpncompany/zabbix_openvpn_user_discovery.py
# Compiled at: 2020-01-06 20:06:55
# Size of source mod 2**32: 1570 bytes
import logging, json, subprocess, os
log = logging.getLogger(__name__)
ENV = os.getenv('ENV')
log.debug('Environment ENV: %s' % ENV)
MANAGEMENT_IP = os.getenv('MANAGEMENT_IP', '127.0.0.1')
log.debug('Environment MANAGEMENT_IP: %s' % MANAGEMENT_IP)
MANAGEMENT_PORT = os.getenv('MANAGEMENT_PORT', '7515')
log.debug('Environment MANAGEMENT_PORT: %s' % MANAGEMENT_PORT)
if ENV == 'prod' or ENV == 'tests':
    logging.basicConfig(level=logging.WARN)
else:
    logging.basicConfig(level=logging.DEBUG)

def find_openvpn_current_users():
    clients_raw = subprocess.getoutput('echo "status 3" | nc -w 1 ' + MANAGEMENT_IP + ' ' + MANAGEMENT_PORT + '| grep CLIENT_LIST | grep -v HEADER')
    log.debug('Raw Clients %s' % clients_raw)
    clients = clients_raw.split('\n')
    to_return = []
    for client in clients:
        line_clients = client.split('\t')
        if len(line_clients) > 1:
            log.debug('Client Data: %s' % line_clients)
            cn = line_clients[1]
            log.debug('Adding client %s' % cn)
            client = {'{#ID}': cn}
            to_return.append(client)

    return to_return


def main():
    log.debug('Starting OpenVPN User Discovery')
    zabbix_client_discovery = find_openvpn_current_users()
    print(json.dumps(zabbix_client_discovery))


if __name__ == '__main__':
    main()