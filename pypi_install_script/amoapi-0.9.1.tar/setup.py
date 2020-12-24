from setuptools import setup

with open('README.md', encoding='utf8') as readme_file:
    long_description = readme_file.read()

setup(
    name='amoapi',
    version='0.9.1',
    packages=['amoapi'],
    url='https://github.com/digitalduke/amoapi',
    license='MIT license',
    author='George P. <digitalduke@gmail.com>, Dmitry Krukov <glebov.ru@gmail.com>',
    author_email='digitalduke@gmail.com',
    description='python API wrapper for amoCRM',
    long_description=long_description,
    long_description_content_type='text/markdown',
    requires=[
        'requests (>=2.3)',
        'responses (>=0.2.2,<0.6)',
        'six (>=1.7.3)',
        'pytz',
    ],
    install_requires=[
        'requests >=2.3',
        'responses >=0.2.2,<0.6',
        'six >=1.7.3',
        'pytz',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
