# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/chinesename/chinesename.py
# Compiled at: 2018-07-22 21:38:48
import json, random, os
__all__ = [
 'ChineseName']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LASTFILE = os.path.join(BASE_DIR, 'source/lastnames.txt')
FIRSTFILE = os.path.join(BASE_DIR, 'source/firstnames.txt')
BOYFILE = os.path.join(BASE_DIR, 'source/boy.json')
GIRLFILE = os.path.join(BASE_DIR, 'source/girl.json')

class ChineseName(object):
    u"""中文名取名"""

    def __init__(self, firstname_file=FIRSTFILE, lastname_file=LASTFILE):
        u"""初始化
        Args:
            firstname_file: 名字文件路径 - String
            lastname_file：姓氏文件路径 - String
            以上两个路径参数有默认值，也可由用户自定义，文件内容以空格分隔即可
        """
        self._firstnames = self._getChars(firstname_file)
        self._lastnames = self._getChars(lastname_file)
        self._loadFirstName()

    def _getChars(self, filename):
        u"""获取中文字符列表
        Args:
            filename: 文件路径 - String (空格分隔文件)
        Returns:
            List: 字符列表
        Raise:
            file not find
        """
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as (f):
                chars = f.read().split(' ')
                return chars
        else:
            raise IOError('file not find!')

    def _loadFirstName(self):
        u"""
        加载男孩女孩名字
        """
        with open(BOYFILE, 'r', encoding='utf-8') as (f):
            self._boy_firstnames = json.loads(f.read())
        with open(GIRLFILE, 'r', encoding='utf-8') as (f):
            self._girl_firstnames = json.loads(f.read())

    def getLastName(self):
        u"""获取姓氏
        Args:
            None
        Returns:
            String: 姓氏
        """
        return random.choice(self._lastnames)

    def _getFirstName(self, char_count=1, sex='boy'):
        u"""
        获取名字
        :param char_count: {int} 名字字数
        :param sex: {str} 性别 (boy | girl)
        :return: {srt} 名字
        """
        firstnames = {'boy': self._boy_firstnames, 
           'girl': self._girl_firstnames}
        try:
            return random.choice(firstnames.get(sex).get(str(char_count)))
        except KeyError:
            raise KeyError('please input char_count between 1-2')

    def getGirlFirstName(self, char_count=1):
        u"""
        获取一个女孩名字
        :param char_count:  {int} 名字字数
        :return: {str} 名字
        """
        return self._getFirstName(char_count, sex='boy')

    def getBoyFirstName(self, char_count=1):
        u"""
        获取一个男孩名字
        :param char_count:  {int} 名字字数
        :return: {str} 名字
        """
        return self._getFirstName(char_count, sex='girl')

    def getFirstName(self, char_count=1, sex=None):
        u"""获取名字
        Args:
            char_count: {int} 名字长度，默认1
            sex: {str} 性别(boy | girl)
        Returns:
            String: 名字
        """
        if sex == 'boy':
            firstname = self.getBoyFirstName(char_count)
        elif sex == 'girl':
            firstname = self.getGirlFirstName(char_count)
        else:
            firstname = []
            for i in range(char_count):
                firstname.append(random.choice(self._firstnames))

            firstname = ('').join(firstname)
        return firstname

    def getName(self, char_count=1, lastname='', sex=None):
        u"""获取一个中文姓名
        Args:
            char_count: 名字长度，默认1 - Integer
            lastname: 姓氏，默认随机 - String
            sex: {str} 性别(boy | girl)
        Returns:
            String: 姓名
        """
        name = []
        if lastname == '':
            name.append(self.getLastName())
        else:
            name.append(lastname)
        name.append(self.getFirstName(char_count, sex))
        name = ('').join(name)
        return name

    def getBoyName(self, char_count=1, lastname=''):
        u"""
        获取男孩姓名
        :param char_count: {int} 名字长度，默认1
        :param lastname: {str} 姓氏 默认随机
        :return: {str} 姓名
        """
        return self.getName(char_count, lastname, sex='boy')

    def getGirlName(self, char_count=1, lastname=''):
        u"""
        获取女孩姓名
        :param char_count: {int} 名字长度，默认1
        :param lastname: {str} 姓氏 默认随机
        :return: {str} 姓名
        """
        return self.getName(char_count, lastname, sex='girl')

    def getNames(self, count, char_count=1, lastname='', sex=None):
        u"""获取一个中文姓名列表
        Args:
            count: 名字数量 - Integer
            char_count: 名字长度，默认1 - Integer
            lastname： 姓氏，默认随机 - String
            sex: {str} 性别(boy | girl)
        Returns:
            List: 姓名列表
        """
        names = []
        for i in range(count):
            names.append(self.getName(char_count, lastname, sex))

        return names

    def getNameGenerator(self, count, char_count=1, lastname='', sex=None):
        u"""获取一个中文姓名生成器，2018年1月22日
        Args:
            count: 名字数量 - Integer
            char_count: 名字长度，默认1 - Integer
            lastname： 姓氏，默认随机 - String
            sex: {str} 性别(boy | girl)
        Returns:
            Yield：姓名生成器
        """
        for i in range(count):
            yield self.getName(char_count, lastname, sex)


def main():
    chinesename = ChineseName()
    name = chinesename.getName(lastname='白', sex='boy')
    print name
    names = chinesename.getNames(100, char_count=2, lastname='彭')
    print names
    name_generator = chinesename.getNameGenerator(10)
    print name_generator


if __name__ == '__main__':
    main()