# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python27\Lib\site-packages\CodeLibWrapper\Src\IO\SimpleFileCompare.py
# Compiled at: 2016-11-29 02:55:28
import filecmp, os, time

def __get_pretty_time(state):
    return time.strftime('%y-%m-%d %H:%M:%S', time.localtime(state.st_mtime))


def __get_path_size(dir_path):
    size = 0
    for root, dirs, files in os.walk(dir_path):
        for m_file in files:
            path = os.path.join(root, m_file)
            size = os.path.getsize(path)

    return size


def dir_compare(source_dir_path, target_dir_path, output_report_path):
    u"""
    比较文件夹内的差异
    :param source_dir_path:Source 文件夹
    :param target_dir_path: Target 文件夹
    :param output_report_path: 比较后的差异报告
    :return: 无返回值
    """
    if output_report_path == '' or output_report_path is None:
        output_report_path = os.getcwd()
    if not os.path.exists(output_report_path):
        os.mkdir(output_report_path)
    if os.path.exists(output_report_path + '\\content_diff.txt'):
        os.remove(output_report_path + '\\content_diff.txt')
    if os.path.exists(output_report_path + '\\diff.txt'):
        os.remove(output_report_path + '\\diff.txt')
    if os.path.exists(output_report_path + '\\OnlyInSource.txt'):
        os.remove(output_report_path + '\\OnlyInSource.txt')
    if os.path.exists(output_report_path + '\\OnlyInTarget.txt'):
        os.remove(output_report_path + '\\OnlyInTarget.txt')
    source_files = []
    target_files = []
    for root, dirs, files in os.walk(source_dir_path):
        for f in files:
            source_files.append(root + '\\' + f)

    for root, dirs, files in os.walk(target_dir_path):
        for f in files:
            target_files.append(root + '\\' + f)

    source_path_len = len(source_dir_path)
    tmp_source_files = []
    for f in source_files:
        tmp_source_files.append(f[source_path_len:])

    target_path_len = len(target_dir_path)
    tmp_target_files = []
    for f in target_files:
        tmp_target_files.append(f[target_path_len:])

    source_files = tmp_source_files
    target_files = tmp_target_files
    set_source_files = set(source_files)
    set_target_files = set(target_files)
    common_files = set_source_files & set_target_files
    print ("=====File with different size in '", source_dir_path, "' and '", target_dir_path, "'=====")
    for f in sorted(common_files):
        sA = os.path.getsize(source_dir_path + '\\' + f)
        sB = os.path.getsize(target_dir_path + '\\' + f)
        if sA == sB:
            saf = []
            sbf = []
            sAfile = open(source_dir_path + '\\' + f)
            iter_f = iter(sAfile)
            for line in iter_f:
                saf.append(line)

            sAfile.close()
            sBfile = open(target_dir_path + '\\' + f)
            iter_fb = iter(sBfile)
            for line in iter_fb:
                sbf.append(line)

            sBfile.close()
            saf1 = sorted(saf)
            sbf1 = sorted(sbf)
            if len(saf1) != len(sbf1):
                with open(output_report_path + '\\content_diff.txt', 'a') as (fp):
                    fp.write(source_dir_path + '\\' + f + ' lines size not equal ' + target_dir_path + '\\' + f + '\n')
            else:
                for i in range(len(saf1)):
                    if saf1[i] != sbf1[i]:
                        with open(output_report_path + '\\content_diff.txt', 'a') as (fp1):
                            fp1.write(source_dir_path + '\\' + f + ' content not equal ' + target_dir_path + '\\' + f + '\n')
                            break

        else:
            with open(output_report_path + '\\diff.txt', 'a') as (di):
                di.write('File Name=%s    Source file size:%d   !=  Target file size:%d' % (f, sA, sB) + '\n')

    only_files = set_source_files ^ set_target_files
    files_only_in_source_dir = []
    files_only_in_target_dir = []
    for of in only_files:
        if of in source_files:
            files_only_in_source_dir.append(of)
        elif of in target_files:
            files_only_in_target_dir.append(of)

    print (
     '#only files in ', source_dir_path)
    for of in sorted(files_only_in_source_dir):
        print of
        with open(output_report_path + '\\OnlyInSource.txt', 'w') as (source):
            source.write(of + '\n')

    print (
     '#only files in ', target_dir_path)
    for of in sorted(files_only_in_target_dir):
        print of
        with open(output_report_path + '\\OnlyInTarget.txt', 'w') as (target):
            target.write(of + '\n')

    return


def file_compare(source_file_path, target_file_path):
    return filecmp.cmp(source_file_path, target_file_path)


def main():
    source_dir = 'D:\\OutputDir\\abc'
    target_dir = 'D:\\OutputDir\\abcd'
    report_output_dir = 'D:\\OutputDir\\123'
    dir_compare(source_dir, target_dir, report_output_dir)
    result = file_compare('D:\\OutputDir\\abc\\log-20161026-131926 - Copy.html', 'D:\\OutputDir\\abc\\log-20161026-131926.html')
    if result:
        print 'Same'
    else:
        print 'Diff'


if __name__ == '__main__':
    main()