from setuptools import setup, find_packages

setup(
    name='hcquant',
    version='0.0.26',
    description=(
        'utils for hcquant'
    ),
    install_requires=[
        'bs4',
        'lxml', 
        'tushare',
        'cn-highcharts'
    ],
    # long_description=open('README.rst').read(),
    author='liubola',
    author_email='lby3523@gmail.com',
    # maintainer='<维护人员的名字>',
    # maintainer_email='<维护人员的邮件地址',
    license='Apache Software License',
    packages=find_packages(),
    platforms=["all"],
    url='https://simpleliu.cc',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
