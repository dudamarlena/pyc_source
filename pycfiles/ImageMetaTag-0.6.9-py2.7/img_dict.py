# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ImageMetaTag/img_dict.py
# Compiled at: 2017-12-06 07:34:27
"""
This submodule contains the :class:`ImageMetaTag.ImageDict` class, and functions for 
preparing instances of it.

The purpose of an :class:`ImageMetaTag.ImageDict` is to sort the image metadata, supplied to
:func:`ImageMetaTag.savefig` and usually stored in a database file, into a useful form that
can quickly and easily be presented as a webpage by :func:`ImageMetaTag.webpage.write_full_page`.

An easy example of creating a webpage, using an ImageDict is shown in
`simplest_image_dict.py <simple.html>`_

.. moduleauthor:: Malcolm Brooks https://github.com/malcolmbrooks

(C) Crown copyright Met Office. All rights reserved.
Released under BSD 3-Clause License. See LICENSE for more details.
"""
import os, re, collections, inspect, copy
from PIL import Image
import pdb
from copy import deepcopy
from itertools import islice, compress
from math import ceil

class ImageDict(object):
    """
    A class which holds a heirachical dictionary of dictionaries, and the associated
    methods for appending/removing dictionaries from it.

    The expected use case for the dictionary is to represent a large set of images,
    which can be organised by their metadata tags.

    When used in this way, the ImageDict module contains functions to produce web
    pages for browsing the images.

    The input_dict should be a heirachical dictionary of dictionaries, containing
    the image metadata, in the required order. In order to convert a flat dictionary
    of metadata items, use :func:`ImageMetaTag.dict_heirachy_from_list`

    Options:
     * level_names - a list of the tagnames, in full, giving a name/description of what                      the metadata item means. Ordered by level of the input dict.
     * selector_widths - a list of html strings giving the widths of each selector in the                          output webpage. CURRENTLY UNUSED!
     * selector_animated - an integer indicating which selector on the output webpage is                            to be animated.
     * animation_dicrection - +1 indicates the animation moves forwards, -1 indicates it                               moves backwards.

    Objects:
     * dict - the heirachical dictionary of dictionaries containing the image structure.
     * keys - a list of keys for each level of the dict, within a dictionary using the level               number as the keys.
     * level_names - If supplied, this stores the full names of the items in keys.
     * selector_animated - the level index which will be animated on the output webpage.
     * animation_direction - the direction of animation (+1 for forward, -1 for backward).
     * selector_widths - a list of desired widths on the output web page (CURRENTLY UNUSED).
    """

    def __init__(self, input_dict, level_names=None, selector_widths=None, selector_animated=None, animation_direction=None):
        if level_names is None:
            self.level_names = None
        elif not isinstance(level_names, list):
            msg = 'A mapping of key names to full names has been supplied, but it is not a list'
            raise ValueError(msg)
        else:
            self.level_names = level_names
        self.dict = input_dict
        self.list_keys_by_depth()
        dict_depth = self.dict_depth()
        if self.level_names is not None:
            if dict_depth != len(self.level_names):
                raise ValueError('Mismatch between depth of dictionary and level_names')
        if selector_widths is None:
            self.selector_widths = [
             ''] * dict_depth
        else:
            if not isinstance(selector_widths, list):
                msg = 'Specified selector_widths should be a list, but it is '
                msg += '"%s" instead' % selector_widths
                raise ValueError(msg)
            if len(selector_widths) != self.dict_depth():
                msg = 'Specified selector_widths length disagrees with the dictionary depth'
                raise ValueError(msg)
            self.selector_widths = selector_widths
        if selector_animated is None:
            self.selector_animated = -1
        else:
            if not isinstance(selector_animated, int):
                msg = 'Specified selector_animated should be a single integer'
                raise ValueError(msg)
            if selector_animated < -1 or selector_animated >= self.dict_depth():
                msg = 'selector_animated (%s)' % selector_animated
                msg += ' is out of range of the plot dictionary depth.'
                raise ValueError(msg)
            self.selector_animated = selector_animated
        if animation_direction is None:
            self.animation_direction = 1
        else:
            if not isinstance(animation_direction, int) or animation_direction != 1 and animation_direction != -1:
                msg = 'Specified animation_direction should be a single integer with values'
                msg += ' +1 or -1, but it is "%s" instead' % animation_direction
                raise ValueError(msg)
            self.animation_direction = animation_direction
        return

    def __repr__(self):
        outstr = 'ImageMetaTag ImageDict:\n'
        outstr = self.dict_print(self.dict, indent=1, outstr=outstr)
        return outstr

    def append(self, new_dict, devmode=False, skip_key_relist=False):
        """
        appends a new dictionary (with a single element in each layer!) into a current ImageDict.

        The skip_key_relist option can be set to True to stop the regeneration of key lists.
        """
        if isinstance(new_dict, ImageDict):
            merged_dict = dict(self.mergedicts(self.dict, new_dict.dict))
            self.dict = merged_dict
        elif isinstance(new_dict, dict):
            merged_dict = dict(self.mergedicts(self.dict, new_dict))
            self.dict = merged_dict
        else:
            raise ValueError('Cannot append data type %s to a ImageDict' % type(new_dict))
        if not skip_key_relist:
            self.list_keys_by_depth(devmode=devmode)
        if isinstance(new_dict, ImageDict) and self.level_names is not None:
            if new_dict.level_names is not None:
                if self.level_names != new_dict.level_names:
                    raise ValueError('Attempting to append two ImageDict objects with different level_names')
        return

    def dict_union(self, in_dict, new_dict):
        """produces the union of a dictionary of dictionaries"""
        for key, val in new_dict.iteritems():
            if not isinstance(val, dict):
                in_dict[key] = val
            else:
                subdict = in_dict.setdefault(key, {})
                self.dict_union(subdict, val)

    def mergedicts(self, dict1, dict2):
        """
        Alternative version of dict_union using generators which is much faster for large dicts
        but needs to be converted to a dict when it's called:
        new_dict = dict(mergdicts(dict1,dict))
        """
        for k in set(dict1.keys()).union(dict2.keys()):
            if k in dict1 and k in dict2:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    yield (
                     k, dict(self.mergedicts(dict1[k], dict2[k])))
                else:
                    yield (k, dict2[k])
            elif k in dict1:
                yield (
                 k, dict1[k])
            else:
                yield (
                 k, dict2[k])

    def remove(self, rm_dict, skip_key_relist=False):
        """
        removes a dictionary from within an ImageDict.
        The skip_key_relist option can be set to True to stop the regeneration of key lists.

        TIP: Because the remove process needs to prune empty sections afterwards,
        it can be slow. When working with large dictionaries, and removing a large number
        of elements from it, is often faster to build up a dictionary of things you want to
        remove, and then do one remove at the end.
        """
        if isinstance(rm_dict, ImageDict):
            self.dict_remove(self.dict, rm_dict.dict)
        else:
            if isinstance(rm_dict, dict):
                self.dict_remove(self.dict, rm_dict)
            else:
                raise ValueError('Cannot remove data type %s from a ImageDict' % type(rm_dict))
            dicts_to_prune = True
            while dicts_to_prune:
                dicts_to_prune = self.dict_prune(self.dict)

        if not skip_key_relist:
            self.list_keys_by_depth()

    def dict_remove(self, in_dict, rm_dict):
        """
        removes a dictionary of dictionaries from another, larger, one.
        This can leave empty branches, at multiple levels of the dict,
        so needs cleaning up afterwards.
        """
        for key, val in rm_dict.iteritems():
            if isinstance(val, dict):
                self.dict_remove(in_dict.setdefault(key, {}), val)
            elif key in in_dict.keys():
                in_dict.pop(key)

    def dict_prune(self, in_dict, dicts_pruned=False):
        """
        Prunes the ImageDict of empty, unterminated, branches
        (which occur after parts have been removed).
        Returns True if a dict was pruned, False if not.
        """
        pop_list = []
        for key, val in in_dict.iteritems():
            if isinstance(val, dict):
                if len(val.keys()) > 0:
                    dicts_pruned = self.dict_prune(val, dicts_pruned=dicts_pruned)
                else:
                    pop_list.append(key)
                    dicts_pruned = True
            elif val is None:
                pop_list.append(key)
                dicts_pruned = True

        for key in pop_list:
            in_dict.pop(key)

        return dicts_pruned

    def dict_print(self, in_dict, indent=0, outstr=''):
        """recursively details a dictionary of dictionaries, with indentation, to a string"""
        n_spaces = 2
        for key, value in in_dict.iteritems():
            outstr = '%s%s%s:\n' % (outstr, ' ' * indent * n_spaces, key)
            if isinstance(value, dict):
                outstr = self.dict_print(value, indent=indent + 1, outstr=outstr)
            else:
                outstr = '%s%s%s\n' % (outstr, ' ' * (indent + 1) * n_spaces, value)

        return outstr

    def dict_depth(self, uniform_depth=False):
        """
        Uses dict_depths to get the depth of all branches of the plot_dict and,
        if required, checks they all equal the max
        """
        dict_depths = [ d for d in self.flatten_lists(self.dict_depths(self.dict)) ]
        dict_depth = max(dict_depths)
        if uniform_depth:
            if len(set(dict_depths)) != 1:
                msg = 'Plot Dictionary has non uniform depth and uniform_depth=True is specified'
                raise ValueError(msg)
        return dict_depth

    def dict_depths(self, in_dict, depth=0):
        """Recursively finds the depth of a ImageDict and returns a list of lists"""
        if not isinstance(in_dict, dict) or not in_dict:
            return depth
        return [ self.dict_depths(next_dict, depth + 1) for next_key, next_dict in in_dict.iteritems() ]

    def flatten_lists(self, in_list):
        """Recursively flattens a list of lists:"""
        for list_element in in_list:
            if isinstance(list_element, collections.Iterable) and not isinstance(list_element, basestring):
                for sub_list in self.flatten_lists(list_element):
                    yield sub_list

            else:
                yield list_element

    def list_keys_by_depth(self, devmode=False):
        """
        Lists the keys of the dictionary to create a list of keys, for each level of the
        dictionary, up to its depth.

        It is usually much faster to create an ImageDict by appending images to it,
        with skip_key_relist=True but this leaves an ImageDict without a list of keys. In this
        case, list_keys_by_depth needs to be called once at the end of the process to complete
        the list of keys.

        It works by converting the sets, from keys_by_depth to a list (where they can be ordered
        and indexed).
        This also produces the unique subdirectory locations of all images.
        """
        keys, subdirs = self.keys_by_depth(self.dict)
        out_keys = {}
        for level in keys.keys():
            out_keys[level] = sorted(list(keys[level]))

        self.keys = out_keys
        self.subdirs = sorted(list(subdirs))

    def keys_by_depth(self, in_dict, depth=0, keys=None, subdirs=None):
        """
        Returns:

        * a dictionary of sets, containing the keys at each level of          the dictionary (keyed by the level number).
        * a set of the subdirectories for the target images
        """
        if keys is None:
            keys = {}
            subdirs = set([])
        if depth not in keys:
            keys[depth] = set()
        for key in in_dict:
            keys[depth].add(key)
            if isinstance(in_dict[key], dict):
                self.keys_by_depth(in_dict[key], depth + 1, keys, subdirs)
            elif isinstance(in_dict[key], list):
                for img_file in in_dict[key]:
                    subdirs.add(os.path.split(img_file)[0])

            elif isinstance(in_dict[key], str):
                subdirs.add(os.path.split(in_dict[key])[0])

        return (
         keys, subdirs)

    def key_at_depth(self, in_dict, depth):
        """returns the keys of a dictionary, at a given depth"""
        if depth > 0:
            return [ key for subdict in in_dict.itervalues() for key in self.key_at_depth(subdict, depth - 1) ]
        return in_dict.keys()

    def return_key_inds(self, in_dict, out_array=None, this_set_of_inds=None, depth=None, level=None, verbose=False, devmode=False):
        """
        Does the work for dict_index_array, by recursively adding indices to
        the keys to a current list, and branching where required, and adding
        compelted lists to the out_array
        """
        for key, value in in_dict.iteritems():
            if verbose:
                print 'IN: level: %s, before changes: %s, key "%s" in %s' % (
                 level, this_set_of_inds, key, self.keys[level])
            if isinstance(value, dict):
                if key in self.keys[level]:
                    this_set_of_inds[level] = self.keys[level].index(key)
                    if level + 1 < depth:
                        level += 1
                        if verbose:
                            print 'new setting: %s' % this_set_of_inds
                            print 'out_array: %s' % out_array
                        self.return_key_inds(value, out_array=out_array, this_set_of_inds=this_set_of_inds, depth=depth, level=level, devmode=devmode)
                    else:
                        out_array.append(deepcopy(this_set_of_inds))
                elif key in self.keys[(level - 1)]:
                    branched_level = deepcopy(level)
                    branched_set_of_inds = deepcopy(this_set_of_inds)
                    branched_set_of_inds[branched_level - 1] = self.keys[(branched_level - 1)].index(key)
                    if verbose:
                        print 'new setting: %s' % this_set_of_inds
                        print 'out_array: %s' % out_array
                    self.return_key_inds(value, out_array=out_array, this_set_of_inds=branched_set_of_inds, depth=depth, level=branched_level, devmode=devmode)
                else:
                    msg = 'Error recursing through dict: key "%s"' % key
                    msg += ' not found in this level, or one below'
                    raise ValueError(msg)
            else:
                if key in self.keys[level]:
                    this_set_of_inds[level] = self.keys[level].index(key)
                elif devmode:
                    pdb.set_trace()
                    print 'stop here'
                else:
                    msg = 'Error recursing through the plot dictionary: '
                    msg += 'key not found in top level!'
                    raise ValueError(msg)
                out_array.append(deepcopy(this_set_of_inds))

    def dict_index_array(self, devmode=False, maxdepth=None, verbose=False):
        """
        Using the list of dictionary keys (at each level of a uniform_depth dictionary
        of dictionaries), this produces a list of the indices that can be used to reference
        the keys to get the result for each element.

        Options:
         * maxdepth - the maximum desired depth to go to (ie. the number of levels)
        """
        out_array = []
        if maxdepth is None:
            depth = self.dict_depth(uniform_depth=True)
            this_set_of_inds = [None] * depth
        else:
            depth = maxdepth
            this_set_of_inds = [None] * depth
        level = 0
        self.return_key_inds(self.dict, out_array=out_array, this_set_of_inds=this_set_of_inds, depth=depth, level=level, devmode=devmode, verbose=verbose)
        out_array.sort()
        return (
         self.keys, out_array)

    def sort_keys(self, sort_methods, devmode=False):
        """
        Sorts the keys of a plot dictionary, according to a particular sort method
        (or a list of sort methods that matches the number of keys).

        Valid sort methods so far are mostly focused on meteorological terms, and include:
         * 'sort' - just an ordinary sort
         * 'level' or 'numeric' - starting with the surface and working upwards, then                                   'special' levels like cross sections etc.
         * 'T+' - in ascending order of the number after a T+ (or similar) string.
         * an input list - Specific elements in the input list are sorted as per their order                           in the list, while the rest are just sorted.

        The methods activated by a string can be reversed as 'reverse_sort' or 'reverse_sort',
        or 'reverse numeric' or 'reverse_numeric'.
        """
        if len(sort_methods) != len(self.keys):
            raise ValueError('inconsistent lengths of the sort_methods and the self.keys to sort')
        for i_key, method in enumerate(sort_methods):
            if isinstance(method, str):
                if method in ('sort', 'alphabetical'):
                    self.keys[i_key].sort()
                elif method in ('reverse sort', 'reverse_sort'):
                    self.keys[i_key].sort(reverse=True)
                elif method in ('T+', 'reverse T+', 'reversed_T+'):
                    try:
                        labels_and_values = [ (x, re.match('[tT][+]{,}([0-9.]{1,})|None', x).group(1)) for x in self.keys[i_key] ]
                        if method == 'T+':
                            labels_and_values = [ (x, float(y)) if y is not None else (x, 'None') for x, y in labels_and_values ]
                        elif method in ('reverse T+', 'reversed_T+'):
                            labels_and_values = [ (x, float(y)) if y is not None else (x, y) for x, y in labels_and_values ]
                    except:
                        msg = 'Keys for plot dictionary level "%s" ' % self.keys[i_key]
                        msg += 'do not match the "T+" (or None) pattern'
                        if devmode:
                            print msg
                            pdb.set_trace()
                            print 'stop'
                        else:
                            raise ValueError(msg)

                    if method == 'T+':
                        labels_and_values.sort(key=lambda x: x[1])
                    elif method in ('reverse T+', 'reversed_T+'):
                        labels_and_values.sort(key=lambda x: x[1], reverse=True)
                    self.keys[i_key] = [ x[0] for x in labels_and_values ]
                elif method in ('level', 'numeric', 'reverse_level', 'reverse_numeric'):
                    tmp_keys = []
                    surface_levels = [
                     'Surface']
                    for item in surface_levels:
                        if item in self.keys[i_key]:
                            tmp_keys.append(self.keys[i_key].pop(self.keys[i_key].index(item)))
                        if len(self.keys[i_key]) == 0:
                            break

                    metre_patterns_and_scalings = [
                     ('([0-9.eE+-]{1,})[\\s]{,}m$', 1.0),
                     (
                      '([0-9.eE+-]{1,})[\\s]{,}mm$', -2.0),
                     (
                      '([0-9.eE+-]{1,})[\\s]{,}microns$', -5.0),
                     (
                      '([0-9.eE+-]{1,})[\\s]{,}\\mum$', -5.0),
                     ('([0-9.eE+-]{1,})[\\s]{,}nm$', 1e-09),
                     ('([0-9.eE+-]{1,})[\\s]{,}km$', 1000.0)]
                    pressure_patterns_and_scalings = [
                     ('([0-9.eE+-]{1,})[\\s]{,}Pa$', 1.0),
                     ('([0-9.eE+-]{1,})[\\s]{,}mb$', 100.0),
                     ('([0-9.eE+-]{1,})[\\s]{,}mbar$', 100.0),
                     ('([0-9.eE+-]{1,})[\\s]{,}hPa$', 100.0)]
                    model_lev_patterns_and_scalings = [
                     ('Model level ([0-9]{1,})', 1.0),
                     ('model level ([0-9]{1,})', 1.0),
                     ('Model lev ([0-9]{1,})', 1.0),
                     ('model level ([0-9]{1,})', 1.0),
                     ('ML([0-9]{1,})', 1.0),
                     ('ml([0-9]{1,})', 1.0)]
                    lattlong_patterns_and_scalings = [
                     ('([0-9.]{1,})[E][,\\s]{,}[0-9.]{1,}[NS]', 1.0),
                     ('([0-9.]{1,})[W][,\\s]{,}[0-9.]{1,}[NS]', -1.0)]
                    numeric_patterns_and_scalings = [
                     ('([0-9.eE+-]{1,})', 1.0)]
                    if method.startswith('reverse'):
                        pattern_order_loop = [
                         (
                          metre_patterns_and_scalings, 'reversed'),
                         (
                          pressure_patterns_and_scalings, 'sort'),
                         (
                          model_lev_patterns_and_scalings, 'reversed'),
                         (
                          lattlong_patterns_and_scalings, 'reversed'),
                         (
                          numeric_patterns_and_scalings, 'reversed')]
                    else:
                        pattern_order_loop = [
                         (
                          metre_patterns_and_scalings, 'sort'),
                         (
                          pressure_patterns_and_scalings, 'reversed'),
                         (
                          model_lev_patterns_and_scalings, 'sort'),
                         (
                          lattlong_patterns_and_scalings, 'sort'),
                         (
                          numeric_patterns_and_scalings, 'sort')]
                    for patterns_scalings, sort_method in pattern_order_loop:
                        labels_and_values = []
                        for item in self.keys[i_key]:
                            for pattern, scaling in patterns_scalings:
                                item_match = re.match(pattern, item)
                                if item_match:
                                    if devmode:
                                        try:
                                            _ = float(item_match.group(1)) * scaling
                                        except:
                                            pdb.set_trace()
                                            print 'unable to convert item "%s" with pattern "%s" to float' % (item, pattern)

                                    labels_and_values.append((item, float(item_match.group(1)) * scaling))
                                    break

                        if sort_method == 'sort':
                            labels_and_values.sort(key=lambda x: x[1])
                        else:
                            if sort_method == 'reversed':
                                labels_and_values.sort(key=lambda x: x[1], reverse=True)
                            else:
                                raise ValueError('Unrecognised sort_method "%s"' % sort_method)
                            for item, scaling in labels_and_values:
                                tmp_keys.append(item)
                                self.keys[i_key].pop(self.keys[i_key].index(item))

                    self.keys[i_key].sort()
                    self.keys[i_key] = tmp_keys + self.keys[i_key]
            elif isinstance(method, list):
                tmp_keys = []
                for item in method:
                    if item in self.keys[i_key]:
                        tmp_keys.append(self.keys[i_key].pop(self.keys[i_key].index(item)))
                    if len(self.keys[i_key]) == 0:
                        break

                self.keys[i_key].sort()
                self.keys[i_key] = tmp_keys + self.keys[i_key]

        return

    def copy_except_dict_and_keys(self):
        """returns a copy of an ImageDict except it will have null values for the dict and keys"""
        out_imgdict = ImageDict({'null': None})
        for mem_name, mem_value in inspect.getmembers(self):
            if mem_name.startswith('__'):
                pass
            elif mem_name in ('dict', 'keys'):
                pass
            elif inspect.ismethod(eval('self.%s' % mem_name)):
                pass
            else:
                setattr(out_imgdict, mem_name, mem_value)

        return out_imgdict

    def return_from_list(self, vals_at_depth):
        """
        Returns the end values of ImageDict, when given a list of values for the keys
        at different depths.
        Returns None if the set of values is not contained in the ImageDict.

        Assumes that the ImageDict has its keys up to date, so last time it was
        appended/removed it was with skip_key_relist=False   or  list_keys_by_depth()
        method has been called since.
        """
        if not isinstance(vals_at_depth, list):
            raise ValueError('Input vals_at_depth should be a list')
        dict_depth = len(self.keys)
        if len(vals_at_depth) > dict_depth:
            msg = 'Length of input list, vals_at_depth, greater than the length of the keys list'
            raise ValueError(msg)
        if vals_at_depth[0] not in self.keys[0]:
            return
        else:
            sub_dict = self.dict[vals_at_depth[0]]
            for depth in range(1, len(vals_at_depth)):
                if vals_at_depth[depth] in sub_dict:
                    sub_dict = sub_dict[vals_at_depth[depth]]
                else:
                    return

            return sub_dict


def readmeta_from_image(img_file, img_format=None):
    """Reads the metadata added by the ImageMetaTag savefig, from an image file,
    and returns a dictionary of *tagname: value* pairs"""
    if img_format is None:
        _, img_format = os.path.splitext(img_file)
        if img_format is None or img_format == '':
            msg = 'Cannot determine file img_format to read from filename "%s"' % img_file
            raise ValueError(msg)
        img_format = img_format[1:]
    elif img_format.startswith('.'):
        img_format = img_format[1:]
    if img_format == 'png':
        try:
            img_obj = Image.open(img_file)
            img_info = img_obj.info
            read_ok = True
        except:
            read_ok = False
            img_info = None

    else:
        msg = 'Currently, ImageMetaTag does not support "%s" format images' % img_format
        raise NotImplementedError(msg)
    return (read_ok, img_info)


def dict_heirachy_from_list(in_dict, payload, heirachy):
    """
    Converts a flat dictionary of *tagname: value* pairs, into an ordered dictionary
    of dictionaries according to the input heirachy (which is a list of tagnames).

    The output dictionary will only have one element per level, but can be used to create or
    append into an :class:`ImageMetaTag.ImageDict`.
    The final level will be the 'payload' input, which is the object the dictionary, with all
    it's levels, is describing.
    The payload would usually be the full/relative path of the image file, or list of image files.

    Returns False if the input dict does not contain the required keys.
    """
    for level in heirachy:
        if level not in in_dict.keys():
            return False

    out_dict = {in_dict[heirachy[(-1)]]: payload}
    for level in heirachy[-2::-1]:
        out_dict = {in_dict[level]: out_dict}

    return out_dict


def dict_split(in_dict, n_split=None, size_split=None, extra_opts=None):
    """
    Generator that breaks up a flat dictionary and yields a set of sub-dictionaries in
    n_split chunks, or size_split in size. It is split on it's first level, not recursively.

    It is very useful for splitting large dictionaries of image metadata
    to parallelise processing these into ImageDicts.

    Inputs:
    in_dict - the dictionary to split

    Options:

    * n_split - the number of dictionaries to break the in_dict up into.
    * size_split - the size of the required output dictionaries.
    * extra_opts - If supplied as an iterable, this routine will yield a tuple containing the                    output sub-dictionary and then each of the elements of extra_opts.

    .. note:: One, and only one, of n_slpit, or size_split must be specified, as an integer.

    """
    if not isinstance(in_dict, dict):
        raise ValueError('Input in_dict is not a dictionary')
    if len(in_dict) == 0:
        out_dict = {}
        if extra_opts is None:
            yield out_dict
        else:
            out_tuple = (out_dict,)
            for opt in extra_opts:
                out_tuple = out_tuple + (opt,)

            yield out_tuple
    elif size_split is None and isinstance(n_split, int):
        if n_split < 1:
            raise ValueError('Cannot split a dictionary into less than 1 dictionary')
        size_split = int(ceil(len(in_dict) / float(n_split)))
    else:
        if isinstance(size_split, int) and n_split is None:
            pass
        else:
            msg = 'One, and only one, of n_slpit, or size_split must be specified, as an integer.'
            raise ValueError(msg)
        iterdict = iter(in_dict)
        for i in xrange(0, len(in_dict), size_split):
            out_dict = {k:in_dict[k] for k in islice(iterdict, size_split)}
            if extra_opts is None:
                yield out_dict
            else:
                out_tuple = (out_dict,)
                for opt in extra_opts:
                    out_tuple = out_tuple + (opt,)

                yield out_tuple

    return


def simple_dict_filter(simple_dict, tests, raise_key_mismatch=False):
    """
    Tests the contents of a simple, un-heirachical dict (properties an image) against
    a set of tests.

    An example set of tests:
    tests = {'number of rolls': ['6 simulated rolls', '216 simulated rolls', '1296 simulated rolls'],             'plot color': None,             'image compression': None,             'plot type': ['Histogram', ('All', ['Histogram', 'Line plots'])],             'image trim': None}
    Here, the 'number of rolls' is restricted to a simple list.

    The plot type is filtered according to 'Histogram', and there is also a second element that
    contains both 'Histogram and 'Line plots' which are to be presented together.

    The other image characteristics are not filtered.

    Options:

    * raise_key_mismatch - if True, then attempting to test a dictionary with a missing key                            will raise. Default is to return all False

    Returns three logicals:

    * The first indicates whether the input dict passes the simple tests
    * The second indicates whether the input dict is part of the grouped elements       of the test (the ['Histogram', 'Line plots'] list).#
    * The third indicates whether the input dict is the first element of a list grouped       elements (is 'Histogram' in this ['Histogram', 'Line plots'] list).

    """
    passes_tests = True
    passes = [
     True] * len(tests)
    passes_and_first = [
     True] * len(tests)
    has_complex_test = False
    if tests is not None:
        for i_test, test in enumerate(tests.keys()):
            if tests[test] is None:
                pass
            else:
                if test not in simple_dict.keys():
                    msg = 'Specified filter test "{}" not a property of the input dict "{}"'
                    if raise_key_mismatch:
                        raise ValueError(msg.format(test, simple_dict))
                    else:
                        print msg.format(test, simple_dict)
                        return (False, False, False)
                if isinstance(tests[test], list):
                    test_is_tuple = [ isinstance(x, tuple) for x in tests[test] ]
                    if any(test_is_tuple):
                        has_complex_test = True
                        any_tuple_passes = False
                        first_tuple_passes = False
                        tuple_tests = compress(tests[test], test_is_tuple)
                        for tuple_test in tuple_tests:
                            if simple_dict[test] in tuple_test[1]:
                                any_tuple_passes = True
                            if simple_dict[test] == tuple_test[1][0]:
                                first_tuple_passes = True

                        if not any_tuple_passes:
                            passes[i_test] = False
                            passes_and_first[i_test] = False
                        elif not first_tuple_passes:
                            passes_and_first[i_test] = False
                        if simple_dict[test] not in tests[test]:
                            passes_tests = False
                    elif simple_dict[test] not in tests[test]:
                        passes_tests = False
                        passes[i_test] = False
                        passes_and_first[i_test] = False
                else:
                    msg = 'Test values should be specified as lists'
                    raise ValueError(msg)

    if has_complex_test:
        passes_complex_test = all(passes)
        passes_and_first = all(passes_and_first)
    else:
        passes_complex_test = False
        passes_and_first = False
    return (passes_tests, passes_complex_test, passes_and_first)


def check_for_required_keys(img_info, req_keys):
    """
    Checks an img_info dictionary has a set of required keys, specifed as a list of strings

    Returns True or False accordingly.
    """
    for key in req_keys:
        if key not in img_info.keys():
            return False

    return True