# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/bdgenomics/workflows/benchmarking/single_node/mkdups.py
# Compiled at: 2017-09-18 01:42:06
import argparse, logging, os
from toil.job import Job
from bdgenomics.workflows.tools.preprocessing import picard_mark_duplicates, run_sambamba_markdup, run_sambamba_sort, run_samblaster, run_samtools_index, run_samtools_rmdup, run_samtools_view
from bdgenomics.workflows.tools.spark_tools import call_adam
from toil_lib.urls import download_url_job
_log = logging.getLogger(__name__)

def run_adam_markdups(job, sampleId):
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
    _log.info('Marking duplicate reads using ADAM.')
    call_adam(job, None, [
     'transform',
     '/data/reads.adam',
     '/data/reads.sorted.adam',
     '-mark_duplicate_reads',
     '-limit_projection'], memory=str(job.memory), run_local=True, container='fnothaft/adam', add_docker_parameters=add_docker_parameters)
    return


def benchmark_duplicate_markers(job, sample):
    _log.info('Downloading reads')
    reads_id = download_url_job(job, sample)
    _log.info('Sorting reads by coordinate.')
    coordinate_sorted_bam = run_sambamba_sort(job, reads_id)
    _log.info('Indexing sorted BAM.')
    bam_index = run_samtools_index(job, coordinate_sorted_bam)
    _log.info('Marking duplicates with picard.')
    picard_bam = picard_mark_duplicates(job, coordinate_sorted_bam, bam_index)
    _log.info('Marking duplicates with samtools.')
    samtools_bam = run_samtools_rmdup(job, coordinate_sorted_bam)
    _log.info('Marking duplicates with sambamba.')
    sambamba_bam = run_sambamba_markdup(job, coordinate_sorted_bam)
    run_adam_markdups(job, reads_id)
    _log.info('Sorting reads by name.')
    queryname_sorted_bam = run_sambamba_sort(job, reads_id, sort_by_name=True)
    _log.info('Dumping queryname sorted sam to bam.')
    queryname_sorted_sam = run_samtools_view(job, queryname_sorted_bam)
    _log.info('Marking duplicates with SAMBLASTER.')
    samblaster_sam = run_samblaster(job, queryname_sorted_sam)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample', help='The S3 URL or local path to the input SAM or BAM file.')
    Job.Runner.addToilOptions(parser)
    args = parser.parse_args()
    Job.Runner.startToil(Job.wrapJobFn(benchmark_duplicate_markers, args.sample), args)


if __name__ == '__main__':
    main()