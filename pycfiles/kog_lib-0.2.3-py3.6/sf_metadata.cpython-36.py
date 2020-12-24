# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kog_lib\metadata\sf_metadata.py
# Compiled at: 2020-01-07 05:06:01
# Size of source mod 2**32: 5213 bytes
import os, collections

class SFMetadata:

    def __init__(self):
        self._SFMetadata__metadata_dict = collections.OrderedDict()
        self._SFMetadata__init_metadata_dict()

    def __init_metadata_dict(self):
        self._SFMetadata__metadata_dict['LHD'] = ''
        self._SFMetadata__metadata_dict['DBN'] = ''
        self._SFMetadata__metadata_dict['SES'] = ''
        self._SFMetadata__metadata_dict['BLANK1'] = ''
        self._SFMetadata__metadata_dict['SRC'] = ''
        self._SFMetadata__metadata_dict['DIR'] = ''
        self._SFMetadata__metadata_dict['LBN'] = ''
        self._SFMetadata__metadata_dict['CCD'] = ''
        self._SFMetadata__metadata_dict['BEG'] = ''
        self._SFMetadata__metadata_dict['END'] = ''
        self._SFMetadata__metadata_dict['REP'] = ''
        self._SFMetadata__metadata_dict['RED'] = ''
        self._SFMetadata__metadata_dict['RET'] = ''
        self._SFMetadata__metadata_dict['BLANK2'] = ''
        self._SFMetadata__metadata_dict['SAM'] = ''
        self._SFMetadata__metadata_dict['SNB'] = ''
        self._SFMetadata__metadata_dict['SBF'] = ''
        self._SFMetadata__metadata_dict['SSB'] = ''
        self._SFMetadata__metadata_dict['QNT'] = ''
        self._SFMetadata__metadata_dict['NCH'] = ''
        self._SFMetadata__metadata_dict['BLANK3'] = ''
        self._SFMetadata__metadata_dict['SCD'] = ''
        self._SFMetadata__metadata_dict['SEX'] = ''
        self._SFMetadata__metadata_dict['AGE'] = ''
        self._SFMetadata__metadata_dict['ACC'] = ''
        self._SFMetadata__metadata_dict['ACT'] = ''
        self._SFMetadata__metadata_dict['BIR'] = ''
        self._SFMetadata__metadata_dict['BLANK4'] = ''
        self._SFMetadata__metadata_dict['MIP'] = ''
        self._SFMetadata__metadata_dict['MIT'] = ''
        self._SFMetadata__metadata_dict['SPP'] = ''
        self._SFMetadata__metadata_dict['SCC'] = ''
        self._SFMetadata__metadata_dict['BLANK5'] = ''
        self._SFMetadata__metadata_dict['LBR'] = ''
        self._SFMetadata__metadata_dict['BLANK6'] = ''

    def load_template(self, filepath):
        lines = self._SFMetadata__get_file_lines(filepath)
        self._SFMetadata__metadata_dict.clear()
        count = 0
        try:
            for line in lines:
                if line.strip() == '':
                    count += 1
                    key, value = 'BLANK' + str(count), ''
                else:
                    if ' ' not in line.strip():
                        key, value = line, ''
                    else:
                        key, value = line.split(' ', 1)
                if key not in self._SFMetadata__metadata_dict.keys():
                    self._SFMetadata__metadata_dict[key] = value
                else:
                    self._SFMetadata__metadata_dict.clear()
                    self._SFMetadata__init_metadata_dict()
                    raise TypeError(f"{filepath}中有重复的key:{key}")

        except Exception as e:
            raise ValueError(f"{e}:{line}")
            raise ValueError(f"{filepath}模板内容有问题，无法区分key-value")

    def set_metadata_element(self, key, value):
        try:
            self._SFMetadata__metadata_dict[key] = value
        except Exception as e:
            raise ValueError(e)

        return True

    def get_metadata_element(self, key):
        if key in self._SFMetadata__metadata_dict:
            return self._SFMetadata__metadata_dict[key]
        raise ValueError(e)

    def make_metadata(self, output):
        if not output.endswith('.metadata'):
            print(f"文件后缀有误: {output}")
            return False
        else:
            write_list = []
            try:
                for key, value in self._SFMetadata__metadata_dict.items():
                    if 'BLANK' in key:
                        write_list.append('')
                    else:
                        write_list.append(key + ' ' + value)

                self._SFMetadata__write_lines(output, write_list)
            except Exception as e:
                raise ValueError(e)

            return True

    def __get_file_lines(self, file_path):
        new_lines = []
        with open(file_path, 'r', encoding='utf-8') as (f):
            for line in f:
                new_lines.append(line.strip())

        return new_lines

    def __write_lines(self, file_path, write_list, mode='w'):
        write_str = '\n'.join(write_list)
        self._SFMetadata__write_file(file_path, write_str, mode=mode)

    def __write_file(self, file_path, write_str, mode='w'):
        with open(file_path, mode, encoding='utf-8') as (f):
            f.write(write_str + '\n')

    @staticmethod
    def help():
        print('\n        ------------SFMetadata类 使用方法---------------------------------------------\n        import kog_lib\n\n        实例化: \n            my_metadata = kog_lib.SFMetadata()\n                此时会实例化一个默认的metadata模板\n\n        导入metadata模板: \n            my_metadata.load_template(filepath)\n                也可以读取现有的metadata文件作为模板\n\n        修改metadata文件内容: \n            my_metadata.set_metadata_element(key,value)\n                如: my_metadata.set_metadata_element("BIR","北美")\n\n        获取metadata某个key的值: \n            my_metadata.get_metadata_element(key)\n                如: value = my_metadata.get_metadata_element("BIR") # value="北美"\n\n        生产metadata文件: \n            my_metadata.make_metadata(output)\n                如: my_metadata.make_metadata("/data/xxxx.metadata")\n        ----------------------------------------------------------------------------\n        ')