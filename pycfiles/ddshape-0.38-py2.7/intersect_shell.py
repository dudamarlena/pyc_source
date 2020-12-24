# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ddshape\intersect_shell.py
# Compiled at: 2015-06-05 08:05:05
import inc

def intersect_shell(index=1, data='', a_center=(0, 0, 0), b_center=(0, 0, 0), out_radius=25, shell=3, precision=1):
    """
    create data with a intersection operation of A sphere(main) and B sphere(used to bool with A)
    :param index: a number which indicate the line numbers of main shape data
    :param data: string with all shape data combined
    :param a_center: a_center of a shell
    :param b_center: a_center of b shell
    :param out_radius: the out radius of sphere
    :param shell: the thickness of the sphere
    :return: int, float
    """
    number_range = inc.get_range(out_radius=out_radius, precision=precision)
    for j in range(number_range[0], number_range[1]):
        for k in range(number_range[2], number_range[3]):
            for m in range(number_range[4], number_range[5]):
                if intersect_shell_validate((j, k, m), a_center, b_center, out_radius, shell, precision):
                    data += inc.print_line(index, a_center, (j, k, m), precision)
                    index += 1

    return (
     index, data)


def intersect_shell_validate(relative_point=(0, 0, 0), a_center=(0, 0, 0), b_center=(0, 0, 0), out_radius=25, shell=3, precision=1):
    """
    the function that check if the point can be write
    :param relative_point: the relative point of the A sphere without add a_center point
    :param a_center: a_center of A sphere(main sphere)
    :param b_center: offset a_center means the a_center of B sphere
    :param out_radius: the out radius of A sphere
    :param shell: the thickness of A sphere
    :return: bool
    """
    sqrt_sum = relative_point[0] ** 2 + relative_point[1] ** 2 + relative_point[2] ** 2
    if not ((out_radius - shell) * precision) ** 2 <= sqrt_sum <= (out_radius * precision) ** 2:
        return False
    point = (relative_point[0] + a_center[0] * precision,
     relative_point[1] + a_center[1] * precision,
     relative_point[2] + a_center[2] * precision)
    offset_sum = (point[0] - b_center[0] * precision) ** 2 + (point[1] - b_center[1] * precision) ** 2 + (point[2] - b_center[2] * precision) ** 2
    if offset_sum <= (out_radius * precision) ** 2:
        return False
    return True