# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: abtools/utils/progbar.py
# Compiled at: 2016-04-25 17:07:29
from __future__ import print_function
import sys
from datetime import datetime

def progress_bar(finished, total, start_time=None):
    """
    Prints an ASCII progress bar.

    Each call to ``progress_bar`` will update the progress bar. An example
    of tracking the progress of a list of items would look like::

        job_list = [job1, job2, job3, ... jobN]
        total_jobs = len(job_list)

        #initialize the progress bar
        progress_bar(0, total_jobs)

        # do the jobs
        for i, job in enumerate(job_list):
            do_job(job)
            progress_bar(i + 1, total_jobs)

    Args:

        finished (int): Number of finished jobs.

        total (int): Total number of jobs.

        start_time (datetime): Start time, as a ``datetime.datetime`` object.
            Only required if you want to display execution time alongside
            the progress bar. If not provided, execution time is not shown.

    """
    pct = int(100.0 * finished / total)
    ticks = pct / 2
    spaces = 50 - ticks
    if start_time is not None:
        elapsed = (datetime.now() - start_time).seconds
        minutes = elapsed / 60
        seconds = elapsed % 60
        minute_str = '0' * (2 - len(str(minutes))) + str(minutes)
        second_str = '0' * (2 - len(str(seconds))) + str(seconds)
        prog_bar = ('\r({}/{}) |{}{}|  {}% ({}:{})').format(finished, total, '|' * ticks, ' ' * spaces, pct, minute_str, second_str)
    else:
        prog_bar = ('\r({}/{}) |{}{}|  {}%  ').format(finished, total, '|' * ticks, ' ' * spaces, pct)
    sys.stdout.write(prog_bar)
    sys.stdout.flush()
    return