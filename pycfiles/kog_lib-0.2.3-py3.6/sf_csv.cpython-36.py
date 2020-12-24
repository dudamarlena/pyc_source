# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kog_lib\excel\sf_csv.py
# Compiled at: 2019-12-19 20:55:20
# Size of source mod 2**32: 3358 bytes
import csv, os
from pprint import pprint

class Csv:
    __doc__ = "\n        用于对csv格式的文件的加载, 生成, 打印.\n\n        example\n        -------\n        读取\n        c = Csv()\n        c.load('data1.csv')\n        c.print_list()\n        输出如下:\n        [['name', 'age', 'sex'],\n         ['japan', '20', 'man'],\n         ['taibei', '103', 'femail'],\n         ['russia', '43', 'man']]\n\n        也可以:\n        c = Csv(data1.csv)\n\n        生成一个csv的文件:\n        data = [['name', 'age', 'sex'],\n                ['japan', '20', 'man'],\n                ['taibei', '103', 'femail'],\n                ['russia', '43', 'man']]\n        c = Csv()\n        c.make(data, filename=name1.csv)\n\n        将会在本地目录下生成一个name1.csv的文件, 内容为data中的内容\n        "

    def __init__(self, file=None):
        self.rowNum = 0
        self.colNum = 0
        self.data = list()
        if file:
            if not os.path.isfile(file):
                raise FileNotFoundError('文件{}不存在'.format(file))
            else:
                self.load(file)

    def load(self, file: str):
        """'
        file:   str, 表示要加载的文件
        index： (int,str), 表示要加载的sheet
        """
        if not os.path.isfile(file):
            raise FileNotFoundError('文件不存在或不是文件')
        if not file.endswith('.csv'):
            raise TypeError('文件格式不正确, 必须以.csv结尾')
        with open(file, 'r') as (f):
            self.data = list(csv.reader(f))
            self.rowNum = len(self.data)
            self.colNum = len(self.data[0])
        print(f"文件{file}加载完毕～")

    def make(self, data, filename='name1.csv'):
        """生成一个excel文件"""
        if not filename.endswith('.csv'):
            raise TypeError(f"{filename}格式不对,不是以csv结尾")
        with open(filename, 'w', encoding='utf-8', newline='') as (f):
            csv_writer = csv.writer(f)
            csv_writer.writerows(data)

    def __str__(self):
        return str(vars(self))

    def print(self, part='all', n=100):
        """
        打印出来
        :return:
        """
        print('行：', self.rowNum, '列：', self.colNum)
        if part == 'all':
            for i in range(self.rowNum):
                for j in range(self.colNum):
                    print((self.data[i][j]), '\t\t', end='')

                print()

        else:
            if part == 'head':
                n = 0 if n - 1 <= 0 else self.rowNum if n - 1 >= self.rowNum else n
                for i in range(n):
                    for j in range(self.colNum):
                        print((self.data[i][j]), '\t\t', end='')

                    print()

            else:
                if part == 'tail':
                    n = 0 if n - 1 <= 0 else self.rowNum if n - 1 >= self.rowNum else n
                    for i in range(n - 1, self.rowNum):
                        for j in range(self.colNum):
                            print((self.data[i][j]), '\t\t', end='')

                        print()

                else:
                    raise ValueError(f"part参数{part}错误")

    def print_list(self):
        pprint(self.data)