from setuptools import setup


setup_requires = [
    'google-cloud-logging==1.6.0',
    'google-cloud-trace==0.19.0',
    'grpcio==1.14.1',
    'opencensus==0.1.5'
]

install_requires = [
]

dependency_links = [
]

setup(
    name='ino-vibe-sdk',
    version='0.1.1',
    description='Ino-Vibe SDK for Python',
    author='Joonkyo Kim',
    author_email='jkkim@ino-on.com',
    packages=['inovibe'],
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=setup_requires,
    dependency_links=dependency_links,
    # scripts=['manage.py'],
    entry_points={
        'console_scripts': [
        ],
        "egg_info.writers": [
            "foo_bar.txt = setuptools.command.egg_info:write_arg",
        ],
    },
)
