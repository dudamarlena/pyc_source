# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/getl/extractors/location_history.py
# Compiled at: 2019-03-07 10:41:53
# Size of source mod 2**32: 1908 bytes
from getl.extractors.extractor import Extractor
import json

class LocationHistory(Extractor):

    def __init__(self, db, path):
        super().__init__(db, path)

    def create_table(self):
        self.sql('\n      CREATE TABLE locations(\n        latitude          FLOAT NOT NULL,\n        longitude         FLOAT NOT NULL,\n        accuracy          FLOAT,\n        altitude          FLOAT,\n        vertical_accuracy FLOAT,\n        activity          JSON,\n        timestamp         DATETIME NOT NULL\n      );\n    ')

    def load(self):
        data = self.load_json('/Location History/Location History.json')
        for raw_location in data['locations']:
            location = self.shape_location(raw_location)
            self.sql(f"""\n        INSERT INTO locations (\n          latitude,\n          longitude,\n          accuracy,\n          altitude,\n          vertical_accuracy,\n          activity,\n          timestamp\n        ) VALUES (\n          {location['latitude']},\n          {location['longitude']},\n          {'NULL' if location['accuracy'] == None else location['accuracy']},\n          {'NULL' if location['altitude'] == None else location['altitude']},\n          {'NULL' if location['vertical_accuracy'] == None else location['vertical_accuracy']},\n          {'NULL' if location['activity'] == None else "'" + json.dumps(location['activity']) + "'"},\n          '{location['timestamp']}'\n        );\n      """)

        self.db.commit()

    def shape_location(self, raw_location):
        return {'timestamp':self.extract_time(raw_location['timestampMs']), 
         'latitude':raw_location['latitudeE7'] / 10000000.0, 
         'longitude':raw_location['longitudeE7'] / 10000000.0, 
         'accuracy':raw_location.get('accuracy'), 
         'altitude':raw_location.get('altitude'), 
         'vertical_accuracy':raw_location.get('verticalAccuracy'), 
         'activity':raw_location.get('activity')}