# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sampedro/Documents/Dev/oide-project/dev-env/local/lib/python2.7/site-packages/oide_slurm_assist-0.0.dev1-py2.7.egg/oideslurm/mixins/slurm_mixin.py
# Compiled at: 2015-11-16 17:49:37
import tornado.web, subprocess

class SlurmCmdMixin(tornado.web.RequestHandler):

    def run_sacct(self, **kwargs):
        output = []
        options = [
         '-P', '--format=JobId,Start,End,State,AllocCPUS,QOS,NodeList,TotalCPU,CPUTime,NNodes']
        cmd = [
         'sacct'] + options
        cmd_out = subprocess.check_output(cmd).split('\n')[:-1]
        field_names = cmd_out[0].split('|')
        for row in cmd_out[1:]:
            job = {}
            row = row.split('|')
            job['JobID'] = row[0][1:]
            for i in range(1, len(field_names)):
                job[field_names[i]] = row[i]

            output.append(job)

        return output

    def job_submit(self, **kwargs):
        file_path = kwargs['filepath']
        cmd = [
         'sbatch'] + [file_path]
        try:
            cmd_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return (0, cmd_out)
        except subprocess.CalledProcessError as e:
            return (
             e.returncode, e.output)