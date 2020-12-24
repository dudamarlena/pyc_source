# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZhongLP/segmenter_pk/shortest_bigram.py
# Compiled at: 2019-12-21 11:19:16
# Size of source mod 2**32: 5638 bytes
import os, pickle

def save_data_to_pkl(data, file_path):
    with open(file_path, 'wb') as (fp):
        pickle.dump(data, fp)


def load_data_from_pkl(file_path):
    with open(file_path, 'rb') as (fp):
        data = pickle.load(fp)
    return data


class ShortestBigramSegmenter(object):
    __doc__ = '\n    '

    def __init__(self):
        """
        """
        self.reset()

    def reset(self):
        """
        """
        self._custom_dict = {}
        self._token_index = {}
        self._bigram_freq = None
        self._smoothen_eps = 0.0001
        file_dir = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.abspath(os.path.join(file_dir, '../zzz_data'))
        file_token_index = os.path.join(data_dir, 'token_index.py')
        file_bigram_freq = os.path.join(data_dir, 'bigram_freq.py')
        print('file_token_index: %s' % file_token_index)
        print('file_bigram_freq: %s' % file_bigram_freq)
        print('the real format of the data files is pkl (not py)')
        self.load_data_all(file_token_index, file_bigram_freq)

    def load_data_all(self, file_token_index, file_bigram_freq):
        """
        """
        self._token_index = load_data_from_pkl(file_token_index)
        self._bigram_freq = load_data_from_pkl(file_bigram_freq)
        self._eps_per_t = self._smoothen_eps / max(100, len(self._token_index))

    def load_custom_dict_file(self, file_path):
        """
        """
        with open(file_path, 'r', encoding='utf-8') as (fp):
            lines = fp.readlines()
            for line in lines:
                line = ''.join(line.strip().split())
                if len(line) == 0:
                    pass
                else:
                    str_arr = line.split()
                    if len(str_arr) > 1:
                        score = float(str_arr[1])
                    else:
                        score = 1.0
                    self.add_custom_token(str_arr[0], score)

    def add_custom_token(self, token, score=1.0):
        self._custom_dict[token] = score

    def remove_custom_token(self, token):
        if token in self._custom_dict:
            self._custom_dict.pop(token)

    def segment(self, text):
        """
        """
        all_paths = self.enumerate_all_paths(text)
        self.calculate_score_bf(all_paths)
        score, tokens = self.get_shortest_path(all_paths)
        return tokens

    def split(self, s, pos=0):
        """ 算出全部的路径, 递归
        """
        if len(s) <= pos:
            return [
             {'key': '<end>'}]
        else:
            result = []
            for k in self._custom_dict.keys():
                end = pos + len(k)
                if len(k) > 1 and end <= len(s) and k == s[pos:end]:
                    result.append({'key':k,  'childs':self.split(s, end)})

            for k in self._token_index.keys():
                end = pos + len(k)
                if len(k) > 1 and end <= len(s) and k == s[pos:end]:
                    result.append({'key':k,  'childs':self.split(s, end)})

            result.append({'key':s[pos:pos + 1],  'childs':self.split(s, pos + 1)})
            return result

    def enumerate_all_paths(self, s):
        return {'key':'<begin>', 
         'childs':self.split(s)}

    def calculate_score_bf(self, node):
        """ 根据bigram频率计算边的权值(得分)，递归
        """
        k = node['key']
        childs = node.get('childs')
        if not childs:
            return
        i1 = self._token_index.get(k)
        for child in childs:
            k2 = child['key']
            if k2 in self._custom_dict:
                child['score'] = self._custom_dict[k2]
            else:
                i2 = self._token_index.get(k2)
                child['score'] = self._bigram_freq[(i1, i2)] if (i1 and i2) else (self._eps_per_t)
            self.calculate_score_bf(child)

    def calculate_score_tf(self, node):
        """ 根据词语频率计算边的权值(得分)，递归
        """
        k = node['key']
        childs = node.get('childs')
        if not childs:
            return
        else:
            if k in self._custom_dict:
                node['score'] = self._custom_dict[k]
            else:
                if k in self._token_freq:
                    node['score'] = self._token_freq[k]
                else:
                    node['score'] = self._eps_per_t
        for child in childs:
            self.calculate_score_tf(child)

    def get_shortest_path(self, node):
        """ 求最大得分的路径，递归
        """
        childs = node.get('childs')
        score = node.get('score', 0)
        key = node.get('key')
        if not childs:
            return (score, [key])
        else:
            current_score, current_seq = -1, []
            for child in childs:
                _score, _seq = self.get_shortest_path(child)
                if _score > current_score:
                    current_score, current_seq = _score, _seq

            return (
             current_score + score, [key] + current_seq)


if __name__ == '__main__':
    pass