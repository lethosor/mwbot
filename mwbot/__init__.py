import imp
import os
import sys
mwclient = None
def load_mwclient():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mwclient')
    try:
        global mwclient
        mwclient = imp.load_module('mwclient', *imp.find_module('mwclient', [path]))
    except ImportError:
        raise ImportError("Could not import module 'mwclient'. Did you forget to initialize submodules?")
load_mwclient()

import mwbot.bot
import mwbot.cli
import mwbot.cred
import mwbot.run
import mwbot.util
