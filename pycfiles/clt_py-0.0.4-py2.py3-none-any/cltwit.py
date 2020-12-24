# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cltwit/cltwit.py
# Compiled at: 2013-01-28 13:40:36
__doc__ = '\nUsage :\ncltwit [OPTIONS]\nOptions :\n-f : Follow (ajouter des personnes qui vous suivent et que vous ne suivez pas)\n-u : Unfollow (cesser de suivre les personnes que vous suivez et qui vous ne suivent pas)\n-t "message de 140 caractères maximum" : Tweet (envoyer un tweet)\n-o (ou --output) FILENAME : Output (exporter l\'intégralité de vos tweets dans le fichier FILENAME)\n'
import ConfigParser, webbrowser, sys, getopt, os, gettext
APP_NAME = 'cltwit'
LOC_PATH = os.path.dirname(__file__) + '/locale'
gettext.find(APP_NAME, LOC_PATH)
gettext.install(APP_NAME, LOC_PATH, True)
try:
    import tweepy
except ImportError:
    print _('Veuillez installer tweetpy https://github.com/tweepy/tweepy')
    sys.exit()

def checkconfig():
    u"""Récupérer la configuration ou la créer"""
    configfile = os.path.expanduser('~/.config/cltwit.conf')
    config = ConfigParser.RawConfigParser()
    try:
        config.read(configfile)
        if config.has_option('twitterapi', 'access_token'):
            access_token = config.get('twitterapi', 'access_token')
        if config.has_option('twitterapi', 'access_password'):
            access_password = config.get('twitterapi', 'access_password')
    except:
        pass

    if not (config.has_option('twitterapi', 'access_token') and config.has_option('twitterapi', 'access_password')):
        auth = tweepy.OAuthHandler('Jus1rnqM6S0WojJfOH1kQ', 'AHQ5sTC8YYArHilXmqnsstOivY6ygQ2N27L1zBwk')
        while True:
            try:
                webbrowser.open(auth.get_authorization_url())
                var = raw_input(_("Entrez le num d'autorisation !\n"))
                auth.get_access_token(var)
            except Exception as e:
                print str(e)
                continue

            break

        var = auth.access_token
        access_password = str(var).split('&')[0].split('=')[1]
        access_token = str(var).split('&')[1].split('=')[1]
        try:
            try:
                cfgfile = open(configfile, 'w')
                if not config.has_section('twitterapi'):
                    config.add_section('twitterapi')
                config.set('twitterapi', 'access_token', access_token)
                config.set('twitterapi', 'access_password', access_password)
                config.write(cfgfile)
            except IOError:
                pass

        finally:
            cfgfile.close

    else:
        auth = tweepy.OAuthHandler('Jus1rnqM6S0WojJfOH1kQ', 'AHQ5sTC8YYArHilXmqnsstOivY6ygQ2N27L1zBwk')
        auth.set_access_token(access_token, access_password)
    return auth


def process_tweet(tdate, tweet, outputfile):
    try:
        tweetlist = open(outputfile, 'a')
        try:
            tweetutf8 = tweet.encode('UTF-8')
            tweetlist.write('-' * 227 + '\n')
            tweetlist.write(tdate.strftime('%Y-%m-%d %H:%M') + '|' + tweetutf8 + '\n')
        finally:
            tweetlist.close()

    except IOError:
        pass


def export_tweets_list(api, outputfile, twittername):
    u"""Créer un fichier avec l'ensemble des tweets"""
    print _(('Création de la liste des tweets de ').decode('utf-8')) + twittername
    page_list = []
    for page in tweepy.Cursor(api.user_timeline, count=200, include_rts=True).pages(16):
        page_list.append(page)

    for page in page_list:
        for status in page:
            process_tweet(status.created_at, status.text, outputfile)

    print _(('Fichier %s écrit').decode('utf-8')) % outputfile


def get_friends_followers(api):
    """Renvoie la liste des id des friends et followers"""
    friend_id = []
    follower_id = []
    print _(('Récupération des Followers...').decode('utf-8'))
    for follower in tweepy.Cursor(api.followers).items():
        follower_id.append(follower.id)

    print _(('Récupération des Friends...\n').decode('utf-8'))
    for friend in tweepy.Cursor(api.friends).items():
        friend_id.append(friend.id)

    return (
     friend_id, follower_id)


def get_diff(liste1, liste2):
    """Renvoie les objets de liste1 qui ne sont pas dans liste2"""
    return list(set(liste1).difference(set(liste2)))


def follow_users(api, user):
    """Suivre une personne"""
    try:
        api.create_friendship(user)
        print _('Vous suivez maintenant %s') % api.get_user(user).screen_name
    except Exception as e:
        print e


def unfollow_user(api, user):
    """Cesser de suivre une personne"""
    try:
        api.destroy_friendship(user)
        print _('Vous ne suivez plus %s') % api.get_user(user).screen_name
    except Exception as e:
        print e


def main(argv=None):
    """Traitement des arguments"""
    if argv is None:
        argv = sys.argv
    if len(argv) == 1:
        help()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hfut:o:', [
         'help', 'follow', 'unfollow', 'tweet', 'output'])
    except getopt.GetoptError as err:
        print err
        help()
        sys.exit()

    for option, value in opts:
        if option in ('-f', '--follow'):
            traitement('f', None)
        if option in ('-u', '--unfollow'):
            traitement('u', None)
        if option in ('-h', '--help'):
            help()
        if option in ('-o', '--output'):
            traitement('o', value)
        if option in ('-t', '--tweet'):
            traitement('t', value)
        else:
            sys.exit()

    return


def traitement(option, value):
    """Traitement principal"""
    auth = checkconfig()
    api = tweepy.API(auth)
    twittername = api.me().screen_name
    print _(('Authentifié avec le user twitter %s\n').decode('utf-8')) % twittername
    if option == 'o':
        print _('Voulez exporter vos tweets') + _('dans le fichier texte %s? (o/N)') % value
        reponse = raw_input('> ')
        if reponse.lower() == 'o' or reponse.lower() == 'y':
            export_tweets_list(api, value, twittername)
        sys.exit()
    if option == 't':
        if len(value) < 141:
            api.update_status(value)
        else:
            print _(('La limite pour un tweet est de 140 caractères, votre message').decode('utf-8')) + _((' fait %s caractères de trop').decode('utf-8')) % str(len(value) - 140)
        sys.exit()
    friend_id, follower_id = get_friends_followers(api)
    follow_liste = get_diff(follower_id, friend_id)
    unfollow_liste = get_diff(friend_id, follower_id)
    if option == 'u':
        print _('Vous suivez %s personnes qui ne vous suivent pas.\n') % len(unfollow_liste)
        print _('Voulez changer cela ? (o/N)')
        reponse = raw_input('> ')
        if reponse.lower() == 'o' or reponse.lower() == 'y':
            for user in unfollow_liste:
                print _('Voulez-vous cesser de suivre %s ? (o/N)') % api.get_user(user).screen_name
                reponse = raw_input('> ')
                if reponse.lower() == 'o' or reponse.lower() == 'y':
                    unfollow_user(api, user)

    if option == 'f':
        print _('%s personnes vous suivent alors que vous ne les suivez pas.\n') % len(follow_liste)
        print _('Voulez changer cela ? (o/N)')
        reponse = raw_input('> ')
        if reponse.lower() == 'o' or reponse.lower() == 'y':
            for user in follow_liste:
                print _('Voulez-vous suivre %s ? (o/N)') % api.get_user(user).screen_name
                reponse = raw_input('> ')
                if reponse.lower() == 'o' or reponse.lower() == 'y':
                    follow_user(api, user)


def help():
    print _(('\nUsage :\ncltwit [OPTIONS]\nOptions :\n-f : Follow (ajouter des personnes qui vous suivent et que vous ne suivez pas)\n-u : Unfollow (cesser de suivre les personnes que vous suivez et qui vous ne suivent pas)\n-t "message de 140 caractères maximum" : Tweet (envoyer un tweet)\n-o (ou --output) FILENAME : Output (exporter l\'intégralité de vos tweets dans le fichier FILENAME)\n    ').decode('utf-8'))


if __name__ == '__main__':
    sys.exit(main())