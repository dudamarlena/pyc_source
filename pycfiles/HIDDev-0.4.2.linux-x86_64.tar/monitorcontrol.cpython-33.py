# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.3/dist-packages/hiddev/monitorcontrol.py
# Compiled at: 2013-10-25 16:26:57
# Size of source mod 2**32: 7412 bytes
""" API for via USB controllable monitors """
import hiddev, time, weakref

class ranged_value(int):
    __SLOTS__ = [
     'min', 'max']

    def __new__(cls, value, min, max):
        self = super().__new__(cls, value)
        self.min = min
        self.max = max
        return self

    def __repr__(self):
        return 'monitorcontrol.ranged_value({0}, {0.min}, {0.max})'.format(self)


class input_property:

    def __init__(self, usage_code, type=ranged_value, factor=0):
        self.usage_code = usage_code
        self.type = type
        self.factor = factor

    def __get__(self, parent, owner):
        report, field_index, usage_index = parent.hiddev.find_input(self.usage_code)
        result = report[field_index][usage_index]
        if self.factor:
            result *= 10.0 ** self.factor
        if self.type is not ranged_value:
            return self.type(report[field_index][usage_index])
        else:
            return self.type(report[field_index][usage_index], *report[field_index].logical_range)

    def __set__(self, parent, value):
        raise AttributeError()


class feature_property:

    def __init__(self, usage_code, type=ranged_value):
        self.usage_code = usage_code
        self.type = type

    def __get__(self, parent, owner):
        report, field_index, usage_index = parent.hiddev.find_feature(self.usage_code)
        report.refresh()
        if self.type is not ranged_value:
            return self.type(report[field_index][usage_index])
        else:
            return self.type(report[field_index][usage_index], *report[field_index].logical_range)

    def __set__(self, parent, value):
        report, field_index, usage_index = parent.hiddev.find_feature(self.usage_code)
        report[field_index][usage_index] = int(value)
        report.commit()


class feature_enumeration_list_property:

    def __init__(self, usage_code, code_mapping):
        self.usage_code = usage_code
        self.code_mapping_name = code_mapping
        self.code_mapping = None
        self.type = type
        return

    def get_mapping(self, parent):
        if not self.code_mapping:
            self.code_mapping = getattr(parent, self.code_mapping_name)
        return self.code_mapping

    def find_feature(self, parent):
        for feature in parent.hiddev.features():
            if feature[0].logical_usage == self.usage_code and feature[0].usages[0] & 4294901760 == 8454144:
                return feature

        return

    def __get__(self, parent, owner):
        report = self.find_feature(parent)
        return tuple(self.get_mapping(parent).get(usage, '<{0:08x}>'.format(usage)) for usage in report[0].usages)

    def __set__(self, parent, value):
        raise AttributeError()


class enumerated_feature_property:

    def __init__(self, usage_code, code_mapping):
        self.usage_code = usage_code
        self.code_mapping_name = code_mapping
        self.code_mapping = None
        self.code_mapping_inverse = None
        self.type = type
        return

    def get_mapping(self, parent, inverse=False):
        if not self.code_mapping:
            self.code_mapping = getattr(parent, self.code_mapping_name)
            self.code_mapping_inverse = {v:k for k, v in self.code_mapping.items()}
        if not inverse:
            return self.code_mapping
        return self.code_mapping_inverse

    def find_feature(self, parent):
        for feature in parent.hiddev.features():
            if feature[0].logical_usage == self.usage_code and feature[0].usages[0] & 4294901760 == 8454144:
                return feature

        return

    def __get__(self, parent, owner):
        report = self.find_feature(parent)
        report.refresh()
        usage_value = report[0].get_array_value()
        return self.get_mapping(parent).get(usage_value, '<{0:08x}>'.format(usage_value))

    def __set__(self, parent, value):
        usage_value = self.get_mapping(parent, True).get(value)
        if not usage_value:
            if isinstance(value, str) and value.startswith('<') and value.endswith('>'):
                usage_value = int(value[1:-1], 16)
            else:
                raise ValueError('Invalid value')
        report = self.find_feature(parent)
        report[0].set_array_value(usage_value)
        report.commit()


class MonitorControls:
    VENDOR = 0
    MODEL = 0
    INPUTS = {8454145: 'VGA1', 
     8454146: 'VGA2', 
     8454147: 'VGA3', 
     8454148: 'RGB1', 
     8454149: 'RGB2', 
     8454150: 'RGB3', 
     8454151: 'EVC1', 
     8454152: 'EVC2', 
     8454153: 'EVC3', 
     8454154: 'MAC1', 
     8454155: 'MAC2', 
     8454156: 'MAC3', 
     8454157: 'COMPOSITE1', 
     8454158: 'COMPOSITE2', 
     8454159: 'COMPOSITE3', 
     8454160: 'SVIDEO1', 
     8454161: 'SVIDEO2', 
     8454162: 'SVIDEO3', 
     8454163: 'SCART1', 
     8454164: 'SCART2', 
     8454165: 'SCART_RGB', 
     8454166: 'SCART_SVIDEO', 
     8454167: 'TUNER1', 
     8454168: 'TUNER2', 
     8454169: 'TUNER3', 
     8454170: 'YUV1', 
     8454171: 'YUV2', 
     8454172: 'YUV3'}

    def __new__(cls, hiddev):
        if cls is MonitorControls:
            for subcls in cls.__subclasses__():
                if hiddev.vendor_id == subcls.VENDOR and hiddev.model_id == subcls.MODEL:
                    return subcls(hiddev)

        return super().__new__(cls, hiddev)

    def __init__(self, hiddev):
        self.hiddev = hiddev

    def __repr__(self):
        return '{0}({1!r})'.format(type(self).__name__, self.hiddev)

    def get_name(self):
        return self.hiddev.get_name()

    def get_edid(self):
        report, field_index, _ = self.hiddev.find_feature(8388610)
        return bytes(report[field_index].read_bytes())

    source = enumerated_feature_property(usage_code=8519776, code_mapping='INPUTS')
    sources = feature_enumeration_list_property(usage_code=8519776, code_mapping='INPUTS')
    brightness = feature_property(usage_code=8519696)
    contrast = feature_property(usage_code=8519698)
    red_gain = feature_property(usage_code=8519702)
    green_gain = feature_property(usage_code=8519704)
    blue_gain = feature_property(usage_code=8519706)
    horizontal_position = feature_property(usage_code=8519712)
    vertical_position = feature_property(usage_code=8519728)
    horizontal_frequency = input_property(usage_code=8519852, type=float)
    vertical_frequency = input_property(usage_code=8519854, type=float, factor=-2)


class EizoMonitorControls(MonitorControls):
    VENDOR = 1389
    MODEL = 2
    INPUTS = {8454145: 'DVI', 
     8454146: 'VGA', 
     8454147: 'INPUT3'}
    KEYS = {1: 'UP', 
     2: 'DOWN', 
     4: 'LEFT', 
     8: 'RIGHT', 
     16: 'MENU', 
     32: 'SOURCE', 
     64: 'AUTO', 
     128: 'POWER', 
     256: 'MANUAL'}
    enabled = feature_property(usage_code=4278190127, type=bool)

    def simulate_keypress(self, key):
        if isinstance(key, str):
            for id, k in self.KEYS.items():
                if k == key:
                    key = id
                    continue

        if isinstance(key, str):
            raise ValueError('invalid key: {0}'.format(key))
        report, field_index, usage_index = self.hiddev.find_feature(4278190095)
        report[field_index][usage_index] = key
        report.commit()

    def wait_for_keypress(self):
        while True:
            event = self.hiddev.read()
            if event.usage_code == 4278190095 and event.value & 4095 != 0:
                return self.KEYS.get(event.value & 4095, event.value & 4095)


def enumerate_udev() -> 'iterator(HIDDevice)':
    """
                Enumerate all Monitor Control HID devices via UDev
        """
    for dev in hiddev.enumerate_udev():
        if 8388609 in dev.applications:
            yield dev
            continue


if __name__ == '__main__':
    for dev in enumerate_udev():
        import code
        device = MonitorControls(dev)
        banner = '\nFound "{0}".\n\nMonitorControls object is at `device\'\n'.format(device.get_name()) + 'Press ^D to switch to the next Monitor device or type exit() to exit.\n'
        code.interact(banner=banner, local=locals())