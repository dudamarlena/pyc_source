from setuptools import setup

setup(
    name="SuperMS",
    description='Supercalifragilisticexpialidocius Monitoring System project',
    author='Daniel Herkel',
    author_email="madalinadaniel60@gmail.com",
    version=2.0,
    url='https://github.com/daniel00oo/CloudBaseSMS',
    scripts=[
        'receive2.py',
        'send.py',
        'Receiver.py',
        'Sender.py',
        'Repeat.py',
        'StorageMongoDB.py',
    ],
    packages=['tools'],
    package_dir={'tools': './tools'},
    package_data={'tools': []},
    install_requires=[
        'pymongo',
        'pika',
    ],
    )