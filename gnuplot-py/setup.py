#! /usr/bin/env python

# Copyright (C) 2001 Michael Haggerty <mhagger@alum.mit.edu>
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

"""Setup script for the Gnuplot module distribution.

"""

__cvs_version__ = '$Revision$'

from distutils.core import setup

# Get the version number from the __init__ file:
from __init__ import __version__

long_description = """\
Gnuplot.py is a Python package that allows you to create graphs from
within Python using the gnuplot plotting program.
"""

setup (
    # Distribution meta-data
    name='Gnuplot',
    version=__version__,
    description='A Python interface to the gnuplot plotting program.',
    long_description=long_description,
    author='Michael Haggerty',
    author_email='mhagger@alum.mit.edu',
    url='http://gnuplot-py.sourceforge.net',
    license='GPL',
    licence='GPL', # Spelling error in distutils

    # Description of the package in the distribution
    package_dir={'Gnuplot' : ''},
    packages=['Gnuplot'],
    )

