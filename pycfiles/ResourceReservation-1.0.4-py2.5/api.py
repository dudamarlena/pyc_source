# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/resreservation/api.py
# Compiled at: 2010-10-14 11:01:30
import re, time, sys, traceback, logging
from datetime import datetime
from trac.core import *
from trac.perm import IPermissionRequestor, PermissionError
from trac.util import get_reporter_id
from trac.util.compat import sorted
from trac.util.datefmt import utc, to_timestamp
from trac.web.api import IRequestHandler

class ResourceReservationSystem(Component):
    """Resource Reservation system for Trac."""
    implements(IPermissionRequestor, IRequestHandler)

    def list_all_resources(self, res_type, res_from, res_to):
        """Get a list of all the reserved resources, optionally in the specified period."""
        result = []
        reservations = {}
        try:
            db = self.env.get_db_cnx()
            cursor = db.cursor()
            sql = "SELECT DISTINCT name FROM resreservation WHERE res_type = '" + res_type + "'"
            cursor.execute(sql)
            for row in cursor:
                reservations[row[0]] = []

            cursor = db.cursor()
            sql = "SELECT name, assignee, res_from, res_to FROM resreservation WHERE res_type = '" + res_type + "'"
            if res_from != None and res_from != '' and res_to != None and res_to != '':
                sql += ' AND res_from >= date(%s) AND res_to <= date(%s)'
                cursor.execute(sql, (res_from, res_to))
            else:
                cursor.execute(sql)
            for row in cursor:
                name = row[0]
                assignee = row[1]
                res_from = row[2]
                res_to = row[3]
                reservations[name].append({'assignee': assignee, 'res_from': res_from, 'res_to': res_to})

            for name in sorted(iter(reservations)):
                result.append({'name': name, 'reservations': reservations[name]})

        except:
            print 'list_all_resources - Error!!!'
            db.rollback()
            raise

        return result

    def assign_resource(self, res_type, resource_name, res_date, curr_assignee, new_assignee, override):
        """Assign a resource."""
        try:
            db = self.env.get_db_cnx()
            if override == 'false':
                cursor = db.cursor()
                sql = 'SELECT assignee FROM resreservation WHERE res_type = %s AND name = %s AND res_from <= date(%s) AND res_to >= date(%s)'
                cursor.execute(sql, (res_type, resource_name, res_date, res_date))
                row = cursor.fetchone()
                if row and row[0] != curr_assignee and row[0] != new_assignee:
                    return False
            cursor = db.cursor()
            sql = 'DELETE FROM resreservation WHERE res_type = %s AND name = %s AND res_from <= date(%s) AND res_to >= date(%s)'
            cursor.execute(sql, (res_type, resource_name, res_date, res_date))
            if new_assignee != '':
                cursor = db.cursor()
                sql = 'INSERT INTO resreservation (res_type, name, assignee, res_from, res_to) VALUES (%s, %s, %s, date(%s), date(%s))'
                cursor.execute(sql, (res_type, resource_name, new_assignee, res_date, res_date))
            db.commit()
            return True
        except:
            print 'assign_resource - Error!!!'
            db.rollback()
            raise
            return False

    def add_resource(self, res_type, resource_name):
        """Add a resource."""
        try:
            db = self.env.get_db_cnx()
            cursor = db.cursor()
            sql = 'INSERT INTO resreservation (res_type, name, assignee, res_from, res_to) VALUES (%s, %s, %s, date(%s), date(%s))'
            cursor.execute(sql, (res_type, resource_name, 'none', '2000-01-01', '2000-01-01'))
            db.commit()
        except:
            print 'add_resource - Error!!!'
            db.rollback()
            raise

    def get_permission_actions(self):
        return [
         'RES_RESERVE_VIEW', 'RES_RESERVE_MODIFY']

    def match_request(self, req):
        return req.path_info.startswith('/resreservation') and 'RES_RESERVE_VIEW' in req.perm

    def process_request(self, req):
        """Handles Ajax requests to set the resource reservation."""
        req.perm.require('RES_RESERVE_MODIFY')
        data = {'title': 'Results'}
        command = req.args.get('command')
        if command == 'assignresource':
            resource_type = req.args.get('resourceType')
            resource_name = req.args.get('resourceName')
            res_date = req.args.get('resDate')
            curr_assignee = req.args.get('currAssignee')
            new_assignee = req.args.get('newAssignee')
            override = req.args.get('override')
            result = self.assign_resource(resource_type, resource_name, res_date, curr_assignee, new_assignee, override)
            if result:
                data['result'] = '"true"'
            else:
                data['result'] = '"false"'
        elif command == 'addresource':
            resource_type = req.args.get('resourceType')
            resource_name = req.args.get('resourceName')
            self.add_resource(resource_type, resource_name)
            data['result'] = '"true"'
        return ('result.html', data, None)