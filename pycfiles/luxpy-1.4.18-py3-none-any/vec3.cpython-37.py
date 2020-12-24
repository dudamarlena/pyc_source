# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\utils\math\vec3\vec3.py
# Compiled at: 2018-12-10 04:03:14
# Size of source mod 2**32: 12688 bytes
"""
Simple module for 3D-vectors.
==================================================================
 :vec3: class for 3D vectors.
 
 :rotate: rotate a vec3 vector.
 
 :plot: plot a vec3 vector.
 
 :cross: calculate cross product of vec3 vectors a and b.
 
 :dot: calculate dot product of vec3 vectors a and b.
 
.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, plt, Axes3D
__all__ = [
 'vec3', 'rotate', 'dot', 'cross', 'plot']

class vec3:

    def __init__(self, *args, argtype='xyz', vtype='xyz', _TINY=1e-15):
        self._TINY = _TINY
        self.vtype = vtype
        if len(args) == 0:
            args = [
             0.0, 0.0, 0.0]
        else:
            args = [np.atleast_1d(args[i]) for i in range(len(args))]
            if vtype == 'xyz':
                self.x = args[0]
                self.y = args[1]
                self.z = args[2]
            else:
                if vtype == 'tpr':
                    if len(args) == 2:
                        args.append(np.ones(args[0].shape))
                    (self.set_tpr)(*args)
        self.shape = self.x.shape

    def __repr__(self):
        return 'vec3' + repr(tuple((self.x, self.y, self.z)))

    def __mul__(self, other, norm=False):
        return _mul(self, other, norm=norm)

    def __rmul__(self, other, norm=False):
        return _mul(self, other, norm=norm)

    def __truediv__(self, other, norm=False):
        return _div(self, other, norm=norm)

    def __rtruediv__(self, other, norm=False):
        return _rdiv(self, other, norm=norm)

    def __add__(self, other, norm=False):
        return _add(self, other, norm=norm)

    def __radd__(self, other, norm=False):
        return _add(self, other, norm=norm)

    def __sub__(self, other, norm=False):
        return _sub(self, other, norm=norm)

    def __rsub__(self, other, norm=False):
        return _rsub(self, other, norm=norm)

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    def __abs__(self):
        return np.sqrt(self * self)

    def __pow__(self, x):
        if x == 2:
            return self * self
        return np.abs(self) ** x

    def __eq__(self, other):
        return np.abs(self - other) < self._TINY

    def __ne__(self, other):
        return not self == other

    def norm(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def rotate(self, vecA=None, vecB=None, rot_axis=None, rot_angle=None, deg=True, norm=False):
        return rotate(self, vecA=vecA, vecB=vecB, rot_axis=rot_axis, rot_angle=rot_angle, deg=deg, norm=norm)

    def copy(self):
        return vec3(self.x.copy(), self.y.copy(), self.z.copy())

    def get_tpr(self, *args):
        if len(args) > 0:
            x, y, z = args
        else:
            x, y, z = self.x, self.y, self.z
        r = np.sqrt(x * x + y * y + z * z)
        zdr = np.asarray(z / r)
        zdr[zdr > 1.0] = 1.0
        zdr[zdr < -1.0] = -1.0
        theta = np.arccos(z / r)
        phi = np.arctan2(y, x)
        phi[phi < 0.0] = phi[(phi < 0.0)] + 2 * np.pi
        phi[r < self._TINY] = 0.0
        theta[r < self._TINY] = 0.0
        return (theta, phi, r)

    def set_tpr(self, *args):
        self.x, self.y, self.z = (self.get_xyz)(*args)

    def get_xyz(self, *args):
        theta, phi, r = args
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        z[np.abs(z) < self._TINY] = 0.0
        return (x, y, z)

    def plot(self, origin=None, ax=None, color='k', marker='.', linestyle='-', **kwargs):
        plot(self, origin=origin, ax=ax, color=color, marker=marker, linestyle=linestyle, **kwargs)


def _mul(a, b, norm=False):
    if (not isinstance(a, vec3)) & isinstance(b, vec3):
        a = vec3(a, a, a)
    else:
        if (not isinstance(b, vec3)) & isinstance(a, vec3):
            b = vec3(b, b, b)
        if isinstance(a, vec3) & isinstance(b, vec3):
            amb = vec3(a.x * b.x, a.y * b.y, a.z * b.z)
            if norm == True:
                amb = amb / amb.norm()
    return amb


def _div(a, b, norm=False):
    if (not isinstance(a, vec3)) & isinstance(b, vec3):
        a = vec3(a, a, a)
    else:
        if (not isinstance(b, vec3)) & isinstance(a, vec3):
            b = vec3(b, b, b)
        if isinstance(a, vec3) & isinstance(b, vec3):
            adb = vec3(a.x / b.x, a.y / b.y, a.z / b.z)
            if norm == True:
                adb = adb / adb.norm()
    return adb


def _rdiv(a, b, norm=False):
    if (not isinstance(a, vec3)) & isinstance(b, vec3):
        a = vec3(a, a, a)
    else:
        if (not isinstance(b, vec3)) & isinstance(a, vec3):
            b = vec3(b, b, b)
        if isinstance(a, vec3) & isinstance(b, vec3):
            adb = vec3(b.x / a.x, b.y / a.y, b.z / a.z)
            if norm == True:
                adb = adb / adb.norm()
    return adb


def _add(a, b, norm=False):
    if (not isinstance(a, vec3)) & isinstance(b, vec3):
        a = vec3(a, a, a)
    else:
        if (not isinstance(b, vec3)) & isinstance(a, vec3):
            b = vec3(b, b, b)
        if isinstance(a, vec3) & isinstance(b, vec3):
            apb = vec3(a.x + b.x, a.y + b.y, a.z + b.z)
            if norm == True:
                apb = apb / apb.norm()
    return apb


def _sub(a, b, norm=False):
    if (not isinstance(a, vec3)) & isinstance(b, vec3):
        a = vec3(a, a, a)
    else:
        if (not isinstance(b, vec3)) & isinstance(a, vec3):
            b = vec3(b, b, b)
        if isinstance(a, vec3) & isinstance(b, vec3):
            amb = vec3(a.x - b.x, a.y - b.y, a.z - b.z)
            if norm == True:
                amb = amb / amb.norm()
    return amb


def _rsub(a, b, norm=False):
    if (not isinstance(a, vec3)) & isinstance(b, vec3):
        a = vec3(a, a, a)
    else:
        if (not isinstance(b, vec3)) & isinstance(a, vec3):
            b = vec3(b, b, b)
        if isinstance(a, vec3) & isinstance(b, vec3):
            amb = vec3(b.x - a.x, b.y - a.y, b.z - a.z)
            if norm == True:
                amb = amb / amb.norm()
    return amb


def dot(a, b, norm=False):
    """
    Calculate dot product between vec3 vectors a and b.
    
    Args:
        :a:
            | vec3 vector(s).
        :b:
            | vec3 vector(s).
        :norm:
            | False, optional
            
    Returns:
        :dot(a,b): 
            | float or ndarray.
    """
    if (not isinstance(a, vec3)) & isinstance(b, vec3):
        a = vec3(a, a, a)
    else:
        if (not isinstance(b, vec3)) & isinstance(a, vec3):
            b = vec3(b, b, b)
        if isinstance(a, vec3) & isinstance(b, vec3):
            dotab = a.x * b.x + a.y * b.y + a.z * b.z
            if norm == True:
                dotab = dotab / (a.norm() * b.norm())
    return dotab


def cross(a, b, norm=False):
    """
    Calculate cross product between vec3 vectors a and b.
    
    Args:
        :a:
            | vec3 vector(s).
        :b:
            | vec3 vector(s).
        :norm:
            | False, optional
            
    Returns:
        :dot(a,b): 
            | float or ndarray.
    """
    if isinstance(a, vec3) & isinstance(b, vec3):
        crossab = vec3(a.y * b.z - b.y * a.z, a.z * b.x - b.z * a.x, a.x * b.y - b.x * a.y)
        if norm == True:
            crossab = crossab / crossab.norm()
    else:
        raise Exception('cross(a,b): at least 1 non-vec3 input!')
    return crossab


def rotate(v, vecA=None, vecB=None, rot_axis=None, rot_angle=None, deg=True, norm=False):
    """
    Rotate vector around rotation axis over angle.
    
    Args:
        :v: 
            | vec3 vector.
        :rot_axis:
            | None, optional
            | vec3 vector specifying rotation axis.
        :rot_angle:
            | None, optional
            | float or int rotation angle.
        :deg:
            | True, optional
            | If False, rot_angle is in radians.
        :vecA:, :vecB:
            | None, optional
            | vec3 vectors defining a normal direction (cross(vecA, vecB)) around 
            | which to rotate the vector in :v:. If rot_angle is None: rotation
            | angle is defined by the in-plane angle between vecA and vecB.
        :norm:
            | False, optional
            | Normalize rotated vector.
        
    """
    if (vecA is not None) & (vecB is not None):
        rot_axis = cross(vecA, vecB)
        if rot_angle is None:
            costheta = dot(vecA, vecB, norm=True)
            costheta[costheta > 1] = 1
            costheta[costheta < -1] = -1
            rot_angle = np.arccos(costheta)
    elif rot_angle is not None:
        if deg == True:
            rot_angle = np.deg2rad(rot_angle)
    else:
        raise Exception('vec3.rotate: insufficient not-None input args.')
    rot_axis = rot_axis / rot_axis.norm()
    u = rot_axis
    cost = np.cos(rot_angle)
    sint = np.sin(rot_angle)
    R = np.asarray([[np.zeros(u.x.shape) for j in range(3)] for i in range(3)])
    R[(0, 0)] = cost + u.x * u.x * (1 - cost)
    R[(0, 1)] = u.x * u.y * (1 - cost) - u.z * sint
    R[(0, 2)] = u.x * u.z * (1 - cost) + u.y * sint
    R[(1, 0)] = u.x * u.y * (1 - cost) + u.z * sint
    R[(1, 1)] = cost + u.y * u.y * (1 - cost)
    R[(1, 2)] = u.y * u.z * (1 - cost) - u.x * sint
    R[(2, 0)] = u.z * u.x * (1 - cost) - u.y * sint
    R[(2, 1)] = u.z * u.y * (1 - cost) + u.x * sint
    R[(2, 2)] = cost + u.z * u.z * (1 - cost)
    v3 = vec3(R[(0, 0)] * v.x + R[(0, 1)] * v.y + R[(0, 2)] * v.z, R[(1, 0)] * v.x + R[(1,
                                                                                        1)] * v.y + R[(1,
                                                                                                       2)] * v.z, R[(2,
                                                                                                                     0)] * v.x + R[(2,
                                                                                                                                    1)] * v.y + R[(2,
                                                                                                                                                   2)] * v.z)
    if norm == True:
        v3 = v3 / v3.norm()
    return v3


def plot(v, origin=None, ax=None, color='k', marker='.', linestyle='-', **kwargs):
    """
    Plot a vector from origin.
    
    Args:
        :v:
            | vec3 vector.
        :origin:
            | vec3 vector with same size attributes as in :v:.
        :ax: 
            | None, optional
            | axes handle.
            | If None, create new figure with axes ax.
        :color:
            | 'k', optional
            | color specifier.
        :marker:
            | '.', optional
            | marker specifier.
        :linestyle:
            | '-', optional
            | linestyle specifier
        :**kwargs:
            | other keyword specifiers for plot.
          
    Returns:
        :ax:
            | handle to figure axes.          
    """
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    if origin is None:
        origin = vec3(np.zeros(v.x.shape), np.zeros(v.x.shape), np.zeros(v.x.shape))
    (ax.plot)(np.hstack([origin.x, v.x]), np.hstack([origin.y, v.y]), np.hstack([origin.z, v.z]), color=color, marker=marker, **kwargs)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    return ax


if __name__ == '__main__':
    n = vec3(0, 0, 1)
    a = vec3(0, 2, 2)
    b = n
    ax = plot(n, ax=None, color='k', marker='o')
    plot(a, ax=ax, color='b', marker='d')
    plot(b, ax=ax, color='g', marker='s')
    c = rotate(a, vecA=a, vecB=b, deg=True)
    d = a.rotate(a, b, deg=True, norm=True)
    plot(c, ax=ax, color='r', marker='p')
    plot(d, ax=ax, color='y', marker='s', linestyle=':')
    c.plot(ax=ax, color='k', marker='p')