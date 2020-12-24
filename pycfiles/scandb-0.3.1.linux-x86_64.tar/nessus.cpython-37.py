# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/scandb/nessus.py
# Compiled at: 2019-09-17 10:08:37
# Size of source mod 2**32: 3269 bytes
from __future__ import print_function
import argparse, os, peewee
from libnessus.parser import NessusParser
from termcolor import colored
from scandb.util import host_to_tupel, get_ports, hash_file
from scandb.models import Scan, Host, Port, Vuln, init_db

def _nessus_host_to_dbhost(h, scan):
    """
    Create a database host object with the values from the nessus host object.

    :param h: nessus host object
    :type h: libnessus.objects.reporthost.NessusReportHost

    :param scan: database scan object
    :type scan: scandb.models.Scan

    :return: database host object
    :rtype: scandb.models.Host
    """
    host = Host(address=(h.ip), hostname=(h.name), scan=scan)
    netbios = h.get_host_properties.get('netbios-name')
    fqdn = h.get_host_properties.get('host-fqdn')
    operating_system = h.get_host_properties.get('operating-system')
    os = h.get_host_properties.get('os')
    if netbios:
        host.hostname = netbios
    if fqdn:
        host.hostname = fqdn
    if os:
        host.os = os
    if operating_system:
        host.os = operating_system
    return host


def _nessus_vuln_to_dbvuln(v, host):
    """

    :param v:
    :type v: libnessus.objects.reportitem.NessusReportItem
    :return:
    """
    vuln = Vuln(host=host, description=(v.description), synopsis=(v.synopsis), port=(v.port), protocol=(v.protocol), service=(v.service),
      solution=(v.solution),
      severity=(v.severity),
      xref=(v.get_vuln_xref),
      info=(v.get_vuln_info),
      plugin=(v.get_vuln_plugin),
      risk=(v.get_vuln_risk))
    return vuln


def import_nessus_file(infile):
    """
    This function is responsable for importing the given file.  For each file a SHA-512 hash is calculated to ensure
    that the file is only imported once.

    :param infile: nessus XML-file to import
    :return:
    """
    print(colored('[*] Importing file: {0}'.format(infile), 'green'))
    try:
        report = NessusParser.parse_fromfile(infile)
        sha512 = hash_file(infile)
        scan = Scan(file_hash=sha512, name=(report.name), type='nessus', start=(report.started), end=(report.endtime), elapsed=(report.elapsed),
          hosts_total=(report.hosts_total))
        scan.save()
        for h in report.hosts:
            host = _nessus_host_to_dbhost(h, scan=scan)
            host.save()
            for v in h.get_report_items:
                vuln = _nessus_vuln_to_dbvuln(v, host)
                vuln.save()

        print(colored('[*] File imported. ', 'green'))
    except peewee.IntegrityError as e:
        try:
            print(colored('[-] File already imported: {0}'.format(infile), 'red'))
            print(colored('[-] {0}'.format(e.message), 'red'))
        finally:
            e = None
            del e

    except Exception as e:
        try:
            print(colored('[-] {0}'.format(e.message), 'red'))
        finally:
            e = None
            del e