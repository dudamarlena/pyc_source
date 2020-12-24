import glob
import os
import sys
from setuptools import setup, Extension
from setuptools.command.build_py import build_py as _build_py

VERSION = '1.0.1'


def read(f):
    return open(f, 'r', encoding='utf-8').read()


class build_ext_first(_build_py):
    def move_extension_to_package(self):
        for f in glob.glob("build/lib.**/*.so", recursive=False):
            chunks = f.split("/")
            new_name = "/".join([chunks[0], chunks[1], "nabto_client", chunks[2]],)
            print(f"Moving {f} to {new_name}")
            os.rename(f, new_name)
    
    def run(self):
        self.run_command('build_ext')
        _build_py.run(self)
        # self.move_extension_to_package()

os_type = ""
if sys.platform == "linux":
    os_type = "linux64"
elif sys.platform == "win32":
    os_type = "win32"
elif sys.platform == "win64":
    os_type = "win64"
elif sys.platform == "darwin":
    os_type = "mac64"

nabto_cpython = Extension(
    'nabto',
    sources=[
        'extension/src/nabto.c'
    ],
    include_dirs=['extension/{0}/include/'.format(os_type)],
    library_dirs=['extension/{0}/lib/'.format(os_type)],
    libraries=['nabto_client_api_static', 'nabto_static_external', 'stdc++'],
)

setup(
    name='nabto_client',
    version=VERSION,
    cmdclass={'build_py': build_ext_first},
    packages=['nabto_client'],
    author='Alexandru Gandrabur',
    author_email='alexandru.gandrabur@tremend.com',
    description="""Nabto Client Wrapper for Python""",
    url='https://www.nabto.com/developer',
    license='MIT',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
    ext_modules=[nabto_cpython],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: MIT License',
    ],
)
