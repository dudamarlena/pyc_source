# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\plugins\exupery\alertlevel.py
# Compiled at: 2010-12-23 17:42:41
"""
Exupery - WP3 - Alert Level resources.

Contact:
 * Moritz Beyreuther (beyreuth@geophysik.uni-muenchen.de)

GIS Layer:
 The Alert level (a single integer value in the XML file) refers to a whole 
 region instead of a single point. Therefore it should not appear in the layer 
 tree, but be available separately (e.g. in the GIS menu). The alert level 
 should be displayed as a color (green, yellow, red). Additional information 
 (e.g. confidence) is available in the XML file. It may be displayed in an 
 info box. URL to display an image (preferably created "on the fly" by an 
 external program) in a new window.
"""
from lxml.etree import Element, SubElement as Sub
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerIndex, registerStylesheet
from seishub.core.packages.interfaces import IResourceType, IMapper
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import sql
import os

class AlertLevelResourceType(Component):
    """
    Alert Level resource type.
    """
    implements(IResourceType)
    package_id = 'exupery'
    resourcetype_id = 'alert-level'
    registerStylesheet('xslt' + os.sep + 'alert-level_metadata.xslt', 'metadata')
    registerStylesheet('xslt' + os.sep + 'alert-level_smile.xslt', 'smile')
    registerIndex('project_id', '/alert_level/@project_id', 'text')
    registerIndex('volcano_id', '/alert_level/@volcano_id', 'text')
    registerIndex('datetime', '/alert_level/datetime/value', 'datetime')
    registerIndex('level', '/alert_level/alert/level', 'integer')
    registerIndex('probability', '/alert_level/alert/probability', 'float')
    registerIndex('comment', '/alert_level/alert/comment', 'text')


class AlertLevelMapper(Component):
    """
    Returns a list of alert levels.
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/alert'

    def process_GET(self, request):
        pid = request.args0.get('project_id', '')
        xml = Element('query')
        query = sql.text('\n           SELECT DISTINCT \n               document_id, \n               volcano_id, \n               datetime,\n               level, \n               comment\n           FROM "/exupery/alert-level"\n           WHERE project_id = :pid\n        ')
        try:
            result = self.env.db.query(query, pid=pid)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, 'resource', document_id=str(i.document_id))
            Sub(s, 'volcano_id').text = i.volcano_id
            Sub(s, 'datetime').text = i.datetime.isoformat()
            Sub(s, 'level').text = str(i.level)
            Sub(s, 'comment').text = i.comment

        return toString(xml)


class S024AlertMapper(Component):
    """
    Returns a list of SO2_range3 values in a given time range.
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/so24alert'

    def process_GET(self, request):
        args = {}
        args['pid'] = request.args0.get('project_id', '')
        args['start'] = request.args0.get('start_datetime', '')
        args['end'] = request.args0.get('end_datetime', '')
        xml = Element('query')
        query = sql.text('\n           SELECT DISTINCT\n               document_id,\n               SO2_range3\n           FROM "/exupery/so2-gome2"\n           WHERE project_id = :pid \n           AND start_datetime > :start \n           AND end_datetime < :end\n        ')
        try:
            result = self.env.db.query(query, **args)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, 'resource', document_id=str(i.document_id))
            Sub(s, 'SO2_range3').text = str(i.SO2_range3)

        return toString(xml)


class Event4AlertMapper(Component):
    """
    Returns a list of Events depending on type
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/event4alert'

    def process_GET(self, request):
        args = {}
        args['pid'] = request.args0.get('project_id', '')
        args['start'] = request.args0.get('start_datetime', '')
        args['end'] = request.args0.get('end_datetime', '')
        args['event'] = request.args0.get('event', '')
        xml = Element('query')
        query = sql.text('\n           SELECT DISTINCT\n               document_id,\n               event_type\n           FROM "/seismology/event"\n           WHERE event_type = :event\n           AND datetime > :start\n           AND datetime < :end\n        ')
        try:
            result = self.env.db.query(query, **args)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, 'resource', document_id=str(i.document_id))
            Sub(s, 'event_type').text = str(i.event_type)

        return toString(xml)


class Infrared4AlertMapper(Component):
    """
    Returns a list of temperature hotspot values in a given time range.
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/infrared4alert'

    def process_GET(self, request):
        args = {}
        args['pid'] = request.args0.get('project_id', '')
        args['start'] = request.args0.get('start_datetime', '')
        args['end'] = request.args0.get('end_datetime', '')
        xml = Element('query')
        query = sql.text('\n           SELECT DISTINCT\n               document_id ,\n               temperature_hotspot\n           FROM "/exupery/infrared"\n           WHERE project_id = :pid \n           AND start_datetime > :start \n           AND end_datetime < :end\n        ')
        try:
            result = self.env.db.query(query, **args)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, 'resource', document_id=str(i.document_id))
            Sub(s, 'temperature_hotspot').text = str(i.temperature_hotspot)

        return toString(xml)


class GPS4AlertMapper(Component):
    """
    Returns a dictionary of absolute height values per station. 
    
    Therefore several SQL queries are necessary. First query all available 
    station IDs. Then for each station retrieve the absolute height and
    confidence for the latest measurement and for the measurements a 
    specified time range before and commit this result. (???)
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/gps4alert'

    def process_GET(self, request):
        args = {}
        args['pid'] = request.args0.get('project_id', '')
        args['start'] = request.args0.get('start_datetime', '')
        args['end'] = request.args0.get('end_datetime', '')
        xml = Element('query')
        query = sql.text('\n           SELECT DISTINCT \n               document_id,\n               station_id \n           FROM "/exupery/gps-station"\n           WHERE project_id = :pid \n           AND start_datetime < :start \n           AND end_datetime > :end\n        ')
        try:
            available_stations = self.env.db.query(query, **args)
        except:
            return toString(xml)

        for s in available_stations:
            sid = s.station_id
            query = sql.text('\n               SELECT DISTINCT \n                   document_id,\n                   abs_height,\n                   abs_height_conf,\n                   start_datetime\n               FROM "/exupery/gps-data"\n               WHERE project_id = :pid\n               AND station_id = :sid\n               ORDER BY start_datetime ASC\n               LIMIT 1\n            ')
            try:
                monitor = self.env.db.query(query, sid=sid, **args)
            except:
                print 'Exception Monitor'
                continue

            query = sql.text('\n               SELECT DISTINCT \n                   document_id,\n                   abs_height,\n                   abs_height_conf,\n                   start_datetime\n               FROM "/exupery/gps-data"\n               WHERE project_id = :pid\n               AND station_id = :sid\n               ORDER BY start_datetime DESC\n               LIMIT 1\n            ')
            try:
                baseline = self.env.db.query(query, sid=sid, **args)
            except:
                print 'Exception BASELINE'
                continue

            s = Sub(xml, 'station', id=str(sid), document_id=str(s.document_id))
            for j in monitor:
                t = Sub(s, 'monitor', document_id=str(j.document_id))
                Sub(t, 'start_datetime').text = j.start_datetime.isoformat()
                Sub(t, 'abs_height').text = str(j.abs_height)
                Sub(t, 'abs_height_conf').text = str(j.abs_height_conf)

            for k in baseline:
                u = Sub(s, 'baseline', document_id=str(k.document_id))
                Sub(u, 'start_datetime').text = k.start_datetime.isoformat()
                Sub(u, 'abs_height').text = str(k.abs_height)
                Sub(u, 'abs_height_conf').text = str(k.abs_height_conf)

        return toString(xml)