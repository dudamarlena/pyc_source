# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\collision_model.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 32322 bytes
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import operator as op, math
import cocos.euclid as eu
msg_abstract = 'abstract method called, needs implementation'

class Cshape(object):
    __doc__ = '\n    Represents an abstract geometric shape in the 2D space, and can\n    answer questions about proximity or intersection with other shapes.\n\n    Implementations are free to restrict the type of geometrical shapes\n    that will accept, by example circles or axis aligned rectangles.\n    '

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
    __doc__ = "\n    Answers questions about proximity or collision with known objects.\n\n    After instantiation or after calling its 'clear' method the instance\n    don't knows any object.\n\n    An object is made known to the CollisionManager instance by calling its\n    'add' method with the object instance.\n\n    Example questions are:\n\n        - which known objects collides with <this object> ?\n        - which known objects are near than 6.0 from <this object> ?\n\n    Note that explicit objects in the question (call) don't need to be known to\n    the collision manager answering the question.\n    If the explicit object indeed is known, then it is omitted in the answer as a\n    trivial case.\n\n    There can be multiple CollisionManager instances in the same scope, and\n    an object can be known to many collision managers at the same time.\n\n    Objects that can be known or can be presented to a Collision Manager in\n    a question must comply with:\n\n        - obj has a member called cshape\n        - obj.cshape supports the interface Cshape\n\n    Such an object can be called 'a collidable' in the documentation, and when\n    'obj' or 'other' is seen in the code you can assume it means collidable.\n\n    While usually all collidables in a collision manager are of the same class\n    (CircleShape or AARectShape) it is allowed to use both types into the same\n    collision manager.\n\n    The known objects collective for each CollisionManager instance is\n    manipulated by calling the methods\n\n        - clean() \\: forgets all objects and empties internal data structures\n        - add(obj) \\: remember obj as a known object\n        - remove_tricky(obj) \\: forgets obj\n\n    When objects are made known to a collision manager, internal data structures\n    are updated based on the obj.cshape value at the 'add' moment.\n    In particular, the obj.cshape indirectly tells where in the internal\n    structures certain info will be stored.\n    Later, the internal data structures are used to accelerate answers.\n\n    This  means that modifying obj.cshape after an 'add' can produce a memory\n    leak in the next 'remove_tricky', and that in the same situation some\n    answers can be partially wrong.\n    What type of wrong ? It can sometimes miss a collision with a know\n    object that changed it cshape.\n\n    It is user code responsibility to drive the know objects update when\n    obj.cshape values changes.\n\n    Common use patterns that are safe and efficient:\n\n    When most of the known objects update cshape each frame\n\n    You do::\n\n        # updating collision info\n        collision_manager.clear() # fast, no leaks even if changed cshapes\n        for actor in moving_actors:\n            collision_manager.add(actor)\n\n        # game logic\n        # do what you need, but defer changes in cshape to next block\n        # by example\n        for actor in moving_actors:\n            actor.new_pos = actor.cshape.center + dt * vel\n            #other logic that potentially needs collision info;\n            #it will be accurate because you have not changed cshapes\n            ...\n\n        # update cshapes for next frame\n        for actor in moving actors:\n            actor.cshape.center = actor.new_pos\n\n    Example actors for this case are player, enemies, soldiers.\n\n    All of the known objects don't change Cshapes\n\n        - At level start you add all objects\n        - When an actor reaches end of life use 'remove_tricky' to make it not known, no problem because his cshape has not changed\n\n    Examples actors for this case are food, coins, trees, rocks.\n    "

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
    __doc__ = '\n    Implements the Cshape interface that uses discs as geometric shape.\n\n    Distance is the euclidean distance.\n\n    Look at Cshape for other class and methods documentation.\n    '

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
        return (self.center[0] - r, self.center[0] + r,
         self.center[1] - r, self.center[1] + r)

    def copy(self):
        return CircleShape((eu.Vector2)(*self.center), self.r)


class AARectShape(Cshape):
    __doc__ = "\n    Implements the Cshape interface that uses rectangles with sides\n    parallel to the coordinate axis as geometric shape.\n\n    Distance is not the euclidean distance but the rectangular or max-min\n    distance, max( min(x0 - x1), min(y0 - y1) : (xi, yi) in recti )\n\n    Good if actors don't rotate.\n\n    Look at Cshape for other class and methods documentation.\n    "

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
    __doc__ = '\n    Implements the CollisionManager interface with with the simpler code possible.\n\n    Intended for reference and debugging, it has very bad performance.\n\n    Look at CollisionManager for other class and methods documentation.\n    '

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
                continue
            d = f_distance(other.cshape)
            if d <= near_distance:
                res.append((other, d))

        return res

    def ranked_objs_near(self, obj, near_distance):
        tmp = self.objs_near_wdistance(obj, near_distance)
        tmp.sort(key=(op.itemgetter(1)))
        return tmp

    def iter_all_collisions(self):
        for i, obj in enumerate(self.objs):
            f_overlaps = obj.cshape.overlaps
            for j, other in enumerate(self.objs):
                if j >= i:
                    break
                if f_overlaps(other.cshape):
                    yield (
                     obj, other)

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
    __doc__ = "\n    Implements the CollisionManager interface based on the scheme\n    known as spatial hashing.\n\n    The idea behind is to divide the space in rectangles with a given width and\n    height, and have a table telling which objects overlaps each rectangle.\n\n    Later, when the question 'which know objects has such and such spatial\n    relation with <some object>' arrives, only the objects in rectangles\n    overlapping <some object> (or nearby ones) needs to be examined for the\n    condition.\n\n    Look at CollisionManager for other class and methods documentation.\n    "

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

    def any_near(self, obj, near_distance):
        minx, maxx, miny, maxy = obj.cshape.minmax()
        minx -= near_distance
        maxx += near_distance
        miny -= near_distance
        maxy += near_distance
        f_distance = obj.cshape.distance
        for cell_id in self._iter_cells_for_aabb((minx, maxx, miny, maxy)):
            for other in self.buckets[cell_id]:
                if other is not obj and f_distance(other.cshape) < near_distance:
                    return other

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
        return [(other, collides[other]) for other in collides]

    def ranked_objs_near(self, obj, near_distance):
        tmp = self.objs_near_wdistance(obj, near_distance)
        tmp.sort(key=(op.itemgetter(1)))
        return tmp

    def iter_all_collisions(self):
        known_collisions = set()
        for bucket in self.buckets:
            for i, obj in enumerate(bucket):
                f_overlaps = obj.cshape.overlaps
                for j, other in enumerate(bucket):
                    if j >= i:
                        break
                    if f_overlaps(other.cshape):
                        if id(obj) < id(other):
                            coll_id = (
                             id(obj), id(other))
                        else:
                            coll_id = (
                             id(other), id(obj))
                        if coll_id not in known_collisions:
                            known_collisions.add(coll_id)
                            yield (obj, other)

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