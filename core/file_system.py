"""
Copy from joption.wht (20230825)
"""

import os
from os.path import exists


class BaseEnv:
    """
    A path helper served as an file environment and function.
    env = BaseEnv(...)
    pout = env('dat', 'project', 'output.txt')
    """

    def __init__(self, *args):
        self.pbase = self.get_default_path_by_env()
        if self.pbase is not None:
            ensure_dir(self.pbase)
            return self

        # windows / linux
        if os.name == "nt":
            self.pbase = "C:\\"
        else:
            self.pbase = "/"

        # add up from root
        self.pbase = self(*args)

        ensure_dir(self.pbase)

    def __call__(self, *args):
        """join path under ``self.pbase``"""
        return os.path.join(self.pbase, *args)

    def get_default_path_by_env(self) -> str|None:
        """
        get possible ``pbase`` if environ var PBASE is available
        """
        return os.getenv('PBASE')


def ensure_dir(fpath):
    """makedirs if corresponding dir is missing"""
    fdir = os.path.dirname(fpath)
    if len(fdir) > 0:
        os.makedirs(fdir, exist_ok=True)
    return fpath


def utouch(file):
    """makedirs + utime + create file"""
    ensure_dir(file)
    try:
        os.utime(file, None)
    except OSError:
        open(file, 'a').close()


def ffread(file):
    """Fast File Read"""
    with open(file, "r") as f:
        return f.read()


def ffwrite(file, text):
    """Fast File Write"""
    with open(file, "w") as f:
        return f.write(text)
