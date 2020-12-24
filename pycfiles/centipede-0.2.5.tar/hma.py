# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/vpn/hma.py
# Compiled at: 2015-09-29 14:51:18
import os, re, requests, sys

def create_config_files(directory):
    """Create all available VPN configuration files in the given directory

    Note: I am basically just following along with what their script
    client does

    """
    template_url = 'https://securenetconnection.com/vpnconfig/openvpn-template.ovpn'
    resp = requests.get(template_url)
    resp.raise_for_status()
    template = resp.content
    server_url = 'https://securenetconnection.com/vpnconfig/servers-cli.php'
    resp = requests.get(server_url)
    resp.raise_for_status()
    servers = resp.content.split('\n')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, 'servers.txt'), 'w') as (f):
        f.write(resp.content)
    for server_line in servers:
        if server_line.strip() == '':
            continue
        server_line = server_line.split('|')
        try:
            ip, desc, country, udp_sup, tcp_sup = server_line
        except ValueError:
            ip, desc, country, udp_sup, tcp_sup, no_rand = server_line

        with open(os.path.join(directory, ip + '.ovpn'), 'w') as (file_o):
            file_o.write(template)
            tcp_sup = tcp_sup.strip()
            if tcp_sup:
                port, proto = (443, 'tcp')
            else:
                port, proto = (53, 'udp')
            file_o.write(('remote {0} {1}\n').format(ip, port))
            file_o.write(('proto {0}\n').format(proto))
            file_o.write('up /etc/openvpn/update-resolv-conf\n')
            file_o.write('down /etc/openvpn/update-resolv-conf\n')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ('Usage {0} <directory to create VPNs in>').format(sys.argv[0])
        sys.exit(1)
    create_config_files(sys.argv[1])