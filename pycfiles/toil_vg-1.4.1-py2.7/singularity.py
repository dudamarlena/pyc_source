# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/singularity.py
# Compiled at: 2018-11-03 15:09:40
"""
    Module for running Docker images with Singularity.   
    Derived from https://github.com/BD2KGenomics/toil/blob/master/src/toil/lib/docker.py

    Contains two user-facing functions: singularityCall and singularityCheckOutput
    Example of using singularityCall in a Toil pipeline to index a FASTA file with SAMtools:
        def toil_job(job):
            work_dir = job.fileStore.getLocalTempDir()
            path = job.fileStore.readGlobalFile(ref_id, os.path.join(work_dir, 'ref.fasta')
            parameters = ['faidx', path]
            singularityCall(job, tool='quay.io/ucgc_cgl/samtools:latest', work_dir=work_dir, parameters=parameters)
"""
import base64, logging, subprocess, pipes, os
_logger = logging.getLogger(__name__)

def singularityCall(job, tool, parameters=None, workDir=None, singularityParameters=None, outfile=None):
    """
    Throws CalledProcessorError if the Singularity invocation returns a non-zero exit code
    This function blocks until the subprocess call to Singularity returns
    :param toil.Job.job job: The Job instance for the calling function.
    :param str tool: Name of the Docker image to be used (e.g. quay.io/ucsc_cgl/samtools:latest).
    :param list[str] parameters: Command line arguments to be passed to the tool.
           If list of lists: list[list[str]], then treat as successive commands chained with pipe.
    :param str workDir: Directory to mount into the container via `-v`. Destination convention is /data
    :param list[str] singularityParameters: Parameters to pass to Singularity. Default parameters are `--rm`,
            `--log-driver none`, and the mountpoint `-v work_dir:/data` where /data is the destination convention.
             These defaults are removed if singularity_parmaters is passed, so be sure to pass them if they are desired.
    :param file outfile: Pipe output of Singularity call to file handle
    """
    _singularity(job, tool=tool, parameters=parameters, workDir=workDir, singularityParameters=singularityParameters, outfile=outfile, checkOutput=False)


def singularityCheckOutput(job, tool, parameters=None, workDir=None, singularityParameters=None):
    """
    Returns the stdout from the Singularity invocation (via subprocess.check_output)
    Throws CalledProcessorError if the Singularity invocation returns a non-zero exit code
    This function blocks until the subprocess call to Singularity returns
    :param toil.Job.job job: The Job instance for the calling function.
    :param str tool: Name of the Docker image to be used (e.g. quay.io/ucsc_cgl/samtools:latest).
    :param list[str] parameters: Command line arguments to be passed to the tool.
           If list of lists: list[list[str]], then treat as successive commands chained with pipe.
    :param str workDir: Directory to mount into the container via `-v`. Destination convention is /data
    :param list[str] singularityParameters: Parameters to pass to Singularity. Default parameters are `--rm`,
            `--log-driver none`, and the mountpoint `-v work_dir:/data` where /data is the destination convention.
             These defaults are removed if singularity_parmaters is passed, so be sure to pass them if they are desired.
    :returns: Stdout from the singularity call
    :rtype: str
    """
    return _singularity(job, tool=tool, parameters=parameters, workDir=workDir, singularityParameters=singularityParameters, checkOutput=True)


def _singularity(job, tool, parameters=None, workDir=None, singularityParameters=None, outfile=None, checkOutput=False):
    """
    :param toil.Job.job job: The Job instance for the calling function.
    :param str tool: Name of the Docker image to be used (e.g. quay.io/ucsc_cgl/samtools).
    :param list[str] parameters: Command line arguments to be passed to the tool.
           If list of lists: list[list[str]], then treat as successive commands chained with pipe.
    :param str workDir: Directory to mount into the container via `--bind`. Destination convention is /data
    :param list[str] singularityrParameters: Parameters to pass to Singularity. Default parameters are the mountpoint
             `--bind work_dir:/data` where /data is the destination convention.
             These defaults are removed if singularity_parmaters is passed, so be sure to pass them if they are desired.
    :param file outfile: Pipe output of Singularity call to file handle
    :param bool checkOutput: When True, this function returns singularity's output.
    """
    if parameters is None:
        parameters = []
    if workDir is None:
        workDir = os.getcwd()
    baseSingularityCall = [
     'singularity', '-q', 'exec']
    if singularityParameters:
        baseSingularityCall += singularityParameters
    else:
        baseSingularityCall += ['-H', ('{}:{}').format(os.path.abspath(workDir), os.environ.get('HOME')), '--pwd', os.environ.get('HOME')]
    if len(parameters) > 0 and type(parameters[0]) is list:
        chain_params = [ (' ').join(p) for p in [ map(pipes.quote, q) for q in parameters ] ]
        call = baseSingularityCall + [('docker://{}').format(tool), '/bin/bash', '-c',
         ('set -eo pipefail && {}').format((' | ').join(chain_params))]
    else:
        call = baseSingularityCall + [('docker://{}').format(tool)] + parameters
    _logger.info('Calling singularity with ' + repr(call))
    params = {}
    if outfile:
        params['stdout'] = outfile
    if checkOutput:
        callMethod = subprocess.check_output
    else:
        callMethod = subprocess.check_call
    out = callMethod(call, **params)
    return out