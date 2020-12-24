# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_scripts/bwa_alignment/bwa_alignment.py
# Compiled at: 2016-10-04 14:54:20
import argparse, multiprocessing, os, sys, textwrap
from urlparse import urlparse
import yaml
from toil.job import Job
from toil_scripts.lib import require, required_length
from toil_scripts.lib.files import copy_file_job
from toil_scripts.lib.jobs import map_job
from toil_scripts.lib.urls import download_url_job, s3am_upload_job
from toil_scripts.rnaseq_cgl.rnaseq_cgl_pipeline import generate_file
from toil_scripts.tools.aligners import run_bwakit
from toil_scripts.tools.indexing import run_samtools_faidx, run_bwa_index

def download_reference_files(job, inputs, samples):
    """
    Downloads shared files that are used by all samples for alignment, or generates them if they were not provided.

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param Namespace inputs: Input arguments (see main)
    :param list[list[str, list[str, str]]] samples: Samples in the format [UUID, [URL1, URL2]]
    """
    shared_ids = {}
    urls = [
     (
      'amb', inputs.amb), ('ann', inputs.ann), ('bwt', inputs.bwt),
     (
      'pac', inputs.pac), ('sa', inputs.sa)]
    if inputs.alt:
        urls.append(('alt', inputs.alt))
    download_ref = job.wrapJobFn(download_url_job, inputs.ref, disk='3G')
    job.addChild(download_ref)
    shared_ids['ref'] = download_ref.rv()
    if inputs.fai:
        shared_ids['fai'] = job.addChildJobFn(download_url_job, inputs.fai).rv()
    else:
        faidx = job.wrapJobFn(run_samtools_faidx, download_ref.rv())
        shared_ids['fai'] = download_ref.addChild(faidx).rv()
    if all(x[1] for x in urls):
        for name, url in urls:
            shared_ids[name] = job.addChildJobFn(download_url_job, url).rv()

    else:
        job.fileStore.logToMaster('BWA index files not provided, creating now')
        bwa_index = job.wrapJobFn(run_bwa_index, download_ref.rv())
        download_ref.addChild(bwa_index)
        for x, name in enumerate(['amb', 'ann', 'bwt', 'pac', 'sa']):
            shared_ids[name] = bwa_index.rv(x)

    job.addFollowOnJobFn(map_job, download_sample_and_align, samples, inputs, shared_ids)


def download_sample_and_align(job, sample, inputs, ids):
    """
    Downloads the sample and runs BWA-kit

    :param JobFunctionWrappingJob job: Passed by Toil automatically
    :param tuple(str, list) sample: UUID and URLS for sample
    :param Namespace inputs: Contains input arguments
    :param dict ids: FileStore IDs for shared inputs
    """
    uuid, urls = sample
    r1_url, r2_url = urls if len(urls) == 2 else (urls[0], None)
    job.fileStore.logToMaster(('Downloaded sample: {0}. R1 {1}\nR2 {2}\nStarting BWA Run').format(uuid, r1_url, r2_url))
    ids['r1'] = job.addChildJobFn(download_url_job, r1_url, s3_key_path=inputs.ssec, disk=inputs.file_size).rv()
    if r2_url:
        ids['r2'] = job.addChildJobFn(download_url_job, r2_url, s3_key_path=inputs.ssec, disk=inputs.file_size).rv()
    else:
        ids['r2'] = None
    inputs.cores = min(inputs.maxCores, multiprocessing.cpu_count())
    inputs.uuid = uuid
    config = dict(**vars(inputs))
    config.update(ids)
    config = argparse.Namespace(**config)
    bam_id = job.wrapJobFn(run_bwakit, config, threads=inputs.cores, sort=inputs.sort, trim=inputs.trim, disk=inputs.file_size, cores=inputs.cores)
    job.addFollowOn(bam_id)
    output_name = uuid + '.bam' + str(inputs.suffix) if inputs.suffix else uuid + '.bam'
    if urlparse(inputs.output_dir).scheme == 's3':
        bam_id.addChildJobFn(s3am_upload_job, file_id=bam_id.rv(), file_name=output_name, s3_dir=inputs.output_dir, num_cores=inputs.cores, s3_key_path=inputs.ssec, cores=inputs.cores, disk=inputs.file_size)
    else:
        bam_id.addChildJobFn(copy_file_job, name=output_name, file_id=bam_id.rv(), output_dir=inputs.output_dir, disk=inputs.file_size)
    return


def generate_config():
    return textwrap.dedent('\n        # BWA Alignment Pipeline configuration file\n        # This configuration file is formatted in YAML. Simply write the value (at least one space) after the colon.\n        # Edit the values in this configuration file and then rerun the pipeline: "toil-bwa run"\n        #\n        # URLs can take the form: http://, file://, s3://, gnos://\n        # Local inputs follow the URL convention: file:///full/path/to/input\n        # S3 URLs follow the convention: s3://bucket/directory/file.txt\n        #\n        # Comments (beginning with #) do not need to be removed. Optional parameters left blank are treated as false.\n        ##############################################################################################################\n        # Required: Reference fasta file\n        ref: s3://cgl-pipeline-inputs/alignment/hg19.fa\n\n        # Required: Output location of sample. Can be full path to a directory or an s3:// URL\n        # Warning: S3 buckets must exist prior to upload or it will fail.\n        output-dir:\n\n        # Required: The library entry to go in the BAM read group.\n        library: Illumina\n\n        # Required: Platform to put in the read group\n        platform: Illumina\n\n        # Required: Program Unit for BAM header. Required for use with GATK.\n        program_unit: 12345\n\n        # Required: Approximate input file size. Provided as a number followed by (base-10) [TGMK]. E.g. 10M, 150G\n        file-size: 50G\n\n        # Optional: If true, sorts bam\n        sort: True\n\n        # Optional. If true, trims adapters\n        trim: false\n\n        # Optional: Reference fasta file (amb) -- if not present will be generated\n        amb: s3://cgl-pipeline-inputs/alignment/hg19.fa.amb\n\n        # Optional: Reference fasta file (ann) -- If not present will be generated\n        ann: s3://cgl-pipeline-inputs/alignment/hg19.fa.ann\n\n        # Optional: Reference fasta file (bwt) -- If not present will be generated\n        bwt: s3://cgl-pipeline-inputs/alignment/hg19.fa.bwt\n\n        # Optional: Reference fasta file (pac) -- If not present will be generated\n        pac: s3://cgl-pipeline-inputs/alignment/hg19.fa.pac\n\n        # Optional: Reference fasta file (sa) -- If not present will be generated\n        sa: s3://cgl-pipeline-inputs/alignment/hg19.fa.sa\n\n        # Optional: Reference fasta file (fai) -- If not present will be generated\n        fai: s3://cgl-pipeline-inputs/alignment/hg19.fa.fai\n\n        # Optional: (string) Path to Key File for SSE-C Encryption\n        ssec:\n\n        # Optional: Use instead of library, program_unit, and platform.\n        rg-line:\n\n        # Optional: Alternate file for reference build (alt). Necessary for alt aware alignment\n        alt:\n\n        # Optional: If true, runs the pipeline in mock mode, generating a fake output bam\n        mock-mode:\n\n        # Optional: Optional suffix to add to sample output\n        suffix:\n    '[1:])


def generate_manifest():
    return textwrap.dedent('\n        #   Edit this manifest to include information for each sample to be run.\n        #   Lines beginning with # are ignored.\n        #\n        #   There are 2 or 3 tab-separated columns: UUID, 1st FASTQ URL, 2nd FASTQ URL (if paired)\n        #   If a sample is paired end: UUID    URL1    URL2\n        #   If a sample is single-ended: UUID    URL\n        #\n        #   UUID            This should be a unique identifier for the sample.\n        #   URL1/URL2       A URL (http://, ftp://, file://, s3://, gnos://) pointing to the sample fastq files.\n        #\n        #   Examples below:\n        #\n        #   Paired_UUID    file:///path/to/R1.fq.gz    file:///path/to/R2.fq.gz\n        #   Unpaired_UUID    file:///path/to/unpaired.fq.gz\n        #\n        #   Place your samples below, one sample per line.\n        '[1:])


def parse_manifest(manifest_path):
    """
    Parse manifest file

    :param str manifest_path: Path to manifest file
    :return: samples
    :rtype: list[str, list]
    """
    samples = []
    with open(manifest_path, 'r') as (f):
        for line in f:
            if not line.isspace() and not line.startswith('#'):
                sample = line.strip().split('\t')
                require(2 <= len(sample) <= 3, ('Bad manifest format! Expected UUID\tURL1\t[URL2] (tab separated), got: {}').format(sample))
                uuid = sample[0]
                urls = sample[1:]
                for url in urls:
                    require(urlparse(url).scheme and urlparse(url), ('Invalid URL passed for {}').format(url))

                samples.append([uuid, urls])

    return samples


def main():
    """
    Computational Genomics Lab, Genomics Institute, UC Santa Cruz
    Toil BWA pipeline

    Alignment of fastq reads via BWA-kit

    General usage:
    1. Type "toil-bwa generate" to create an editable manifest and config in the current working directory.
    2. Parameterize the pipeline by editing the config.
    3. Fill in the manifest with information pertaining to your samples.
    4. Type "toil-bwa run [jobStore]" to execute the pipeline.

    Please read the README.md located in the source directory or at:
    https://github.com/BD2KGenomics/toil-scripts/tree/master/src/toil_scripts/bwa_alignment

    Structure of the BWA pipeline (per sample)

        0 --> 1

    0 = Download sample
    1 = Run BWA-kit
    ===================================================================
    :Dependencies:
    cURL:       apt-get install curl
    Toil:       pip install toil
    Docker:     wget -qO- https://get.docker.com/ | sh

    Optional:
    S3AM:       pip install --s3am (requires ~/.boto config file)
    Boto:       pip install boto
    """
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('generate-config', help='Generates an editable config in the current working directory.')
    subparsers.add_parser('generate-manifest', help='Generates an editable manifest in the current working directory.')
    subparsers.add_parser('generate', help='Generates a config and manifest in the current working directory.')
    parser_run = subparsers.add_parser('run', help='Runs the BWA alignment pipeline')
    group = parser_run.add_mutually_exclusive_group()
    parser_run.add_argument('--config', default='config-toil-bwa.yaml', type=str, help='Path to the (filled in) config file, generated with "generate-config".')
    group.add_argument('--manifest', default='manifest-toil-bwa.tsv', type=str, help='Path to the (filled in) manifest file, generated with "generate-manifest". \nDefault value: "%(default)s".')
    group.add_argument('--sample', nargs='+', action=required_length(2, 3), help='Space delimited sample UUID and fastq files in the format: uuid url1 [url2].')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    Job.Runner.addToilOptions(parser_run)
    args = parser.parse_args()
    cwd = os.getcwd()
    if args.command == 'generate-config' or args.command == 'generate':
        generate_file(os.path.join(cwd, 'config-toil-bwa.yaml'), generate_config)
    if args.command == 'generate-manifest' or args.command == 'generate':
        generate_file(os.path.join(cwd, 'manifest-toil-bwa.tsv'), generate_manifest)
    elif args.command == 'run':
        require(os.path.exists(args.config), ('{} not found. Please run generate-config').format(args.config))
        if not args.sample:
            args.sample = None
            require(os.path.exists(args.manifest), ('{} not found and no sample provided. Please run "generate-manifest"').format(args.manifest))
        parsed_config = {x.replace('-', '_'):y for x, y in yaml.load(open(args.config).read()).iteritems()}
        config = argparse.Namespace(**parsed_config)
        config.maxCores = int(args.maxCores) if args.maxCores else sys.maxint
        samples = [args.sample[0], args.sample[1:]] if args.sample else parse_manifest(args.manifest)
        require(config.ref, ('Missing URL for reference file: {}').format(config.ref))
        require(config.output_dir, ('No output location specified: {}').format(config.output_dir))
        Job.Runner.startToil(Job.wrapJobFn(download_reference_files, config, samples), args)
    return


if __name__ == '__main__':
    main()