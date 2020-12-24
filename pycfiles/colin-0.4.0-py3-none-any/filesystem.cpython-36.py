# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/colin/core/checks/filesystem.py
# Compiled at: 2018-06-08 08:01:48
# Size of source mod 2**32: 5078 bytes
import logging
from conu import DockerRunBuilder
from conu.exceptions import ConuException
from colin.core.target import TargetType
from ..exceptions import ColinException
from ..result import CheckResult
from .containers import ContainerAbstractCheck
from .images import ImageAbstractCheck
logger = logging.getLogger(__name__)

class FileCheck(ContainerAbstractCheck, ImageAbstractCheck):
    __doc__ = ' Check presence of files; w/o mounting the whole FS '

    def __init__(self, message, description, reference_url, tags, files, all_must_be_present):
        super(FileCheck, self).__init__(message, description, reference_url, tags)
        self.files = files
        self.all_must_be_present = all_must_be_present

    def check(self, target):
        passed = self.all_must_be_present
        cleanup = False
        if target.target_type is TargetType.IMAGE:
            drb = DockerRunBuilder(command=['/bin/sleep', 'infinity'], additional_opts=[
             '--entrypoint='])
            cont = target.instance.run_via_binary(run_command_instance=drb)
            cleanup = True
        else:
            if target.target_type is TargetType.CONTAINER:
                cont = target.instance
            else:
                return CheckResult(ok=False, description=(self.description),
                  message=(self.message),
                  reference_url=(self.reference_url),
                  check_name=(self.name),
                  logs=[
                 'Unsupported target, this check can process only containers and images'])
        logs = []
        try:
            for f in self.files:
                cmd = [
                 '/bin/ls', '-1', f]
                try:
                    f_present = cont.execute(cmd)
                    logs.append("File '{}' is {}present.".format(f, '' if f_present else 'not '))
                except ConuException as ex:
                    logger.info('File %s is not present, ex: %s', f, ex)
                    f_present = False
                    logs.append('File {} is not present.'.format(f))

                if self.all_must_be_present:
                    passed = f_present and passed
                else:
                    passed = f_present or passed

            return CheckResult(ok=passed, description=(self.description),
              message=(self.message),
              reference_url=(self.reference_url),
              check_name=(self.name),
              logs=logs)
        finally:
            if cleanup:
                cont.stop()
                cont.delete()


class FileSystemCheck(ContainerAbstractCheck, ImageAbstractCheck):

    def __init__(self, message, description, reference_url, tags, files, all_must_be_present):
        super(FileSystemCheck, self).__init__(message, description, reference_url, tags)
        self.files = files
        self.all_must_be_present = all_must_be_present

    def check(self, target):
        try:
            with target.instance.mount() as (fs):
                passed = self.all_must_be_present
                logs = []
                for f in self.files:
                    try:
                        f_present = fs.file_is_present(f)
                        logs.append("File '{}' is {}present.".format(f, '' if f_present else 'not '))
                    except IOError as ex:
                        f_present = False
                        logs.append('Error: {}'.format(str(ex)))

                    if self.all_must_be_present:
                        passed = f_present and passed
                    else:
                        passed = f_present or passed

                return CheckResult(ok=passed, description=(self.description),
                  message=(self.message),
                  reference_url=(self.reference_url),
                  check_name=(self.name),
                  logs=logs)
        except Exception as ex:
            raise ColinException('There was an error while operating on filesystem of {}: {}'.format(target.instance, str(ex)))