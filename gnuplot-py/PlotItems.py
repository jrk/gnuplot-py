# $Id$

# Copyright (C) 1998-2001 Michael Haggerty <mhagger@alum.mit.edu>
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

"""PlotItems.py -- Objects that can be plotted by Gnuplot.

This module contains several types of PlotItems.  PlotItems can be
plotted by passing them to a Gnuplot.Gnuplot object.  You can derive
your own classes from the PlotItem hierarchy to customize their
behavior.

"""

__cvs_version__ = '$Revision$'

import os, string, tempfile

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import Numeric

import gp, utils, Errors


class _unset:
    """Used to represent unset keyword arguments."""

    pass


class PlotItem:
    """Plotitem represents an item that can be plotted by gnuplot.

    For the finest control over the output, you can create 'PlotItems'
    yourself with additional keyword options, or derive new classes
    from 'PlotItem'.

    The handling of options is complicated by the attempt to allow
    options and their setting mechanism to be inherited conveniently.
    Note first that there are some options that can only be set in the
    constructor then never modified, and others that can be set in the
    constructor and/or modified using the 'set_option()' member
    function.  The former are always processed within '__init__'.  The
    latter are always processed within 'set_option', which is called
    by the constructor.

    'set_option' is driven by a class-wide dictionary called
    '_option_list', which is a mapping '{ <option> : <setter> }' from
    option name to the function object used to set or change the
    option.  <setter> is a function object that takes two parameters:
    'self' (the 'PlotItem' instance) and the new value requested for
    the option.  If <setter> is 'None', then the option is not allowed
    to be changed after construction and an exception is raised.

    Any 'PlotItem' that needs to add options can add to this
    dictionary within its class definition.  Follow one of the
    examples in this file.  Alternatively it could override the
    'set_option' member function if it needs to do wilder things.

    Members:

      '_basecommand' -- a string holding the elementary argument that
          must be passed to gnuplot's `plot' command for this item;
          e.g., 'sin(x)' or '"filename.dat"'.

      '_options' -- a dictionary of (<option>,<string>) tuples
          corresponding to the plot options that have been set for
          this instance of the PlotItem.  <option> is the option as
          specified by the user; <string> is the string that needs to
          be set in the command line to set that option (or None if no
          string is needed).  Example::

              {'title' : ('Data', 'title "Data"'),
               'with' : ('linespoints', 'with linespoints')}

    """

    # For _option_list explanation, see docstring for PlotItem.
    _option_list = {
        'axes' : lambda self, axes: self.set_string_option(
            'axes', axes, None, 'axes %s'),
        'with' : lambda self, with: self.set_string_option(
            'with', with, None, 'with %s'),
        'title' : lambda self, title: self.set_string_option(
            'title', title, 'notitle', 'title "%s"'),
        }

    # order in which options need to be passed to gnuplot:
    _option_sequence = ['binary', 'using', 'smooth', 'axes', 'title', 'with']

    def __init__(self, basecommand, **keyw):
        """Construct a 'PlotItem'.

        Keyword options:

          'with=<string>' -- choose how item will be plotted, e.g.,
              with='points 3 3'.

          'title=<string>' -- set the title to be associated with the item
              in the plot legend.

          'title=None' -- choose 'notitle' option (omit item from legend).

        Note that omitting the title option is different than setting
        'title=None'; the former chooses gnuplot's default whereas the
        latter chooses 'notitle'.

        """

        self._basecommand = basecommand
        self._options = {}
        apply(self.set_option, (), keyw)

    def get_option(self, name):
        """Return the setting of an option.  May be overridden."""

        try:
            return self._options[name][0]
        except:
            raise KeyError('option %s is not set!' % name)

    def set_option(self, **keyw):
        """Set or change a plot option for this PlotItem.

        See documentation for '__init__' for information about allowed
        options.  This function can be overridden by derived classes
        to allow additional options, in which case those options will
        also be allowed by '__init__' for the derived class.  However,
        it is easier to define a new '_option_list' variable for the
        derived class.

        """

        for (option, value) in keyw.items():
            try:
                setter = self._option_list[option]
            except KeyError:
                raise Errors.OptionError('%s=%s' % (option,value))
            if setter is None:
                raise Errors.OptionError(
                    'Cannot modify %s option after construction!', option)
            else:
                setter(self, value)

    def set_string_option(self, option, value, default, fmt):
        """Set an option that takes a string value."""

        if value is None:
            self._options[option] = (value, default)
        elif type(value) is type(''):
            self._options[option] = (value, fmt % value)
        else:
            Errors.OptionError('%s=%s' % (option, value,))

    def clear_option(self, name):
        """Clear (unset) a plot option.  No error if option was not set."""

        try:
            del self._options[name]
        except KeyError:
            pass

    def command(self):
        """Build the plot command to be sent to gnuplot.

        Build and return the plot command, with options, necessary to
        display this item.  If anything else needs to be done once per
        plot, it can be done here too.

        """

        cmd = [self._basecommand]
        for opt in self._option_sequence:
            (val,str) = self._options.get(opt, (None,None))
            if str is not None:
                cmd.append(str)
        return string.join(cmd)

    def pipein(self, f):
        """Pipe necessary inline data to gnuplot.

        If the plot command requires data to be put on stdin (i.e.,
        'plot "-"'), this method should put that data there.  Can be
        overridden in derived classes.

        """

        pass


class Func(PlotItem):
    """Represents a mathematical expression to plot.

    Func represents a mathematical expression that is to be computed by
    gnuplot itself, as if you would type for example::

        gnuplot> plot sin(x)

    into gnuplot itself.  The argument to the contructor is a string
    that should be a mathematical expression.  Example::

        g.plot(Func('sin(x)', with='line 3'))

    As shorthand, a string passed to the plot method of a Gnuplot
    object is also treated as a Func::

        g.plot('sin(x)')

    """

    # The PlotItem constructor does what we need.
    pass


class AnyFile:
    """Representation of any kind of file to be used by gnuplot.

    An AnyFile represents a file, but presumably one that holds data
    in a format readable by gnuplot.  This class simply remembers the
    filename; the existence and format of the file are not checked
    whatsoever.  If no filename is specfied, a random one is created.
    Note that this is not a 'PlotItem', though it is used by the 'File'
    'PlotItem'.

    Members:

        'self.filename' -- the filename of the file

    """

    def __init__(self, filename=None):
        """Make an 'AnyFile' referencing the file with name <filename>.

        If <filename> is not specified, choose a random filename (but
        do not create the file).

        """

        if filename is None:
            filename = tempfile.mktemp()
        self.filename = filename


class TempFile(AnyFile):
    """A file that is automatically deleted.

    A 'TempFile' points to a file.  The file is deleted automatically
    when the 'TempFile' object is deleted.  'TempFile' does not create
    the file; it just references it.

    The constructor is inherited from 'AnyFile'.  It can be passed a
    filename or nothing (in which case a random filename is chosen).

    WARNING: whatever filename you pass to the constructor
    **WILL BE DELETED** when the TempFile object is deleted, even if
    it was a pre-existing file!

    """

    def __del__(self):
        """Delete the referenced file."""

        os.unlink(self.filename)


class ArrayFile(AnyFile):
    """A file to which, upon creation, an array is written.

    When an ArrayFile is constructed, it creates a file and fills it
    with the contents of a 2-d or 3-d Numeric array in the format
    expected by gnuplot (see 'write_array()' for details).  The
    filename can be specified, otherwise a random filename is chosen.
    The file is NOT deleted automatically.

    """

    def __init__(self, set, filename=None):
        """Create a file and write an array to it.

        Arguments:

          'set' -- a Numeric array of arbitrary dimension.

          'filename' -- the (optional) name of the file to which the
              array should be written.  If 'filename' is not
              specified, a random filename is chosen.

        """

        AnyFile.__init__(self, filename)
        utils.write_array(open(self.filename, 'w'), set)


class File(PlotItem):
    """A PlotItem representing a file that contains gnuplot data."""

    _option_list = PlotItem._option_list.copy()
    _option_list.update({
        'smooth' : lambda self, smooth: self.set_string_option(
            'smooth', smooth, None, 'smooth %s'),
        'using' : lambda self, using: self.set_option_using(using),
        'binary' : lambda self, binary: self.set_option_binary(binary),
        })

    def __init__(self, file, **keyw):
        """Construct a File object.

        <file> can be either a string holding the filename of an
        existing file, or it can be an object of any class derived
        from 'AnyFile' (such as a 'TempArrayFile').

        Keyword arguments:

            'using=<int>' -- plot that column against line number

            'using=<tuple>' -- plot using a:b:c:d etc.

            'using=<string>' -- plot `using <string>' (allows gnuplot's
                arbitrary column arithmetic)

            'binary=<boolean>' -- data in file is in binary format
                (only recognized for grid data for splot).

            'smooth=<string>' -- smooth the data.  Option should be
                'unique', 'csplines', 'acsplines', 'bezier', or
                'sbezier'.

        The keyword arguments recognized by 'PlotItem' can also be
        used here.

        Note that the 'using' option is interpreted by gnuplot, so
        columns must be numbered starting with 1.  The default 'title'
        for a TempFile is 'notitle' to avoid using the temporary
        file's name as the title.

        """

        if isinstance(file, AnyFile):
            self.file = file
            # If no title is specified, then use `notitle' for
            # TempFiles (to avoid using the temporary filename as the
            # title.)
            if isinstance(file, TempFile) and not keyw.has_key('title'):
                keyw['title'] = None
        elif type(file) is type(''):
            self.file = AnyFile(file)
        else:
            raise Errors.OptionError(
                'file argument (%s) must be a file object or filename'
                % (file,)
                )
        # Use single-quotes so that pgnuplot can handle DOS filenames:
        apply(PlotItem.__init__, (self, "'%s'" % self.file.filename), keyw)

    def set_option_using(self, using):
        if using is None:
            self.clear_option('using')
        elif type(using) in [type(''), type(1)]:
            self._options['using'] = (using, 'using %s' % using)
        elif type(using) is type(()):
            self._options['using'] = (using,
                                      'using %s' %
                                      string.join(map(repr, using), ':'))
        else:
            raise Errors.OptionError('using=%s' % (using,))

    def set_option_binary(self, binary):
        if binary:
            if not gp.GnuplotOpts.recognizes_binary_splot:
                raise Errors.OptionError(
                    'Gnuplot.py is currently configured to reject binary data')
            self._options['binary'] = (1, 'binary')
        else:
            self._options['binary'] = (0, None)


class Data(PlotItem):
    """Represents data from memory to be plotted with Gnuplot.

    Takes a numeric array from memory and outputs it to a temporary
    file that can be plotted by gnuplot.

    """

    _option_list = PlotItem._option_list.copy()
    _option_list.update({
        'smooth' : lambda self, smooth: self.set_string_option(
            'smooth', smooth, None, 'smooth %s'),
        'cols' : None,
        'inline' : None,
        })

    def __init__(self, *set, **keyw):
        """Construct a 'Data' object from a numeric array.

        Create a 'Data' object (which is a type of 'PlotItem') out of
        one or more Float Python Numeric arrays (or objects that can
        be converted to a Float Numeric array).  If the routine is
        passed one array, the last index ranges over the values
        comprising a single data point (e.g., [<x>, <y>, <sigma>]) and
        the rest of the indices select the data point.  If the routine
        is passed more than one array, they must have identical
        shapes, and then each data point is composed of one point from
        each array.  E.g., 'Data(x,x**2)' is a 'PlotItem' that
        represents x squared as a function of x.  For the output
        format, see the comments for 'write_array()'.

        The array is first written to a temporary file, then that file
        is plotted.  No copy is kept in memory.

        Keyword arguments:

            'cols=<tuple>' -- write only the specified columns from each
                data point to the file.  Since cols is used by python,
                the columns should be numbered in the python style
                (starting from 0), not the gnuplot style (starting
                from 1).

            'inline=<bool>' -- transmit the data to gnuplot "inline"
                rather than through a temporary file.  The default is
                the value of gp.GnuplotOpts.prefer_inline_data.

            'smooth=<string>' -- smooth the data.  Option should be
                'unique', 'csplines', 'acsplines', 'bezier', or
                'sbezier'.

        The keyword arguments recognized by 'PlotItem' can also be
        used here.

        """

        if len(set) == 1:
            # set was passed as a single structure
            set = utils.float_array(set[0])
        else:
            # set was passed column by column (for example,
            # Data(x,y)); pack it into one big array (this will test
            # that sizes are all the same):
            set = utils.float_array(set)
            dims = len(set.shape)
            # transpose so that the last index selects x vs. y:
            set = Numeric.transpose(set, (dims-1,) + tuple(range(dims-1)))
        if keyw.has_key('cols'):
            cols = keyw['cols']
            del keyw['cols']
            if type(cols) is type(1):
                cols = (cols,)
            set = Numeric.take(set, cols, -1)

        # If no title is specified, then use `notitle' (to avoid using
        # the temporary filename as the title).
        if not keyw.has_key('title'):
            keyw['title'] = None

        if keyw.has_key('inline'):
            self.inline = keyw['inline']
            del keyw['inline']
        else:
            self.inline = gp.GnuplotOpts.prefer_inline_data

        if self.inline:
            f = StringIO()
            utils.write_array(f, set)
            f.write('e\n')
            self._data = f.getvalue()
            apply(PlotItem.__init__, (self, "'-'"), keyw)
        else:
            self.file = TempFile()
            utils.write_array(open(self.file.filename, 'w'), set)
            self._data = None
            apply(PlotItem.__init__, (self, "'%s'" % self.file.filename), keyw)

    def pipein(self, f):
        if self._data:
            f.write(self._data)


class GridData(PlotItem):
    """Holds data representing a function of two variables, for use in splot.

    'GridData' represents a function that has been tabulated on a
    rectangular grid.  The data are written to a file; no copy is kept
    in memory.

    """

    _option_list = PlotItem._option_list.copy()
    _option_list.update({
        'binary' : None,
        'inline' : None,
        })

    def __init__(self, data, xvals=None, yvals=None,
                 binary=1, inline=_unset, **keyw):
        """GridData constructor.

        Arguments:

            'data' -- the data to plot: a 2-d array with dimensions
                (numx,numy).

            'xvals' -- a 1-d array with dimension 'numx'

            'yvals' -- a 1-d array with dimension 'numy'

            'binary=<bool>' -- send data to gnuplot in binary format?

            'inline=<bool>' -- send data to gnuplot "inline"?

        Note the unusual argument order!  The data are specified
        *before* the x and y values.  (This inconsistency was probably
        a mistake; after all, the default xvals and yvals are not very
        useful.)

        'data' must be a data array holding the values of a function
        f(x,y) tabulated on a grid of points, such that 'data[i,j] ==
        f(xvals[i], yvals[j])'.  If 'xvals' and/or 'yvals' are
        omitted, integers (starting with 0) are used for that
        coordinate.  The data are written to a temporary file; no copy
        of the data is kept in memory.

        If 'binary=0' then the data are written to a datafile as 'x y
        f(x,y)' triplets (y changes most rapidly) that can be used by
        gnuplot's 'splot' command.  Blank lines are included each time
        the value of x changes so that gnuplot knows to plot a surface
        through the data.

        If 'binary=1' then the data are written to a file in a binary
        format that 'splot' can understand.  Binary format is faster
        and usually saves disk space but is not human-readable.  If
        your version of gnuplot doesn't support binary format (it is a
        recently-added feature), this behavior can be disabled by
        setting the configuration variable
        'gp.GnuplotOpts.recognizes_binary_splot=0' in the appropriate
        gp*.py file.

        Thus if you have three arrays in the above format and a
        Gnuplot instance called g, you can plot your data by typing
        'g.splot(Gnuplot.GridData(data,xvals,yvals))'.

        """

        # Try to interpret data as an array:
        data = utils.float_array(data)
        try:
            (numx, numy) = data.shape
        except ValueError:
            raise Errors.DataError('data array must be two-dimensional')

        if xvals is None:
            xvals = Numeric.arange(numx)
        else:
            xvals = utils.float_array(xvals)
            if xvals.shape != (numx,):
                raise Errors.DataError(
                    'The size of xvals must be the same as the size of '
                    'the first dimension of the data array')

        if yvals is None:
            yvals = Numeric.arange(numy)
        else:
            yvals = utils.float_array(yvals)
            if yvals.shape != (numy,):
                raise Errors.DataError(
                    'The size of yvals must be the same as the size of '
                    'the second dimension of the data array')

        if inline is _unset:
            inline = (not binary) and gp.GnuplotOpts.prefer_inline_data

        # xvals, yvals, and data are now all filled with arrays of data.
        if binary and gp.GnuplotOpts.recognizes_binary_splot:
            if inline:
                raise Errors.OptionError('binary inline data not supported')
            self._data = None
            # write file in binary format

            # It seems that the gnuplot documentation for binary mode
            # disagrees with its actual behavior (as of v. 3.7).  The
            # documentation has the roles of x and y exchanged.  We
            # ignore the documentation and go with the code.

            mout = Numeric.zeros((numy + 1, numx + 1), Numeric.Float32)
            mout[0,0] = numx
            mout[0,1:] = xvals.astype(Numeric.Float32)
            mout[1:,0] = yvals.astype(Numeric.Float32)
            try:
                # try copying without the additional copy implied by astype():
                mout[1:,1:] = Numeric.transpose(data)
            except:
                # if that didn't work then downcasting from double
                # must be necessary:
                mout[1:,1:] = Numeric.transpose(data.astype(Numeric.Float32))
            self.file = TempFile()
            open(self.file.filename, 'wb').write(mout.tostring())

            # avoid using the temporary filename as the title:
            if not keyw.has_key('title'):
                keyw['title'] = None
            apply(PlotItem.__init__, (self, "'%s'" % self.file.filename), keyw)

            # Include the command-line option to read in binary data:
            self._options['binary'] = (1, 'binary')
        else:
            # output data to file as "x y f(x)" triplets.  This
            # requires numy copies of each x value and numx copies of
            # each y value.  First reformat the data:
            set = Numeric.transpose(
                Numeric.array(
                    (Numeric.transpose(Numeric.resize(xvals, (numy, numx))),
                     Numeric.resize(yvals, (numx, numy)),
                     data)), (1,2,0))

            # avoid using the temporary filename as the title:
            if not keyw.has_key('title'):
                keyw['title'] = None

            # now just output the data with the usual routine.  This
            # will produce data properly formatted in blocks separated
            # by blank lines so that gnuplot can connect the points
            # into a grid.
            self.inline = inline
            if self.inline:
                f = StringIO()
                utils.write_array(f, set)
                f.write('e\n')
                self._data = f.getvalue()
                apply(PlotItem.__init__, (self, "'-'"), keyw)
            else:
                self.file = TempFile()
                utils.write_array(open(self.file.filename, 'w'), set)
                apply(PlotItem.__init__,
                      (self, "'%s'" % self.file.filename), keyw)
                self._data = None

            self._options['binary'] = (0, None)

    def pipein(self, f):
        if self._data:
            f.write(self._data)


