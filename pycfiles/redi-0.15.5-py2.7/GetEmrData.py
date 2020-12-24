# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/utils/GetEmrData.py
# Compiled at: 2018-08-13 08:58:37
"""
This module is used to connect to an sftp server
and retrieve the raw EMR file to be used as input for RED-I.
"""
import os, csv
from xml.sax import saxutils
import logging, pysftp
from csv2xml import openio, Writer
from paramiko.ssh_exception import SSHException, BadAuthenticationType
import sys, ast, copy
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class EmrFileAccessDetails(object):
    """
    Encapsulate the settings used to retrieve the EMR
    source file using an SFTP connection
    @see redi#_run()
    """

    def __init__(self, emr_sftp_project_name, emr_download_list, emr_host, emr_username, emr_password, emr_port, emr_private_key, emr_private_key_pass):
        self.sftp_project_name = emr_sftp_project_name
        try:
            self.download_list = ast.literal_eval(emr_download_list)
        except ValueError:
            self.download_list = {str(emr_download_list): 'raw.txt'}

        self.host = emr_host
        self.username = emr_username
        self.password = emr_password
        self.port = int(emr_port)
        self.private_key = emr_private_key
        self.private_key_pass = emr_private_key_pass


def download_files(destination, access_details):
    """
    Download a file from the sftp server
    :destination the name of the file which will be downloaded
    :access_details holds info for accessing the source file over sftp

    @see get_emr_data()
    """
    connection_info = dict(access_details.__dict__)
    del connection_info['download_list']
    del connection_info['sftp_project_name']
    try:
        with pysftp.Connection(**connection_info) as (sftp):
            logger.info('User %s connected to sftp server %s' % (
             connection_info['username'], connection_info['host']))
            sftp.get(access_details.download_list, destination)
    except IOError as e:
        logger.error('Please verify that the private key file mentioned in settings.ini exists.')
        logger.exception(e)
        sys.exit()
    except BadAuthenticationType as e:
        logger.error('Please verify that the EMR server connection details under section emr_data in settings.ini are correct')
        logger.exception(e)
        sys.exit()
    except SSHException as e:
        logger.error('Please verify that the EMR server connection details under section emr_data in settings.ini are correct')
        logger.exception(e)
        sys.exit()


def data_preprocessing(input_filename, output_filename):
    with open(input_filename, 'r') as (raw):
        with open(output_filename, 'w') as (processed):
            for line in raw:
                processed.write(saxutils.escape(line))


def generate_xml(input_filename, output_filename):

    class Arguments:
        pass

    args = Arguments()
    args.iencoding = 'cp1252'
    args.oencoding = 'utf8'
    args.header = (True,)
    args.delimiter = ','
    args.declaration = True
    args.root_elem = 'study'
    args.record_elem = 'subject'
    args.ofile = output_filename
    args.ifile = input_filename
    args.linebreak = '\n'
    args.escapechar = None
    args.indent = '    '
    args.quoting = csv.QUOTE_MINIMAL
    args.skipinitialspace = False
    args.field_elem = 'field'
    args.flat_fields = False
    args.doublequote = True
    args.quotechar = '"'
    args.newline_elem = None
    csv.register_dialect('custom', delimiter=args.delimiter, doublequote=args.doublequote, escapechar=args.escapechar, quotechar=args.quotechar, quoting=args.quoting, skipinitialspace=args.skipinitialspace)
    with openio(args.ifile, mode='r', encoding=args.iencoding, newline='') as (ifile):
        csvreader = csv.reader(ifile, dialect='custom')
        if args.header:
            args.header = next(csvreader)
        with openio(args.ofile, 'w', args.oencoding) as (ofile):
            writer = Writer(ofile, args)
            writer.write_file(csvreader)
    return


def cleanup(file_to_delete):
    os.remove(file_to_delete)


def get_emr_data(conf_dir, connection_details):
    """
    :conf_dir configuration directory name
    :connection_details EmrFileAccessDetails object
    """
    number_of_files = len(connection_details.download_list)
    counter = 1
    for key in connection_details.download_list:
        logger.info('Now downloading %i of %i file(s)', counter, number_of_files)
        temp_connection_details = copy.deepcopy(connection_details)
        raw_txt_file = os.path.join(conf_dir, connection_details.download_list[key])
        temp_connection_details.download_list = os.path.join(connection_details.sftp_project_name, key)
        logger.info('Downloading remote file file: ' + temp_connection_details.download_list)
        logger.info('Saving to local file name: ' + raw_txt_file)
        download_files(raw_txt_file, temp_connection_details)
        counter += 1