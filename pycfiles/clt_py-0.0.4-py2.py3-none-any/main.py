# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cltwit/main.py
# Compiled at: 2013-02-03 16:48:21
__doc__ = '\nCltwit is a command line twitter utility\nAuthor : Jérôme Launay\nDate : 2013\n'
from sqlite2csv import sqlite2csv
from cltwitdb import cltwitdb
from utils import LocalTimezone
from cltwitreport import TweetsReport
import ConfigParser, webbrowser, os, sys, getopt, gettext, sqlite3
APP_NAME = 'cltwit'
LOC_PATH = os.path.dirname(__file__) + '/locale'
gettext.find(APP_NAME, LOC_PATH)
gettext.install(APP_NAME, LOC_PATH, True)
try:
    import tweepy
except ImportError:
    print _('Veuillez installer tweetpy https://github.com/tweepy/tweepy')
    sys.exit()

__cltwitdir__ = os.path.expanduser('~/.config/cltwit')
__configfile__ = __cltwitdir__ + '/cltwit.conf'
__dblocation__ = __cltwitdir__ + '/data.db'
__tablename__ = 'twitter'
__Local__ = LocalTimezone()
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def has_colours(stream):
    u"""Vérifier la prise en charge des couleurs par le terminal"""
    if not hasattr(stream, 'isatty'):
        return False
    if not stream.isatty():
        return False
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum('colors') > 2
    except:
        return False


__has_colours__ = has_colours(sys.stdout)

def printout(text, colour=WHITE):
    """Print en couleur"""
    if __has_colours__:
        seq = '\x1b[1;%dm' % (30 + colour) + text + '\x1b[0m'
        sys.stdout.write(seq)
    else:
        sys.stdout.write(text)


def checkdb():
    u""" Vérifier la présence de la bdd sqlite et la créer si absente """
    if not os.path.exists(__dblocation__):
        printout(_("Vous devez d'abord lancer la commande --database create pour créer une base de données de vos tweets."), RED)
        sys.exit()


def checkconfig():
    u"""Récupérer la configuration ou la créer"""
    config = ConfigParser.RawConfigParser()
    try:
        config.read(__configfile__)
        if config.has_option('twitterapi', 'access_token'):
            access_token = config.get('twitterapi', 'access_token')
        if config.has_option('twitterapi', 'access_password'):
            access_password = config.get('twitterapi', 'access_password')
    except:
        pass

    auth = tweepy.OAuthHandler('Jus1rnqM6S0WojJfOH1kQ', 'AHQ5sTC8YYArHilXmqnsstOivY6ygQ2N27L1zBwk')
    if not (config.has_option('twitterapi', 'access_token') and config.has_option('twitterapi', 'access_password')):
        while True:
            try:
                webbrowser.open(auth.get_authorization_url())
                var = raw_input(_('Entrez le token !\n'))
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
                cfgfile = open(__configfile__, 'w')
                if not config.has_section('twitterapi'):
                    config.add_section('twitterapi')
                config.set('twitterapi', 'access_token', access_token)
                config.set('twitterapi', 'access_password', access_password)
                config.write(cfgfile)
            except IOError:
                pass

        finally:
            cfgfile.close()

    else:
        auth.set_access_token(access_token, access_password)
    return auth


def login():
    u""" Se connecter à l'api twitter via tweepy """
    auth = checkconfig()
    api = tweepy.API(auth)
    try:
        twittername = api.me().screen_name
    except Exception as e:
        if 'Unable to get username' in str(e):
            printout(_("Impossible de s'authentifier avec l'api Twitter.Fonctionne en mode déconnecté"), RED)
            print '\n'
            twittername = 'offline_mode'

    printout(_('Authentifié avec le user twitter {0}').format(twittername.decode('utf-8')), GREEN)
    print '\n'
    return (
     api, auth, twittername)


def get_friends_followers(api):
    """Renvoie la liste des id des friends et followers"""
    friend_id = []
    follower_id = []
    printout(_('Récupération des Followers...'), YELLOW)
    print '\n'
    for follower in tweepy.Cursor(api.followers).items():
        follower_id.append(follower.id)

    printout('Récupération des Friends...', YELLOW)
    print '\n'
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
        printout(_('Vous suivez maintenant {0}').format(api.get_user(user).screen_name.decode('utf-8')), GREEN)
    except Exception as e:
        print e


def unfollow_user(api, user):
    """Cesser de suivre une personne"""
    try:
        api.destroy_friendship(user)
        printout(_('Vous ne suivez plus {0}').format(api.get_user(user).screen_name.decode('utf-8')), GREEN)
    except Exception as e:
        print e


def main(argv=None):
    u""" Point d'entrée """
    if not os.path.exists(__cltwitdir__):
        os.makedirs(__cltwitdir__)
    if argv is None:
        argv = sys.argv
    if len(argv) == 1:
        help()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'r:ahfut:o:s:d:', [
         'report', 'api', 'help', 'follow', 'unfollow', 'tweet=', 'output=', 'search=', 'database='])
    except getopt.GetoptError as err:
        print err
        help()
        sys.exit()

    for option, value in opts:
        if option in ('-a', '--api'):
            api, auth, twittername = login()
            res = api.rate_limit_status()
            rtime = res['reset_time']
            rhits = res['remaining_hits']
            hlimit = res['hourly_limit']
            from dateutil.parser import parse
            drtime = parse(rtime)
            printout(_("Informations sur l'utilisation de l'api Twitter"), YELLOW)
            print '\n'
            rlocaltime = drtime.astimezone(__Local__)
            printout(_("Maximum d'appels par heure: "), BLUE)
            print hlimit
            printout(_("Nombre d'appels restants: "), BLUE)
            print rhits
            printout(_('Heure du prochain reset: '), BLUE)
            print rlocaltime.strftime('%H:%M %Y-%m-%d')
        if option in ('-r', '--report'):
            api, auth, twittername = login()
            checkdb()
            conn = sqlite3.connect(__dblocation__)
            c = conn.cursor()
            c.execute('select substr(date, 1,4)  from twitter order by date asc limit 1')
            dmois = c.fetchone()[0]
            c.execute('select substr(date, 1,4)  from twitter order by date desc limit 1')
            fmois = c.fetchone()[0]
            dd = dict()
            for a in range(int(dmois), int(fmois) + 1):
                result = []
                for m in range(1, 13):
                    mois = ('{num:02d}').format(num=m)
                    c.execute(("select count(*) from twitter where substr(date, 1,4)  = '{0}' and substr(date, 6,2) = '{1}'").format(a, mois))
                    result.append(c.fetchone()[0])

                dd[a] = result

            c.close()
            conn.close()
            treport = TweetsReport(value)
            treport.ecrireTitre(twittername)
            nb = 0
            for annee, donnees in dd.items():
                nb += 1
                if nb == 4:
                    treport.NextPage()
                    nb = 1
                    saut = 0
                if nb == 1:
                    saut = 0
                if nb == 2:
                    saut = 200
                if nb == 3:
                    saut = 400
                treport.ecrireLegende(saut, annee, donnees)
                treport.addPie(saut, donnees)

            treport.save()
            printout(_('Report {0} créé !').format(value), GREEN)
            print '\n'
            sys.exit(0)
        if option in ('-d', '--database'):
            if value in ('u', 'update'):
                api, auth, twittername = login()
                db = cltwitdb(__dblocation__, __tablename__)
                printout(_('Mise à jour de la base de données de {0}').format(twittername.decode('utf-8')), YELLOW)
                print '\n'
                nb = db.update(api, twittername)
                printout(_('Ajout de {0} tweet(s) dans la base de données.').format(nb), GREEN)
            if value in ('c', 'create'):
                api, auth, twittername = login()
                db = cltwitdb(__dblocation__, __tablename__)
                printout(_('Création de la liste des tweets de ') + twittername.decode('utf-8'), YELLOW)
                db.create(api, twittername)
                printout(_('Base de données crée'), GREEN)
                sys.exit()
        if option in ('-o', '--output'):
            checkdb()
            conn = sqlite3.connect(__dblocation__)
            c = conn.cursor()
            c.execute(('select date, tweet, url from {0} order by date desc').format(__tablename__))
            export = sqlite2csv(open(value, 'wb'))
            export.writerow(['Date', 'Tweet', 'URL'])
            export.writerows(c)
            c.close()
            conn.close()
            printout(_('Fichier csv {0} créé.').format(value.decode('utf-8')), GREEN)
            sys.exit()
        if option in ('-s', '--search'):
            checkdb()
            printout(_('Recherche de {0} dans vos anciens tweets...').format(value.decode('utf-8')), YELLOW)
            print '\n'
            db = cltwitdb(__dblocation__, __tablename__)
            results = db.search(value, 'tweet')
            for result in results:
                print ('{0} -> {1}\n{2}\n\n').format(result[1].decode('utf-8'), result[4].decode('utf-8'), result[2].decode('utf-8'))

        if option in ('-u', '--unfollow'):
            api, auth, twittername = login()
            friend_id, follower_id = get_friends_followers(api)
            follow_liste = get_diff(follower_id, friend_id)
            unfollow_liste = get_diff(friend_id, follower_id)
            printout(_('Vous suivez {0} personnes qui ne vous suivent pas.').format(len(unfollow_liste)), YELLOW)
            print '\n'
            printout(_('Voulez changer cela ? (o/N)'), BLUE)
            print '\n'
            reponse = raw_input('> ')
            if reponse.lower() == 'o' or reponse.lower() == 'y':
                for user in unfollow_liste:
                    printout(_('Voulez-vous cesser de suivre {0} ? (o/N)').format(api.get_user(user).screen_name), BLUE)
                    print '\n'
                    reponse = raw_input('> ')
                    if reponse.lower() == 'o' or reponse.lower() == 'y':
                        unfollow_user(api, user)

        if option in ('-f', '--follow'):
            api, auth, twittername = login()
            friend_id, follower_id = get_friends_followers(api)
            follow_liste = get_diff(follower_id, friend_id)
            unfollow_liste = get_diff(friend_id, follower_id)
            printout(_('{0} personnes vous suivent alors que vous ne les suivez pas.').format(len(follow_liste)), YELLOW)
            print '\n'
            printout(_('Voulez changer cela ? (o/N)'), BLUE)
            print '\n'
            reponse = raw_input('> ')
            if reponse.lower() == 'o' or reponse.lower() == 'y':
                for user in follow_liste:
                    printout(_(('Voulez-vous suivre {0} ? (o/N)').format(api.get_user(user).screen_name)), BLUE)
                    print '\n'
                    reponse = raw_input('> ')
                    if reponse.lower() == 'o' or reponse.lower() == 'y':
                        follow_users(api, user)

        if option in ('-t', '--tweet'):
            api, auth, twittername = login()
            if len(value) < 141:
                api.update_status(value)
                print '\n'
                printout(_('Tweet envoyé !'), GREEN)
            else:
                printout(_('La limite pour un tweet est de 140 caractères, votre message fait {0} caractères de trop').format(str(len(value) - 140).decode('utf-8')), RED)
            sys.exit()
        if option in ('-h', '--help'):
            help()

    return


def help():
    printout(_("\nUsage :\ncltwit [OPTIONS]\nOptions :\n-f (--follow)\n    *Ajouter des personnes qui vous suivent et que vous ne suivez pas\n-u (--unfollow)\n    *Cesser de suivre les personnes que vous suivez et qui vous ne suivent pas\n-s (--search) MOTIF\n    *Search ( rechercher MOTIF dans vos anciens tweets)\n-t  (--tweet)\n    *Envoyer un tweet (message de 140 caractères maximum)\n-o (--output) FILENAME.csv\n    *Exporter l'intégralité de vos tweets dans le fichier FILENAME.csv\n-a (--api)\n    * Obtenir des informations sur l'utilisation de l'api twitter\n-r (--report) FILENAME.pdf\n    * Générer un reporting format pdf avec la repartition des tweets par année et par mois\n-d (--database) c|u\n    c (create)\n            *Créer ou récréer la base de données des tweets\n    u (update)\n            *Mettre à jour la base de données des tweets\n"), BLUE)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print '\n'
        print _("Merci d'avoir utilisé clitwit !")