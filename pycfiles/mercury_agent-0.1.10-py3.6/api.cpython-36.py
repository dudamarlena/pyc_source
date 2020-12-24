# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/hardware/raid/abstraction/api.py
# Compiled at: 2018-12-17 12:57:51
# Size of source mod 2**32: 16133 bytes
from size import PercentString, Size

class RAIDAbstractionException(Exception):
    pass


class RAIDActions(object):
    __doc__ = '\n    Bare bones RAID abstraction layer. Simple support for querying and modifying a RAID controller\n    through a standard interface. Many things are not supported, but may be added at a later date\n    If controller specific advanced features are needed, see the provider APIs and RPC capabilities\n\n    '

    def transform_adapter_info(self, adapter_index):
        raise NotImplementedError

    def _add_indexes(self, configuration):
        """
        This method is called to add drive indexes to transformed configuration. This is necessary
        because drives are now only present within an adapter configuration, but we need still
        need abstractly map drives physical location. This is achieved by calling instance.sort_drives
        on a list of aggregate drives, enumerating them, and storing the enumeration as drive.index

        :param configuration: configuration reference of instance.transform_adapter_info output
        :return: None
        """
        drives = [pd for array in configuration['arrays'] for pd in array['physical_drives']]
        drives += configuration['spares'] + configuration['unassigned']
        self.sort_drives(drives)
        for idx, drive in enumerate(drives):
            drive.update({'index': idx})

    def _add_totals(self, adapter_info):
        """
        Adds drive and size totals to adapter_info
        :param adapter_info:
        :return:
        """
        all_drives = self.get_all_drives_from_adapter(adapter_info)
        adapter_info['total_size'] = sum([drive['size'] for drive in all_drives])
        adapter_info['total_drives'] = len(all_drives)

    def get_adapter_info(self, adapter_index):
        """
        Returns adapter details in a standard format. The driver is responsible for finding
        adapters to perform actions on. The abstraction uses indexes rather than vendor references.

        For instance, hpsa uses pci slot ids to specify adapters, onboard adapters will be 0,
        expansion cards will be 3 and 4, should they occupy pci-e slots 3 and 4 on the riser card.
        In order to 'flatten' the interface, these cards will be accessed by enumeration:

        adapter0: slot0
        adapter1: slot3
        adapter2: slot4

        In the rare occurrence that there are multiple manufacturers, cards will enumerated based
        on there subsystem ids (PCI Ids for example). To implement this, the driver probe process
        will need to change so that drivers and handlers are registered in PCI order and not import
        order. Talk to Jared R. about implementation details as he is soldiering on.

        :param adapter_index: The index of the adapter to populate configuration information
        :return: A dictionary representing the adapter

        """
        adapter_info = self.transform_adapter_info(adapter_index)
        self._add_indexes(adapter_info['configuration'])
        self._add_totals(adapter_info)
        return adapter_info

    def create(self, adapter_info, level, drives=None, size=None, array=None):
        """
        This method should only be called from the base classes create_logical_volume method.
        This method will be implemented by all Actions classes.

        :param adapter_info: Transformed adapter data
        :param level: A supported RAID level
        :type level: str
        :param drives: A zero based, expanded list of participating drive indexes.
            Should be None if array is specified
        :param size: A python-size object or None (maximum)
        :param array: The index of the existing array (with sufficient free space) being targeted
            Should be None if drives are specified
        :return:
        """
        raise NotImplementedError

    def create_logical_drive_on_existing_array(self, adapter, adapter_info, level, array, converted_size, percent_string):
        """

        :param adapter:
        :param adapter_info:
        :param level:
        :param array:
        :param converted_size:
        :param percent_string:
        :return:
        """
        try:
            array = adapter_info['configuration']['arrays'][array]
        except (KeyError, IndexError):
            raise RAIDAbstractionException('The referenced array {}:{} does not exist'.format(adapter, array))

        free_space = Size(array['free_space'])
        if free_space < Size('1MiB'):
            raise RAIDAbstractionException('The array {}:{} has not free space'.format(adapter, array))
        else:
            if converted_size:
                if free_space < converted_size:
                    raise RAIDAbstractionException('Requested size {} exceeds available size {}'.format(converted_size, free_space))
            elif percent_string:
                if percent_string.free:
                    converted_size = Size(percent_string.value * free_space.bytes)
                else:
                    raise RAIDAbstractionException('only %FREE is supported for RAID abstraction')
        return self.create(adapter_info, level, drives=None, size=converted_size, array=array)

    def create_logical_drive_on_new_array(self, adapter, adapter_info, level, drives, converted_size, percent_string):
        """

        :param adapter:
        :param adapter_info:
        :param level:
        :param drives:
        :param converted_size:
        :param percent_string:
        :return:
        """
        target_drives = self.get_drives_from_selection(adapter, drives)
        self.raid_minimums(level, len(target_drives))
        if converted_size or percent_string:
            smallest_drive_size = sorted([x['size'] for x in target_drives])[0]
            available_size = self.raid_calculator(level, len(target_drives), smallest_drive_size)
            if converted_size:
                if available_size < converted_size.bytes:
                    raise RAIDAbstractionException('Requested size of {} exceeds available size of {}'.format(converted_size, Size(available_size)))
            else:
                converted_size = Size(percent_string.value * available_size)
        return self.create(adapter_info, level, drives=target_drives, size=converted_size, array=None)

    def create_logical_drive(self, adapter, level, drives=None, size=None, array=None):
        """
        :param adapter:
        :type adapter: int
        :param level: 0, 1, 5, 6, 10, 1+0, 50, 60
        :type level: str
        :param drives: drives should be referenced as 0 based comma separated indexes, ranges, or
        a combination of both. When using a range, both the lower and upper bounds are inclusive.
        Another option is to use all or unassigned. `all` requires that all drives on the adapter
        are not part of the array. `unassigned` will select all drives not currently members of an
        array or participating as spares
        :param size: Size can be specified in bytes (int), a string using SI or IEC standards, a
        percent of total space, or a percent of free space available. If no size is listed, all
        available space will be used
        :param array: An index of an existing array we are updating
        """
        if not (array is not None or drives is not None):
            raise RAIDAbstractionException('Either drive targets or an array must be specified')
        else:
            adapter_info = self.get_adapter_info(adapter)
            percent_string = None
            converted_size = None
            if size:
                if isinstance(size, str) and '%' in size:
                    percent_string = PercentString(size)
                else:
                    converted_size = Size(size)
        if drives is not None:
            return self.create_logical_drive_on_new_array(adapter, adapter_info, level, drives, converted_size, percent_string)
        else:
            return self.create_logical_drive_on_existing_array(adapter, adapter_info, level, array, converted_size, percent_string)

    def delete_logical_drive(self, adapter, array, logical_drive):
        raise NotImplementedError

    def clear_configuration(self, adapter):
        raise NotImplementedError

    def add_spares(self, adapter, drives, arrays=None):
        raise NotImplementedError

    def get_all_drives_from_adapter(self, adapter):
        """
        Get drives while preserving array membership
        :param adapter: target adapter
        :return: drives
        :return type: list
        """
        drives = []
        arrays = adapter['configuration']['arrays']
        for array_idx in range(len(arrays)):
            this_array = arrays[array_idx]
            for pd in this_array['physical_drives']:
                pd.update({'member_of': array_idx})
                drives.append(pd)

        drives += adapter['configuration']['spares'] + adapter['configuration']['unassigned']
        self.sort_drives(drives)
        return drives

    def get_all_drives(self, adapter_index):
        """
        Get drives while preserving array membership
        :param adapter_index: target adapter index
        :return: drives
        :return type: list
        """
        return self.get_all_drives_from_adapter(self.get_adapter_info(adapter_index))

    def get_unassigned(self, adapter_index):
        drives = self.get_all_drives(adapter_index)
        pruned = []
        for drive in drives:
            if 'member_of' in drive:
                pass
            else:
                if 'target' in drive:
                    pass
                else:
                    pruned.append(drive)

        return pruned

    @staticmethod
    def sort_drives(drives):
        drives.sort()

    @staticmethod
    def get_selection_from_pattern(pattern):
        """
        The pattern is a mechanism to target one or more drives attached to a controller.
        See the create_logical_volume documentation for the full format
        :param pattern:
        :type pattern: str
        :return: a list of indexes
        """
        invalid_msg = 'Pattern {} is invalid'.format(pattern)
        items = pattern.split(',')
        selection = []
        for item in items:
            if item.strip().isdigit():
                selection.append(int(item))
            else:
                if '-' not in item:
                    raise RAIDAbstractionException(invalid_msg)
                else:
                    our_range = item.split('-')
                    if len(our_range) != 2:
                        raise RAIDAbstractionException(invalid_msg)
                    try:
                        front, back = [int(x) for x in our_range]
                    except ValueError:
                        raise RAIDAbstractionException('Range is nonsense: {}'.format(our_range))

                if not back > front:
                    raise RAIDAbstractionException(invalid_msg + ' [Range is negative]')
                selection += list(range(front, back + 1))

        return selection

    def parse_selection(self, adapter_index, drive_selector):
        if isinstance(drive_selector, int):
            return [drive_selector]
        else:
            if isinstance(drive_selector, list):
                return drive_selector
            else:
                if drive_selector.lower() == 'all':
                    return [drive['index'] for drive in self.get_all_drives(adapter_index)]
                if drive_selector.lower() == 'unassigned':
                    return [drive['index'] for drive in self.get_unassigned(adapter_index)]
            return sorted(self.get_selection_from_pattern(drive_selector))

    def fetch_selection(self, adapter_index, selection):
        unassigned_drives = {d['index']:d for d in self.get_unassigned(adapter_index)}
        selected_drives = []
        for drive in selection:
            ud = unassigned_drives.get(drive)
            if not ud:
                raise RAIDAbstractionException('Drive {} is not available'.format(drive))
            if not ud['status'] == 'OK':
                raise RAIDAbstractionException('Attempting to initialize a failed drive : {} {}'.format(drive, ud['status']))
            selected_drives.append(ud)

        return selected_drives

    def get_drives_from_selection(self, adapter_index, drive_selector):
        selection = self.parse_selection(adapter_index, drive_selector)
        return self.fetch_selection(adapter_index, selection)

    @staticmethod
    def raid_calculator(level, number_of_drives, size_of_drive, span_depth=2):
        if level == '0':
            return size_of_drive * number_of_drives
        else:
            if level == '1':
                return size_of_drive
            else:
                if level == '5':
                    return size_of_drive * (number_of_drives - 1)
                else:
                    if level == '6':
                        return size_of_drive * (number_of_drives - 2)
                    if level == '10' or level == '1+0':
                        return size_of_drive * (number_of_drives / span_depth)
                if level == '50':
                    return size_of_drive * (number_of_drives - 2)
            if level == '60':
                return size_of_drive * (number_of_drives - 4)
        raise RAIDAbstractionException('Unsupported RAID level')

    @staticmethod
    def raid_minimums(level, number_of_drives):
        if level == '1':
            if number_of_drives < 2:
                raise RAIDAbstractionException('RAID 1 requires at least 2 drives')
            else:
                if level == '5':
                    if number_of_drives < 3:
                        raise RAIDAbstractionException('RAID 5 requires at least 3 drives')
                if level == '6':
                    if number_of_drives < 4:
                        raise RAIDAbstractionException('RAID 6 requires at least 4 drives')
                if (level == '10' or level == '1+0') and number_of_drives < 4:
                    raise RAIDAbstractionException('RAID 10 requires at least 4 drives')
                elif level == '50' and number_of_drives < 6:
                    raise RAIDAbstractionException('RAID 50 requires at least 6 drives')
                elif level == '60':
                    if number_of_drives < 8:
                        raise RAIDAbstractionException('RAID 60 requires at least 8 drives')
        else:
            if level in ('10', '1+0', '50', '60'):
                if number_of_drives % 2:
                    raise RAIDAbstractionException('RAID10/50/60 require an even number of drives')

    def erase(self, adapter, drives, method='fast'):
        """

        :param adapter:
        :param drives:
        :param method:
        :return:
        """
        raise NotImplementedError

    def get_erase_status(self, adapter):
        """

        :param adapter:
        :return:
        """
        raise NotImplementedError

    def erase_in_progress(self, adapter):
        raise NotImplementedError