# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wptherml/colorlib.py
# Compiled at: 2019-03-10 22:23:41
# Size of source mod 2**32: 10980 bytes
import wptherml.numlib as numlib
import wptherml.datalib as datalib
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cmx

def classify_color(spec, lam):
    colors = {'red':[
      1.0, 0, 0], 
     'orange':[
      1.0, 0.5019607843137255, 0], 
     'yellow':[
      1.0, 1.0, 0], 
     'green':[
      0, 1.0, 0], 
     'blue':[
      0, 0, 1.0], 
     'indigo':[
      0.29411764705882354, 0, 0.5098039215686274], 
     'violet':[
      1.0, 0, 1.0]}
    color_keys = [
     'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    rgb = RGB_FromSpec(spec, lam)
    distance_list = np.zeros(len(color_keys))
    for i in range(0, len(distance_list)):
        temp = colors[color_keys[i]]
        distance = np.sqrt((rgb[0] - temp[0]) ** 2 + (rgb[1] - temp[1]) ** 2 + (rgb[2] - temp[2]) ** 2)
        distance_list[i] = distance

    color = color_keys[np.argmin(distance_list)]
    return color


def RGB_FromSpec(TE, lam):
    cie = datalib.CIE(lam)
    X = numlib.Integrate(TE * cie['xbar'], lam, 3.8e-07, 7.8e-07)
    Y = numlib.Integrate(TE * cie['ybar'], lam, 3.8e-07, 7.8e-07)
    Z = numlib.Integrate(TE * cie['zbar'], lam, 3.8e-07, 7.8e-07)
    tot = X + Y + Z
    x = X / tot
    y = Y / tot
    z = Z / tot
    xrgbw = [
     0.67, 0.21, 0.15, 0.3127]
    yrgbw = [0.33, 0.71, 0.06, 0.3291]
    zrgbw = []
    for i in range(0, len(xrgbw)):
        zrgbw.append(1.0 - xrgbw[i] - yrgbw[i])

    rx = yrgbw[1] * zrgbw[2] - yrgbw[2] * zrgbw[1]
    ry = xrgbw[2] * zrgbw[1] - xrgbw[1] * zrgbw[2]
    rz = xrgbw[1] * yrgbw[2] - xrgbw[2] * yrgbw[1]
    gx = yrgbw[2] * zrgbw[0] - yrgbw[0] * zrgbw[2]
    gy = xrgbw[0] * zrgbw[2] - xrgbw[2] * zrgbw[0]
    gz = xrgbw[2] * yrgbw[0] - xrgbw[0] * yrgbw[2]
    bx = yrgbw[0] * zrgbw[1] - yrgbw[1] * zrgbw[0]
    by = xrgbw[1] * zrgbw[0] - xrgbw[0] * zrgbw[1]
    bz = xrgbw[0] * yrgbw[1] - xrgbw[1] * yrgbw[0]
    rw = (rx * xrgbw[3] + ry * yrgbw[3] + rz * zrgbw[3]) / yrgbw[3]
    gw = (gx * xrgbw[3] + gy * yrgbw[3] + gz * zrgbw[3]) / yrgbw[3]
    bw = (bx * xrgbw[3] + by * yrgbw[3] + bz * zrgbw[3]) / yrgbw[3]
    rx = rx / rw
    ry = ry / rw
    rz = rz / rw
    gx = gx / gw
    gy = gy / gw
    gz = gz / gw
    bx = bx / bw
    by = by / bw
    bz = bz / bw
    r = rx * x + ry * y + rz * z
    g = gx * x + gy * y + gz * z
    b = bx * x + by * y + bz * z
    rgblist = []
    rgblist.append(r)
    rgblist.append(g)
    rgblist.append(b)
    w = np.amin(rgblist)
    if w < 0:
        rgblist[0] = rgblist[0] - w
        rgblist[1] = rgblist[1] - w
        rgblist[2] = rgblist[2] - w
    mag = np.amax(rgblist)
    rgblist[0] = rgblist[0] / mag
    rgblist[1] = rgblist[1] / mag
    rgblist[2] = rgblist[2] / mag
    return rgblist


def FalseColor_FromSpec(TE, lam):
    SR = datalib.SR_InGaAsSb(lam)
    X = numlib.Integrate(TE, lam, 2.25e-06, 1e-05)
    Y = numlib.Integrate(TE * SR, lam, 1.9e-06, 2.25e-06)
    Z = numlib.Integrate(TE * SR, lam, 4e-07, 1.9e-06)
    tot = X + Y + Z
    x = X / tot
    y = Y / tot
    z = Z / tot
    xrgbw = [
     0.67, 0.21, 0.15, 0.3127]
    yrgbw = [0.33, 0.71, 0.06, 0.3291]
    zrgbw = []
    for i in range(0, len(xrgbw)):
        zrgbw.append(1.0 - xrgbw[i] - yrgbw[i])

    rx = yrgbw[1] * zrgbw[2] - yrgbw[2] * zrgbw[1]
    ry = xrgbw[2] * zrgbw[1] - xrgbw[1] * zrgbw[2]
    rz = xrgbw[1] * yrgbw[2] - xrgbw[2] * yrgbw[1]
    gx = yrgbw[2] * zrgbw[0] - yrgbw[0] * zrgbw[2]
    gy = xrgbw[0] * zrgbw[2] - xrgbw[2] * zrgbw[0]
    gz = xrgbw[2] * yrgbw[0] - xrgbw[0] * yrgbw[2]
    bx = yrgbw[0] * zrgbw[1] - yrgbw[1] * zrgbw[0]
    by = xrgbw[1] * zrgbw[0] - xrgbw[0] * zrgbw[1]
    bz = xrgbw[0] * yrgbw[1] - xrgbw[1] * yrgbw[0]
    rw = (rx * xrgbw[3] + ry * yrgbw[3] + rz * zrgbw[3]) / yrgbw[3]
    gw = (gx * xrgbw[3] + gy * yrgbw[3] + gz * zrgbw[3]) / yrgbw[3]
    bw = (bx * xrgbw[3] + by * yrgbw[3] + bz * zrgbw[3]) / yrgbw[3]
    rx = rx / rw
    ry = ry / rw
    rz = rz / rw
    gx = gx / gw
    gy = gy / gw
    gz = gz / gw
    bx = bx / bw
    by = by / bw
    bz = bz / bw
    r = rx * x + ry * y + rz * z
    g = gx * x + gy * y + gz * z
    b = bx * x + by * y + bz * z
    rgblist = []
    rgblist.append(r)
    rgblist.append(g)
    rgblist.append(b)
    w = np.amin(rgblist)
    if w < 0:
        rgblist[0] = rgblist[0] - w
        rgblist[1] = rgblist[1] - w
        rgblist[2] = rgblist[2] - w
    mag = np.amax(rgblist)
    rgblist[0] = rgblist[0] / mag
    rgblist[1] = rgblist[1] / mag
    rgblist[2] = rgblist[2] / mag
    return rgblist


def RenderColor(TE, lam, string):
    fig, ax = plt.subplots()
    cierbg = RGB_FromSpec(TE, lam)
    x, y = (0.0, 0.0)
    circle = Circle(xy=(x, y * 1.2), radius=0.4, fc=cierbg)
    ax.add_patch(circle)
    ax.annotate(string, xy=(x, y * 1.2 - 0.5), va='center', ha='center',
      color=cierbg)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')
    ax.set_aspect('equal')
    plt.show()
    return 1


def RenderColor_Deuteranopia(TE, lam, T):
    fig, ax = plt.subplots()
    cierbg = RGB_FromSpec(TE, lam)
    cierbg = [1.0, 0.427, 0.713]
    rb = 0.625 * cierbg[0] + 0.375 * cierbg[1]
    gb = 0.7 * cierbg[0] + 0.3 * cierbg[1]
    bb = 0.3 * cierbg[1] + 0.7 * cierbg[2]
    cbrbg = [
     rb, gb, bb]
    scal = np.amax(cbrbg)
    cbrbg = cbrbg / scal
    x, y = (0.0, 0.0)
    circle = Circle(xy=(x, y * 1.2), radius=0.4, fc=cbrbg)
    ax.add_patch(circle)
    ax.annotate(('{:4d} K'.format(T)), xy=(x, y * 1.2 - 0.5), va='center', ha='center',
      color=cbrbg)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')
    ax.set_aspect('equal')
    plt.show()
    return 1


def RenderFalseColor(TE, lam, T):
    fig, ax = plt.subplots()
    cierbg = FalseColor_FromSpec(TE, lam)
    x, y = (0.0, 0.0)
    circle = Circle(xy=(x, y * 1.2), radius=0.4, fc=cierbg)
    ax.add_patch(circle)
    ax.annotate(('{:4d} K'.format(T)), xy=(x, y * 1.2 - 0.5), va='center', ha='center',
      color=cierbg)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')
    ax.set_aspect('equal')
    plt.show()
    return 1