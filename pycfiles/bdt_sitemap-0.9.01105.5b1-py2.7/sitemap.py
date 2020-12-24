# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bdt\sitemap.py
# Compiled at: 2014-08-14 07:35:27
import os, sys, datetime
from urllib2 import urlopen, URLError, HTTPError
from urllib import pathname2url
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
emod_time = datetime.date(1990, 1, 1)

def init_emod_time():
    global emod_time
    emod_time = datetime.date(1990, 1, 1)


def compare_emod_time(newtime):
    global emod_time
    if emod_time < newtime:
        emod_time = newtime


def create_sitemap(domain, site_dir, ignorelist=[]):
    sitemap_index = "<sitemapindex xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'></sitemapindex>"
    empty_record = '<sitemap><loc></loc><lastmod></lastmod></sitemap>'
    for root, dirs, files in os.walk(os.path.abspath(site_dir), topdown=False):
        skipdir = False
        for term in ignorelist:
            if term in root.replace(site_dir, ''):
                skipdir = True
                break

        if skipdir:
            break
        sitemap_index_element = ET.fromstring(sitemap_index)
        init_emod_time()
        for name in files:
            skipitem = False
            for term in ignorelist:
                if term in name:
                    skipitem = True

            if skipitem:
                continue
            record = ET.fromstring(empty_record)
            curfile_path = os.path.join(root, name)
            record.find('loc').text = pathname2url(curfile_path.replace(site_dir, ''))
            lastmod = datetime.date.fromtimestamp(os.stat(curfile_path).st_mtime)
            record.find('lastmod').text = lastmod.__str__()
            compare_emod_time(lastmod)
            if name.endswith('html'):
                htmlsoup = BeautifulSoup(open(curfile_path))
                for meta in htmlsoup.find_all('meta'):
                    metatag_name = meta.get('name')
                    if metatag_name != None:
                        ET.SubElement(record, meta.get('name'))
                        record.find(meta.get('name')).text = meta.get('content')

            sitemap_index_element.append(record)

        for name in dirs:
            skipitem = False
            for term in ignorelist:
                if term in name:
                    skipitem = True

            if skipitem:
                continue
            record = ET.fromstring(empty_record)
            curdir_path = os.path.join(root, name)
            index_path = os.path.join(curdir_path, 'index.html')
            record.find('loc').text = pathname2url(curdir_path.replace(site_dir, ''))
            record.find('lastmod').text = ET.parse(os.path.join(curdir_path, 'sitemap.xml')).getroot().find('lastmod').text
            compare_emod_time(lastmod)
            sitemap_index_element.append(record)

        sitemap_index_element.append(ET.Element('lastmod'))
        sitemap_index_element.find('lastmod').text = emod_time.__str__()
        ET.ElementTree(sitemap_index_element).write(os.path.join(root, 'sitemap.xml'), encoding='UTF-8', xml_declaration=True)

    print 'All sitemaps successfully generated.'
    return


def run_shell():
    help_notice = "\n\tDomain:\t\tIn url form, the domain name for which you're generating sitemaps\n\tLocalPath:\tPath to the website directory as stored locally. WARNING: If this argument is not passed, current directory will be assumed! You will be asked if this was a mistake, and given a chance to exit, but that's all! You will end up with sitemap.xmls all over the place if you're not careful!\n"
    arglength = len(sys.argv) - 1
    domain = 'http://www.nonsense.ru/'
    workdir = os.getcwd()
    if arglength == 0:
        print 'Insufficient arguments, please pass' + help_notice
        exit(1)
    elif arglength > 0:
        if sys.argv[1].lower() in ('-h', '-help', 'help'):
            print help_notice
            exit(0)
        if arglength > 2:
            print 'Too many arguments passed! Valid arguments are' + help_notice
            exit(1)
        domain = sys.argv[1]
        if arglength == 1:
            print 'Only one argument passed!'
            print 'Domain name set to:' + domain
            print 'Working directory will be assumed to be current working directory, ie:' + os.getcwd()
            if raw_input('\nContinue?').lower() not in ('y', 'yes', 'yeah'):
                exit(1)
        else:
            workdir = sys.argv[2]
            if not (os.path.exists(workdir) or os.path.isdir(workdir)):
                print 'The work directory you have passed is invalid! Check your second argument:' + help_notice
                exit(1)
    create_sitemap(domain, workdir, ['testing', 'sitemap.xml'])