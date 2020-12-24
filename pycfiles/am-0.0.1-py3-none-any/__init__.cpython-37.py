# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\python\envs\alyvix\alyvix_py37\lib\site-packages\alyvix\ide\server\__init__.py
# Compiled at: 2019-11-29 09:13:19
# Size of source mod 2**32: 4932 bytes
import cv2, base64
from flask import Flask, request
import logging, threading
from multiprocessing import Process
from alyvix.core.contouring import ContouringManager
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
from .views import *

class ServerManager:

    def __init__(self):
        super(ServerManager, self).__init__()

    def run(self, port, log_level=0):
        global app
        if log_level == 0:
            server_log = None
        elif log_level > 0:
            server_log = 'default'
            print('Serving on http://127.0.0.1:' + str(port))
        views.current_port = port
        views.loglevel = log_level
        http_server = WSGIServer(('127.0.0.1', port), app, log=server_log)
        views.server_process = http_server
        http_server.serve_forever()

    def set_window(self, window):
        views.win32_window = window

    def set_browser_class(self, browser_class):
        views.browser_class = browser_class

    def set_background(self, background_image, scaling_factor):
        png_image = cv2.imencode('.png', background_image)
        views.base64png = base64.b64encode(png_image[1]).decode('ascii')
        views.img_h = int(background_image.shape[0] / scaling_factor)
        views.img_w = int(background_image.shape[1] / scaling_factor)
        views.background_image = background_image
        views.autocontoured_rects = self.auto_contouring(background_image, scaling_factor)

    def set_scaling_factor(self, scaling_factor):
        views.scaling_factor = scaling_factor

    def set_file_name(self, filename):
        views.current_filename = filename

    def set_object_name(self, objectname):
        views.current_objectname = objectname

    def set_json(self, json_dict):
        views.library_dict = json_dict

    def auto_contouring(self, image, scaling_factor=1):
        contouring_manager = ContouringManager(canny_threshold1=50.0,
          canny_threshold2=75.0,
          canny_apertureSize=3,
          hough_threshold=10,
          hough_minLineLength=30,
          hough_maxLineGap=1,
          line_angle_tolerance=0,
          ellipse_width=2,
          ellipse_height=2,
          text_roi_emptiness=0.45,
          text_roi_proportion=1.3,
          image_roi_emptiness=0.1,
          vline_hw_proportion=2,
          vline_w_maxsize=10,
          hline_wh_proportion=2,
          hline_h_maxsize=10,
          rect_w_minsize=5,
          rect_h_minsize=5,
          rect_w_maxsize_01=800,
          rect_h_maxsize_01=100,
          rect_w_maxsize_02=100,
          rect_h_maxsize_02=800,
          rect_hw_proportion=2,
          rect_hw_w_maxsize=10,
          rect_wh_proportion=2,
          rect_wh_h_maxsize=10,
          hrect_proximity=10,
          vrect_proximity=10,
          vrect_others_proximity=40,
          hrect_others_proximity=80)
        contouring_manager.auto_contouring(image, scaling_factor)
        autocontoured_rects = []
        autocontoured_rects.extend(contouring_manager.getImageBoxes())
        autocontoured_rects.extend(contouring_manager.getRectBoxes())
        autocontoured_rects.extend(contouring_manager.getTextBoxes())
        return autocontoured_rects

    def set_boxes(self, boxes):
        views.current_boxes = boxes

    def set_output_pipeline(self, output_pipeline):
        views.output_pipeline = output_pipeline