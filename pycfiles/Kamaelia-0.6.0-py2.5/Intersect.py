# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/OpenGL/Intersect.py
# Compiled at: 2008-10-19 12:19:52
"""=============================================================
Intersect: provides a set of static 3D intersection functions
=============================================================
"""
from math import *

class Intersect:
    """ A collection of static intersection functions. """
    epsilon = 1e-08

    def ray_OBB(r_origin, r_dir, b_pos, b_orientation, b_halflengths):
        """        Intersects a ray with an oriented bounding box.
        
        Arguments:
        
        - r_origin -- origin of the ray
        - r_dir -- normalized direction of the ray
        - b_pos -- position of the box
        - b_orientation -- list of normalised half length vectors of the box
        - b_halflengths -- list of positive half lengths of the box
        
        returns the distance from r_origin to the point of intersection
        """
        tmin = -10000
        tmax = 10000
        p = b_pos - r_origin
        for i in range(3):
            print 'pos', str(p)
            a = b_orientation[i] - p
            print 'a', a, a.length()
            h = b_halflengths[i]
            print 'h', h
            e = a.dot(p)
            print 'e', e
            f = a.dot(r_dir)
            print 'f', f
            if abs(f) > Intersect.epsilon:
                t1 = (e + h) / f
                t2 = (e - h) / f
                if t1 > t2:
                    x = t1
                    t1 = t2
                    t2 = x
                print 't1', t1
                print 't2', t2
                if t1 > tmin:
                    tmin = t1
                if t2 < tmax:
                    tmax = t2
                print 'tmin', tmin
                print 'tmax', tmax
                if tmin > tmax:
                    return 0
                if tmax < 0:
                    return 0
            elif -e - h > 0 or -e + h < 0:
                return 0

        if tmin > 0:
            return tmin
        else:
            return tmax

    ray_OBB = staticmethod(ray_OBB)

    def ray_Plane(r_origin, r_dir, p_points):
        """        Intersects a ray with a plane.

        Arguments:
        - r_origin -- origin of the ray
        - r_dir -- normalized direction of the ray
        - points -- list of 3 Vectors that represent non collinear points on the plane

        returns the distance from r_origin to the point of intersection
        """
        p = p_points[0]
        n = (p_points[0] - p_points[2]).cross(p_points[1] - p_points[2])
        d = -n.dot(p)
        den = n.dot(r_dir)
        if abs(den) < Intersect.epsilon:
            return 0
        nom = -d - n.dot(r_origin)
        return nom / den

    ray_Plane = staticmethod(ray_Plane)

    def ray_Polygon(r_origin, r_dir, p_points):
        """        Intersects a ray with a polygon.
        
        Arguments:
        - r_origin -- origin of the ray
        - r_dir -- normalized direction of the ray
        - points -- list of Vectors that represent the points of the polygon
        
        returns the distance from r_origin to the point of intersection
        """
        p = p_points[0]
        n = (p_points[0] - p_points[2]).cross(p_points[1] - p_points[2])
        d = -n.dot(p)
        den = n.dot(r_dir)
        if abs(den) < Intersect.epsilon:
            t = 0
        else:
            nom = -d - n.dot(r_origin)
            t = nom / den
        if t == 0:
            return 0
        p3d = r_origin + r_dir * t
        maxn = max(abs(n.x), abs(n.y), abs(n.z))
        if abs(n.x) == maxn:
            points = [ [point.y, point.z] for point in p_points ]
            p = [
             p3d.y, p3d.z]
        elif abs(n.y) == maxn:
            points = [ [point.x, point.z] for point in p_points ]
            p = [
             p3d.x, p3d.z]
        elif abs(n.z) == maxn:
            points = [ [point.x, point.y] for point in p_points ]
            p = [
             p3d.x, p3d.y]
        inside = False
        e0 = points[(-1)]
        e1 = points[0]
        y0 = e0[1] >= p[1]
        for i in range(1, len(points) + 1):
            y1 = e1[1] >= p[1]
            if y0 != y1:
                y2 = (e1[1] - p[1]) * (e0[0] - e1[0]) >= (e1[0] - p[0]) * (e0[1] - e1[1])
                if y2 == y1:
                    inside = not inside
            if i < len(points):
                y0 = y1
                e0 = e1
                e1 = points[i]

        if inside:
            return t
        else:
            return 0

    ray_Polygon = staticmethod(ray_Polygon)

    def ray_Sphere():
        """        NOT IMPLEMENTED YET
        """
        pass

    ray_Sphere = staticmethod(ray_Sphere)

    def plane_OOB():
        """        NOT IMPLEMENTED YET
        """
        pass

    plane_OOB = staticmethod(plane_OOB)

    def OOB_OOB():
        """        NOT IMPLEMENTED YET
        """
        pass

    OOB_OOB = staticmethod(OOB_OOB)