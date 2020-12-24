# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ploader/download_handler.py
# Compiled at: 2014-01-14 07:49:27
# Size of source mod 2**32: 3556 bytes
import threading, subprocess, os, os.path, time, re, sys, ploader.utils as utils, ploader.rar_handler, rarfile

class Download(object):

    def __init__(self, name, link_list, passwd=None):
        self.name = name
        self.links = link_list
        self.passwd = passwd
        self.settings = utils.load_config()
        self.dw_dir = utils.set_dir(os.path.join(self.settings['download-dir'], self.name.replace(' ', '_')))
        self.log_dir = utils.set_dir(os.path.join(self.dw_dir, 'logs'))
        self.saver = None
        self.cur_item = None
        return

    def __str__(self):
        out = '\n'
        out += '%s (%i) - %s\n' % (self.name, len(self.links), self.passwd)
        for ele in self.links:
            out += '[%s] %s (%s)\n' % (ele['status'], ele['link'], ele['progress'] if 'progress' in ele.keys() else '-')

        out += '-> %s\n' % self.dw_dir
        return out

    def __repr__(self):
        return repr(str(self))

    def set_save_function(self, save_fun):
        self.saver = save_fun

    def get_status(self):
        suc = True
        for ele in self.links:
            if ele['status'] != 'success':
                suc = False
                continue

        if suc:
            return 'success'
        nots = True
        for ele in self.links:
            if ele['status'] != 'not started':
                nots = False
                continue

        if nots:
            return 'not started'
        return 'loading'

    def unpack(self):
        if self.get_status() == 'success':
            for ele in self.links:
                fn = ele['filename']
                if ploader.rar_handler.is_rar(os.path.join(self.dw_dir, fn)):
                    pass
                rar = ploader.rar_handler.RAR(os.path.join(self.dw_dir, fn), self.passwd)
                if rar.all_files_present():
                    if rar.is_first_vol():
                        sys.stdout.write('Extracting "%s"...' % fn)
                        sys.stdout.flush()
                        try:
                            rar.extract()
                            print(' Done')
                        except rarfile.RarNoFilesError:
                            print(' Fail: No files found')
                        except rarfile.RarCRCError:
                            print(' Fail: CRC error')

                    else:
                        print('Could not find all compressed files for "%s"' % fn)
                else:
                    print('No decompression method found for "%s"' % fn)

    def download(self):
        """Handles complete download
                        Puts link to end of list if error occurs
                """

        def load():
            error_item = None
            for ele in self.links:
                if ele['status'] == 'success':
                    continue
                ele['progress'] = '-'
                self.cur_item = ele
                link = ele['link']
                fname = ele['filename']
                ele['status'] = 'loading'
                self.loading = True
                answ = utils.parse_url_info(*utils.get_url_info(link))
                error = not answ
                if not error:
                    fname, download_link = answ
                    if not ele['filename']:
                        ele['filename'] = fname
                    final_path = os.path.join(self.dw_dir, fname)
                    error = not utils.load_file(download_link, final_path, self.handle_download_progress)
                self.loading = False
                if error:
                    ele['status'] = 'error'
                    error_item = ele
                else:
                    ele['status'] = 'success'
                if error_item:
                    self.links.remove(error_item)
                    self.links.append(error_item)
                    error_item = None
                self.saver()

            return

        load()

    def handle_download_progress(self, loaded_block_num, block_size, total_size):
        self.cur_item['progress'] = str(utils.sizeof_fmt(loaded_block_num * block_size)) + '/' + str(utils.sizeof_fmt(total_size))