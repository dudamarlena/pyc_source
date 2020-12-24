# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/hwlib/test_lspci.py
# Compiled at: 2018-02-03 12:28:05
# Size of source mod 2**32: 11514 bytes
"""Module to unit test mercury_agent.inspector.hwlib.lspci"""
import mock, pytest, mercury_agent.inspector.hwlib.lspci as lspci
from tests.unit.base import MercuryAgentUnitTest
EXAMPLE_LSPCI_OUTPUT = 'Slot:\t00:00.0\nClass:\tHost bridge [0600]\nVendor:\tIntel Corporation [8086]\nDevice:\tXeon E7 v3/Xeon E5 v3/Core i7 DMI2 [2f00]\nSVendor:\tIntel Corporation [8086]\nSDevice:\tDevice [0000]\nRev:\t02\nNUMANode:\t0\n\nSlot:\t00:01.0\nClass:\tPCI bridge [0604]\nVendor:\tIntel Corporation [8086]\nDevice:\tXeon E7 v3/Xeon E5 v3/Core i7 PCI Express Root Port 1 [2f02]\nRev:\t02\nDriver:\tpcieport\nModule:\tshpchp\nNUMANode:\t0\n\nSlot:\t00:14.0\nClass:\tUSB controller [0c03]\nVendor:\tIntel Corporation [8086]\nDevice:\tC610/X99 series chipset USB xHCI Host Controller [8d31]\nSVendor:\tASUSTeK Computer Inc. [1043]\nSDevice:\tDevice [8600]\nRev:\t05\nProgIf:\t30\nDriver:\txhci_hcd\nNUMANode:\t0\n\nSlot:\t00:16.0\nClass:\tCommunication controller [0780]\nVendor:\tIntel Corporation [8086]\nDevice:\tC610/X99 series chipset MEI Controller #1 [8d3a]\nSVendor:\tASUSTeK Computer Inc. [1043]\nSDevice:\tDevice [8600]\nRev:\t05\nDriver:\tmei_me\nModule:\tmei_me\nNUMANode:\t0\n\nSlot:\t00:19.0\nClass:\tEthernet controller [0200]\nVendor:\tIntel Corporation [8086]\nDevice:\tEthernet Connection (2) I218-V [15a1]\nSVendor:\tASUSTeK Computer Inc. [1043]\nSDevice:\tDevice [85c4]\nRev:\t05\nDriver:\te1000e\nModule:\te1000e\nNUMANode:\t0\n\n\n\nSlot:\t05:00.0\nClass:\tNon-Volatile memory controller [0108]\nVendor:\tSamsung Electronics Co Ltd [144d]\nDevice:\tNVMe SSD Controller SM951/PM951 [a802]\nSVendor:\tSamsung Electronics Co Ltd [144d]\nSDevice:\tDevice [a801]\nPhySlot:\t2-1\nRev:\t01\nProgIf:\t02\nDriver:\tnvme\nModule:\tnvme\nNUMANode:\t0\n'
EXPECTED_PARSED_EXAMPLE_LSPCI_OUTPUT = [
 {'slot':'00:00.0', 
  'class_name':'Host bridge', 
  'class_id':'0600', 
  'vendor_name':'Intel Corporation', 
  'vendor_id':'8086', 
  'device_name':'Xeon E7 v3/Xeon E5 v3/Core i7 DMI2', 
  'device_id':'2f00', 
  'svendor_name':'Intel Corporation', 
  'svendor_id':'8086', 
  'sdevice_name':'Device', 
  'sdevice_id':'0000', 
  'revision':'02'},
 {'slot':'00:01.0', 
  'class_name':'PCI bridge', 
  'class_id':'0604', 
  'vendor_name':'Intel Corporation', 
  'vendor_id':'8086', 
  'device_name':'Xeon E7 v3/Xeon E5 v3/Core i7 PCI Express Root Port 1', 
  'device_id':'2f02', 
  'revision':'02', 
  'driver':'pcieport'},
 {'slot':'00:14.0', 
  'class_name':'USB controller', 
  'class_id':'0c03', 
  'vendor_name':'Intel Corporation', 
  'vendor_id':'8086', 
  'device_name':'C610/X99 series chipset USB xHCI Host Controller', 
  'device_id':'8d31', 
  'svendor_name':'ASUSTeK Computer Inc.', 
  'svendor_id':'1043', 
  'sdevice_name':'Device', 
  'sdevice_id':'8600', 
  'revision':'05', 
  'progif':'30', 
  'driver':'xhci_hcd'},
 {'slot':'00:16.0', 
  'class_name':'Communication controller', 
  'class_id':'0780', 
  'vendor_name':'Intel Corporation', 
  'vendor_id':'8086', 
  'device_name':'C610/X99 series chipset MEI Controller #1', 
  'device_id':'8d3a', 
  'svendor_name':'ASUSTeK Computer Inc.', 
  'svendor_id':'1043', 
  'sdevice_name':'Device', 
  'sdevice_id':'8600', 
  'revision':'05', 
  'driver':'mei_me'},
 {'slot':'00:19.0', 
  'class_name':'Ethernet controller', 
  'class_id':'0200', 
  'vendor_name':'Intel Corporation', 
  'vendor_id':'8086', 
  'device_name':'Ethernet Connection (2) I218-V', 
  'device_id':'15a1', 
  'svendor_name':'ASUSTeK Computer Inc.', 
  'svendor_id':'1043', 
  'sdevice_name':'Device', 
  'sdevice_id':'85c4', 
  'revision':'05', 
  'driver':'e1000e'},
 {'slot':'05:00.0', 
  'class_name':'Non-Volatile memory controller', 
  'class_id':'0108', 
  'vendor_name':'Samsung Electronics Co Ltd', 
  'vendor_id':'144d', 
  'device_name':'NVMe SSD Controller SM951/PM951', 
  'device_id':'a802', 
  'svendor_name':'Samsung Electronics Co Ltd', 
  'svendor_id':'144d', 
  'sdevice_name':'Device', 
  'sdevice_id':'a801', 
  'revision':'01', 
  'driver':'nvme', 
  'progif':'02'}]
FIELDS_PARSED_BY_MODULE = [
 'class_id',
 'class_name',
 'device_id',
 'device_name',
 'driver',
 'progif',
 'revision',
 'sdevice_id',
 'sdevice_name',
 'slot',
 'svendor_id',
 'svendor_name',
 'vendor_id',
 'vendor_name']

def _fixup_parsed_output():
    for device in EXPECTED_PARSED_EXAMPLE_LSPCI_OUTPUT:
        for field in FIELDS_PARSED_BY_MODULE:
            if field not in device.keys():
                device[field] = None


_fixup_parsed_output()

def get_fake_pcidevice_required_args(slot='00:00.0', class_id='beef', vendor_id='dead', device_id='ffff'):
    """Get a dict of args for lspci.PCIDevice"""
    return {'slot':slot, 
     'class_id':class_id, 
     'vendor_id':vendor_id, 
     'device_id':device_id}


class MercuryMiscLspciUnitTests(MercuryAgentUnitTest):
    __doc__ = 'Unit tests for mercury_agent.inspector.hwlib.lspci'

    @mock.patch('mercury_agent.inspector.hwlib.lspci.subprocess.Popen')
    def setUp(self, popen_mock):
        """Setup a PCIBus object for each test."""
        popen_mock.return_value.communicate.return_value = (
         EXAMPLE_LSPCI_OUTPUT, '')
        popen_mock.return_value.returncode = 0
        self.pci_bus = lspci.PCIBus()

    def test_example_output_parsing(self):
        """Test if PCIBus/parse_lspci parsed the example output correctly."""
        assert len(self.pci_bus) == len(EXPECTED_PARSED_EXAMPLE_LSPCI_OUTPUT)
        for device in self.pci_bus:
            assert device in EXPECTED_PARSED_EXAMPLE_LSPCI_OUTPUT

    @mock.patch('mercury_agent.inspector.hwlib.lspci.subprocess.Popen')
    def test_lscpi_run_raises(self, popen_mock):
        """Test what happens when lspci returns non-zero error."""
        popen_mock.return_value.communicate.return_value = (
         EXAMPLE_LSPCI_OUTPUT, '')
        popen_mock.return_value.returncode = 1
        with pytest.raises(lspci.LSPCIError):
            lspci.lspci_run()

    def test_pci_device_raises_on_missing_arg(self):
        """Test that PCIDevice raises when missing args."""
        test_args = get_fake_pcidevice_required_args()
        (lspci.PCIDevice)(**test_args)
        for key in test_args:
            value = test_args[key]
            del test_args[key]
            with pytest.raises(lspci.LSPCIError):
                (lspci.PCIDevice)(**test_args)
            test_args[key] = value

    def test_pci_device__getattr__(self):
        """Test PCIDevice.__getattr__ behavior."""
        pci_device = (lspci.PCIDevice)(**get_fake_pcidevice_required_args())
        if not pci_device.slot == '00:00.0':
            raise AssertionError
        elif not pci_device.asdfjkl is None:
            raise AssertionError

    def test_pcibus_get_devices_by_class(self):
        """Test PCIBus.get_devices_by_class()"""
        devices = self.pci_bus.get_devices_by_class('0108')
        if not isinstance(devices, list):
            raise AssertionError
        else:
            assert len(devices) == 1
            assert devices[0]['device_id'] == 'a802'

    def test_pcibus_has_device_class(self):
        """Test PCIBus.has_device_class()"""
        if not self.pci_bus.has_device_class('0108'):
            raise AssertionError
        else:
            if not self.pci_bus.has_device_class('0200'):
                raise AssertionError
            elif not not self.pci_bus.has_device_class('1337'):
                raise AssertionError
            assert not self.pci_bus.has_device_class('beef')

    def test_pcibus_get_devices_by_vendor(self):
        """Test PCIBus.get_devices_by_vendor()"""
        intel_devices = self.pci_bus.get_devices_by_vendor('8086')
        if not isinstance(intel_devices, list):
            raise AssertionError
        else:
            if not len(intel_devices) == 5:
                raise AssertionError
            else:
                for device in intel_devices:
                    assert device['vendor_id'] == '8086'
                    assert device in EXPECTED_PARSED_EXAMPLE_LSPCI_OUTPUT

                samsung_devices = self.pci_bus.get_devices_by_vendor('144d')
                assert isinstance(intel_devices, list)
                assert len(samsung_devices) == 1
                assert samsung_devices[0]['vendor_id'] == '144d'
                assert samsung_devices[0] in EXPECTED_PARSED_EXAMPLE_LSPCI_OUTPUT
                no_devices = self.pci_bus.get_devices_by_vendor('1337')
                assert isinstance(no_devices, list)
            assert len(no_devices) == 0

    def _membership_and_retrieval_test_helper(self, class_id, name):
        get_function_name = 'get_' + name + '_devices'
        get_func = getattr(self.pci_bus, get_function_name)
        has_function_name = 'has_' + name
        has_func = getattr(self.pci_bus, has_function_name)
        to_delete = []
        for index in range(0, len(self.pci_bus)):
            if self.pci_bus[index]['class_id'] == class_id:
                to_delete.append(index)

        for index in reversed(to_delete):
            del self.pci_bus[index]

        if not not has_func():
            raise AssertionError
        else:
            class_devices = get_func()
            assert isinstance(class_devices, list)
            assert len(class_devices) == 0
            self.pci_bus.append((lspci.PCIDevice)(**get_fake_pcidevice_required_args(class_id=class_id)))
            assert has_func()
            class_devices = get_func()
            assert isinstance(class_devices, list)
            assert len(class_devices) == 1

    def test_pcibus_get_has_fibre_channel_devices(self):
        """Test PCIBus.get_fibre_channel_devices()"""
        self._membership_and_retrieval_test_helper(lspci.FIBRE_CHANNEL, 'fibre_channel')

    def test_pcibus_get_has_ethernet_devices(self):
        """Test PCIBus.{get,has}_ethernet[_devices]()"""
        self._membership_and_retrieval_test_helper(lspci.ETHERNET_CONTROLLER, 'ethernet')

    def test_pcibus_get_has_network_devices(self):
        """Test PCIBus.{get,has}_network[_devices]()"""
        self._membership_and_retrieval_test_helper(lspci.NETWORK_CONTROLLER, 'network')

    def test_pcibus_get_has_raid_bus_devices(self):
        """Test PCIBus.{get,has}_raid_bus[_devices]()"""
        self._membership_and_retrieval_test_helper(lspci.RAID_CONTROLLER, 'raid_bus_controller')