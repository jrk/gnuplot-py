#! /usr/bin/env python

# $Id$

"""utils.py -- Utility functions used by Gnuplot.

Copyright (C) 1998-2001 Michael Haggerty <mhagger@alum.mit.edu>

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

This module contains utility functions used by Gnuplot.py which aren't
particularly gnuplot-related.

"""

__cvs_version__ = '$Revision$'

import string
import Numeric


def float_array(m):
    """Return the argument as a Numeric array of type at least 'Float32'.

    Leave 'Float64' unchanged, but upcast all other types to
    'Float32'.  Allow also for the possibility that the argument is a
    python native type that can be converted to a Numeric array using
    'Numeric.asarray()', but in that case don't worry about
    downcasting to single-precision float.

    """

    try:
        # Try Float32 (this will refuse to downcast)
        return Numeric.asarray(m, Numeric.Float32)
    except TypeError:
        # That failure might have been because the input array was
        # of a wider data type than Float32; try to convert to the
        # largest floating-point type available:
        return Numeric.asarray(m, Numeric.Float)


def write_array(f, set,
                item_sep=' ',
                nest_prefix='', nest_suffix='\n', nest_sep=''):
    """Write an array of arbitrary dimension to a file.

    A general recursive array writer.  The last four parameters allow
    a great deal of freedom in choosing the output format of the
    array.  The defaults for those parameters give output that is
    gnuplot-readable.  But using '(",", "{", "}", ",\n")' would output
    an array in a format that Mathematica could read.  item_sep should
    not contain '%' (or if it does, it should be escaped to '%%')
    since it is put into a format string.

    The default 2-d file organization is, for example:

        set[0,0] set[0,1] ...
        set[1,0] set[1,1] ...

    The 3-d format is, for example:

        set[0,0,0] set[0,0,1] ...
        set[0,1,0] set[0,1,1] ...

        set[1,0,0] set[1,0,1] ...
        set[1,1,0] set[1,1,1] ...

    """

    if len(set.shape) == 1:
        (columns,) = set.shape
        assert columns > 0
        fmt = string.join(['%s'] * columns, item_sep)
        f.write(nest_prefix)
        f.write(fmt % tuple(set.tolist()))
        f.write(nest_suffix)
    elif len(set.shape) == 2:
        # This case could be done with recursion, but `unroll' for
        # efficiency.
        (points, columns) = set.shape
        assert points > 0 and columns > 0
        fmt = string.join(['%s'] * columns, item_sep)
        f.write(nest_prefix + nest_prefix)
        f.write(fmt % tuple(set[0].tolist()))
        f.write(nest_suffix)
        for point in set[1:]:
            f.write(nest_sep + nest_prefix)
            f.write(fmt % tuple(point.tolist()))
            f.write(nest_suffix)
        f.write(nest_suffix)
    else:
        # Use recursion for three or more dimensions:
        assert set.shape[0] > 0
        f.write(nest_prefix)
        write_array(f, set[0],
                    item_sep, nest_prefix, nest_suffix, nest_sep)
        for subset in set[1:]:
            f.write(nest_sep)
            write_array(f, subset,
                        item_sep, nest_prefix, nest_suffix, nest_sep)
        f.write(nest_suffix)


