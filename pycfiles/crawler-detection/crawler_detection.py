# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: crawler_detection.py
# Compiled at: 2013-11-11 01:08:38


def crawler_detection():
    """
    import glob
    import os
    for files in glob.glob("*.log"):
        print files
    """
    import glob, pandas as pd, apachelog, sys, numpy as np, re, csv
    from datetime import datetime
    import string, os, pandas
    from socket import gethostbyaddr
    import subprocess, io
    from bulkwhois.shadowserver import BulkWhoisShadowserver
    from pandas import read_csv
    import httpbl
    from dateutil import parser
    fformat = '%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\"'
    p = apachelog.parser(fformat)
    log_list = []
    path = os.path.abspath('crawler-detection/Data/*.log')
    for file in glob.glob(path):
        with open(file, 'r') as (f):
            for line in f:
                try:
                    data = p.parse(line)
                except:
                    pass

                log_list.append(data)

    df = pd.DataFrame(log_list)
    df = df.rename(columns={'%>s': 'Status', '%b': 'Bytes', '%h': 'IP', 
       '%l': 'UserName', '%r': 'Request', '%t': 'Time', '%u': 'UserID', '%{Referer}i': 'Referer', '%{User-Agent}i': 'Agent'})

    class color:
        PURPLE = '\x1b[95m'
        CYAN = '\x1b[96m'
        DARKCYAN = '\x1b[36m'
        BLUE = '\x1b[94m'
        GREEN = '\x1b[92m'
        YELLOW = '\x1b[93m'
        RED = '\x1b[91m'
        BOLD = '\x1b[1m'
        UNDERLINE = '\x1b[4m'
        END = '\x1b[0m'

    def parse(x):
        date, hh, mm, ss = x.split(':')
        dd, mo, yyyy = date.split('/')
        return parser.parse('%s %s %s %s:%s:%s' % (yyyy, mo, dd, hh, mm, ss))

    df['Time'] = df['Time'].apply(lambda x: x[1:-7])
    df['Time'] = pd.DataFrame(dict(time=pd.to_datetime(map(parse, df['Time']))))
    g = df.groupby(['IP', 'Agent'])
    df['session_number'] = g['Time'].apply(lambda s: (s - s.shift(1) > pd.offsets.Minute(30).nanos).fillna(0).cumsum(skipna=False))
    df1 = df.set_index(['IP', 'Agent', 'session_number'])
    g1 = df.groupby(['IP', 'Agent', 'session_number'])
    df1['session'] = g1.apply(lambda x: 1).cumsum()
    NoOfSessions = len(df1.groupby('session'))
    print color.BOLD + '\n1.0 Total No of Sessions : ' + color.END + str(NoOfSessions)
    df2 = pd.DataFrame(df1.reset_index())
    df2 = df2[(~df2['Agent'].str.contains('pingdom|panopta|nagios', na=False))]
    df3 = pd.DataFrame({'count': df2.groupby(['Request', 'session']).size()}).reset_index()
    robotssessions = df3[(df3['Request'] == 'GET /robots.txt HTTP/1.1')]['session'].unique()
    robotsaccessed = pd.DataFrame(df2[df2['session'].isin(robotssessions)][['IP', 'Agent', 'session']].drop_duplicates(cols='session', take_last=False))
    print color.BOLD + '\n2.0 No of sessions accessed "robots.txt" : ' + color.END + str(len(robotsaccessed))
    robotsaccessed.to_csv('robots.txt Accessed', sep=',', header=False, index=False)
    hiddenlinkType1 = df3[df3['Request'].str.contains('link1.html', na=False)]['session'].unique()
    hiddenlinkType2 = df3[df3['Request'].str.contains('link2.html', na=False)]['session'].unique()
    hiddenlinkType3 = df3[df3['Request'].str.contains('link3.html', na=False)]['session'].unique()
    hiddenlinkaccessedType1 = pd.DataFrame(df2[df2['session'].isin(hiddenlinkType1)][['IP', 'Agent', 'session']].drop_duplicates(cols='session', take_last=False))
    hiddenlinkaccessedType2 = pd.DataFrame(df2[df2['session'].isin(hiddenlinkType2)][['IP', 'Agent', 'session']].drop_duplicates(cols='session', take_last=False))
    hiddenlinkaccessedType3 = pd.DataFrame(df2[df2['session'].isin(hiddenlinkType3)][['IP', 'Agent', 'session']].drop_duplicates(cols='session', take_last=False))
    hiddenlinksessions = df3[df3['Request'].str.contains('link1', na=False)]['session'].unique()
    hiddenlinkaccessed = pd.DataFrame(df2[df2['session'].isin(hiddenlinksessions)][['IP', 'Agent', 'session']].drop_duplicates(cols='session', take_last=False))
    print color.BOLD + '\n3.0 No of sessions accessed any type of hidden link : ' + color.END + str(len(hiddenlinkaccessed))
    hiddenlinkaccessed.to_csv('hiddenlinks Accessed', sep=',', header=False, index=False)
    hiddenlinkaccessedip = hiddenlinkaccessed.IP.unique()
    hiddenlinkaccessed2 = pd.DataFrame(df2[df2['IP'].isin(hiddenlinkaccessedip)][['IP', 'Agent', 'session']])
    hitcount = pd.DataFrame({'count': df2.groupby(['session', 'IP']).size()}).reset_index()
    hitcountgreater = pd.DataFrame(hitcount[(hitcount['count'] > 50)])
    hitcountgreatersessions = hitcountgreater.session.unique()
    dfhitcountgreater = df2[df2['session'].isin(hitcountgreatersessions)][['IP', 'Agent', 'session']].drop_duplicates(cols='session', take_last=False)
    hitsswithagent = pd.DataFrame(pd.merge(hitcountgreater, dfhitcountgreater, how='outer'))
    df4 = pd.DataFrame({'count': df2.groupby(['Referer', 'session']).size()}).reset_index()
    blanksessions = pd.DataFrame(df2[(df2['Referer'] == '-')][['IP', 'Agent', 'Referer', 'session']])
    dfx = pd.DataFrame({'count': blanksessions.groupby(['session', 'IP']).size()}).reset_index()
    thresh2 = pd.DataFrame(dfx[(dfx['count'] > 50)])
    thresh2Sessions = thresh2.session.unique()
    blankreferrer = pd.DataFrame(df2[df2['session'].isin(thresh2Sessions)][['IP', 'Agent', 'Referer', 'session']].drop_duplicates(cols='session', take_last=False))
    dfblankreferrer = pd.DataFrame(pd.merge(thresh2, blankreferrer, how='outer'))
    merged1 = pd.merge(robotsaccessed, hiddenlinkaccessed, how='outer')
    merged3 = pd.merge(merged1, hitsswithagent, how='outer')
    merged4 = pd.merge(merged3, dfblankreferrer, how='outer')
    dfmeged = pd.DataFrame(merged4)
    dfmeged.drop_duplicates(cols='session', take_last=False).to_csv('PossibleCrawlers', sep=',', header=False, index=False)
    print color.BOLD + '\n4.0 No of All Possible Web crawler Sessions : ' + color.END + str(len(dfmeged.drop_duplicates(cols='session', take_last=False)))
    dfmeged.drop_duplicates(cols='IP', take_last=False).to_csv('PossibleCrawlers2', sep=',', header=False, index=False)
    print color.BOLD + '\n5.0 Single IP using multiple User Agents : ' + color.END
    useragents = pd.DataFrame(dfmeged.groupby(['IP', 'Agent']).size().reset_index().groupby('IP').size()[50:80])
    useragents = useragents.reset_index()
    useragents.columns = ['IP', 'AgentCount']
    useragentscountgreater = pd.DataFrame(useragents[(useragents['AgentCount'] >= 2)])
    mergeMultipleUA = pd.merge(dfmeged, useragentscountgreater, how='inner')
    if mergeMultipleUA.empty:
        print 'No Results Found!'
    else:
        print mergeMultipleUA[0:25]
    multiuseragentIPs = mergeMultipleUA.IP.unique()
    blankagents = pd.DataFrame(dfmeged[(dfmeged['Agent'] == '-')][['IP', 'Agent', 'Referer', 'session']])
    hiddenlinksessions = df3[df3['Request'].str.contains('aboutnic', na=False)]['session'].unique()
    hiddenlinkaccessed = pd.DataFrame(df2[df2['session'].isin(hiddenlinksessions)][['IP', 'Request', 'Agent', 'session']])
    bulk_whois = BulkWhoisShadowserver()
    f = open('PossibleCrawlers')
    lines = f.readlines()
    ip = []
    myfile = open('whois', 'w')
    for line in lines:
        ip.append(line.split(',')[0])

    records = bulk_whois.lookup_ips(ip)
    xy = []
    for record in records:
        kk = ('\t').join([records[record]['ip'], records[record]['asn'],
         records[record]['as_name'], records[record]['cc']])
        myfile.write(records[record]['ip'] + ',' + records[record]['as_name'] + '\n')

    myfile.close()
    foo = open('whois', 'r')
    lines = foo.readlines()
    verifiedlist = []
    for line in lines:
        ip = line.split(',')[0]
        desc = line.split(',')[1]

    dfverified = read_csv('whois')
    dfverified.columns = ['IP', 'Verified']
    test = pd.merge(dfverified, dfmeged, how='inner')
    dfmerged = pd.DataFrame(test)
    goodcrawlers = dfmerged[dfmerged['Verified'].str.contains('YANDEX|MICROSOFT|GOOGLE|SOFTLAYER|CNNIC-BAIDU|CHINANET-IDC-BJ|CHINA169', na=False)]
    dfGoodCrawlers = pd.DataFrame(goodcrawlers)
    print color.BOLD + '\n6.0 No of unique "known" crawler sessions(only first 25) : ' + color.END + str(len(dfGoodCrawlers.drop_duplicates(cols='session', take_last=False)))
    dfGoodCrawlers['Verified'] = dfGoodCrawlers['Verified'].fillna('Not Found')
    dfGoodCrawlers.to_csv('Known Crawlers', sep=',', header=False, index=False)
    notGoodcrawlers = dfmerged[(~dfmerged['Verified'].str.contains('YANDEX|MICROSOFT|GOOGLE|SOFTLAYER|CNNIC-BAIDU|CHINANET-IDC-BJ|CHINA169', na=False))]
    dfNotGoodCrawlers = pd.DataFrame(notGoodcrawlers)
    print color.BOLD + '\n7.0 Fake use of a "known" crawler user-agent string(only first 25) : ' + color.END
    dfNotGoodCrawlers2 = dfNotGoodCrawlers
    dfNotGoodCrawlers2 = dfNotGoodCrawlers2.dropna()
    dfNotGoodCrawlers3 = dfNotGoodCrawlers2[dfNotGoodCrawlers2['Agent'].str.contains('yandex|msn|google|baidu|pingdom|Google|ahrefs', na=False)]
    if dfNotGoodCrawlers3.empty:
        print 'No Results Found!'
    else:
        print dfNotGoodCrawlers3[0:25]
    dfNotGoodCrawlers.drop_duplicates(cols='IP', take_last=False).to_csv('Not Known Crawlers', sep=' ', header=False, index=False)
    fakeuseragent = dfNotGoodCrawlers[dfNotGoodCrawlers['Agent'].str.contains('yandex|msn|google|baidu|pingdom|Google|ahrefs', na=False)][['IP', 'Agent', 'session']]
    fakeuseragentS = fakeuseragent.session
    allip = open('Not Known Crawlers').readlines()
    fo = open('blacklistIps', 'w')
    for line in allip:
        ips = line.strip().split(' ')[0]
        ip = str(ips).split('.')
        rev = '%s.%s.%s.%s' % (ip[3], ip[2], ip[1], ip[0])
        spamdbs = ['.cbl.abuseat.org', '.zen.spamhaus.org']
        for db in spamdbs:
            if db == '.pbl.spamhaus.org':
                break
            p = subprocess.Popen(['dig', '+short', rev + db], stdout=subprocess.PIPE)
            output, err = p.communicate()
            if output != '':
                fo.write(db + ',' + ips + '\n')

    key = 'ornrkapawxsj'
    bl = httpbl.HttpBL(key)
    res = []
    honeypotips = []
    for line in allip:
        ips = line.strip().split(' ')[0]
        response = bl.query(ips)
        if response['threat_score'] > 50:
            res.extend((ips, response['threat_score'], response['type']))
            honeypotips.append(ips)

    fo.close()
    myfile = open('honeypot', 'w')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(honeypotips)
    if os.path.getsize('honeypot') > 0:
        print honeypotips
        print color.BOLD + '\n8.0 Honeypot Project Crawlers\n' + color.END
        print dfNotGoodCrawlers[dfNotGoodCrawlers['IP'].isin(honeypotips)][['IP', 'Agent', 'Verified']].drop_duplicates(cols='IP', take_last=False)
    if os.path.getsize('blacklistIps') > 0:
        dfMalicious = pd.read_csv('blacklistIps', sep=',', header=None)
        dfMalicious.columns = ['BlacklistDatabase', 'IP']
        joinedMalicious = dfMalicious.groupby('IP').agg(lambda x: (', ').join(x.values))
        dfMaliciousNew = pd.DataFrame(joinedMalicious)
        dfMaliciousNew = dfMaliciousNew.reset_index()
        malIP = dfMaliciousNew.IP
        dfdata = dfNotGoodCrawlers[dfNotGoodCrawlers['IP'].isin(malIP)][['IP', 'Agent', 'Verified']].drop_duplicates(cols='IP', take_last=False)
        dfMaliciousCrawlers1 = pd.DataFrame(dfdata)
        test = pd.merge(dfMaliciousCrawlers1, dfMaliciousNew, how='inner')
        dfMaliciousCrawlers2 = pd.DataFrame(test)
        dfMaliciousCrawlers2 = dfMaliciousCrawlers2.reset_index()
        dfMaliciousCrawlersIPs = dfMaliciousCrawlers2.IP.unique()
        dfMaliciousCrawlersSessions = dfNotGoodCrawlers[dfNotGoodCrawlers['IP'].isin(dfMaliciousCrawlersIPs)][['session']].drop_duplicates(cols='session', take_last=False)
        blacklistip1 = pd.DataFrame(dfMaliciousCrawlersSessions)
        blacklistip1.columns = ['session']
        blacklistip2 = pd.DataFrame(fakeuseragentS)
        blacklistip2.columns = ['session']
        multiuseragentS = dfNotGoodCrawlers[dfNotGoodCrawlers['IP'].isin(multiuseragentIPs)][['session']].drop_duplicates(cols='session', take_last=False)
        blacklistip3 = pd.DataFrame(multiuseragentS)
        blacklistip3.columns = ['session']
        blacklistip5 = pd.DataFrame(blankagents.session.unique())
        blacklistip5.columns = ['session']
        blacklistip6 = pd.DataFrame(hiddenlinkaccessedType3.session.unique())
        blacklistip6.columns = ['session']
        IPmerge1 = pd.merge(blacklistip1, blacklistip2, how='outer')
        IPmerge2 = pd.merge(IPmerge1, blacklistip3, how='outer')
        IPmerge4 = pd.merge(IPmerge2, blacklistip5, how='outer')
        anomalousIPS = pd.merge(IPmerge4, blacklistip6, how='outer')
        anomalousips = anomalousIPS.session
        dfanodata = dfNotGoodCrawlers[dfNotGoodCrawlers['session'].isin(anomalousips)][['IP', 'Agent', 'Verified', 'session']].drop_duplicates(cols='session', take_last=False)
        dfanomalousCrawlers = pd.DataFrame(dfanodata)
        anomaloussessions = dfanomalousCrawlers.session
        dfanomalousCrawlers.to_csv('Suspicious Crawlers', sep=',', header=False, index=False)
        print color.BOLD + '\n9.0 No of "suspicious" crawler sessions : ' + color.END + str(len(dfanomalousCrawlers.drop_duplicates(cols='session', take_last=False)))
        other = dfNotGoodCrawlers[(~dfNotGoodCrawlers['session'].isin(anomaloussessions))][['IP', 'Agent', 'session']].drop_duplicates(cols='session', take_last=False)
        dfOther = pd.DataFrame(other)
        print color.BOLD + '\n10.0 No of "other" crawler sessions : ' + color.END + str(len(dfOther.drop_duplicates(cols='session', take_last=False)))
        dfOther.to_csv('Other Crawlers', sep=',', header=False, index=False)
    else:
        blacklistip2 = pd.DataFrame(fakeuseragentIPs)
        blacklistip2.columns = ['IP']
        blacklistip3 = pd.DataFrame(multiuseragentIPs)
        blacklistip3.columns = ['IP']
        blacklistip5 = pd.DataFrame(blankagents.IP.unique())
        blacklistip5.columns = ['IP']
        IPmerge1 = pd.merge(blacklistip2, blacklistip3, how='outer')
        anomalousIPS = pd.merge(IPmerge1, blacklistip5, how='outer')
        dfanodata = dfNotGoodCrawlers[dfNotGoodCrawlers['session'].isin(anomalousips)][['IP', 'Agent', 'Verified', 'session']].drop_duplicates(cols='session', take_last=False)
        dfanomalousCrawlers = pd.DataFrame(dfanodata)
        anomaloussessions = dfanomalousCrawlers.session
        dfanomalousCrawlers.to_csv('Suspicious Crawlers', sep=',', header=False, index=False)
        print color.BOLD + '\n9.0 No of "suspicious" crawler sessions : ' + color.END + str(len(dfanomalousCrawlers.drop_duplicates(cols='session', take_last=False)))
        print dfanomalousCrawlers[0:25]
        other = dfNotGoodCrawlers[(~dfNotGoodCrawlers['session'].isin(anomaloussessions))][['IP', 'Agent', 'session']].drop_duplicates(cols='session', take_last=False)
        dfOther = pd.DataFrame(other)
        print color.BOLD + '\n10.0 No of "other" crawler sessions : ' + color.END + len(dfOther.drop_duplicates(cols='session', take_last=False))
        dfOther.to_csv('Other Crawlers', sep=',', header=False, index=False)
    return