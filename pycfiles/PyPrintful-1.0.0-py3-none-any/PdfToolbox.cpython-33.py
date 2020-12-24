# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/PdfToolbox.py
# Compiled at: 2014-04-03 10:37:45
# Size of source mod 2**32: 5108 bytes
__doc__ = '\nCreated on Sep 21, 2013\n\n@author: "Colin Manning"\n'
import os, subprocess, hashlib, time, logging, traceback, utils

class PdfToolbox(object):
    """PdfToolbox"""
    pdftoolbox_path = None
    cache_path = None
    logger = None
    activation_code = None
    ready = False
    tmp_folder = None
    webroot_folder = None

    def __init__(self, pdftoolbox_path, cache_path, activation_code, tmp_folder, webroot_folder):
        self.pdftoolbox_path = pdftoolbox_path
        self.cache_path = cache_path
        self.logger = logging.getLogger('printflow2')
        self.activation_code = activation_code
        self.ready = True
        utils.ensureDirectoryExists(tmp_folder)
        self.tmp_folder = tmp_folder
        self.webroot_folder = webroot_folder

    def run_preview(self, serial_no, file_path, file_name, guid):
        status = -1
        if self.ready:
            theFile = os.path.join(file_path, file_name)
            preview_folder = os.path.join(self.webroot_folder, guid.replace('-', '/'))
            utils.ensureDirectoryExists(preview_folder)
            preview_file_name = file_name + '.jpg'
            previewFile = os.path.join(preview_folder, preview_file_name)
            try:
                cmd = [
                 '"' + self.pdftoolbox_path + '"', '--license=' + str(serial_no), '--secret=' + str(self.get_license(serial_no)),
                 '--saveasimg', '--noprogress', '--pagerange=1', '--imgformat=JPEG', '--resolution=400x400', '--compression=JPEG_high',
                 '--outputfile="' + previewFile + '"',
                 '"' + str(theFile) + '"']
                cmd_str = ' '.join(cmd)
                p = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                processResult = p.communicate()
            except subprocess.CalledProcessError:
                self.logger.error('Problem calling command: ' + str(cmd))
                self.logger(traceback.format_exc())

        return (
         status, processResult, previewFile, preview_file_name)

    def run_job(self, serial_no, file_path, file_name, profile, guid):
        status = -1
        if self.ready:
            try:
                theFile = os.path.join(file_path, file_name)
                report_folder = os.path.join(os.path.join(self.webroot_folder, guid.replace('-', '/')))
                utils.ensureDirectoryExists(report_folder)
                report_file_text = os.path.join(report_folder, 'report_' + utils.removeNonAscii(file_name) + '.txt')
                if os.path.exists(report_file_text):
                    try:
                        os.remove(report_file_text)
                    except:
                        self.logger.error('Problem removing tmp text report file: ' + report_file_text)

                report_file_html = os.path.join(report_folder, 'report_' + utils.removeNonAscii(file_name) + '.html')
                if os.path.exists(report_file_html):
                    try:
                        os.remove(report_file_html)
                    except:
                        self.logger.error('Problem removing tmp html report file: ' + report_file_html)

                self.logger.info('Processing file:' + theFile)
                processResult = None
                cmd = [
                 '"' + str(self.pdftoolbox_path) + '"', '--license=' + str(serial_no), '--secret=' + str(self.get_license(serial_no)),
                 '--nosummary', '--noprogress', '--nohits', '--nofixups',
                 '--report=XSLT=compacttext_point,ALWAYS,PATH="' + str(report_file_text) + '"',
                 '--report=XSLT=compacthtml_point,ALWAYS,PATH="' + str(report_file_html) + '"',
                 '"' + str(profile) + '"', '"' + str(theFile) + '"']
                cmd_str = ' '.join(cmd)
                p = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                processResult = p.communicate()
                if p.returncode is not None:
                    status = p.returncode
            except subprocess.CalledProcessError:
                self.logger.error('Problem calling command: ' + str(cmd))
                traceback.print_exc()

        else:
            self.logger.error('pdftoolbox not correctly initialised')
        return (status, processResult[0].decode(), report_folder, report_file_text, report_file_html)

    def get_license(self, serial_no):
        this_check_time = time.strftime('%Y-%m-%d-%H-%M', time.localtime())
        secret = '<' + self.activation_code + '><' + this_check_time + '><' + serial_no + '>'
        return hashlib.md5(secret.encode('utf-8')).hexdigest()