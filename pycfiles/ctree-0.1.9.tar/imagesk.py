# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/imagesk.py
# Compiled at: 2013-09-24 00:46:30
from scipy.misc.pilutil import imresize
import numpy as num, wx, string

def img_normalize(img):
    img -= num.min(img)
    v = num.max(img)
    if v > 0:
        img /= v
    return img


def double2mono8(img_d, donormalize=True):
    img_8 = img_d.copy()
    if not img_8.dtype == num.dtype('double'):
        img_8 = img_8.astype(num.double)
    if donormalize:
        img_8 -= num.min(img_8)
        v = num.max(img_8)
        if v > 0:
            img_8 *= 255.0 / v
    img_8 = img_8.round().astype(num.uint8)
    return img_8


def draw_image(img, windowsize=None, zoomaxes=None):
    if zoomaxes is None:
        zoomaxes = [
         0, img.shape[1] - 1, 0, img.shape[0] - 1]
    if int(zoomaxes[3]) < int(zoomaxes[2]) or int(zoomaxes[1]) < int(zoomaxes[0]):
        raise ValueError('Invalid zoom axes input')
    scale_img = img.copy()
    scale_img = scale_img[int(zoomaxes[2]):int(zoomaxes[3] + 1), int(zoomaxes[0]):int(zoomaxes[1] + 1)]
    if windowsize is not None:
        scale_x = float(windowsize[1]) / float(scale_img.shape[1])
        scale_y = float(windowsize[0]) / float(scale_img.shape[0])
        if scale_x < scale_y:
            size_x = windowsize[1]
            size_y = scale_img.shape[0] * scale_x
            resize = scale_x
        else:
            size_y = windowsize[0]
            size_x = scale_img.shape[1] * scale_y
            resize = scale_y
        scale_img = imresize(scale_img, (int(size_y), int(size_x)))
    if scale_img.ndim == 3:
        if not scale_img.dtype == 'uint8':
            scale_img = scale_img.astype('uint8')
    elif scale_img.dtype == 'uint8':
        scale_img = to_rgb8('MONO8', scale_img)
    elif scale_img.dtype == 'double':
        scale_img = num.astype(img_normalize(scale_img) * 255.0, 'uint8')
        scale_img = to_rgb8('MONO8', scale_img)
    h, w, three = scale_img.shape
    img_size = [h, w]
    image = wx.EmptyImage(w, h)
    image.SetData(scale_img.tostring())
    bmp = wx.BitmapFromImage(image)
    return (
     bmp, resize, img_size)


def draw_annotated_image(img, pointlists=None, linelists=None, circlelists=None, windowsize=None, zoomaxes=None, pointcolors=None, linecolors=None, circlecolors=None, pointsizes=None, linewidth=None, circlewidths=None):
    if zoomaxes is None:
        zoomaxes = [
         0, img.shape[1] - 1, 0, img.shape[0] - 1]
    if int(zoomaxes[3]) < int(zoomaxes[2]) or int(zoomaxes[1]) < int(zoomaxes[0]):
        raise ValueError('Invalid zoom axes input')
    scale_img = img.copy()
    scale_img = scale_img[int(zoomaxes[2]):int(zoomaxes[3] + 1), int(zoomaxes[0]):int(zoomaxes[1] + 1)]
    xoffset = -zoomaxes[0]
    yoffset = -zoomaxes[2]
    if windowsize is not None:
        scale_x = float(windowsize[1]) / float(scale_img.shape[1])
        scale_y = float(windowsize[0]) / float(scale_img.shape[0])
        if scale_x < scale_y:
            size_x = windowsize[1]
            size_y = scale_img.shape[0] * scale_x
            resize = scale_x
        else:
            size_y = windowsize[0]
            size_x = scale_img.shape[1] * scale_y
            resize = scale_y
        scale_img = imresize(scale_img, (int(size_y), int(size_x)))
    if scale_img.ndim == 3:
        if not scale_img.dtype == 'uint8':
            scale_img = scale_img.astype('uint8')
    elif scale_img.dtype == 'uint8':
        scale_img = to_rgb8('MONO8', scale_img)
    elif scale_img.dtype == 'double':
        scale_img = num.astype(img_normalize(scale_img) * 255.0, 'uint8')
        scale_img = to_rgb8('MONO8', scale_img)
    h, w, three = scale_img.shape
    img_size = [h, w]
    image = wx.EmptyImage(w, h)
    image.SetData(scale_img.tostring())
    bmp = wx.BitmapFromImage(image)
    drawDC = wx.MemoryDC()
    drawDC.SelectObject(bmp)
    drawDC.SetPen(wx.Pen('GREEN'))
    drawDC.SetBrush(wx.Brush(wx.Colour(255, 255, 255), wx.TRANSPARENT))
    point_radius = 8
    if pointlists is not None:
        pointcolor = 'GREEN'
        for i, points in enumerate(pointlists):
            if pointcolors is not None and len(pointcolors) > i:
                pointcolor = wx.Colour(pointcolors[i][0], pointcolors[i][1], pointcolors[i][2])
            if pointsizes is not None and len(pointsizes) > i:
                point_radius = pointsizes[i]
            drawDC.SetPen(wx.Pen(colour=pointcolor, width=point_radius))
            for j, pt in enumerate(points):
                x = int((xoffset + pt[0]) * resize)
                y = int((yoffset + pt[1]) * resize)
                if x >= 0 and x < img_size[1] and y >= 0 and y < img_size[0]:
                    drawDC.DrawCircle(x, y, point_radius)

    if linelists is not None:
        linecolor = 'GREEN'
        if linewidth is None:
            linewidth = 1
        for i, lines in enumerate(linelists):
            points = []
            for j, pt in enumerate(lines):
                x = int((xoffset + pt[0]) * resize)
                y = int((yoffset + pt[1]) * resize)
                newpoint = wx.Point(x, y)
                if j < 1 or not newpoint == lastpoint:
                    points.append(newpoint)
                    lastpoint = newpoint

            if len(points) == 0:
                continue
            if len(points) == 1:
                points.append(newpoint)
            if linecolors is not None and len(linecolors) > i:
                linecolor = wx.Colour(linecolors[i][0], linecolors[i][1], linecolors[i][2])
            drawDC.SetPen(wx.Pen(colour=linecolor, width=linewidth))
            drawDC.DrawLines(points)

    if circlelists is not None:
        circlecolor = 'GREEN'
        for i, circles in enumerate(circlelists):
            if circlecolors is not None and len(circlecolors) > i:
                circlecolor = wx.Colour(circlecolors[i][0], circlecolors[i][1], circlecolors[i][2])
            if circlewidths is not None and len(circlewidths) > i:
                circlewidth = circlewidths[i]
            drawDC.SetPen(wx.Pen(colour=circlecolor, width=circlewidth))
            if circlewidths is not None and len(circlewidths) > i:
                circlewidth = circlewidths[i]
            for j, circle in enumerate(circles):
                x = int((xoffset + circle[0]) * resize)
                y = int((yoffset + circle[1]) * resize)
                r = int(circle[2] * resize)
                if x >= 0 and x < img_size[1] and y >= 0 and y < img_size[0]:
                    drawDC.DrawCircle(x, y, r)

    return (
     bmp, resize, img_size)


def add_annotations(bmp, resize, pointlists=None, linelists=None, zoomaxes=[
 0, 10, 0, 10], pointcolors=None, linecolors=None, pointsizes=None, linewidth=None):
    if zoomaxes is None or int(zoomaxes[3]) < int(zoomaxes[2]) or int(zoomaxes[1]) < int(zoomaxes[0]):
        raise ValueError('Invalid zoom axes input')
    xoffset = -zoomaxes[0]
    yoffset = -zoomaxes[2]
    drawDC = wx.MemoryDC()
    drawDC.SelectObject(bmp)
    drawDC.SetPen(wx.Pen('GREEN'))
    drawDC.SetBrush(wx.Brush(wx.Colour(255, 255, 255), wx.TRANSPARENT))
    point_radius = 8
    if pointlists is not None:
        for i, points in enumerate(pointlists):
            if pointcolors is not None and len(pointcolors) > i:
                c = wx.Colour(pointcolors[i][0], pointcolors[i][1], pointcolors[i][2])
                drawDC.SetPen(wx.Pen(c))
            if pointsizes is not None and len(pointsizes) > i:
                point_radius = pointsizes[i]
            for j, pt in enumerate(points):
                x = int((xoffset + pt[0]) * resize)
                y = int((yoffset + pt[1]) * resize)
                drawDC.DrawCircle(x, y, point_radius)

    if linelists is not None:
        linecolor = 'GREEN'
        if linewidth is None:
            linewidth = 1
        for i, lines in enumerate(linelists):
            points = []
            for j, pt in enumerate(lines):
                x = int((xoffset + pt[0]) * resize)
                y = int((yoffset + pt[1]) * resize)
                newpoint = wx.Point(x, y)
                if j < 1 or not newpoint == lastpoint:
                    points.append(newpoint)
                    lastpoint = newpoint

            if len(points) == 0:
                continue
            if len(points) == 1:
                points.append(newpoint)
            if linecolors is not None and len(linecolors) > i:
                linecolor = wx.Colour(linecolors[i][0], linecolors[i][1], linecolors[i][2])
            drawDC.SetPen(wx.Pen(colour=linecolor, width=linewidth))
            drawDC.DrawLines(points)

    return bmp


def draw_circle(x, y, r, color=(0, 255, 0), step=10 * num.pi / 180.0):
    lines = []
    aa = 0
    xx = x + num.cos(aa) * r
    yy = y + num.sin(aa) * r
    for aa in num.arange(0.0, 2.0 * num.pi + step, step):
        xprev = xx
        yprev = yy
        xx = x + num.cos(aa) * r
        yy = y + num.sin(aa) * r
        lines.append([xprev + 1, yprev + 1, xx + 1, yy + 1, color])

    return lines


def draw_line(x0, y0, x1, y1, color=(0, 255, 0)):
    linesegs = [
     [
      x0, y0, x1, y1, color]]
    return linesegs


def draw_arc(xc, yc, r, theta0, theta1, color=(0, 255, 0), step=10 * num.pi / 180.0):
    lines = []
    aa = theta0
    xx = xc + num.cos(aa) * r
    yy = yc + num.sin(aa) * r
    for aa in num.arange(theta0, theta1, step):
        xprev = xx
        yprev = yy
        xx = xc + num.cos(aa) * r
        yy = yc + num.sin(aa) * r
        lines.append([xprev + 1, yprev + 1, xx + 1, yy + 1, color])

    return lines


def zoom_linesegs_and_image(linesegs, im, zoomaxes):
    if zoomaxes is None or int(zoomaxes[3]) < int(zoomaxes[2]) or int(zoomaxes[1]) < int(zoomaxes[0]):
        raise ValueError('Invalid zoom axes input')
    zoomim = im[int(zoomaxes[2]):int(zoomaxes[3] + 1), int(zoomaxes[0]):int(zoomaxes[1] + 1)]
    xoffset = -int(zoomaxes[0]) - 0.5
    yoffset = -int(zoomaxes[2]) - 0.5
    for i, line in enumerate(linesegs):
        linesegs[i][0] += xoffset
        linesegs[i][1] += yoffset
        linesegs[i][2] += xoffset
        linesegs[i][3] += yoffset

    return (
     linesegs, zoomim)


def separate_linesegs_colors(linesegs):
    lines = []
    colors = []
    for i, line in enumerate(linesegs):
        lines.append(line[0:4])
        color = (line[4][0] / 255.0, line[4][1] / 255.0, line[4][2] / 255.0, 1)
        colors.append(color)

    return (
     lines, colors)


def to_rgb8(inputtype, img):
    if string.lower(inputtype) == 'mono8':
        rgb_img = img.reshape(img.shape[0], img.shape[1], 1)
        rgb_img = num.tile(rgb_img, (1, 1, 3))
    else:
        print 'Inputtype: ' + inputtype + ' not supported.'
        rgb_img = img
    return rgb_img