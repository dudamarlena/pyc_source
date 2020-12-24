# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/FormatTransformer/FormatAdapters/nx_format_adapter.py
# Compiled at: 2016-03-13 23:02:30
from nexusformat import nexus
import numpy
missing = 'NXtransformation'
docstring = 'NXtransformation class'
setattr(nexus, missing, type(missing, (nexus.NXgroup,), {'_class': missing, '__doc__': docstring}))
canonical_groupings = {('wavelength id', ): ['incident wavelength'], ('simple detector axis id', ): [
                                 'simple detector axis vector mcstas', 'simple detector axis offset mcstas', 'simple detector axis type'], 
   ('goniometer axis id', ): [
                            'goniometer axis vector mcstas', 'goniometer axis offset mcstas', 'goniometer axis type'], 
   ('simple scan frame scan id', 'simple scan frame frame id'): [
                                                               'simple scan data'], 
   ('data axis id', ): [
                      'data axis precedence'], 
   ('frame axis location scan id', 'frame axis location axis id', 'frame axis location frame id'): [
                                                                                                  'frame axis location angular position']}

class NXAdapter(object):

    def __init__(self, domain_config):
        self.domain_names = domain_config
        self.filehandle = None
        self.current_entry = None
        self.all_entries = []
        self.has_data = []
        self.name_locations = {'source current': (
                            [
                             'NXinstrument', 'NXsource'], 'current', None, None), 
           'incident wavelength': (
                                 [
                                  'NXinstrument', 'NXmonochromator'], 'wavelength', None, None), 
           'probe': (
                   [
                    'NXinstrument', 'NXsource'], 'probe', self.convert_probe, None), 
           'start time': ([], '@start_time', 'to be done', None), 'simple scan data': (
                              [
                               'NXinstrument', 'NXdetector', 'NXdata'], 'data', None, None), 
           'goniometer axis id': (
                                [
                                 'NXsample', 'NXtransformation'], '', None, None), 
           'goniometer axis vector mcstas': ([], '@vector', None, None), 'goniometer axis offset mcstas': ([], '@offset', None, None), 'simple detector axis id': (
                                     [
                                      'NXinstrument', 'NXdetector', 'NXtransformation'], '', None, None), 
           'simple detector axis vector mcstas': ([], '@vector', None, None), 'simple detector axis offset mcstas': ([], '@offset', None, None), 'frame axis location axis id': (
                                         [
                                          'NXtransformation'], '', None, None), 
           'frame axis location angular position': ([], 'position', None, None), 'simple scan frame scan id': ([], '', None, None), '__data_axis_info': (
                              [
                               'NXinstrument', 'NXdetector', 'NXdata'], 'data@axes', None, None)}
        self.ordering_ids = {'wavelength id': 'L', 
           'frame id': 'Frame'}
        self.equivalent_ids = {'goniometer axis id': [
                                'goniometer location axis id'], 
           'frame id': [
                      'frame axis location frame id', 'simple scan frame frame id'], 
           'simple scan frame scan id': [
                                       'frame axis location scan id']}
        for k, i in self.equivalent_ids.items():
            for one_id in i:
                if self.name_locations.has_key(k):
                    self.name_locations[one_id] = self.name_locations[k]

            if k in self.ordering_ids:
                id_prefix = self.ordering_ids[k]
                for one_id in i:
                    self.ordering_ids[one_id] = id_prefix

        print 'NX: ordered ids now ' + `(self.ordering_ids)`
        try:
            del self.domain_names[('data axis id', )]
        except KeyError:
            pass

        self.keyed_names = set()
        [ self.keyed_names.update(n) for n in self.domain_names.values() ]
        self.all_keys = set()
        [ self.all_keys.update(n) for n in self.domain_names.keys() ]
        self.new_entry()
        self.write_orders = {'simple scan data': ['data axis precedence', 'data axis id'], 'simple detector axis vector mcstas': [
                                                'frame axis location angular position'], 
           'goniometer axis vector mcstas': [
                                           'frame axis location angular position']}
        self.synthetic_values = {'__data_axis_info': (['data axis precedence', 'data axis id'],
                              self.create_axes, self.extract_data_axes)}
        self.from_synthetic = set()
        [ self.from_synthetic.update(n[0]) for n in self.synthetic_values.values() ]
        self.all_known_names = set(self.name_locations.keys()) | set(self.ordering_ids.keys())
        self.all_known_names.update(*[ v[0] for v in self.synthetic_values.values() ])
        self.unit_conversions = {'metres': 'm', 
           'centimetres': 'cm', 
           'millimetres': 'mm', 
           'nanometres': 'nm', 
           'angstroms': 'A', 
           'picometres': 'pm', 
           'femtometres': 'fm', 
           'celsius': 'C', 
           'kelvins': 'K', 
           'degrees': 'deg', 
           'radians': 'rad'}
        return

    def new_entry(self):
        """Initialise all values"""
        self._id_orders = {}
        self._stored = {}
        self.top_name = ''

    def get_by_class(self, parent_group, classname):
        """Return all groups in parent_group with class [[classname]]"""
        classes = [ a for a in parent_group.walk() if getattr(a, 'nxclass') == classname ]
        return classes

    def is_parent(self, child, putative_parent):
        """Return true if the child has parent type putative_parent"""
        return getattr(child.nxgroup, 'nxclass') == putative_parent

    def get_field_value(self, base_group, name):
        """Return value of name in parent_group"""
        if not self.name_locations.has_key(name):
            raise ValueError, 'Do not know how to retrieve %s' % name
        location, property, dummy, convert_func = self.name_locations.get(name)
        parent_group = self._find_group(location, base_group, create=False)
        units = None
        if name == '_parent':
            return (parent_group.nxgroup.nxpath, None)
        else:
            fields = property.split('@')
            prop = fields[0]
            is_attr = len(fields) == 2
            is_property_attr = is_attr and prop != '' and prop != '*'
            is_group = prop == '' or prop == '*'
            if is_attr:
                attr = fields[1]
            if not is_group:
                allvalues = getattr(parent_group, prop)
                try:
                    units = getattr(allvalues, 'units')
                except (AttributeError, KeyError):
                    pass

            else:
                allvalues = parent_group
            if not is_attr:
                if not is_group:
                    return (allvalues.nxdata, units)
                if prop == '':
                    return (allvalues.nxname, None)
                if prop == '*':
                    return (allvalues.nxvalue, None)
            else:
                print 'NX: retrieving %s attribute (prop was %s)' % (attr, prop)
                try:
                    final_values = getattr(allvalues, attr)
                except nexus.NeXusError:
                    raise ValueError, 'Cannot read %s in %s' % (attr, allvalues)

                try:
                    units = getattr(allvalues, attr + '_units')
                except:
                    units = None

                print 'NX: found ' + `final_values` + ',' + `units`
                return (
                 final_values, units)
            return

    def extract_data_axes(self, axes_string):
        """Return the axis precedence for the array data"""
        axes = numpy.array(axes_string.split(':'))
        return (
         numpy.arange(1, len(axes) + 1), axes)

    def create_axes(self, incoming):
        """Create and set the axis specification string"""
        print 'NX: creating axes string with ' + `incoming`
        axis_list = incoming[1]
        axis_order = incoming[0]
        axes_in_order = range(len(axis_order))
        for axis, axis_pos in zip(axis_list, axis_order):
            axes_in_order[axis_pos - 1] = axis

        axis_string = ''
        for axis in axes_in_order:
            axis_string = axis_string + axis + ':'

        print 'NX: Created axis string ' + `(axis_string[:-1])`
        return (
         axis_string[:-1], 'Text', None)

    def manage_units(self, values, old_units, new_units):
        """Convert values from old_units to new_units"""
        if new_units is None or old_units is None or old_units == new_units:
            return values
        import math
        convert_table = {('mm', 'm'): (0, 0.001), 
           ('cm', 'm'): (0, 0.01), 
           ('km', 'm'): (0, 1000), 
           ('pm', 'm'): (0, 1e-09), 
           ('A', 'm'): (0, 1e-10), 
           ('rad', 'deg'): (
                          0, 180 / math.pi), 
           ('K', 'C'): (-273, 1)}
        if (
         old_units, new_units) in convert_table.keys():
            add_const, mult_const = convert_table[(old_units, new_units)]
            return add_const + mult_const * values
        else:
            if (
             new_units, old_units) in convert_table.keys():
                sub_const, div_const = convert_table[(new_units, old_units)]
                return (values - sub_const) / div_const
            poss_units = [ n[0] for n in convert_table.keys() ]
            print 'NX: possible unit conversions: ' + `poss_units`
            if old_units in poss_units and new_units in poss_units:
                common_unit = [ n[1] for n in convert_table.keys() if n[0] == old_units ][0]
                step1 = self.manage_units(values, old_units, common_unit)
                return self.manage_units(step1, common_unit, new_units)
            raise ValueError, 'Unable to convert between units %s and %s' % (old_units, new_units)
            return

    def make_id(self, value_list, prefix=''):
        """Synthesize an ID"""
        try:
            newids = [ prefix + str(r) for r in range(1, len(value_list) + 1) ]
        except TypeError:
            newids = [
             prefix + '1']

        return newids

    def convert_probe(self, values):
        """Convert the xray/neutron/gamma keywords"""
        return values

    def check_type(self, incoming, target_type):
        """Make sure that [[incoming]] has values of type [[target_type]]"""
        try:
            incoming_type = incoming.dtype.kind
            if hasattr(incoming, 'nxdata'):
                incoming_data = incoming.nxdata
            else:
                incoming_data = incoming
        except AttributeError:
            incoming_data = incoming
            if isinstance(incoming, basestring):
                incoming_type = 'S'
            elif isinstance(incoming, int):
                incoming_type = 'i'
            elif isinstance(incoming, float):
                incoming_type = 'f'
            else:
                raise ValueError, 'Unrecognised type for ' + `incoming`

        if target_type == 'Real':
            if incoming_type not in 'fiu':
                raise ValueError, 'Real type has actual type %s' % incoming_type
        elif target_type == 'Int':
            if incoming_type not in 'iu':
                raise ValueError, 'Integer type has actual type %s' % incoming_type
        elif target_type == 'Text':
            if incoming_type not in 'OSU':
                print 'Warning: character type has actual type %s' % incoming_type
                incoming_data = str(incoming_data)
        return incoming_data

    def get_single_names(self):
        """Return a list of canonical ids that may only take a single
        unique value in one data unit"""
        return [
         'simple scan frame scan id']

    def get_by_name(self, name, value_type, units=None):
        """Return values as [[value_type]] for [[name]]"""
        try:
            raw_values, old_units = self.internal_get_by_name(name)
        except ValueError:
            raw_values = None

        if raw_values is None or raw_values == []:
            return raw_values
        raw_values = numpy.atleast_1d(raw_values)
        print 'NX: raw value for %s:' % name + `raw_values`
        before_units = numpy.atleast_1d(map(lambda a: self.check_type(a, value_type), raw_values))
        unit_abbrev = self.unit_conversions.get(units, units)
        old_unit_abbrev = self.unit_conversions.get(old_units, old_units)
        proper_units = self.manage_units(before_units, old_unit_abbrev, unit_abbrev)
        return [ a for a in proper_units ]

    def internal_get_by_name(self, name):
        """Return a value with native format and units"""
        if name in self._stored:
            return self._stored[name]
        else:
            if name in self.from_synthetic:
                internal_name = [ a for a in self.synthetic_values.keys() if name in self.synthetic_values[a][0] ][0]
                external_names, creat_func, extract_func = self.synthetic_values[internal_name]
                internal_val, dummy = self.internal_get_by_name(internal_name)
                new_vals = extract_func(internal_val)
                for n, v in zip(external_names, new_vals):
                    self._stored[n] = (
                     v, None)

                return self._stored[name]
            is_a_primary = len([ k for k in self.domain_names.values() if name in k ]) > 0
            if is_a_primary:
                key_arrays = self.get_key_arrays(name)
                print 'NX: all keys and values for %s: ' % name + `key_arrays`
                self._stored.update(key_arrays)
                if name in key_arrays:
                    return key_arrays[name]
                print 'NX: tried to find %s, not found' % `name`
                raise ValueError, 'Primary name not found: %s' % name
            poss_names = [ k[1] for k in self.domain_names.items() if name in k[0] ]
            if len(poss_names) > 0:
                print 'NX: possible names for %s: ' % name + `poss_names`
                for pn in poss_names[0]:
                    try:
                        result = self.internal_get_by_name(pn)
                    except ValueError:
                        continue

                    if name in self._stored:
                        return self._stored[name]

            if name not in self.name_locations:
                raise ValueError, 'No such name known: ' + `name`
            group_loc, property, dummy1, dummy2 = self.name_locations[name]
            if property == '' or property[0] == '@':
                n = self.get_group_values(name, self.current_entry)
                if n is not None:
                    result, result_classes = zip(*n)
                    return (
                     result, None)
                return (None, None)
            else:
                return self.get_field_value(self.current_entry, name)
            return

    def get_group_values(self, name, parent_group=None):
        """Use our lookup table to get the value of group name relative to parent group"""
        if parent_group is None:
            upper_group = self.current_entry
        else:
            upper_group = parent_group
        print 'NX: searching for value of %s in %s' % (name, upper_group)
        nxlocation = self.name_locations.get(name, None)
        if nxlocation is None:
            print 'NX: warning - no location found for %s in %s' % (name, upper_group)
            return
        else:
            nxclassloc, property, convert_function, dummy = nxlocation
            if property != '':
                raise ValueError, 'Group-valued name has field/attribute name set:' + `name`
            upper_classes = list(nxclassloc)
            upper_classes.reverse()
            new_classes = [upper_group]
            if len(upper_classes) > 0:
                while len(upper_classes) > 1:
                    target_class = upper_classes.pop()
                    if target_class == '*':
                        target_class = target_classes.pop()
                    new_classes = self.get_by_class(upper_group, target_class)
                    if len(new_classes) > 1:
                        raise ValueError, 'Multiple groups found of type %s but only one expected: %s' % (target_class, new_classes)
                    elif len(new_classes) == 0:
                        return
                    upper_group = new_classes[0]

                new_classes = self.get_by_class(new_classes[0], upper_classes[0])
            if len(new_classes) == 0:
                return
            all_values = [ s.nxname for s in new_classes ]
            print 'NX: for %s obtained %s' % (name, `all_values`)
            if convert_function is not None:
                all_values = convert_function(all_values)
                print 'NX: converted %s using %s to get %s' % (name, `convert_function`, `all_values`)
            return zip(all_values, new_classes)

    def get_key_arrays(self, name):
        """Get arrays corresponding to all keys and values used with name"""
        all_keys = [ k for k in self.domain_names.keys() if name in self.domain_names[k] ]
        if len(all_keys) == 0:
            raise ValueError, 'Request for a key name or non-existent name %s' % name
        all_keys = all_keys[0]
        print 'NX: keys for %s: ' % name + `all_keys`
        if len(all_keys) == 0:
            return {name: self.get_field_value(self.current_entry, name)}
        else:
            if len(all_keys) == 1 and all_keys[0] in self.ordering_ids:
                main_data = self.get_field_value(self.current_entry, name)
                return {name: main_data, all_keys[0]: (self.make_id(main_data[0]), None)}
            all_keys = list(all_keys)
            if all_keys[(-1)] in self.ordering_ids:
                ordering_key = all_keys[(-1)]
                all_keys = all_keys[:-1]
            else:
                ordering_key = None
            all_keys.append(name)
            key_tree, dummy1, ordering_tree = self.get_sub_tree(self.current_entry, all_keys, do_ordering=ordering_key is not None)
            if key_tree is None:
                raise ValueError, 'No tree found for key list ' + `all_keys`
            print 'NX: found key tree ' + `key_tree`
            key_tree = (
             key_tree, None)
            if ordering_key is not None:
                maxlen = self.get_leaf_length(key_tree)
                print 'Found maximum leaf length of %d' % maxlen
                self.uncompress_tree(key_tree, (ordering_tree, None), maxlen)
            final_arrays = []
            [ final_arrays.append([]) for k in all_keys ]
            length, units_array = self.synthesize_values(final_arrays, key_tree)
            valuedict = dict(zip(all_keys, zip(final_arrays, units_array)))
            if ordering_key is not None:
                counting_arrays = []
                dummy_array = []
                [ counting_arrays.append([]) for k in all_keys ]
                print 'NX: creating ordering id'
                length, dummy_array = self.synthesize_values(counting_arrays, (ordering_tree, None))
                counting_dict = dict(zip(all_keys, zip(counting_arrays, dummy_array)))
                key_prefix = self.ordering_ids[ordering_key]
                valuedict[ordering_key] = ([ key_prefix + str(c) for c in counting_dict[all_keys[(-1)]][0] ], None)
                print 'NX: set %s to %s' % (ordering_key, valuedict[ordering_key])
            return valuedict

    def get_sub_tree(self, parent_group, keynames, do_ordering=False):
        """Get the key tree underneath parent_group, or return an ordering
          if do_ordering is True"""
        print 'NX: get_sub_tree called with parent %s, keys %s' % (parent_group, keynames)
        sub_dict = {}
        ordering_dict = {}
        if len(keynames) == 1:
            value = self.get_field_value(parent_group, keynames[0])
            if do_ordering:
                print 'NX: creating an ordering for actual values'
                return (
                 value[0], value[1], self.make_id(value[0]))
            if isinstance(value[0], numpy.ndarray):
                return ([value[0]], value[1], None)
            return (
             value[0], value[1], None)
        keys_and_groups = self.get_group_values(keynames[0], parent_group)
        if keys_and_groups is None:
            return (None, None, None)
        else:
            for another_key, another_group in keys_and_groups:
                new_tree, units, ordering_tree = self.get_sub_tree(another_group, keynames[1:], do_ordering)
                if new_tree is not None:
                    sub_dict[another_key] = (
                     new_tree, units)
                    ordering_dict[another_key] = (ordering_tree, None)

            return (
             sub_dict, None, ordering_dict)

    def get_leaf_length(self, target_tree):
        maxlen = 0
        if isinstance(target_tree[0], dict):
            for k in target_tree[0].keys():
                maxlen = max(self.get_leaf_length(target_tree[0][k]), maxlen)

        else:
            try:
                maxlen = len(target_tree[0])
            except TypeError:
                print 'Warning, unable to determine length of ' + `(target_tree[0])`
                maxlen = 1

        return maxlen

    def uncompress_tree(self, target_tree, ordering_tree, target_length):
        if isinstance(target_tree[0], dict):
            for k in target_tree[0].keys():
                test_val = target_tree[0][k]
                if isinstance(test_val[0], list):
                    if len(test_val[0]) == 1:
                        print 'Expanding ' + `test_val`
                        target_tree[k] = (list(test_val[0]) * target_length, test_val[1])
                        ordering_tree[k] = (self.make_id(target_tree[k][0]), None)
                elif isinstance(test_val[0], numpy.ndarray):
                    if test_val[0].size == 1:
                        print 'Expanding ' + `test_val`
                        target_tree[0][k] = (list(numpy.atleast_1d(test_val[0])) * target_length, test_val[1])
                        ordering_tree[0][k] = (self.make_id(target_tree[0][k][0]), None)
                else:
                    for k in target_tree[0].keys():
                        self.uncompress_tree(target_tree[0][k], ordering_tree[0][k], target_length)

        else:
            print 'Warning: uncompress dropped off end with value ' + `target_tree`
        return

    def synthesize_values(self, key_arrays, key_tree):
        """Given a key tree, return an array of equal-length values, one for
          each level in key_tree. Key_arrays and units_array
          should have the same length as the depth of key_tree.

          """
        print 'Called with %s, tree %s' % (`key_arrays`, `key_tree`)
        units_array = [None]
        for one_key in key_tree[0].keys():
            if isinstance(key_tree[0][one_key][0], dict):
                extra_length, units = self.synthesize_values(key_arrays[1:], key_tree[0][one_key])
                key_arrays[0].extend([one_key] * extra_length)
                print 'Extended %s with %s' % (`(key_arrays[0])`, `one_key`)
            else:
                value, units = key_tree[0][one_key]
                print 'Leaf value for %s is: ' % one_key + `value` + ',' + `units`
                extra_length = len(value)
                key_arrays[1].extend(value)
                key_arrays[0].extend([one_key] * len(value))

        if isinstance(units, list):
            units_array.extend(units)
        else:
            units_array.append(units)
        print 'Key arrays now ' + `key_arrays`
        print 'Units array now ' + `units_array`
        return (
         extra_length * len(key_tree[0]), units_array)

    def set_by_name(self, name, value, value_type, units=None):
        """Set value of canonical [[name]] in datahandle"""
        if not isinstance(value, (list, tuple, numpy.ndarray)) and name not in self.get_single_names():
            raise ValueError, 'All values must be lists,tuples or arrays: passed %s for %s' % (value, name)
        if name not in self.all_known_names:
            raise ValueError, 'Name %s not recognised' % name
        if name in self.get_single_names() and not isinstance(value, list):
            self._stored[name] = (
             [
              value], value_type, units)
        else:
            self._stored[name] = (
             value, value_type, units)
        print 'NX: stored %s:' % name + `(self._stored[name])`

    def partition(self, first_array, second_array):
        """Partition the second array into segments corresponding to identical values of the 
        first array, returning the partitioned array and the unique values. Each array is
        a tuple ([values],units)."""
        print 'Partition called with 1st, 2nd:' + `first_array` + ' ' + `second_array`
        combined = zip(first_array[0], second_array[0])
        unique_vals = list(set(first_array[0]))
        final_vals = []
        for v in unique_vals:
            final_vals.append(([ k[1] for k in combined if k[0] == v ], second_array[1]))

        print 'NX: partition returns ' + `final_vals`
        return (
         final_vals, unique_vals)

    def create_tree(self, start_arrays, current_depth=0, max_depth=None):
        """Return a tree created by partitioning each array into unique elements, with
        each subsequent array being the next level in the tree. Each element in start_arrays
        is a two-element tuple ([values], units). """
        check_len = set([ len(a) for a in start_arrays ])
        if check_len != set([2]):
            raise ValueError, 'Calls to create tree must provide ([values],units) tuples, we            were passed ' + `start_arrays`
        print 'Creating a tree to depth %s from %s' % (`max_depth`, `start_arrays`)
        if current_depth == max_depth or max_depth is None and len(start_arrays) == 1:
            return start_arrays[0]
        else:
            partitioned = [ self.partition(start_arrays[0], a) for a in start_arrays[1:] ]
            part_arrays = zip(*[ a[0] for a in partitioned ])
            sub_tree = (dict(zip(partitioned[0][1], [ self.create_tree(p, current_depth + 1, max_depth) for p in part_arrays ])), None)
            print 'NX: returned ' + `sub_tree`
            return sub_tree

    def create_index(self, first_array, second_array):
        """Return second array in a canonical order with ordering given by values in first array.
        The sort order is also returned for reference."""
        sort_order = first_array[:]
        sort_order.sort()
        sort_order = [ first_array.index(k) for k in sort_order ]
        canonical_order = [ second_array[p] for p in sort_order ]
        return (
         canonical_order, sort_order)

    def output_tree(self, parent_group, names, value_tree, ordering_tree, compress=False):
        """Output a tree of values, with each level corresponding to values in [names]"""
        sort_order = None
        print 'Outputting tree: ' + `value_tree` + ' with ordering ' + `ordering_tree`
        if len(names) == 0:
            return
        else:
            if isinstance(value_tree[0], dict):
                for one_key in value_tree[0].keys():
                    child_group = self.store_a_group(parent_group, names[0], one_key, self._stored[names[0]][1], self._stored[names[0]][2])
                    self.output_tree(child_group, names[1:], value_tree[0][one_key], ordering_tree[0][one_key], compress)

            else:
                if ordering_tree != value_tree and isinstance(value_tree[0], list) and len(value_tree[0]) > 1:
                    print 'Found ordering tree: %s for %s' % (`ordering_tree`, `value_tree`)
                    output_order, sort_order = self.create_index(ordering_tree[0], value_tree[0])
                    if compress:
                        print 'Trying to compress:' + `output_order`
                        try:
                            if len(set(output_order)) == 1:
                                output_order = [
                                 output_order[0]]
                            else:
                                print 'Unable to compress, %d distinct values' % len(set(output_order))
                        except TypeError:
                            print 'Unhashable, no compression'

                else:
                    output_order, sort_order = value_tree[0][0], None
                self.store_a_value(parent_group, names[0], output_order, self._stored[names[0]][1], self._stored[names[0]][2])
            return

    def store_a_group(self, parent_group, name, value, value_type, units):
        location_info = self.name_locations[name][0]
        print 'NX: setting %s (location %s) to %s' % (name, `location_info`, value)
        current_loc = parent_group
        if len(location_info) > 1:
            current_loc = self._find_group(location_info[:-1], parent_group)
        elif len(location_info) == 0:
            parent_group.nxname = value
            return parent_group
        target_class = location_info[(-1)]
        target_groups = [ g for g in current_loc.walk() if g.nxclass == target_class ]
        found = [ g for g in target_groups if g.nxname == value ]
        if len(found) > 1:
            raise ValueError, 'More than one group with name %s' % value
        elif len(found) == 1:
            return found[0]
        new_group = getattr(nexus, target_class)()
        current_loc[value] = new_group
        print 'NX: created a new %s group value %s' % (target_class, value)
        return new_group

    def store_a_value(self, parent_group, name, value, value_type, units):
        """Store a non-group value (attribute or field)"""
        location_info = self.name_locations[name]
        group_location = location_info[0]
        print 'NX: setting %s (location %s relative to %s) to %s' % (name, `location_info`, `parent_group`, value)
        current_loc = self._find_group(group_location, parent_group)
        self.write_a_value(current_loc, location_info[1], value, value_type, units)

    def write_a_value(self, current_loc, name, value, value_type, unit_abbrev):
        """Write a value to the group"""
        if '@' not in name:
            current_loc[name] = value
            if unit_abbrev is not None:
                current_loc[name].units = unit_abbrev
        else:
            base, attribute = name.split('@')
            if unit_abbrev is not None:
                print 'Warning: trying to set units %s on attribute, will write units to ' % `unit_abbrev` + attribute + '_units'
            if base != '' and not current_loc.has_key(base):
                raise AttributeError, 'NX: Cannot write attribute %s as field %s missing' % (attribute, base)
            elif base == '':
                current_loc.attrs[attribute] = value
                if unit_abbrev is not None:
                    current_loc.attrs[attribute + '_units'] = unit_abbrev
            else:
                current_loc[base].attrs[attribute] = value
                if unit_abbrev is not None:
                    current_loc[base].attrs[attribute + '_units'] = unit_abbrev
        return

    def _find_group(self, location, start_group, create=True):
        """Find or create a group corresponding to location and return the NXgroup"""
        current_loc = start_group
        if len(location) == 0:
            return start_group
        for nxtype in location:
            candidates = [ a for a in current_loc.walk() if getattr(a, 'nxclass') == nxtype ]
            if len(candidates) > 1:
                raise ValueError, 'Non-singleton group %s in item location: ' % nxtype + `location`
            if len(candidates) == 1:
                current_loc = candidates[0]
            elif create:
                new_group = getattr(nexus, nxtype)()
                current_loc[nxtype[2:]] = new_group
                print 'NX: created new group %s of type %s' % (nxtype[2:], nxtype)
                current_loc = new_group

        return current_loc

    def write_a_group(self, name, location, nxtype):
        """Write a group of nxtype in location"""
        current_loc = self._find_group(location)
        current_loc.insert(getattr(nexus, nxtype)(), name=name)

    def open_file(self, filename):
        """Open the NeXus file [[filename]]"""
        self.filehandle = nexus.nxload(filename, 'r')

    def open_data_unit(self, entryname=None):
        """Open a
        particular entry .If
        entryname is not provided, the first entry found is
        used and a unique name created"""
        entries = [ e for e in self.filehandle.NXentry ]
        if entryname is None:
            self.current_entry = entries[0]
        else:
            our_entry = [ e for e in entries if e.nxname == entryname ]
            if len(our_entry) == 1:
                self.current_entry = our_entry[0]
            else:
                raise ValueError, 'Entry %s not found' % entryname
        return

    def create_data_unit(self, entryname=None):
        """Start a new data unit"""
        self.current_entry = nexus.NXentry()
        self.current_entry.nxname = 'entry' + `(len(self.all_entries) + 1)`

    def close_data_unit(self):
        """Finish all processing"""
        output_names = set(self._stored.keys())
        self.has_data.append('simple data' in output_names)
        print 'NX:now outputting ' + `output_names`
        priority_names = set()
        wait_names = set()
        for name in output_names:
            priority_names.update([ k for k in self.write_orders.keys() if name in self.write_orders[k] ])
            [ wait_names.update(list(k)) for k in self.domain_names.keys() if name in self.domain_names[k] ]

        waiting = (priority_names | wait_names) - output_names
        priority_names = priority_names - waiting
        print 'Priority names: ' + `priority_names`
        if len(waiting) > 0:
            print 'Warning: following IDs not found but might be needed in order to output:' + `waiting`
        for synth_name, synth_methods in self.synthetic_values.items():
            external_names, create_meth, dummy = self.synthetic_values[synth_name]
            if output_names.intersection(external_names) == set(external_names):
                ext_vals = [ self._stored[k][0] for k in external_names ]
                self._stored[synth_name] = create_meth(ext_vals)
                output_names.difference_update(external_names)
                output_names.add(synth_name)

        primary_names = set()
        [ primary_names.update(n[1]) for n in self.domain_names.items() if len(n[0]) > 1 or n[0][0] not in self.ordering_ids
        ]
        primary_names = primary_names.intersection(output_names)
        for pn in priority_names:
            print 'NX: outputting priority name: ' + pn
            if pn in primary_names:
                self.output_keyed_values([pn], output_names)
            else:
                self.output_unkeyed_values([pn], output_names)

        print 'NX: now outputting primary names ' + `primary_names`
        self.output_keyed_values(primary_names, output_names)
        dangling_keys = self.all_keys.intersection(output_names).difference(self.ordering_ids.keys())
        print 'NX: found dangling keys %s' % `dangling_keys`
        while len(dangling_keys) > 0:
            dk = dangling_keys.pop()
            key_seq = [ list(k) for k in self.domain_names.keys() if dk in k ][0]
            key_seq = [ k for k in key_seq[:key_seq.index(dk) + 1] if k in self._stored.keys() ]
            key_vals = [ (self._stored[k][0], self._stored[k][2]) for k in key_seq ]
            key_vals.append(([[]] * len(key_vals[(-1)][0]), None))
            tree_for_output = self.create_tree(key_vals, max_depth=len(key_vals) - 1)
            self.output_tree(self.current_entry, key_seq, tree_for_output, tree_for_output)
            output_names.difference_update(key_seq)
            dangling_keys.difference_update(key_seq)

        straight_names = output_names.difference(self.ordering_ids.keys())
        print 'NX: now outputting straight names ' + `straight_names`
        self.output_unkeyed_values(straight_names, output_names)
        if len(output_names) > 0:
            raise ValueError, 'Did not output all data: %s remain' % `output_names`
        self.all_entries.append(self.current_entry)
        self.current_entry = None
        self.new_entry()
        return

    def output_keyed_values(self, primary_names, output_names):
        """Output all names in primary_names, including any keys"""
        for pn in primary_names:
            pn_keys = [ k for k in self.domain_names.keys() if pn in self.domain_names[k] ]
            pn_value = (
             self._stored[pn][0], self._stored[pn][2])
            if len(pn_keys) > 0:
                pn_keys = pn_keys[0]
            ordering_keys = [ k for k in pn_keys if k in self.ordering_ids ]
            if len(ordering_keys) > 1:
                raise ValueError, 'Only one ordering key possible for %s, but found %s' % (pn, `ordering_keys`)
            ordering_key = None
            if len(ordering_keys) == 1:
                ordering_key = ordering_keys[0]
                if pn_keys.index(ordering_key) != len(pn_keys) - 1:
                    raise ValueError, 'Only the final key can be an ordering key: %s in %s for name %s' % (ordering_key, `pn_keys`, pn)
                pn_keys = pn_keys[:-1]
            pn_key_vals = [ (self._stored[k][0], self._stored[k][2]) for k in pn_keys ] + [pn_value]
            tree_for_output = self.create_tree(pn_key_vals, max_depth=len(pn_keys))
            tree_for_ordering = tree_for_output
            if ordering_key is not None:
                pn_key_vals[-1] = (
                 self._stored[ordering_key][0], None)
                tree_for_ordering = self.create_tree(pn_key_vals, max_depth=len(pn_keys))
            self.output_tree(self.current_entry, pn_keys + (pn,), tree_for_output, tree_for_ordering, compress=ordering_key is not None)
            output_names.discard(pn)
            output_names.difference_update(pn_keys)
            output_names.discard(ordering_key)

        return

    def output_unkeyed_values(self, straight_names, output_names):
        for sn in straight_names:
            if sn not in self.keyed_names:
                output_order = self._stored[sn][0]
            else:
                ordered_key = [ k[0] for k in self.domain_names.keys() if sn in self.domain_names[k] ][0]
                output_order, sort_order = self.create_index(self._stored[ordered_key][0], self._stored[sn][0])
                output_names.remove(ordered_key)
            if sn in self.get_single_names():
                self.current_entry.nxname = output_order[0]
            else:
                self.store_a_value(self.current_entry, sn, output_order, self._stored[sn][1], self._stored[sn][2])
            output_names.remove(sn)

    def output_file(self, filename):
        """Output a file containing the data units in self.all_entries"""
        root = nexus.NXroot()
        for one_entry, link_data in zip(self.all_entries, self.has_data):
            root.insert(one_entry)
            if link_data:
                main_data = one_entry.NXinstrument[0].NXdetector[0].data
                print 'Found main data at' + `main_data`
                data_link = nexus.NXdata()
                one_entry.data = data_link
                data_link.makelink(main_data)
                one_entry.data.nxsignal = one_entry.data.data

        root.save(filename)