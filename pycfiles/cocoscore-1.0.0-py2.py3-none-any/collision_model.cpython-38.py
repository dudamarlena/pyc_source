# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\collision_model.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 32322 bytes
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import operator as op, math
import cocos.euclid as eu
msg_abstract = 'abstract method called, needs implementation'

class Cshape(object):
    """Cshape"""

    def overlaps(self, other):
        """
        Returns True if overlapping other, False otherwise

        :rtype: bool
        """
        raise NotImplementedError(msg_abstract)

    def distance(self, other):
        """
        Returns a float, distance from itself to other;

        Not necessarily  euclidean distance.
        It is distances between boundaries.

        :rtype: float
        """
        raise NotImplementedError(msg_abstract)

    def near_than(self, other, near_distance):
        """
        Returns a boolean, True if distance(self, other)<=near_distance

        :rtype: bool
        """
        raise NotImplementedError(msg_abstract)

    def touches_point(self, x, y):
        """
        Returns True if the point (x,y) overlaps the shape, False otherwise

        :rtype: bool
        """
        raise NotImplementedError(msg_abstract)

    def fits_in_box(self, packed_box):
        """
        Returns a boolean, True if the shape fully fits into the axis aligned
        rectangle defined by packed_box, False otherwise.

        :Parameters:
            `packed_box` : 4-tuple floats
                An axis aligned rectangle expressed as (minx, maxx, miny, maxy)
        :rtype: bool
        """
        raise NotImplementedError(msg_abstract)

    def minmax(self):
        """
        Returns the smallest axis aligned rectangle that contains all shape points.

        The rectangle is expressed as a 4-tuple of floats (minx, maxx, miny, maxy)
        Such a rectangle is also know as the Axis Aligned Bounding Box for shape;
        AABB for short.

        :rtype: 4-tuple of floats

        """
        raise NotImplementedError(msg_abstract)

    def copy(self):
        """
        Returns a copy of itself

        :rtype: Cshape
        """
        raise NotImplementedError(msg_abstract)


class CollisionManager(object):
    """CollisionManager"""

    def add(self, obj):
        """
        Makes obj a know entity
        """
        raise NotImplementedError(msg_abstract)

    def remove_tricky(self, obj):
        """
        *(obj should have the same .cshape value that when added)*
        Makes collision manager forget about obj, thus no further query will
        return obj.
        obj is required to be a known object.
        """
        pass

    def clear(self):
        """
        Empties the known set
        """
        raise NotImplementedError(msg_abstract)

    def they_collide(self, obj1, obj2):
        """
        Returns a boolean, True if obj1 overlaps objs2
        obj1, obj2 are not required to be known objects
        """
        raise NotImplementedError(msg_abstract)

    def objs_colliding(self, obj):
        """
        Returns a container with known objects that overlaps obj,
        excluding obj itself
        obj is not required to be a known object
        """
        raise NotImplementedError(msg_abstract)

    def iter_colliding(self, obj):
        """
        A lazy iterator over objects colliding with obj, allows to spare some
        CPU when the loop processing the collisions breaks before exhausting
        the collisions.
        obj is not required to be a known object

        Usage::

            for other in collision_manager.iter_colliding(obj):
                # process event 'obj touches other'

        """
        raise NotImplementedError(msg_abstract)

    def any_near(self, obj, near_distance):
        """
        Returns None if no know object (except itself) is near than
        near_distance, else an arbitrary known object with distance
        less than near_distance
        obj is not required to be a known object
        """
        raise NotImplementedError(msg_abstract)

    def objs_near(self, obj, near_distance):
        """
        Returns a container with the objects known by collision manager that
        are at distance to obj less or equal than near_distance, excluding
        itself.
        Notice that it includes the ones colliding with obj.
        obj is not required to be a known object
        """
        raise NotImplementedError(msg_abstract)

    def objs_near_wdistance(self, obj, near_distance):
        """
        Returns a list with the (other, distance) pairs that with all the
        known objects at distance less or equal than near_distance to obj,
        except obj itself.
        Notice that it includes the ones colliding with obj.
        obj is not required to be a known object
        If the game logic wants the list ordered by ascending distances, use
        ranked_objs_near instead.
        """
        raise NotImplementedError(msg_abstract)

    def ranked_objs_near(self, obj, near_distance):
        """
        Same as objs_near_wdistance but the list is ordered in increasing distance
        obj is not required to be a known object
        """
        raise NotImplementedError(msg_abstract)

    def iter_all_collisions(self):
        """
        Iterator that exposes all collisions between known objects.
        At each step it will yield a pair (obj, other).
        If (obj1, obj2) is seen when consuming the iterator, then (obj2, obj1)
        will not be seen.
        In other worlds, 'obj1 collides with obj2' means (obj1, obj2) or
        (obj2, obj1) will appear in the iterator output but not both.
        """
        pass

    def knows(self, obj):
        """Returns True if obj was added to the collision manager, false otherwise
        Used for debug and testing.
        """
        raise NotImplementedError(msg_abstract)

    def known_objs(self):
        """Returns a set with all the objects known by the CollisionManager
        Used for debug and testing.
        """
        raise NotImplementedError(msg_abstract)

    def objs_touching_point(self, x, y):
        """Returns a container with known objects touching point (x, y)

        Useful for mouse pick
        """
        raise NotImplementedError(msg_abstract)

    def objs_into_box(self, minx, maxx, miny, maxy):
        """Returns a container with know objects that fully fits into the axis
        aligned rectangle defined by params

        Useful for elastic box selection
        """
        raise NotImplementedError(msg_abstract)


class CircleShape(Cshape):
    """CircleShape"""

    def __init__(self, center, r):
        """
        :Parameters:
            `center` : euclid.Vector2
                rectangle center
            `r` : float
                disc radius
        """
        self.center = center
        self.r = r

    def overlaps(self, other):
        if isinstance(other, CircleShape):
            return circle_overlaps_circle(self, other)
        if isinstance(other, AARectShape):
            return aa_rect_overlaps_circle(other, self)
        raise NotImplementedError('Collision between CircleShape and {0} is not implemented'.format(other.__class__.__name__))

    def distance(self, other):
        if isinstance(other, CircleShape):
            return circle_distance_circle(self, other)
        if isinstance(other, AARectShape):
            return aa_rect_distance_circle(other, self)
        raise NotImplementedError('Distance between CircleShape and {0} is not implemented'.format(other.__class__.__name__))

    def near_than(self, other, near_distance):
        return self.distance(other) <= near_distance

    def touches_point(self, x, y):
        return abs(self.center - (x, y)) <= self.r

    def fits_in_box(self, packed_box):
        r = self.r
        return packed_box[0] + r <= self.center[0] <= packed_box[1] - r and packed_box[2] + r <= self.center[1] <= packed_box[3] - r

    def minmax(self):
        r = self.r
        return (
         self.center[0] - r, self.center[0] + r,
         self.center[1] - r, self.center[1] + r)

    def copy(self):
        return CircleShape((eu.Vector2)(*self.center), self.r)


class AARectShape(Cshape):
    """AARectShape"""

    def __init__(self, center, half_width, half_height):
        """
        :Parameters:
            `center` : euclid.Vector2
                rectangle center
            `half_width` : float
                half width of rectangle
            `half_height` : float
                half height of rectangle
        """
        self.center = center
        self.rx = half_width
        self.ry = half_height

    def overlaps(self, other):
        if isinstance(other, AARectShape):
            return aa_rect_overlaps_aa_rect(self, other)
        if isinstance(other, CircleShape):
            return aa_rect_overlaps_circle(self, other)
        raise NotImplementedError('Collision between AARectShape and {0} is not implemented'.format(other.__class__.__name__))

    def distance(self, other):
        if isinstance(other, AARectShape):
            return aa_rect_distance_aa_rect(self, other)
        if isinstance(other, CircleShape):
            return aa_rect_distance_circle(self, other)
        raise NotImplementedError('Distance between AARectShape and {0} is not implemented'.format(other.__class__.__name__))

    def near_than(self, other, near_distance):
        return self.distance(other) <= near_distance

    def touches_point(self, x, y):
        return abs(self.center[0] - x) < self.rx and abs(self.center[1] - y) < self.ry

    def fits_in_box(self, packed_box):
        return packed_box[0] + self.rx <= self.center[0] <= packed_box[1] - self.rx and packed_box[2] + self.ry <= self.center[1] <= packed_box[3] - self.ry

    def minmax(self):
        return (
         self.center[0] - self.rx, self.center[0] + self.rx,
         self.center[1] - self.ry, self.center[1] + self.ry)

    def copy(self):
        return AARectShape((eu.Vector2)(*self.center), self.rx, self.ry)


def clamp(value, minimum, maximum):
    return max(min(value, maximum), minimum)


def aa_rect_overlaps_aa_rect(aa_rect, other):
    """
    Tells if two axis aligned rectangles overlap.

    The rects must have members 'center', 'rx', 'ry' where the latest two are
    the rect half_width and half_height.
    """
    return abs(aa_rect.center[0] - other.center[0]) < aa_rect.rx + other.rx and abs(aa_rect.center[1] - other.center[1]) < aa_rect.ry + other.ry


def circle_overlaps_circle(circle, other):
    """
    Tells if two circles overlap.

    The circles must have members 'center', 'r', where the latest is the radius.
    """
    return (circle.center - other.center).magnitude_squared() < (circle.r + other.r) ** 2


def aa_rect_overlaps_circle(aa_rect, circle):
    """
    Tells if an axis aligned rectangle and a circle overlap.

    The rect must have members 'center', 'rx', 'ry' where the latest two are
    the rect half_width and half_height.
    The circle must have members 'center', 'r', where the latest is the radius.
    """
    d = circle.center - aa_rect.center
    d_clamped = eu.Vector2(clamp(d.x, -aa_rect.rx, aa_rect.rx), clamp(d.y, -aa_rect.ry, aa_rect.ry))
    return (d - d_clamped).magnitude_squared() < circle.r ** 2


def circle_distance_circle(circle, other):
    """
    Give the distance between two circles.

    The circles must have members 'center', 'r', where the latest is the radius.
    """
    d = abs(circle.center - other.center) - circle.r - other.r
    if d < 0.0:
        d = 0.0
    return d


def aa_rect_distance_circle(aa_rect, circle):
    """
    Give the distance between an axis-aligned rectangle and a circle.

    The rect must have members 'center', 'rx', 'ry' where the latest two are
    the rect half_width and half_height.
    The circle must have members 'center', 'r', where the latest is the radius.
    """
    d = circle.center - aa_rect.center
    d_clamped = eu.Vector2(clamp(d.x, -aa_rect.rx, aa_rect.rx), clamp(d.y, -aa_rect.ry, aa_rect.ry))
    d = abs(d - d_clamped) - circle.r
    if d < 0.0:
        d = 0.0
    return d


def aa_rect_distance_aa_rect(aa_rect, other):
    """
    Give the distance between two axis-aligned rectangles.

    The rect must have members 'center', 'rx', 'ry' where the latest two are
    the rect half_width and half_height.
    """
    d = max((abs(aa_rect.center[0] - other.center[0]) - aa_rect.rx - other.rx,
     abs(aa_rect.center[1] - other.center[1]) - aa_rect.ry - other.ry))
    if d < 0.0:
        d = 0.0
    return d


class CollisionManagerBruteForce(CollisionManager):
    """CollisionManagerBruteForce"""

    def __init__(self):
        self.objs = set()

    def add(self, obj):
        self.objs.add(obj)

    def remove_tricky(self, obj):
        self.objs.remove(obj)

    def clear(self):
        self.objs.clear()

    def they_collide(self, obj1, obj2):
        return obj1.cshape.overlaps(obj2.cshape)

    def objs_colliding(self, obj):
        f_overlaps = obj.cshape.overlaps
        return [other for other in self.objs if other is not obj if f_overlaps(other.cshape)]

    def iter_colliding(self, obj):
        f_overlaps = obj.cshape.overlaps
        for other in self.objs:
            if other is not obj and f_overlaps(other.cshape):
                yield other

    def any_near(self, obj, near_distance):
        f_near_than = obj.cshape.near_than
        for other in self.objs:
            if other is not obj and f_near_than(other.cshape, near_distance):
                return other

    def objs_near(self, obj, near_distance):
        f_near_than = obj.cshape.near_than
        return [other for other in self.objs if other is not obj if f_near_than(other.cshape, near_distance)]

    def objs_near_wdistance(self, obj, near_distance):
        f_distance = obj.cshape.distance
        res = []
        for other in self.objs:
            if other is obj:
                pass
            else:
                d = f_distance(other.cshape)
                if d <= near_distance:
                    res.append((other, d))
                return res

    def ranked_objs_near(self, obj, near_distance):
        tmp = self.objs_near_wdistance(obj, near_distance)
        tmp.sort(key=(op.itemgetter(1)))
        return tmp

    def iter_all_collisions--- This code section failed: ---

 L. 630         0  LOAD_GLOBAL              enumerate
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                objs
                6  CALL_FUNCTION_1       1  ''
                8  GET_ITER         
               10  FOR_ITER             80  'to 80'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'i'
               16  STORE_FAST               'obj'

 L. 631        18  LOAD_FAST                'obj'
               20  LOAD_ATTR                cshape
               22  LOAD_ATTR                overlaps
               24  STORE_FAST               'f_overlaps'

 L. 632        26  LOAD_GLOBAL              enumerate
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                objs
               32  CALL_FUNCTION_1       1  ''
               34  GET_ITER         
             36_0  COME_FROM            64  '64'
               36  FOR_ITER             78  'to 78'
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'j'
               42  STORE_FAST               'other'

 L. 633        44  LOAD_FAST                'j'
               46  LOAD_FAST                'i'
               48  COMPARE_OP               >=
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L. 634        52  POP_TOP          
               54  JUMP_BACK            10  'to 10'
             56_0  COME_FROM            50  '50'

 L. 635        56  LOAD_FAST                'f_overlaps'
               58  LOAD_FAST                'other'
               60  LOAD_ATTR                cshape
               62  CALL_FUNCTION_1       1  ''
               64  POP_JUMP_IF_FALSE    36  'to 36'

 L. 636        66  LOAD_FAST                'obj'
               68  LOAD_FAST                'other'
               70  BUILD_TUPLE_2         2 
               72  YIELD_VALUE      
               74  POP_TOP          
               76  JUMP_BACK            36  'to 36'
               78  JUMP_BACK            10  'to 10'

Parse error at or near `JUMP_BACK' instruction at offset 76

    def knows(self, obj):
        return obj in self.objs

    def known_objs(self):
        return self.objs

    def objs_touching_point(self, x, y):
        touching = set()
        for obj in self.objs:
            if obj.cshape.touches_point(x, y):
                touching.add(obj)
            return touching

    def objs_into_box(self, minx, maxx, miny, maxy):
        into = set()
        packed_box = (minx, maxx, miny, maxy)
        for obj in self.objs:
            if obj.cshape.fits_in_box(packed_box):
                into.add(obj)
            return into


class CollisionManagerGrid(CollisionManager):
    """CollisionManagerGrid"""

    def __init__(self, xmin, xmax, ymin, ymax, cell_width, cell_height):
        """
        Cell width and height have impact on performance.
        For objects with same with, and with width==height, a good value
        is 1.25 * (object width).
        For mixed widths, a good guess can be
        ~ 1.25 * { width(object): all objects not exceptionlly big}

        :Parameters:
            `xmin` : float
                minimum x coordinate for a point in world
            `xmax` : float
                maximum x coordinate for a point in world
            `ymin` : float
                minimum y coordinate for a point in world
            `ymax` : float
                maximum y coordinate for a point in world
            `cell_width` : float
                width for the rectangles the space will be broken
            `cell_height` : float
                height for the rectangles the space will be broken
        """
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.cell_width = cell_width
        self.cell_height = cell_height
        cols = int(math.ceil((xmax - xmin) / cell_width))
        rows = int(math.ceil((ymax - ymin) / cell_height))
        self.cols = cols
        self.rows = rows
        numbuckets = cols * rows
        self.buckets = [set() for k in range(numbuckets)]

    def add(self, obj):
        for cell_idx in self._iter_cells_for_aabb(obj.cshape.minmax()):
            self.buckets[cell_idx].add(obj)

    def remove_tricky(self, obj):
        for cell_idx in self._iter_cells_for_aabb(obj.cshape.minmax()):
            self.buckets[cell_idx].remove(obj)

    def clear(self):
        for bucket in self.buckets:
            bucket.clear()

    def they_collide(self, obj1, obj2):
        return obj1.cshape.overlaps(obj2.cshape)

    def objs_colliding(self, obj):
        aabb = obj.cshape.minmax()
        f_overlaps = obj.cshape.overlaps
        collides = set()
        collides.add(obj)
        for cell_id in self._iter_cells_for_aabb(aabb):
            for other in self.buckets[cell_id]:
                if other not in collides and f_overlaps(other.cshape):
                    collides.add(other)

            collides.remove(obj)
            return collides

    def iter_colliding(self, obj):
        aabb = obj.cshape.minmax()
        f_overlaps = obj.cshape.overlaps
        collides = set()
        collides.add(obj)
        for cell_id in self._iter_cells_for_aabb(aabb):
            for other in self.buckets[cell_id]:
                if other not in collides and f_overlaps(other.cshape):
                    collides.add(other)
                    yield other

    def any_near--- This code section failed: ---

 L. 758         0  LOAD_FAST                'obj'
                2  LOAD_ATTR                cshape
                4  LOAD_METHOD              minmax
                6  CALL_METHOD_0         0  ''
                8  UNPACK_SEQUENCE_4     4 
               10  STORE_FAST               'minx'
               12  STORE_FAST               'maxx'
               14  STORE_FAST               'miny'
               16  STORE_FAST               'maxy'

 L. 759        18  LOAD_FAST                'minx'
               20  LOAD_FAST                'near_distance'
               22  INPLACE_SUBTRACT 
               24  STORE_FAST               'minx'

 L. 760        26  LOAD_FAST                'maxx'
               28  LOAD_FAST                'near_distance'
               30  INPLACE_ADD      
               32  STORE_FAST               'maxx'

 L. 761        34  LOAD_FAST                'miny'
               36  LOAD_FAST                'near_distance'
               38  INPLACE_SUBTRACT 
               40  STORE_FAST               'miny'

 L. 762        42  LOAD_FAST                'maxy'
               44  LOAD_FAST                'near_distance'
               46  INPLACE_ADD      
               48  STORE_FAST               'maxy'

 L. 763        50  LOAD_FAST                'obj'
               52  LOAD_ATTR                cshape
               54  LOAD_ATTR                distance
               56  STORE_FAST               'f_distance'

 L. 765        58  LOAD_FAST                'self'
               60  LOAD_METHOD              _iter_cells_for_aabb
               62  LOAD_FAST                'minx'
               64  LOAD_FAST                'maxx'
               66  LOAD_FAST                'miny'
               68  LOAD_FAST                'maxy'
               70  BUILD_TUPLE_4         4 
               72  CALL_METHOD_1         1  ''
               74  GET_ITER         
               76  FOR_ITER            132  'to 132'
               78  STORE_FAST               'cell_id'

 L. 766        80  LOAD_FAST                'self'
               82  LOAD_ATTR                buckets
               84  LOAD_FAST                'cell_id'
               86  BINARY_SUBSCR    
               88  GET_ITER         
             90_0  COME_FROM           114  '114'
             90_1  COME_FROM           100  '100'
               90  FOR_ITER            130  'to 130'
               92  STORE_FAST               'other'

 L. 767        94  LOAD_FAST                'other'
               96  LOAD_FAST                'obj'
               98  COMPARE_OP               is-not
              100  POP_JUMP_IF_FALSE    90  'to 90'
              102  LOAD_FAST                'f_distance'
              104  LOAD_FAST                'other'
              106  LOAD_ATTR                cshape
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_FAST                'near_distance'
              112  COMPARE_OP               <
              114  POP_JUMP_IF_FALSE    90  'to 90'

 L. 768       116  LOAD_FAST                'other'
              118  ROT_TWO          
              120  POP_TOP          
              122  ROT_TWO          
              124  POP_TOP          
              126  RETURN_VALUE     
              128  JUMP_BACK            90  'to 90'
              130  JUMP_BACK            76  'to 76'

Parse error at or near `ROT_TWO' instruction at offset 122

    def objs_near(self, obj, near_distance):
        minx, maxx, miny, maxy = obj.cshape.minmax()
        minx -= near_distance
        maxx += near_distance
        miny -= near_distance
        maxy += near_distance
        f_distance = obj.cshape.distance
        collides = set()
        for cell_id in self._iter_cells_for_aabb((minx, maxx, miny, maxy)):
            for other in self.buckets[cell_id]:
                if other not in collides and f_distance(other.cshape) < near_distance:
                    collides.add(other)

            collides.discard(obj)
            return collides

    def objs_near_wdistance(self, obj, near_distance):
        minx, maxx, miny, maxy = obj.cshape.minmax()
        minx -= near_distance
        maxx += near_distance
        miny -= near_distance
        maxy += near_distance
        f_distance = obj.cshape.distance
        collides = {}
        collides[obj] = 0.0
        for cell_id in self._iter_cells_for_aabb((minx, maxx, miny, maxy)):
            for other in self.buckets[cell_id]:
                if other not in collides:
                    d = f_distance(other.cshape)
                    if d <= near_distance:
                        collides[other] = d

            del collides[obj]
            return [(
             other, collides[other]) for other in collides]

    def ranked_objs_near(self, obj, near_distance):
        tmp = self.objs_near_wdistance(obj, near_distance)
        tmp.sort(key=(op.itemgetter(1)))
        return tmp

    def iter_all_collisions--- This code section failed: ---

 L. 815         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'known_collisions'

 L. 816         6  LOAD_FAST                'self'
                8  LOAD_ATTR                buckets
               10  GET_ITER         
               12  FOR_ITER            162  'to 162'
               14  STORE_FAST               'bucket'

 L. 817        16  LOAD_GLOBAL              enumerate
               18  LOAD_FAST                'bucket'
               20  CALL_FUNCTION_1       1  ''
               22  GET_ITER         
               24  FOR_ITER            160  'to 160'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'i'
               30  STORE_FAST               'obj'

 L. 818        32  LOAD_FAST                'obj'
               34  LOAD_ATTR                cshape
               36  LOAD_ATTR                overlaps
               38  STORE_FAST               'f_overlaps'

 L. 819        40  LOAD_GLOBAL              enumerate
               42  LOAD_FAST                'bucket'
               44  CALL_FUNCTION_1       1  ''
               46  GET_ITER         
             48_0  COME_FROM           134  '134'
             48_1  COME_FROM            76  '76'
               48  FOR_ITER            158  'to 158'
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'j'
               54  STORE_FAST               'other'

 L. 820        56  LOAD_FAST                'j'
               58  LOAD_FAST                'i'
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_FALSE    68  'to 68'

 L. 821        64  POP_TOP          
               66  JUMP_BACK            24  'to 24'
             68_0  COME_FROM            62  '62'

 L. 822        68  LOAD_FAST                'f_overlaps'
               70  LOAD_FAST                'other'
               72  LOAD_ATTR                cshape
               74  CALL_FUNCTION_1       1  ''
               76  POP_JUMP_IF_FALSE    48  'to 48'

 L. 823        78  LOAD_GLOBAL              id
               80  LOAD_FAST                'obj'
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_GLOBAL              id
               86  LOAD_FAST                'other'
               88  CALL_FUNCTION_1       1  ''
               90  COMPARE_OP               <
               92  POP_JUMP_IF_FALSE   112  'to 112'

 L. 824        94  LOAD_GLOBAL              id
               96  LOAD_FAST                'obj'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_GLOBAL              id
              102  LOAD_FAST                'other'
              104  CALL_FUNCTION_1       1  ''
              106  BUILD_TUPLE_2         2 
              108  STORE_FAST               'coll_id'
              110  JUMP_FORWARD        128  'to 128'
            112_0  COME_FROM            92  '92'

 L. 826       112  LOAD_GLOBAL              id
              114  LOAD_FAST                'other'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_GLOBAL              id
              120  LOAD_FAST                'obj'
              122  CALL_FUNCTION_1       1  ''
              124  BUILD_TUPLE_2         2 
              126  STORE_FAST               'coll_id'
            128_0  COME_FROM           110  '110'

 L. 827       128  LOAD_FAST                'coll_id'
              130  LOAD_FAST                'known_collisions'
              132  COMPARE_OP               not-in
              134  POP_JUMP_IF_FALSE    48  'to 48'

 L. 828       136  LOAD_FAST                'known_collisions'
              138  LOAD_METHOD              add
              140  LOAD_FAST                'coll_id'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          

 L. 829       146  LOAD_FAST                'obj'
              148  LOAD_FAST                'other'
              150  BUILD_TUPLE_2         2 
              152  YIELD_VALUE      
              154  POP_TOP          
              156  JUMP_BACK            48  'to 48'
              158  JUMP_BACK            24  'to 24'
              160  JUMP_BACK            12  'to 12'

Parse error at or near `JUMP_BACK' instruction at offset 158

    def knows(self, obj):
        for bucket in self.buckets:
            if obj in bucket:
                return True

        return False

    def known_objs(self):
        objs = set()
        for bucket in self.buckets:
            objs |= bucket

        return objs

    def objs_touching_point(self, x, y):
        touching = set()
        for cell_id in self._iter_cells_for_aabb((x, x, y, y)):
            for obj in self.buckets[cell_id]:
                if obj.cshape.touches_point(x, y):
                    touching.add(obj)

            return touching

    def objs_into_box(self, minx, maxx, miny, maxy):
        into = set()
        buckets = self.buckets
        packed_box = (minx, maxx, miny, maxy)
        for cell_idx in self._iter_cells_for_aabb(packed_box):
            for obj in buckets[cell_idx]:
                if obj not in into and obj.cshape.fits_in_box(packed_box):
                    into.add(obj)

            return into

    def _iter_cells_for_aabb(self, aabb):
        minx, maxx, miny, maxy = aabb
        ix_lo = int(math.floor((minx - self.xmin) / self.cell_width))
        ix_sup = int(math.ceil((maxx - self.xmin) / self.cell_width))
        iy_lo = int(math.floor((miny - self.ymin) / self.cell_height))
        iy_sup = int(math.ceil((maxy - self.ymin) / self.cell_height))
        if ix_lo < 0:
            ix_lo = 0
        if ix_sup > self.cols:
            ix_sup = self.cols
        if iy_lo < 0:
            iy_lo = 0
        if iy_sup > self.rows:
            iy_sup = self.rows
        for iy in range(iy_lo, iy_sup):
            contrib_y = iy * self.cols
            for ix in range(ix_lo, ix_sup):
                cell_id = ix + contrib_y
                yield cell_id