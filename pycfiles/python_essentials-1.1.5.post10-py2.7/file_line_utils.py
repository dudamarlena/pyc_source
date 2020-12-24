# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/file_line_utils.py
# Compiled at: 2014-12-28 23:09:37
import re, os

def file_replace_line(file_path, old_line_re, new_line):
    if file_path == None:
        raise ValueError("file_path mustn't be None")
    if not os.path.exists(file_path):
        create_file_wrapper(file_path)
    file_obj = open(file_path, 'r')
    file_lines = file_obj.readlines()
    file_obj.close()
    new_file_lines = []
    for file_line in file_lines:
        if re.match(old_line_re, file_line) != None:
            new_file_lines.append(new_line)
        else:
            new_file_lines.append(file_line)

    file_obj = open(file_path, 'w')
    file_obj.writelines(new_file_lines)
    file_obj.close()
    return


def retrieve_column_from_line(line, column, whitespace='\\s'):
    result = re.findall('[^' + whitespace + ']+', line)
    if len(result) <= column:
        raise ValueError("the requested column doesn't match the number of columns in the specified line")
    return result[column]


def retrieve_column_values(output, column_count, comment_symbol='#'):
    output_lines0 = filter_output_lines(output, comment_symbol=comment_symbol)
    ret_value = []
    for output_line in output_lines0:
        column_value = retrieve_column_from_line(output_line, column_count)
        ret_value.append(column_value)

    return ret_value


def file_lines(file_, comment_symbol='#'):
    if file_ == None:
        raise ValueError("file_ mustn't be None")
    if comment_symbol == '':
        raise ValueError("comment_symbol mustn't be the empty string ''")
    file_obj = open(file_, 'r')
    file_content = file_obj.read()
    file_obj.close()
    file_lines = file_content.split('\n')
    ret_value = filter_output_lines(file_lines, comment_symbol)
    return ret_value


def filter_output_lines(lines, comment_symbol='#'):
    if comment_symbol == '':
        raise ValueError("comment_symbol mustn't be the empty string ''")
    if str(type(lines)) != "<type 'list'>" and str(type(lines)) != "<class 'list'>":
        raise ValueError("lines %s isn't a list" % (lines,))
    ret_value = []
    for i in lines:
        i = i.strip()
        if comment_symbol is None:
            if i != '':
                ret_value.append(i)
        elif not re.match('[\\s]*' + comment_symbol + '.*', i) and re.match('[\\s]+', i) == None and i != '':
            if comment_symbol not in i:
                ret_value.append(i)
            else:
                ret_value.append(i[:i.find(comment_symbol)])

    return ret_value


def file_lines_matches(file_, pattern, comment_symbol='#'):
    if comment_symbol == '':
        raise ValueError("comment_symbol mustn't be the empty string ''")
    retvalue = []
    filelines = file_lines(file_, comment_symbol)
    return output_lines_matches(filelines, pattern, comment_symbol=comment_symbol)


def output_lines_matches(lines, pattern, comment_symbol='#'):
    retvalue = []
    lines = filter_output_lines(lines, comment_symbol=comment_symbol)
    for line in lines:
        if re.match(pattern, line) != None:
            retvalue.append(line)

    return retvalue


def file_lines_match(file_, pattern, comment_symbol='#'):
    if comment_symbol == '':
        raise ValueError("comment_symbol mustn't be the empty string ''")
    file_lines0 = file_lines(file_, comment_symbol=comment_symbol)
    return output_lines_match(file_lines0, pattern, comment_symbol=comment_symbol)


def output_lines_match(lines, pattern, comment_symbol='#'):
    if comment_symbol == '':
        raise ValueError("comment_symbol mustn't be the empty string ''")
    lines = filter_output_lines(lines, comment_symbol=comment_symbol)
    for line in lines:
        if re.match(pattern, line):
            return True

    return False


def comment_out(file_path, line, comment_symbol):
    if comment_symbol == '':
        raise ValueError("comment_symbol mustn't be the empty string ''")
    new_lines = []
    file_lines0 = file_lines(file_path, comment_symbol=None)
    for file_line in file_lines0:
        if not re.match('[\\s]*%s[\\s]*' % line):
            new_lines.append(file_line)
        else:
            new_lines.append('%s %s' % (comment_symbol, line))

    file_obj = open(file_path, 'rw+')
    for new_line in new_lines:
        file_obj.write('%s\n' % new_line)

    file_obj.flush()
    file_obj.close()
    return


def comment_in(file_path, line, comment_symbol):
    new_lines = []
    file_lines0 = file_lines(file_path, comment_symbol=None)
    for file_line in file_lines0:
        if not re.match('[\\s]*%s[\\s]*%s' % (comment_symbol, line), line):
            new_lines.append(file_line)
        else:
            new_lines.append(re.search(line, file_line).group(0))

    file_obj = open(file_path, 'w')
    for new_line in new_lines:
        file_obj.write('%s\n' % new_line)

    file_obj.flush()
    file_obj.close()
    return


def create_file_wrapper(path):
    if not check_os.check_python3():
        file_obj = open(path, 'w')
        file_obj.close()
    else:
        file_obj = open(path, 'x')
        file_obj.close()