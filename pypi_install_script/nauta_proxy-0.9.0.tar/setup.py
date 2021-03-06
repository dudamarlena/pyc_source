# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools.command.install import install
import os
import re


with open('nauta_proxy/__init__.py', 'rt', encoding='utf8') as fd:
    source = fd.read()
    author = re.search(r'__author__ = \'(.*?)\'', source, re.M).group(1)
    version = re.search(r'__version__ = \'(.*?)\'', source, re.M).group(1)


def create_shortcut():
    sh = os.path.join(os.path.expanduser('~'), '.shortcuts')
    if not os.path.exists(sh):
        os.mkdir(sh)
    sh = os.path.join(sh, 'Nauta-Proxy')
    with open(sh, 'w') as fd:
        fd.write('''#!/usr/bin/bash
CMD="nauta-proxy"
SELF="bash $0 -r"

if [ $# == 0 ]; then
    $CMD &
    sleep 1
fi

$CMD --stats | termux-notification -t "Nauta Proxy '''+version+'''" -i nauta_proxy --alert-once --ongoing --action "$SELF; $CMD --options" --button2 "Opciones" --button2-action "$CMD --options" --button1 "Refrescar" --button1-action "$SELF; $CMD --serverstats; $SELF"

if [ $# == 0 ]; then
    wait $!
fi''')
        os.system(
            'termux-notification --ongoing -t "Nauta Proxy {0}" -i nauta_proxy -c "Nauta Proxy {0} Instalado!\nPara iniciar el proxy ejecuta en Termux:\nnauta-proxy --stop; nauta-proxy" --action "{1}" --button1 "Aceptar" --button1-action "{1}"'.format(version, 'nauta-proxy --stop; nauta-proxy -n'))


class InstallCommand(install):
    def run(self):
        install.run(self)
        create_shortcut()


with open('README.rst') as fd:
    long_desc = fd.read()


setup(
    name='nauta_proxy',
    version=version,
    description='A simple Python proxy for Delta Chat and Nauta email server',
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    author=author,
    author_email='adbenitez@nauta.cu',
    url='https://github.com/adbenitez/nauta_proxy',
    packages=['nauta_proxy'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Topic :: Utilities',
                 'Programming Language :: Python :: 3'],
    entry_points='''
        [console_scripts]
        nauta-proxy=nauta_proxy:main
    ''',
    python_requires='>=3.5',
    # install_requires=[],
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'install': InstallCommand,
    },
)
