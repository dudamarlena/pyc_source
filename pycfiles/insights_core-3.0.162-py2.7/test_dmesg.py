# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_dmesg.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.dmesg import DmesgLineList
from insights.tests import context_wrap
MSGINFO = ('\nlo: Dropping TSO features since no CSUM feature.\nbnx2 0000:0b:00.0: irq 86 for MSI/MSI-X\nbnx2 0000:0b:00.0: eth0: using MSIX\n(null): Dropping TSO features since no CSUM feature.\n(null): Dropping TSO6 features since no CSUM feature.\nbonding: bond0: enslaving eth0 as a backup interface with a down link.\nHP HPSA Driver (v 3.4.4-1-RH2)\n  alloc irq_desc for 34 on node 0\n  alloc kstat_irqs on node 0\nscsi4 : hpsa\nhpsa 0000:02:00.0: RAID              device c4b3t0l0 added.\nhpsa 0000:02:00.0: Direct-Access     device c4b0t0l0 added.\nscsi 4:3:0:0: RAID              HP       P420i            3.04 PQ: 0 ANSI: 5\nscsi 4:0:0:0: Direct-Access     HP       LOGICAL VOLUME   3.04 PQ: 0 ANSI: 5\nHP HPSA Driver (v 3.4.4-1-RH2)\n[    8.687252] HP HPSA Driver (v 3.4.4-1-RH2) 2.5.0\nlo: Dropping TSO features since no CSUM feature duplicated.\n').strip()
TS_MSGINFO = "\n[    0.000000] tsc: Fast TSC calibration using PIT\n[    0.000000] tsc: Detected 2693.827 MHz processor\n[    0.000026] Calibrating delay loop (skipped), value calculated using timer frequency.. 5387.65 BogoMIPS (lpj=2693827)\n[    0.000028] pid_max: default: 32768 minimum: 301\n[    0.000048] Security Framework initialized\n[    0.000053] SELinux:  Initializing.\n[    0.000059] SELinux:  Starting in permissive mode\n[    0.001043] Dentry cache hash table entries: 2097152 (order: 12, 16777216 bytes)\n[    0.003709] Inode-cache hash table entries: 1048576 (order: 11, 8388608 bytes)\n[    0.004791] Mount-cache hash table entries: 4096\n[    0.004944] Initializing cgroup subsys memory\n[    0.004958] Initializing cgroup subsys net_prio\n[    0.004982] CPU: Physical Processor ID: 0\n[    0.004983] CPU: Processor Core ID: 0\n[    0.004987] ENERGY_PERF_BIAS: Set to 'normal', was 'performance'\n[    0.004987] ENERGY_PERF_BIAS: View and update with x86_energy_perf_policy(8)\n[    0.005828] mce: CPU supports 9 MCE banks\n[    0.005841] CPU0: Thermal monitoring enabled (TM1)\n[    0.005851] Last level iTLB entries: 4KB 0, 2MB 0, 4MB 0\n[    0.005852] Last level dTLB entries: 4KB 64, 2MB 0, 4MB 0\n[    0.005853] tlb_flushall_shift: 6\n[    0.005933] Freeing SMP alternatives: 28k freed\n[    0.006814] ACPI: Core revision 20130517\n[    0.014594] ACPI: All ACPI Tables successfully acquired\n[    0.015670] ftrace: allocating 25815 entries in 101 pages\n[    0.024837] smpboot: Max logical packages: 2\n[    0.024847] DMAR: Host address width 39\n[    0.025063] Enabling x2apic\n[    0.025064] Enabled x2apic\n[    0.025069] Switched APIC routing to cluster x2apic.\n[    0.025482] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1\n[    0.035484] smpboot: CPU0: Intel(R) Core(TM) i7-4800MQ CPU @ 2.70GHz (fam: 06, model: 3c, stepping: 03)\n[    0.035490] TSC deadline timer enabled\n\n[10424.756954] perf: interrupt took too long (2507 > 2500), lowering kernel.perf_event_max_sample_rate to 79750\n"

def test_dmesg():
    dmesg_info = DmesgLineList(context_wrap(MSGINFO))
    assert sorted([ i['raw_message'] for i in dmesg_info.get('HPSA') ]) == sorted([
     'HP HPSA Driver (v 3.4.4-1-RH2)', 'HP HPSA Driver (v 3.4.4-1-RH2)', '[    8.687252] HP HPSA Driver (v 3.4.4-1-RH2) 2.5.0'])
    assert len(dmesg_info.get('lo:')) == 2
    assert 'Dropping' in dmesg_info
    assert dmesg_info.has_startswith('bonding:')
    assert not dmesg_info.has_startswith('xfs:')
    assert len(list(dmesg_info.get_after(0.0001))) == 2
    assert list(dmesg_info.get_after(0.0001))[0]['raw_message'] == '[    8.687252] HP HPSA Driver (v 3.4.4-1-RH2) 2.5.0'
    assert dmesg_info.logs_startwith('(null)') == ['(null): Dropping TSO features since no CSUM feature.', '(null): Dropping TSO6 features since no CSUM feature.']
    ts_info = DmesgLineList(context_wrap(TS_MSGINFO))
    assert ts_info
    assert ts_info.get('Processor Core ID')[0]['raw_message'] == '[    0.004983] CPU: Processor Core ID: 0'
    assert ts_info.has_startswith('ENERGY_PERF_BIAS')
    assert not ts_info.has_startswith('Intel(R) Core(TM)')
    assert 'tlb_flushall_shift' in ts_info
    assert len(list(ts_info.get_after(0.024847))) == 9
    assert len(list(ts_info.get_after(0.024847, 'x2apic'))) == 3
    assert ts_info.logs_startwith('perf') == ['perf: interrupt took too long (2507 > 2500), lowering kernel.perf_event_max_sample_rate to 79750']
    assert ts_info.logs_startwith('systemd') == []