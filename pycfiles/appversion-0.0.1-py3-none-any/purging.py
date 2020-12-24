# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/App/Validation/Automation/purging.py
# Compiled at: 2012-05-03 04:57:17
import os, glob, time, string, logging

class Purging:
    """ Deletes old log files as per retention policy.The retention period 
        is a part of the configuration file.
    """
    __module__ = __name__

    def __init__(self):
        self.config = {}
        self.data = {}

    def purge(self, log_dir, log_ret_period, log_extn='log'):
        """ Delete log files older than retention days

            >>> auto_obj = Purging()
            >>> auto_obj.purge('/tmp', 10000000000000, 'TRASH')
            True
        """
        logger = logging.getLogger(__name__)

        def older(log_file):
            return time.time() - os.path.getmtime(log_file) > log_ret_period

        try:
            os.chdir(log_dir)
            pattern = './*.' + log_extn
            log_files_purge = filter(older, glob.glob(pattern))
            if log_files_purge:
                msg = 'Log files in log_dir older than log_ret_period days:\n'
                msg += string.join(log_files_purge, '\n')
                for file in log_files_purge:
                    os.unlink(file)

                self.data['PURGE_MSG'] = msg
        except OSError, err:
            logger.error('Log File deletion Failed :ERROR:' + str(err) + '\n')
            self.data['PURGE_MSG'] = str(err)
            return False
        except IOError, err:
            logger.error('Log File deletion Failed :ERROR:' + str(err) + '\n')
            self.data['PURGE_MSG'] = str(err)
            return False

        return True


if __name__ == '__main__':
    import doctest
    doctest.testmod()