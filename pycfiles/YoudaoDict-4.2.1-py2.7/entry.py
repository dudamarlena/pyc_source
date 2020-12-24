# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/youdao/entry.py
# Compiled at: 2019-02-16 23:49:25
import json
from functools import wraps
from youdao.racer import Race
from youdao.sqlsaver import SQLSaver

def void_return(fun):
    """check void return"""

    @wraps(fun)
    def check(self):
        if not self.result or not self.valid:
            return ''
        return fun(self)

    return check


class Youdao(object):

    def __init__(self, phrase=''):
        self.phrase = phrase.lower()
        self.result = {}
        self.valid = True
        self.raw = ''
        self.is_new = False

    def set_phrase(self, phrase):
        self.phrase = phrase.lower()

    def valid_check(self):
        if not self.result:
            self.is_new = True
            self.valid = False
            return False
        if 'errorCode' not in self.result:
            self.is_new = True
        if not self.is_new:
            if 'translation' not in self.result or len(self.result['translation']) == 1 and self.result['translation'][0] == self.result['query']:
                self.valid = False

    def executor(self):
        race = Race(self.phrase)
        race.launch_race()
        self.result = race.result
        self.valid_check()
        return self.result

    def check_raw(self):
        return json.dumps(self.result, indent=2)

    @void_return
    def web(self):
        temp = ''
        if not self.is_new:
            if 'web' not in self.result:
                return temp
            temp += '网络释义 \x1b[01;34m>>>\x1b[00m\n'
            for i in self.result['web']:
                temp += ('\t{}\n\t').format(i['key'])
                for j in i['value']:
                    temp += '  ' + j + ','

                temp += '\n'

        elif 'web_translate' in self.result and self.result['web_translate']:
            temp += '网络释义 \x1b[01;34m>>>\x1b[00m\n'
            for i in self.result['web_translate']:
                temp += ('\t{}\n').format(i)

        return temp.strip()

    @void_return
    def trans(self):
        temp = ''
        if not self.is_new:
            temp += '翻译     \x1b[01;33m>>>\x1b[00m\n'
            for i in self.result['translation']:
                temp += ('\t{}\n').format(i)

        else:
            possibles = self.result.get('possibles', [])
            if possibles:
                temp += '相关词语     \x1b[01;33m>>>\x1b[00m\n'
                for i in possibles:
                    temp += ('\t{}\n\t{}\n\n').format(i['possible'], i['explain'])

            else:
                temp = ''
        return temp

    @void_return
    def basic(self):
        temp = ''
        if not self.is_new:
            data = self.result.get('basic', {})
            if not data:
                return temp
            temp += '基本释义 \x1b[01;32m>>>\x1b[00m\n'
            phonetic = data.get('phonetic', '')
            us_phonetic = data.get('us-phonetic', '')
            uk_phonetic = data.get('uk-phonetic', '')
            base = data.get('explains', '')
            if phonetic:
                temp += ('\t[{}]\n').format(phonetic)
            if us_phonetic:
                temp += ('\tus. [{}]\n').format(us_phonetic)
            if uk_phonetic:
                temp += ('\tuk. [{}]\n').format(uk_phonetic)
            if base:
                for i in base:
                    temp += ('\t{}\n').format(i)

        else:
            trans = self.result.get('translate', [])
            if trans:
                temp += '基本释义 \x1b[01;32m>>>\x1b[00m\n'
                pronounce = self.result.get('pronounces', [])
                for i in pronounce:
                    temp += ('\t{}\n').format(i)

                for i in trans:
                    temp += ('\t{}\n').format(i)

            else:
                temp = ''
        return temp

    @staticmethod
    def shred_auto_complete(shred):
        shreds = SQLSaver().shred_query(shred)
        return (' ').join(x[0] for x in shreds if len(shreds) > 1 and not x[0] == shred or x[0].startswith(shred))

    @staticmethod
    def complete_code():
        return '###-begin-youdao-completion-###\n# simple youdaoDict word auto completion script\n# Installation: youdao -cp >> ~/.bashrc  (or ~/.zshrc)\n# or youdao -cp >> ~/.bash_profile (.etc)\n#\n_youdao_parser_options()\n{\n  local curr_arg;\n  curr_arg=${COMP_WORDS[COMP_CWORD]}\n  COMPREPLY=( $(compgen -W "$(youdao --shard $curr_arg)" $curr_arg ) );\n}\ncomplete -F _youdao_parser_options youdao\n###-end-youdao-completion-###'


if __name__ == '__main__':
    youdao = Youdao()
    print youdao.shred_auto_complete('f')