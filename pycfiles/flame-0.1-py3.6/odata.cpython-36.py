# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/odata.py
# Compiled at: 2018-06-20 09:13:36
# Size of source mod 2**32: 7765 bytes
import json, numpy as np

class Odata:

    def __init__(self, parameters, results):
        self.results = results
        self.parameters = parameters
        self.format = self.parameters['output_format']

    def _output_md(self):
        """ dumps the molecular descriptors to a TSV file"""
        with open('output_md.tsv', 'w') as (fo):
            if 'var_nam' in self.results:
                header = 'name'
                var_nam = self.results['var_nam']
                for nam in var_nam:
                    header += '\t' + nam

                fo.write(header + '\n')
            if 'xmatrix' in self.results and 'obj_nam' in self.results:
                xmatrix = self.results['xmatrix']
                obj_nam = self.results['obj_nam']
                shape = np.shape(xmatrix)
                if len(shape) > 1:
                    for x in range(shape[0]):
                        line = obj_nam[x]
                        for y in range(shape[1]):
                            line += '\t' + str(xmatrix[(x, y)])

                        fo.write(line + '\n')

                else:
                    line = obj_nam[0]
                    for y in range(shape[0]):
                        line += '\t' + str(xmatrix[y])

                    fo.write(line + '\n')

    def run_learn(self):
        """ Process the results of lear, usually a report on the model quality """
        if 'model_build' in self.results:
            for val in self.results['model_build']:
                if len(val) < 3:
                    print(val)
                else:
                    print(val[0], ' (', val[1], ') : ', val[2])

        else:
            if 'model_validate' in self.results:
                for val in self.results['model_validate']:
                    if len(val) < 3:
                        print(val)
                    else:
                        print(val[0], ' (', val[1], ') : ', val[2])

            if self.parameters['output_md']:
                self._output_md()
        return (True, 'building OK')

    def run_apply(self):
        """ Process the results of apply, usually a list of results and serializing to JSON """
        main_results = self.results['meta']['main']
        for key in main_results:
            if key not in self.results:
                self.results['error'] = 'unable to find "' + key + '" in results'
                return self.run_error()

        output = ''
        if self.parameters['output_md']:
            self._output_md()
        if 'TSV' in self.format:
            key_list = [
             'obj_nam']
            if 'SMILES' in self.results:
                key_list.append('SMILES')
            key_list += self.results['meta']['main']
            manifest = self.results['manifest']
            for item in manifest:
                if item['dimension'] == 'objs' and item['key'] not in key_list:
                    key_list.append(item['key'])

            with open('output.tsv', 'w') as (fo):
                header = ''
                for label in key_list:
                    header += label + '\t'

                fo.write(header + '\n')
                obj_num = int(self.results['obj_num'])
                for i in range(obj_num):
                    line = ''
                    for key in key_list:
                        if i > len(self.results[key]):
                            val = None
                        else:
                            val = self.results[key][i]
                        if val == None:
                            line += '-'
                        else:
                            if isinstance(val, float):
                                line += '%.4f' % val
                            else:
                                line += str(val)
                        line += '\t'

                    fo.write(line + '\n')

        if 'JSON' in self.format:
            black_list = []
            for k in self.results['manifest']:
                if k['dimension'] not in ('objs', 'single'):
                    black_list.append(k['key'])

            temp_json = {}
            for key in self.results:
                if key in black_list:
                    pass
                else:
                    value = self.results[key]
                    if 'numpy.ndarray' in str(type(value)):
                        if 'bool_' in str(type(value[0])):
                            temp_json[key] = ['True' if x else 'False' for x in value]
                        else:
                            temp_json[key] = [x if not np.isnan(x) else None for x in value]
                    else:
                        temp_json[key] = value

            output = json.dumps(temp_json)
        return (True, output)

    def run_error(self):
        """ Formats error messages, sending only the error and the error source """
        white_list = [
         'error', 'warning', 'origin']
        error_json = {key:val for key, val in self.results.items() if key in white_list}
        if 'TSV' in self.format:
            with open('error.tsv', 'w') as (fo):
                for key, value in error_json.items():
                    fo.write(key + '\t' + value + '\n')

        if 'JSON' in self.format:
            return (False, json.dumps(error_json))
        else:
            return (False, 'errors found')

    def run(self):
        """ Formats the results produced by "learn" or "apply" as appropriate """
        if 'error' in self.results:
            success, results = self.run_error()
        else:
            if self.results['origin'] == 'learn':
                success, results = self.run_learn()
            else:
                if self.results['origin'] == 'apply':
                    success, results = self.run_apply()
                else:
                    return (False, 'invalid result format')
        return (
         success, results)