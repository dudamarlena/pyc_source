# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_scripts/transfer_tcga_to_s3/transfer_tcga_to_s3.py
# Compiled at: 2016-10-04 14:54:21
"""
Toil script to move TCGA data into an S3 bucket.

Dependencies
Curl:       apt-get install curl
Docker:     wget -qO- https://get.docker.com/ | sh
Toil:       pip install toil
S3AM:       pip install --pre s3am
"""
import argparse, glob, hashlib, os, shutil, subprocess
from toil.job import Job

def build_parser():
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-g', '--genetorrent', default=None, required=True, help='Path to a file with one analysis ID per line for data hosted on CGHub.')
    parser.add_argument('-k', '--genetorrent_key', default=None, required=True, help='Path to a CGHub key that has access to the TCGA data being requested. An exception willbe thrown if "-g" is set but not this argument.')
    parser.add_argument('--s3_dir', default=None, required=True, help='S3 Bucket. e.g. tcga-data')
    parser.add_argument('--ssec', default=None, required=True, help='Path to Key File for SSE-C Encryption')
    parser.add_argument('--sudo', dest='sudo', default=None, action='store_true', help='Docker usually needs sudo to execute locally, but not when running Mesos or when the user is a member of a Docker group.')
    return parser


def generate_unique_key(master_key_path, url):
    """
    master_key_path: str    Path to the BD2K Master Key (for S3 Encryption)
    url: str                S3 URL (e.g. https://s3-us-west-2.amazonaws.com/bucket/file.txt)

    Returns: str            32-byte unique key generated for that URL
    """
    with open(master_key_path, 'r') as (f):
        master_key = f.read()
    assert len(master_key) == 32, ('Invalid Key! Must be 32 characters. Key: {}, Length: {}').format(master_key, len(master_key))
    new_key = hashlib.sha256(master_key + url).digest()
    assert len(new_key) == 32, ('New key is invalid and is not 32 characters: {}').format(new_key)
    return new_key


def docker_call(work_dir, tool_parameters, tool, java_opts=None, sudo=False, outfile=None):
    """
    Makes subprocess call of a command to a docker container.

    tool_parameters: list   An array of the parameters to be passed to the tool
    tool: str               Name of the Docker image to be used (e.g. quay.io/ucsc_cgl/samtools)
    java_opts: str          Optional commands to pass to a java jar execution. (e.g. '-Xmx15G')
    outfile: file           Filehandle that stderr will be passed to
    sudo: bool              If the user wants the docker command executed as sudo
    """
    base_docker_call = ('docker run --log-driver=none --rm -v {}:/data').format(work_dir).split()
    if sudo:
        base_docker_call = [
         'sudo'] + base_docker_call
    if java_opts:
        base_docker_call = base_docker_call + ['-e', ('JAVA_OPTS={}').format(java_opts)]
    try:
        if outfile:
            subprocess.check_call(base_docker_call + [tool] + tool_parameters, stdout=outfile)
        else:
            subprocess.check_call(base_docker_call + [tool] + tool_parameters)
    except subprocess.CalledProcessError:
        raise RuntimeError('docker command returned a non-zero exit status. Check error logs.')
    except OSError:
        raise RuntimeError('docker not found on system. Install on all nodes.')


def parse_genetorrent(path_to_config):
    """
    Parses genetorrent config file.  Returns list of samples: [ [id1, id1 ], [id2, id2], ... ]
    Returns duplicate of ids to follow UUID/URL standard.
    """
    samples = []
    with open(path_to_config, 'r') as (f):
        for line in f.readlines():
            if not line.isspace():
                samples.append(line.strip())

    return samples


def start_batch(job, input_args):
    """
    This function will administer 5 jobs at a time then recursively call itself until subset is empty
    """
    samples = parse_genetorrent(input_args['genetorrent'])
    job.addChildJobFn(download_and_transfer_sample, input_args, samples, cores=1, disk='30G')


def download_and_transfer_sample(job, input_args, samples):
    """
    Downloads a sample from CGHub via GeneTorrent, then uses S3AM to transfer it to S3

    input_args: dict        Dictionary of input arguments
    analysis_id: str        An analysis ID for a sample in CGHub
    """
    if len(samples) > 1:
        a = samples[len(samples) / 2:]
        b = samples[:len(samples) / 2]
        job.addChildJobFn(download_and_transfer_sample, input_args, a, disk='30G')
        job.addChildJobFn(download_and_transfer_sample, input_args, b, disk='30G')
    else:
        analysis_id = samples[0]
        work_dir = job.fileStore.getLocalTempDir()
        folder_path = os.path.join(work_dir, os.path.basename(analysis_id))
        sudo = input_args['sudo']
        shutil.copy(input_args['genetorrent_key'], os.path.join(work_dir, 'cghub.key'))
        parameters = ['-vv', '-c', 'cghub.key', '-d', analysis_id]
        docker_call(tool='quay.io/ucsc_cgl/genetorrent:3.8.7--9911761265b6f08bc3ef09f53af05f56848d805b', work_dir=work_dir, tool_parameters=parameters, sudo=sudo)
        try:
            sample = glob.glob(os.path.join(folder_path, '*tar*'))[0]
        except KeyError as e:
            print ('No tarfile found inside of folder: ').format(e)
            raise

        key_path = input_args['ssec']
        if sample.endswith('gz'):
            sample_name = analysis_id + '.tar.gz'
            shutil.move(sample, os.path.join(work_dir, sample_name))
        else:
            sample_name = analysis_id + '.tar'
            shutil.move(sample, os.path.join(work_dir, sample_name))
        s3_dir = input_args['s3_dir']
        bucket_name = s3_dir.lstrip('/').split('/')[0]
        base_url = 'https://s3-us-west-2.amazonaws.com/'
        url = os.path.join(base_url, bucket_name, sample_name)
        with open(os.path.join(work_dir, 'temp.key'), 'wb') as (f_out):
            f_out.write(generate_unique_key(key_path, url))
        s3am_command = ['s3am',
         'upload',
         '--sse-key-file', os.path.join(work_dir, 'temp.key'),
         ('file://{}').format(os.path.join(work_dir, sample_name)),
         's3://' + bucket_name + '/']
        subprocess.check_call(s3am_command)


def main():
    """
    This is a Toil pipeline to transfer TCGA data into an S3 Bucket

    Data is pulled down with Genetorrent and transferred to S3 via S3AM.
    """
    parser = build_parser()
    Job.Runner.addToilOptions(parser)
    args = parser.parse_args()
    inputs = {'genetorrent': args.genetorrent, 'genetorrent_key': args.genetorrent_key, 
       'ssec': args.ssec, 
       's3_dir': args.s3_dir, 
       'sudo': args.sudo}
    assert args.ssec and os.path.isfile(args.ssec)
    if args.genetorrent:
        assert os.path.isfile(args.genetorrent)
        assert args.genetorrent_key and os.path.isfile(args.genetorrent_key)
    Job.Runner.startToil(Job.wrapJobFn(start_batch, inputs), args)


if __name__ == '__main__':
    main()