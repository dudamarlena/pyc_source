from setuptools import setup
with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='lzbTestLib',
    version='0.0.3',
    description='这是刘子彬的python测试包',
    author="lzb",
    author_email="1835064412@qq.com",
    packages=['lzbTestLib'],
    py_modules=['Tool'],    # 指明单文件
    long_description= long_description,
    url='https://gitee.com/zibincode/PythonStudyDemo.git',
)

'''
 打包命令
 1. cd  到 具有setup.py文件的路径
 2. python3 setup.py sdist  发布包生成目标文件
 

'''