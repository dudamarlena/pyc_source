# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/blame.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
from localization import N_
from outputable import Outputable
from changes import FileDiff
import comment, changes, datetime, filtering, format, gravatar, interval, multiprocessing, re, subprocess, sys, terminal, textwrap, threading
NUM_THREADS = multiprocessing.cpu_count()

class BlameEntry:
    rows = 0
    skew = 0
    comments = 0


__thread_lock__ = threading.BoundedSemaphore(NUM_THREADS)
__blame_lock__ = threading.Lock()
AVG_DAYS_PER_MONTH = 30.4167

class BlameThread(threading.Thread):

    def __init__(self, useweeks, changes, blame_string, extension, blames, filename):
        __thread_lock__.acquire()
        threading.Thread.__init__(self)
        self.useweeks = useweeks
        self.changes = changes
        self.blame_string = blame_string
        self.extension = extension
        self.blames = blames
        self.filename = filename
        self.is_inside_comment = False

    def __clear_blamechunk_info__(self):
        self.blamechunk_email = None
        self.blamechunk_is_last = False
        self.blamechunk_is_prior = False
        self.blamechunk_revision = None
        self.blamechunk_time = None
        return

    def __handle_blamechunk_content__(self, content):
        author = None
        comments, self.is_inside_comment = comment.handle_comment_block(self.is_inside_comment, self.extension, content)
        if self.blamechunk_is_prior and interval.get_since():
            return
        else:
            try:
                author = self.changes.get_latest_author_by_email(self.blamechunk_email)
            except KeyError:
                return

            __blame_lock__.acquire()
            if not filtering.set_filtered(author, b'author') and not filtering.set_filtered(self.blamechunk_email, b'email') and not filtering.set_filtered(self.blamechunk_revision, b'revision'):
                if self.blames.get((author, self.filename), None) == None:
                    self.blames[(author, self.filename)] = BlameEntry()
                self.blames[(author, self.filename)].comments += comments
                self.blames[(author, self.filename)].rows += 1
                if (self.blamechunk_time - self.changes.first_commit_date).days > 0:
                    self.blames[(author, self.filename)].skew += (self.changes.last_commit_date - self.blamechunk_time).days / (7.0 if self.useweeks else AVG_DAYS_PER_MONTH)
            __blame_lock__.release()
            return

    def run(self):
        git_blame_r = subprocess.Popen(self.blame_string, shell=True, bufsize=1, stdout=subprocess.PIPE).stdout
        rows = git_blame_r.readlines()
        git_blame_r.close()
        self.__clear_blamechunk_info__()
        for j in range(0, len(rows)):
            row = rows[j].decode(b'utf-8', b'replace').strip()
            keyval = row.split(b' ', 2)
            if self.blamechunk_is_last:
                self.__handle_blamechunk_content__(row)
                self.__clear_blamechunk_info__()
            elif keyval[0] == b'boundary':
                self.blamechunk_is_prior = True
            elif keyval[0] == b'author-mail':
                self.blamechunk_email = keyval[1].lstrip(b'<').rstrip(b'>')
            elif keyval[0] == b'author-time':
                self.blamechunk_time = datetime.date.fromtimestamp(int(keyval[1]))
            elif keyval[0] == b'filename':
                self.blamechunk_is_last = True
            elif Blame.is_revision(keyval[0]):
                self.blamechunk_revision = keyval[0]

        __thread_lock__.release()


PROGRESS_TEXT = N_(b'Checking how many rows belong to each author (Progress): {0:.0f}%')

class Blame:

    def __init__(self, hard, useweeks, changes):
        self.blames = {}
        ls_tree_r = subprocess.Popen(b'git ls-tree --name-only -r ' + interval.get_ref(), shell=True, bufsize=1, stdout=subprocess.PIPE).stdout
        lines = ls_tree_r.readlines()
        for i, row in enumerate(lines):
            row = row.strip().decode(b'unicode_escape', b'ignore')
            row = row.encode(b'latin-1', b'replace')
            row = row.decode(b'utf-8', b'replace').strip(b'"').strip(b"'").strip()
            if FileDiff.is_valid_extension(row) and not filtering.set_filtered(FileDiff.get_filename(row)):
                blame_string = (b'git blame --line-porcelain -w {0} ').format(b'-C -C -M' if hard else b'') + interval.get_since() + interval.get_ref() + b' -- "' + row + b'"'
                thread = BlameThread(useweeks, changes, blame_string, FileDiff.get_extension(row), self.blames, row.strip())
                thread.daemon = True
                thread.start()
                if hard:
                    Blame.output_progress(i, len(lines))

        for i in range(0, NUM_THREADS):
            __thread_lock__.acquire()

    @staticmethod
    def output_progress(pos, length):
        if sys.stdout.isatty() and format.is_interactive_format():
            terminal.clear_row()
            print(_(PROGRESS_TEXT).format(100 * pos / length), end=b'')
            sys.stdout.flush()

    @staticmethod
    def is_revision(string):
        revision = re.search(b'([0-9a-f]{40})', string)
        if revision == None:
            return False
        else:
            return revision.group(1).strip()

    @staticmethod
    def get_stability(author, blamed_rows, changes):
        if author in changes.get_authorinfo_list():
            return 100.0 * blamed_rows / changes.get_authorinfo_list()[author].insertions
        return 100

    @staticmethod
    def get_time(string):
        time = re.search(b' \\(.*?(\\d\\d\\d\\d-\\d\\d-\\d\\d)', string)
        return time.group(1).strip()

    def get_summed_blames(self):
        summed_blames = {}
        for i in self.blames.items():
            if summed_blames.get(i[0][0], None) == None:
                summed_blames[i[0][0]] = BlameEntry()
            summed_blames[i[0][0]].rows += i[1].rows
            summed_blames[i[0][0]].skew += i[1].skew
            summed_blames[i[0][0]].comments += i[1].comments

        return summed_blames


__blame__ = None

def get(hard, useweeks, changes):
    global __blame__
    if __blame__ == None:
        __blame__ = Blame(hard, useweeks, changes)
    return __blame__


BLAME_INFO_TEXT = N_(b'Below are the number of rows from each author that have survived and are still intact in the current revision')

class BlameOutput(Outputable):

    def __init__(self, hard, useweeks):
        if format.is_interactive_format():
            print(b'')
        self.hard = hard
        self.useweeks = useweeks
        self.changes = changes.get(hard)
        get(self.hard, self.useweeks, self.changes)
        Outputable.__init__(self)

    def output_html(self):
        blame_xml = b'<div><div class="box">'
        blame_xml += b'<p>' + _(BLAME_INFO_TEXT) + b'.</p><div><table id="blame" class="git">'
        blame_xml += (b'<thead><tr> <th>{0}</th> <th>{1}</th> <th>{2}</th> <th>{3}</th> <th>{4}</th> </tr></thead>').format(_(b'Author'), _(b'Rows'), _(b'Stability'), _(b'Age'), _(b'% in comments'))
        blame_xml += b'<tbody>'
        chart_data = b''
        blames = sorted(__blame__.get_summed_blames().items())
        total_blames = 0
        for i in blames:
            total_blames += i[1].rows

        for i, entry in enumerate(blames):
            work_percentage = str((b'{0:.2f}').format(100.0 * entry[1].rows / total_blames))
            blame_xml += b'<tr ' + (b'class="odd">' if i % 2 == 1 else b'>')
            if format.get_selected() == b'html':
                author_email = self.changes.get_latest_email_by_author(entry[0])
                blame_xml += (b'<td><img src="{0}"/>{1}</td>').format(gravatar.get_url(author_email), entry[0])
            else:
                blame_xml += b'<td>' + entry[0] + b'</td>'
            blame_xml += b'<td>' + str(entry[1].rows) + b'</td>'
            blame_xml += b'<td>' + ((b'{0:.1f}').format(Blame.get_stability(entry[0], entry[1].rows, self.changes)) + b'</td>')
            blame_xml += b'<td>' + (b'{0:.1f}').format(float(entry[1].skew) / entry[1].rows) + b'</td>'
            blame_xml += b'<td>' + (b'{0:.2f}').format(100.0 * entry[1].comments / entry[1].rows) + b'</td>'
            blame_xml += b'<td style="display: none">' + work_percentage + b'</td>'
            blame_xml += b'</tr>'
            chart_data += (b'{{label: "{0}", data: {1}}}').format(entry[0], work_percentage)
            if blames[(-1)] != entry:
                chart_data += b', '

        blame_xml += b'<tfoot><tr> <td colspan="5">&nbsp;</td> </tr></tfoot></tbody></table>'
        blame_xml += b'<div class="chart" id="blame_chart"></div></div>'
        blame_xml += b'<script type="text/javascript">'
        blame_xml += (b'    blame_plot = $.plot($("#blame_chart"), [{0}], {{').format(chart_data)
        blame_xml += b'        series: {'
        blame_xml += b'            pie: {'
        blame_xml += b'                innerRadius: 0.4,'
        blame_xml += b'                show: true,'
        blame_xml += b'                combine: {'
        blame_xml += b'                    threshold: 0.01,'
        blame_xml += b'                    label: "' + _(b'Minor Authors') + b'"'
        blame_xml += b'                }'
        blame_xml += b'            }'
        blame_xml += b'        }, grid: {'
        blame_xml += b'            hoverable: true'
        blame_xml += b'        }'
        blame_xml += b'    });'
        blame_xml += b'</script></div></div>'
        print(blame_xml)

    def output_text(self):
        if sys.stdout.isatty() and format.is_interactive_format():
            terminal.clear_row()
        print(textwrap.fill(_(BLAME_INFO_TEXT) + b':', width=terminal.get_size()[0]) + b'\n')
        terminal.printb(terminal.ljust(_(b'Author'), 21) + terminal.rjust(_(b'Rows'), 10) + terminal.rjust(_(b'Stability'), 15) + terminal.rjust(_(b'Age'), 13) + terminal.rjust(_(b'% in comments'), 20))
        for i in sorted(__blame__.get_summed_blames().items()):
            print(terminal.ljust(i[0], 20)[0:20 - terminal.get_excess_column_count(i[0])], end=b' ')
            print(str(i[1].rows).rjust(10), end=b' ')
            print((b'{0:.1f}').format(Blame.get_stability(i[0], i[1].rows, self.changes)).rjust(14), end=b' ')
            print((b'{0:.1f}').format(float(i[1].skew) / i[1].rows).rjust(12), end=b' ')
            print((b'{0:.2f}').format(100.0 * i[1].comments / i[1].rows).rjust(19))

    def output_xml(self):
        message_xml = b'\t\t<message>' + _(BLAME_INFO_TEXT) + b'</message>\n'
        blame_xml = b''
        for i in sorted(__blame__.get_summed_blames().items()):
            author_email = self.changes.get_latest_email_by_author(i[0])
            name_xml = b'\t\t\t\t<name>' + i[0] + b'</name>\n'
            gravatar_xml = b'\t\t\t\t<gravatar>' + gravatar.get_url(author_email) + b'</gravatar>\n'
            rows_xml = b'\t\t\t\t<rows>' + str(i[1].rows) + b'</rows>\n'
            stability_xml = b'\t\t\t\t<stability>' + (b'{0:.1f}').format(Blame.get_stability(i[0], i[1].rows, self.changes)) + b'</stability>\n'
            age_xml = b'\t\t\t\t<age>' + (b'{0:.1f}').format(float(i[1].skew) / i[1].rows) + b'</age>\n'
            percentage_in_comments_xml = b'\t\t\t\t<percentage-in-comments>' + (b'{0:.2f}').format(100.0 * i[1].comments / i[1].rows) + b'</percentage-in-comments>\n'
            blame_xml += b'\t\t\t<author>\n' + name_xml + gravatar_xml + rows_xml + stability_xml + age_xml + percentage_in_comments_xml + b'\t\t\t</author>\n'

        print(b'\t<blame>\n' + message_xml + b'\t\t<authors>\n' + blame_xml + b'\t\t</authors>\n\t</blame>')