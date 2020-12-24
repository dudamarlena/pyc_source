from distutils.core import setup

setup(
    name='mis-logging',
    packages=['mis_logging'],
    version='0.0.2',
    license='bsd-3-clause',
    description='LOGGING FOR MIS PRODUCTS.',
    author='McKenzie Intelligence',
    author_email='dev@mckenzieintelligence.co.uk',
    url='https://gitlab.com/mckenzieintelligence-os/mis-logging',
    download_url='https://gitlab.com/mckenzieintelligence-os/mis-logging/-/archive/v0.0.1/mis-logging-v0.0.1.tar.gz',
    keywords=['LOGGING', 'MIS'],
    install_requires=['psutil'],
    classifiers=[
        'Development Status :: 3 - Alpha',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
    ],
)