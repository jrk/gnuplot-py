# $Id$

# Copyright (C) 1998,1999 Michael Haggerty <mhagger@alum.mit.edu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.  This program is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more
# details; it is available at <http://www.fsf.org/copyleft/gpl.html>,
# or by writing to the Free Software Foundation, Inc., 59 Temple Place
# - Suite 330, Boston, MA 02111-1307, USA.

"""gp -- a platform-independent interface to a gnuplot process.

This file imports a low-level, platform-independent interface to the
gnuplot program.  Which interface is imported depends on the platform.
There are variations of this file for Unix, the Macintosh, and for
Windows called gp_unix.py, gp_mac.py, and gp_win32.py, respectively.
Note that the end-user should use the more capable interface from
__init__.py (i.e., 'import Gnuplot') rather than the low-level
interface imported by this file.

See gp_unix.py for most documentation about the facilities of the
gp_*.py modules.

"""

__cvs_version__ = '$Revision$'

import sys

# Low-level communication with gnuplot is platform-dependent.  Import
# the appropriate implementation of GnuplotProcess based on the
# platform:
if sys.platform == 'mac':
    from gp_mac import GnuplotOpts, GnuplotProcess, test_persist
elif sys.platform == 'win32':
    from gp_win32 import GnuplotOpts, GnuplotProcess, test_persist
elif sys.platform == 'darwin':
    from gp_macosx import GnuplotOpts, GnuplotProcess, test_persist
else:
    from gp_unix import GnuplotOpts, GnuplotProcess, test_persist


