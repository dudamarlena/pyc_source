# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/changes.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
from localization import N_
from outputable import Outputable
import codecs, datetime, extensions, filtering, format, gravatar, interval, os, subprocess, terminal, textwrap

class FileDiff:

    def __init__(self, string):
        commit_line = string.split(b'|')
        if commit_line.__len__() == 2:
            self.name = commit_line[0].strip()
            self.insertions = commit_line[1].count(b'+')
            self.deletions = commit_line[1].count(b'-')

    @staticmethod
    def is_filediff_line(string):
        string = string.split(b'|')
        return string.__len__() == 2 and string[1].find(b'Bin') == -1 and (b'+' in string[1] or b'-' in string[1])

    @staticmethod
    def get_extension(string):
        string = string.split(b'|')[0].strip().strip(b'{}').strip(b'"').strip(b"'")
        return os.path.splitext(string)[1][1:]

    @staticmethod
    def get_filename(string):
        return string.split(b'|')[0].strip().strip(b'{}').strip(b'"').strip(b"'")

    @staticmethod
    def is_valid_extension(string):
        extension = FileDiff.get_extension(string)
        for i in extensions.get():
            if extension == i:
                return True

        return False


class Commit:

    def __init__(self, string):
        self.filediffs = []
        commit_line = string.split(b'|')
        if commit_line.__len__() == 4:
            self.date = commit_line[0]
            self.sha = commit_line[1]
            self.author = commit_line[2].strip()
            self.email = commit_line[3].strip()

    def add_filediff(self, filediff):
        self.filediffs.append(filediff)

    def get_filediffs(self):
        return self.filediffs

    @staticmethod
    def get_author_and_email(string):
        commit_line = string.split(b'|')
        if commit_line.__len__() == 4:
            return (commit_line[2].strip(), commit_line[3].strip())

    @staticmethod
    def is_commit_line(string):
        return string.split(b'|').__len__() == 4


class AuthorInfo:
    email = None
    insertions = 0
    deletions = 0
    commits = 0


class Changes:
    authors = {}
    authors_dateinfo = {}
    authors_by_email = {}
    emails_by_author = {}

    def __init__(self, hard):
        self.commits = []
        git_log_r = subprocess.Popen(b'git log --reverse --pretty="%cd|%H|%aN|%aE" --stat=100000,8192 --no-merges -w ' + interval.get_since() + interval.get_until() + (b'{0} --date=short').format(b'-C -C -M' if hard else b''), shell=True, bufsize=1, stdout=subprocess.PIPE).stdout
        commit = None
        found_valid_extension = False
        lines = git_log_r.readlines()
        for i in lines:
            j = i.strip().decode(b'unicode_escape', b'ignore')
            j = j.encode(b'latin-1', b'replace')
            j = j.decode(b'utf-8', b'replace')
            if Commit.is_commit_line(j):
                author, email = Commit.get_author_and_email(j)
                self.emails_by_author[author] = email
                self.authors_by_email[email] = author
            if Commit.is_commit_line(j) or i is lines[(-1)]:
                if found_valid_extension:
                    self.commits.append(commit)
                found_valid_extension = False
                commit = Commit(j)
            if FileDiff.is_filediff_line(j) and not filtering.set_filtered(FileDiff.get_filename(j)) and not filtering.set_filtered(commit.author, b'author') and not filtering.set_filtered(commit.email, b'email') and not filtering.set_filtered(commit.sha, b'revision'):
                extensions.add_located(FileDiff.get_extension(j))
                if FileDiff.is_valid_extension(j):
                    found_valid_extension = True
                    filediff = FileDiff(j)
                    commit.add_filediff(filediff)

        if interval.has_interval() and len(self.commits) > 0:
            interval.set_ref(self.commits[0].sha)
        if len(self.commits) > 0:
            self.first_commit_date = datetime.date(int(self.commits[0].date[0:4]), int(self.commits[0].date[5:7]), int(self.commits[0].date[8:10]))
            self.last_commit_date = datetime.date(int(self.commits[(-1)].date[0:4]), int(self.commits[(-1)].date[5:7]), int(self.commits[(-1)].date[8:10]))
        return

    def get_commits(self):
        return self.commits

    def __modify_authorinfo__(self, authors, key, commit):
        if authors.get(key, None) == None:
            authors[key] = AuthorInfo()
        if commit.get_filediffs():
            authors[key].commits += 1
        for j in commit.get_filediffs():
            authors[key].insertions += j.insertions
            authors[key].deletions += j.deletions

        return

    def get_authorinfo_list(self):
        if not self.authors:
            for i in self.commits:
                self.__modify_authorinfo__(self.authors, i.author, i)

        return self.authors

    def get_authordateinfo_list(self):
        if not self.authors_dateinfo:
            for i in self.commits:
                self.__modify_authorinfo__(self.authors_dateinfo, (i.date, i.author), i)

        return self.authors_dateinfo

    def get_latest_author_by_email(self, name):
        if not hasattr(name, b'decode'):
            name = str.encode(name)
        name = name.decode(b'unicode_escape', b'ignore')
        return self.authors_by_email[name]

    def get_latest_email_by_author(self, name):
        return self.emails_by_author[name]


__changes__ = None

def get(hard):
    global __changes__
    if __changes__ == None:
        __changes__ = Changes(hard)
    return __changes__


HISTORICAL_INFO_TEXT = N_(b'The following historical commit information, by author, was found in the repository')
NO_COMMITED_FILES_TEXT = N_(b'No commited files with the specified extensions were found')

class ChangesOutput(Outputable):

    def __init__(self, hard):
        self.changes = get(hard)
        Outputable.__init__(self)

    def output_html(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0
        changes_xml = b'<div><div class="box">'
        chart_data = b''
        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            changes_xml += b'<p>' + _(HISTORICAL_INFO_TEXT) + b'.</p><div><table id="changes" class="git">'
            changes_xml += (b'<thead><tr> <th>{0}</th> <th>{1}</th> <th>{2}</th> <th>{3}</th> <th>{4}</th>').format(_(b'Author'), _(b'Commits'), _(b'Insertions'), _(b'Deletions'), _(b'% of changes'))
            changes_xml += b'</tr></thead><tbody>'
            for i, entry in enumerate(sorted(authorinfo_list)):
                authorinfo = authorinfo_list.get(entry)
                percentage = 0 if total_changes == 0 else (authorinfo.insertions + authorinfo.deletions) / total_changes * 100
                changes_xml += b'<tr ' + (b'class="odd">' if i % 2 == 1 else b'>')
                if format.get_selected() == b'html':
                    changes_xml += (b'<td><img src="{0}"/>{1}</td>').format(gravatar.get_url(self.changes.get_latest_email_by_author(entry)), entry)
                else:
                    changes_xml += b'<td>' + entry + b'</td>'
                changes_xml += b'<td>' + str(authorinfo.commits) + b'</td>'
                changes_xml += b'<td>' + str(authorinfo.insertions) + b'</td>'
                changes_xml += b'<td>' + str(authorinfo.deletions) + b'</td>'
                changes_xml += b'<td>' + (b'{0:.2f}').format(percentage) + b'</td>'
                changes_xml += b'</tr>'
                chart_data += (b'{{label: "{0}", data: {1}}}').format(entry, (b'{0:.2f}').format(percentage))
                if sorted(authorinfo_list)[(-1)] != entry:
                    chart_data += b', '

            changes_xml += b'<tfoot><tr> <td colspan="5">&nbsp;</td> </tr></tfoot></tbody></table>'
            changes_xml += b'<div class="chart" id="changes_chart"></div></div>'
            changes_xml += b'<script type="text/javascript">'
            changes_xml += (b'    changes_plot = $.plot($("#changes_chart"), [{0}], {{').format(chart_data)
            changes_xml += b'        series: {'
            changes_xml += b'            pie: {'
            changes_xml += b'                innerRadius: 0.4,'
            changes_xml += b'                show: true,'
            changes_xml += b'                combine: {'
            changes_xml += b'                    threshold: 0.01,'
            changes_xml += b'                    label: "' + _(b'Minor Authors') + b'"'
            changes_xml += b'                }'
            changes_xml += b'            }'
            changes_xml += b'        }, grid: {'
            changes_xml += b'            hoverable: true'
            changes_xml += b'        }'
            changes_xml += b'    });'
            changes_xml += b'</script>'
        else:
            changes_xml += b'<p>' + _(NO_COMMITED_FILES_TEXT) + b'.</p>'
        changes_xml += b'</div></div>'
        print(changes_xml)

    def output_text(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0
        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            print(textwrap.fill(_(HISTORICAL_INFO_TEXT) + b':', width=terminal.get_size()[0]) + b'\n')
            terminal.printb(terminal.ljust(_(b'Author'), 21) + terminal.rjust(_(b'Commits'), 13) + terminal.rjust(_(b'Insertions'), 14) + terminal.rjust(_(b'Deletions'), 15) + terminal.rjust(_(b'% of changes'), 16))
            for i in sorted(authorinfo_list):
                authorinfo = authorinfo_list.get(i)
                percentage = 0 if total_changes == 0 else (authorinfo.insertions + authorinfo.deletions) / total_changes * 100
                print(terminal.ljust(i, 20)[0:20 - terminal.get_excess_column_count(i)], end=b' ')
                print(str(authorinfo.commits).rjust(13), end=b' ')
                print(str(authorinfo.insertions).rjust(13), end=b' ')
                print(str(authorinfo.deletions).rjust(14), end=b' ')
                print((b'{0:.2f}').format(percentage).rjust(15))

        else:
            print(_(NO_COMMITED_FILES_TEXT) + b'.')

    def output_xml(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0
        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            message_xml = b'\t\t<message>' + _(HISTORICAL_INFO_TEXT) + b'</message>\n'
            changes_xml = b''
            for i in sorted(authorinfo_list):
                authorinfo = authorinfo_list.get(i)
                percentage = 0 if total_changes == 0 else (authorinfo.insertions + authorinfo.deletions) / total_changes * 100
                name_xml = b'\t\t\t\t<name>' + i + b'</name>\n'
                gravatar_xml = b'\t\t\t\t<gravatar>' + gravatar.get_url(self.changes.get_latest_email_by_author(i)) + b'</gravatar>\n'
                commits_xml = b'\t\t\t\t<commits>' + str(authorinfo.commits) + b'</commits>\n'
                insertions_xml = b'\t\t\t\t<insertions>' + str(authorinfo.insertions) + b'</insertions>\n'
                deletions_xml = b'\t\t\t\t<deletions>' + str(authorinfo.deletions) + b'</deletions>\n'
                percentage_xml = b'\t\t\t\t<percentage-of-changes>' + (b'{0:.2f}').format(percentage) + b'</percentage-of-changes>\n'
                changes_xml += b'\t\t\t<author>\n' + name_xml + gravatar_xml + commits_xml + insertions_xml + deletions_xml + percentage_xml + b'\t\t\t</author>\n'

            print(b'\t<changes>\n' + message_xml + b'\t\t<authors>\n' + changes_xml + b'\t\t</authors>\n\t</changes>')
        else:
            print(b'\t<changes>\n\t\t<exception>' + _(NO_COMMITED_FILES_TEXT) + b'</exception>\n\t</changes>')