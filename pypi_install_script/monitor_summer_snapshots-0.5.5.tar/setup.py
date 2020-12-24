from io import open

from setuptools import find_packages, setup

version = '0.5.5'

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

REQUIRES=[
    'asn1crypto==0.24.0',
    'bcrypt==3.1.4',
    'certifi==2018.4.16',
    'cffi==1.11.5',
    'chardet==3.0.4',
    'cryptography==2.2.2',
    'idna==2.7',
    'influxdb==5.0.0',
    'paramiko==2.4.1',
    'py-zabbix==1.1.5',
    'pyasn1==0.4.3',
    'pycparser==2.18',
    'PyNaCl==1.2.1',
    'python-dateutil==2.7.3',
    'pytz==2018.4',
    'PyYAML==5.1',
    'requests==2.19.1',
    'six==1.11.0',
    'urllib3==1.23'
]

setup(
    name='monitor_summer_snapshots',
    version=version,
    description='Scan summer volumes and get snapshots sizes. Report the numbers in various storage systems (currently influxdb and zabbix supported)',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='Jonathan Schaeffer',
    author_email='jonathan.schaeffer@univ-grenoble-alpes.fr',
    maintainer='Jonathan Schaeffer',
    maintainer_email='jonathan.schaeffer@univ-grenoble-alpes.fr',
    url='https://gricad-gitlab.univ-grenoble-alpes.fr/schaeffj/monitoring-summer-snapshot',
    license='GPLv3',
    entry_points={
        'console_scripts': ['monitor_summer_snapshots = monitor_summer_snapshots:main']
    },

    data_files=[('/etc/monitor_summer_snapshots/',[
        'monitor_summer_snapshots/config.yml.example',
        'monitor_summer_snapshots/logger.conf',
        'monitor_summer_snapshots/zabbix_discovery.py'
    ]),
               ('doc',['monitor_summer_snapshots/graphana_dashboard.json','monitor_summer_snapshots/zabbix_template.xml'])
    ],
    keywords=[
        'monitoring',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    packages=find_packages(),
)
