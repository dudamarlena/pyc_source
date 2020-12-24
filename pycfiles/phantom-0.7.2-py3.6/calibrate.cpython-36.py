# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\phantom\measures\calibrate.py
# Compiled at: 2019-12-18 07:24:29
# Size of source mod 2**32: 2705 bytes
"""
Algorithms and functions to calibrate images removing distortions.
"""
import cv2, numpy as np

def find_distortion(img, nx, ny):
    """
    Finds the distortion created by a camera
    
    :param img: Image of a chess board taken by the camera
    :param nx: number of inside corners in x 
    :param ny: number of inside corners in y
    :return: objpoints[List] of 3D points in real world space and 
        imgpoints[List] of 2D points in image plane
    """
    objpoints = []
    imgpoints = []
    objp = np.zeros((ny * nx, 3), np.float32)
    objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
    if ret == True:
        imgpoints.append(corners)
        objpoints.append(objp)
    return (
     imgpoints, objpoints)


def find_and_draw_corners(img, nx, ny):
    """
    Finds and draws the inner corners of a chess board in the image, if found
    
    :param img: Image of a chess board taken by the camera
    :param nx: number of inside corners in x 
    :param ny: number of inside corners in y
    :return: True if the chess board was found, and an image with the drawing(in gray scale)
        False if the chess board wasn't found, and the original image(in gray scale)
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
    if ret == True:
        cv2.drawChessboardCorners(gray, (nx, ny), corners, ret)
        return (
         True, gray)
    else:
        return (
         False, gray)


def calibrate(img, img_chess_board, nx, ny):
    """
    Removes distortion of an image created by the camera that took the photo
    
    :param img: Image to be corrected
    :param img_chess_board: Image of a chess board taken by the camera
    :param nx: number of inside corners in x 
    :param ny: number of inside corners in y
    :return: Undistorted image. If the chess board wasn't found,
        it returns the origina image (img)
    """
    imgpoints, objpoints = find_distortion(img_chess_board, nx, ny)
    if imgpoints:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1:], None, None)
        return cv2.undistort(img, mtx, dist, None, mtx)
    else:
        return img