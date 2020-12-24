# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/hpc/provider/slurm/BatchProviderSLURM.py
# Compiled at: 2017-04-23 10:30:41
from future.utils import iteritems
import json
from datetime import datetime
import textwrap
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.TableParser import TableParser
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.cloud.hpc.BatchProviderBase import BatchProviderBase
from cloudmesh_client.db import CloudmeshDatabase
import os
from cloudmesh_client.common.Error import Error

class BatchProviderSLURM(BatchProviderBase):
    cm = CloudmeshDatabase()
    kind = 'slurm'

    @classmethod
    def queue(cls, cluster, format='json', job=None):
        try:
            args = 'squeue '
            if job is not None:
                if job.isdigit():
                    args += (' -j {} ').format(str(job))
                else:
                    args += (' -n {} ').format(job)
            f = '--format=%all'
            args += f
            result = Shell.ssh(cluster, args)
            l = result.splitlines()
            for i, res in enumerate(l):
                if 'ACCOUNT|GRES|' in res:
                    result = ('\n').join(str(x) for x in l[i:])
                    break

            parser = TableParser(strip=True)
            d = parser.to_dict(result)
            for key in list(d.keys()):
                d[key]['cluster'] = cluster
                d[key]['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if format == 'json':
                return json.dumps(d, indent=4, separators=(',', ': '))
            return Printer.write(d, order=[
             'cluster',
             'jobid',
             'partition',
             'name',
             'user',
             'st',
             'time',
             'nodes',
             'nodelist',
             'updated'], output=format)
        except Exception as e:
            Error.traceback(e)
            return e

        return

    @classmethod
    def info(cls, cluster, format='json', all=False):
        if all:
            result = Shell.ssh(cluster, 'sinfo --format="%all"')
        else:
            result = Shell.ssh(cluster, 'sinfo --format="%P|%a|%l|%D|%t|%N"')
        l = result.splitlines()
        for i, res in enumerate(l):
            if 'PARTITION|AVAIL|' in res:
                result = ('\n').join(l[i:])
                break

        parser = TableParser(strip=False)
        d = parser.to_dict(result)
        for key in list(d.keys()):
            d[key]['cluster'] = cluster
            d[key]['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if format == 'json':
            return json.dumps(d, indent=4, separators=(',', ': '))
        else:
            return Printer.write(d, order=[
             'cluster',
             'partition',
             'avail',
             'timelimit',
             'nodes',
             'state',
             'nodelist',
             'updated'], output=format)

    @classmethod
    def test(cls, cluster, time):
        result = Shell.ssh(cluster, ("srun -n1 -t {} echo '#CLOUDMESH: Test ok'").format(time))
        return result

    @classmethod
    def run(cls, cluster, group, cmd, **kwargs):
        config = cls.read_config(cluster)
        if config['credentials']['username'] == 'TBD':
            return ('Please enter username in cloudmesh.yaml for cluster {}').format(cluster)
        else:
            cls.incr()
            data = {'cluster': cluster, 
               'count': cls.counter(), 
               'username': config['credentials']['username'], 
               'remote_experiment_dir': config['default']['experiment_dir'], 
               'queue': config['default']['queue'], 
               'id': None, 
               'nodes': 1, 
               'tasks_per_node': 1}
            data['script_base_name'] = ('{username}-{count}').format(**data)
            data['script_name'] = ('{username}-{count}.sh').format(**data)
            data['script_output'] = ('{username}-{count}.out').format(**data)
            data['script_error'] = ('{username}-{count}.err').format(**data)
            data['remote_experiment_dir'] = ('{remote_experiment_dir}/{count}').format(**data).format(**data)
            data['group'] = group
            option_mapping = {'-t': ('{tasks_per_node}').format(**data), '-N': ('{nodes}').format(**data), 
               '-p': ('{queue}').format(**data), 
               '-o': ('{script_output}').format(**data), 
               '-D': ('{remote_experiment_dir}').format(**data), 
               '-e': ('{script_error}').format(**data)}
            for k, v in iteritems(option_mapping):
                option_mapping[k] = kwargs.get(k) or v

            config = cls.read_config(cluster)
            project = None
            try:
                project = config['credentials']['project']
                if project.lower() not in ('tbd', 'none'):
                    option_mapping['-A'] = project
            except:
                pass

            for key in option_mapping:
                data[key] = option_mapping[key]

            options = ''
            for key, value in option_mapping.items():
                options += ('#SBATCH {} {}\n').format(key, value)

            cls.create_remote_dir(cluster, data['remote_experiment_dir'])
            if os.path.isfile(Config.path_expand(cmd)):
                _from = Config.path_expand(cmd)
                _to = ('{cluster}:{remote_experiment_dir}').format(**data)
                local_file_name = cmd.split('/')[(-1)]
                Shell.execute('rsync', [_from, _to])
                data['command'] = ('{remote_experiment_dir}/{local_file_name}').format(local_file_name=local_file_name, **data)
            else:
                data['command'] = cmd
            data['options'] = options
            script = textwrap.dedent('\n            #! /bin/sh\n            {options}\n\n            echo \'#CLOUDMESH: BATCH ENVIRONMENT\'\n            echo \'BASIL_RESERVATION_ID:\' $BASIL_RESERVATION_ID\n            echo \'SLURM_CPU_BIND:\' $SLURM_CPU_BIND\n            echo \'SLURM_JOB_ID:\' $SLURM_JOB_ID\n            echo \'SLURM_JOB_CPUS_PER_NODE:\' $SLURM_JOB_CPUS_PER_NODE\n            echo \'SLURM_JOB_DEPENDENCY:\' $SLURM_JOB_DEPENDENCY\n            echo \'SLURM_JOB_NAME:\' $SLURM_JOB_NAME\n            echo \'SLURM_JOB_NODELIST:\' $SLURM_JOB_NODELIST\n            echo \'SLURM_JOB_NUM_NODES:\' $SLURM_JOB_NUM_NODES\n            echo \'SLURM_MEM_BIND:\' $SLURM_MEM_BIND\n            echo \'SLURM_TASKS_PER_NODE:\' $SLURM_TASKS_PER_NODE\n            echo \'MPIRUN_NOALLOCATE:\' $MPIRUN_NOALLOCATE\n            echo \'MPIRUN_NOFREE:\' $MPIRUN_NOFREE\n            echo \'SLURM_NTASKS_PER_CORE:\' $SLURM_NTASKS_PER_CORE\n            echo \'SLURM_NTASKS_PER_NODE:\' $SLURM_NTASKS_PER_NODE\n            echo \'SLURM_NTASKS_PER_SOCKET:\' $SLURM_NTASKS_PER_SOCKET\n            echo \'SLURM_RESTART_COUNT:\' $SLURM_RESTART_COUNT\n            echo \'SLURM_SUBMIT_DIR:\' $SLURM_SUBMIT_DIR\n            echo \'MPIRUN_PARTITION:\' $MPIRUN_PARTITION\n            d=$(date)\n            echo "#CLOUDMESH: status, start, $d"\n            srun -l echo "#CLOUDMESH: status, start, $d"\n            srun -l {command}\n            d=$(date)\n            srun -l echo "#CLOUDMESH: status, finished, $d"\n            d=$(date)\n            echo "#CLOUDMESH: status, finished, $d"\n            ').format(**data).replace('\r\n', '\n').strip()
            _from = Config.path_expand(('~/.cloudmesh/{script_name}').format(**data))
            _to = ('{cluster}:{remote_experiment_dir}').format(**data)
            data['from'] = _from
            data['to'] = _to
            data['script'] = script
            with open(_from, 'w') as (local_file):
                local_file.write(script)
            Shell.scp(_from, _to)
            cmd = ('sbatch {remote_experiment_dir}/{script_name}').format(**data)
            data['cmd'] = cmd
            result = Shell.ssh(cluster, cmd)
            data['output'] = result
            for line in result.split('\n'):
                if 'Submitted batch job' in line:
                    data['job_id'] = int(line.replace('Submitted batch job ', '').strip())
                    break

            for key in ['-t', '-N', '-p', '-o', '-D', '-e']:
                if key in data:
                    print (
                     key, data[key])
                    del data[key]

            data['status'] = 'started'
            cls.add_db(**data)
            return data

    @classmethod
    def delete(cls, cluster, job, group=None):
        """
        This method is used to terminate a job with the specified or a group of jobs
        job_id or job_name in a given cluster
        :param group:
        :param cluster: the cluster like comet
        :param job: the job id or name
        :return: success message or error
        """
        try:
            if group is not None:
                arguments = {'cluster': cluster, 'group': group}
                db_jobs = cls.cm.find('batchjob', **arguments)
                list1 = []
                for i in db_jobs:
                    list1.append(db_jobs[i]['job_id'])

                active_jobs = json.loads(cls.queue(cluster))
                list2 = []
                for i in active_jobs:
                    list2.append(active_jobs[i]['jobid'])

                res = set(list1).intersection(set(list2))
                if res is not None:
                    for j in res:
                        cmd = ('scancel {}').format(str(j))
                        Shell.ssh(cluster, cmd)
                        print ('Deleted {}').format(j)

                return ('All jobs for group {} killed successfully').format(group)
            else:
                args = 'scancel '
                if job.isdigit():
                    args += job
                else:
                    args += ('-n {}').format(job)
                Shell.ssh(cluster, args)
                return ('Job {} killed successfully').format(job)

        except Exception as ex:
            print 'in exceptio'
            print ex
            return ex

        return

    @classmethod
    def add_db(cls, **kwargs):
        kwargs['name'] = kwargs.get('script_name')
        db_obj = {0: {'batchjob': kwargs}}
        cls.cm.add_obj(db_obj)
        cls.cm.save()