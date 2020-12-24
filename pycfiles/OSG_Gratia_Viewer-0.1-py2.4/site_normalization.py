# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gratia/tools/site_normalization.py
# Compiled at: 2008-02-15 09:40:27
import sys
from gratia.gip.ldap import read_bdii, config_file
from gratia.gip.common import join_FK
from gratia.gip.analysis import create_count_dict, sub_cluster_info, correct_sc_info

def create_site_dict(ce_entries, cp):
    """
    Determine site ownership of CEs.
    """
    cluster_entries = read_bdii(cp, query='(objectClass=GlueCluster)')
    site_entries = read_bdii(cp, query='(objectClass=GlueSite)')
    ownership = {}
    for ce in ce_entries:
        cluster = join_FK(ce, cluster_entries, 'ClusterUniqueID')
        site = join_FK(cluster, site_entries, 'SiteUniqueID')
        ownership[ce.glue['CEHostingCluster']] = site.glue['SiteName']

    return ownership


def main():
    cp = config_file()
    entries = read_bdii(cp, query='(objectClass=GlueCE)')
    cluster_info = create_count_dict(entries)
    sc_info = sub_cluster_info(cluster_info.keys(), cp)
    specint = eval(cp.get('cpu_count', 'specint2k'))
    ksi2k_info = {}
    site_dict = create_site_dict(entries, cp)
    sites = cp.get('site_normalization', 'sites').split(',')
    sites = [ i.strip() for i in sites ]
    for (cluster, cpu) in cluster_info.items():
        correct_sc_info(cluster, cpu, sc_info, specint)
        ksi2k = 0
        sc_cores = 0
        for sc in sc_info[cluster]:
            ksi2k += sc.glue['KSI2K']
            sc_cores += int(sc.glue['SubClusterLogicalCPUs'])

        site = site_dict[cluster]
        if site in sites:
            print site, ksi2k * 1000 / sc_cores