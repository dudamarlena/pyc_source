# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/json.py
# Compiled at: 2014-11-03 05:47:13
# Size of source mod 2**32: 8546 bytes
from __future__ import absolute_import
from beehive.formatter.base import Formatter
from beehive.compat import unicode, long
import base64
try:
    import json
except ImportError:
    import simplejson as json

class JSONFormatter(Formatter):
    name = 'json'
    description = 'JSON dump of test run'
    dumps_kwargs = {}
    split_text_into_lines = True
    json_number_types = (
     int, long, float)
    json_scalar_types = json_number_types + (unicode, bool, type(None))

    def __init__(self, stream_opener, config):
        super(JSONFormatter, self).__init__(stream_opener, config)
        self.stream = self.open()
        self.feature_count = 0
        self.current_feature = None
        self.current_feature_data = None
        self._step_index = 0

    def reset(self):
        self.current_feature = None
        self.current_feature_data = None
        self._step_index = 0

    def uri(self, uri):
        pass

    def feature(self, feature):
        self.reset()
        self.current_feature = feature
        self.current_feature_data = {'keyword': feature.keyword, 
         'name': feature.name, 
         'tags': list(feature.tags), 
         'location': unicode(feature.location), 
         'status': feature.status}
        element = self.current_feature_data
        if feature.description:
            element['description'] = feature.description

    def background(self, background):
        element = self.add_feature_element({'type': 'background', 
         'keyword': background.keyword, 
         'name': background.name, 
         'location': unicode(background.location), 
         'steps': []})
        if background.name:
            element['name'] = background.name
        self._step_index = 0
        for step_ in background.steps:
            self.step(step_)

    def scenario(self, scenario):
        element = self.add_feature_element({'type': 'scenario', 
         'keyword': scenario.keyword, 
         'name': scenario.name, 
         'tags': scenario.tags, 
         'location': unicode(scenario.location), 
         'steps': []})
        if scenario.description:
            element['description'] = scenario.description
        self._step_index = 0

    def scenario_outline(self, scenario_outline):
        element = self.add_feature_element({'type': 'scenario_outline', 
         'keyword': scenario_outline.keyword, 
         'name': scenario_outline.name, 
         'tags': scenario_outline.tags, 
         'location': unicode(scenario_outline.location), 
         'steps': [],  'examples': []})
        if scenario_outline.description:
            element['description'] = scenario_outline.description
        self._step_index = 0

    @classmethod
    def make_table(cls, table):
        table_data = {'headings': table.headings, 
         'rows': [list(row) for row in table.rows]}
        return table_data

    def examples(self, examples):
        e = {'type': 'examples', 
         'keyword': examples.keyword, 
         'name': examples.name, 
         'location': unicode(examples.location)}
        if examples.table:
            e['table'] = self.make_table(examples.table)
        element = self.current_feature_element
        element['examples'].append(e)

    def step(self, step):
        s = {'keyword': step.keyword, 
         'step_type': step.step_type, 
         'name': step.name, 
         'location': unicode(step.location)}
        if step.text:
            text = step.text
            if self.split_text_into_lines:
                if '\n' in text:
                    text = text.splitlines()
            s['text'] = text
        if step.table:
            s['table'] = self.make_table(step.table)
        element = self.current_feature_element
        element['steps'].append(s)

    def match(self, match):
        args = []
        for argument in match.arguments:
            argument_value = argument.value
            if not isinstance(argument_value, self.json_scalar_types):
                argument_value = argument.original
            assert isinstance(argument_value, self.json_scalar_types)
            arg = {'value': argument_value}
            if argument.name:
                arg['name'] = argument.name
            if argument.original != argument_value:
                arg['original'] = argument.original
            args.append(arg)

        match_data = {'location': unicode(match.location) or '', 
         'arguments': args}
        if match.location:
            steps = self.current_feature_element['steps']
            steps[self._step_index]['match'] = match_data

    def result(self, result):
        steps = self.current_feature_element['steps']
        steps[self._step_index]['result'] = {'status': result.status, 
         'duration': result.duration}
        if result.error_message:
            if result.status == 'failed':
                error_message = result.error_message
                if self.split_text_into_lines:
                    if '\n' in error_message:
                        error_message = error_message.splitlines()
                result_element = steps[self._step_index]['result']
                result_element['error_message'] = error_message
        self._step_index += 1

    def embedding(self, mime_type, data):
        step = self.current_feature_element['steps'][(-1)]
        step['embeddings'].append({'mime_type': mime_type, 
         'data': base64.b64encode(data).replace('\n', '')})

    def eof(self):
        """
        End of feature
        """
        if not self.current_feature_data:
            return
        self.update_status_data()
        if self.feature_count == 0:
            self.write_json_header()
        else:
            self.write_json_feature_separator()
        self.write_json_feature(self.current_feature_data)
        self.current_feature_data = None
        self.feature_count += 1

    def close(self):
        self.write_json_footer()
        self.close_stream()

    def add_feature_element(self, element):
        assert self.current_feature_data is not None
        if 'elements' not in self.current_feature_data:
            self.current_feature_data['elements'] = []
        self.current_feature_data['elements'].append(element)
        return element

    @property
    def current_feature_element(self):
        assert self.current_feature_data is not None
        return self.current_feature_data['elements'][(-1)]

    def update_status_data(self):
        assert self.current_feature
        assert self.current_feature_data
        self.current_feature_data['status'] = self.current_feature.status

    def write_json_header(self):
        self.stream.write('[\n')

    def write_json_footer(self):
        self.stream.write('\n]\n')

    def write_json_feature(self, feature_data):
        self.stream.write(json.dumps(feature_data, **self.dumps_kwargs))
        self.stream.flush()

    def write_json_feature_separator(self):
        self.stream.write(',\n\n')


class PrettyJSONFormatter(JSONFormatter):
    __doc__ = '\n    Provides readable/comparable textual JSON output.\n    '
    name = 'json.pretty'
    description = 'JSON dump of test run (human readable)'
    dumps_kwargs = {'indent': 2,  'sort_keys': True}