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

import sys, math
import Numeric
from Numeric import *
import Gnuplot
gp = Gnuplot # abbreviation

def wait():
    raw_input('Please press return...\n')


def main():
    """Exercise the Gnuplot module."""

    # Make a temporary file:
    file1 = gp.TempFile() # will be deleted upon exit
    f = open(file1.filename, 'w')
    for x in arange(100)/5. - 10.:
        f.write('%s %s %s\n' % (x, math.cos(x), math.sin(x)))
    f.close()

    g = gp.Gnuplot()

    ############### test Func ########################################
    print 'Plot a gnuplot-generated function'
    g.plot(gp.Func('sin(x)'))
    wait()

    print 'Set title and axis labels and try replot()'
    g.title('Title')
    g.xlabel('x')
    g.ylabel('y')
    g.replot()
    wait()

    print 'Style linespoints'
    g.plot(gp.Func('sin(x)', with='linespoints'))
    wait()
    print 'title=None'
    g.plot(gp.Func('sin(x)', title=None))
    wait()
    print 'title="Sine of x"'
    g.plot(gp.Func('sin(x)', title='Sine of x'))
    wait()

    print 'Change Func attributes after construction:'
    f = gp.Func('sin(x)')
    print 'Original'
    g.plot(f)
    wait()
    print 'Style linespoints'
    f.set_option(with='linespoints')
    g.plot(f)
    wait()
    print 'title=None'
    f.set_option(title=None)
    g.plot(f)
    wait()
    print 'title="Sine of x"'
    f.set_option(title='Sine of x')
    g.plot(f)
    wait()

    ############### test File ########################################
    print 'Generate a File from a filename'
    g.plot(gp.File(file1.filename))
    wait()
    print 'Generate a File given a TempFile object'
    g.plot(gp.File(file1))
    wait()

    print 'Style lines'
    g.plot(gp.File(file1.filename, with='lines'))
    wait()
    print 'using=1, using=(1,)'
    g.plot(gp.File(file1.filename, using=1, with='lines'),
           gp.File(file1.filename, using=(1,), with='points'))
    wait()
    print 'using=(1,2), using="1:3"'
    g.plot(gp.File(file1.filename, using=(1,2)),
           gp.File(file1.filename, using='1:3'))
    wait()
    print 'title=None'
    g.plot(gp.File(file1.filename, title=None))
    wait()
    print 'title="title"'
    g.plot(gp.File(file1.filename, title='title'))
    wait()

    print 'Change File attributes after construction:'
    f = gp.File(file1.filename)
    print 'Original'
    g.plot(f)
    wait()
    print 'Style linespoints'
    f.set_option(with='linespoints')
    g.plot(f)
    wait()
    print 'using=(1,3)'
    f.set_option(using=(1,3))
    g.plot(f)
    wait()
    print 'title=None'
    f.set_option(title=None)
    g.plot(f)
    wait()

    ############### test Data ########################################
    x = arange(100)/5. - 10.
    y1 = Numeric.cos(x)
    y2 = Numeric.sin(x)
    d = Numeric.array((x,y1,y2))

    print 'Plot Data, specified column-by-column'
    g.plot(gp.Data(x,y1))
    wait()
    print 'Plot Data, specified by an array'
    g.plot(gp.Data(d))
    wait()
    print 'with="lp 4 4"'
    g.plot(gp.Data(d, with='lp 4 4'))
    wait()
    print 'cols=0'
    g.plot(gp.Data(d, cols=0))
    wait()
    print 'cols=(0,1), cols=(0,2)'
    g.plot(gp.Data(d, cols=(0,1)),
           gp.Data(d, cols=(0,2)))
    wait()
    print 'title=None'
    g.plot(gp.Data(d, title=None))
    wait()
    print 'title="Cosine of x"'
    g.plot(gp.Data(d, title='Cosine of x'))
    wait()

    ############### test shortcuts ###################################
    print 'plot Func and Data using shortcuts'
    g.plot('sin(x)', d)
    wait()

    ############### test GridData ####################################
    # set up x and y values at which the function will be tabulated:
    x = arange(35)/2.0
    y = arange(30)/10.0 - 1.5
    # Make a 2-d array containing a function of x and y.  First create
    # xm and ym which contain the x and y values in a matrix form that
    # can be `broadcast' into a matrix of the appropriate shape:
    xm = x[:,NewAxis]
    ym = y[NewAxis,:]
    m = (sin(xm) + 0.1*xm) - ym**2
    g('set parametric')
    g('set data style lines')
    g('set hidden')
    g('set contour base')
    g.xlabel('x')
    g.ylabel('y')
    # The `binary=1' option would cause communication with gnuplot to
    # be in binary format, which is considerably faster and uses less
    # disk space.  (This only works with the splot command due to
    # limitations of gnuplot.)  `binary=1' is the default, but here we
    # disable binary because older versions of gnuplot don't allow
    # binary data.  Change this to `binary=1' (or omit the binary
    # option) to get the advantage of binary format.
    g.splot(gp.GridData(m,x,y, binary=0))

    ############### test HardCopy ####################################
    g.ylabel('x^2') # take advantage of enhanced postscript mode
    print ('\n******** Generating postscript file '
           '"gnuplot_test_plot.ps" ********\n')
    g.hardcopy('gnuplot_test_plot.ps', enhanced=1, color=1)


if __name__ == '__main__':
    main()


