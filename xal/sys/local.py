"""Provider that handle local system-related information."""
import platform
import os
import sys

from xal.sys.provider import SysProvider


class LocalSysProvider(SysProvider):
    """Base class for sys provider."""
    @property
    def name(self):
        """Proxy to :func:`os.name`."""
        return os.name

    @property
    def uname(self):
        """Proxy to :func:`platform.uname`."""
        return platform.uname()

    @property
    def platform(self):
        """Proxy to :func:`sys.platform`."""
        return sys.platform

    @property
    def is_posix(self):
        """Use :glob:`os.sep` to determine if system is POSIX."""
        return os.sep == '/'

    def supports(self, session):
        """Return ``True`` if session is local."""
        return session.is_local
