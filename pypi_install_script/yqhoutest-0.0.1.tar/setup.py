from setuptools import setup, find_packages


TEST_VERSION = '0.0.1'

setup(
    name='yqhoutest',
    version=TEST_VERSION,
    packages=["yqhouhello",],
    entry_points={
        "console_scripts": ['']
    },
    install_requires=[
     ],
    url='http://gitlab.aibee.cn/ProductAnalysis/AutoTraining/tree/master/HotproductAutoTrain',
    license='GNU General Public License v3.0',
    author='yqhou',
    author_email='1773054317@qq.com',
    description='just for test'
)
