from setuptools import setup, find_packages

setup(
    name='ngs',
    version='0.2.5',
    packages=find_packages(),
    install_requires=[
        "aiohttp==3.6.2",
        "aioredis==1.2.0",
        "redis==3.3.11",
        "asgiref==3.2.3",
        "channels==2.3.1",
        "channels-redis==2.4.1",
        "daphne==2.3.0",
        "Django==2.2.6",
        "djangorestframework==3.10.3",
        "mysqlclient==1.4.4",
        "PyYAML==5.1.2",
        "Twisted==19.7.0",
        "protobuf>=3.9.0",
        "psutil==5.6.3",
        "pysnmp==4.4.9",
        "ipython==7.9.0"
    ],
    include_package_data=True,
    url='https://broadtech.com.cn',
    license='GNU General Public License v3.0',
    author='Lee',
    author_email='canyun@live.com',
    description='ngs system',
)
