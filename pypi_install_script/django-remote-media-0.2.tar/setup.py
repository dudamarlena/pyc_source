from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='django-remote-media',
    version='0.2',
    url='https://github.com/jcmcp/django-remote-media',
    download_url='https://pypi.python.org/pypi/django-remote-media',
    license='MIT',
    author='John McPherson',
    author_email='jcmcph@gmail.com',
    description='Save remote files to django FileField',
    long_description=readme(),
    install_requires=[
        'requests',
        'Django',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ]
)
