from setuptools import setup, find_packages

setup(
    name='sangreal',
    version='0.0.1',
    description=(
        'sangreal for quant'
    ),
    install_requires=[
        # 'bs4',
        # 'lxml', 
        # 'tushare',
        # 'requests',
        # 'cn-highcharts',
        # 'alphalens',
    ],
    # long_description=open('README.rst').read(),
    author='liubola',
    author_email='lby3523@gmail.com',
    # maintainer='<维护人员的名字>',
    # maintainer_email='<维护人员的邮件地址',
    license='Apache Software License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/liubola',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
