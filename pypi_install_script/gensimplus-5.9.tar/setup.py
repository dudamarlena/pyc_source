# coding=utf-8


from setuptools import setup, find_packages
import os

CURPATH = os.path.dirname(os.path.abspath(__file__))
print(CURPATH)
CURPATH = os.path.dirname(os.path.realpath(__file__))
print(CURPATH)
CURPATH = "~/iba/dutil/gensimplus"
setup(
        name='gensimplus',
        version=5.3,
        description=(
            'gensim在项目中的公共应用方法'
        ),
        long_description=open('README.rst','r').read(),
        author='秦海宁',
        author_email='2364839934@qq.com',
        maintainer='秦海宁',
        maintainer_email='2364839934@qq.com',
        license='BSD License',
        packages=find_packages(),
        platforms=["all"],
    url='http://www.github.com/scmsqhn/gensimplus',
    classifiers=[
                'Development Status :: 4 - Beta',
                'Operating System :: OS Independent',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Programming Language :: Python',
                'Programming Language :: Python :: Implementation',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Topic :: Software Development :: Libraries'
    ],
)
