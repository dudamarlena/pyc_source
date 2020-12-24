# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/generated_sample_events/events.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3900 bytes
"""
Methods to expose the event types and generate the event jsons for use in SAM CLI generate-event
"""
import os, json, base64
from requests.utils import quote
from chevron import renderer

class Events:
    __doc__ = '\n    Events library class that loads and customizes event json files\n\n    Methods\n    ---------------\n    expose_event_metadata(self):\n        return the event mapping file\n    generate-event(self, service_name, event_type, values_to_sub):\n        load in and substitute values into json file (if necessary)\n    '

    def __init__(self):
        """
        Constructor for event library
        """
        this_folder = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(this_folder, 'event-mapping.json')
        with open(file_name) as (f):
            self.event_mapping = json.load(f)

    def encode(self, tags, encoding, values_to_sub):
        """
        reads the encoding type from the event-mapping.json
        and determines whether a value needs encoding

        Parameters
        ----------
        tags: dict
            the values of a particular event that can be substituted
            within the event json
        encoding: string
            string that helps navigate to the encoding field of the json
        values_to_sub: dict
            key/value pairs that will be substituted into the json
        Returns
        -------
        values_to_sub: dict
            the encoded (if need be) values to substitute into the json.
        """
        for tag in tags:
            if tags[tag].get(encoding) != 'None':
                if tags[tag].get(encoding) == 'url':
                    values_to_sub[tag] = self.url_encode(values_to_sub[tag])
                if tags[tag].get(encoding) == 'base64':
                    values_to_sub[tag] = self.base64_utf_encode(values_to_sub[tag])

        return values_to_sub

    def url_encode(self, value):
        """
        url encodes the value passed in

        Parameters
        ----------
        value: string
            the value that needs to be encoded in the json
        Returns
        -------
        string: the url encoded value
        """
        return quote(value)

    def base64_utf_encode(self, value):
        """
        base64 utf8 encodes the value passed in

        Parameters
        ----------
        value: string
            value that needs to be encoded in the json
        Returns
        -------
        string: the base64_utf encoded value
        """
        return base64.b64encode(value.encode('utf8')).decode('utf-8')

    def generate_event(self, service_name, event_type, values_to_sub):
        """
        opens the event json, substitutes the values in, and
        returns the customized event json

        Parameters
        ----------
        service_name: string
            name of the top level service (S3, apigateway, etc)
        event_type: string
            name of the event underneath the service
        values_to_sub: dict
            key/value pairs to substitute into the json
        Returns
        -------
        renderer.render(): string
            string version of the custom event json
        """
        tags = self.event_mapping[service_name][event_type]['tags']
        values_to_sub = self.encode(tags, 'encoding', values_to_sub)
        this_folder = os.path.dirname(os.path.abspath(__file__))
        file_name = self.event_mapping[service_name][event_type]['filename'] + '.json'
        file_path = os.path.join(this_folder, 'events', service_name, file_name)
        with open(file_path) as (f):
            data = json.load(f)
        data = json.dumps(data, indent=2)
        return renderer.render(data, values_to_sub)