# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eyefi/twisted_flickrapi.py
# Compiled at: 2010-11-28 17:21:43
from twisted.web.client import getPage
from twisted.internet.defer import succeed
from flickrapi import FlickrAPI, rest_parsers, LOG, FlickrError

class TwistedFlickrAPI(FlickrAPI):

    def _FlickrAPI__flickr_call(self, **kwargs):
        LOG.debug('Calling %s' % kwargs)
        post_data = self.encode_and_sign(kwargs)
        if self.cache and self.cache.get(post_data):
            return defer.succeed(self.cache.get(post_data))
        else:
            url = 'http://' + FlickrAPI.flickr_host + FlickrAPI.flickr_rest_form
            reply = getPage(url, method='POST', postdata=post_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            if self.cache is not None:
                reply.addCallback(self._add_to_cache, post_data)
            return reply

    def _add_to_cache(self, reply, post_data):
        self.cache.set(post_data, reply)
        return reply

    def _FlickrAPI__wrap_in_parser(self, wrapped_method, parse_format, *args, **kwargs):
        if parse_format in rest_parsers and 'format' in kwargs:
            kwargs['format'] = 'rest'
        LOG.debug('Wrapping call %s(self, %s, %s)' % (wrapped_method, args,
         kwargs))
        data = wrapped_method(*args, **kwargs)
        if parse_format not in rest_parsers:
            return data
        parser = rest_parsers[parse_format]
        return data.addCallback(lambda resp: parser(self, resp))

    def _FlickrAPI__send_multipart(self, url, body, progress_callback=None):
        assert not progress_callback, 'twisted upload/replace does not support progress callbacks yet'
        LOG.debug('Uploading to %s' % url)
        reply = getPage(url, method='POST', postdata=str(body), headers=dict([body.header()]))
        return reply

    def trait_names(self):
        """
        ipython introspection needs to be synchornous, disable it
        """
        return

    def get_token_part_one(self, perms='read'):
        token = succeed(self.token_cache.token)

        @token.addCallback
        def check(token):
            if not token:
                return None
            else:
                LOG.debug("Trying cached token '%s'" % token)
                rsp = self.auth_checkToken(auth_token=token, format='xmlnode')

                @rsp.addCallback
                def check_get(rsp):
                    tokenPerms = rsp.auth[0].perms[0].text
                    if tokenPerms == 'read' and perms != 'read':
                        return None
                    else:
                        if tokenPerms == 'write' and perms == 'delete':
                            return None
                        return token

                @rsp.addErrback
                def check_err(err):
                    err.trap(FlickrError)
                    LOG.debug('Cached token invalid')
                    self.token_cache.forget()
                    return

                return rsp

        @token.addCallback
        def need_new(token):
            if token:
                return (token, None)
            else:
                LOG.debug('Getting frob for new token')
                rsp = self.auth_getFrob(auth_token=None, format='xmlnode')

                @rsp.addCallback
                def valid_frob(rsp):
                    frob = rsp.frob[0].text
                    self.validate_frob(frob, perms)
                    return (token, frob)

                return rsp

        return token

    def get_token(self, frob):
        rsp = self.auth_getToken(frob=frob, auth_token=None, format='xmlnode')

        @rsp.addCallback
        def extract_token(rsp):
            token = rsp.auth[0].token[0].text
            LOG.debug("get_token: new token '%s'" % token)
            self.token_cache.token = token
            return token

        return rsp

    def authenticate_console(self, perms='read'):
        d = self.get_token_part_one(perms)

        @d.addCallback
        def wait(arg):
            token, frob = arg
            if not token:
                print 'Press ENTER after you authorized this program'
                raw_input()
            return (
             token, frob)

        d.addCallback(self.get_token_part_two)
        return d


def main():
    from twisted.internet import reactor
    from twisted.python import log
    import logging
    log.PythonLoggingObserver().start()
    logging.getLogger().setLevel(level=logging.DEBUG)
    LOG.setLevel(level=logging.DEBUG)
    api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    api_secret = 'XXXXXXXXXXXX'
    flickr = TwistedFlickrAPI(api_key, api_secret)
    flickr.photos_search(user_id='73509078@N00', per_page='10').addBoth(log.msg).addBoth(lambda _: reactor.callLater(0, reactor.stop))
    reactor.run()


if __name__ == '__main__':
    main()