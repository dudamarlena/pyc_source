# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/face_pose.py
# Compiled at: 2018-09-11 09:30:58
import numpy as np, cv2, ldm, os
from zprint import *
import math
ldm0 = ldm.LDM()

def get_camera_matrix(rect):
    y = rect.top()
    x = rect.left()
    ym = rect.bottom()
    xm = rect.right()
    rows_center = (y + ym) / 2.0
    cols_center = (x + xm) / 2.0
    cols = xm
    rows = ym
    camera_matrix = np.zeros((3, 3))
    camera_matrix[0] = np.array([cols * 1.0, 0.0, cols_center])
    camera_matrix[1] = np.array([0.0, cols * 1.0, rows_center])
    camera_matrix[2] = np.array([0.0, 0.0, 1])
    return camera_matrix


def get_face_pose(landmarks):
    model_points = np.zeros((6, 3))
    model_points[0] = np.array([0.0, 0.0, 0.0])
    model_points[1] = np.array([0.0, -330.0, -65.0])
    model_points[2] = np.array([-225.0, 170.0, -135.0])
    model_points[3] = np.array([225.0, 170.0, -135.0])
    model_points[4] = np.array([-150.0, -150.0, -125.0])
    model_points[5] = np.array([150.0, -150.0, -125.0])
    return model_points


def get_quaternion(rotation_vector):
    theta = cv2.norm(rotation_vector, cv2.NORM_L2)
    quaternion = np.zeros((4, 1))
    quaternion[0] = math.cos(theta / 2)
    quaternion[1] = math.sin(theta / 2) * rotation_vector[0] / theta
    quaternion[2] = math.sin(theta / 2) * rotation_vector[1] / theta
    quaternion[3] = math.sin(theta / 2) * rotation_vector[2] / theta
    return quaternion


def degree(theta):
    degree = theta * 180 / math.pi
    degree = degree - 180 if degree > 90 else degree
    degree = degree + 180 if degree < -90 else degree
    return degree


def get_eulerangle(quaternion):
    w = quaternion[0]
    x = quaternion[1]
    y = quaternion[2]
    z = quaternion[3]
    pitch = math.atan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
    t2 = 2.0 * (w * y - z * x)
    t2 = 1.0 if t2 > 1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    yaw = math.asin(t2)
    roll = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
    print 'pitch:%f,yaw:%f,roll:%f' % (degree(pitch), degree(yaw), degree(roll))
    return (pitch, yaw, roll)


def get_rotation_matrix(v, pitch, yaw, roll):
    theta = yaw
    y_m = np.array([[math.cos(theta), 0, math.sin(theta)],
     [
      0, 1, 0],
     [
      -math.sin(theta), 0, math.cos(theta)]])
    theta = roll
    z_m = np.array([[math.cos(theta), -math.sin(theta), 0],
     [
      math.sin(theta), math.cos(theta), 0],
     [
      0, 0, 1]])
    theta = pitch
    x_m = np.array([[1, 0, 0],
     [
      0, math.cos(theta), -math.sin(theta)],
     [
      0, math.sin(theta), math.cos(theta)]])
    return (
     x_m, y_m, z_m)


def rotation_it(v, x_m, y_m, z_m):
    v = np.dot(v, x_m)
    v = np.dot(v, y_m)
    v = np.dot(v, z_m)
    return v


def display(fig, x_m, y_m, z_m):
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    xv = np.array([1, 0, 0])
    vx = rotation_it(xv, x_m, y_m, z_m)
    ax.plot(np.array([0, vx[0]]), np.array([0, vx[1]]), np.array([0, vx[2]]), label='x')
    vx = rotation_it(np.array([0, 1, 0]), x_m, y_m, z_m)
    ax.plot([0, vx[0]], [0, vx[1]], [0, vx[2]], label='y')
    vx = rotation_it(np.array([0, 0, 1]), x_m, y_m, z_m)
    ax.plot([0, vx[0]], [0, vx[1]], [0, vx[2]], label='z')
    ax.legend()
    plt.show()


def get_image_pose(img):
    pitch = -100
    yaw = -100
    roll = -100
    ldl, facel = ldm0.landmark_list(img)
    if len(ldl) > 0:
        landmarks = np.zeros((6, 2))
        i = 0
        landmarks[0] = ldl[0]['all'][30]
        landmarks[1] = ldl[0]['all'][8]
        landmarks[2] = ldl[0]['all'][36]
        landmarks[3] = ldl[0]['all'][45]
        landmarks[4] = ldl[0]['all'][48]
        landmarks[5] = ldl[0]['all'][54]
        model_points = get_face_pose(landmarks)
        ret, rotation_vector, translation_vector = cv2.solvePnP(model_points, landmarks, get_camera_matrix(facel[0]), np.zeros((4,
                                                                                                                                1)))
        pitch, yaw, roll = get_eulerangle(get_quaternion(rotation_vector))
    return (
     pitch, yaw, roll)


def face_pose(pitch, yaw, roll):
    import sys, getopt
    cascade_fn = 'trained_face_model4\\cascade.xml'
    cascade = cv2.CascadeClassifier(cascade_fn)
    if True:
        img = get_screen()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        ldl, facel = ldm0.landmark_list(img)
        if len(ldl) > 0:
            print facel
            landmarks = np.zeros((6, 2))
            i = 0
            landmarks[0] = ldl[0]['all'][30]
            landmarks[1] = ldl[0]['all'][8]
            landmarks[2] = ldl[0]['all'][36]
            landmarks[3] = ldl[0]['all'][45]
            landmarks[4] = ldl[0]['all'][48]
            landmarks[5] = ldl[0]['all'][54]
            model_points = get_face_pose(landmarks)
            ret, rotation_vector, translation_vector = cv2.solvePnP(model_points, landmarks, get_camera_matrix(facel[0]), np.zeros((4,
                                                                                                                                    1)))
            pitch, yaw, roll = get_eulerangle(get_quaternion(rotation_vector))
        t = clock()
        rects = detect(gray, cascade)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]

        dt = clock() - t
        draw_str(vis, 10, 5, 'time: %.1f ms' % (dt * 1000), 0.8)
        draw_str(vis, 10, 30, 'pfs: %.1f f' % (1 / dt), 0.8)
        cv2.imshow('facedetect', vis)
    return (
     pitch, yaw, roll)


def main():
    import sys, getopt
    print help_message
    fig = plt.figure()
    plt.ion()
    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try:
        video_src = video_src[0]
    except:
        video_src = 0

    args = dict(args)
    cascade_fn = args.get('--cascade', 'trained_face_model4\\cascade.xml')
    nested_fn = args.get('--nested-cascade', '..\\opencv-2.4.13\\data\\haarcascades\\haarcascade_eye.xml')
    cascade = cv2.CascadeClassifier(cascade_fn)
    nested = cv2.CascadeClassifier(nested_fn)
    cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')
    while True:
        img = get_screen()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        ldl, facel = ldm0.landmark_list(img)
        if len(ldl) > 0:
            landmarks = np.zeros((6, 2))
            i = 0
            landmarks[0] = ldl[0]['all'][30]
            landmarks[1] = ldl[0]['all'][8]
            landmarks[2] = ldl[0]['all'][36]
            landmarks[3] = ldl[0]['all'][45]
            landmarks[4] = ldl[0]['all'][48]
            landmarks[5] = ldl[0]['all'][54]
            model_points = get_face_pose(landmarks)
            ret, rotation_vector, translation_vector = cv2.solvePnP(model_points, landmarks, get_camera_matrix(img), np.zeros((4,
                                                                                                                               1)))
            pitch, yaw, roll = get_eulerangle(get_quaternion(rotation_vector))
        t = clock()
        rects = detect(gray, cascade)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            subrects = detect(roi.copy(), nested)
            draw_rects(vis_roi, subrects, (255, 0, 0))

        dt = clock() - t
        draw_str(vis, 10, 5, 'time: %.1f ms' % (dt * 1000), 0.8)
        draw_str(vis, 10, 30, 'pfs: %.1f f' % (1 / dt), 0.8)
        cv2.imshow('facedetect', vis)
        if 255 & cv2.waitKey(5) == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    imgf = 'test.jpg'
    img = cv2.imread(imgf)
    print get_image_pose(img)