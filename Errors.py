# $Id$

"""Exception types that can be raised by Gnuplot.py."""


class Error(Exception):
    """All our exceptions are derived from this one."""
    pass


class OptionError(Error):
    """Raised for unrecognized option(s)"""
    pass


class DataError(Error):
    """Raised for data in the wrong format"""
    pass


