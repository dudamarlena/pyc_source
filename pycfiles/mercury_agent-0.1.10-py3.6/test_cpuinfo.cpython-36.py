# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/hwlib/test_cpuinfo.py
# Compiled at: 2018-02-03 12:28:05
# Size of source mod 2**32: 20515 bytes
"""Module to unit test mercury_agent.inspector.hwlib.cpuinfo"""
import mock, pytest, mercury_agent.inspector.hwlib.cpuinfo as cpuinfo
from tests.unit.base import MercuryAgentUnitTest
EXAMPLE_PROC_CPUINFO_OUTPUT = 'processor\t: 0\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1268.115\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 0\ncpu cores\t: 6\napicid\t\t: 0\ninitial apicid\t: 0\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6612.06\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\n\nprocessor\t: 1\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1199.835\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 1\ncpu cores\t: 6\napicid\t\t: 2\ninitial apicid\t: 2\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6615.66\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor\t: 2\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1200.036\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 2\ncpu cores\t: 6\napicid\t\t: 4\ninitial apicid\t: 4\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6616.18\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor\t: 3\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1200.036\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 3\ncpu cores\t: 6\napicid\t\t: 6\ninitial apicid\t: 6\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6616.25\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor\t: 4\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1200.640\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 4\ncpu cores\t: 6\napicid\t\t: 8\ninitial apicid\t: 8\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6616.27\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor\t: 5\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1200.439\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 5\ncpu cores\t: 6\napicid\t\t: 10\ninitial apicid\t: 10\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6616.28\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor\t: 6\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1300.543\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 0\ncpu cores\t: 6\napicid\t\t: 1\ninitial apicid\t: 1\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6618.23\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor\t: 7\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1200.439\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 1\ncpu cores\t: 6\napicid\t\t: 3\ninitial apicid\t: 3\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6616.75\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor\t: 8\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1200.439\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 2\ncpu cores\t: 6\napicid\t\t: 5\ninitial apicid\t: 5\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6616.36\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor\t: 9\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1200.036\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 3\ncpu cores\t: 6\napicid\t\t: 7\ninitial apicid\t: 7\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6616.22\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor\t: 10\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1199.835\ncache size\t: 15360 KB\nphysical id\t: 0\nsiblings\t: 12\ncore id\t\t: 4\ncpu cores\t: 6\napicid\t\t: 9\ninitial apicid\t: 9\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs\t\t:\nbogomips\t: 6616.40\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\nprocessor       : 11\nvendor_id       : GenuineIntel\ncpu family      : 6\nmodel           : 63\nmodel name      : Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping        : 2\nmicrocode       : 0x39\ncpu MHz         : 1201.245\ncache size      : 15360 KB\nphysical id     : 0\nsiblings        : 12\ncore id         : 5\ncpu cores       : 6\napicid          : 11\ninitial apicid  : 11\nfpu             : yes\nfpu_exception   : yes\ncpuid level     : 15\nwp              : yes\nflags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts\nbugs            :\nbogomips        : 6616.29\nclflush size    : 64\ncache_alignment : 64\naddress sizes   : 46 bits physical, 48 bits virtual\npower management:\n\n'
CPUINFO_TEMPLATE_SINGLE_CPU_ENTRY = 'processor\t: %(processor_num)s\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 63\nmodel name\t: Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz\nstepping\t: 2\nmicrocode\t: 0x39\ncpu MHz\t\t: 1200.640\ncache size\t: 15360 KB\nphysical id\t: %(physical_id)s\nsiblings\t: %(siblings)s\ncore id\t\t: %(core_id)s\ncpu cores\t: %(cpu_cores)s\napicid\t\t: %(apic_id)s\ninitial apicid\t: %(apic_id)s\nfpu\t\t: yes\nfpu_exception\t: yes\ncpuid level\t: 15\nwp\t\t: yes\nflags\t\t: %(flags)s\nbugs\t\t:\nbogomips\t: 6616.29\nclflush size\t: 64\ncache_alignment\t: 64\naddress sizes\t: 46 bits physical, 48 bits virtual\npower management:\n\n'
DEFAULT_CPU_FLAGS = 'fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc dtherm ida arat pln pts'

def get_fake_cpuinfo_output(num_logical_processors=2, hyper_threaded=False, flags=DEFAULT_CPU_FLAGS):
    """Generates valid-looking cpuinfo output for testing."""
    fake_output = ''
    cpu_cores = num_logical_processors / 2 if hyper_threaded else num_logical_processors
    for proc_num in range(0, num_logical_processors):
        fake_output += CPUINFO_TEMPLATE_SINGLE_CPU_ENTRY % {'processor_num':proc_num, 
         'physical_id':0, 
         'siblings':num_logical_processors, 
         'core_id':proc_num % 2 if hyper_threaded else proc_num, 
         'cpu_cores':cpu_cores, 
         'apic_id':proc_num, 
         'flags':flags}

    return fake_output


class MercuryHwlibCpuinfoUnitTests(MercuryAgentUnitTest):
    __doc__ = 'Unit tests for mercury_agent.inspector.hwlib.cpuinfo'

    @mock.patch('mercury_agent.inspector.hwlib.cpuinfo.os.path.exists')
    @mock.patch('mercury_agent.inspector.hwlib.cpuinfo.open')
    def setUp(self, open_mock, os_path_exists_mock):
        super(MercuryHwlibCpuinfoUnitTests, self).setUp()
        os_path_exists_mock.return_value = True
        open_mock.return_value.__enter__.return_value.read.return_value = EXAMPLE_PROC_CPUINFO_OUTPUT
        self.cpuinfo_obj = cpuinfo.CPUInfo()

    @mock.patch('mercury_agent.inspector.hwlib.cpuinfo.os.path.exists')
    def test_proc_cpuinfo_absent(self, os_path_exists_mock):
        """Test what happens if /proc/cpuinfo doesn't exist.

        Particularly when constrcuting a CPUInfo object.
        """
        os_path_exists_mock.return_value = False
        with pytest.raises(OSError):
            cpuinfo.CPUInfo()

    def test_cpu_info_example_output(self):
        """Look at various properties of cpuinfo object to check sanity.

        Tests against EXAMPLE_PROC_CPUINFO_OUTPUT, which is cpuinfo output
        for a 5820k (6 physical cores, 12 logical ones).
        """
        cores_zero = self.cpuinfo_obj.get_cores(0)
        if not isinstance(cores_zero, list):
            raise AssertionError
        else:
            if not len(cores_zero) == 12:
                raise AssertionError
            else:
                for core in cores_zero:
                    assert isinstance(core, dict)

                assert self.cpuinfo_obj.processor_ids == list(range(0, 12))
                assert self.cpuinfo_obj.logical_core_count == 12
                assert self.cpuinfo_obj.total_physical_core_count == 6
                assert self.cpuinfo_obj.cores_per_processor == 6
                lpi = self.cpuinfo_obj.logical_processor_index
                assert isinstance(lpi, dict)
                assert len(lpi.keys()) == 12
                assert list(lpi.keys()) == list(range(0, 12))
                core_zi = self.cpuinfo_obj.core_zero_index
                assert isinstance(core_zi, dict)
            assert len(core_zi.keys()) == 1

    def test_core_dict_missing_phys_id(self):
        """Test behavior when a core_dict is missing data."""
        del self.cpuinfo_obj.core_dicts[0]['physical_id']
        result = self.cpuinfo_obj.physical_index
        if not isinstance(result, dict):
            raise AssertionError
        elif not len(result.keys()) == 1:
            raise AssertionError

    @mock.patch('mercury_agent.inspector.hwlib.cpuinfo.os.path.exists')
    @mock.patch('mercury_agent.inspector.hwlib.cpuinfo.open')
    def test_get_cpufreq_info(self, open_mock, os_path_exists_mock):
        """Test get_cpufreq_info()."""
        os_path_exists_mock.return_value = True
        open_mock.return_value.__enter__.return_value.read.side_effect = [
         '1200000', '4000000', '2000000']
        result = cpuinfo.get_cpufreq_info('0')
        cpufreq_address = '/sys/devices/system/cpu/cpu0/cpufreq'
        if not os_path_exists_mock.called:
            raise AssertionError
        else:
            os_path_exists_mock.assert_called_with(cpufreq_address)
            open_mock.assert_has_calls([
             mock.call(cpufreq_address + '/scaling_min_freq'),
             mock.call(cpufreq_address + '/scaling_max_freq'),
             mock.call(cpufreq_address + '/scaling_cur_freq')],
              any_order=True)
            assert isinstance(result, dict)
            assert len(result.keys()) == 3
            assert result['min'] == 1200000
            assert result['max'] == 4000000
            assert result['cur'] == 2000000
            os_path_exists_mock.return_value = False
            result = cpuinfo.get_cpufreq_info('0')
            assert result == {}

    @mock.patch('mercury_agent.inspector.hwlib.cpuinfo.get_cpufreq_info')
    def test_get_speed_info(self, cpufreq_info_mock):
        """Test CPUInfo.get_physical_speed_info() operation."""
        cpufreq_info_mock.side_effect = [
         {'min':1200000, 
          'max':4000000,  'cur':2000000}] * 12
        speed_info = self.cpuinfo_obj.get_physical_speed_info()
        if not isinstance(speed_info, list):
            raise AssertionError
        else:
            if not len(speed_info) == 1:
                raise AssertionError
            else:
                if not speed_info[0]['cpufreq_enabled'] == True:
                    raise AssertionError
                else:
                    if not speed_info[0]['bogomips'] == 6612.06:
                        raise AssertionError
                    else:
                        if not speed_info[0]['current'] == 2000000.0:
                            raise AssertionError
                        else:
                            if not speed_info[0]['min'] == 1200000.0:
                                raise AssertionError
                            else:
                                if not speed_info[0]['max'] == 4000000.0:
                                    raise AssertionError
                                else:
                                    cpufreq_info_mock.side_effect = [
                                     False]
                                    speed_info = self.cpuinfo_obj.get_physical_speed_info()
                                    assert isinstance(speed_info, list)
                                assert len(speed_info) == 1
                            assert speed_info[0]['cpufreq_enabled'] == False
                        assert speed_info[0]['bogomips'] == 6612.06
                    assert speed_info[0]['current'] == 1268.115
                assert speed_info[0]['min'] == 1268.115
            assert speed_info[0]['max'] == 1268.115