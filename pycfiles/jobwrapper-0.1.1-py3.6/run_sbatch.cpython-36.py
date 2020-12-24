# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/run_sbatch.py
# Compiled at: 2018-09-07 06:06:58
# Size of source mod 2**32: 2273 bytes
import subprocess as sbp, time, numpy as np
from .slurm_wrapper import launch_job, return_status, kill_job, exist_job
from .job_watcher import JobState, is_memo_created, last_file_created, get_errfile_notempty
from .mail import sendmail
time_tol = 600

def main():
    jobID = launch_job()
    print('watching ', jobID)
    time.sleep(5)
    State = JobState(jobID)
    State.wait_pending_job()
    if State.is_running():
        print('The job is running !!')
    else:
        print('The job no working... /')
        print('status is:', State.status_string)
        return
        State.wait()
        memo_exist = is_memo_created()
        if memo_exist:
            print('the memo has been dumped, the job seems fine')
        else:
            print("The memo doesn't exist !!")
            kill_job(jobID)
            print('error file is not empty: ', get_errfile_notempty(jobID))
            sbp.call(['cat', jobID + '.err'])
    print(last_file_created())
    send_news(jobID)
    time_last_news = time.time()
    while 1:
        time.sleep(600)
        filename, t = last_file_created()
        ctime = time.time()
        rt = abs(ctime - t)
        print(filename, rt)
        if rt > time_tol:
            print('No file have been created for to much time :')
            print(f"relative time = {rt} s, while tolerence is {time_tol} [s]")
            print('We suspecte a blocking MPI communication or a while True loop')
            kill_job(jobID)
            break
        if ctime - time_last_news > 1800.0:
            time_last_news = ctime
            send_news(jobID)


def send_news(jobID):
    datas = np.loadtxt('temporal_values.dat')
    if datas.ndim == 1:
        data = datas
    else:
        data = datas[-1, :]
    phys_time = data[0]
    ne = data[1]
    ni = data[2]
    Te = sum(data[3:5])
    body = f"Last news from the run:\nPhysical time of the simulation: {phys_time * 1000000.0} mu s\nNumber of Macroparticle: N_e = {ne}, N_i = {ni}\nMean electron temperature: T_e = {Te}\n"
    sendmail(subject=f"News From run {jobID}, t={phys_time * 1000000.0} mus", body=(body.encode('ascii')))


if __name__ == '__main__':
    main()