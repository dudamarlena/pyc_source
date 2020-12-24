# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/rain/RainHadoop.py
# Compiled at: 2012-09-06 11:03:15
"""
A shell command to dynamically deploy an Apache Hadoop environments on FG.

This command line tool deploys Apache Hadoop in to a FutureGrid resource 
and executes the given job. Users can specify a directory containing input 
data, which will get uploaded to the HDFS under the "input" directory. 
Users can also specify a directory to download the output data (contents 
of the "output" directory) from HDFS. HADOOP_HOME environment variable, 
pointing to the Hadoop distribution, needs to be set before running this 
command.
"""
__author__ = 'Thilina Gunarathne, Javier Diaz'
import subprocess, time, sys, os, argparse
from random import randrange
import re

class RainHadoop(object):

    def __init__(self):
        super(RainHadoop, self).__init__()
        self._hpc = False
        self._hdfsDir = None
        self._dataInputDir = None
        self._dataOutputDir = None
        self._hadoopDir = None
        self._hadoopConfDir = None
        return

    def getDataOutputDir(self):
        return self._dataOutputDir

    def getDataInputDir(self):
        return self._dataInputDir

    def getHpc(self):
        return self._hpc

    def setHpc(self, hpc):
        self._hpc = hpc

    def setHadoopConfDir(self, hadoopConfDir):
        self._hadoopConfDir = hadoopConfDir

    def setDataInputDir(self, dataInputDir):
        self._dataInputDir = dataInputDir

    def setDataOutputDir(self, dataOutputDir):
        self._dataOutputDir = dataOutputDir

    def setHadoopDir(self, hadoopDir):
        self._hadoopDir = hadoopDir

    def setHdfsDir(self, hdfsDir):
        if hdfsDir:
            self._hdfsDir = hdfsDir
        else:
            self._hdfsDir = '/tmp/'

    def generate_shutdown(self):
        job_script = ''
        if self._dataOutputDir:
            job_script = 'hadoop fs -rmr ' + os.path.basename(self._dataOutputDir.rstrip('/')) + '\n'
        job_script += 'stop-mapred.sh\n'
        job_script += 'stop-dfs.sh\n'
        return job_script

    def generate_runjob(self, hadoop_command):
        job_script = 'sleep 10 \n'
        if self._dataInputDir:
            job_script += 'hadoop fs -put '
            job_script += self._dataInputDir + ' ' + os.path.basename(self._dataInputDir.rstrip('/')) + ' \n'
        job_script += 'echo Running the hadoop job  \n'
        if not re.search('^hadoop', hadoop_command):
            job_script += 'hadoop '
        job_script += hadoop_command + '\n \n'
        if self._dataOutputDir:
            job_script += 'hadoop fs -get ' + os.path.basename(self._dataOutputDir.rstrip('/')) + ' '
            job_script += self._dataOutputDir + ' \n'
        return job_script

    def generate_config_hadoop(self, randfile, randir, randhadooptempdir, randhadoophdfsdir):
        job_script = 'echo Generating Configuration Scripts \n'
        job_script += 'python ' + randir + '/' + randfile + 'RainHadoopSetupScript.py --hostfile '
        if self._hpc:
            job_script += ' $PBS_NODEFILE '
        else:
            job_script += ' $HOME/machines '
        if self._hdfsDir:
            self._hdfsDir += '/' + randhadoophdfsdir
        else:
            self._hdfsDir += '/' + randhadoophdfsdir
        job_script += ' --hdfs ' + str(self._hdfsDir)
        job_script += ' --tempdir ' + randhadooptempdir + ' \n'
        return job_script

    def generate_start_hadoop(self):
        job_script = 'echo Formatting HDFS  \n'
        job_script += 'hadoop namenode -format   \n\n'
        job_script += 'echo Starting the cluster  \n'
        job_script += 'start-dfs.sh \n'
        job_script += 'echo Waiting in the safemode  \n'
        job_script += 'hadoop dfsadmin -safemode wait \n'
        job_script += 'echo Starting MapReduce daemons  \n'
        job_script += 'start-mapred.sh  \n'
        return job_script

    def save_job_script(self, job_name, job_script):
        job_script_name = job_name
        job_script_file = open(job_script_name, 'w')
        job_script_file.write(job_script)
        job_script_file.close()
        return job_script_name