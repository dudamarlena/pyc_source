# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/grsync/bootstrap.py
# Compiled at: 2020-04-26 00:22:04
# Size of source mod 2**32: 2469 bytes
import logging
logger = logging.getLogger(__name__)

class BootstrapGenerator(object):
    __doc__ = '\n    Generate the script that creates the distribution on the target machine.\n\n    '
    SCRIPT = '#!/bin/sh\n\nif [ $# -eq 0 ] ; then\n    echo "usage: $0 <python_dir> [grsync dir] [python<version>]"\n    echo "where: python_dir is the bin directory where python is installed"\n    echo "       grsync_dir is the distribution directory copied from the source"\n    echo "       python<version> is the version of python (i.e. python3.6)"\n    exit 1\nfi\nNATIVE_PYTHON_BIN_DIR=$1\n\nif [ $# -ge 2 ]; then\n    echo "setting inst dir: $2"\n    GRSYNC_INST_DIR=$2\nelse\n    GRSYNC_INST_DIR=`pwd`\nfi\n\nif [ $# -ge 3 ]; then\n    echo "setting python ver: $3"\n    PYTHON_VER=$3\nelse\n    PYTHON_VER=$NATIVE_PYTHON_BIN_DIR\nfi\n\nPYTHON_DIR=${HOME}/opt/lib/python3\nPIP=${PYTHON_DIR}/bin/pip\nVIRTUAL_ENV=${NATIVE_PYTHON_BIN_DIR}/virtualenv\nPYTHON_PAR=`dirname $PYTHON_DIR`\nWHEELS_DIR=${GRSYNC_INST_DIR}/%(wheel_dir)s\nWHEELS=${WHEELS_DIR}/*.whl\n\nif [ -f ${PIP} ] ; then\n    PIP=${PYTHON_DIR}/bin/pip3\nfi\n\necho "GRSYNC_INST_DIR=${GRSYNC_INST_DIR}"\necho "PYTHON_DIR=${PYTHON_DIR}"\necho "PYTHON_VER=${PYTHON_VER}"\necho "PIP=${PIP}"\necho "VIRTUAL_ENV=${VIRTUAL_ENV}"\necho "PYTHON_PAR=${PYTHON_PAR}"\necho "WHEELS_DIR=${WHEELS_DIR}"\necho "WHEELS=${WHEELS}"\n\nif [ ! -e "${VIRTUAL_ENV}" ] ; then\n    echo "virtual environment not installed: \'pip3 install virtualenv\'"\n    exit 1\nfi\n\necho "bootstrapping python env in ${PYTHON_DIR}, wheels: ${WHEELS}"\n\nrm -rf $PYTHON_PAR\n\ncmd="${VIRTUAL_ENV} -p ${PYTHON_VER} `basename ${PYTHON_DIR}`"\n\necho "invoke $cmd"\nmkdir -p $PYTHON_PAR &&     cd $PYTHON_PAR &&     $cmd &&     cd - || exit 1\n\nif [ -d ${WHEELS_DIR} ] ; then\n    echo "installing from wheel"\n    ${PIP} install ${GRSYNC_INST_DIR}/%(wheel_dir)s/zensols.grsync*\nelse\n    echo "installing from net"\n    ${PIP} install zensols.grsync\nfi\n\n# ${PIP} install ${WHEELS}\n\nrm ${HOME}/.bash* ${HOME}/.profile*\n# echo to thaw the repo: ${PYTHON_DIR}/bin/grsync thaw -d ${GRSYNC_INST_DIR}\n${PYTHON_DIR}/bin/grsync thaw -d ${GRSYNC_INST_DIR}\n'
    PARAM_PATH = 'discover.bootstrap'

    def __init__(self, config):
        self.config = config

    def generate(self, path):
        params = self.config.get_options(self.PARAM_PATH)
        script = self.SCRIPT % params
        logger.info('creating bootstrap script at: {}'.format(path))
        with open(path, 'w') as (f):
            f.write(script)