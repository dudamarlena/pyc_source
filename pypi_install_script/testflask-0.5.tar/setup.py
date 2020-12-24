from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='testflask',
    version='0.5',
    description='Test flask applications easily.',
    long_description=readme(),
    url='avoid3d.co.za/testflask',
    author='Pierre Hugo',
    author_email='avoid3d@gmail.com',
    license='MIT',
    packages=['testflask'],
    install_requires=[
        'mechanize',
        ],
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    zip_safe=False)
