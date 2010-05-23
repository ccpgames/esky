

import os
import errno
import esky
from functools import wraps


def _check_needsroot(func):
    @wraps(func)
    def do_check_needsroot(self,*args,**kwds):
        if os.environ.get("ESKY_NEEDSROOT",""):
            if not self.has_root():
                raise OSError(errno.EACCES,"you need root")
        return func(self,*args,**kwds)
    return do_check_needsroot


class TestableEsky(esky.Esky):
    """Esky subclass that tries harder to be testable.

    If the environment variable "ESKY_NEEDSROOT" is set, operations that
    alter the filesystem will fail with EACCES when not executed as root.
    """

    @_check_needsroot
    def lock(self,num_retries=0):
        return super(TestableEsky,self).lock(num_retries)

    @_check_needsroot
    def unlock(self):
        return super(TestableEsky,self).unlock()

    @_check_needsroot
    def cleanup(self):
        return super(TestableEsky,self).cleanup()

    @_check_needsroot
    def fetch_version(self,version):
        return super(TestableEsky,self).fetch_version(version)

    @_check_needsroot
    def install_version(self,version):
        return super(TestableEsky,self).install_version(version)

    @_check_needsroot
    def uninstall_version(self,version):
        super(TestableEsky,self).uninstall_version(version)




