# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/bdgenomics/workflows/benchmarking/single_node/sort.py
# Compiled at: 2017-09-18 01:42:06
import argparse, logging, os
from toil.job import Job
from bdgenomics.workflows.tools.preprocessing import run_picard_sort, run_samtools_sort, run_sambamba_sort
from bdgenomics.workflows.tools.spark_tools import call_adam
from toil_lib.urls import download_url_job
_log = logging.getLogger(__name__)

def run_adam_sort(job, sampleId):
    work_dir = job.fileStore.getLocalTempDir()
    job.fileStore.readGlobalFile(sampleId, os.path.join(work_dir, 'reads.bam'))
    add_docker_parameters = [
     '-v',
     ('{}:/data').format(work_dir)]
    _log.info('Converting BAM to ADAM format.')
    call_adam(job, None, [
     'transform',
     '/data/reads.bam',
     '/data/reads.adam'], memory=str(job.memory), run_local=True, container='fnothaft/adam', add_docker_parameters=add_docker_parameters)
    _log.info('Sorting reads using ADAM.')
    call_adam(job, None, [
     'transform',
     '/data/reads.adam',
     '/data/reads.sorted.adam',
     '-sort_reads',
     '-limit_projection'], memory=str(job.memory), run_local=True, container='fnothaft/adam', add_docker_parameters=add_docker_parameters)
    return


def benchmark_sorters(job, sample):
    _log.info('Downloading reads')
    reads_id = download_url_job(job, sample)
    _log.info('Sorting reads with picard.')
    picard_sorted_bam = run_picard_sort(job, reads_id)
    _log.info('Sorting reads with samtools.')
    samtools_sorted_bam = run_samtools_sort(job, reads_id)
    _log.info('Sorting reads with sambamba.')
    sambamba_sorted_bam = run_sambamba_sort(job, reads_id)
    run_adam_sort(job, reads_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample', help='The S3 URL or local path to the input SAM or BAM file.')
    Job.Runner.addToilOptions(parser)
    args = parser.parse_args()
    Job.Runner.startToil(Job.wrapJobFn(benchmark_sorters, args.sample), args)


if __name__ == '__main__':
    main()