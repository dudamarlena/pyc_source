# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/geometry.py
# Compiled at: 2019-04-18 15:00:47
# Size of source mod 2**32: 30201 bytes
"""
Part of beampy project.

Placement class for relative placement of elements in slides
"""
from beampy.functions import dict_deep_update, convert_unit
from beampy.document import document
import operator, sys
DEFAULT_X = {'align': 'left', 'reference': 'slide', 'shift': 0, 
 'unit': 'width', 'anchor': 'left'}
DEFAULT_Y = {'align': 'top', 'reference': 'slide', 'shift': 0, 
 'unit': 'width', 'anchor': 'top'}

def center(shift=0):
    out = {'anchor': 'middle', 'shift': shift}
    if isinstance(shift, str):
        out['shift'] = float(convert_unit(shift))
        out['unit'] = 'px'
    return out


def top(shift=0):
    out = {'anchor': 'top', 'shift': shift}
    if isinstance(shift, str):
        out['shift'] = float(convert_unit(shift))
        out['unit'] = 'px'
    return out


def bottom(shift=0):
    out = {'anchor': 'bottom', 'shift': shift}
    if isinstance(shift, str):
        out['shift'] = float(convert_unit(shift))
        out['unit'] = 'px'
    return out


def right(shift=0):
    out = {'anchor': 'right', 'shift': shift}
    if isinstance(shift, str):
        out['shift'] = float(convert_unit(shift))
        out['unit'] = 'px'
    return out


class positionner:

    def __init__(self, x, y, width, height, elem_id, slideid):
        """
            This class need position x and y of the element

            width and height is the size of the svg or html object (need to be
            updated after rendering)

            x, y: could be a dict, a float or a string

            Default position dict:
            ======================

                {'align': 'left', 'reference': 'slide', 'shift': 0, 'unit': 'rel'}

                align: define the alignement for the coordinate
                       ('center' (page centering),'left','right','middle',
                       'top','bottom')
                reference: 'relative' element for placement or 'slide' relative to slide
                           'slide' for placement refenreced on slide
                shift: the value of the shift
                unit: 'width': relative to page (or group) width
                      'height': relative to page (or group) height
                      'cm', 'pt', 'px': shift value unit
                anchor: 'left', 'right', 'middle', 'top', 'bottom', define the anchor on the object bounding-box
        """
        self.id = elem_id
        self.slideid = slideid
        try:
            self.id_index = document._slides[self.slideid].element_keys.index(self.id)
        except IndexError:
            print('Element not found in document._content[gcs()].element_keys')
            print('Positionner set for elem: %s in slide: %s' % (self.id, self.slideid))
            self.id_index = -1
            sys.exit(1)

        self.width = Length(self.id, self.slideid)
        self.height = Length(self.id, self.slideid)
        self.update_size(width, height)
        if isinstance(x, dict):
            self.x = x.copy()
        else:
            self.x = x
        if isinstance(y, dict):
            self.y = y.copy()
        else:
            self.y = y
        self.convert_position()
        self.compute_anchors()

    def update_x(self, x):
        """
        Update the x position and run the converter
        """
        if isinstance(x, dict):
            self.x = x.copy()
        else:
            self.x = x
        self.convert_position()

    def update_y(self, y):
        """
        Update the y position and run the converter
        """
        if isinstance(y, dict):
            self.y = y.copy()
        else:
            self.y = y
        self.convert_position()

    def update_size(self, width, height):
        """
            Update width and height to computed ones by the element render.

            If width is less than 1px, use it as a percentage of the width
        """
        if isinstance(width, Length):
            if width.value is None:
                width.run_render()
            width = width.value
        if isinstance(height, Length):
            if height.value is None:
                height.run_render()
            height = height.value
        if isinstance(width, str):
            if '%' in width:
                ratio = float(width.replace('%', '')) / 100.0
                width = document._slides[self.slideid].curwidth * ratio
        else:
            width = float(convert_unit(width))
        if isinstance(height, str):
            if '%' in height:
                ratio = float(height.replace('%', '')) / 100.0
                height = document._slides[self.slideid].curheight * ratio
        else:
            height = float(convert_unit(height))
        if width is not None and width < 1:
            ratio = width / 100.0
            width = document._slides[self.slideid].curwidth * ratio
        if height is not None and height < 1:
            ratio = height / 100.0
            height = document._slides[self.slideid].curheight * ratio
        self.width.value = width
        self.height.value = height

    def compute_anchors(self):
        """
            Compute the anchors for the element self.left self.right self.top and self.bottom
        """
        self.bottom = anchor('bottom', self.id, self.slideid)
        self.top = anchor('top', self.id, self.slideid)
        self.left = anchor('left', self.id, self.slideid)
        self.right = anchor('right', self.id, self.slideid)
        self.center = anchor('center', self.id, self.slideid)

    def convert_position(self):
        tmpx = DEFAULT_X.copy()
        tmpy = DEFAULT_Y.copy()
        slidects = document._slides[self.slideid].contents
        if self.id_index > 0:
            prev_ct = slidects[document._slides[self.slideid].element_keys[(self.id_index - 1)]]
        else:
            prev_ct = None
        if isinstance(self.x, float) or isinstance(self.x, int):
            tmpx['shift'] = self.x
        else:
            if isinstance(self.x, dict):
                tmpx = dict_deep_update(tmpx, self.x)
            else:
                if isinstance(self.x, str):
                    converted = False
                    if '+' in self.x:
                        newx = convert_unit(self.x.replace('+', ''))
                        if prev_ct is not None:
                            dict_old = prev_ct.positionner.right + newx
                            tmpx = dict_deep_update(tmpx, dict_old)
                        else:
                            tmpx['shift'] = newx
                        tmpx['unit'] = 'px'
                        converted = True
                    if '-' in self.x:
                        newx = convert_unit(self.x.replace('-', ''))
                        if prev_ct is not None:
                            dict_old = prev_ct.positionner.left - newx
                            tmpx = dict_deep_update(tmpx, dict_old)
                        else:
                            tmpx['shift'] = newx
                        tmpx['unit'] = 'px'
                        converted = True
                    if self.x in ('auto', 'center'):
                        tmpx['shift'] = 0
                        tmpx['align'] = self.x
                        converted = True
                    if not converted:
                        try:
                            tmpx['shift'] = float(convert_unit(self.x))
                            tmpx['unit'] = 'px'
                        except:
                            print('[Error] x position is incorect string format')
                            print(self.x)

                else:
                    if isinstance(self.x, Length):
                        if self.x.value is None:
                            self.x.run_render()
                        tmpx['shift'] = self.x.value
                        tmpx['unit'] = 'px'
                    else:
                        print('[Error] x position need to be a float or a dict')
                    if isinstance(self.y, float) or isinstance(self.y, int):
                        tmpy['shift'] = self.y
                    else:
                        if isinstance(self.y, dict):
                            tmpy = dict_deep_update(tmpy, self.y)
                        else:
                            if isinstance(self.y, str):
                                converted = False
                                if '+' in self.y:
                                    newy = convert_unit(self.y.replace('+', ''))
                                    if prev_ct is not None:
                                        dict_old = prev_ct.positionner.bottom + newy
                                        tmpy = dict_deep_update(tmpy, dict_old)
                                    else:
                                        tmpy['shift'] = newy
                                    tmpy['unit'] = 'px'
                                    converted = True
                                if '-' in self.y:
                                    newy = convert_unit(self.y.replace('-', ''))
                                    if prev_ct is not None:
                                        dict_old = prev_ct.positionner.top - newy
                                        tmpy = dict_deep_update(tmpy, dict_old)
                                    else:
                                        tmpy['shift'] = newy
                                    tmpy['unit'] = 'px'
                                    converted = True
                                if self.y in ('auto', 'center'):
                                    tmpy['shift'] = 0
                                    tmpy['align'] = self.y
                                    converted = True
                                if not converted:
                                    try:
                                        tmpy['shift'] = convert_unit(self.y)
                                        tmpy['unit'] = 'px'
                                    except:
                                        print('[Error] y position is incorect string format')
                                        print(self.y)

                            else:
                                if isinstance(self.y, Length):
                                    if self.y.value is None:
                                        self.y.run_render()
                                    tmpy['shift'] = self.y.value
                                    tmpy['unit'] = 'px'
                                else:
                                    print('[Error] y position need to be a float or an int or a dict')
        self.x = tmpx
        self.y = tmpy
        if self.x['shift'] > 1.0 and self.x['unit'] in ('width', 'height'):
            self.x['unit'] = 'px'
        if self.y['shift'] > 1.0 and self.y['unit'] in ('width', 'height'):
            self.y['unit'] = 'px'
        if self.x['unit'] in ('cm', 'pt', 'mm'):
            self.x['shift'] = float(convert_unit('%f%s' % (self.x['shift'], self.x['unit'])))
        if self.y['unit'] in ('cm', 'pt', 'mm'):
            self.y['shift'] = float(convert_unit('%f%s' % (self.y['shift'], self.y['unit'])))

    def place(self, available_size, ytop=0):
        """
            Method to place the given element. This method is used by renders.py in
            the place_content function

            available_size: (width, heith) is the page or group width and height

            ytop[default 0]: is the y offset (used to center verticaly taking into
                             account the title)

        """
        available_width, available_height = available_size
        if available_width is not None:
            if self.x['unit'] == 'width':
                self.x['shift'] *= available_width
            if self.y['unit'] == 'width':
                self.y['shift'] *= available_width
        if available_height is not None:
            if self.x['unit'] == 'height':
                self.x['shift'] *= available_height
            if self.y['unit'] == 'height':
                self.y['shift'] *= available_height
        if self.x['align'] == 'center':
            self.x['final'] = element_centering(self.width.value, available_width) + self.x['shift']
        if self.y['align'] == 'center':
            self.y['final'] = element_centering(self.height.value, available_height - ytop, pos_init=ytop) + self.y['shift']
        if self.x['reference'] == 'slide':
            if self.x['align'] == 'left':
                self.x['final'] = self.x['shift']
            if self.x['align'] == 'right':
                self.x['final'] = available_width - self.x['shift']
            if self.x['align'] == 'middle':
                self.x['final'] = self.x['shift'] + self.width.value / 2.0
        if self.y['reference'] == 'slide':
            if self.y['align'] == 'top':
                self.y['final'] = self.y['shift']
            if self.y['align'] == 'bottom':
                self.y['final'] = available_height - self.y['shift']
            if self.y['align'] == 'middle':
                self.y['final'] = self.y['shift'] + self.height.value / 2.0
        if self.x['reference'] == 'relative':
            self.x['final'] = relative_placement(self.x['ref_id'], self.x, 'x')
        if self.y['reference'] == 'relative':
            self.y['final'] = relative_placement(self.y['ref_id'], self.y, 'y')
        self.x['final'] = round(self.x['final'], 1)
        self.y['final'] = round(self.y['final'], 1)
        if self.x['anchor'] == 'right':
            self.x['final'] -= self.width.value
        if self.x['anchor'] == 'middle':
            self.x['final'] -= self.width.value / 2.0
        if self.y['anchor'] == 'bottom':
            self.y['final'] -= self.height.value
        if self.y['anchor'] == 'middle':
            self.y['final'] -= self.height.value / 2.0

    def guess_size_for_group(self):
        """Function to guess parent group final position to place elements relatively
        to this group.
        """
        if 'final' not in self.x:
            if self.width.value is None:
                cur_width = document._slides[self.slideid].curwidth
                print('Warning: Relative "x" placement to parent group without\n                width could gives unexpected results. Width: %i is used.' % cur_width)
                self.width = Length(self.id, self.slideid, cur_width)
            if self.x == 'auto':
                print('Warning: Relative "x" placement to a parent group with\n                auto-positioning! This will lead to unexpected results!')
            if 'final' not in self.y:
                if self.height.value is None:
                    cur_height = document._height
                    print('Warning: Relative "y" placement to parent group without\n                width could gives unexpected results. Width: %i is used.' % cur_height)
                    self.height = Length(self.id, self.slideid, cur_height)
                if self.y == 'auto':
                    print('Warning: Relative "y" placement to a parent group with\n                auto-positioning! This will lead to unexpected results!')


class anchor:

    def __init__(self, atype, elem_id, slide_id):
        """
            Define the anchor class:
            atype [top, left, bottom, center]
            elem_id the id of the current element
        """
        self.type = atype
        self.element_id = elem_id
        self.slide_id = slide_id
        self.position = {'reference': 'relative', 
         'ref_id': (self.element_id, self.slide_id), 
         'ref_anchor': self.type}

    def __add__(self, new_value):
        self.position['math'] = '+'
        self.parse_newvalue(new_value)
        return self.position.copy()

    def __sub__(self, new_value):
        self.position['math'] = '-'
        self.parse_newvalue(new_value)
        return self.position.copy()

    def parse_newvalue(self, new_value):
        """
            New_value can be a string like "+5cm" or a float 0.4 or a new dict
            like {"shift": 0, "align": 'left'}
        """
        if isinstance(new_value, str):
            self.position['shift'] = float(convert_unit(new_value))
            self.position['unit'] = 'px'
        else:
            if isinstance(new_value, float) or isinstance(new_value, int):
                self.position['shift'] = new_value
            else:
                if isinstance(new_value, dict):
                    self.position = dict_deep_update(new_value.copy(), self.position)
                else:
                    if isinstance(new_value, Length):
                        new_value.process_value()
                        self.position['shift'] = float(new_value.value)
                        self.position['unit'] = 'px'
                    else:
                        print('Invalid relative coordinate type!')


def element_centering(object_size, container_size, pos_init=0):
    """
        Function to center and object on the container_size

        final position:
            pos_init + available_space/2
    """
    if container_size > object_size:
        available_space = container_size - object_size
        pos_new = pos_init + available_space / 2
    else:
        pos_new = pos_init
    return pos_new


def relative_placement(prev_element_id, curpos, axis):
    """
        Compute relative placement

        return final position on the given axis
    """
    prev_elem, prev_slide = prev_element_id
    if curpos['math'] == '-':
        op = operator.sub
    else:
        op = operator.add
    if axis == 'x':
        try:
            oldpos = document._slides[prev_slide].contents[prev_elem].positionner.x
        except KeyError as e:
            print('Reference to element error')
            print(e)
            print('Slide %s' % prev_slide)
            print(document._slides[prev_slide].contents)
            sys.exit(1)

    if axis == 'y':
        try:
            oldpos = document._slides[prev_slide].contents[prev_elem].positionner.y
        except KeyError as e:
            print('Reference to element error')
            print(e)
            print('Slide %s' % prev_slide)
            print(document._slides[prev_slide].contents)
            sys.exit(1)

    if 'final' not in oldpos:
        if document._slides[prev_slide].contents[prev_elem].type == 'group':
            oldpos_final = 0
            document._slides[prev_slide].contents[prev_elem].positionner.guess_size_for_group()
        else:
            raise ValueError('Relative placement error: \nReference element:\n%s\nThis element have no final position' % str(document._slides[prev_slide].contents[prev_elem]))
    else:
        oldpos_final = oldpos['final']
    oldwidth = document._slides[prev_slide].contents[prev_elem].positionner.width
    if oldwidth.value is None:
        oldwidth.run_render()
    oldwidth = oldwidth.value
    oldheight = document._slides[prev_slide].contents[prev_elem].positionner.height
    if oldheight.value is None:
        oldheight.run_render()
    oldheight = oldheight.value
    if curpos['ref_anchor'] == 'left':
        if axis == 'x':
            newpos = op(oldpos_final, curpos['shift'])
    else:
        print('left anchor only works for x coordinate')
        sys.exit(1)
    if curpos['ref_anchor'] == 'right':
        if axis == 'x':
            newpos = op(oldpos_final + oldwidth, curpos['shift'])
    else:
        print('right anchor only works for x coordinate')
        sys.exit(1)
    if curpos['ref_anchor'] == 'center':
        if axis == 'x':
            newpos = op(oldpos_final + oldwidth / 2.0, curpos['shift'])
        if axis == 'y':
            newpos = op(oldpos_final + oldheight / 2.0, curpos['shift'])
    if curpos['ref_anchor'] == 'top':
        if axis == 'y':
            newpos = op(oldpos_final, curpos['shift'])
    else:
        print('top anchor only works for y coordinate')
        sys.exit(1)
    if curpos['ref_anchor'] == 'bottom':
        if axis == 'y':
            newpos = op(oldpos_final + oldheight, curpos['shift'])
    else:
        print('bottom anchor only works for y coordinate')
        sys.exit(1)
    return newpos


def align(positionner_list, alignement):
    """
        Function to align all given elements defined by their positionner.

        alignement:

        'left': align left
        'right': align right
        'xcenter': align center (verticaly)
        'ycenter': align center (horizontaly)
        'baseline': if all elements are text align their baseline
        'top': align top
        'bottom': align bottom

    """
    print('TODO')


def distribute(element_list, mode, available_size, offset=0, curslide=None):
    """
        Distribute the given elements list along the slide using the given
        mode

        element_list:
            A list of beampy module (if curslide is none)
            A list of beampy module keys, in this case curslide must be the
            curent slide where module are stored

        mode:
            'hspace': horizontal spacing from the center of each elements
            'vspace': vertical spacing from the center of each elements

        offset:
            gives the first offset of the slide (due to the title for instance)

        curslide [None]:
            If curslide is not None the element_list must refers to elements keys
            surch that

            curslide.content[elemnt_list[0]] is a beampy module

    """
    if mode == 'vspace':
        if curslide is None:
            all_height = [elem.positionner.height for elem in element_list]
        else:
            all_height = [curslide.contents[elemk].positionner.height for elemk in element_list]
        sumheight = 0
        for h in all_height:
            sumheight = h + sumheight

        sumheight = sumheight.value
        if sumheight > available_size:
            print('Warning alignement elements overflow given height %s' % available_size)
        available_space = available_size - offset - sumheight
        dy = available_space / float(len(all_height) + 1)
        curpos = dy + offset
        for elemt in element_list:
            if curslide is None:
                elem = elemt
            else:
                elem = curslide.contents[elemt]
            H = elem.positionner.height.value
            elem.positionner.y['shift'] = curpos
            elem.positionner.y['unit'] = 'px'
            elem.positionner.y['align'] = 'top'
            curpos += dy + H

    elif mode == 'hspace':
        if curslide is None:
            all_width = [elem.positionner.width for elem in element_list]
        else:
            all_width = [curslide.contents[elemk].positionner.width for elemk in element_list]
        sumwidth = 0
        for w in all_width:
            sumwidth = w + sumwidth

        sumwidth = sumwidth.value
        if sumwidth > available_size:
            print('Warning alignement elements overflow given width %s' % available_size)
        available_space = available_size - offset - sumwidth
        dx = available_space / float(len(all_width) + 1)
        curpos = dx + offset
        for elemt in element_list:
            if curslide is None:
                elem = elemt
            else:
                elem = curslide.contents[elemt]
            W = elem.positionner.width.value
            elem.positionner.x['shift'] = curpos
            elem.positionner.x['unit'] = 'px'
            elem.positionner.x['align'] = 'left'
            curpos += dx + W


class Length(object):
    __doc__ = "Define the length for complexe operation. \n\n    Allow operation like None + '12cm', where None will be transformed to the elem_id Length \n    (render the module to get his size) and convert the '12cm' to pixels.\n\n    Parameters:\n    -----------\n\n    elem_id, str:\n        the id of the beampy module for which the length apply\n\n    slide_id, str:\n        the id of the slide where the module is registered\n\n    "

    def __init__(self, elem_id, slide_id, value=None):
        self.elem_id = elem_id
        self.slide_id = slide_id
        self.value = value

    def run_render(self):
        elem = document._slides[self.slide_id].contents[self.elem_id]
        if elem.type == 'group':
            print('Render group to get its size')
            for gelem_id in elem.elementsid:
                gelem = document._slides[self.slide_id].contents[gelem_id]
                if gelem.rendered is False:
                    print('Need to render elem %s in group to get its size' % gelem.name)
                    gelem.pre_render()
                    gelem.run_render()

            elem.compute_group_size()
        else:
            print('Run render to get length of %s' % elem.name)
            if elem.rendered is False:
                elem.pre_render()
                elem.run_render()
            assert elem.width.value is not None
            if not elem.height.value is not None:
                raise AssertionError

    def process_value(self):
        if self.elem_id is not None and self.slide_id is not None and self.value is None:
            self.run_render()
        if isinstance(self.value, str):
            self.value = float(convert_unit(self.value))

    @staticmethod
    def process_right_value(right_value):
        """
        Process the right value of the operation (could be another element Length or string with length + unit or pixels)
        """
        if isinstance(right_value, Length):
            if right_value.value is None:
                right_value.run_render()
            tmp_rvalue = float(right_value.value)
        if isinstance(right_value, str):
            tmp_rvalue = float(convert_unit(right_value))
        if isinstance(right_value, float) or isinstance(right_value, int):
            tmp_rvalue = float(right_value)
        return tmp_rvalue

    def __add__(self, right_value):
        rvalue = self.process_right_value(right_value)
        self.process_value()
        sumv = self.value + rvalue
        assert sumv >= 0
        return Length(None, None, sumv)

    def __sub__(self, right_value):
        rvalue = self.process_right_value(right_value)
        self.process_value()
        subv = self.value - rvalue
        assert subv >= 0
        return Length(None, None, subv)

    def __mul__(self, right_value):
        rvalue = self.process_right_value(right_value)
        self.process_value()
        mulv = self.value * rvalue
        assert mulv >= 0
        return Length(None, None, mulv)

    def __rmul__(self, left_value):
        lvalue = self.process_right_value(left_value)
        self.process_value()
        mulv = lvalue * self.value
        assert mulv >= 0
        return Length(None, None, mulv)

    def __radd__(self, left_value):
        lvalue = self.process_right_value(left_value)
        self.process_value()
        sumv = lvalue + self.value
        assert sumv >= 0
        return Length(None, None, sumv)

    def __rsub__(self, left_value):
        lvalue = self.process_right_value(left_value)
        self.process_value()
        diffv = lvalue - self.value
        assert diffv >= 0
        return Length(None, None, diffv)

    def __truediv__(self, right_value):
        rvalue = self.process_right_value(right_value)
        self.process_value()
        assert rvalue != 0
        divv = self.value / rvalue
        assert divv >= 0
        return Length(None, None, divv)

    def __rtruediv__(self, left_value):
        lvalue = self.process_right_value(left_value)
        self.process_value()
        divv = lvalue / self.value
        assert divv >= 0
        return Length(None, None, divv)

    def __div__(self, right_value):
        return self.__truediv__(right_value)

    def __rdiv__(self, left_value):
        return self.__rtruediv__(left_value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'Length with value %s' % str(self.value)