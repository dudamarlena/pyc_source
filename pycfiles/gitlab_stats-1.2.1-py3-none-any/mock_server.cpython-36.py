# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sylvain.hareng1/Documents/Github/gitlab_stats/tests/mock_server.py
# Compiled at: 2019-08-15 15:47:42
# Size of source mod 2**32: 3190 bytes
import json, re, socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import requests, tests

class MockGitlabServer(BaseHTTPRequestHandler):
    PIPELINE = re.compile('pipelines')
    PROJECTS = re.compile('projects')
    PER_PAGE = re.compile('per_page')
    THE_PROJECT = re.compile('4895805')
    THE_PIPELINE = re.compile('33409')

    def do_GET(self):
        """ Default get handler method of BaseHTTPRequestHandler """
        if self.headers['PRIVATE-TOKEN'] == 'wrong token':
            self.response(requests.codes.not_found)
        elif re.search(self.PIPELINE, self.path) and re.search(self.PER_PAGE, self.path):
            self.send_all_pipeline()
        elif re.search(self.PROJECTS, self.path) and re.search(self.PER_PAGE, self.path):
            self.send_all_projects()
        elif re.search(self.PIPELINE, self.path) and re.search(self.THE_PIPELINE, self.path):
            self.send_pipeline()
        else:
            if re.search(self.THE_PROJECT, self.path):
                self.send_project()
            else:
                if re.search(self.PROJECTS, self.path):
                    self.response(requests.codes.ok)
                else:
                    self.response(requests.codes.not_found)

    def response(self, response):
        self.send_response(response)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps([{}])
        self.wfile.write(response_content.encode('utf-8'))

    def send_project(self):
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps(tests.PROJECT_INFO)
        self.wfile.write(response_content.encode('utf-8'))

    def send_pipeline(self):
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps(tests.PIPELINE_INFO)
        self.wfile.write(response_content.encode('utf-8'))

    def send_all_projects(self):
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps(tests.PROJECT_ALL)
        self.wfile.write(response_content.encode('utf-8'))

    def send_all_pipeline(self):
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps(tests.PIPELINES_ALL)
        self.wfile.write(response_content.encode('utf-8'))


def get_free_port():
    s = socket.socket((socket.AF_INET), type=(socket.SOCK_STREAM))
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port, server):
    mock_server = HTTPServer(('localhost', port), server)
    mock_server_thread = Thread(target=(mock_server.serve_forever))
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()