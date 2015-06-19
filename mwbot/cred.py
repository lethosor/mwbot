from ConfigParser import ConfigParser
from os import makedirs
from os.path import exists, isdir, isfile, expanduser, join

import mwbot

cred_path = join(expanduser('~'), '.mwbot-creds')

class CredError(Exception): pass
class CredNotFoundError(CredError): pass

class UserCreds(object):
    def __init__(self, ident, url=None, password=None):
        ident = ident.split(':')
        if len(ident) != 2:
            raise ValueError('Invalid user identifier: "%s"' % ':'.join(ident))
        self.site_id, self.username = ident
        self.filename = join(cred_path, '%s.txt' % self.site_id)
        self.parser = ConfigParser()
        self.parser.optionxform = str  # Do not modify case of keys/values
        if url is not None and password is not None:
            self.url, self.password = url, password
            self.save()
        else:
            self.load()

    def load(self):
        if not isdir(cred_path):
            makedirs(cred_path)
        if not exists(self.filename):
            raise CredNotFoundError
        self.parser.read(self.filename)
        try:
            self.url = self.parser.get('site', 'url')
            self.password = self.parser.get('creds', self.username)
        except ConfigParser.Error:
            raise CredNotFoundError

    def save(self):
        self.parser.read(self.filename)
        for section in ('site', 'creds'):
            if not self.parser.has_section(section):
                self.parser.add_section(section)
        self.parser.set('site', 'url', self.url)
        self.parser.set('creds', self.username, self.password)
        with open(self.filename, 'w') as f:
            self.parser.write(f)

    @property
    def url_domain(self):
        domain = self.url
        if '://' in domain:
            domain = domain.split('://', 1)[1]
        return domain.split('/', 1)[0]

    @property
    def url_path(self):
        path = self.url
        if '://' in path:
            path = path.split('://', 1)[1]
        if not '/' in path:
            return '/'
        path = path[path.index('/'):]
        if not path.endswith('/'):
            path += '/'
        return path
