import inspect

import mwbot
import mwbot.cli as cli

def main(cls):
    if type(cls) != type:
        raise TypeError('Not a class')
    if not issubclass(cls, mwbot.bot.Task):
        raise TypeError('Not an instance of Task')
    last_frame = inspect.stack()[1][0]
    if last_frame.f_globals['__name__'] == '__main__':
        while True:
            try:
                cls().main()
                break
            except mwbot.cred.CredNotFoundError:
                try:
                    if cli.prompt_yn('User not found. Create new user?', default=True):
                        creds = cli.prompt_new_user()
                        creds.save()
                    else:
                        break
                except cli.AbortInput:
                    print('')
                    break

    return cls
