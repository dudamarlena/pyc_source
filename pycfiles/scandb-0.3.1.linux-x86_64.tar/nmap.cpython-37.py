# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/scandb/nmap.py
# Compiled at: 2019-09-17 10:08:37
# Size of source mod 2**32: 2178 bytes
import argparse, os, peewee
from libnmap.parser import NmapParser
from termcolor import colored
from scandb.util import host_to_tupel, get_ports, hash_file
from scandb.models import Scan, Host, Port, init_db

def import_nmap_file(infile):
    """
    This function is responsable for importing the given file.  For each file a SHA-512 hash is calculated to ensure
    that the file is only imported once.

    :param infile: nmap XML-file to import
    :return:
    """
    sha512 = ''
    print(colored('[*] Importing file: {0}'.format(infile), 'green'))
    try:
        report = NmapParser.parse_fromfile(infile)
        sha512 = hash_file(infile)
        scan = Scan(file_hash=sha512, name=(report.commandline), type='nmap', start=(report.started), end=(report.endtime), elapsed=(report.elapsed),
          hosts_total=(report.hosts_total),
          hosts_up=(report.hosts_up),
          hosts_down=(report.hosts_down))
        scan.save()
        for h in report.hosts:
            address, hostname, os, osgen, status = host_to_tupel(h)
            host = Host(address=address, hostname=hostname, os=os, os_gen=osgen, status=status, scan=scan)
            host.save()
            ports = get_ports(h)
            for p, proto, servicename, state, banner in ports:
                port = Port(host=host, address=address, port=p, protocol=proto, service=servicename, banner=banner, status=state)
                port.save()

        print(colored('[*] File imported. ', 'green'))
    except peewee.IntegrityError as e:
        try:
            print(colored('[-] File already imported: {0}'.format(infile), 'red'))
        finally:
            e = None
            del e

    except Exception as e:
        try:
            print(colored('[-] File cannot be imported : {0}'.format(infile), 'red'))
        finally:
            e = None
            del e