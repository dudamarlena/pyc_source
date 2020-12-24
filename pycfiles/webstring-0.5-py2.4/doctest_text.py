# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\tests\doctest_text.py
# Compiled at: 2007-01-03 01:19:31
"""Doctests for webstring text"""

def _test():
    '''
    >>> from webstring import Template
    >>> example = Template("""<rss version="2.0">
    ...  <channel>
    ...   <title>Example</title>
    ...   <link>http://www.example.org/</link>
    ...   <description>RSS Example</description>
    ...   <language>en-us</language>
    ...   $$cpubdate<pubDate>$month$ $day$, $year$</pubDate>$$
    ...   $$lastbuilddate<lastBuildDate>$month$ $day$, $year$</lastBuildDate>$$
    ...   $$item<item>
    ...    <title>$title$</title>
    ...    <link>$link$</link>
    ...    <guid isPermaLink="true">$guid$</guid>
    ...    <description>$description$</description>
    ...    <pubDate>$ipubdate$</pubDate>
    ...   </item>
    ...  $$</channel>
    ... </rss>""", format='text')
    >>> example.exclude('cpubdate') 
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     </channel>
    </rss>
    >>> example.include('cpubdate') 
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate> , </pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     </channel>
    </rss>
    >>> example.cpubdate %= {'month':'June', 'day':'06', 'year':'2006'}
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate>June 06, 2006</pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     </channel>
    </rss>
    >>> example.lastbuilddate %= {'month':'June', 'day':'06', 'year':'2006'}
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
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
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
      <pubDate>June 06, 2006</pubDate>
      <lastBuildDate>June 06, 2006</lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description>Example of assigning text to a field.</description>
       <pubDate></pubDate>
      </item>
     </channel>
    </rss>
    >>> example.item.link.text = 'http://www.example.com/rss/5423093'
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
       <title></title>
       <link>http://www.example.com/rss/5423093</link>
       <guid isPermaLink="true"></guid>
       <description>Example of assigning text to a field.</description>
       <pubDate></pubDate>
      </item>
     </channel>
    </rss>
    >>> example.item.title.text = 'Example Title: First Example'
    >>> example.item.ipubdate.text = 'June 6, 2006'
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
       <link>http://www.example.com/rss/5423093</link>
       <guid isPermaLink="true"></guid>
       <description>Example of assigning text to a field.</description>
       <pubDate>June 6, 2006</pubDate>
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
      <pubDate>June 06, 2006</pubDate>
      <lastBuildDate>June 06, 2006</lastBuildDate>
      <item>
       <title>Example Title: First Example</title>
       <link>http://www.example.com/rss/5423093</link>
       <guid isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description>Example of assigning text to a field.</description>
       <pubDate>June 6, 2006</pubDate>
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
      <pubDate> , </pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     </channel>
    </rss>
    >>> example %= {
    ... 'cpubdate':{'month':'June', 'day':'06', 'year':'2006'}, 
    ... 'lastbuilddate':{'month':'June', 'day':'06', 'year':'2006'},
    ... 'item':{'title':'Example Title: First Example',
    ...     'link':'http://www.example.com/rss/5423093',
    ...     'guid':'http://www.example.com/rss/5423093',
    ...     'description':'Example of assigning text to a field.',
    ...     'ipubdate':'June 6, 2006'}}
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
       <link>http://www.example.com/rss/5423093</link>
       <guid isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description>Example of assigning text to a field.</description>
       <pubDate>June 6, 2006</pubDate>
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
      <pubDate>June 06, 2006</pubDate>
      <lastBuildDate>June 06, 2006</lastBuildDate>
      <item>
       <title>Example Title: First Example</title>
       <link>http://www.example.com/rss/5423093</link>
       <guid isPermaLink="true">http://www.example.com/rss/5423093</guid>
       <description>Example of assigning text to a field.</description>
       <pubDate>June 6, 2006</pubDate>
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
      <pubDate> , </pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
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
      <pubDate> , </pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     </channel>
    </rss><rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate> , </pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     </channel>
    </rss>
    >>> print example.item + example.item
    <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
    <BLANKLINE>
    >>> print example.item.title + example.item.title
    <BLANKLINE>
    >>> example.item += example.item
    >>> print example.item
    <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
    <BLANKLINE>
    >>> example.reset()
    >>> example.item.repeat()
    >>> print example
    <rss version="2.0">
     <channel>
      <title>Example</title>
      <link>http://www.example.org/</link>
      <description>RSS Example</description>
      <language>en-us</language>
      <pubDate> , </pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
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
      <pubDate> , </pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
      </item>
     <item>
       <title></title>
       <link></link>
       <guid isPermaLink="true"></guid>
       <description></description>
       <pubDate></pubDate>
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
      <pubDate> , </pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title>Example Title: First Example</title>
       <link>http://www.example.com/rss/5423092</link>
       <guid isPermaLink="true">http://www.example.com/rss/5423092</guid>
       <description>Example of assigning text to a field.</description>
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
      <pubDate> , </pubDate>
      <lastBuildDate> , </lastBuildDate>
      <item>
       <title>Example Title: First Example</title>
       <link>http://www.example.com/rss/5423092</link>
       <guid isPermaLink="true">http://www.example.com/rss/5423092</guid>
       <description>Example of assigning text to a field.</description>
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
    </rss>
    >>> example.cpubdate %= {'month':'June', 'day':'06', 'year':'2006'}
    >>> example.lastbuilddate %= {'month':'June', 'day':'06', 'year':'2006'}
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
       <description>Example of assigning text to a field.</description>
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