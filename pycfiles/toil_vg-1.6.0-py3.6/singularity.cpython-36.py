# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/singularity.py
# Compiled at: 2020-04-30 13:47:21
# Size of source mod 2**32: 12432 bytes
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
import base64, hashlib, logging, subprocess, pipes, os, shutil, sys, tempfile, time
from toil.lib.misc import mkdir_p
logger = logging.getLogger(__name__)
if sys.version_info[0] < 3:
    FileExistsError = OSError

def is_containerized():
    """
    Return True if we think we are already running in a Docker/Kubernetes
    container (where Singularity is unlikely to work without user-mode
    namespaces), and False otherwsie.
    """
    if not os.path.exists('/proc/self/cgroup'):
        return False
    else:
        with open('/proc/self/cgroup') as (fh):
            for line in fh:
                line = line.lower()
                if 'docker' in line or 'kube' in line:
                    return True

        return False


def singularityCall(job, tool, parameters=None, workDir=None, singularityParameters=None, outfile=None):
    """
    Throws CalledProcessorError if the Singularity invocation returns a non-zero exit code
    This function blocks until the subprocess call to Singularity returns
    :param toil.Job.job job: The Job instance for the calling function.
    :param str tool: Name of the Docker image to be used (e.g. quay.io/ucsc_cgl/samtools:latest).
    :param list[str] parameters: Command line arguments to be passed to the tool.
           If list of lists: list[list[str]], then treat as successive commands chained with pipe.
    :param str workDir: Directory to mount into the container via `-v`.
           Destination convention is /mnti, which almost certainly exists in the
           container.
    :param list[str] singularityParameters: Parameters to pass to Singularity.
           Overrides defaults which mount the workDir and configure user mode and
           writability.
    :param file outfile: Pipe output of Singularity call to file handle
    """
    return _singularity(job, tool=tool, parameters=parameters, workDir=workDir, singularityParameters=singularityParameters, outfile=outfile,
      checkOutput=False)


def singularityCheckOutput(job, tool, parameters=None, workDir=None, singularityParameters=None):
    """
    Returns the stdout from the Singularity invocation (via subprocess.check_output)
    Throws CalledProcessorError if the Singularity invocation returns a non-zero exit code
    This function blocks until the subprocess call to Singularity returns
    :param toil.Job.job job: The Job instance for the calling function.
    :param str tool: Name of the Docker image to be used (e.g. quay.io/ucsc_cgl/samtools:latest).
    :param list[str] parameters: Command line arguments to be passed to the tool.
           If list of lists: list[list[str]], then treat as successive commands chained with pipe.
    :param str workDir: Directory to mount into the container via `-v`.
           Destination convention is /mnti, which almost certainly exists in the
           container.
    :param list[str] singularityParameters: Parameters to pass to Singularity.
           Overrides defaults which mount the workDir and configure user mode and
           writability.
    :returns: Stdout from the singularity call
    :rtype: str
    """
    return _singularity(job, tool=tool, parameters=parameters, workDir=workDir, singularityParameters=singularityParameters,
      checkOutput=True)


def _singularity(job, tool, parameters=None, workDir=None, singularityParameters=None, outfile=None, checkOutput=False):
    """
    :param toil.Job.job job: The Job instance for the calling function.
    :param str tool: Name of the Docker image to be used (e.g. quay.io/ucsc_cgl/samtools).
    :param list[str] parameters: Command line arguments to be passed to the tool.
           If list of lists: list[list[str]], then treat as successive commands chained with pipe.
    :param str workDir: Directory to mount into the container via `-v`.
           Destination convention is /mnti, which almost certainly exists in the
           container.
    :param list[str] singularityParameters: Parameters to pass to Singularity.
           Overrides defaults which mount the workDir and configure user mode and
           writability.
    :param file outfile: Pipe output of Singularity call to file handle
    :param bool checkOutput: When True, this function returns singularity's output.
    """
    if parameters is None:
        parameters = []
    else:
        if workDir is None:
            workDir = os.getcwd()
        else:
            baseSingularityCall = [
             'singularity', 'exec']
            if singularityParameters:
                baseSingularityCall += singularityParameters
            else:
                baseSingularityCall.append('-w')
                if is_containerized():
                    baseSingularityCall.append('-u')
                baseSingularityCall += ['-B', '{}:{}'.format(os.path.abspath(workDir), '/mnt'), '--pwd', '/mnt']
            cache_dir = os.path.join(os.environ.get('SINGULARITY_CACHEDIR', os.path.join(os.environ.get('HOME'), '.singularity')), 'toil')
            mkdir_p(cache_dir)
            source_image = _convertImageSpec(tool)
            sandbox_dirname = os.path.join(cache_dir, '{}.sandbox'.format(hashlib.sha256(source_image.encode()).hexdigest()))
            if not os.path.exists(sandbox_dirname):
                temp_sandbox_dirname = tempfile.mkdtemp(dir=cache_dir)
                download_env = os.environ.copy()
                download_env['SINGULARITY_CACHEDIR'] = job.fileStore.getLocalTempDir()
                subprocess.check_call(['singularity', 'build', '-s', '-F', temp_sandbox_dirname, source_image], env=download_env)
                shutil.rmtree(download_env['SINGULARITY_CACHEDIR'])
                try:
                    os.rename(temp_sandbox_dirname, sandbox_dirname)
                except FileExistsError:
                    assert os.path.exists(sandbox_dirname)
                    shutil.rmtree(temp_sandbox_dirname)

            download_env = os.environ.copy()
            if 'rocker/tidyverse' not in tool:
                download_env['TMPDIR'] = '.'
            elif len(parameters) > 0 and type(parameters[0]) is list:
                chain_params = [' '.join(p) for p in [list(map(pipes.quote, q)) for q in parameters]]
                call = baseSingularityCall + [sandbox_dirname, '/bin/bash', '-c',
                 'set -eo pipefail && {}'.format(' | '.join(chain_params))]
            else:
                call = baseSingularityCall + [sandbox_dirname] + parameters
            logger.info('Calling singularity with ' + repr(call))
            params = {}
            params['env'] = download_env
            if outfile:
                params['stdout'] = outfile
        if checkOutput:
            callMethod = subprocess.check_output
        else:
            callMethod = subprocess.check_call
    out = callMethod(call, **params)
    time.sleep(0.5)
    return out


def _convertImageSpec(spec):
    """
    Given an image specifier that may be either a Docker container specifier,
    or a Singularity URL or filename, produce the Singularity URL or filename
    that points to it.
    
    This consists of identifying the Docker container specifiers and prefixing
    them with "docker://".
    """
    if spec.startswith('/'):
        return spec
    else:
        if '://' in spec:
            return spec
        return 'docker://' + spec