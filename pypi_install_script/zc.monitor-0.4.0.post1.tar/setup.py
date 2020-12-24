from setuptools import setup, find_packages

name = 'zc.monitor'

long_description = (open('src/zc/monitor/README.txt').read() +
                    "\n\n" +
                    open('CHANGES.rst').read())

setup(
    name=name,
    version='0.4.0.post1',
    author='Jim Fulton',
    author_email='jim@zope.com',
    license='ZPL 2.1',
    keywords='zope3',
    description=open('README.txt').read().strip(),
    long_description=long_description,
    url='https://github.com/zopefoundation/zc.monitor',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=find_packages('src'),
    namespace_packages=['zc'],
    package_dir={'': 'src'},
    install_requires=[
        'setuptools', 'zc.ngi', 'zope.component', 'zope.testing',
    ],
    include_package_data=True,
    zip_safe=False,
)
