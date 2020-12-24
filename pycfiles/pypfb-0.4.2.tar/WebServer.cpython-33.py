# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/WebServer.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 4123 bytes
__doc__ = '\nCreated on Jan 21, 2014\n\n@author: "Colin Manning"\n'
from http.server import BaseHTTPRequestHandler, HTTPServer
import os.path, requests, uuid, time, traceback, json, logging
from .JDs import JDs
import utils
serverName = 'localhost'
serverPort = 8087
server = None

class WebServer(BaseHTTPRequestHandler):
    """WebServer"""
    APP_NAME = 'aprintflow2webserver'
    JSON_CONTENT_TYPE = 'application/json;charset=UTF-8'
    ENCODING = 'utf-8'
    WORKGROUP_CLASS = 'workgroup'
    PROJECT_CLASS = 'project'
    SPECIFICATION_CLASS = 'specification'
    FILE_CLASS = 'file'
    USER_CLASS = 'user'
    logging = None
    jds = None
    db_dir = '/opt/printflow27db'
    os_userid = 501
    os_groupid = 501

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.logger = logging.getLogger(self.APP_NAME)
        self.jds = JDs(self.db_dir, self.os_userid, self.os_groupid)
        self.jds.register_class(self.WORKGROUP_CLASS)
        self.jds.register_class(self.PROJECT_CLASS)
        self.jds.register_class(self.SPECIFICATION_CLASS)
        self.jds.register_class(self.FILE_CLASS)
        self.jds.register_class(self.USER_CLASS)

    def do_HEAD(self):
        try:
            self.send_response(200)
            self.send_header(self.JSON_CONTENT_TYPE)
            self.end_headers()
        except:
            self.logger.error('problem processing HEAD request')
            self.logger.error(traceback.format_exc())

    def do_GET(self):
        try:
            result = None
            return_status = 200
            path_bits = self.path.split('/')
            object_id = path_bits[(-1)]
            object_class = path_bits[(-2)]
            if object_class == self.PROJECT_CLASS:
                result = self.jds.fetch(object_class, object_id)
            if result is None:
                result = {}
                return_status = 401
                self.logger.error('could not find ' + object + ': with id: ' + object_id)
                self.send_header('Content-type', self.JSON_CONTENT_TYPE)
                self.end_headers()
                self.send_response(return_status)
                self.wfile.write(json.dumps(result).encode(self.ENCODING))
            else:
                return_status = 200
                self.send_header('Content-type', self.JSON_CONTENT_TYPE)
                self.end_headers()
                self.send_response(return_status)
                self.wfile.write(json.dumps(result).encode(self.ENCODING))
        except:
            self.logger.error('problem processing GET request')
            self.logger.error(traceback.format_exc())
            self.send_response(401)

        return

    def do_POST(self):
        try:
            self.end_headers()
            self.send_response(200)
        except:
            self.logger.error('problem processing POST request')
            self.logger.error(traceback.format_exc())
            self.send_response(401)

    def get_project(self, project_id):
        result = None
        try:
            result = self.jds.fetch(self.PROJECT_CLASS, project_id)
        except:
            self.logger.error('problem getting project: ' + project_id)
            self.logger.error(traceback.format_exc())

        return result

    def get_specification(self, specification_id):
        result = None
        try:
            result = self.jds.fetch(self.PSPECIFICATION_CLASS, specification_id)
        except:
            self.logger.error('problem getting specification: ' + specification_id)
            self.logger.error(traceback.format_exc())

        return result

    def get_file(self, file_id):
        result = None
        try:
            result = self.jds.fetch(self.FILE_CLASS, file_id)
        except:
            self.logger.error('problem getting file: ' + file_id)
            self.logger.error(traceback.format_exc())

        return result