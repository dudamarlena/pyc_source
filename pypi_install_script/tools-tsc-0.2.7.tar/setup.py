# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
LONGDOC = """
作者:
    Shicheng Tan
    xxj.tan@gmail.com
包括:
    用于读取参数文件
    文件、xml、正则的一般处理/读写
    时间/过程处理
日志:
    2018年09月11日: 增加过程时间输出(ProgressAndTime)
    2018年09月13日: 增加pickle读写(FileProcess)等
    2018年09月14日: 增加简化的时间输出(ProgressAndTime.ProgressOut2)等
    2018-11-17：仿照 tqdm 增加 ProgressOut3，可以在循环中控制头部输出
"""

setup(name='tools-tsc',
      version='0.2.7',
      description="tsc's tools",
      long_description=LONGDOC,
      author='Shicheng Tan',
      author_email='xxj.tan@gmail.com',
      license='GPLv3',
      url='https://github.com/burongjiashe',
      keywords='tools',
      packages=find_packages(),

      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
      ],
      install_requires=[],
)
