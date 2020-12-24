# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/gui.py
# Compiled at: 2012-08-26 09:08:47
import pygtk, gtk, gobject, glob, os, time, ConfigParser, webkit, mechanize, vte
from subprocess import Popen, PIPE, STDOUT
import version, new_version, directory, opencores, tcl
pygtk.require('2.0')
import pango, shlex, editor, devices
from pygments.lexers import PythonLexer
from pygments.styles.tango import TangoStyle
from pygments.token import Name, Keyword
gobject.threads_init()

class mk_gui:
    """gui class for the main GUI of boot.
    """

    def dir_entry_changed(self, widget):
        _tmp = self.dir_entry.get_text()
        self.top_level_label.set_text(_tmp)

    def entry_keypress(self, widget, event):
        if event.keyval in (gtk.keysyms.D, gtk.keysyms.d) and event.state & gtk.gdk.CONTROL_MASK:
            full_path_file = self.dir_entry.get_text()
            if os.path.isdir(full_path_file):
                print 'Wrong file name format. No file deleted.'
                self.on_warn('Wrong file name format. No file deleted.')
                return 1
            if os.path.isfile(full_path_file):
                answer = self.on_warn('The following file will be deleted:  ' + os.path.basename(full_path_file))
                if answer == gtk.RESPONSE_OK:
                    os.remove(full_path_file)
                    print 'File deleted.'
                else:
                    print 'File not deleted.'
            else:
                print 'This file does not exist. No file deleted.'
                self.on_warn('This file does not exist. No file deleted.')
                return 1
        if event.keyval in (gtk.keysyms.N, gtk.keysyms.n) and event.state & gtk.gdk.CONTROL_MASK:
            full_path_file = self.dir_entry.get_text()
            if os.path.isdir(full_path_file):
                print 'Wrong file name format. No file created.'
                return 1
            if not os.path.isfile(full_path_file):
                answer = self.on_warn('The following file will be created:  ' + os.path.basename(full_path_file))
                if answer == gtk.RESPONSE_OK:
                    open(full_path_file, 'w').close()
                    print 'New file created.'
                else:
                    print 'File not created.'
            else:
                print 'This file already exists, no file created.'
                return 1
        else:
            print 'Key combination inactive.'
        return 0

    def compileSimulateAction(self, widget, action):
        wd = os.path.dirname(os.path.realpath(self.dir_entry.get_text()))
        tld_file = os.path.basename(self.dir_entry.get_text())
        sim_opt = self.sim_opt_entry.get_text()
        if action == 'Compile':
            print 'Start compiling process'
            self.comm_i.send([wd, tld_file, self.GTKWAVE_COMM_SOCKET_ID,
             sim_opt, True, False])
            self.btn_compile.set_label('Stop')
        if action == 'Compile & Simulate':
            print 'Start compiling process'
            self.comm_i.send([wd, tld_file, self.GTKWAVE_COMM_SOCKET_ID,
             sim_opt, True, True])
            self.btn_compile.set_label('Stop')
        if action == 'Stop':
            print 'Stop compiling process (not implemented)'
            self.btn_compile.set_label('Compile')

    def select_file(self, widget):
        dialog = gtk.FileChooserDialog('Choose top-level VHDL design file', None, gtk.FILE_CHOOSER_ACTION_OPEN, (
         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        _dir = os.path.dirname(os.path.realpath(self.dir_entry.get_text()))
        dialog.set_current_folder(_dir)
        print _dir
        filter = gtk.FileFilter()
        filter.set_name('.vhdl files')
        filter.add_pattern('*.vhdl')
        filter.add_pattern('*.vhd')
        dialog.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name('All files')
        filter.add_pattern('*')
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            print dialog.get_filename(), 'selected'
            self.dir_entry.set_text(dialog.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            pass
        dialog.destroy()
        return 0

    def delete(self, widget, event=None):
        gtk.main_quit()
        return False

    def add_conn(self, compute_prc, comm_i):
        self.compute_prc = compute_prc
        self.comm_i = comm_i
        fd = comm_i.fileno()
        gobject.io_add_watch(fd, gobject.IO_IN, self.update_gui)
        return 0

    def update_gui(self, fd, cond):
        val = self.comm_i.recv()
        self.make_pretty_txt(self, val, self.comp_textbuffer)
        if 'Begin compiling' in val:
            self.comp_bar_go = True
            self.comp_bar.set_text('Compiling...')
        elif 'compilation error' in val:
            self.comp_bar_go = False
            self.comp_bar.set_text('Compilation Error.')
            self.comp_bar.set_fraction(0.0)
            print 'Compilation error.'
        elif 'End compiling' in val:
            self.comp_bar_go = False
            self.comp_bar.set_text('Compilation Successful.')
            self.comp_bar.set_fraction(0.0)
            self.btn_compile.set_label('Compile')
            print 'Compilation process ended.'
        elif 'End processing' in val:
            self.comp_bar_go = False
            self.comp_bar.set_text('Compilation Successful.')
            self.comp_bar.set_fraction(1.0)
            print 'Compiled successfully.'
        elif 'CLEAR ALL' in val:
            self.comp_textbuffer.set_text('')
        return True

    def on_warn(self, _text=''):
        md = gtk.MessageDialog(self.window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK_CANCEL, _text)
        answer = md.run()
        md.destroy()
        return answer

    def save_configuration_locally(self):
        print 'Saving some parameters in local "~/.boot" file'
        ma = self.ma.get_model()[self.ma.get_active()][0]
        fa = self.fa.get_model()[self.fa.get_active()][0]
        de = self.de.get_model()[self.de.get_active()][0]
        pa = self.pa.get_model()[self.pa.get_active()][0]
        sp = self.sp.get_model()[self.sp.get_active()][0]
        wd = os.path.dirname(os.path.realpath(self.dir_entry.get_text()))
        tld_file = os.path.basename(self.dir_entry.get_text())
        sim_opt = self.sim_opt_entry.get_text()
        syn_tool_path = self.tool_path_entry.get_text()
        syn_cmd = self.tool_command_entry.get_text()
        config = ConfigParser.RawConfigParser()
        config.add_section('boot')
        config.set('boot', 'version', version.boot_version)
        config.add_section('Last parameters')
        config.set('Last parameters', 'working directory', wd)
        config.set('Last parameters', 'top-level design file', tld_file)
        config.set('Last parameters', 'simulation options', sim_opt)
        config.set('Last parameters', 'synthesis tool path', syn_tool_path)
        config.set('Last parameters', 'synthesis command', syn_cmd)
        config.set('Last parameters', 'manufacturer', ma)
        config.set('Last parameters', 'family', fa)
        config.set('Last parameters', 'device', de)
        config.set('Last parameters', 'package', pa)
        config.set('Last parameters', 'speed grade', sp)
        conf_file = os.path.join(os.environ['HOME'], '.boot')
        with open(conf_file, 'wb') as (configfile):
            config.write(configfile)
        return 0

    def load_local_configuration_file(self):
        conf_file = os.path.join(os.environ['HOME'], '.boot')
        if os.path.isfile(conf_file):
            print 'Loading some parameters from local "~/.boot" file'
            config = ConfigParser.ConfigParser()
            config.readfp(open(conf_file))
            _ma = config.get('Last parameters', 'manufacturer')
            _fa = config.get('Last parameters', 'family')
            _de = config.get('Last parameters', 'device')
            _pa = config.get('Last parameters', 'package')
            _sp = config.get('Last parameters', 'speed grade')
            sim_opt = config.get('Last parameters', 'simulation options')
            syn_tool_path = config.get('Last parameters', 'synthesis tool path')
            syn_comm = config.get('Last parameters', 'synthesis command')
            for x, y in enumerate(self.ma.get_model()):
                if y[0] == _ma:
                    self.ma.set_active(x)

            for x, y in enumerate(self.fa.get_model()):
                if y[0] == _fa:
                    self.fa.set_active(x)

            for x, y in enumerate(self.de.get_model()):
                if y[0] == _de:
                    self.de.set_active(x)

            for x, y in enumerate(self.pa.get_model()):
                if y[0] == _pa:
                    self.pa.set_active(x)

            for x, y in enumerate(self.sp.get_model()):
                if y[0] == _sp:
                    self.sp.set_active(x)

            self.sim_opt_entry.set_text(sim_opt)
            self.tool_path_entry.set_text(syn_tool_path)
            self.tool_command_entry.set_text(syn_comm)
        return 0

    def gen_syn_script_button_action(self, widget, action):
        tl, files, constraints_file = (None, None, None)
        tl = os.path.basename(self.dir_entry.get_text())
        tl = tl.split('.')[0]
        wd = os.path.dirname(os.path.realpath(self.dir_entry.get_text()))
        syn_out_dir = os.path.join(wd, 'build')
        files = glob.glob(os.path.join(wd, '*.vhd')) + glob.glob(os.path.join(wd, '*.vhdl'))
        files = [ os.path.basename(x) for x in files ]
        for x in files:
            if '_tb' in x:
                files.remove(x)

        constraints_file = glob.glob(os.path.join(wd, '*.ucf'))
        print 'Synthesis script about to be generated.'
        print 'top-level design:', tl
        print 'vhdl file list:', files
        print 'Constrains file:', constraints_file
        ma = self.ma.get_model()[self.ma.get_active()][0]
        fa = self.fa.get_model()[self.fa.get_active()][0]
        de = self.de.get_model()[self.de.get_active()][0]
        pa = self.pa.get_model()[self.pa.get_active()][0]
        sp = self.sp.get_model()[self.sp.get_active()][0]
        if os.path.isdir(syn_out_dir):
            pass
        else:
            try:
                os.path.os.mkdir(syn_out_dir)
            except:
                print "You don't have the permission for creating:", syn_out_dir

        if tcl.make_xilinx(syn_out_dir, tl, files, constraints_file, fa, de, pa, sp):
            _start = self.syn_textbuffer.get_end_iter()
            _txt = 'Problems in saving the Xilinx synthesis script.\n' + 'Maybe you have writing permission problems.\n'
            self.syn_textbuffer.insert_with_tags(_start, _txt)
            return 1
        else:
            print 'Xilinx synthesis script successfully generated.'
            _start = self.syn_textbuffer.get_end_iter()
            _txt = 'Xilinx synthesis script successfully generated ' + '(you can inspect it with the link on the right).\n'
            self.syn_textbuffer.insert_with_tags(_start, _txt)
            _txt = 'xtclsh src/build/xil_syn_script.tcl'
            self.tool_command_entry.set_text(_txt)
            return 0

    def open_in_editor(self, label, uri):
        wd = os.path.dirname(os.path.realpath(self.dir_entry.get_text()))
        tld_file = os.path.basename(self.dir_entry.get_text())
        _fl = ''
        if 'synthesis_report' in uri:
            tld = tld_file.split('.')[0]
            _fl = os.path.join(wd, 'build', tld + '.syr')
        if 'xtclsh_script' in uri:
            _fl = os.path.join(wd, 'build', 'xil_syn_script.tcl')
        if os.path.isfile(_fl):
            try:
                print 'Opening the file in boot text viewer.'
                editor.text_editor(_fl).start()
            except:
                print 'Problems in loading the file'

        return True

    def syn_watchdog(self, w):
        if type(self.syn_p) is Popen and self.syn_p.poll() == None:
            self.start_stop_syn_button.set_label('Stop Synthesis')
            self.syn_spinner.start()
        else:
            gobject.source_remove(self.g_syn_id)
            print 'Synthesis process naturally ended and pipe closed.'
            self.start_stop_syn_button.set_label('Start Synthesis')
            self.syn_spinner.stop()
            return False
        startiter, enditer = self.syn_textbuffer.get_bounds()
        _txt = self.syn_textbuffer.get_text(startiter, enditer)
        if 'End of ISE Tcl script.' in _txt:
            _txt = ''
            print 'Synthesis process has ended.'
            self.syn_button_action(self, 'Stop Synthesis')
        elif 'no such file or directory' in _txt:
            _txt = ''
            print 'Synthesis process has ended.'
            self.syn_button_action(self, 'Stop Synthesis')
        return True

    def syn_button_action(self, widget, action):
        action = self.start_stop_syn_button.get_label()
        tl = self.dir_entry.get_text()
        syn_path = self.tool_path_entry.get_text()
        syn_cmd = self.tool_command_entry.get_text()
        wd = os.path.dirname(os.path.realpath(self.dir_entry.get_text()))
        if action == 'Start Synthesis':
            self.save_configuration_locally()
            if self.syn_p != None and self.syn_p.returncode == None:
                print 'Synthesis process not terminated yet. Exiting'
                return 0
            print 'Starting synthesis process.'
            self.syn_textbuffer.set_text('Synthesis process output window.\n')
            all_unwanted_fls = glob.glob(os.path.join(wd, 'build', '*.xise'))
            for fl in all_unwanted_fls:
                os.remove(fl)

            command = [
             'bash', '-c', syn_path + '>>/dev/null; env']
            print 'Running command:', command
            proc = Popen(command, stdout=PIPE)
            for line in proc.stdout:
                key, _, value = line.rstrip('\n').partition('=')
                os.environ[key] = value

            proc.communicate()
            try:
                self.syn_p = Popen(['/bin/sh'], shell=False, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                cmd = 'cd ' + wd + '/..\n'
                print 'Running the commmand:', cmd
                self.syn_p.stdin.write(cmd)
                cmd = syn_cmd + '\n'
                print 'Running the commmand:', cmd
                self.syn_p.stdin.write(cmd)
                print 'New Synthesis process ID:', self.syn_p.pid
            except:
                print 'Process "xtclsh" cannot start.'
                _start = self.syn_textbuffer.get_end_iter()
                self.syn_textbuffer.insert_with_tags(_start, 'Process "xtclsh" cannot start. Maybe you do not have ' + 'Xilinx ISE installed in your machine.\n')
                return 0

            self.start_stop_syn_button.set_label('Stop Synthesis')
            if self.g_syn_id != None:
                gobject.source_remove(self.g_syn_id)
            self.g_syn_id = gobject.io_add_watch(self.syn_p.stdout, gobject.IO_IN, self.write_to_syn_output)
            gobject.timeout_add(200, self.syn_watchdog, self)
        elif action == 'Stop Synthesis':
            if self.g_syn_id != None:
                gobject.source_remove(self.g_syn_id)
            if type(self.syn_p) is Popen:
                try:
                    print 'Current Synthesis process ID:', self.syn_p.pid
                    self.syn_p.kill()
                    while self.syn_p.poll() == None:
                        time.sleep(0.2)

                    print 'Synthesis process stopped.'
                    self.start_stop_syn_button.set_label('Start Synthesis')
                except:
                    print 'Synthesis process already killed.'
                    self.start_stop_syn_button.set_label('Start Synthesis')

        else:
            print 'Wrong synthesis command.'
        return 0

    class MyPythonLexer(PythonLexer):
        EXTRA_KEYWORDS = [
         'Begin', 'End', 'simulation', 'compiling', 'error', 'Noprocessing',
         'completed', 'successfully', 'warning',
         'Completed', 'failed']

        def get_tokens_unprocessed(self, text):
            for index, token, value in PythonLexer.get_tokens_unprocessed(self, text):
                if token is Name and value in self.EXTRA_KEYWORDS:
                    yield (
                     index, Keyword.Pseudo, value)
                else:
                    yield (
                     index, token, value)

    def make_pretty_txt(self, widget, _txt, _buff):
        STYLE = TangoStyle
        styles = {}
        for token, value in self.MyPythonLexer().get_tokens(_txt):
            while not STYLE.styles_token(token) and token.parent:
                token = token.parent

            if token not in styles:
                styles[token] = _buff.create_tag()
            start = _buff.get_end_iter()
            _buff.insert_with_tags(start, value.encode('utf-8'), styles[token])

        for token, tag in styles.iteritems():
            style = STYLE.style_for_token(token)
            if style['bgcolor']:
                tag.set_property('background', '#' + style['bgcolor'])
            if style['color']:
                tag.set_property('foreground', '#' + style['color'])
            if style['bold']:
                tag.set_property('weight', pango.WEIGHT_BOLD)
            if style['italic']:
                tag.set_property('style', pango.STYLE_ITALIC)
            if style['underline']:
                tag.set_property('underline', pango.UNDERLINE_SINGLE)

        return 0

    def write_to_syn_output(self, fd, condition):
        if condition == gobject.IO_IN:
            char = fd.readline()
            self.make_pretty_txt(self, char, self.syn_textbuffer)
            return True
        else:
            return False

    def make_dropdown_menu(self, data_in):
        store = gtk.TreeStore(str)
        for x in data_in:
            store.append(None, [x])

        combo = gtk.ComboBox(store)
        combo_cell_text = gtk.CellRendererText()
        combo.pack_start(combo_cell_text, True)
        combo.add_attribute(combo_cell_text, 'text', 0)
        combo.set_size_request(142, -1)
        return combo

    def filter_dropdown(self, widget):
        current_fa = self.fa.get_model()[self.fa.get_active()][0]
        model = self.de.get_model()
        self.de.set_model(None)
        model.clear()
        for x in devices.dev_device:
            if current_fa in x:
                y = x.split()[1]
                model.append(None, [y])

        self.de.set_model(model)
        self.de.set_active(0)
        return 0

    def set_default_boot(self, widget):
        try:
            homedir = os.path.expanduser('~')
            os.remove(os.path.join(homedir, '.boot'))
            print 'Local configuration file: ~/.boot deleted.'
        except:
            print 'Nothing to do.'

        _txt = 'Done, you should now restart boot.'
        self.set_default_button_label.set_text(_txt)
        return 0

    def check_for_new_ver(self, widget):
        self.update_boot_msg.set_text('')
        _answer = new_version.check_on_pypi()
        print _answer
        self.update_boot_msg.set_text(_answer)
        return 0

    def oc_go_back(self, widget, data=None):
        self.oc_browser.go_back()

    def oc_go_forward(self, widget, data=None):
        self.oc_browser.go_forward()

    def oc_load_www(self, widget, url):
        try:
            url.index('://')
        except:
            url = 'http://' + url

        self.oc_www_adr_bar.set_text(url)
        self.oc_browser.open(url)

    def oc_load_www_bar(self, widget):
        url = self.oc_www_adr_bar.get_text()
        self.oc_load_www(widget, url)

    def oc_update_buttons(self, widget, data=None):
        self.oc_www_adr_bar.set_text(widget.get_main_frame().get_uri())
        self.oc_back_button.set_sensitive(self.oc_browser.can_go_back())
        self.oc_forward_button.set_sensitive(self.oc_browser.can_go_forward())

    def oc_load_progress_amount(self, oc_webview, amount):
        self.oc_progress.set_fraction(amount / 100.0)
        js_code = '\n    // check if JQuery is loaded\n    if (typeof jQuery != \'undefined\'){\n    \n        // check if the title of the page contains the word \'OpenCores\'\n        if ($(\'title\').text().indexOf("OpenCores")!=-1){\n    \n            // Execure JQuery commands    \n            $(document).ready(function(){\n           \n               // hide unwanted portions of the page\n               $(".main .top").hide()\n               $(".main .line").hide()\n               $(".main .mid .mainmenu").hide()\n               $(".main .mid .content .banner").hide()\n               $(".main .mid .content .home-right").hide()\n               $(".main .mid .content").next().hide()\n               \n               // style stuff\n               $("body").css({"width":"95%"});\n               $("body .main").css({"width":"100%","border-radius": "0pt"});\n               $("body .main .mid").css({"width":"100%"});\n    \n               $(".main .mid .content h1.projects ").each(function(i) {\n                                            $(this).css({"color":"#999797", \n                                            "textShadow":"#999797 0px 0px 0px",\n                                            "width": "100%"});\n                                            });\n    \n               $("body .content").css({"width":"100%","padding-bottom":"50pt"});\n               $("body .content").children().last().css({"height":"220pt"});\n               $("body").css({"backgroundColor":"#FFF"});\n        \n               // turn off some css3 attributes \n               $(".main").css(\'boxShadow\', \'0px 0px 0px 0px #FFF\');\n               $(".main").css(\'MozBoxShadow\', \'0px 0px 0px 0px #FFF\');\n               $(".main").css(\'WebkitBoxShadow\', \'0px 0px 0px #FFF\');\n            });\n        }  \n    }\n    '
        try:
            oc_webview.execute_script(js_code)
        except:
            pass

    def oc_load_started(self, webview, frame):
        self.oc_scroller.hide()
        self.oc_progress.set_visible(True)

    def oc_load_finished(self, webview, frame):
        self.oc_scroller.show()
        self.oc_progress.set_visible(False)

    def oc_download(self, webview, download):
        import threading
        saveas = gtk.FileChooserDialog(title=None, action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(
         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        _dir = os.path.dirname(os.path.realpath(self.dir_entry.get_text()))
        saveas.set_current_folder(_dir)
        downloadfrom = download.get_network_request().get_uri()
        if 'http://opencores.org/download,' in downloadfrom:
            dl_fl = downloadfrom.split('http://opencores.org/download,')[(-1)] + '.tar.gz'
        elif downloadfrom.endswith('.html') or downloadfrom.endswith('.htm'):
            dl_fl = downloadfrom.split('/')[(-1)]
        else:
            dl_fl = downloadfrom.split('/')[(-1)] + '.html'
        saveas.set_current_name(dl_fl)
        saveas.set_default_response(gtk.RESPONSE_OK)
        resp = saveas.run()
        if resp == gtk.RESPONSE_OK:
            dl_fl = saveas.get_filename()
        saveas.destroy()
        if resp == gtk.RESPONSE_OK:
            dl_dir = saveas.get_current_folder()
            if not self.oc_login_data[1]:
                self.oc_login_data = self.oc_loginBox()
            if not self.oc_login_data[1]:
                print 'No password entered.'
                return 1
            if 'yes' in self.oc_website.login_needed():
                _answer = self.oc_website.login(self.oc_login_data)
                if _answer == 1:
                    print 'Loging failed.'
                    self.oc_login_data = ['', '']
                    return 1
            mythread = threading.Thread(target=self.oc_website.download, args=(
             downloadfrom, dl_dir, dl_fl))
            mythread.start()
            self.on_warn('File succesfully downloaded')
        return

    def oc_loginBox(self):
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK_CANCEL, None)
        dialog.set_title('OpenCores Login')
        dialog.set_markup('Enter your <b>OpenCores log information</b>.')
        login = gtk.Entry()
        password = gtk.Entry()
        login.set_visibility(True)
        password.set_visibility(False)
        hbox1 = gtk.HBox()
        hbox1.pack_start(gtk.Label('Login:          '), False, 5, 5)
        hbox1.pack_end(login)
        hbox2 = gtk.HBox()
        hbox2.pack_start(gtk.Label('Password:'), False, 5, 5)
        hbox2.pack_end(password)
        dialog.format_secondary_markup('This information will be used for <i>temporary identification</i> purposes.')
        dialog.vbox.pack_end(hbox2, True, True, 0)
        dialog.vbox.pack_end(hbox1, True, True, 0)
        dialog.show_all()
        response = dialog.run()
        login_info = ['', '']
        if response == gtk.RESPONSE_CANCEL:
            print 'Exiting.'
        else:
            print 'Request submitted.'
            login_info[0] = login.get_text()
            login_info[1] = password.get_text()
        dialog.destroy()
        return login_info

    def go_back(self, widget, data=None):
        self.browser.go_back()

    def go_forward(self, widget, data=None):
        self.browser.go_forward()

    def go_home(self, widget, data=None):
        _txt = 'http://www.freerangefactory.org/site/pmwiki.php/Main/BootDoc'
        self.browser.open(_txt)

    def load_www(self, widge, data=None):
        url = self.www_adr_bar.get_text()
        try:
            url.index('://')
        except:
            url = 'http://' + url

        self.www_adr_bar.set_text(url)
        self.browser.open(url)

    def update_buttons(self, widget, data=None):
        self.www_adr_bar.set_text(widget.get_main_frame().get_uri())
        self.back_button.set_sensitive(self.browser.can_go_back())
        self.forward_button.set_sensitive(self.browser.can_go_forward())

    def load_progress_amount(self, webview, amount):
        self.progress.set_fraction(amount / 100.0)

    def load_started(self, webview, frame):
        self.progress.set_visible(True)

    def load_finished(self, webview, frame):
        self.progress.set_visible(False)

    def syn_rescroll(self, widget):
        self.vadj.set_value(self.vadj.upper - self.vadj.page_size)
        self.syn_scroller.set_vadjustment(self.vadj)

    def comp_rescroll(self, widget):
        self.comp_vadj.set_value(self.comp_vadj.upper - self.comp_vadj.page_size)
        self.comp_scroller.set_vadjustment(self.comp_vadj)

    def comp_bar_timeout(self, pbobj):
        if self.comp_bar_go:
            self.comp_bar.set_visible(True)
            pbobj.comp_bar.pulse()
        else:
            self.comp_bar.set_visible(False)
        return True

    def destroy_progress(self, widget, data=None):
        gobject.source_remove(self.comp_bar_timer)
        self.comp_bar_timer = 0
        gtk.main_quit()

    def auto_compile_timeout(self, widget):
        if self.chk1.get_active():
            wd = os.path.dirname(os.path.realpath(self.dir_entry.get_text()))
            if directory.src_dir_modified(wd):
                print 'Auto-compiling...'
                self.compileSimulateAction(widget, 'Compile')
            else:
                print '[', time.ctime(), '] No VHDL files were modified. Nothing to do.'
        return True

    def auto_compile_and_simulate_timeout(self, widget):
        if self.chk2.get_active():
            wd = os.path.dirname(os.path.realpath(self.dir_entry.get_text()))
            if directory.src_dir_modified(wd):
                print 'Auto-compiling and simulating...'
                self.compileSimulateAction(widget, 'Compile & Simulate')
            else:
                print '[', time.ctime(), '] No VHDL files were modified. Nothing to do.'
        return True

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('destroy', self.destroy_progress)
        self.window.set_border_width(2)
        self.window.set_size_request(920, 600)
        _txt = 'freerangefactory.org - boot ver. ' + version.boot_version
        self.window.set_title(_txt)
        table = gtk.Table(rows=1, columns=1, homogeneous=False)
        terminal = vte.Terminal()
        terminal.connect('child-exited', lambda term: gtk.main_quit())
        terminal.fork_command()
        colours = [
         (11822, 13364, 13878), (52428, 0, 0),
         (20046, 39578, 1542), (50372, 41120, 0),
         (13364, 25957, 42148), (30069, 20560, 31611),
         (1542, 38944, 39578), (54227, 55255, 53199),
         (21845, 22359, 21331), (61423, 10537, 10537),
         (35466, 58082, 13364), (64764, 59881, 20303),
         (29298, 40863, 53199), (44461, 32639, 43176),
         (13364, 58082, 58082), (61166, 61166, 60652)]
        foreground = gtk.gdk.Color(0, 0, 0)
        background = gtk.gdk.Color(65535, 65535, 65535)
        palette = [ gtk.gdk.Color(*colour) for colour in colours ]
        terminal.set_colors(foreground, background, palette)
        terminal_window = gtk.ScrolledWindow()
        terminal_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        terminal_window.add(terminal)
        vpaned = gtk.VPaned()
        vpaned.pack1(terminal_window, shrink=True)
        vpaned.pack2(table, shrink=True)
        self.window.add(vpaned)
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        table.attach(child=notebook, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xpadding=0, ypadding=0)
        Vbox1 = gtk.VBox(False, 0)
        notebook.append_page(Vbox1, gtk.Label('Compile'))
        self.comp_scroller = gtk.ScrolledWindow()
        self.comp_scroller.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.comp_scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        comp_out = gtk.TextView()
        comp_out.set_left_margin(10)
        comp_out.set_right_margin(10)
        comp_out.set_editable(False)
        self.comp_textbuffer = comp_out.get_buffer()
        self.comp_scroller.add(comp_out)
        _txt = 'For the synthesis of your design select your VHDL top-level ' + 'design file.\nIf you are interested in running a simulation ' + 'of your design, select instead your test-bench file.\n\n' + 'For any addtional help please consult the Help Tab.'
        self.comp_textbuffer.set_text(_txt)
        comp_out.modify_font(pango.FontDescription('monospace 9'))
        self.comp_vadj = self.comp_scroller.get_vadjustment()
        self.comp_vadj.connect('changed', self.comp_rescroll)
        self.dir_entry = gtk.Entry()
        self.dir_entry.set_tooltip_text('Here you select the top-level design file or the test-bench file.\n' + 'The following shortcuts are also available:\n' + 'CTRL-N:  create a new file.\n' + 'CTRL-D:  delete current file.\n')
        self.dir_entry.connect('changed', self.dir_entry_changed)
        self.dir_entry.connect('key-press-event', self.entry_keypress)
        self.img_ind = gtk.Image()
        self.img_ind.set_from_stock(gtk.STOCK_INDEX, gtk.ICON_SIZE_BUTTON)
        btn_ind = gtk.Button()
        btn_ind.add(self.img_ind)
        btn_ind.connect('clicked', self.select_file)
        btn_ind.set_tooltip_text('Select top-level design file or test-bench file.')
        self.btn_compile = gtk.Button('Compile')
        self.btn_compile.connect('clicked', self.compileSimulateAction, 'Compile')
        self.btn_compile.set_tooltip_text('Check and compile your design.')
        Hbox1 = gtk.HBox(False, 0)
        Hbox1.pack_start(btn_ind, False, False, 0)
        Hbox1.pack_start(self.dir_entry, True, True, 0)
        Hbox1.pack_start(self.btn_compile, False, False, 0)
        self.comp_bar = gtk.ProgressBar()
        self.comp_bar.set_text('sleeping')
        self.comp_bar.set_pulse_step(0.04)
        self.comp_bar.set_fraction(0.1)
        self.comp_bar_go = False
        self.comp_bar.set_visible(False)
        self.comp_bar_timer = gobject.timeout_add(100, self.comp_bar_timeout, self)
        Vbox1.pack_start(Hbox1, False, False, 0)
        lb1 = gtk.Label()
        fixed1 = gtk.Fixed()
        lb1.set_use_markup(gtk.TRUE)
        lb1.set_markup('<span size="8000"                         foreground="#B5B2AC">top-level VHDL design file</span>')
        fixed1.put(lb1, 35, 0)
        self.chk1 = gtk.CheckButton('auto')
        self.chk1.set_active(False)
        self.chk1.set_tooltip_text('Automatically compile your design ' + 'every time a vhdl file in "src/" is modified')
        gobject.timeout_add(600, self.auto_compile_timeout, self)
        fixed2 = gtk.Fixed()
        fixed2.put(self.chk1, -70, -1)
        Hbox3 = gtk.HBox(False, 0)
        Hbox3.pack_start(fixed1, False, False, 0)
        Hbox3.pack_end(fixed2, False, False, 0)
        Vbox1.pack_start(Hbox3, False, False, 0)
        Vbox1.pack_start(self.comp_scroller, True, True, 2)
        Vbox1.pack_start(self.comp_bar, False, False, 0)
        self.my_socket = gtk.Socket()
        Vbox2 = gtk.VBox(False, 0)
        notebook.append_page(Vbox2, gtk.Label('Simulate'))
        self.btn_compileAndSimulate = gtk.Button('Compile & Simulate')
        self.btn_compileAndSimulate.connect('clicked', self.compileSimulateAction, 'Compile & Simulate')
        self.btn_compileAndSimulate.set_tooltip_text('Check, compile and simulate your VHDL design.')
        Hbox3 = gtk.HBox(False, 0)
        self.sim_opt_entry = gtk.Entry()
        self.sim_opt_entry.set_tooltip_text('Enter simulation options.')
        self.sim_opt_entry.set_text('--stop-time=200ns')
        sim_opt_label = gtk.Label('Simulation options: ')
        Hbox3.pack_start(sim_opt_label, False, False, 2)
        Hbox3.pack_start(self.sim_opt_entry, True, True, 2)
        Hbox3.pack_end(self.btn_compileAndSimulate, False, False, 2)
        Vbox2.pack_start(Hbox3, False, False, 0)
        self.chk2 = gtk.CheckButton('auto')
        self.chk2.set_active(False)
        self.chk2.set_sensitive(True)
        self.chk2.set_tooltip_text('Automatically compile and simulate your design ' + 'every time a vhdl file in "src/" is modified')
        gobject.timeout_add(600, self.auto_compile_and_simulate_timeout, self)
        fixed3 = gtk.Fixed()
        fixed3.put(self.chk2, -145, -1)
        Hbox4 = gtk.HBox(False, 0)
        Hbox4.pack_end(fixed3, False, False, 0)
        Vbox2.pack_start(Hbox4, False, False, 0)
        Vbox2.pack_start(self.my_socket, True, True, 0)
        self.GTKWAVE_COMM_SOCKET_ID = hex(self.my_socket.get_id())[:-1]
        print 'GtkWave Comm. socket ID:', self.GTKWAVE_COMM_SOCKET_ID
        Hbox_syn1 = gtk.HBox(False, 0)
        Hbox_syn2 = gtk.HBox(False, 0)
        Hbox_syn3 = gtk.HBox(False, 0)
        Hbox_syn4 = gtk.HBox(False, 0)
        Hbox_syn5 = gtk.HBox(False, 0)
        Vbox_syn1 = gtk.VBox(False, 0)
        Vbox_syn1.set_border_width(10)
        self.top_level_label = gtk.Label()
        self.top_level_label.set_tooltip_text('This is your top-level design ' + 'file. You can edit this in the Compile tab.')
        self.tool_path_entry = gtk.Entry()
        self.tool_path_entry.set_tooltip_text('This is the path where the ' + 'synthesis tools are installed.')
        self.tool_command_entry = gtk.Entry()
        self.tool_command_entry.set_tooltip_text('This is the command to ' + 'synthesis your design.')
        Hbox_syn1.pack_start(self.top_level_label, False, False, 3)
        Hbox_syn2.pack_start(gtk.Label('Synthesis tool path setting command: '), False, False, 3)
        Hbox_syn2.pack_start(self.tool_path_entry, True, True, 3)
        Hbox_syn3.pack_start(gtk.Label('Synthesis command: '), False, False, 3)
        Hbox_syn3.pack_start(self.tool_command_entry, True, True, 3)
        Hbox_syn5.pack_start(gtk.Label('Device type: '), False, False, 3)
        self.ma = self.make_dropdown_menu(devices.dev_manufacturer)
        self.fa = self.make_dropdown_menu(devices.dev_family)
        self.de = self.make_dropdown_menu(devices.dev_device)
        self.pa = self.make_dropdown_menu(devices.dev_package)
        self.sp = self.make_dropdown_menu(devices.dev_speed)
        self.ma.set_active(0)
        self.fa.set_active(0)
        self.pa.set_active(4)
        self.sp.set_active(3)
        self.de.set_wrap_width(3)
        self.pa.set_wrap_width(7)
        self.sp.set_wrap_width(2)
        dev_lb1 = gtk.Label()
        dev_fixed = gtk.Fixed()
        dev_lb1.set_use_markup(gtk.TRUE)
        dev_lb1.set_markup('<span size="8000"' + 'foreground="#B5B2AC">' + 'manufacturer' + (' ').join([ ' ' for i in range(22) ]) + 'family' + (' ').join([ ' ' for i in range(30) ]) + 'device' + (' ').join([ ' ' for i in range(30) ]) + 'package' + (' ').join([ ' ' for i in range(28) ]) + 'speed grade </span>')
        dev_fixed.put(dev_lb1, 95, 0)
        self.syn_scroller = gtk.ScrolledWindow()
        self.syn_scroller.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.syn_scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        syn_out = gtk.TextView()
        syn_out.set_left_margin(10)
        syn_out.set_right_margin(10)
        syn_out.set_editable(False)
        self.syn_textbuffer = syn_out.get_buffer()
        self.syn_scroller.add(syn_out)
        self.syn_textbuffer.set_text('ready to go!\n')
        syn_out.modify_font(pango.FontDescription('monospace 9'))
        self.vadj = self.syn_scroller.get_vadjustment()
        self.vadj.connect('changed', self.syn_rescroll)
        Hbox_syn5.pack_start(self.ma, False, False, 3)
        Hbox_syn5.pack_start(self.fa, False, False, 3)
        Hbox_syn5.pack_start(self.de, False, False, 3)
        Hbox_syn5.pack_start(self.pa, False, False, 3)
        Hbox_syn5.pack_start(self.sp, False, False, 3)
        Vbox_syn1.pack_start(Hbox_syn1, False, False, 5)
        separator = gtk.HSeparator()
        Vbox_syn1.pack_start(separator, False, False, 10)
        Vbox_syn1.pack_start(Hbox_syn2, False, False, 5)
        Vbox_syn1.pack_start(Hbox_syn3, False, False, 10)
        Vbox_syn1.pack_start(Hbox_syn5, False, False, 0)
        Vbox_syn1.pack_start(dev_fixed, False, False, 0)
        self.fa.connect('changed', self.filter_dropdown)
        self.filter_dropdown(self.window)
        self.start_stop_syn_button = gtk.Button('Start Synthesis')
        gen_syn_script_button = gtk.Button('Generate Script')
        self.syn_p = None
        self.g_syn_id = None
        self.start_stop_syn_button.connect('clicked', self.syn_button_action, self.start_stop_syn_button.get_label())
        gen_syn_script_button.connect('clicked', self.gen_syn_script_button_action, 'gen_script')
        syn_report_lb = gtk.Label()
        syn_report_lb_fixed = gtk.Fixed()
        syn_report_lb.modify_font(pango.FontDescription('monospace 9'))
        _txt = '<a href="xtclsh_script">xtclsh script</a> ' + '<a href="synthesis_report">synthesis report</a>'
        syn_report_lb.set_markup(_txt)
        syn_report_lb.connect('activate-link', self.open_in_editor)
        syn_report_lb_fixed.put(syn_report_lb, 0, 15)
        self.syn_spinner = gtk.Spinner()
        self.syn_spinner.set_size_request(25, 25)
        Hbox_syn4.pack_start(gen_syn_script_button, False, False, 3)
        Hbox_syn4.pack_start(self.start_stop_syn_button, False, False, 3)
        Hbox_syn4.pack_start(self.syn_spinner, False, False, 3)
        Hbox_syn4.pack_end(syn_report_lb_fixed, False, False, 3)
        Vbox_syn1.pack_start(Hbox_syn4, False, False, 7)
        Vbox_syn1.pack_start(self.syn_scroller, True, True)
        notebook.append_page(Vbox_syn1, gtk.Label('Synthesize'))
        self.oc_scroller = gtk.ScrolledWindow()
        self.oc_browser = webkit.WebView()
        oc_settings = self.oc_browser.get_settings()
        oc_settings.set_property('enable-default-context-menu', True)
        self.oc_browser.connect('load-progress-changed', self.oc_load_progress_amount)
        self.oc_browser.connect('load-started', self.oc_load_started)
        self.oc_browser.connect('load-finished', self.oc_load_finished)
        self.oc_browser.connect('load_committed', self.oc_update_buttons)
        self.oc_browser.connect('download_requested', self.oc_download)
        oc_prj_button = gtk.Button('OpenCores')
        oc_login_button = gtk.Button('Login')
        oc_account_button = gtk.Button('My Account')
        oc_faq_button = gtk.Button('FAQ')
        oc_prj_button.connect('clicked', self.oc_load_www, 'http://opencores.org/projects')
        oc_login_button.connect('clicked', self.oc_load_www, 'http://opencores.org/login')
        oc_account_button.connect('clicked', self.oc_load_www, 'http://opencores.org/acc')
        oc_faq_button.connect('clicked', self.oc_load_www, 'http://opencores.org/faq')
        self.oc_www_adr_bar = gtk.Entry()
        self.oc_www_adr_bar.connect('activate', self.oc_load_www_bar)
        oc_hbox = gtk.HBox()
        oc_vbox = gtk.VBox()
        self.oc_progress = gtk.ProgressBar()
        self.oc_back_button = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.oc_back_button.connect('clicked', self.oc_go_back)
        self.oc_forward_button = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.oc_forward_button.connect('clicked', self.oc_go_forward)
        oc_hbox.pack_start(self.oc_back_button, False, False, 2)
        oc_hbox.pack_start(self.oc_forward_button, False, False)
        oc_hbox.pack_start(oc_prj_button, False, False, 2)
        oc_hbox.pack_start(oc_login_button, False, False, 2)
        oc_hbox.pack_start(oc_account_button, False, False, 2)
        oc_hbox.pack_start(oc_faq_button, False, False, 2)
        oc_hbox.pack_start(self.oc_www_adr_bar, True, True, 2)
        oc_vbox.pack_start(oc_hbox, False, False, 4)
        oc_vbox.pack_start(self.oc_scroller, True, True, 4)
        oc_vbox.pack_end(self.oc_progress, False, False, 4)
        self.oc_scroller.add(self.oc_browser)
        notebook.append_page(oc_vbox, gtk.Label('OpenCores'))
        self.oc_back_button.set_sensitive(False)
        self.oc_forward_button.set_sensitive(False)
        scroller = gtk.ScrolledWindow()
        self.browser = webkit.WebView()
        self.browser.connect('load-progress-changed', self.load_progress_amount)
        self.browser.connect('load-started', self.load_started)
        self.browser.connect('load-finished', self.load_finished)
        self.browser.connect('load_committed', self.update_buttons)
        self.www_adr_bar = gtk.Entry()
        self.www_adr_bar.connect('activate', self.load_www)
        hlp_hbox = gtk.HBox()
        hlp_vbox = gtk.VBox()
        self.progress = gtk.ProgressBar()
        self.back_button = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.back_button.connect('clicked', self.go_back)
        self.forward_button = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.forward_button.connect('clicked', self.go_forward)
        home_button = gtk.ToolButton(gtk.STOCK_HOME)
        home_button.connect('clicked', self.go_home)
        hlp_hbox.pack_start(self.back_button, False, False, 0)
        hlp_hbox.pack_start(self.forward_button, False, False)
        hlp_hbox.pack_start(home_button, False, False)
        hlp_hbox.pack_start(self.www_adr_bar, True, True)
        hlp_vbox.pack_start(hlp_hbox, False, False, 5)
        hlp_vbox.pack_start(scroller, True, True)
        hlp_vbox.pack_start(self.progress, False, False, 5)
        scroller.add(self.browser)
        notebook.append_page(hlp_vbox, gtk.Label('Help'))
        self.back_button.set_sensitive(False)
        self.forward_button.set_sensitive(False)
        check_updates_button = gtk.Button('Check for Updates')
        set_default_button = gtk.Button('Set Default')
        _txt = 'Reset boot to its default configuration.'
        self.set_default_button_label = gtk.Label(_txt)
        pr_Hbox1 = gtk.HBox(False, 0)
        pr_Hbox2 = gtk.HBox(False, 0)
        pr_Hbox1.pack_start(check_updates_button, False, False, 7)
        pr_Hbox2.pack_start(set_default_button, False, False, 7)
        pr_Hbox2.pack_start(self.set_default_button_label, False, False, 2)
        self.update_boot_msg = gtk.Label('')
        pr_Hbox1.pack_start(self.update_boot_msg, False, False, 7)
        pr_Vbox1 = gtk.VBox(False, 0)
        pr_Vbox1.pack_start(pr_Hbox1, False, False, 7)
        pr_Vbox1.pack_start(pr_Hbox2, False, False, 7)
        notebook.append_page(pr_Vbox1, gtk.Label('Preferences'))
        check_updates_button.connect('clicked', self.check_for_new_ver)
        set_default_button.connect('clicked', self.set_default_boot)
        check_updates_button.set_tooltip_text('Download a new version of boot')
        set_default_button.set_tooltip_text('Set boot to its default status')
        wd = os.getcwd()
        vhdl_files = glob.glob(os.path.join(wd, '*.vhd')) + glob.glob(os.path.join(wd, '*.vhdl'))
        new_wd = os.path.join(os.getcwd(), 'src')
        if os.path.isdir(new_wd):
            wd = new_wd
            vhdl_files = []
            new_vhdl_files = glob.glob(os.path.join(wd, '*.vhd')) + glob.glob(os.path.join(wd, '*.vhdl'))
            if len(new_vhdl_files) != 0:
                vhdl_files = new_vhdl_files
        print 'Current working directory:', wd
        self.dir_entry.set_text(wd)
        if len(vhdl_files) != 0:
            best_guess_vhdl_file = os.path.join(wd, vhdl_files[(-1)])
            self.dir_entry.set_text(best_guess_vhdl_file)
            possible_vhdl_top = glob.glob(os.path.join(wd, '*_top.vhd')) + glob.glob(os.path.join(wd, '*_top.vhdl'))
            if len(possible_vhdl_top) != 0:
                self.dir_entry.set_text(os.path.join(wd, possible_vhdl_top[0]))
            possible_vhdl_tb = glob.glob(os.path.join(wd, '*_tb.vhd')) + glob.glob(os.path.join(wd, '*_tb.vhdl'))
            if len(possible_vhdl_tb) != 0:
                self.dir_entry.set_text(os.path.join(wd, possible_vhdl_tb[0]))
        _txt = 'http://www.freerangefactory.org/site/pmwiki.php/Main/BootDoc'
        default_www = _txt
        self.www_adr_bar.set_text(default_www)
        self.browser.open(default_www)
        self.top_level_label.set_text('Top-level design: ' + self.dir_entry.get_text())
        _txt = directory.guess_xilinx_ise_path()
        self.tool_path_entry.set_text(_txt)
        self.tool_command_entry.set_text('Not set')
        self.load_local_configuration_file()
        self.window.show_all()
        self.comp_bar.set_visible(False)
        oc_default_www = 'http://opencores.org/projects'
        self.oc_www_adr_bar.set_text(oc_default_www)
        self.oc_browser.open(oc_default_www)
        self.oc_login_data = [
         '', '']
        self.oc_website = opencores.open_cores_website()
        return