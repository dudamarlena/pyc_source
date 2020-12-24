# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\glacier_length\_src.py
# Compiled at: 2019-11-12 20:52:50
# Size of source mod 2**32: 28428 bytes
from itertools import combinations
import logging, networkx as nx
from networkx.exception import NetworkXNoPath
import numpy as np
from scipy.spatial import Voronoi
from scipy.ndimage import filters
from shapely.geometry import LineString, Point
from shapely.geometry import shape
from osgeo import gdal
import sys, time
from glacier_length.exceptions import LengthError
logger = logging.getLogger(__name__)

def get_all_length(src, filename0, error_filename, dem):
    """
    冰川长度终结者
    :param src: 冰川边界面图层，的.geojson格式。

    :return: allcenterlines,即 .geojson 中所有所有的所有冰川的长度。
    """
    top_head0 = '{"type":"FeatureCollection", "features":['
    top = top_head0.replace("'", ' ')
    with open(filename0, 'a') as (f):
        f.write(top)
    allcenterlines = []
    n0 = 0
    for i in src:
        sum0 = len(src)
        name1 = i['properties']['NEW_ID']
        print(name1)
        a = shape(i['geometry'])
        b = a.geom_type
        logger.debug('geometry type %s', a.geom_type)
        if b == 'MultiPolygon':
            with open(error_filename, 'a') as (f):
                f.write('\r\n')
                f.write(str(name1))
            n0 += 1
        else:
            all_outline_points, outline_pointss, all_area = _get_all_outline_points(a)
            vor = Voronoi(all_outline_points)
            print('生成了voronoi===================================================')
            graph = _graph_from_voronoi(vor, a)
            print('生成了graph==================================================')
            start_end_nodes0 = _get_end_nodes(graph)
            print(start_end_nodes0)
            print('这是start_end_nodes0。。。。。。。。。。。。。。。。。。。。')
            print(len(start_end_nodes0))
            print('这是start_end_nodes0的个数。。。。。。。。。。。。。。。。。。。。。')
            if all_area > 2510000:
                all_contours, hiers, lo, hi, all_contours_sort = _get_high_border_contour(outline_pointss, dem)
                end_high_nodes = _get_high_nodes(start_end_nodes0, vor, hiers, graph)
            else:
                all_contours, lo, hi, all_contours_sort = _get_high_border_contour2(outline_pointss, dem)
                end_high_nodes = _get_high_nodes2(start_end_nodes0, vor, hi, all_contours_sort, graph)
            print(all_contours)
            print('这是冰川 外边界点（有高程的）。。。。。。。')
            end_low_nodes = _get_low_nodes(start_end_nodes0, vor, lo, all_contours_sort, graph)
            print(end_low_nodes)
            print(end_high_nodes)
            print('====test end_low_nodes 和 end_high_nodes========================================')
            longest_path, high_xy, low_xy = _get_longest_path(end_low_nodes, end_high_nodes, vor, graph, name1)
            if len(longest_path):
                centerlin = _get_single_centerline(longest_path, vor, i, low_xy, high_xy)
                print(centerlin)
                db = '{0},'.format(centerlin)
                db1 = db.replace("'", ' ')
                with open(filename0, 'a') as (f):
                    f.write(db1)
                print('一个又一个=======================================================')
                n0 += 1
            else:
                with open(error_filename, 'a') as (f):
                    f.write('\r\n')
                    f.write(str(name1))
                n0 += 1
        print(n0, sum0)

    top_head2 = ']}'
    with open(filename0, 'a') as (f):
        f.write(top_head2)


def _get_high_threshold(all_contours):
    """
    :param all_contours:是冰川外边界的点（包含了高程）
    :return: threshold 是一个冰川的最高海拔和最低海拔的四分之三， 阈值 。
    """
    all_contours2 = all_contours
    for i in range(len(all_contours2) - 1):
        for j in range(len(all_contours2) - 1 - i):
            if all_contours2[j]['value'] > all_contours2[(j + 1)]['value']:
                all_contours2[j], all_contours2[j + 1] = all_contours2[(j + 1)], all_contours2[j]

    lo = all_contours2[0]['value']
    hi = all_contours2[(-1)]['value']
    threshold = int((hi - lo) * 4 / 5 + lo)
    return (
     threshold, lo, hi)


def _get_contour_value(dem, x, y):
    """
    如果提取高程出错，那一定是因为dem的坐标和冰川边界的坐标不一致。
    :param dem: 区域范围内的dem。
    :param x: x坐标
    :param y: y坐标
    :return: 我 希望 返回的 data 是一个数值，一个坐标一个值。
    """
    gdal.AllRegister()
    dataset = gdal.Open(dem, gdal.GA_ReadOnly)
    if dataset is None:
        sys.exit(1)
    transform = dataset.GetGeoTransform()
    x_origin = transform[0]
    y_origin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    xOffset = int((x - x_origin) / pixelWidth)
    yOffset = int((y - y_origin) / pixelHeight)
    band = dataset.GetRasterBand(1)
    data = band.ReadAsArray(xOffset, yOffset, 1, 1)
    return data[0][0]


def _get_high_border_contour(outline_pointss, dem):
    """
    :param outline_pointss: 是 get_all_outline_points(a)中得到的，冰川外边界的点。形式是[( , ),( , ),( , )...]
    :return: all_contours [{( ，):值},{( , ):值}..] 是所有外边界点(包含了高程)；
             hiers [] 是30个点内最高的点；
             lo 冰川边界的最低海拔值。
             hi 冰川边界的最高海拔值。
             all_contours_sort 是排序好的 all_contours。
    """
    all_contours = []
    for lis in outline_pointss:
        coo_contours = {}
        vv = _get_contour_value(dem, lis[0], lis[1])
        coo_contours['type'] = Point
        coo_contours['coordinates'] = lis
        coo_contours['value'] = vv
        all_contours.append(coo_contours)

    all_contours_sort = sorted(all_contours, key=(lambda x: x['value']), reverse=False)
    hiers = []
    nn = [nn for nn in range(0, len(all_contours), 40)]
    if len(all_contours) / 40 == 0:
        print(nn)
    else:
        nn.append(len(all_contours))
    for i in range(len(nn)):
        if i < len(nn) - 1:
            hii = []
            for j in all_contours[nn[i]:nn[(i + 1)]]:
                hii.append(j)

            hier = sorted(hii, key=(lambda x: x['value']), reverse=False)[(-1)]
            threshold, lo, hi = _get_high_threshold(all_contours)
            if hier['value'] > threshold:
                hiers.append(hier)

    return (
     all_contours, hiers, lo, hi, all_contours_sort)


def _get_high_border_contour2(outline_pointss, dem):
    """
    和get_high_border_contour 的区别是 这个函数是提供给面积小的冰川。只找一个最高点而不是一个列表的最高点。
    :param outline_pointss: 是get_all_outline_points(a)中得到的，冰川外边界的点。形式是[( , ),( , ),( , )...]
    :return: all_contours [{( ，):值},{( , ):值}..]是所有外边界点(包含了高程)；
             hiers [] ；
             lo 冰川边界的最低海拔值。
             hi 冰川边界的最高海拔值。
             all_contours_sort 是排序好的 all_contours。
    """
    all_contours = []
    for lis in outline_pointss:
        coo_contours = {}
        vv = _get_contour_value(dem, lis[0], lis[1])
        coo_contours['type'] = Point
        coo_contours['coordinates'] = lis
        coo_contours['value'] = vv
        all_contours.append(coo_contours)

    all_contours_sort = sorted(all_contours, key=(lambda x: x['value']), reverse=False)
    threshold, lo, hi = _get_high_threshold(all_contours)
    return (all_contours, lo, hi, all_contours_sort)


def _get_all_outline_points(a):
    """
    :param a:    a = shape(i["geometry"]), //for i in src: //src = fiona.open(url + "json_818_2.geojson", "r")
    :return: all_outline_points 内外边界所有的点。
             outline_pointss 是外边界的所有的点。
             all_area 冰川的面积， 用来做判断用的。
    """
    all_outline_points = []
    outline_pointss = []
    all_area = a.area
    print(all_area)
    for subai in a.interiors:
        points = []
        max_len = 0.5
        for previous, current in zip(subai.coords, subai.coords[1:]):
            line_segment = LineString([previous, current])
            points.extend([line_segment.interpolate(max_len * i).coords[0] for i in range(int(line_segment.length / max_len))])
            points.append(current)

        outline = LineString(points)
        outline_points = outline.coords
        simplification = 0.05
        max_points = 5000
        simplification_updated = simplification
        while len(outline_points) > max_points:
            simplification_updated += simplification
            outline_points = outline.simplify(simplification_updated).coords

        print('a.interiors finished==================================================')
        all_outline_points.extend(outline_points)

    points0 = []
    max_len = 0.5
    for previous, current in zip(a.exterior.coords, a.exterior.coords[1:]):
        line_segment0 = LineString([previous, current])
        points0.extend([line_segment0.interpolate(max_len * i).coords[0] for i in range(int(line_segment0.length / max_len))])
        points0.append(current)

    outline0 = LineString(points0)
    outline_points0 = outline0.coords
    simplification = 0.05
    max_points = 5000
    simplification_updated0 = simplification
    while len(outline_points0) > max_points:
        simplification_updated0 += simplification
        outline_points0 = outline0.simplify(simplification_updated0).coords

    print('a.exterior finished==================================================')
    all_outline_points.extend(outline_points0)
    outline_pointss.extend(outline_points0)
    return (all_outline_points, outline_pointss, all_area)


def _yield_ridge_vertices(vor, geometry, dist=False):
    """Yield Voronoi ridge vertices within geometry."""
    for x, y in vor.ridge_vertices:
        if x < 0 or y < 0:
            continue
        point1 = Point(vor.vertices[[x, y]][0])
        point2 = Point(vor.vertices[[x, y]][1])
        if point1.within(geometry) and point2.within(geometry):
            if dist:
                yield (
                 x, y, point1.distance(point2))
            else:
                yield (
                 x, y)


def _graph_from_voronoi(vor, geometry):
    """Return networkx.Graph from Voronoi diagram within geometry."""
    graph = nx.Graph()
    for x, y, dist in _yield_ridge_vertices(vor, geometry, dist=True):
        graph.add_nodes_from([x, y])
        graph.add_edge(x, y, weight=dist)

    return graph


def _get_end_nodes(graph):
    """
    :param graph:graph = nx.Graph()
    :return: 返回graph中只有一个邻居节点的节点列表（为后面找到和最高点最低点相近的节点做铺垫）。
    """
    return [i for i in graph.nodes() if len(list(graph.neighbors(i))) == 1]


def _bubble_sort(points_geo):
    """
    ：使用了bubble_sort算法进行排序。
    :param points_geo: 是从arcgis中获取的最高点最低点的 POINT 的geojson文件。
    :return: 返回的是排序好的最高点最低点。points_geo1[0]就是最低点。
    """
    points_geo1 = []
    for x in points_geo:
        points_geo1.append(x)

    for i in range(len(points_geo1) - 1):
        for j in range(len(points_geo1) - 1 - i):
            if points_geo1[j]['properties']['RASTERVALU'] > points_geo1[(j + 1)]['properties']['RASTERVALU']:
                points_geo1[j], points_geo1[j + 1] = points_geo1[(j + 1)], points_geo1[j]

    highest_value = points_geo1[(-1)]['properties']['RASTERVALU']
    lowest_value = points_geo1[0]['properties']['RASTERVALU']
    return (
     points_geo1, highest_value, lowest_value)


def _get_low_nodes(start_end_nodes, vor, lo, all_contours_sort, graph):
    """
    :param start_end_nodes: graph中只有一个邻居节点的节点列表。
    :param vor:是之前生成的vor。
    :param lo: 冰川最低海拔， 是一个数值。
    :param all_contours_sort:排序好的 冰川外边界 所有点（包含了高程）。
    :param graph:
    :return: 返回最低点附近的节点列表的第一个，因为我只希望最低点有且只有一个。
             向graph中添加了一个（最低点）节点，和（最低点和接近它的一个node）边，和距离。
    """
    end_low_nodes = []
    low_nodes = {}
    n = 0
    for v in all_contours_sort[0:]:
        if v['value'] == lo:
            n = n + 1

    look = []
    for q in all_contours_sort[0:n]:
        po = Point(q['coordinates'])
        zz = {}
        for j in start_end_nodes:
            jj = Point(vor.vertices[j])
            dio = jj.distance(po)
            low_nodes[j] = dio

        aa = sorted((low_nodes.items()), key=(lambda x: x[1]), reverse=False)
        zz['coordinates'] = q['coordinates']
        zz['dis'] = aa[0]
        look.append(zz)
        low_nodes.clear()

    look_gd = sorted(look, key=(lambda x: x['dis']), reverse=False)[0]
    graph.add_node(look_gd['coordinates'])
    graph.add_edge((look_gd['coordinates']), (look_gd['dis'][0]), weight=(look_gd['dis'][1]))
    end_low_nodes.append(look_gd['coordinates'])
    return end_low_nodes


def _get_high_nodes2(start_end_nodes, vor, hi, all_contours_sort, graph):
    """
    原理同get_low_nodes函数。
    和get_high_nodes2的区别是 这是为小冰川准备的， 只想要一个最高点。
    :param start_end_nodes:
    :param vor:
    :param hi:
    :param all_contours_sort:
    :param graph:
    :return:
    """
    end_high_nodes = []
    high_nodes = {}
    n = 0
    for v in all_contours_sort:
        if v['value'] == hi:
            n = n + 1

    look = []
    for q in all_contours_sort[-n:]:
        po = Point(q['coordinates'])
        zz = {}
        for j in start_end_nodes:
            jj = Point(vor.vertices[j])
            dio = jj.distance(po)
            high_nodes[j] = dio

        aa = sorted((high_nodes.items()), key=(lambda x: x[1]), reverse=False)
        zz['coordinates'] = q['coordinates']
        zz['dis'] = aa[0]
        look.append(zz)
        high_nodes.clear()

    look_gd = sorted(look, key=(lambda x: x['dis']), reverse=False)[0]
    graph.add_node(look_gd['coordinates'])
    graph.add_edge((look_gd['coordinates']), (look_gd['dis'][0]), weight=(look_gd['dis'][1]))
    end_high_nodes.append(look_gd['coordinates'])
    return end_high_nodes


def _get_high_nodes(start_end_nodes, vor, hiers, graph):
    """
    :param start_end_nodes: graph中只有一个邻居节点的节点列表。
    :param vor: 是之前生成的vor.
    :param hiers: 是大冰川特有的，对大冰川最高点的选取是一个列表，多个值。
    :param graph:
    :return: 返回每个最高点附近的最近的一个节点，最后生成总的列表。
             且向graph中添加了。
    """
    end_high_nodes = []
    high_nodes = {}
    for q in hiers:
        po = Point(q['coordinates'])
        for j in start_end_nodes:
            jj = Point(vor.vertices[j])
            dio = po.distance(jj)
            high_nodes[j] = dio

        aa = sorted((high_nodes.items()), key=(lambda x: x[1]), reverse=False)
        graph.add_node(q['coordinates'])
        graph.add_edge((q['coordinates']), (aa[0][0]), weight=(po.distance(Point(vor.vertices[aa[0][0]]))))
        end_high_nodes.append(q['coordinates'])
        high_nodes.clear()

    return end_high_nodes


def _get_longest_paths(end_low_nodes, end_high_nodes, graph):
    """
    :param end_low_nodes: source节点。
    :param end_high_nodes: target节点。
    :param graph: graph = nx.Graph（）。
    :param maxnum: 这里的maxnum参数我需要最后修改。
    :return: 返回每个最高点附近的最近的一个节点，最后生成总的列表。
    """

    def get_paths_distances():
        for node1 in end_low_nodes:
            for node2 in end_high_nodes:
                try:
                    yield nx.single_source_dijkstra(G=graph, source=node1, target=node2, weight='weight')
                except NetworkXNoPath:
                    continue

    return [x for y, x in sorted((get_paths_distances()), reverse=True)][:len(end_high_nodes)]


def _get_longest_path(end_low_nodes, end_high_nodes, vor, graph, name1):
    """
    在这个函数里，我做了一个判断，如果最后得到的最长路径列表是空，就跳过，记录在txt中。
    :param end_low_nodes: source节点。
    :param end_high_nodes: target节点。
    :param graph: graph = nx.Graph（）。
    :param name1: 冰川的名称。
    :param maxnum: 这里的maxnum参数我需要最后修改。
    :return: 只返回最长的那条线 or 空列表。
    """

    def get_paths_distances():
        for node1 in end_low_nodes:
            for node2 in end_high_nodes:
                try:
                    yield nx.single_source_dijkstra(G=graph, source=node1, target=node2, weight='weight')
                except NetworkXNoPath:
                    continue

    aha = [x for y, x in sorted((get_paths_distances()), reverse=True)]
    if len(aha):
        high_xy = [x for y, x in sorted((get_paths_distances()), reverse=True)][0][(-1)]
        low_xy = [x for y, x in sorted((get_paths_distances()), reverse=True)][0][0]
        return ([x for y, x in sorted((get_paths_distances()), reverse=True)][0], high_xy, low_xy)
    high_xy = 0
    low_xy = 0
    lis5 = []
    return (lis5, high_xy, low_xy)


def _get_single_centerline(longest_path, vor, one, low_xy, high_xy):
    """
    [
        {"type":"Feature","geometry":{"type":"LineString","coordinates":[[],[],[],[]]},"properties":{"OBJECTID":7139}}
    ]
    :param longest_path:是get_longest_path()函数的产物。
    :param vor:
    :param one:是.geojson文件里的每一条信息。
    :param low_xy:是一条冰川中的最低点的点位置坐标，它是个tuple形式。
    :return:
    """
    lis1 = list(low_xy)
    liss = []
    liss.append(lis1)
    aa = vor.vertices[longest_path[1:-1]].tolist()
    liss.extend(aa)
    lis2 = list(high_xy)
    liss.append(lis2)
    centerline0 = LineString(liss)
    centerlin_sm = _smooth_linestring(centerline0, low_xy, high_xy, smooth_sigma=2)
    centerline1 = []
    for i in centerlin_sm.coords:
        ll = list(i)
        centerline1.append(ll)

    name = one['properties']['NEW_ID']
    form1 = '{"type":"Feature","geometry":{"type":"LineString",'
    form2 = '"coordinates":{0}'.format(centerline1)
    form3 = '},"properties":{'
    form4 = '"NEW_ID":"{0}"'.format(name)
    form5 = '}}'
    form = form1 + form2 + form3 + form4 + form5
    return form


def _smooth_linestring(linestring, low_xy, high_xy, smooth_sigma=2):
    """Use a gauss filter to smooth out the LineString coordinates."""
    lis1 = list(zip(np.array(filters.gaussian_filter1d((linestring.xy[0]), smooth_sigma, mode='nearest', truncate=3)), np.array(filters.gaussian_filter1d((linestring.xy[1]), smooth_sigma, mode='nearest', truncate=3))))
    lis2 = list(low_xy)
    lis22 = list(high_xy)
    lis3 = []
    lis3.append(lis2)
    lis3.extend(lis1)
    lis3.append(lis22)
    tuple1 = tuple(lis3)
    return LineString(tuple1)


def _get_all_data(filename, allcenterlines):
    top_head0 = '{"type":"FeatureCollection", "features":'
    top_head1 = '{0}'.format(allcenterlines)
    top_head2 = '}'
    top_head = top_head0 + top_head1 + top_head2
    top = top_head.replace("'", ' ')
    with open(filename, 'w') as (f):
        f.write(top)


def _get_all_data1(filename, centerline):
    top_head1 = '{0}'.format(centerline)
    top_head2 = '}'
    top_head = top_head1 + top_head2
    top = top_head.replace("'", ' ')
    with open(filename, 'w') as (f):
        f.write(top)