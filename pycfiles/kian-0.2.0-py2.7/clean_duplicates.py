# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scripts/clean_duplicates.py
# Compiled at: 2016-03-18 19:30:50
import sys, MySQLdb, urllib2
url = 'http://tools.wmflabs.org/autolist/index.php?wdq=claim[{statemnt}:{value}]&run=Run&download=1'
res_human = urllib2.urlopen(url.format(statemnt='31', value='5')).read().decode('utf-8')

def main():
    db = MySQLdb.connect(host='tools-db', db='s52709__kian_p', read_default_file='~/replica.my.cnf')
    cursor = db.cursor()
    select_statement = 'SELECT property, value from kian where status = 0 group by property, value;'
    cursor.execute(select_statement)
    cases = list(cursor.fetchall())
    for case in cases:
        print ('Working on {case}').format(case=case)
        url = 'http://tools.wmflabs.org/autolist/index.php?wdq=claim[{statemnt}:{value}]&run=Run&download=1'
        if case[1] != 'Q5':
            res = urllib2.urlopen(url.format(statemnt=case[0][1:], value=case[1][1:])).read().decode('utf-8')
        else:
            res = res_human
        res = set(res.split('\n'))
        select_statement = ("SELECT qid from kian where status = 0 and property = '{prop}' and value = '{val}';").format(prop=case[0], val=case[1])
        cursor.execute(select_statement)
        res2 = set([ i[0] for i in cursor.fetchall() ])
        intersection = res & res2
        print (len(res), len(res2), len(intersection))
        str_intersection = str(tuple(intersection)).replace("u'Q", "'Q")
        set_statement = ("UPDATE kian SET status = 1 where qid in {qid} and property = '{prop}' and value = '{val}';").format(qid=str_intersection, prop=case[0], val=case[1])
        cursor.execute(set_statement)

    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()