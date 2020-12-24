from setuptools import setup

setup(
    name='nzpaye',
    version='0.1.0',
    description='NZ Paye Summary',
    long_description="""Calculate the NZ Paye Summary based on the hourly rate and the number of hours worked.""",
    url='https://github.com/anuj-ssharma/PayeSummary',
    author='Anuj Sharma',
    author_email='anuj576@gmail.com',
    license='MIT',
    packages=['nzpaye'],
    install_requires=['tabulate==0.8.7'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='nzpaye.test',
    tests_require=[
            'mock'
    ],
    entry_points={
        'console_scripts': [
            'nzpaye = nzpaye.__main__:main',
        ]
    }
)
