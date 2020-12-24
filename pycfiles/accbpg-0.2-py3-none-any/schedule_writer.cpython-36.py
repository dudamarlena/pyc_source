# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\accasim\experimentation\schedule_writer.py
# Compiled at: 2018-05-28 14:50:52
# Size of source mod 2**32: 6743 bytes
__doc__ = '\nMIT License\n\nCopyright (c) 2017 cgalleguillosm\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'
from abc import ABC, abstractclassmethod
from accasim.utils.file import file_exists

class WorkloadWriter(ABC):

    def __init__(self, path, overwrite=False, append=False):
        """
        Abstract class used to write workload files.

        :param path: Path to the target file
        :param overwrite: If True, any existing files with the same name will be overwritten
        :param append: If True, the new workload will be appended to a file with the same name, if it exists
        """
        exists = file_exists(path, True)
        if exists:
            if not (overwrite or append):
                raise Exception('File already exists. Overwrite option is False. Set True to overwrite or change the filename/filepath.')
        if overwrite:
            if append:
                raise Exception('Only one mode (append or overwrite) can be True. ')
        mode = None
        if overwrite:
            mode = 'w'
        else:
            if append:
                mode = 'a'
            assert mode, 'File exists and the overwrite and append modes are False'
        self.file = open(path, mode)

    def add_newline(self, job_dict):
        """
        Writes a new line corresponding to a job dictionary given as input

        :param job_dict: The input job dictionary
        """
        line = self.process_dictionary(job_dict)
        if line[(-1)] != '\n':
            line += '\n'
        self.file.write(line)

    @abstractclassmethod
    def process_dictionary(self, job_dict):
        """
        This method must convert the job dictionary to a string formatted in a specific way, according to the implementation

        :param job_dict: Dictionary related to one specific job
        :return: The string corresponding to the input dictionary
        """
        raise NotImplementedError()

    def close_file(self):
        """
        Closes the output file stream
        """
        self.file.close()

    def __del__(self):
        """
        If present, closes the file stream.
        """
        if hasattr(self, 'file'):
            self.close_file()


class DefaultWriter(WorkloadWriter):
    """DefaultWriter"""
    JOB_NUMBER = ('job_number', 0)
    SUBMIT_TIME = ('submit_time', 0)
    WAIT_TIME = ('wait_time', -1)
    DURATION = ('duration', 0)
    ALLOCATED_PROCESSORS = ('allocated_processors', 0)
    AVG_CPU_TIME = ('avg_cpu_time', -1)
    USED_MEMORY = ('used_memory', 0)
    REQUESTED_NUMBER_PROCESSORS = ('requested_number_processors', -1)
    REQUESTED_TIME = ('requested_time', -1)
    REQUESTED_MEMORY = ('requested_memory', -1)
    STATUS = ('status', 1)
    USER_ID = ('user_id', -1)
    GROUP_ID = ('group_id', -1)
    EXECUTABLE_NUMBER = ('executable_number', -1)
    QUEUE_NUMBER = ('queue_number', -1)
    PARTITION_NUMBER = ('partition_number', -1)
    PRECEDING_JOB_NUMBER = ('preceding_job_number', -1)
    THINK_TIME_PREJOB = ('think_time_prejob', -1)
    SWF_ATTRIBUTES = [
     JOB_NUMBER, SUBMIT_TIME, WAIT_TIME, DURATION, ALLOCATED_PROCESSORS,
     AVG_CPU_TIME, USED_MEMORY, REQUESTED_NUMBER_PROCESSORS, REQUESTED_TIME,
     REQUESTED_MEMORY, STATUS, USER_ID, GROUP_ID, EXECUTABLE_NUMBER,
     QUEUE_NUMBER, PARTITION_NUMBER, PRECEDING_JOB_NUMBER, THINK_TIME_PREJOB]

    def __init__(self, path, max_time=14400, overwrite=False, append=False):
        """
        Constructor for the class

        :param path: Path of the target workload file
        :param max_time: Represents a wall-time value for jobs to be used in the workload
        :param overwrite: If True, any existing files with the same name will be overwritten
        :param append: If True, the new workload will be appended to a file with the same name, if it exists
        """
        WorkloadWriter.__init__(self, path, overwrite, append)
        self.max_time = max_time

    def process_dictionary(self, job_dict):
        """
        Converts a job dictionary to a string to be written in the workload.

        :param job_dict: The job dictionary
        :return: A properly formatted SWF string entry
        """
        line = [str(self.prepare_data(job_dict, attr_name, default_value)) for attr_name, default_value in self.SWF_ATTRIBUTES]
        return '\t'.join(line)

    def prepare_data(self, job_dict, attr_name, default_value):
        """
        Method used to prepare specific SWF attributes, by converting entries from the original job dictionary

        :param job_dict: The job dictionary
        :param attr_name: The name of the attribute to be processed
        :param default_value: Default value to be used for the attribute, if not present in job_dict
        :return: The processed value for attr_name, if present, or default_value otherwise
        """
        total_processors = job_dict['resources']['core'] * job_dict['nodes']
        total_mem = job_dict['resources']['mem'] * job_dict['nodes']
        job_dict['requested_number_processors'] = total_processors
        job_dict['allocated_processors'] = total_processors
        job_dict['requested_memory'] = total_mem
        job_dict['used_memory'] = total_mem
        if not job_dict['requested_time']:
            job_dict['requested_time'] = self.max_time
        if attr_name in job_dict:
            return job_dict[attr_name]
        else:
            return default_value