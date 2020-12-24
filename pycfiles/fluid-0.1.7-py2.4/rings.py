# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fluid/ocean/rings.py
# Compiled at: 2006-12-04 09:19:16
"""Ocean Rings related stuff."""
try:
    import numpy as N
except:
    try:
        import numarray as N
    except:
        import Numeric as N

_NM2KM = 1.852
_M2NM = 0.00053996

def uv2nt(u, v, x, y, x_c=0, y_c=0):
    """Convert orthogonal velocity components to normal and tangent ones

    Based on x_c and y_c, with default values (0,0) convert u and v to
    normal (n) and tangent(t) velocities.
    Input:
        - u =>
        - v =>
        - x =>
        - y =>
        - x_c =>
        - y_c =>
    Output:
        - n =>
        - t =>
    """
    dx = x - x_c
    dy = y - y_c
    alpha = N.arctan2(dy, dx)
    n = u * N.cos(alpha) + v * N.sin(alpha)
    t = v * N.cos(alpha) - u * N.sin(alpha)
    return [
     n, t]


def nt2uv(n, t, x, y, x_c=0, y_c=0):
    """Convert normal and tangent velocities to Orthogonal ones

    Convert normal(n) and tangent(t) velocities to orthogonal ones,
    u and v, based on x,y of each (n,t) velocity and the circular center
    x_c and y_c
    Input:
        - n =>
        - t =>
        - x =>
        - y =>
        - x_c =>
        - y_c =>
    Output:
        - u =>
        - v =>
    """
    dx = x - x_c
    dy = y - y_c
    alpha = N.arctan2(dy, dx)
    u = n * N.cos(alpha) - t * N.sin(alpha)
    v = n * N.sin(alpha) + t * N.cos(alpha)
    return [
     u, v]


def ringcenter(x, y, u, v, n=None, method='kinetic'):
    """Define the ring center

    !!!Atention, this routine need a improve. It only accept 1-D data array!!!

    !!!Another suggestion is consider the possibility o the center is outside the data domain.
    
    Input:
        - x =>
        - y =>
        - u =>
        - v =>
        - n =>
        - method (Criteria):
            + kinetic => highest ratio between tangent kinetic energy versus 
                         normal one.
    Output:
        - x_c =>
        - y_c =>
        - E_ratio (kinetic) => For kinetic method return the energy ratio 
                               matrix.
    """
    if method == 'kinetic':
        x_min = x[N.argmin(x)]
        x_max = x[N.argmax(x)]
        y_min = y[N.argmin(y)]
        y_max = y[N.argmax(y)]
        if n == None:
            n = 100.0
        p_x = (x_max - x_min) / n
        p_y = (y_max - y_min) / n
        x_test = N.arange(x_min, x_max + p_x, p_x)
        y_test = N.arange(y_max + p_y, y_min, -p_y)
        I = len(x_test)
        J = len(y_test)
        E_ratio = N.zeros((J, I), N.Float)
        E_max = 0
        for j in range(J):
            for i in range(I):
                (n, t) = uv2nt(u, v, x, y, x_c=x_test[i], y_c=y_test[j])
                E_ratio[(j, i)] = N.sum(t ** 2) / N.sum(n ** 2)
                if E_ratio[(j, i)] > E_max:
                    E_max = E_ratio[(j, i)]
                    x_c = x_test[i]
                    y_c = y_test[j]

        x_c = round(x_c, 3)
        y_c = round(y_c, 3)
        return (
         x_c, y_c, E_ratio, x_test, y_test, E_max)
    else:
        return
    return


def adjustringcenter(t_orig, lon_orig, lat_orig, u_orig, v_orig, sections, u_c=0, v_c=0, method='kinetic'):
    """Adjust ring center compensating propagation velocity

    !!! Include checks:
        - shape t=lon_orig=lat_orig=u=v
        - Must be tuples => t,lon_orig,lat_orig,u,v

    """
    print 'Center velocities (start)', u_c, v_c
    section_index = sections
    ring_index = N.greater(N.sum(section_index), 0)
    t = t_orig - min(t_orig)
    dt = max(t) - min(t)
    (lon, lat, u, v) = center_velocity_correction(t, lon_orig, lat_orig, u_orig, v_orig, u_c, v_c)
    (x_c_new, y_c_new, E_ratio, x_test, y_test, E_max) = ringcenter(N.compress(ring_index, lon), N.compress(ring_index, lat), N.compress(ring_index, u), N.compress(ring_index, v))
    Dcenter = 10000.0
    tol = 100.0
    while Dcenter > tol:
        x_c_s = []
        y_c_s = []
        for s in sections:
            (x_c_tmp, y_c_tmp, E_ratio, x_test, y_test, E_max) = ringcenter(N.compress(s, lon), N.compress(s, lat), N.compress(s, u), N.compress(s, v), n=50)
            x_c_s.append(x_c_tmp)
            y_c_s.append(y_c_tmp)

        if len(x_c_s) == 2:
            dlon = x_c_s[1] - x_c_s[0]
            dlat = y_c_s[1] - y_c_s[0]
        elif len(x_c_s) == 3:
            dlon = (x_c_s[1] + x_c_s[2] - (x_c_s[0] + x_c_s[1])) / 2
            dlat = (y_c_s[1] + y_c_s[2] - (y_c_s[0] + y_c_s[1])) / 2
        else:
            print 'uncomplete!!!'
        dx_c = dlon * 60 * 1852
        dy_c = dlat * 60 * 1852
        du_c = dx_c / dt
        dv_c = dy_c / dt
        if du_c > 0.01:
            du_c = 0.01
        if du_c < -0.01:
            du_c = -0.01
        if dv_c > 0.01:
            dv_c = 0.01
        if dv_c < -0.01:
            dv_c = -0.01
        du_c = round(du_c, 2)
        dv_c = round(dv_c, 2)
        u_c = du_c + u_c
        v_c = dv_c + v_c
        print 'New ring velocities', u_c, v_c
        (lon, lat, u, v) = center_velocity_correction(t, lon_orig, lat_orig, u_orig, v_orig, u_c, v_c)
        x_c_old = x_c_new
        y_c_old = y_c_new
        (x_c_new, y_c_new, E_ratio, x_test, y_test, E_max) = ringcenter(N.compress(ring_index, lon), N.compress(ring_index, lat), N.compress(ring_index, u), N.compress(ring_index, v))
        Dcenter = ((x_c_old - x_c_new) ** 2 + (y_c_old - y_c_new) ** 2) ** 0.5
        Dcenter = Dcenter * 60 * 1852

    x_c = round(x_c_old, 3)
    y_c = round(y_c_old, 3)
    u_c = round(u_c, 2)
    v_c = round(v_c, 2)
    print 'centros', x_c_new, y_c_new
    print 'velocidades', u_c, v_c
    return (
     x_c, y_c, u_c, v_c)


def center_velocity_correction(t, lon, lat, u, v, u_c, v_c):
    """Correct data due ring propagation velocity
    
    Input:
        -> u => Zonal velocity [m/s]
        -> v => Meridional velocity [m/s]
        -> u_c => Ring center zonal velocity [m/s]
        -> v_c => Ring center meridional velocity [m/s]

    Subtract the velocity field by the ring propagation and
      move the data position according to the ring propagation,
      so estimate what should be the sample if was done on one
      instant.
    """
    delta_t = t - min(t)
    u_new = u - u_c
    v_new = v - v_c
    dx = -delta_t * u_c
    dy = -delta_t * v_c
    (lon_new, lat_new) = dx2ddeg(dx, dy, lon, lat)
    return (
     lon_new, lat_new, u_new, v_new)


def dx2ddeg(dx, dy, lon, lat):
    """Latitude/Longitude final position due an x/y movement

    !!Temporary!!! Improve it! Consider an Earth projection. Maybe a good
        approach is convert to UTM and than back to Lat/Lon
        This is not a good solution for higher latitudes
    !!Here is the best place for it?
    
    """
    _M2NM = 0.00053996
    lon_new = dx * _M2NM / 60 + lon
    lat_new = dy * _M2NM / 60 + lat
    return (
     lon_new, lat_new)


def R_maximum_velocity(t, R):
    """Estimate the radius of maximum tangent velocity

    Input:
        - t => Tangent velocity
        - R => Radius of velocities data
    Output:
        - R_vmax => Radius of maximum velocity
        - precision => Precision in which R_max was defined
    """
    from fluid.common.window_mean import window_mean
    R_max = max(R)
    R_min = min(R)
    precision = 5000.0
    R_bin = N.arange(40000.0, R_max, precision)
    t_bin = window_mean(t, R, R_bin, method='triangular', boxsize=40000.0)
    index_R_vmax = N.argmax(N.abs(t_bin))
    R_vmax = R_bin[index_R_vmax]
    return (
     R_vmax, R_bin, t_bin)