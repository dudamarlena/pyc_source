# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\lib_common.py
# Compiled at: 2018-05-08 17:51:36
import os, sys, fnmatch, shutil, datetime, ipaddress, lib_logger
logger = lib_logger.logger()

def arg_passing(default_arg_dict={}):
    arg_dict = {}
    for key, value in default_arg_dict.iteritems():
        arg_dict[key] = value

    f_arg_index = 0
    for n in range(1, len(sys.argv)):
        if '=' not in sys.argv[n]:
            arg_dict[f_arg_index] = sys.argv[n]
            f_arg_index += 1
            continue
        if len(sys.argv[n]) < 3:
            continue
        test_list = sys.argv[n].split('=')
        flag = test_list[1]
        if flag == '1':
            flag = True
        elif flag == '0':
            flag = False
        arg_dict[test_list[0]] = flag

    return arg_dict


def count_down(op, max=1, current=0, text='Processing '):
    if op == 'count':
        x = int(100.0 * (float(current) / float(max)))
        print '%s [%d%%]\r' % (text, x),
    else:
        print '%s [100%%]\r' % text


def find_all(name, path, file=True, dir=False, depth=0):
    result = []
    current_depth = 0
    for dirname, dirs, files in os.walk(path):
        current_depth += 1
        if file:
            if name in files or name == '':
                result.append(os.path.join(dirname, name))
        if dir:
            for dirName in dirs:
                if name in dirName or name == '':
                    result.append(dirName)

        if depth > 0:
            if current_depth >= depth:
                break

    return result


def find_first_dir(name, path):
    result = []
    for dirname, dirs, files in os.walk(path):
        if name[-1:] == '/':
            against = dirs
            check_name = name[:-1]
        else:
            against = files
            check_name = name
        if check_name in against:
            result = dirname.replace('\\', '/')
            break

    return result


def delete_dir_content(path):
    filename = []
    foldername = []
    for dirname, dirs, files in os.walk(path):
        for name in files:
            filename.append(os.path.join(dirname, name))

        for folder in dirs:
            foldername.append(os.path.join(dirname, folder))

    for f in filename[0:]:
        logger.log('debug', 'Deleting file: %s' % f)
        try:
            os.remove(f)
        except:
            logger.log('warning', 'File/"%s/" could not be deleted. Close it if open and retry...' % f)
            continue

    for d in foldername[0:]:
        logger.log('debug', 'Deleting folder: %s' % d)
        try:
            shutil.rmtree(d)
        except:
            logger.log('error', 'Folder"%s" could not be deleted. Close it if open and retry...' % d)
            continue


def find_file(root_dir, and_list=[], not_list=[]):
    tmp_list = []
    include_list = []
    new_and_list = []
    new_not_list = []
    for pattern in and_list:
        new_and_list.append('*' + pattern + '*')

    for pattern in not_list:
        new_not_list.append('*' + pattern + '*')

    for root, dirs, files in os.walk(root_dir):
        for f in files:
            fullpath = os.path.join(root, f)
            if new_not_list != []:
                if not any(fnmatch.fnmatch(f, '*' + pattern + '*') for pattern in new_not_list):
                    tmp_list.append(fullpath)
            else:
                tmp_list.append(fullpath)

    if new_and_list != []:
        for pathname in tmp_list:
            path, f = os.path.split(pathname)
            if all(fnmatch.fnmatch(f, pattern) for pattern in new_and_list):
                include_list.append(path + '/' + f)

    else:
        include_list = tmp_list
    return include_list


def get_file_path_name_extension(pathname):
    path = os.path.dirname(pathname)
    namext = os.path.basename(pathname)
    name = os.path.splitext(namext)[0]
    ext = os.path.splitext(namext)[1]
    return (path, name, ext)


def hhmmss(secs_duration):
    dseconds = datetime.timedelta(0, int(round(secs_duration)), 0)
    days, seconds = dseconds.days, dseconds.seconds
    hours = days * 24 + seconds // 3600
    minutes = seconds % 3600 // 60
    seconds = seconds % 60
    return str(hours) + ':' + str(minutes) + ':' + str(seconds)


run_time_stamp = ''

def time_stamp(action):
    global run_time_stamp
    if action == 'GET':
        if run_time_stamp == '':
            run_time_stamp = ('{:%m%d%y_%H%M%S}').format(datetime.datetime.now())
            logger.log('debug', 'Getting new time stamp: %s' % run_time_stamp)
    elif action == 'RESET':
        logger.log('debug', 'Resetting time stamp.')
        run_time_stamp = ''
        run_time_stamp = ('{:%m%d%y_%H%M%S}').format(datetime.datetime.now())
        logger.log('debug', 'Getting new time stamp after reset: %s' % run_time_stamp)
    else:
        logger.log('warning', 'Invalid time stamp action: %s' % action)
        if run_time_stamp == '':
            run_time_stamp = ('{:%m%d%y_%H%M%S}').format(datetime.datetime.now())
    return run_time_stamp


def time_stamp_lexi_order(MMDDYY_hhmmss):
    ts_split = MMDDYY_hhmmss.split('_')
    YY = ts_split[0][-2:]
    YYMMDD = YY + ts_split[0][:-2]
    hhmmss = ts_split[1]
    YYMMDD_hhmmss = YYMMDD + '_' + hhmmss
    return YYMMDD_hhmmss


def time_stamp_natural_order(YYMMDD_hhmmss):
    ts_split = YYMMDD_hhmmss.split('_')
    YY = ts_split[0][:2]
    YYMMDD = ts_split[0][2:] + YY
    hhmmss = ts_split[1]
    MMDDYY_hhmmss = YYMMDD + '_' + hhmmss
    return MMDDYY_hhmmss


def build_filename(part_list, extension='.txt', timeStamp='y'):
    logger.log('debug', 'part_list=%s, extension=%s' % (part_list, extension))
    filename = ''
    logger.log('debug', 'part_list = %s' % part_list)
    for part in part_list:
        if filename != '':
            filename += '_'
        logger.log('debug', 'part = %s' % part)
        if part == '':
            continue
        if len(part.split()) != 1:
            part = part.replace('.', '_')
        part = part.replace(' ', '_')
        part = part.replace(':', '')
        if '.' in part:
            part_list = part.split('.')
            part = part_list[0]
            extension = '.' + part_list[1]
        filename = filename + part

    if timeStamp == 'y':
        filename = filename + '_' + time_stamp('GET')
    elif timeStamp == 'n':
        filename = filename
    else:
        filename = filename + '_' + timeStamp
    filename = filename + extension
    filename = filename.replace('/', '')
    filename = filename.replace('\\', '')
    return filename


def create_file_from_list(pathname, list):
    fh = open(pathname, 'w')
    for line in list:
        line = normalize_newlines(line)
        if '\n' in line:
            fh.write(line)
        else:
            fh.write(line + '\n')

    fh.close()


def enter_before_exit(confirm=False, silent=False, Kinterrupt=False, exit_message='', option_dict={}):
    if silent:
        logger.log('warning', 'Exiting process ... %s' % exit_message)
        os._exit(0)
    if Kinterrupt:
        print 'Exiting ... %s' % exit_message
        os._exit(0)
    if confirm:
        try:
            reply = raw_input('Confirm exit (y/n): ')
        except (KeyboardInterrupt, EOFError):
            os._exit(0)

        if reply != 'y':
            return
    exit_string = '\nPress [Enter] to exit...'
    raw_input(exit_string)
    os._exit(0)


def normalize_newlines(string):
    return string.replace('\r\n', '\n').replace('\n\r', '\n').replace('\n\n', '\n').replace('\r', '\n')


def normalize_text_file(filename):
    fh = open(filename, 'r+')
    full_content = fh.read()
    full_content = normalize_newlines(full_content)
    fh.close()
    fh = open(filename, 'w')
    fh.write(full_content)
    fh.close()


def name_valid(name, pattern_list_of_lists):
    for pattern_list in pattern_list_of_lists:
        check = False
        for pattern in pattern_list:
            if pattern in name:
                check = True

        if check == False:
            return False

    return check


def generate_dict_key(command):
    key = ''
    cmd_words = command.split()
    for n in range(0, len(cmd_words)):
        key = key + cmd_words[n]
        if n < len(cmd_words) - 1:
            key += '_'

    return key


def cmd_key_match(key, word_str):
    word_list = word_str.split()
    for word in word_list:
        if word not in key:
            return False

    for key_i in key.split('_'):
        if key_i not in word_str:
            return False

    return True


def prompt_processing(prompt_, list=[], return_=False, quit_proc=True, test=False):
    if type(prompt_).__name__ == 'list' and type(prompt_[0]).__name__ == 'str':
        prompt = prompt_[0]
    else:
        if type(prompt_).__name__ == 'str' or type(prompt_).__name__ == 'unicode':
            prompt = prompt_
        else:
            logger.log('warning', 'Invalid prompt %s. Valid type are only "string" of "list" of string' % prompt_)
            return
        if '(y/n):' not in prompt and '(y/n/b):' not in prompt and '(y/q):' not in prompt and '(y/b):' not in prompt and '(y/q/b):' not in prompt and '(y/n/q):' not in prompt and '(y/n/q/b):' not in prompt and '(y/s):' not in prompt and '(y/s/b):' not in prompt and '(y/s/q):' not in prompt and '(y/s/q/b):' not in prompt and '(y/n/s):' not in prompt and '(y/n/s/b):' not in prompt and '[enter]' not in prompt.lower() and ':' != prompt[-1:] and ': ' != prompt[-2:]:
            print prompt
            return 'yes'
        if test and list == []:
            print prompt
            if '[enter]' in prompt.lower():
                return True
            return 'yes'
        if len(list) > 0:
            n_quit = 'no'
            quit_option = ''
            for n_idx in range(0, len(list)):
                if 'quit' in list[n_idx]:
                    n_quit = n_idx + 1
                    quit_option = ' or quit'
                    break

            print prompt
            cat = 'an'
            while True:
                print ''
                for index, item in enumerate(list):
                    print '%6s: %s' % (index + 1, item)
                    prompt = '\nEnter %s option %s%s: ' % (cat, [ n + 1 for n in range(0, len(list)) if n + 1 != n_quit ], quit_option)

                try:
                    option = raw_input(prompt)
                except (KeyboardInterrupt, EOFError) as e:
                    enter_before_exit(Kinterrupt=True, exit_message=e)

                valid_option = [ str(n) for n in range(1, int(index) + 2) ]
                if option == '' and return_:
                    return ''
                if option == str(n_quit):
                    print '\nTo exit the word "quit" must be entered'
                    continue
                if option == 'quit' and n_quit != 0:
                    enter_before_exit(confirm=True)
                    continue
                if option not in valid_option:
                    cat = 'a valid'
                    continue
                break

            return list[(int(option) - 1)]
        if '[enter]' in prompt.lower():
            if test:
                return True
            while True:
                try:
                    any_input = raw_input(prompt)
                except (KeyboardInterrupt, EOFError) as e:
                    enter_before_exit(Kinterrupt=True, exit_message=e)

                if any_input == 'quit':
                    enter_before_exit()
                return any_input

        reply_list = []
        if '(y/n):' in prompt:
            reply_list = ['y', 'n']
        elif '(y/q):' in prompt:
            reply_list = ['y', 'q']
        elif '(y/n/q):' in prompt:
            reply_list = ['y', 'n', 'q']
        elif '(y/n/s):' in prompt:
            reply_list = ['y', 'n', 's']
        elif '(y/s):' in prompt:
            reply_list = ['y', 's']
        elif '(y/b):' in prompt:
            reply_list = ['y', 'b']
        elif '(y/s/q):' in prompt:
            reply_list = ['y', 's', 'q']
        elif '(y/n/b):' in prompt:
            reply_list = ['y', 'n', 'b']
        elif '(y/q/b):' in prompt:
            reply_list = ['y', 'q', 'b']
        elif '(y/n/q/b):' in prompt:
            reply_list = ['y', 'n', 'q', 'b']
        elif '(y/n/s/b):' in prompt:
            reply_list = ['y', 'n', 's', 'b']
        elif '(y/s/b):' in prompt:
            reply_list = ['y', 's', 'b']
        elif '(y/s/q/b):' in prompt:
            reply_list = ['y', 's', 'q', 'b']
        elif ':' in prompt:
            reply_list = [':']
        else:
            logger.log('warning', 'Invalid prompt. Must include one of [:, (y/n):, (y/q):, (y/n/q):, (y/n/s):, (y/s):, (y/b):, (y/s/q):, (y/n/b):, (y/q/b):, (y/n/q/b):, (y/n/s/b):, (y/s/b):, (y/s/q/b):]')
            print prompt
            return
        logger.log('info', 'Prompt message with %s' % reply_list)
        confirm = False
        while True:
            answer = ''
            if len(reply_list) > 0:
                try:
                    answer = raw_input(prompt)
                except (KeyboardInterrupt, EOFError) as e:
                    enter_before_exit(Kinterrupt=True, exit_message=e)

                lower_answer = answer.lower()
                if answer == 'quit':
                    lower_answer = 'q'
                logger.log('info', 'answer=%s lower_answer=%s' % (lower_answer, answer))
                if lower_answer in ('y', 'ye', 'yes'):
                    reply = ['y', 'yes']
                else:
                    if lower_answer in ('n', 'no'):
                        reply = ['n', 'no']
                    elif lower_answer in ('s', 'skip'):
                        reply = ['s', 'skip']
                    elif lower_answer in ('b', 'bypass'):
                        reply = ['b', 'bypass']
                    elif lower_answer == 'q':
                        reply = ['q']
                    elif reply_list == [':']:
                        reply = ['']
                    else:
                        print 'Enter a valid reply [%s].' % answer
                        continue
                    if reply[0] not in reply_list and ':' not in reply_list and answer != 'quit':
                        print 'Invalid reply, try again...'
                        continue
                    if reply[0] != 'q' and ':' not in reply_list:
                        return reply[1]
                if reply[0] == 'q' and answer != 'quit' and 'q' in reply_list:
                    confirm = True
            if reply_list[0] == ':':
                if answer != 'quit':
                    return answer
            if quit_proc == True:
                enter_before_exit(confirm)
                print 'Try again...'
                continue

    return 'quit'


def check_create_file_folder(output_path_list):
    tmp_flag = []
    for ff in output_path_list:
        if ff[-1:] == '/' or ff[-1:] == '\\':
            tmp_flag.append('d')
        else:
            tmp_flag.append('f')

    for n in range(0, len(output_path_list)):
        ff = output_path_list[n]
        flag = tmp_flag[n]
        ff_1 = os.path.isfile(ff)
        fd_1 = os.path.isdir(os.path.dirname(ff))
        if not os.path.isdir(os.path.dirname(ff)):
            os.makedirs(os.path.dirname(output_path_list[n]))
        if not os.path.isfile(ff) and flag == 'f':
            open(output_path_list[n], 'a').close()


def convert_to_string(item_to_convert):
    if type(item_to_convert) == unicode:
        return str(item_to_convert)
    list_level_1 = item_to_convert
    if type(item_to_convert) == list:
        list_level_1 = []
        for element_1 in item_to_convert:
            list_level_2 = []
            if type(element_1) == unicode:
                list_level_2 = str(element_1)
            elif type(element_1) == list:
                for element_2 in item_to_convert:
                    if type(element_2) == unicode:
                        element_2 = str(element_2)
                    list_level_2.append(element_2)

            else:
                list_level_2 = element_1
            list_level_1.append(list_level_2)

    return list_level_1


def get_substring(str, start=[
 1, '', 0, '-'], end=[-1, '', 0, '+']):

    def getindex(pattern):
        if pattern[0] > 0:
            id = 0
        else:
            id = len(str) - 1
            if pattern[2] == 0:
                id += 1
            for n in range(0, pattern[2]):
                if pattern[0] > 0:
                    id = str.find('.', id)
                    if n == pattern[2] - 1:
                        break
                    id += 1
                else:
                    id = str.rfind('.', 0, id + 1)
                    if n == pattern[2] - 1:
                        break
                    id -= 1

        return id

    start_index = getindex(start)
    if start[3] == '-' and start[2] != 0:
        start_index += 1
    end_index = getindex(end)
    if end[3] == '+':
        end_index += 1
    logger.log('debug', '[start, end] = [%s, %s]' % (start_index, end_index))
    logger.log('debug', 'sub-string=%s' % str[start_index:end_index])
    return str[start_index:end_index]


def valid_bh_port(block_list, filter={'AND': [], 'NOT': []}):
    if type(block_list) == list:
        block = [ x for x in block_list if x is not None ]
        block = (' ').join(block)
    for filter_item in filter['AND']:
        if filter_item not in block:
            return False

    for filter_item in filter['NOT']:
        if filter_item in block:
            return False

    return True


def string_intersect(a, b, word=True):
    matches = map(lambda x: x[0] == x[1], zip(list(a), list(b)))
    substrings = filter(lambda x: x.find('_') == -1 and x != '', ('').join(map(lambda x: ['_', a[x]][matches[x]], range(len(a)))).split('_'))
    intersection = substrings[0].strip()
    if word:
        intersection += ' '
        if intersection not in a or intersection not in b:
            intersection = ''
    return intersection


def flatten(test_list):
    if isinstance(test_list, list):
        if len(test_list) == 0:
            return []
        first, rest = test_list[0], test_list[1:]
        return flatten(first) + flatten(rest)
    else:
        return [
         test_list]


def check_ip_address(ipadd):
    try:
        ip_address = unicode(ipadd)
        iptype = ipaddress.IPv4Address(ip_address)
        return 'IPv4'
    except:
        try:
            ip_address = unicode(ipadd)
            iptype = ipaddress.IPv6Address(ip_address)
            return 'IPv6'
        except:
            logger.log('info', 'Ip address: [%s] has an invalid format' % ipadd)
            return False


def check_ip_network(ipnet):
    try:
        ip_address = unicode(ipnet)
        ipaddress.IPv4Network(ip_address)
        return 'IPv4'
    except:
        try:
            ip_address = unicode(ipnet)
            ipaddress.IPv6Network(ip_address)
            return 'IPv6'
        except:
            logger.log('info', 'Ip network: [%s] has an invalid format' % ipnet)
            return False


def assert_file_exist(pathname):
    while 1:
        if True:
            print os.path.isfile(pathname) or '\nThis file %s must exist before starting.' % pathname
            prompt = 'Create this file and press [enter] to continue...'
            prompt_processing(prompt)
        return


def assert_valid_ip(ip_address, name='', req_new_ip=True, ask_write=False, description='', excel_wb='', tab='', cell=''):
    while True:
        try:
            ip_address = unicode(ip_address.strip())
        except:
            pass

        iptype = check_ip_address(ip_address)
        if ip_address == None or iptype != 'IPv4' and iptype != 'IPv6':
            if req_new_ip:
                print '\n%s[%s] is an invalid IP address...' % (name, ip_address)
                prompt = 'Enter a valid %s %s IP address: ' % (name, description)
                ip_address = prompt_processing(prompt)
                ask_write = True
            else:
                ip_address = ''
                break
        else:
            break

    if ask_write:
        if excel_wb != '' and tab != '' and cell != '':
            prompt = 'Save address in file? (y/n): '
            reply = prompt_processing(prompt)
            if reply == 'yes':
                try:
                    col, row = excel_wb.get_cell_coordinate(cell)
                    excel_wb.writeCell(tab, col, row, ip_address, force_save=True)
                except:
                    print 'Invalid excel file.  Address not saved. Continuing ...'

    return (
     ip_address, iptype)


def assert_valid_item(item, name, description='', excel_wb='', tab='', cell=''):
    prompt = 'Enter %s %s [%s]: ' % (name, description, item)
    new_item = prompt_processing(prompt)
    ask_write = True
    if excel_wb != '' and tab != '' and cell != '' and new_item != '':
        prompt = 'Save item in file? (y/n): '
        reply = prompt_processing(prompt)
        if reply == 'yes':
            try:
                col, row = excel_wb.get_cell_coordinate(cell)
                excel_wb.writeCell(tab, col, row, new_item, force_save=True)
            except:
                print 'Invalid excel file.  Item not saved. Continuing ...'

    if new_item != '':
        item = new_item
    return item


def assert_object_dict(objects_dict, element_name, instance_type):
    try:
        vtype = type(objects_dict)
    except:
        logger.log('warning', 'objects_dict[%s] is not a dictionary' % objects_dict)
        return False

    if vtype != dict:
        logger.log('warning', 'objects_dict[%s] is not a dictionary' % vtype)
        return False
    try:
        if isinstance(objects_dict[element_name], instance_type):
            return True
    except:
        pass

    logger.log('info', 'objects_dict[%s] is not a "%s" object instance' % (element_name, instance_type))
    return False


class q_lifo:

    def __init__(self, item=''):
        if item != '':
            self._queue = [
             item]
            self._count = 1
        else:
            self._queue = []
            self._count = 0

    def push(self, item):
        self._queue.append(item)
        self._count += 1

    def pop(self):
        if self._count == 0:
            return ''
        item = self._queue.pop()
        self._count -= 1
        return item

    def read(self, position=0):
        if self._count == 0:
            return ''
        index = self._count - 1
        if position < 0:
            index += position
        item = self._queue[index]
        return item

    def stat(self):
        return self._count