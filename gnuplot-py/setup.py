#! /usr/bin/env python

"""Setup script for the Gnuplot module distribution."""

__revision__ = "$Id$"

from distutils.core import setup

setup (# Distribution meta-data
    name = "Gnuplot",
    version = "1.4",
    description = "A pipe-based Python interface to the gnuplot plotting program.",
    author = "Michael Haggerty",
    author_email = "mhagger@blizzard.harvard.edu",
    url = "http://monsoon.harvard.edu/~mhagger/Gnuplot/Gnuplot.html",

    # Description of the package in the distribution
    package_dir = {'Gnuplot' : ''},
    packages = ['Gnuplot']
    )

