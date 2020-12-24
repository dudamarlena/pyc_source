# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\msg_abstract.py
# Compiled at: 2017-12-13 03:23:02
# Size of source mod 2**32: 3481 bytes
from abc import ABCMeta, abstractmethod

class MsgFactoryAbstract(metaclass=ABCMeta):
    __doc__ = '\n    '

    @abstractmethod
    def msg_create(self):
        pass


class MsgFactory1(MsgFactoryAbstract):
    __doc__ = '\n    '

    def msg_create(self):
        return Msg1()


class MsgAbstract(metaclass=ABCMeta):
    __doc__ = '\n    '

    @abstractmethod
    def call_msg(self):
        pass


class Msg1(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return 'Yesなら 1  No なら 2 を入力してください。: '


class Msg2(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '入力値は 数値 で入力してください。'


class Msg3(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '正しい数値を入力してください。'


class Msg4(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '手動で1行ずつ実行しますか？ファイルを読み込んで一括で実行しますか？'


class Msg5(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '手動で実行なら 1  ファイルを読み込んで実行するなら 2 を入力してください。: '


class Msg6(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '実行したいSQL文を入力: '


class Msg7(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '正しいSQL文を入力してください。'


class Msg8(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '次のSQL文を実行する場合は 1 を、入力を中止する場合は 2 を入力: '


class Msg9(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return 'SQL文をファイルから読み込んで一括で実行します。読み込むファイルのパスを指定してください。: '


class Msg10(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '文字エンコーディングの指定 デフォルトはUTF-8 特に指定しない場合はそのままEnter'


class Msg11(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '使用できる値の例...utf_8, shift_jis, euc_jp, cp932, etc...: '


class Msg12(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return '実行結果を書き込むファイルのパスを指定 ex.. /var/log/aaa.log'


class Msg13(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return 'コンソールに出力する場合は 1 を入力してください:'


class Msg14(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return 'Unicodeエラーが検出されました。エラー内容に従って対処をしてください。'


class Msg15(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return 'このままCOMMITする場合は 1 , ROLLBACKする場合は 2 を入力してください。:'


class Msg16(MsgAbstract):
    __doc__ = '\n    '

    def call_msg(self):
        return __file__ + 'is ended.'


def main():
    pass


if __name__ == '__main__':
    main()