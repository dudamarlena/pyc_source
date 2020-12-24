# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hudan/Git/nerlogparser/nerlogparser/nerlogparser.py
# Compiled at: 2019-01-07 02:05:39
# Size of source mod 2**32: 3826 bytes
import pprint
from optparse import OptionParser
from collections import OrderedDict
from nerlogparser.model.ner_model import NERModel
from nerlogparser.model.config import Config
from nerlogparser.output.to_json import ToJson

class Nerlogparser(object):

    def __init__(self):
        self.model = None
        self.config = None
        self.master_label = {}
        self._Nerlogparser__load_pretrained_model()
        self._Nerlogparser__load_label()

    def __load_pretrained_model(self):
        self.config = Config()
        self.model = NERModel(self.config)
        self.model.build()
        self.model.restore_session(self.config.dir_model)

    def __load_label(self):
        with open(self.config.label_file, 'r') as (f):
            label = f.readlines()
        labels = {}
        for line in label:
            line_split = line.split(' ')
            ner_label, final_label = line_split[0], line_split[1]
            labels[ner_label] = final_label.rstrip()

        self.master_label = labels

    def __get_per_entity(self, words_raw, ner_label):
        entity = OrderedDict()
        for index, label in enumerate(ner_label):
            if '-' in label:
                main_label = label.split('-')[1]
            else:
                main_label = label
            if main_label not in entity.keys():
                entity[main_label] = []
            entity[main_label].append(words_raw[index])

        final_entity = OrderedDict()
        for main_label, words in entity.items():
            final_label = self.master_label[main_label]
            final_entity[final_label] = ' '.join(words)

        if 'message' not in final_entity.keys():
            final_entity['message'] = ''
        return final_entity

    def parse_logs(self, log_file):
        raw_logs = {}
        parsed_logs = OrderedDict()
        parsed_log_index = 0
        with open(log_file) as (f):
            for line_index, line in enumerate(f):
                if line not in ('\n', '\r\n'):
                    raw_logs[parsed_log_index] = line
                    words_raw = line.strip().split()
                    ner_label = self.model.predict(words_raw)
                    parsed = self._Nerlogparser__get_per_entity(words_raw, ner_label)
                    parsed_logs[parsed_log_index] = parsed
                    parsed_log_index += 1

        return parsed_logs


def main():
    parser = OptionParser(usage='usage: nerlogparser [options]')
    parser.add_option('-i', '--input', action='store', dest='input_file', help='Input log file.')
    parser.add_option('-o', '--output', action='store', dest='output_file', help='Parsed log file.')
    options, args = parser.parse_args()
    input_file = options.input_file
    output_file = options.output_file
    if options.input_file:
        nerlogparser = Nerlogparser()
        parsed_results = nerlogparser.parse_logs(input_file)
        if options.output_file:
            print('Write results to', output_file)
            ToJson.write_to_json(parsed_results, output_file)
        else:
            print('No output file. Print parsing results on terminal.')
            for line_id, parsed in parsed_results.items():
                print('Line:', line_id)
                pprint.pprint(parsed)
                print()

    else:
        print('Please see help: nerlogparser -h')


if __name__ == '__main__':
    main()