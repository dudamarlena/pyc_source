
from os.path import join, dirname
from setuptools import setup


setup(
    name='instantlab_apiclient',
    version='0.2.6',
    maintainer='Andreas Grapentin',
    maintainer_email='andreas.grapentin@hpi.uni-potsdam.de',
    url='http://instantlab.org',
    description='An API to the instantlab middleware',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),

    keywords='instantlab api',
    packages=['instantlab_apiclient'],

    install_requires=[
        'requests'
    ],

    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    test_suite='tests',
    tests_require=[
        'pytest',
        'pytest-localserver',
    ],

    setup_requires=['pytest_runner'],
)
