#! /usr/bin/env python
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

import sys, os, math, time
import Numeric
from Numeric import *
import Gnuplot
gp = Gnuplot # abbreviation

def wait(str='Press return to show results...\n'):
    raw_input(str)


def main():
    """Exercise the Gnuplot module."""

    # Make a temporary file:
    file1 = gp.TempFile() # will be deleted upon exit
    f = open(file1.filename, 'w')
    for x in arange(100)/5. - 10.:
        f.write('%s %s %s\n' % (x, math.cos(x), math.sin(x)))
    f.close()

    g = gp.Gnuplot()
    g.clear()
    print 'A blank gnuplot screen should have appeared on your screen.'
    print

    ############### test Func ########################################
    print 'Plot a gnuplot-generated function'
    wait()
    g.plot(gp.Func('sin(x)'))

    print 'Set title and axis labels and try replot()'
    wait()
    g.title('Title')
    g.xlabel('x')
    g.ylabel('y')
    g.replot()

    print 'Style linespoints'
    wait()
    g.plot(gp.Func('sin(x)', with='linespoints'))
    print 'title=None'
    wait()
    g.plot(gp.Func('sin(x)', title=None))
    print 'title="Sine of x"'
    wait()
    g.plot(gp.Func('sin(x)', title='Sine of x'))

    print 'Change Func attributes after construction:'
    f = gp.Func('sin(x)')
    print 'Original'
    wait()
    g.plot(f)
    print 'Style linespoints'
    wait()
    f.set_option(with='linespoints')
    g.plot(f)
    print 'title=None'
    wait()
    f.set_option(title=None)
    g.plot(f)
    print 'title="Sine of x"'
    wait()
    f.set_option(title='Sine of x')
    g.plot(f)

    ############### test File ########################################
    print 'Generate a File from a filename'
    wait()
    g.plot(gp.File(file1.filename))
    print 'Generate a File given a TempFile object'
    wait()
    g.plot(gp.File(file1))

    print 'Style lines'
    wait()
    g.plot(gp.File(file1.filename, with='lines'))
    print 'using=1, using=(1,)'
    wait()
    g.plot(gp.File(file1.filename, using=1, with='lines'),
           gp.File(file1.filename, using=(1,), with='points'))
    print 'using=(1,2), using="1:3"'
    wait()
    g.plot(gp.File(file1.filename, using=(1,2)),
           gp.File(file1.filename, using='1:3'))
    print 'title=None'
    wait()
    g.plot(gp.File(file1.filename, title=None))
    print 'title="title"'
    wait()
    g.plot(gp.File(file1.filename, title='title'))

    print 'Change File attributes after construction:'
    f = gp.File(file1.filename)
    print 'Original'
    wait()
    g.plot(f)
    print 'Style linespoints'
    wait()
    f.set_option(with='linespoints')
    g.plot(f)
    print 'using=(1,3)'
    wait()
    f.set_option(using=(1,3))
    g.plot(f)
    print 'title=None'
    wait()
    f.set_option(title=None)
    g.plot(f)

    ############### test Data ########################################
    x = arange(100)/5. - 10.
    y1 = Numeric.cos(x)
    y2 = Numeric.sin(x)
    d = Numeric.transpose((x,y1,y2))

    print 'Plot Data, specified column-by-column'
    wait()
    g.plot(gp.Data(x,y2))
    print 'Plot Data, specified by an array'
    wait()
    g.plot(gp.Data(d))
    print 'with="lp 4 4"'
    wait()
    g.plot(gp.Data(d, with='lp 4 4'))
    print 'cols=0'
    wait()
    g.plot(gp.Data(d, cols=0))
    print 'cols=(0,1), cols=(0,2)'
    wait()
    g.plot(gp.Data(d, cols=(0,1)),
           gp.Data(d, cols=(0,2)))
    print 'title=None'
    wait()
    g.plot(gp.Data(d, title=None))
    print 'title="Cosine of x"'
    wait()
    g.plot(gp.Data(d, title='Cosine of x'))

    ############### test HardCopy ####################################
    print 'testing hardcopy'
    wait()
    print '******** Generating postscript file ' \
          '"gp_test.ps" ********'
    g.hardcopy('gp_test.ps', enhanced=1, color=1)
    print 'Listing file'
    os.system('ls -la gp_test.ps')

    ############### test shortcuts ###################################
    print 'plot Func and Data using shortcuts'
    wait()
    g.plot('sin(x)', d)

    ############### test splot #######################################
    print 'testing splot:'
    wait()
    g.splot(gp.Data(d, with='linesp'))

    ############### test GridData ####################################
    print 'testing GridData:'
    # set up x and y values at which the function will be tabulated:
    x = arange(35)/2.0
    y = arange(30)/10.0 - 1.5
    # Make a 2-d array containing a function of x and y.  First create
    # xm and ym which contain the x and y values in a matrix form that
    # can be `broadcast' into a matrix of the appropriate shape:
    xm = x[:,NewAxis]
    ym = y[NewAxis,:]
    m = (sin(xm) + 0.1*xm) - ym**2
    print 'a function of two variables from a GridData file'
    wait()
    g('set parametric')
    g('set data style lines')
    g('set hidden')
    g('set contour base')
    g.xlabel('x')
    g.ylabel('y')
    g.splot(gp.GridData(m,x,y, binary=0))

    print 'The same thing using binary mode'
    wait()
    g.splot(gp.GridData(m,x,y, binary=1))

    print 'And now for a little fun'
    wait()
    for view in range(0,90,5):
        g('set view 60, %d' % view)
        g.replot()
        time.sleep(1.0)

    wait('Press return to end the test.\n')


if __name__ == '__main__':
    main()


