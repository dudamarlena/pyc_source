# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/unit/test_mercury_id.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 6344 bytes
"""Unit tests for mercury_id module."""
import itertools, pytest, six
import mercury.common.exceptions as m_exc
import mercury.common.mercury_id as m_id
from tests.common.unit.base import MercuryCommonUnitTest

def get_fake_dmi_dict():
    """Get a dmi dict test-fixture.

    :returns: A dictionary consumable by mercury_id.dmi_methods
    """
    dmi_keys = ('product_uuid', 'chassis_asset_tag', 'chassis_serial', 'board_asset_tag',
                'board_serial')
    return {key:''.join(['fake_', key]) for key in dmi_keys}


def get_fake_inspected_interfaces(num_interfaces=3):
    """Get a inspected interfaces dict test-fixture.

    :returns: A dictionary consumable by mercury_id.generate_mercury_id
    """

    def get_fake_interface(biosdevname='embedded_fake_bios_dev_name', address='192.168.1.1'):
        """Get a fake interface to use to test mercury_id functionality."""
        return {'predictable_names':{'biosdevname': biosdevname}, 
         'address':address}

    return [get_fake_interface(name, address) for name, address in [('embedded_intel_nic_bios_%d' % n, '192.168.1.%d' % n) for n in range(0, num_interfaces)]]


class MercuryIdUnitTest(MercuryCommonUnitTest):
    __doc__ = 'Unit tests for mercury.common.mercury_id module.'

    def test__get_embedded(self):
        """Test _get_embedded()"""
        inspected_interfaces = get_fake_inspected_interfaces()
        print(inspected_interfaces)
        embedded_interfaces = m_id._get_embedded(inspected_interfaces)
        inspected_interfaces[0]['predictable_names']['biosdevname'] = 'what'
        print(inspected_interfaces)
        should_be_changed_ei = m_id._get_embedded(inspected_interfaces)
        assert embedded_interfaces != should_be_changed_ei

    def test__dmi_methods(self):
        """Test _dmi_methods(): When dmi information looks normal."""
        fake_dmi = get_fake_dmi_dict()
        result = m_id._dmi_methods(fake_dmi)
        assert result is not None
        assert isinstance(result, six.string_types)
        fake_dmi['product_uuid'] = 'some_other_uuid'
        new_result = m_id._dmi_methods(fake_dmi)
        assert new_result is not None
        assert isinstance(result, six.string_types)
        assert result != new_result

    def test__dmi_methods_disqualified(self):
        """Test _dmi_methods(): the disqualified message is in the dmi dict."""
        for key in ('chassis_asset_tag', 'chassis_serial', 'board_asset_tag', 'board_serial'):
            fake_dmi = get_fake_dmi_dict()
            fake_dmi[key] = m_id.DMI_DISQUALIFIED_STRING
            fake_dmi['product_uuid'] = None
            assert m_id._dmi_methods(fake_dmi) is None

    def test__dmi_methods_dmi_pairs(self):
        """Test _dmi_methods(): Chassis or board DMI pair not set correctly."""
        fake_dmi = get_fake_dmi_dict()
        fake_dmi['product_uuid'] = None
        result = m_id._dmi_methods(fake_dmi)
        assert result is not None
        assert isinstance(result, six.string_types)
        fake_dmi['chassis_asset_tag'] = None
        second_result = m_id._dmi_methods(fake_dmi)
        assert second_result is not None
        assert isinstance(second_result, six.string_types)
        assert result != second_result
        fake_dmi['board_asset_tag'] = None
        assert m_id._dmi_methods(fake_dmi) is None

    def test_generate_mercury_id(self):
        """Test generate_mercury_id(): Normal cases."""
        inspected_dmi = get_fake_dmi_dict()
        inspected_interfaces = get_fake_inspected_interfaces(3)
        results = [
         m_id.generate_mercury_id(inspected_dmi, inspected_interfaces)]
        inspected_dmi['product_uuid'] = 'something_else'
        results.append(m_id.generate_mercury_id(inspected_dmi, inspected_interfaces))
        inspected_dmi['product_uuid'] = None
        results.append(m_id.generate_mercury_id(inspected_dmi, inspected_interfaces))
        inspected_dmi['chassis_asset_tag'] = m_id.DMI_DISQUALIFIED_STRING
        results.append(m_id.generate_mercury_id(inspected_dmi, inspected_interfaces))
        inspected_interfaces[0]['predictable_names']['biosdevname'] = 'something_else'
        results.append(m_id.generate_mercury_id(inspected_dmi, inspected_interfaces))
        for result in results:
            assert result is not None
            assert isinstance(result, six.string_types)

        for first, second in itertools.combinations(results, 2):
            assert first != second

    def test_generate_mercury_id_raises(self):
        """Test generate_mercury_id(): When it should raise."""
        inspected_dmi = get_fake_dmi_dict()
        inspected_dmi['product_uuid'] = None
        inspected_dmi['chassis_asset_tag'] = m_id.DMI_DISQUALIFIED_STRING
        inspected_interfaces = get_fake_inspected_interfaces(0)
        with pytest.raises(m_exc.MercuryIdException):
            m_id.generate_mercury_id(inspected_dmi, inspected_interfaces)