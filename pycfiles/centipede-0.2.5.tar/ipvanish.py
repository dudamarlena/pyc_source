# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/vpn/ipvanish.py
# Compiled at: 2016-11-10 09:15:01
import httplib2, logging, os, shutil, socket, sys, urllib, zipfile

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as (zf):
        zf.extractall(dest_dir)


def create_config_files(directory):
    """
    Initialize directory ready for vpn walker
    :param directory: the path where you want this to happen
    :return:
    """
    config_zip_url = 'http://www.ipvanish.com/software/configs/configs.zip'
    if not os.path.exists(directory):
        os.makedirs(directory)
    logging.info('Starting to download IPVanish config file zip')
    url_opener = urllib.URLopener()
    zip_path = os.path.join(directory, '../configs.zip')
    unzip_path = os.path.join(directory, '../unzipped')
    if not os.path.exists(unzip_path):
        os.makedirs(unzip_path)
    url_opener.retrieve(config_zip_url, zip_path)
    logging.info('Extracting zip file')
    unzip(zip_path, unzip_path)
    os.remove(zip_path)
    shutil.copyfile(os.path.join(unzip_path, 'ca.ipvanish.com.crt'), os.path.join(directory, '../ca.ipvanish.com.crt'))
    server_country = {}
    for filename in os.listdir(unzip_path):
        if filename.endswith('.ovpn'):
            country = filename.split('-')[1]
            file_path = os.path.join(unzip_path, filename)
            lines = [ line.rstrip('\n') for line in open(file_path) ]
            ip = ''
            for line in lines:
                if line.startswith('remote'):
                    hostname = line.split(' ')[1]
                    ip = socket.gethostbyname(hostname)
                    break

            if len(ip) > 0:
                new_path = os.path.join(directory, ip + '.ovpn')
                shutil.copyfile(file_path, new_path)
                server_country[ip] = country
            else:
                logging.warn('Unable to resolve hostname and remove %s' % filename)
                os.remove(file_path)

    with open(os.path.join(directory, 'servers.txt'), 'w') as (f):
        for ip in server_country:
            f.write(('|').join([ip, server_country[ip]]) + '\n')

    shutil.rmtree(unzip_path)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ('Usage {0} <directory to create VPNs in>').format(sys.argv[0])
        sys.exit(1)
    create_config_files(sys.argv[1])