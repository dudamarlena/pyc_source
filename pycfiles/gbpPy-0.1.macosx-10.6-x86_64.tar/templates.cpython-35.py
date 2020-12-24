# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python3.5/site-packages/gbpPy/templates.py
# Compiled at: 2018-01-18 01:22:07
# Size of source mod 2**32: 24343 bytes
import gbpPy.log as SID, shutil, os, re, filecmp

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def check_and_remove_trailing_occurance(txt_in, occurance):
    n_occurance = len(occurance)
    if txt_in[-n_occurance:] == occurance:
        txt_out = txt_in[0:-n_occurance]
        flag_found = True
    else:
        txt_out = txt_in
        flag_found = False
    return (
     txt_out, flag_found)


def get_base_name(project_dir_abs):
    head, tail = os.path.split(project_dir_abs)
    if tail == '':
        head, tail = os.path.split(head)
    return tail


_protected_inputs = [
 '_PARAMETERS.key', '_PARAMETERS.value']

class project_inputs:

    def __init__(self, user_params):
        self.list = []
        self.list.append({'name': '_PARAMETERS.key', 'input': [key for key in user_params.keys()]})
        self.list.append({'name': '_PARAMETERS.value', 'input': [val for val in user_params.values()]})
        for input_name_i in _protected_inputs:
            input_check = self.get_input(input_name_i)
            if not input_check:
                SID.error('Failed to add protected input {%s} to the project parameter list.' % input_name_i)

        for param_i_key, param_i_value in user_params.items():
            if hasattr(param_i_value, '__iter__') and not isinstance(param_i_value, str):
                self.list.append({'name': param_i_key, 'input': param_i_value})
            else:
                self.list.append({'name': param_i_key, 'input': [param_i_value]})

    def get_input(self, name_get):
        input_return = None
        for input_i in self.list:
            if input_i['name'] == name_get:
                input_return = input_i
                break

        return input_return

    def get_value(self, name_get, idx=0):
        input_get = self.get_input(name_get)
        if not input_get:
            SID.error('Failed to find requested parameter {%s} in project parameter list.' % name_get)
        if abs(idx) >= len(input_get):
            SID.error('Requested input index {%d} exceeds allowed bounds of paramerer {%s; size=%d}.' % (idx, name_get, size(input_get)))
        return input_get[idx]


def find_parameter_references(line):
    regex = re.compile('%[\\w:.]*%')
    matches = []
    for match in regex.finditer(line):
        param = {}
        directive = match.group().strip('%')
        if directive not in _protected_inputs:
            param['name'] = directive
            param['span'] = match.span()
            matches.append(param)

    return matches


def _perform_parameter_substitution_ith(line, params, idx=None):
    line_new = line
    regex = re.compile('%[\\w:.]*%')
    match = regex.search(line_new)
    n_lines = 1
    while match:
        directive = match.group().strip('%')
        param_insert = params.get_input(directive)
        param_insert_size = len(param_insert['input'])
        if param_insert_size > 1:
            if n_lines == 1:
                n_lines = param_insert_size
            else:
                if param_insert_size != 1 and n_lines != param_insert_size:
                    SID.error('There is an input list size incompatibility (%d!=%d) in {%s}.' % (n_lines, param_insert_size, line))
                if idx == None:
                    line_new = line_new[0:match.start()] + str(param_insert['input'][0]) + line_new[match.end():]
                else:
                    line_new = line_new[0:match.start()] + str(param_insert['input'][idx]) + line_new[match.end():]
            match = regex.search(line_new)

    if idx == None:
        return (n_lines, line_new)
    else:
        return line_new


def perform_parameter_substitution(line, params):
    n_lines, line_new = _perform_parameter_substitution_ith(line, params)
    lines_new = []
    if n_lines > 1:
        for idx in range(n_lines):
            lines_new.append(_perform_parameter_substitution_ith(line, params, idx=idx))

    else:
        lines_new.append(line_new)
    return lines_new


def format_template_names(name_list):
    name_txt = ''
    for i_name, name_i in enumerate(name_list):
        if i_name == 0:
            name_txt += name_i
        else:
            name_txt += ',' + name_i

    return name_txt


def update_element(element, update):
    return update == None or update == element.template_path_out()


class template_directory:

    def __init__(self, dirname_template, dirname):
        if not os.path.isdir(dirname):
            raise IsADirectoryError('Directory name {%s} passed to template_directory constructor does not point to a valid directory.' % dirname)
        dirname_rel_template = os.path.normpath(os.path.relpath(os.path.abspath(dirname), dirname_template))
        self.parse_name(dirname_rel_template)
        self._template_path = os.path.normpath(os.path.dirname(dirname_rel_template))
        self._full_path_in_abs = os.path.abspath(dirname)
        self.files = []
        self.dirname_template = dirname_template
        if os.path.islink(dirname):
            self.is_symlink = True
        else:
            self.is_symlink = False

    def parse_name(self, dirname_rel_template):
        self.name_in = os.path.basename(dirname_rel_template)
        self.name_out = self.name_in.replace('_dot_', '.', 1)
        self.name_out, self.is_link = check_and_remove_trailing_occurance(self.name_out, '.link')

    def is_root(self):
        return os.path.realpath(self.full_path_in()) == os.path.realpath(self.dirname_template)

    def full_path_in(self):
        return os.path.normpath(self._full_path_in_abs)

    def full_path_out(self, dir_install):
        return os.path.normpath(os.path.normpath(os.path.join(dir_install, self._template_path, self.name_out)))

    def template_path_in(self):
        return os.path.normpath(os.path.join(self._template_path, self.name_in))

    def template_path_out(self):
        return os.path.normpath(os.path.join(self._template_path, self.name_out))

    def install(self, dir_install, silent=False):
        try:
            if not self.is_root():
                if os.path.isdir(self.full_path_out(dir_install)):
                    SID.log.open('Directory %s exists.' % self.full_path_out(dir_install))
                else:
                    if self.is_link:
                        symlink_path = os.path.relpath(self.full_path_in(), os.path.dirname(self.full_path_out(dir_install)))
                    if not silent:
                        if self.is_link:
                            if os.path.lexists(self.full_path_out(dir_install)):
                                os.unlink(self.full_path_out(dir_install))
                                os.symlink(symlink_path, self.full_path_out(dir_install))
                                SID.log.open('Directory %s link updated.' % self.full_path_out(dir_install))
                            else:
                                os.symlink(symlink_path, self.full_path_out(dir_install))
                                SID.log.open('Directory %s linked.' % self.full_path_out(dir_install))
                        else:
                            os.mkdir(self.full_path_out(dir_install))
                            SID.log.open('Directory %s created.' % self.full_path_out(dir_install))
                    else:
                        if self.is_link:
                            SID.log.open('Directory %s linked silently.' % self.full_path_out(dir_install))
                        else:
                            SID.log.open('Directory %s created silently.' % self.full_path_out(dir_install))
            else:
                if os.path.isdir(self.full_path_out(dir_install)):
                    SID.log.open('Directory %s -- root valid.' % self.full_path_out(dir_install))
                else:
                    raise NotADirectoryError
        except:
            SID.log.error('Failed to install directory {%s}.' % self.full_path_out())

    def uninstall(self, dir_install, silent=False):
        try:
            if not self.is_root():
                if not os.path.isdir(self.full_path_out(dir_install)):
                    SID.log.close('Not found.')
                else:
                    if not silent:
                        if self.is_link:
                            os.unlink(self.full_path_out(dir_install))
                            SID.log.close('Unlinked.')
                        else:
                            os.rmdir(self.full_path_out(dir_install))
                            SID.log.close('Removed.')
                    else:
                        if self.is_link:
                            SID.log.close('Unlinked silently.')
                        else:
                            SID.log.close('Removed silently.')
            else:
                SID.log.close('Root ignored.')
        except:
            SID.log.error('Failed to uninstall directory {%s}.' % self.name_out)


class template_file:

    def __init__(self, filename, dir_host):
        if not dir_host:
            dir_host = template_directory('.')
        self.parse_name(filename)
        self.dir_in = dir_host
        if not os.path.isfile(self.full_path_in()):
            raise FileNotFoundError('File name {%s} passed to template_file constructor does not point to a valid file.' % self.full_path_in())
        if os.path.islink(filename):
            self.is_symlink = True
        else:
            self.is_symlink = False

    def parse_name(self, filename):
        self.name_in = filename
        self.name_out = self.name_in.replace('_dot_', '.', 1)
        self.name_out, self.is_link = check_and_remove_trailing_occurance(self.name_out, '.link')
        if not self.is_link:
            self.name_out, self.is_template = check_and_remove_trailing_occurance(self.name_out, '.template')
        else:
            self.is_template = False

    def full_path_in(self):
        return os.path.normpath(os.path.join(self.dir_in.full_path_in(), self.name_in))

    def full_path_out(self, dir_install):
        return os.path.normpath(os.path.join(self.dir_in.full_path_out(dir_install), self.name_out))

    def template_path_in(self):
        return os.path.normpath(os.path.join(self.dir_in.template_path_in(), self.name_in))

    def template_path_out(self):
        return os.path.normpath(os.path.join(self.dir_in.template_path_out(), self.name_out))

    def install(self, dir_install, params=None, silent=False):
        project_params = project_inputs(params)
        try:
            if os.path.isfile(self.full_path_out(dir_install)):
                SID.log.comment('   --> %s exists.' % self.full_path_out(dir_install))
            else:
                if self.is_link:
                    symlink_path = os.path.relpath(self.full_path_in(), self.dir_in.full_path_out(dir_install))
                if not silent:
                    if self.is_link:
                        if os.path.lexists(self.full_path_out(dir_install)):
                            os.unlink(self.full_path_out(dir_install))
                            os.symlink(symlink_path, self.full_path_out(dir_install))
                            SID.log.comment('--> %s link updated.' % self.full_path_out(dir_install))
                        else:
                            os.symlink(symlink_path, self.full_path_out(dir_install))
                            SID.log.comment('--> %s linked.' % self.full_path_out(dir_install))
                    else:
                        self.write_with_substitution(dir_install, params=project_params)
                        SID.log.comment('--> %s created.' % self.full_path_out(dir_install))
                else:
                    if self.is_link:
                        SID.log.comment('--> %s linked silently.' % self.full_path_out(dir_install))
                    else:
                        SID.log.comment('--> %s created silently.' % self.full_path_out(dir_install))
        except:
            SID.log.error('Failed to install file {%s}.' % self.full_path_out(dir_install))

    def uninstall(self, dir_install, silent=False):
        try:
            if not os.path.isfile(self.full_path_out(dir_install)):
                SID.log.comment('--> %s not found.' % self.full_path_out(dir_install))
            else:
                if not silent:
                    if self.is_link:
                        os.unlink(self.full_path_out(dir_install))
                        SID.log.comment('--> %s unlinked.' % self.full_path_out(dir_install))
                    else:
                        os.remove(self.full_path_out(dir_install))
                        SID.log.comment('--> %s removed.' % self.full_path_out(dir_install))
                else:
                    if self.is_link:
                        SID.log.comment('--> %s unlinked silently.' % self.full_path_out(dir_install))
                    else:
                        SID.log.comment('--> %s removed silently.' % self.full_path_out(dir_install))
        except:
            SID.log.error('Failed to uninstall file {%s}.' % self.full_path_out(dir_install))

    def write_with_substitution(self, dir_install, params=None):
        try:
            if self.is_link:
                os.symlink(os.path.relpath(self.full_path_in(), os.path.dirname(self.full_path_out(dir_install))), self.full_path_out(dir_install))
            elif self.is_template:
                with open(self.full_path_in(), 'r') as (fp_in):
                    with open(self.full_path_out(dir_install), 'w') as (fp_out):
                        for line_in in fp_in:
                            for line_out in perform_parameter_substitution(line_in, params):
                                fp_out.write(line_out)

            else:
                shutil.copy2(self.full_path_in(), self.full_path_out(dir_install))
        except:
            SID.log.error('Failed write template file {%s}.' % self.name_in)


class template:

    def __init__(self, template_name=None, path=None):
        self.path = []
        self.dir = []
        self.name = []
        self.directories = []
        if template_name != None:
            self.add(template_name, path=path)

    def add(self, template_name, path=None):
        if not path:
            path = os.environ.get('GBPPY_TEMPLATE_PATH')
        if not path:
            path = './templates/'
        path_list = path.split(':')
        template_dir_abs = None
        for path_i in path_list:
            dir_test = os.path.join(path_i, template_name)
            if os.path.isdir(dir_test):
                template_dir_abs = dir_test
                break

        if not template_dir_abs:
            raise IsADirectoryError("Could not find template '%s' in template path {%s}" % (template_name, path))
        template_path_dir, template_name = os.path.split(template_dir_abs)
        self.path.append(template_path_dir)
        self.dir.append(template_dir_abs)
        self.name.append(template_name)
        SID.log.open("Loading template {'%s' from %s}..." % (self.name[(-1)], self.path[(-1)]))
        n_template_files = 0
        for root, dirs, files in os.walk(self.dir[(-1)]):
            dir_new = template_directory(self.dir[(-1)], root)
            self.add_directory(dir_new)
            for test_dir_i in os.listdir(root):
                test_dir = os.path.join(dir_new.full_path_in(), test_dir_i)
                if os.path.islink(test_dir) and os.path.isdir(test_dir):
                    self.add_directory(template_directory(self.dir[(-1)], test_dir))

            for file_i in files:
                file_new = template_file(file_i, dir_new)
                if file_new.is_template:
                    n_template_files += 1
                self.add_file(file_new)

        if n_template_files > 0:
            SID.log.open('Scanning template files for parameters...')
            self.params = set()
            for dir_i in self.directories:
                for file_i in [f for f in dir_i.files if f.is_template]:
                    with open(file_i.full_path_in(), 'r') as (file_in):
                        for line in file_in:
                            param_refs = find_parameter_references(line)
                            for param_ref_i in param_refs:
                                self.params.add(param_ref_i['name'])

            SID.log.close('Done')
        self.print()
        SID.log.close('Done')

    def get_directory(self, template_path_out):
        for dir_i in self.directories:
            if dir_i.template_path_out() == template_path_out:
                return dir_i

    def get_file(self, template_path_out):
        for dir_i in self.directories:
            for file_i in dir_i.files:
                if file_i.template_path_out() == template_path_out:
                    return file_i

    def add_directory(self, dir_add):
        dir_check = self.get_directory(dir_add.template_path_out())
        if dir_check == None:
            self.directories.append(dir_add)

    def add_file(self, file_add):
        if file_add.dir_in.is_symlink:
            raise Exception('Can not add file {%s} to symlinked directory {%s}.' % (file_add.name_in, file_add.dir_in.name_in))
        dir_check = self.get_directory(file_add.dir_in.template_path_out())
        if dir_check == None:
            dir_out = file_add.dir_in
        else:
            dir_out = dir_check
        file_check = self.get_file(file_add.template_path_out())
        if file_check != None:
            if not filecmp.cmp(file_add.full_path_in(), file_check.full_path_in()):
                SID.log.error("There is a file incompatability between template files '%s' and '%s'." % (file_add.full_path_in(), file_check.full_path_in()))
        if file_check == None:
            dir_out.files.append(file_add)

    def n_files(self):
        n_files = 0
        for dir_i in self.directories:
            n_files += len(dir_i.files)

        return n_files

    def print(self):
        SID.log.open('Template contents:')
        SID.log.comment('n_directories=%d' % len(self.directories))
        SID.log.comment('n_files      =%d' % self.n_files())
        SID.log.comment('n_parameters =%d' % len(self.params))
        for param_ref_i in self.params:
            SID.log.comment('   --> %s' % param_ref_i)

        for dir_i in sorted(self.directories, key=lambda dir_j: len(dir_j.template_path_out())):
            SID.log.open('Directory {%s}:' % dir_i.template_path_out())
            for file_i in sorted(dir_i.files, key=lambda file_j: file_j.template_path_out()):
                SID.log.comment('--> %s' % file_i.template_path_out())

            SID.log.close()

        SID.log.close()

    def _process_template(self, dir_install, params=None, uninstall=False, silent=False, update=None):
        name_txt = format_template_names(self.name)
        if not uninstall:
            if len(self.name) > 1:
                SID.log.open('Installing templates {%s} to {%s}...' % (name_txt, dir_install))
            else:
                SID.log.open('Installing template {%s} to {%s}...' % (name_txt, dir_install))
            flag_reverse_sort = False
        else:
            flag_reverse_sort = True
            if len(self.name) > 1:
                SID.log.open('Uninstalling templates {%s} from {%s}...' % (name_txt, dir_install))
            else:
                SID.log.open('Uninstalling template {%s} from {%s}...' % (name_txt, dir_install))
        for dir_i in sorted(self.directories, key=lambda k: len(k._full_path_in_abs), reverse=flag_reverse_sort):
            if not uninstall and update_element(dir_i, update):
                dir_i.install(dir_install, silent=silent)
            elif update_element(dir_i, update):
                SID.log.open('Uninstalling directory %s...' % dir_i.full_path_out(dir_install))
            for file_i in dir_i.files:
                if uninstall and update_element(file_i, update):
                    file_i.uninstall(dir_install, silent=silent)
                elif update_element(file_i, update):
                    file_i.install(dir_install, params=params, silent=silent)

            if uninstall and update_element(dir_i, update):
                dir_i.uninstall(dir_install, silent=silent)
            elif update_element(dir_i, update):
                SID.log.close()

        SID.log.close('Done.')

    def install(self, dir_out, params=None, silent=False, update=None):
        for param_i in self.params:
            if param_i not in params:
                SID.log.error('Required parameter {%s} is not present in template installation dictionary.' % param_i)

        self._process_template(dir_out, params=params, silent=silent, update=update)

    def uninstall(self, dir_out, silent=False, update=None):
        self._process_template(dir_out, uninstall=True, silent=silent, update=update)