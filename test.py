#!/usr/local/bin/python -t
# $Id$

"""Gnuplot_test.py -- Exercise the Gnuplot.py module.

Copyright (C) 1998,1999 Michael Haggerty

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.  This program is distributed in the
hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License for more details; it is
available at <http://www.fsf.org/copyleft/gpl.html>, or by writing to
the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.

"""

__cvs_version__ = 'CVS version $Revision$'

import tempfile
from Numeric import *
import Gnuplot
from Gnuplot import write_array, grid_function
from Gnuplot import AnyFile, TempFile, ArrayFile, TempArrayFile
from Gnuplot import PlotItem, Func, File, Data, GridData

def main():
    """Exercise the Gnuplot module."""

    g = Gnuplot.Gnuplot()
    g.title('Title')
    g('set data style linespoints')
    g.plot([[0,1.1], [1,5.8], [2,3.3], [3,4.2]])

    # Plot one dataset from an array and one via a gnuplot function;
    # also demonstrate the use of item-specific options:
    g2 = Gnuplot(debug=1)
    x = arange(10, typecode=Float)
    y1 = x**2
    # Notice how this plotitem is created here but used later?  This
    # is convenient if the same dataset has to be plotted multiple
    # times.  It is also more efficient because the data need only be
    # written to a temporary file once.
    d = Data(x, y1,
             title='calculated by python',
             with='points 3 3')
    g2.title('Data can be computed by python or gnuplot')
    g2.xlabel('x')
    g2.ylabel('x squared')
    # Plot a function alongside the Data PlotItem defined above:
    g2.plot(Func('x**2', title='calculated by gnuplot'), d)

    # Save what we just plotted as a color postscript file.

    # With the enhanced postscript option, it is possible to show `x
    # squared' with a superscript (plus much, much more; see `help set
    # term postscript' in the gnuplot docs).  If your gnuplot doesn't
    # support enhanced mode, set `enhanced=0' below.
    g2.ylabel('x^2') # take advantage of enhanced postscript mode
    print ('\n******** Generating postscript file '
           '"gnuplot_test_plot.ps" ********\n')
    g2.hardcopy('gnuplot_test_plot.ps', enhanced=1, color=1)

    # Demonstrate a 3-d plot:
    g3 = Gnuplot(debug=1)
    # set up x and y values at which the function will be tabulated:
    x = arange(35)/2.0
    y = arange(30)/10.0 - 1.5
    # Make a 2-d array containing a function of x and y.  First create
    # xm and ym which contain the x and y values in a matrix form that
    # can be `broadcast' into a matrix of the appropriate shape:
    xm = x[:,NewAxis]
    ym = y[NewAxis,:]
    m = (sin(xm) + 0.1*xm) - ym**2
    g3('set parametric')
    g3('set data style lines')
    g3('set hidden')
    g3('set contour base')
    g3.xlabel('x')
    g3.ylabel('y')
    # The `binary=1' option would cause communication with gnuplot to
    # be in binary format, which is considerably faster and uses less
    # disk space.  (This only works with the splot command due to
    # limitations of gnuplot.)  `binary=1' is the default, but here we
    # disable binary because older versions of gnuplot don't allow
    # binary data.  Change this to `binary=1' (or omit the binary
    # option) to get the advantage of binary format.
    g3.splot(GridData(m,x,y, binary=0))

    # Delay so the user can see the plots:
    sys.stderr.write('Three plots should have appeared on your screen '
                     '(they may be overlapping).\n'
                     'Please press return to continue...\n')
    sys.stdin.readline()

    # ensure processes and temporary files are cleaned up:
    del g1, g2, g3, d

    # Enable the following code to test the old-style gnuplot interface
    if 0:
        # List of (x, y) pairs
        plot([(0.,1),(1.,5),(2.,3),(3.,4)])

        # List of y values, file output
        print '\n            Generating postscript file "gnuplot_test2.ps"\n'
        plot([1, 5, 3, 4], file='gnuplot_test2.ps')

        # Two plots; each given by a 2d array
        x = arange(10, typecode=Float)
        y1 = x**2
        y2 = (10-x)**2
        plot(transpose(array([x, y1])), transpose(array([x, y2])))


if __name__ == '__main__':
    main()


