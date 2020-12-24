# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/work/vulnmine/plugins/plugin2.py
# Compiled at: 2017-08-02 18:00:14
import sys, pandas as pd, re
from yapsy.IPlugin import IPlugin
import vulnmine
sys.path.append('../')
if 'jovyan' in open('/etc/passwd').read():
    import vulns, gbls
else:
    import vulnmine.vulns as vulns, vulnmine.gbls as gbls

class PluginTwo(IPlugin):

    def print_name(self):
        print 'Plugin 2 for custom Vulnmine Reporting has loaded successfully.'
        return

    def custom_stats(self, my_match_vulns):
        """
        Actions
        =======

        Data is grouped by host function to see which type of machine is
        most vulnerable.

        The machines in the VIP AD group are analyzed to determine how
        vulnerable they are.

        Then data is filtered to focus on servers, and then grouped by
        "Region" / criticality of vulns.

        """
        print 'Plugin 2: starting custom_stats.'
        my_df_sft_vuln = my_match_vulns.get()
        my_df_sft_vuln['crit_X'] = my_df_sft_vuln['crit_X_cat'].astype(object)
        dfs2 = my_df_sft_vuln.groupby(['HostFn_X', 'crit_X']).size()
        dfs2a = dfs2.unstack('crit_X').fillna(0)
        print ('\n\nGrouping host vuln data by host function \n{0}\n\n').format(dfs2a)
        dfs2a.reset_index().to_json(orient='records', force_ascii=False, path_or_buf=('{0}').format(gbls.csvdir + 'host_vuln_by_fn.json'))
        s_tmp = my_df_sft_vuln['VIP_X'].value_counts()
        print ('\n\nCount of hosts in various AD groups\n{0}\n\n').format(s_tmp)
        s_tmp.reset_index().to_json(orient='records', force_ascii=False, path_or_buf=('{0}').format(gbls.csvdir + 'num_hosts_AD_gps.json'))
        try:
            df_sys_dsA1_vip = my_df_sft_vuln[my_df_sft_vuln['VIP_X'].notnull()]
            df_3sft_most_vuln_excl_gp = df_sys_dsA1_vip.groupby([
             'VIP_X',
             'crit_X_cat'])
            s_tmp = df_3sft_most_vuln_excl_gp.get_group(('vip', 'High'))['t_cve_name'].value_counts().nlargest(25)
            print ('\n\nFor hosts in VIP AD group: what is the most vulnerable software? \n{0}\n\n').format(s_tmp)
            s_tmp.reset_index().to_json(orient='records', force_ascii=False, path_or_buf=('{0}').format(gbls.csvdir + 'VIP_high.json'))
        except KeyError as e:
            print ('\n\n***VIP / High - KeyError: {0}\n\n').format(e)

        df_sys_dsA1_tmp = my_df_sft_vuln[my_df_sft_vuln.HostFn_X.notnull()]
        df_sys_dsA1_srv = df_sys_dsA1_tmp[(df_sys_dsA1_tmp.HostFn_X == 'server')]
        df_3sft_most_vuln_srv_gp = df_sys_dsA1_srv.groupby([
         'Region_X',
         'crit_X_cat'])
        try:
            s_tmp = df_3sft_most_vuln_srv_gp.get_group(('Region_A', 'High'))['t_cve_name'].value_counts().nlargest(25)
            print ('\n\nFor servers: list top vulnerable software for Region_A \n{0}\n\n').format(s_tmp)
        except KeyError as e:
            print ('\n\n***Corp servers - High vulns - KeyError: {0}\n\n').format(e)

        return