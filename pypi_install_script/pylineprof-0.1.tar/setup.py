from setuptools import setup, Extension


setup(
    name='pylineprof',
    version='0.1',
    description='Python line profiler',
    long_description=open('readme.rst').read(),
    author='Nazar Kanaev',
    author_email='nkanaev@live.com',
    url='https://github.com/nkanaev/pylineprof',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['pylineprof'],
    ext_modules=[Extension('pylineprof._profile', ['pylineprof/_profile.c'])],
    include_package_data=True,
)
