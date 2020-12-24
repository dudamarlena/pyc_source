# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/work/vulnmine/plugins/plugin1.py
# Compiled at: 2017-08-02 17:59:06
import sys, pandas as pd, re
from yapsy.IPlugin import IPlugin
import vulnmine
sys.path.append('../')
if 'jovyan' in open('/etc/passwd').read():
    import sccm, gbls
else:
    import vulnmine.sccm as sccm, vulnmine.gbls as gbls

class PluginOne(IPlugin):

    def print_name(self):
        print 'Plugin 1 for custom Vulnmine Input has loaded successfully.'

    def modify_hosts(self, my_hosts):
        """
        Functions
        =========

        _classify_using_sccm_data
            Classify discovered hosts using SCCM discovery data.
        _classify_using_DN_OUs
            Classify hosts by membership in AD OUs
        _classify_using_ad_grps
            Use membership in AD groups to classify hosts.

        """
        new_df_sys = ''

        def _classify_using_sccm_data():
            """Classify discovered hosts using sccm v_R_System data.

            Actions
            =======

            To categorize by Region:

                The AD_Site_Name0 is used to map hosts to a Region.

            Hardcoded lists of sites are then used to classify by region.

            """
            REGION_A = [
             'NTH', 'WST']
            REGION_B = ['STH', 'EST']
            print '\n\n\nEntering plugin1 - _classify_using_sccm_data\n\n'

            def __classify_site_by_region(mysite):
                try:
                    if mysite in REGION_A:
                        myregion = 'Region_A'
                    elif mysite in REGION_B:
                        myregion = 'Region_B'
                    else:
                        myregion = 'Unknown'
                except:
                    print ('\n\n***Error in classifying by \nregion for value: "{0}"\n\n').format(mysite)
                    myregion = None

                return myregion

            s_myRegion = new_df_sys['Site_X'].apply(__classify_site_by_region).astype('category')
            new_df_sys['Region_X'] = pd.Series(s_myRegion, index=new_df_sys.index)
            print ('\n\nRegions: \n{0}\n\n').format(pd.unique(new_df_sys['Region_X'].values))
            print ('\n# hosts in each region: \n{0}\n\n').format(new_df_sys['Region_X'].value_counts())
            return

        def _classify_using_DN_OUs():
            """Classify hosts member of an AD OU.

            Actions
            =======
            Extract various patterns from 'Distinguished_Name0' field of
            the v_R_System table. Use these values to classify the hosts.

            Exceptions
            ==========
            IOError     Produce error message and then ignore

            """
            print '\n\nEntering plugin1 - _classify_using_DN_OUs\n\n'
            s_dn = new_df_sys['Distinguished_Name0'].str.strip().str.lower()
            pattern = re.compile('ou=[0-9A-Za-z_ ]*(desktop|laptop|server)', re.IGNORECASE | re.UNICODE)
            new_df_sys['HostFn_X'] = s_dn.str.extract(pattern, expand=False).astype('category')
            print ('\n\n# hosts of each type:\n{0}').format(new_df_sys['HostFn_X'].value_counts())
            return

        def _classify_using_ad_grps():
            """Classify hosts member of an AD group.

            Actions
            =======
            Read CSV format data which lists contents of the AD groups.

            Mark hosts that are members of these groups.

            Exceptions
            ==========
            IOError     Produce error message and then ignore

            """
            print '\n\nEntering plugin1 - _classify_using_ad_grps\n\n'
            try:
                df_ad_vip = pd.io.parsers.read_csv(gbls.ad_vip_grps, sep=gbls.SEP2, error_bad_lines=False, warn_bad_lines=True, quotechar='"', comment=gbls.HASH, encoding='utf-16')
            except IOError as e:
                print ('\n\n***I/O error({0}): {1}\n\n').format(e.errno, e.strerror)
            except ValueError as e:
                print ('\n\n***Value error: {0}\n- empty data set returned\n\n').format(sys.exc_info()[0])
                df_ad_vip = pd.DataFrame({'distinguishedName': []})
            except:
                print ('\n\n***Unexpected error: {0}\n\n').format(sys.exc_info()[0])
                raise

            print ('\n\nRaw input: Hosts in VIP AD group : \n{0}\n{1}\n\n').format(df_ad_vip.shape, df_ad_vip.columns)
            crit_ad_excl = new_df_sys.Distinguished_Name0.isin(df_ad_vip['distinguishedName'])
            new_df_sys.loc[(crit_ad_excl, 'VIP_X')] = 'vip'
            print ('\n\nSCCM-managed hosts in VIP AD group: \n{0}\n\n').format(new_df_sys['VIP_X'].value_counts())
            print ('\nSystem dataframe with additional classification columns: \n{0}\n{1}\n\n').format(new_df_sys.shape, new_df_sys.columns)
            return

        my_hosts.load()
        new_df_sys = my_hosts.get()
        print ('\nPlugin I/P sccm dframe:\n{0}\n{1}').format(new_df_sys.shape, new_df_sys.columns)
        _classify_using_sccm_data()
        _classify_using_DN_OUs()
        _classify_using_ad_grps()
        my_hosts.df_sys = new_df_sys
        my_hosts.save()
        return