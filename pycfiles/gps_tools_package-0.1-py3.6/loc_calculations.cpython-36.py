# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GPS_Tools\loc_calculations.py
# Compiled at: 2019-03-27 03:50:45
# Size of source mod 2**32: 15675 bytes
import math
from GPS_Tools.loc_utils import radians_to_deg, deg_to_radians, transform_to_cartesian, transform_to_gps, GPS, get_photos_names_from_dir
import numpy as np
RZ = 6371008.8

def check_distance_threshold(first_point_latitude, first_point_longitude, second_point_latitude, second_point_longitude, distance_threshold):
    """Check if object is within distance threshold (in meters) of the other object, also return azimuth from first point to second
    
    :param first_point_latitude: first point latitude
    :type first_point_latitude: float
    :param first_point_longitude: first point longitude
    :type first_point_longitude: float
    :param second_point_latitude: second point latitude
    :type second_point_latitude: float
    :param second_point_longitude: second point longitude
    :type second_point_longitude: float
    :param distance_threshold: distance threshold in meters
    :type distance_threshold: float
    :return: bool determining if points are within given dange and azimuth of their position (in that order)
    :rtype: [bool, float, float]
    """
    distance = calculate_distance(first_point_latitude, first_point_longitude, second_point_latitude, second_point_longitude)
    azimuth = calculate_azimuth(first_point_latitude, first_point_longitude, second_point_latitude, second_point_longitude)
    if distance > distance_threshold:
        return (False, distance, azimuth)
    else:
        return (
         True, distance, azimuth)


def calculate_azimuth_points(first_point, second_point):
    """Calculate azimuth between two GPS points
    Source: https://www.movable-type.co.uk/scripts/latlong.html

    :param first_point: first point gps coordinates
    :type first_point: GPS class
    :param second_point: second point gps coordinates
    :type second_point: GPS class
    :return: azimuth in degrees
    :rtype: float
    """
    azimuth = calculate_azimuth(first_point.latitude, first_point.longitude, second_point.latitude, second_point.longitude)
    return azimuth


def calculate_azimuth(first_point_latitude, first_point_longitude, second_point_latitude, second_point_longitude):
    """Calculate azimuth between two GPS points given raw coordinates 
    
    Source: https://www.movable-type.co.uk/scripts/latlong.html
    Formula: θ = atan2(sin Δλ ⋅ cos φ2, cos φ1 ⋅ sin φ2 − sin φ1 ⋅ cos φ2 ⋅ cos Δλ)

    :param first_point_latitude: latitude of first point
    :type first_point_latitude: float
    :param first_point_longitude: longitude of first point
    :type first_point_longitude: float
    :param second_point_latitude: latitude of second point
    :type second_point_latitude: float
    :param second_point_longitude: longitude of second point
    :type second_point_longitude: float
    :return: azimuth in degrees
    :rtype: float
    """
    longitude_difference = deg_to_radians(second_point_longitude - first_point_longitude)
    latitude_first_point_rad = deg_to_radians(first_point_latitude)
    latitude_secon_point_rad = deg_to_radians(second_point_latitude)
    y_prod = math.sin(longitude_difference) * math.cos(latitude_secon_point_rad)
    x_prod = math.cos(latitude_first_point_rad) * math.sin(latitude_secon_point_rad) - math.sin(latitude_first_point_rad) * math.cos(latitude_secon_point_rad) * math.cos(longitude_difference)
    degResult = radians_to_deg(math.atan2(y_prod, x_prod))
    result = (degResult + 360) % 360
    return result


def calculate_point_geographic_coordinates(point_azimuth, first_point_latitude, first_point_longitude, distance):
    """Calculate single point coordinates based on azimuth distance and starting gps points"
    
     Source: https://www.movable-type.co.uk/scripts/latlong.html

    :param point_azimuth: azimuth to searched point
    :type point_azimuth: float
    :param first_point_latitude: latitude of known point
    :type first_point_latitude: float
    :param first_point_longitude: longitude of known point
    :type first_point_longitude: float
    :param distance: distance to searched point
    :type distance: float
    :return: coordinates of searched gps point
    :rtype: class GPS
    """
    searched_point_coordinates = GPS()
    first_point_latitude_rad = deg_to_radians(first_point_latitude)
    first_point_longitude_rad = deg_to_radians(first_point_longitude)
    azimuth_rad = deg_to_radians(point_azimuth)
    second_point_latitude = math.asin(math.sin(first_point_latitude_rad) * math.cos(distance / RZ) + math.cos(first_point_latitude_rad) * math.sin(distance / RZ) * math.cos(azimuth_rad))
    second_point_longitude = first_point_longitude_rad + math.atan2(math.sin(azimuth_rad) * math.sin(distance / RZ) * math.cos(first_point_latitude_rad), math.cos(distance / RZ) - math.sin(first_point_latitude_rad) * math.sin(second_point_latitude))
    second_point_latitude_deg = radians_to_deg(second_point_latitude)
    second_point_longitude_deg = radians_to_deg(second_point_longitude)
    second_point_longitude_deg = (second_point_longitude_deg + 540) % 360 - 180
    searched_point_coordinates.latitude = second_point_latitude_deg
    searched_point_coordinates.longitude = second_point_longitude_deg
    searched_point_coordinates.altitude = 0
    return searched_point_coordinates


def calculate_side_point_azimuth(absolute_angle_to_point, azimuth):
    """ Calculate absolute azimuth of given point based on relative azimuth

    :param absolute_angle_to_point: Relative angle to point
    :type absolute_angle_to_point: float
    :param azimuth: global azimuth
    :type azimuth: float
    """
    side_point_azimuth = absolute_angle_to_point + azimuth
    side_point_full_azimuth = (side_point_azimuth + 360) % 360
    return side_point_full_azimuth


def calculate_distance(first_point_lat, first_point_long, second_point_lat, second_point_long):
    """
    Calculate distance between two gps points in world

    :param first_point_lat: first point latutude
    :type first_point_lat: float
    :param first_point_long: first point longitude
    :type first_point_long: float
    :param second_point_lat: second point latitude
    :type second_point_lat: float
    :param second_point_long: second point longitude
    :type second_point_long: float

    :param return: distance between points in meters
    :type return: float 
    """
    if first_point_lat == second_point_lat:
        if first_point_long == second_point_long:
            return 0
    lat_first = deg_to_radians(first_point_lat)
    lon_first = deg_to_radians(first_point_long)
    lat_sec = deg_to_radians(second_point_lat)
    lon_sec = deg_to_radians(second_point_long)
    lon_differ = lon_sec - lon_first
    cos_distance = math.acos(math.sin(lat_first) * math.sin(lat_sec) + math.cos(lat_first) * math.cos(lat_sec) * math.cos(lon_differ)) * RZ
    return cos_distance


def calculate_distance_points(first_point, second_point):
    """Calculate distance between two gps points in world. Parameters are GPS class objects. Usage same as method calculate_distance
    
    :param first_point: first gps point
    :type first_point: GPS class
    :param second_point: second gps point
    :type second_point: GPS class
   """
    cos_distance = calculate_distance(first_point.latitude, first_point.longitude, second_point.latitude, second_point.longitude)
    return cos_distance


def calculate_pix_meter_coef(left_corner_latitude, left_corner_longitude, right_corner_latitude, right_corner_longitude, resolution_width):
    """Calculate pixel/meter coef based on image corner distance.

    :param left_corner_latitude: latitude of the first corner point
    :type left_corner_latitude: float
    :param left_corner_longitude: longitude of the first corner point
    :type left_corner_longitude: float
    :param right_corner_latitude: latitude of the second corner point
    :type right_corner_latitude: float
    :param right_corner_longitude: longitude of the second corner point
    :type right_corner_longitude: float
    :param resolution_width: image width resolution
    :type resolution_width: int
    :return: coeficient determining distance in world in order to pixels in given image
    :rtype: float
    """
    image_distance = calculate_distance(left_corner_latitude, left_corner_longitude, right_corner_latitude, right_corner_longitude)
    pixel_coef = resolution_width / image_distance
    return pixel_coef


def calculate_pix_meter_coef_points(left_corner, right_corner, resolution_width):
    """Function corresponds to calculate_pix_meter_coef. Parameters are just GPS class type

    :param left_corner: left corner GPS
    :type left_corner: GPS
    :param right_corner: right corner GPS
    :type right_corner: GPS
    :param resolution: image width
    :type resolution: float
    :return: coeficient determining distance in world in order to pixels in given image
    :rtype: float
    """
    image_distance = calculate_distance_points(left_corner, right_corner)
    pixel_coef = resolution_width / image_distance
    return pixel_coef


def calculate_pix_meter_coef_points_TEST(left_corner_up, right_corner_up, left_down_corner, resolution_width, resolution_height):
    """Function corresponds to calculate_pix_meter_coef. Parameters are just GPS class type

    :param left_corner: left corner GPS
    :type left_corner: GPS
    :param right_corner: right corner GPS
    :type right_corner: GPS
    :param resolution: image width
    :type resolution: float
    :return: coeficient determining distance in world in order to pixels in given image
    :rtype: float
    """
    image_distance_x = calculate_distance_points(left_corner_up, right_corner_up)
    image_distance_y = calculate_distance_points(left_corner_up, left_down_corner)
    print(image_distance_x)
    print(image_distance_y)
    pixel_coef_x = resolution_width / image_distance_x
    pixel_coef_y = resolution_height / image_distance_y
    return (pixel_coef_x, pixel_coef_y)


def calculate_object_gps(left_upper_corner, right_upper_corner, pixel_position, azimuth, x_resolution):
    """ Calculate gps coordinates of the pixel position on given image, base od gps corners and azimuth
    
    :param left_upper_corner: letf upper GPS corner of image
    :type left_upper_corner: GPS class
    :param right_upper_corner: right upper GPS corner of image
    :type right_upper_corner: GPS class
    :param pixel_position: pixel coordinates to calculate gps (x,y)
    :type pixel_position: touple (int, int)
    :param azimuth: image azimuth
    :type azimuth: float
    :param x_resolution: given image resolution
    :type x_resolution: int
    :return: GPS point in world coresponding to given pixel position
    :rtype: GPS class
    """
    px_met_coef = calculate_pix_meter_coef_points(left_upper_corner, right_upper_corner, x_resolution)
    distance_to_obj_px = math.sqrt(pixel_position[0] ** 2 + pixel_position[1] ** 2)
    angle_to_obj = math.degrees(math.atan2(pixel_position[1], pixel_position[0])) + 90
    real_distance = distance_to_obj_px * 1 / px_met_coef
    obj_coords = calculate_point_geographic_coordinates(azimuth + angle_to_obj, left_upper_corner.latitude, left_upper_corner.longitude, real_distance)
    return obj_coords


def calculate_object_gps_center_reference(left_upper_corner, right_upper_corner, left_down_corner, center_corner, pixel_position, azimuth, x_resolution, y_resolution):
    """ Calculate gps coordinates of the pixel position on given image, base od gps corners and azimuth
    
    :param left_upper_corner: left upper GPS corner of image
    :type left_upper_corner: GPS class
    :param right_upper_corner: right upper GPS corner of image
    :type right_upper_corner: GPS class
    :param pixel_position: pixel coordinates to calculate gps (x,y)
    :type pixel_position: touple (int, int)
    :param azimuth: image azimuth
    :type azimuth: float
    :param x_resolution: given image resolution
    :type x_resolution: int
    :return: GPS point in world coresponding to given pixel position
    :rtype: GPS class
    """
    x_center = x_resolution // 2
    y_center = y_resolution // 2
    px_met_coef = calculate_pix_meter_coef_points(left_upper_corner, right_upper_corner, x_resolution)
    py_met_coef = calculate_pix_meter_coef_points(left_upper_corner, left_down_corner, y_resolution)
    real_distance = math.sqrt(((x_center - pixel_position[0]) / px_met_coef) ** 2 + ((y_center - pixel_position[1]) / py_met_coef) ** 2)
    angle_to_obj = math.degrees(math.atan2(pixel_position[0] - x_center, y_center - pixel_position[1]))
    obj_coords = calculate_point_geographic_coordinates(azimuth + angle_to_obj, center_corner.latitude, center_corner.longitude, real_distance)
    return obj_coords


def divide_flight(start_flight_gps_point, end_flight_gps_point, gap_distance):
    """ Divide flight in straight line on points
    
    :param start_flight_gps_point: first point gps coordinates
    :type start_flight_gps_point: GPS class
    :param end_flight_gps_point: end point gps coordinates
    :type end_flight_gps_point: GPS class
    :param gap_distance: point gap
    :type gap_distance: float
    :return: list of gps poinst betwwen start and end point with gap distance
    :rtype: list of GPS class
    """
    divided_flight_points = []
    global_flight_distance = calculate_distance_points(start_flight_gps_point, end_flight_gps_point)
    azimuth = calculate_azimuth_points(start_flight_gps_point, end_flight_gps_point)
    gap_number = int(global_flight_distance // gap_distance)
    starting_point = start_flight_gps_point
    for i in range(gap_number):
        current_point = calculate_point_geographic_coordinates(azimuth, starting_point.latitude, starting_point.longitude, gap_distance)
        divided_flight_points.append(current_point)
        starting_point = current_point

    divided_flight_points.append(end_flight_gps_point)
    return divided_flight_points