# $Id$

# Copyright (C) 1999 Michael Haggerty <mhagger@alum.mit.edu>
# Thanks to Tony Ingraldi and Noboru Yamamoto for their contributions.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.  This program is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details; it is
# available at <http://www.fsf.org/copyleft/gpl.html>, or by writing to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

"""gp_mac -- an interface to gnuplot for the Macintosh.

"""

__cvs_version__ = '$Revision$'

import os, string

import Errors


# ############ Configuration variables: ################################

class GnuplotOpts:
    """The configuration options for gnuplot on the Macintosh.

    See gp.py for details about the meaning of these options.  Please
    let me know if you know better choices for these settings."""

    # The '-persist' option is not supported on the Mac:
    recognizes_persist = 0

    # Apparently the Mac can use binary data:
    recognizes_binary_splot = 1

    # Apparently the Mac can not use inline data:
    prefer_inline_data = 0

    # The default choice for the 'set term' command (to display on screen):
    default_term = 'pict'

    # I don't know how to print directly to a printer on the Mac:
    default_lpr = '| lpr'

    # Used the 'enhanced' option of postscript by default?  Set to
    # None (*not* 0!) if your version of gnuplot doesn't support
    # enhanced postscript.
    prefer_enhanced_postscript = 1

# ############ End of configuration options ############################


# The Macintosh doesn't support pipes so communication is via
# AppleEvents.

import gnuplot_Suites
import Required_Suite
import aetools


# Mac doesn't recognize persist.
def test_persist():
    return 0

class _GNUPLOT(aetools.TalkTo,
               Required_Suite.Required_Suite,
               gnuplot_Suites.gnuplot_Suite,
               gnuplot_Suites.odds_and_ends,
               gnuplot_Suites.Standard_Suite,
               gnuplot_Suites.Miscellaneous_Events):
    """Start a gnuplot program and emulate a pipe to it."""

    def __init__(self):
        aetools.TalkTo.__init__(self, '{GP}', start=1)


class GnuplotProcess:
    """Unsophisticated interface to a running gnuplot program.

    See gp_unix.GnuplotProcess for usage information.

    """

    def __init__(self, persist=0):
        """Start a gnuplot process.

        Create a 'GnuplotProcess' object.  This starts a gnuplot
        program and prepares to write commands to it.

        Keyword arguments:

          'persist' -- the '-persist' option is not supported on the
                       Macintosh so this argument must be zero.

        """

        if persist:
            raise Errors.OptionError(
                '-persist is not supported on the Macintosh!')

        self.gnuplot = _GNUPLOT()

        # forward close method:
        self.close = self.gnuplot.quit

    def write(self, s):
        """Mac gnuplot apparently requires '\r' to end statements."""

        self.gnuplot.gnuexec(string.replace(s, '\n', os.linesep))

    def flush(self):
		pass
		
    def __call__(self, s):
        """Send a command string to gnuplot, for immediate execution."""

        # Apple Script doesn't seem to need the trailing '\n'.
        self.write(s)
        self.flush()


