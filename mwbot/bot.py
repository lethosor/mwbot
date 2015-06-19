import mwbot
from mwbot import mwclient, cli

class Resource(object):
    pass

class ResourceMap(dict):
    pass

class Task(object):
    resource_class = Resource
    def __init__(self):
        pass

    def _get_resource_classes(self):
        for attr in dir(self):
            obj = getattr(self, attr)
            if type(obj) == type and issubclass(obj, self.resource_class):
                yield obj

    def _get_resources(self, *args):
        pass

    def arguments(self, arg):
        """ Set up recognized command-line arguments

        arg: A bound argparse.ArgumentParser.add_argument method
        """
        pass

    def main(self):
        parser = mwbot.cli.new_parser(require_user=True)
        self.arguments(parser.add_argument)
        self.args = args = parser.parse_args()
        creds = mwbot.cred.UserCreds(args.user)
        cli.debug('Logging in as %s:%s', creds.site_id, creds.username)
        self.site = mwclient.Site(creds.url_domain, path=creds.url_path)
        self.site.login(creds.username, creds.password)
        cli.debug('Login successful')

class PageTask(Task):
    pass
