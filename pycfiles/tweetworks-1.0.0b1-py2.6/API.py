# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tweetworks/API.py
# Compiled at: 2009-07-06 21:00:43
"""
Generate Tweetworks API requests and handle the response.

Nicolas Ward
@ultranurd
ultranurd@yahoo.com
http://www.ultranurd.net/code/tweetworks/
2009.06.19
"""
import sys, os, urllib, urllib2, lxml.etree, tweetworks

class API:
    """
    Implement the Tweetworks API with HTTP POSTs.

    In general, API methods are named for their URL, and are organized by type:
    post-, group-, and user-related methods.
    """

    class TweetworksException(Exception):
        """
        Errors in handling Tweetworks API calls.
        """

        def __init__(self, value, url=''):
            self.url = url
            if url != '':
                self.parameter = '%s: %s' % (url, value)
            else:
                self.parameter = value

        def __str__(self):
            return repr(self.parameter)

    def __init__(self, api_key, username='', password=''):
        """
        We need a Tweetworks API key to send requests. Optionally specify a
        Tweetworks username and password to use those methods that require
        authentication.
        """
        self.api_key = api_key
        if username != '' and password != '':
            password_mgr = urllib2.HTTPPasswordMgr()
            password_mgr.add_password('Login please', 'http://www.tweetworks.com', username, password)
            auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            self.auth = urllib2.build_opener(auth_handler)
        else:
            self.auth = None
        return

    def __request(self, url, data={}):
        """
        POST the data (if any) to the specified URL, and return the parsed
        XML. An exception is thrown if there was an error.
        """
        data['data[key]'] = self.api_key
        encoded_data = urllib.urlencode(data)
        request = urllib2.Request(url, encoded_data)
        try:
            if self.auth != None:
                response = self.auth.open(request)
            else:
                response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            if e.code == 401:
                raise API.TweetworksException('Authentication required', url)
            else:
                raise API.TweetworksException(str(e), url)

        xml_response = lxml.etree.parse(response)
        error = xml_response.xpath('/error/text/text()')
        if len(error) > 0:
            raise API.TweetworksException(error[0], url)
        return xml_response

    def __request_all_pages(self, url, page_reader, data={}):
        """
        Repeatedly requests the specified URL with the specified POST data,
        incrementing the page by 1 until no new pages are available. Each page
        is read by the specified reader to convert XML into a list of objects,
        which are appended. The final output list is returned.

        url must be specified ending in ? or & as appropriate for the query.
        """
        items = []
        page = 1
        last_items_xml_string = ''
        while True:
            paged_url = '%spage=%d' % (url, page)
            items_xml = self.__request(paged_url, data)
            items_xml_string = lxml.etree.tostring(items_xml)
            if last_items_xml_string == items_xml_string:
                break
            items = items + page_reader(items_xml)
            last_items_xml_string = items_xml_string
            page = page + 1

        return items

    def __read_post_xml(self, posts_xml):
        """
        Converts a <posts> element to a list of Post objects.
        """
        posts = []
        for post_xml in posts_xml.xpath('/posts/post'):
            post_string = lxml.etree.tostring(post_xml)
            posts.append(Post.Post(lxml.etree.fromstring(post_string)))

        return posts

    def __paginate_posts(self, url_prefix, sort_by_updated=False, pages=None, all=False, before_id=None, after_id=None):
        """
        Retrieves posts at the specified URL, paginating if necessary according
        to the options.

        sort_by_updated - Whether posts should be sorted in descending creation
                          order or by descending last updated order.

        pages - An optional list of specific pages to retrieve.
        all - Whether all posts at this URL should be retrieved.

        before_id - Retrieve posts created/updated before the specified post
        after_id - Retrieve posts created/updated after the specified post

        If no paging options are specified, 20 posts matching the criteria are
        retrieved.
        """
        url = '%s/%s.xml' % (url_prefix, ('newest', 'updated')[sort_by_updated])
        if before_id != None:
            url += '?beforeId=%d' % before_id
            if after_id != None:
                url += '&afterId=%d' % after_id
        elif after_id != None:
            url += '?afterId=%d' % after_id
        if pages != None:
            if all:
                raise API.TweetworksException('Conflicting pages requested')
            posts = []
            for page in pages:
                if before_id != None or after_id != None:
                    page_url = '%s&page=%d' % (url, page)
                else:
                    page_url = '%s?page=%d' % (url, page)
                posts = posts + self.__read_post_xml(self.__request(page_url))

            return posts
        else:
            if all:
                return self.__request_all_pages(url + '&', self.__read_post_xml)
            else:
                return self.__read_post_xml(self.__request(url))
            return

    def __read_group_xml(self, groups_xml):
        """
        Converts a <groups> element to a list of Group objects.
        """
        groups = []
        for group_xml in groups_xml.xpath('/groups/group'):
            group_string = lxml.etree.tostring(group_xml)
            groups.append(tweetworks.Group(lxml.etree.fromstring(group_string)))

        return groups

    def __paginate_groups(self, url, data={}, pages=None, all=False):
        """
        Retrieves groups at the specified URL, paginating if necessary according
        to the options.

        data - Any additional data to add to the request.

        pages - An optional list of specific pages to retrieve.
        all - Whether all posts at this URL should be retrieved.

        If no paging options are specified, 30 groups matching the criteria are
        retrieved.
        """
        if pages != None:
            if all:
                raise API.TweetworksException('Conflicting pages requested')
            groups = []
            for page in pages:
                page_url = '%s?page=%d' % (url, page)
                groups = groups + self.__read_group_xml(self.__request(page_url, data))

            return groups
        else:
            if all:
                return self.__request_all_pages(url + '?', self.__read_group_xml, data)
            else:
                return self.__read_group_xml(self.__request(url, data))
            return

    def __read_user_xml(self, users_xml):
        """
        Converts a <users> element to a list of User objects.
        """
        users = []
        for user_xml in users_xml.xpath('/users/user'):
            user_string = lxml.etree.tostring(user_xml)
            users.append(User.User(lxml.etree.fromstring(user_string)))

        return users

    def __paginate_users(self, url, data={}, pages=None, all=False):
        """
        Retrieves users at the specified URL, paginating if necessary according
        to the options.

        data - Any additional data to add to the request.

        pages - An optional list of specific pages to retrieve.
        all - Whether all posts at this URL should be retrieved.

        If no paging options are specified, 30 users matching the criteria are
        retrieved.
        """
        if pages != None:
            if all:
                raise API.TweetworksException('Conflicting pages requested')
            users = []
            for page in pages:
                page_url = '%s?page=%d' % (url, page)
                users = users + self.__read_user_xml(self.__request(page_url, data))

            return users
        else:
            if all:
                return self.__request_all_pages(url + '?', self.__read_user_xml, data)
            else:
                return self.__read_user_xml(self.__request(url, data))
            return

    def add_posts(self, body, group_id=None, parent_id=None, tweet=False):
        """
        Submits a post with the specified body text as the authenticated user.
        The destination group ID is optional (if none, the post will be public);
        the parent ID is optional (if none, the post will be top-level);
        the post can be optionally sent to Twitter. If a parent ID is supplied
        for a group post, the group ID is not necessary.

        Requires authentication; post will originate from that user.
        """
        url = 'http://www.tweetworks.com/posts/add.xml'
        data = {'data[Post][body]': body, 'data[Post][groupId]': (
                                 '', str(group_id))[(group_id != None)], 
           'data[Post][parentId]': (
                                  '', str(parent_id))[(parent_id != None)], 
           'data[Post][sendToTwitter]': (0, 1)[tweet]}
        return Post.Post(self.__request(url, data))

    def contributed_posts(self, username, sort_by_updated=False, pages=None, all=False, before_id=None, after_id=None):
        """
        Retrieves posts contributed by the specified user, selected by the
        specified optional criteria.

        Requires authentication from the specified user.
        """
        url_prefix = 'http://www.tweetworks.com/posts/contributed/%s' % username
        return self.__paginate_posts(url_prefix, sort_by_updated, pages, all, before_id, after_id)

    def group_posts(self, group, sort_by_updated=False, pages=None, all=False, before_id=None, after_id=None):
        """
        Retrieves posts contained in the specified group, selected by the
        specified optional criteria.

        A private group requires authentication from a user in that group.
        """
        url_prefix = 'http://www.tweetworks.com/posts/group/%s' % group
        return self.__paginate_posts(url_prefix, sort_by_updated, pages, all, before_id, after_id)

    def index_posts(self, sort_by_updated=False, pages=None, all=False, before_id=None, after_id=None):
        """
        Retrieves all posts, selected by the specified optional criteria.
        """
        url_prefix = 'http://www.tweetworks.com/posts/index'
        return self.__paginate_posts(url_prefix, sort_by_updated, pages, all, before_id, after_id)

    def joined_groups_posts(self, username, sort_by_updated=False, pages=None, all=False, before_id=None, after_id=None):
        """
        Retrieves posts contained in all of the groups joined by the specified
        user, selected by the specified optional criteria.

        Requires authentication from the specified user.
        """
        url_prefix = 'http://www.tweetworks.com/posts/joined_groups/%s' % username
        return self.__paginate_posts(url_prefix, sort_by_updated, pages, all, before_id, after_id)

    def view_posts(self, id):
        """
        Retrieves a single discussion and threaded list of replies.
        """
        url = 'http://www.tweetworks.com/posts/view/%d.xml' % id
        posts = self.__read_post_xml(self.__request(url))
        if len(posts) == 1:
            return posts[0]
        raise API.TweetworksException('%d posts were returned' % len(posts), url)

    def index_groups(self, pages=None, all=False):
        """
        Retrieves all Tweetworks groups, selected by the specified optional
        criteria.
        """
        url = 'http://www.tweetworks.com/groups/index.xml'
        return self.__paginate_groups(url, {}, pages, all)

    def join_groups(self, group):
        """
        Join the specified Tweetworks group as the authenticated user.

        Requires authentication; the authenticated user will join the group.
        """
        url = 'http://www.tweetworks.com/groups/join/%s.xml' % group
        groups = self.__read_group_xml(self.__request(url))
        if len(groups) == 1:
            return groups[0]
        raise API.TweetworksException('%d groups were joined' % len(posts), url)

    def joined_groups(self, username, pages=None, all=False):
        """
        Retrieves all groups of which the specified user is a member, selected
        by the specified optional criteria.

        Requires authentication from the specified user.
        """
        url = 'http://www.tweetworks.com/groups/joined/%s.xml' % username
        return self.__paginate_groups(url, {}, pages, all)

    def search_groups(self, query):
        """
        Searches groups for the specified query string, including name,
        description, and posts. Always returns all matches.
        """
        url = 'http://www.tweetworks.com/groups/search.xml'
        data = {'data[query]': query}
        return self.__paginate_groups(url, data, all=True)

    def group_users(self, group, pages=None, all=False):
        """
        Retrieves all users who are members of the specified group, selected
        by the specified optional criteria.
        """
        url = 'http://www.tweetworks.com/users/group/%s.xml' % group
        return self.__paginate_users(url, {}, pages, all)

    def index_users(self, pages=None, all=False):
        """
        Retrieves all Tweetworks users, selected by the specified optional
        criteria.
        """
        url = 'http://www.tweetworks.com/users/index.xml'
        return self.__paginate_users(url, {}, pages, all)

    def search_users(self, query):
        """
        Searches usernames and real names for the specified query string. Always
        returns all matches.
        """
        url = 'http://www.tweetworks.com/users/search.xml'
        data = {'data[query]': query}
        return self.__paginate_users(url, data, all=True)