# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/podchecker/exector.py
# Compiled at: 2019-12-04 04:07:27
# Size of source mod 2**32: 14405 bytes
"""
    USAGE

        python3 <script_name>.py --src_path=<src_path> --dst_path=<dst_path> --log_path=<log_path> [--sortedbyname] [--displayfully] [--help]

    SUPPORT FUNCTIONS

        1. support compare files as below
            ------------------------------------------------------------
              Platform      SRC_FILE                DST_FILE
            ------------------------------------------------------------
              iOS           podfile                    podfile
              iOS           podfile                    podfile.lock
              iOS           podfile.lock            podfile
              iOS           podfile.lock            podfile.lock
              Android       version.properties      version.properties
            ------------------------------------------------------------
              TODO:
              Compounded    pods.cfg                pods.cfg
            ------------------------------------------------------------

        2. group output
            - compare rslts: src & dst (equal)
            - compare rslts: src & dst (unequal)
            - compare rslts: src - dst (dst None)
            - compare rslts: dst - src (src None)

        3. file log

    SUPPORT OPTIONS

        -s, --src_path
            [Required] src file path (local url or remote url is FINE)

        -d, --dst_path
            [Required] dst file path (local url or remote url is FINE)

        -l, --log_path
            [Optional] Log File Path

        -t, --sortedbyname
            [Optional] Sort by comparison (default), or sort by name if specified

        -f, --displayfully
            [Optional] Display unequal rows only (default), or display all if specified

        -h, --help
            [Optional] Show this USAGE and exit.

    MORE

        requires python3

        requires valid file path (case insensitive):
            xxx/**/podfile
            xxx/**/podfile.lock
            xxx/**/version.properties
"""
import os, sys, getopt, requests, re, subprocess
from enum import Enum, unique
sys.path.append(os.path.abspath(os.path.curdir))
from .utils import *
from humanfriendly.terminal import usage, warning

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 's:d:l:tfh', ['src_path=', 'dst_path=', 'log_path=', 'sortedbyname', 'displayfullyhelp'])
    except getopt.GetoptError:
        warning(__doc__)
        sys.exit(2)

    GlobalVars.sort_type = 0
    for opt, arg in opts:
        if opt in {'-s', '--src_path'}:
            GlobalVars.src_path = arg
        elif opt in {'--dst_path', '-d'}:
            GlobalVars.dst_path = arg
        elif opt in {'--log_path', '-l'}:
            GlobalVars.log_path = arg
        elif opt in {'-t', '--sortedbyname'}:
            GlobalVars.sortedbyname = True
        else:
            if opt in {'--displayfully', '-f'}:
                GlobalVars.displayfully = True

    do_check()


class GlobalVars(object):
    src_path = ''
    dst_path = ''
    log_path = ''
    sortedbyname = False
    displayfully = False


def do_check():
    LoggerAdapter.setfilepath(GlobalVars.log_path)
    LoggerAdapter.logblue(f"\n-> begin {os.path.basename(__file__)}")
    LoggerAdapter.logblue('-> extracting files...')
    src_fileinfo, dst_fileinfo = FileInfo(GlobalVars.src_path), FileInfo(GlobalVars.dst_path)
    if src_fileinfo.location is FileLocation.invalid or dst_fileinfo.location is FileLocation.invalid:
        LoggerAdapter.logred('[!] error: src_path or dst_path is unreachable!')
        return
    elif not src_fileinfo.filetype is FileType.invalid:
        if dst_fileinfo.filetype is FileType.invalid:
            LoggerAdapter.logred('[!] error: src_path or dst_path has invalid file type! (podfile|')
            return
        src_extractor = PodExtractorFactory.extractor(src_fileinfo).run()
        dst_extractor = PodExtractorFactory.extractor(dst_fileinfo).run()
        src_extractor and dst_extractor or LoggerAdapter.logred('[!] error: src or dst extractor failed!')
        return
        a, b, c, d = PodComparer().compare(src_extractor, dst_extractor)
        LoggerAdapter.logblue('\n-> saying rslts...')
        if GlobalVars.displayfully:
            say_content = f"不同库:{b}个, 相同库:{a}个, 源-目标差集库:{c}个, 目标-源差集库:{d}个, 共计:{a + b + c + d}个 依赖库. \\(仅供参考\\)"
    else:
        say_content = f"不同库:{b}个, 相同库:{a}个, 共计:{a + b}个 依赖库. \\(仅供参考\\)"
    LoggerAdapter.logblue(f"\n-> {say_content}")
    subprocess.call(f"say {say_content}", shell=True)
    LoggerAdapter.logblue(f"\n-> end {os.path.basename(__file__)}\n")


class LoggerAdapter(object):
    logger = None
    logger: logging.Logger

    @classmethod
    def setfilepath(cls, fp):
        cls.logger = LoggerBuilder.build('podchecker', (logging.DEBUG), msgOnly=True).addFile(fp).logger()

    @classmethod
    def filelog(cls, log):
        if cls.logger:
            cls.logger.info(log)

    @classmethod
    def logblue(cls, log):
        PrintWithColor.blue(log)
        cls.filelog(log)

    @classmethod
    def loggreen(cls, log):
        PrintWithColor.green(log)
        cls.filelog(log)

    @classmethod
    def logred(cls, log):
        PrintWithColor.red(log)
        cls.logger.info(log)

    @classmethod
    def logyellow(cls, log):
        PrintWithColor.yellow(log)
        cls.logger.info(log)

    @classmethod
    def logcyan(cls, log):
        PrintWithColor.cyan(log)
        cls.logger.info(log)


@unique
class FileLocation(Enum):
    invalid = 0
    disk = 1
    remote = 2


@unique
class FileType(Enum):
    invalid = 'invalid'
    podfile = 'podfile'
    podfilelock = 'podfile.lock'
    properties = 'version.properties'
    config = '.cfg'


class FileInfo(object):
    filepath = ''
    filepath: str
    location = FileLocation.invalid
    location: FileLocation
    filetype = FileType.invalid
    filetype: FileType

    def __init__(self, filepath):
        self.filepath = filepath
        self.location = self._verify_location(filepath)
        self.filetype = self._verify_filetype(filepath)

    def _verify_location(self, fp):
        if os.path.isfile(fp):
            return FileLocation.disk
        if fp.startswith('http'):
            return FileLocation.remote
        return FileLocation.invalid

    def _verify_filetype(self, fp):
        if re.compile('podfile\\.lock$', re.IGNORECASE).search(fp):
            return FileType.podfilelock
        if re.compile('podfile$', re.IGNORECASE).search(fp):
            return FileType.podfile
        if re.compile('version\\.properties$', re.IGNORECASE).search(fp):
            return FileType.properties
        if re.compile('\\.cfg$', re.IGNORECASE).search(fp):
            return FileType.config
        return FileType.invalid


class Pod(object):
    name = ''
    version = ''

    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __eq__(self, other):
        a = self.__class__ == other.__class__
        b = self.name == other.name
        c = self.version == other.version
        return a and b and c

    def __ne__(self, other):
        return not self == other


class PodExtractor(object):
    fileInfo: FileInfo
    pods = []
    pods: list

    def __init__(self, fileInfo):
        self.fileInfo = fileInfo
        self.pods = []

    def _get_all_content(self):
        f_text = ''
        if self.fileInfo.location is FileLocation.disk:
            LoggerAdapter.logblue(f"-> reading file content: {self.fileInfo.filepath}")
            with open((self.fileInfo.filepath), encoding='utf-8') as (f):
                f_text = f.read()
        else:
            if self.fileInfo.location is FileLocation.remote:
                LoggerAdapter.logblue(f"-> requesting file content: {self.fileInfo.filepath}")
                r = requests.get(self.fileInfo.filepath)
                f_text = r.text
        return f_text

    def extract(self, pattern):
        f_text = self._get_all_content()
        ai = re.compile(pattern).findall(f_text)
        if ai is not None:
            pod_dict = {t[0]:t[1] for t in ai}
            for k, v in pod_dict.items():
                tmp_pod = Pod(k, v)
                if tmp_pod not in self.pods:
                    self.pods.append(tmp_pod)

    def run(self):
        self.extract()
        return self


class IOSPodfileExtractor(PodExtractor):

    def extract(self):
        super().extract("pod[\\s]+\\'(.+?)\\'[\\s]*,[\\s]*\\'(.+?)\\'")


class IOSPodfileLockExtractor(PodExtractor):

    def extract(self):
        super().extract('-[\\s]*(.+?)[\\s]*\\([=~>\\s]*(.+?)\\)')


class AndroidPropertiesExtractor(PodExtractor):

    def extract(self):
        super().extract('(.+?)=(.+)')


class ConfigExtractor(PodExtractor):

    def extract(self):
        pass


class PodExtractorFactory(object):

    @classmethod
    def extractor(cls, fileinfo) -> PodExtractor:
        if fileinfo.filetype is FileType.podfile:
            return IOSPodfileExtractor(fileinfo)
        if fileinfo.filetype is FileType.podfilelock:
            return IOSPodfileLockExtractor(fileinfo)
        if fileinfo.filetype is FileType.properties:
            return AndroidPropertiesExtractor(fileinfo)
        if fileinfo.filetype is FileType.config:
            return ConfigExtractor(fileinfo)
        return


class PodComparer(object):

    def compare(self, src_extractor, dst_extractor):
        LoggerAdapter.logblue('-> comparing...')
        src_pods = src_extractor.pods
        dst_pods = dst_extractor.pods
        src_pods_dict = {pod.name:pod for pod in src_pods}
        dst_pods_dict = {pod.name:pod for pod in dst_pods}

        class PodComparePair(object):
            name: str
            srcPod: Pod
            dstPod: Pod
            cmpRslt: VersionCompareResult
            cmpRsltValue: str

            def __init__(self, name, srcPod, dstPod):
                self.name = name
                self.srcPod = srcPod
                self.dstPod = dstPod
                if srcPod:
                    if not dstPod:
                        self.cmpRslt = None
                        self.cmpRsltValue = 'src-none' if not srcPod else 'dst-none'
                else:
                    self.cmpRslt = VersionComparer().compare(srcPod.version, dstPod.version)
                    self.cmpRsltValue = self.cmpRslt.value

        def print_pairs(pairs, header_desc):

            def _print_format(arg1, arg2, arg3, arg4, arg4Color=0):
                if arg4Color == 1:
                    arg4 = PrintWithColor.simple_preferred_formatted_string(kFore.GREEN, arg4)
                else:
                    if arg4Color == 2:
                        arg4 = PrintWithColor.simple_preferred_formatted_string(kFore.RED, arg4)
                return f"{arg1:<60s} {arg2:<40s} {arg3:<40s} {arg4:<10s}"

            LoggerAdapter.logcyan('\n' + header_desc + '\n')
            LoggerAdapter.logyellow(_print_format(f"pod_name({len(pairs)})", 'src_version', 'dst_version', 'comparison'))
            LoggerAdapter.logyellow(_print_format('-----------------------', '-----------', '-----------', '----------'))
            if GlobalVars.sortedbyname:
                sort = sorted(pairs, key=(lambda x: x.name))
            else:
                sort = sorted(pairs, key=(lambda x: x.cmpRsltValue), reverse=True)
            for pair in sort:
                name = pair.name
                src = pair.srcPod.version if pair.srcPod else 'None'
                dst = pair.dstPod.version if pair.dstPod else 'None'
                compare = pair.cmpRsltValue
                color = 0
                if pair.cmpRslt is not None:
                    if pair.cmpRslt.isUpper():
                        color = 1
                    elif pair.cmpRslt.isLower():
                        color = 2
                else:
                    color = 2
                PrintWithColor.yellow(_print_format(name, src, dst, compare, color))
                LoggerAdapter.filelog(_print_format(name, src, dst, compare, 0))

            LoggerAdapter.logyellow(_print_format('-----------------------', '-----------', '-----------', '----------'))

        intersection_keys = set(src_pods_dict.keys()) & set(dst_pods_dict.keys())
        intersection_pairs = [PodComparePair(k, src_pods_dict[k], dst_pods_dict[k]) for k in intersection_keys]
        intersection_unequal_pairs = [x for x in intersection_pairs if x.srcPod != x.dstPod]
        print_pairs(intersection_unequal_pairs, '--> begin to compare (src & dst) : unequal')
        intersection_equal_pairs = [x for x in intersection_pairs if x.srcPod == x.dstPod]
        print_pairs(intersection_equal_pairs, '--> begin to compare (src & dst) : equal')
        if GlobalVars.displayfully:
            src2dst_keys = set(src_pods_dict.keys()) - set(dst_pods_dict.keys())
            src2dst_pairs = [PodComparePair(k, src_pods_dict[k], None) for k in src2dst_keys]
            print_pairs(src2dst_pairs, '--> begin to compare (src - dst)')
        else:
            src2dst_pairs = []
        if GlobalVars.displayfully:
            dst2src_keys = set(dst_pods_dict.keys()) - set(src_pods_dict.keys())
            dst2src_pairs = [PodComparePair(k, None, dst_pods_dict[k]) for k in dst2src_keys]
            print_pairs(dst2src_pairs, '--> begin to compare (dst - src)')
        else:
            dst2src_pairs = []
        return (
         len(intersection_equal_pairs), len(intersection_unequal_pairs), len(src2dst_pairs), len(dst2src_pairs))


if '__main__' == __name__:
    main(sys.argv[1:])