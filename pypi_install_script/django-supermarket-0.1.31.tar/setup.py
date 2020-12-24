import os

import git
from setuptools import setup


def version():
    f = open("./version.txt", "r+", encoding='utf8')
    version = f.read()
    version = version.replace("\x00", "")
    version = version.split(".")
    build_number = int(version[2])
    build_number += 1
    version = "{}.{}.{}".format(version[0], version[1], build_number)
    f.truncate(0)
    f.write(version)
    f.close()
    return version


def readme():
    with open('README.md') as f:
        return f.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    'paypalrestsdk',
    'django-model-utils'
]

setup(
    name='django-supermarket',
    version=version(),
    packages=[
        'payment'
    ],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to facilitate e-commerce.',
    long_description='https://github.com/49e94b8f256530dc0d41f740dfe8a4c1/django-supermarket',
    install_requires=install_requires,
    url='https://blog.takeshispalace.com/',
    author='Ken Okech',
    author_email='kenokech94@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
