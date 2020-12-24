# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\tests\doctest_webstring.py
# Compiled at: 2006-12-06 22:08:38
"""Doctests for webstring"""

def _test():
    '''
    >>> from webstring import Template
    >>> example = Template("""<rss version="2.0">
    ...  <channel>
    ...   <title>Example</title>
    ...   <link>http://www.example.org/</link>
    ...   <description>RSS Example</description>
    ...   <language>en-us</language>
    ...   <pubDate id="cpubdate">$month $day, $year</pubDate>
    ...   <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
    ...   <item class="item">
    ...    <title id="title" />
    ...    <link id="link" />
    ...    <guid id="guid" isPermaLink="true" />
    ...    <description id="description" />
    ...    <pubDate id="ipubdate" />
    ...   </item>
    ...  </channel>
    ...  </rss>""")
    >>> example.exclude('cpubdate', 'guid') 
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example.include('cpubdate', 'guid') 
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example.cpubdate.text = {'month':'June', 'day':'06', 'year':'2006'}
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example.lastbuilddate.text = {'month':'June', 'day':'06', 'year':'2006'}
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example.item.description.text = 'Example of assigning text to a field.' 
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> print example.lastbuilddate.template
    %(month)s %(day)s, %(year)s
    >>> example.item.link.template = 'http://www.example.com/rss/$id'
    >>> example.item.link.text = {'id':'5423093'}
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="guid" isPermaLink="true" />
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example.item.templates({'title':{'text':'Example Title: $content'}, 'ipubdate':{'text':'$month $day, $year'}})
    >>> example.item.title.text = {'content':'First Example'}
    >>> example.item.ipubdate.text = {'month':'June', 'day':'6', 'year':'2006'}
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="guid" isPermaLink="true" />
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 6, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.item.guid.update({'isPermaLink':'true', 'id':'GUID', '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource':'http://www.example.com/rss/5423093'})
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="GUID" isPermaLink="true" rdf:resource="http://www.example.com/rss/5423093" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" />
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 6, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.item.guid.atemplates({'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource':'http://www.example.com/rss/$guid'})
    >>> example.item.guid.update({'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource':{'guid':'5423094'}})
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="GUID" isPermaLink="true" rdf:resource="http://www.example.com/rss/5423094" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" />
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 6, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.item.guid.resource = {'guid':'5423093'}
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="GUID" isPermaLink="true" rdf:resource="http://www.example.com/rss/5423093" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" />
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 6, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.item.guid.purge('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="GUID" isPermaLink="true" />
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 6, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.item.guid.text = 'http://www.example.com/rss/5423093'
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="GUID" isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 6, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.reset()
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example %= {
    ... 'cpubdate':{'text':{'month':'June', 'day':'06', 'year':'2006'}}, 
    ... 'lastbuilddate':{'text':{'month':'June', 'day':'06', 'year':'2006'}},
    ... 'item':{'templates':{'title':{'text':'Example Title: $content'}, 'ipubdate':{'text':'$month $day, $year'},
    ...         'link':{'text':'http://www.example.com/rss/$id'}},
    ...         'title':{'text':{'content':'First Example'}},
    ...         'link':{'text':{'id':'5423093'}},
    ...         'guid':{'attrib':{'id':'GUID'}, 'text':'http://www.example.com/rss/5423093'},
    ...         'description':{'text':'Example of assigning text to a field.'},
    ...         'ipubdate':{'text':{'month':'June', 'day':'6', 'year':'2006'}}}}
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="GUID" isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 6, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.cpubdate %= {'text':{'month':'June', 'day':'06', 'year':'2006'}}
    >>> example.lastbuilddate %= {'text':{'month':'June', 'day':'06', 'year':'2006'}}
    >>> example.item %= {
    ... 'templates':{
    ...     'title':{'text':'Example Title: $content'},
    ...     'ipubdate':{'text':'$month $day, $year'},
    ...     'link':{'text':'http://www.example.com/rss/$id'}},
    ... 'subs':((
    ...     {'text':{'content':'First Example'}},
    ...     {'text':{'id':'5423093'}}, {'attrib':{'id':'GUID'},
    ...     'text':'http://www.example.com/rss/5423093'},
    ...     'Example of assigning text to a field.',
    ...     {'text':{'month':'June', 'day':'6', 'year':'2006'}}),)}
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="GUID" isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 6, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> print example.current
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="GUID" isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 6, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> print example.default
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example.reset()
    >>> print example + example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss></rss>
    >>> print example.item + example.item
    <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
    <BLANKLINE>
    >>> print example.item.title + example.item.title
    <title id="title" />
       <title id="title" />
    <BLANKLINE>
    >>> example.item += example.item
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example.reset()
    >>> example.item.repeat()
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example.reset()
    >>> example.item *= 2
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     <item class="item">
       <title id="title" />
       <link id="link" />
       <guid id="guid" isPermaLink="true" />
       <description id="description" />
       <pubDate id="ipubdate" />
      </item>
     </channel>
     </rss>
    >>> example.reset()
    >>> example.item %= ('Example Title: First Example', 'http://www.example.com/rss/5423092', 'http://www.example.com/rss/5423092', 'Example of assigning text to a field.', 'June 06, 2006')
    >>> example.item.repeat(('Example Title: Second Example', 'http://www.example.com/rss/5423093', 'http://www.example.com/rss/5423093', 'Example of group repetition.', 'June 06, 2006'))
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423092</link>
       <guid id="guid" isPermaLink="true">http://www.example.com/rss/5423092</guid>
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 06, 2006</pubDate>
      </item>
     <item class="item">
       <title id="title">Example Title: Second Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="guid" isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description id="description">Example of group repetition.</description>
       <pubDate id="ipubdate">June 06, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.reset()
    >>> example.item **= (('Example Title: First Example', 'http://www.example.com/rss/5423092', 'http://www.example.com/rss/5423092', 'Example of assigning text to a field.', 'June 06, 2006'),
    ... ('Example Title: Second Example', 'http://www.example.com/rss/5423093', 'http://www.example.com/rss/5423093', 'Example of group repetition.', 'June 06, 2006'))
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423092</link>
       <guid id="guid" isPermaLink="true">http://www.example.com/rss/5423092</guid>
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 06, 2006</pubDate>
      </item>
     <item class="item">
       <title id="title">Example Title: Second Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="guid" isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description id="description">Example of group repetition.</description>
       <pubDate id="ipubdate">June 06, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.reset()
    >>> example.item %= {'templates':{'title':{'text':'Example Title: $content'}, 'ipubdate':{'text':'$month $day, $year'}, 'link':{'text':'http://www.example.com/rss/$id'}},
    ... 'subs':(
    ... ({'text':{'content':'First Example'}}, {'text':{'id':'5423092'}}, 'http://www.example.com/rss/5423092', 
    ... 'Example of assigning text to a field.', {'text':{'month':'June', 'day':'06', 'year':'2006'}}),
    ... ({'text':{'content':'Second Example'}}, {'text':{'id':'5423093'}}, 'http://www.example.com/rss/5423093', 
    ... 'Example of group repetition.', {'text':{'month':'June', 'day':'06', 'year':'2006'}}))}
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">$month $day, $year</pubDate>
      <lastBuildDate id="lastbuilddate">%(month)s %(day)s, %(year)s</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423092</link>
       <guid id="guid" isPermaLink="true">http://www.example.com/rss/5423092</guid>
       <description id="description">Example of assigning text to a field.</description>
       <pubDate id="ipubdate">June 06, 2006</pubDate>
      </item>
     <item class="item">
       <title id="title">Example Title: Second Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="guid" isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description id="description">Example of group repetition.</description>
       <pubDate id="ipubdate">June 06, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> example.reset()
    >>> example.cpubdate.text = {'month':'June', 'day':'06', 'year':'2006'}
    >>> example.lastbuilddate.text = {'month':'June', 'day':'06', 'year':'2006'}
    >>> example.item %= {'templates':{'title':{'text':'Example Title: $content'}, 'ipubdate':{'text':'$month $day, $year'}, 'link':{'text':'http://www.example.com/rss/$id'}},
    ... 'subs':(
    ... ({'text':{'content':'First Example'}}, {'text':{'id':'5423092'}}, 'http://www.example.com/rss/5423092', 
    ... 'Example of assigning text to a field.', {'text':{'month':'June', 'day':'06', 'year':'2006'}}),
    ... ({'text':{'content':'Second Example'}}, {'text':{'id':'5423093'}}, 'http://www.example.com/rss/5423093', 
    ... 'Example of group repetition.', {'text':{'month':'June', 'day':'06', 'year':'2006'}}))}
    >>> example.item.description.append(Template('<html><head><title>Example</title></head><body><p>Paragraph</p></body></html>'))
    >>> del example.item.description.text
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate id="cpubdate">June 06, 2006</pubDate>
      <lastBuildDate id="lastbuilddate">June 06, 2006</lastBuildDate>
      <item class="item">
       <title id="title">Example Title: First Example</title>
       <link id="link">http://www.example.com/rss/5423092</link>
       <guid id="guid" isPermaLink="true">http://www.example.com/rss/5423092</guid>
       <description id="description"><html><head><title>Example</title></head><body><p>Paragraph</p></body></html></description>
       <pubDate id="ipubdate">June 06, 2006</pubDate>
      </item>
     <item class="item">
       <title id="title">Example Title: Second Example</title>
       <link id="link">http://www.example.com/rss/5423093</link>
       <guid id="guid" isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description id="description">Example of group repetition.</description>
       <pubDate id="ipubdate">June 06, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> del example.mark
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate>June 06, 2006</pubDate>
      <lastBuildDate>June 06, 2006</lastBuildDate>
      <item class="item">
       <title>Example Title: First Example</title>
       <link>http://www.example.com/rss/5423092</link>
       <guid isPermaLink="true">http://www.example.com/rss/5423092</guid>
       <description><html><head><title>Example</title></head><body><p>Paragraph</p></body></html></description>
       <pubDate>June 06, 2006</pubDate>
      </item>
     <item class="item">
       <title>Example Title: Second Example</title>
       <link>http://www.example.com/rss/5423093</link>
       <guid isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description>Example of group repetition.</description>
       <pubDate>June 06, 2006</pubDate>
      </item>
     </channel>
     </rss>
    >>> del example.groupmark
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate>June 06, 2006</pubDate>
      <lastBuildDate>June 06, 2006</lastBuildDate>
      <item>
       <title>Example Title: First Example</title>
       <link>http://www.example.com/rss/5423092</link>
       <guid isPermaLink="true">http://www.example.com/rss/5423092</guid>
       <description><html><head><title>Example</title></head><body><p>Paragraph</p></body></html></description>
       <pubDate>June 06, 2006</pubDate>
      </item>
     <item>
       <title>Example Title: Second Example</title>
       <link>http://www.example.com/rss/5423093</link>
       <guid isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description>Example of group repetition.</description>
       <pubDate>June 06, 2006</pubDate>
      </item>
     </channel>
     </rss>'''
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()