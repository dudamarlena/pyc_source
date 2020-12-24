# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marx/venv3/lib/python3.6/site-packages/tsr/modules/scrapers.py
# Compiled at: 2018-06-02 09:44:59
# Size of source mod 2**32: 2430 bytes
from .general import ls_in_str

def replace_images_with_hrefs(soup):
    images = soup.find_all('img')
    for img in images:
        if 'src' in img:
            src = img['src']
            src = src.split('/smilies/')[(-1)]
            src = src.split('/attachment.php?')[(-1)]
            img.replaceWith(' ' + src)


def replace_lists(soup):
    ls = soup.find_all('li')
    for l in ls:
        l.replaceWith('- ' + l.text)


def replace_tags(soup):
    l = []
    try:
        tags = soup.find_all('a', {'class': 'bb-user'})
        tags = tags[1:]
        for tag in tags:
            href = tag['href']
            user_id = int(href.split('?u=')[(-1)])
            name = tag.text
            tag.decompose()
            user = {user_id: {name}}
            l.append(user)

    except:
        pass

    return l


def full_urls(soup):
    urls = soup.find_all('a')
    for u in urls:
        if ls_in_str(['http://', 'https://', 'ftp://', 'smb://', 'magnet:?xt='], u.text):
            try:
                u.replaceWith(u['href'])
            except:
                pass


def get_security_token(soup):
    try:
        securitytoken = [x.text.lower() for x in soup.find_all('script') if 'var securitytoken' in x.text.lower()][0]
        securitytoken = securitytoken.split('var securitytoken = "')[(-1)].split('"')[0]
    except:
        securitytoken = soup.find('input', {'name': 'securitytoken'})['value']

    return securitytoken


def get_post_hash(soup):
    try:
        securitytoken = [x.text.lower() for x in soup.find_all('script') if 'var posthash' in x.text.lower()][0]
        securitytoken = securitytoken.split('var posthash = "')[(-1)].split('"')[0]
    except:
        try:
            securitytoken = soup.find('input', {'name': 'posthash'})['value']
        except:
            securitytoken = [x.text.lower() for x in soup.find_all('script') if 'posthash' in x.text.lower()][0]
            securitytoken = [x for x in securitytoken.split('\n') if 'posthash' in x][0]
            securitytoken = securitytoken.split(':')[(-1)].split(',')[0].strip()[1:-1]

    return securitytoken


def get_logout_url(soup):
    return soup.find('a', {'id': 'logoutButton'})['href']