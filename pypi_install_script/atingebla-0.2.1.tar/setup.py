from setuptools import find_packages, setup


def read(filename):
    with open(filename) as fp:
        return fp.read()


setup(
    name='atingebla',
    version='0.2.1',
    description='Gandi DNS auto-updater',
    long_description=read('Readme.rst'),
    keywords=['gandi', 'dns'],
    url='https://gitlab.com/fbochu/atingebla',
    author='Fabien Bochu',
    author_email='fabien.bochu+atingebla@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': str('src')},
    include_package_data=True,
    zip_safe=True,
    license='BSD',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': (
            'atingebla = atingebla.cli:main',
        ),
    },
)
