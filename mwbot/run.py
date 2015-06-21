import functools
import inspect

import mwbot.cli as cli
import mwbot.cred as cred
import mwbot.util as util
from mwbot.bot import Task

__all__ = []
export = util.append_name_wrapper(__all__)

export(Task)

def require_task(func):
    @functools.wraps(func)
    def wrapper(cls, *args, **kwargs):
        if type(cls) != type:
            raise TypeError('Not a class')
        if not issubclass(cls, Task):
            raise TypeError('Not an instance of Task')
        return func(cls, *args, **kwargs)
    return wrapper

@export
@require_task
def main(cls):
    last_frame = inspect.stack()[2][0]
    if last_frame.f_globals['__name__'] == '__main__':
        while True:
            try:
                cls().main()
                break
            except cred.CredNotFoundError:
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

@export
def arg(*args, **kwargs):
    @require_task
    def wrapper(cls):
        if not hasattr(cls, '_arguments'):
            cls._arguments = []
        cls._arguments.append(cli.ArgWrapper(*args, **kwargs))
        return cls
    return wrapper
