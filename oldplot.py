#! /usr/bin/env python
# $Id$

"""oldplot.py -- Obsolete functional interface to Gnuplot.

Copyright (C) 1998-1999 Michael Haggerty <mhagger@alum.mit.edu>

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

This module implements a function 'plot' that can be used to plot
array data through the gnuplot program.  It is provided for backwards
compatibility with Konrad Hinsen's old module.  The new
object-oriented interface defined in Gnuplot.py has far more features
and should be used for new work.

See Gnuplot.py and the README file for more information.

The module can be tested by typing 'python plot.py'.

"""

__cvs_version__ = '$Revision$'

import Numeric

# The real work is done by Gnuplot.py; this module is just a wrapper.
import Gnuplot
from Gnuplot import Data, File, TempArrayFile, DataException
from utils import float_array
from gp import test_persist


# When persist is not available, the plotters will be stored here to
# prevent their being closed:
_gnuplot_processes = []


def plot(*items, **keyw):
    """Plot data using gnuplot through Gnuplot.

    This command is roughly compatible with old Gnuplot plot command.
    It is provided for backwards compatibility with the old functional
    interface only.  It is recommended that you use the new
    object-oriented Gnuplot interface, which is much more flexible.

    It can only plot Numeric array data.  In this routine an NxM array
    is plotted as M-1 separate datasets, using columns 1:2, 1:3, ...,
    1:M.

    Limitations:

        - If persist is not available, the temporary files are not
          deleted until final python cleanup.

    """

    newitems = []
    for item in items:
        # assume data is an array:
        item = float_array(item)
        dim = len(item.shape)
        if dim == 1:
            newitems.append(Data(item[:, Numeric.NewAxis], with='lines'))
        elif dim == 2:
            if item.shape[1] == 1:
                # one column; just store one item for tempfile:
                newitems.append(Data(item, with='lines'))
            else:
                # more than one column; store item for each 1:2, 1:3, etc.
                tempf = TempArrayFile(item)
                for col in range(1, item.shape[1]):
                    newitems.append(File(tempf, using=(1,col+1), with='lines'))
        else:
            raise DataException('Data array must be 1 or 2 dimensional')
    items = tuple(newitems)
    del newitems

    if keyw.has_key('file'):
        g = Gnuplot.Gnuplot()
        # setup plot without actually plotting (so data don't appear
        # on the screen):
        g._add_to_queue(items)
        g.hardcopy(keyw['file'])
        # process will be closed automatically
    elif test_persist():
        g = Gnuplot.Gnuplot(persist=1)
        apply(g.plot, items)
        # process will be closed automatically
    else:
        g = Gnuplot.Gnuplot()
        apply(g.plot, items)
        # prevent process from being deleted:
        _gnuplot_processes.append(g)


def demo():
    """Demonstration."""

    from Numeric import *
    import sys

    # List of (x, y) pairs
    plot([(0.,1),(1.,5),(2.,3),(3.,4)])

    # List of y values, file output
    print '\n            Generating postscript file "gp_test.ps"\n'
    plot([1, 5, 3, 4], file='gp_test.ps')

    # Two plots; each given by a 2d array
    x = arange(10, typecode=Float)
    y1 = x**2
    y2 = (10-x)**2
    plot(transpose(array([x, y1])), transpose(array([x, y2])))


if __name__ == '__main__':
    demo()


