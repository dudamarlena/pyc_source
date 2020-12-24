"""
:authors: Wilidon
:license: , see LICENSE file

:copyright: (c) 2020 Wilidon
"""
from distutils.core import setup

setup(
    name='MpetsMobi',
    packages=['mpetsmobi', 'mpetsmobi.resources', 
              'mpetsmobi.resources.main', 
              'mpetsmobi.resources.profile'],
    version='0.4.4',
    license='MIT',
    description='DESCRIPTION',
    author='Wilidon',
    author_email='Wilidon@bk.ru',
    keywords=['mpetsapi', 'api', 'mpets.mobi'],
    install_requires=[
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
