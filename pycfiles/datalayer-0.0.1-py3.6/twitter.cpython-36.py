# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jupyterlab_twitter/twitter.py
# Compiled at: 2018-06-25 10:44:27
# Size of source mod 2**32: 15071 bytes
"""
This is a Module where actual Twitter Commands are written & Executed &  the result
is sent back to the calling module.
"""
import os, subprocess
from subprocess import Popen, PIPE

class Twitter:
    __doc__ = '\n    A single parent Twitter Class which has all the individual twitter methods in it.\n    '

    def status(self, current_path):
        """
        Function used to execute twitter status command & send back the result.
        """
        p = Popen([
         'git', 'status', '--porcelain'],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + current_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            result = []
            line_array = my_output.decode('utf-8').splitlines()
            for line in line_array:
                to1 = None
                from_path = line[3:]
                if line[0] == 'R':
                    to0 = line[3:].split(' -> ')
                    to1 = to0[(len(to0) - 1)]
                else:
                    to1 = line[3:]
                if to1.startswith('"'):
                    to1 = to1[1:]
                if to1.endswith('"'):
                    to1 = to1[:-1]
                result.append({'x':line[0], 
                 'y':line[1], 
                 'to':to1, 
                 'from':from_path})

            return {'code':p.returncode, 
             'files':result}
        else:
            return {'code':p.returncode, 
             'command':'twitter status --porcelain', 
             'message':my_error.decode('utf-8')}

    def log(self, current_path):
        """
        Function used to execute twitter log command & send back the result.
        """
        p = Popen([
         'git', 'log', '--pretty=format:%H%n%an%n%ar%n%s', '-10'],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + current_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            result = []
            line_array = my_output.decode('utf-8').splitlines()
            i = 0
            while i < len(line_array):
                if i + 4 < len(line_array):
                    result.append({'commit':line_array[i], 
                     'author':line_array[i + 1], 
                     'date':line_array[i + 2], 
                     'commit_msg':line_array[i + 3], 
                     'pre_commit':line_array[i + 4]})
                else:
                    result.append({'commit':line_array[i], 
                     'author':line_array[i + 1], 
                     'date':line_array[i + 2], 
                     'commit_msg':line_array[i + 3], 
                     'pre_commit':''})
                i += 4

            return {'code':p.returncode,  'commits':result}
        else:
            return {'code':p.returncode, 
             'message':my_error.decode('utf-8')}

    def log_1(self, selected_hash, current_path):
        """
        Function used to execute the second twitter log command (used to get
        insertions & deletions per file) & send back the result.
        """
        p = Popen([
         'twitter', 'log', '-1', '--stat', '--numstat', '--oneline',
         selected_hash],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + current_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            result = []
            note = [
             0] * 3
            count = 0
            temp = ''
            line_array = my_output.decode('utf-8').splitlines()
            length = len(line_array)
            if length > 1:
                temp = line_array[(length - 1)]
                words = temp.split()
                for i in range(0, len(words)):
                    if words[i].isditwitter():
                        note[count] = words[i]
                        count += 1

                for num in range(1, int(length / 2)):
                    line_info = line_array[num].split()
                    words = line_info[2].split('/')
                    length = len(words)
                    result.append({'modified_file_path':line_info[2], 
                     'modified_file_name':words[length - 1], 
                     'insertion':line_info[0], 
                     'deletion':line_info[1]})

            if note[2] == 0:
                if length > 1:
                    if '-' in temp:
                        exchange = note[1]
                        note[1] = note[2]
                        note[2] = exchange
            return {'code':p.returncode,  'modified_file_note':temp, 
             'modified_files_count':note[0], 
             'number_of_insertions':note[1], 
             'number_of_deletions':note[2], 
             'modified_files':result}
        else:
            return {'code':p.returncode,  'command':'twitter log_1', 
             'message':my_error.decode('utf-8')}

    def diff(self, top_repo_path):
        """
        Function used to execute twitter diff command & send back the result.
        """
        p = Popen([
         'git', 'diff', '--numstat'],
          stdout=PIPE,
          stderr=PIPE,
          cwd=top_repo_path)
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            result = []
            line_array = my_output.decode('utf-8').splitlines()
            for line in line_array:
                linesplit = line.split()
                result.append({'insertions':linesplit[0], 
                 'deletions':linesplit[1], 
                 'filename':linesplit[2]})

            return {'code':p.returncode, 
             'result':result}
        else:
            return {'code':p.returncode, 
             'message':my_error.decode('utf-8')}

    def branch(self, current_path):
        """
        Function used to execute branch status command & send back the result.
        """
        p = Popen([
         'git', 'branch', '-a'],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + current_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            result = []
            line_array = my_output.decode('utf-8').splitlines()
            for line_full in line_array:
                line_cut = (
                 line_full.split(' -> '),)
                tag = (None, )
                current = (False, )
                remote = (False, )
                if len(line_cut[0]) > 1:
                    tag = line_cut[0][1]
                line = (
                 line_cut[0][0],)
                if line_full[0] == '*':
                    current = (True, )
                if len(line_full) >= 10 and line_full[2:10] == 'remotes/':
                    remote = (True, )
                    result.append({'current':current, 
                     'remote':remote, 
                     'name':line[0][10:], 
                     'tag':tag})
                else:
                    result.append({'current':current, 
                     'remote':remote, 
                     'name':line_full[2:], 
                     'tag':tag})

            return {'code':p.returncode,  'branches':result}
        else:
            return {'code':p.returncode, 
             'command':'twitter branch -a', 
             'message':my_error.decode('utf-8')}

    def showtoplevel(self, current_path):
        """
        Function used to execute twitter --show-toplevel command & send back the
        result.
        """
        p = Popen([
         'git', 'rev-parse', '--show-toplevel'],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + current_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            result = {'code':p.returncode,  'top_repo_path':my_output.decode('utf-8').strip('\n')}
            return result
        else:
            return {'code':p.returncode, 
             'command':'twitter rev-parse --show-toplevel', 
             'message':my_error.decode('utf-8')}

    def showprefix(self, current_path):
        """
        Function used to execute twitter --show-prefix command & send back the
        result.
        """
        p = Popen([
         'git', 'rev-parse', '--show-prefix'],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + current_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            result = {'code':p.returncode,  'under_repo_path':my_output.decode('utf-8').strip('\n')}
            return result
        else:
            return {'code':p.returncode, 
             'command':'twitter rev-parse --show-prefix', 
             'message':my_error.decode('utf-8')}

    def add(self, filename, top_repo_path):
        """
        Function used to execute twitter add<filename> command & send back the
        result.
        """
        my_output = subprocess.check_output([
         'git', 'add', filename],
          cwd=top_repo_path)
        return my_output

    def add_all(self, top_repo_path):
        """
        Function used to execute twitter add all command & send back the result.
        """
        my_output = subprocess.check_output([
         'git', 'add', '-u'],
          cwd=top_repo_path)
        return my_output

    def add_all_untracked(self, top_repo_path):
        """
        Function used to execute twitter add_all_untracked command & send back the
        result.
        """
        e = 'echo "a\n*\nq\n" | twitter add -i'
        my_output = subprocess.call(e, shell=True, cwd=top_repo_path)
        return {'result': my_output}

    def reset(self, filename, top_repo_path):
        """
        Function used to execute twitter reset <filename> command & send back the
        result.
        """
        my_output = subprocess.check_output([
         'git', 'reset', filename],
          cwd=top_repo_path)
        return my_output

    def reset_all(self, top_repo_path):
        """
        Function used to execute twitter reset all command & send back the result.
        """
        my_output = subprocess.check_output([
         'git', 'reset'],
          cwd=top_repo_path)
        return my_output

    def checkout_new_branch(self, branchname, current_path):
        """
        Function used to execute twitter checkout <make-branch> command & send back
        the result.
        """
        p = Popen([
         'git', 'checkout', '-b', branchname],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + current_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            return {'code':p.returncode,  'message':my_output.decode('utf-8')}
        else:
            return {'code':p.returncode, 
             'command':'twitter checkout -b' + branchname, 
             'message':my_error.decode('utf-8')}

    def checkout_branch(self, branchname, current_path):
        """
        Function used to execute twitter checkout <branch-name> command & send back
        the result.
        """
        p = Popen([
         'git', 'checkout', branchname],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + current_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            return {'code':p.returncode,  'message':my_output.decode('utf-8')}
        else:
            return {'code':p.returncode, 
             'command':'twitter checkout ' + branchname, 
             'message':my_error.decode('utf-8')}

    def checkout(self, filename, top_repo_path):
        """
        Function used to execute twitter checkout for the filename & send back the
        result.
        """
        my_output = subprocess.check_output([
         'git', 'checkout', '--', filename],
          cwd=top_repo_path)
        return my_output

    def checkout_all(self, top_repo_path):
        """
        Function used to actually execute twitter checkout command & send back the
        result.
        """
        my_output = subprocess.check_output([
         'git', 'checkout', '--', '.'],
          cwd=top_repo_path)
        return my_output

    def commit(self, commit_msg, top_repo_path):
        """
        Function used to execute twitter commit <filename> command & send back the
        result.
        """
        my_output = subprocess.check_output([
         'git', 'commit', '-m', commit_msg],
          cwd=top_repo_path)
        return my_output

    def pull(self, origin, master, curr_fb_path):
        """
        Function used to execute twitter pull <branch1> <branch2> command & send
        back the result.
        """
        p = Popen([
         'git', 'pull', origin, master, '--no-commit'],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + curr_fb_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            return {'code': p.returncode}
        else:
            return {'code':p.returncode, 
             'command':'twitter pull ' + origin + ' ' + master + ' --no-commit', 
             'message':my_error.decode('utf-8')}

    def push(self, origin, master, curr_fb_path):
        """
        Function used to execute twitter push <branch1> <branch2> command & send
        back the result.
        """
        p = Popen([
         'git', 'push', origin, master],
          stdout=PIPE,
          stderr=PIPE,
          cwd=(os.getcwd() + '/' + curr_fb_path))
        my_output, my_error = p.communicate()
        if p.returncode == 0:
            return {'code': p.returncode}
        else:
            return {'code':p.returncode, 
             'command':'twitter push ' + origin + ' ' + master, 
             'message':my_error.decode('utf-8')}

    def init(self, current_path):
        """
        Function used to execute twitter init command & send back the result.
        """
        my_output = subprocess.check_output([
         'git', 'init'],
          cwd=(os.getcwd() + '/' + current_path))
        return my_output