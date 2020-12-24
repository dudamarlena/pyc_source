#!/usr/bin/env python

from setuptools import setup
import platform

DEFINE_VERSION = '0.3'

system = platform.system()

#add pykill to /usr/bin begin.
if system == 'Linux':
    try:
        f = open('/usr/bin/pykill', 'w')
        f.write("""#!/usr/bin/env python

import pykill.pykill as pykill
import sys

kw = sys.argv[1]
be_killed = pykill.kill_by_keyword(kw)
print 'killed:'
for line in be_killed:
    print line""")
        f.close()
        print 'copy pykill to /usr/bin'
        cmd = 'chmod 777 /usr/bin/pykill'
        commands.getstatusoutput(cmd)
        print cmd
    except Exception, ex:
        print 'Warning:' + str(ex)
#add pykill to /usr/bin end.

setup(
    name='pykill',
    version=DEFINE_VERSION,
    description='kill process by keyword',
    author='lyc',
    license='MIT',
    platforms = "linux",
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='pykill',
    packages=['pykill'],
    include_package_data=True
)