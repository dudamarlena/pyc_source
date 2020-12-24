# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gratia/tools/gip_record.py
# Compiled at: 2008-02-15 09:40:27
import datetime, MySQLdb
from gratia.gip.ldap import query_bdii, read_ldap, config_file
from gratia.gip.common import cp_get, getGipDBConn, findCE
insert_vo_info = '\ninsert into vo_info values\n( %(time)s,\n  %(runningJobs)s,\n  %(totalCpus)s,\n  %(freeJobSlots)s,\n  %(maxTotalJobs)s,\n  %(totalJobs)s,\n  %(status)s,\n  %(lrmsType)s,\n  %(lrmsVersion)s,\n  %(vo)s,\n  %(assignedJobSlots)s,\n  %(freeCpus)s,\n  %(waitingJobs)s,\n  %(maxRunningJobs)s,\n  %(hostName)s,\n  %(queue)s\n)\n'

def main():
    cp = config_file('$HOME/dbinfo/gip_password.conf')
    fp = query_bdii(cp, '(objectClass=GlueVOView)')
    vo_entries = read_ldap(fp)
    fp = query_bdii(cp, '(objectClass=GlueCE)')
    ce_entries = read_ldap(fp)
    conn = getGipDBConn(cp)
    curs = conn.cursor()
    for entry in vo_entries:
        try:
            ce_entry = findCE(entry, ce_entries)
        except:
            continue

        info = {'time': datetime.datetime.now(), 'runningJobs': entry.glue['CEStateRunningJobs'], 'totalCpus': ce_entry.glue['CEInfoTotalCPUs'], 'freeJobSlots': entry.glue['CEStateFreeJobSlots'], 'maxTotalJobs': ce_entry.glue['CEPolicyMaxTotalJobs'], 'totalJobs': entry.glue['CEStateTotalJobs'], 'status': ce_entry.glue['CEStateStatus'], 'lrmsType': ce_entry.glue['CEInfoLRMSType'], 'lrmsVersion': ce_entry.glue['CEInfoLRMSVersion'], 'vo': entry.glue['VOViewLocalID'], 'assignedJobSlots': ce_entry.glue['CEPolicyAssignedJobSlots'], 'freeCpus': ce_entry.glue['CEStateFreeCPUs'], 'waitingJobs': entry.glue['CEStateWaitingJobs'], 'maxRunningJobs': ce_entry.glue['CEPolicyMaxRunningJobs'], 'hostName': ce_entry.glue['CEInfoHostName'], 'queue': ce_entry.glue['CEInfoJobManager']}
        curs.execute(insert_vo_info, info)

    conn.commit()


if __name__ == '__main__':
    main()