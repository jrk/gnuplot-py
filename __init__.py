#! /usr/bin/env python
# $Id$

"""Gnuplot -- A pipe-based interface to the gnuplot plotting program.

This is the main module of the Gnuplot package.

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

Written by Michael Haggerty <mhagger@blizzard.harvard.edu>.  Inspired
by and partly derived from an earlier version by Konrad Hinsen
<hinsen@ibs.ibs.fr>.  If you find a problem or have a suggestion,
please let me know at <mhagger@blizzard.harvard.edu>.  Other feedback
would also be appreciated.

The Gnuplot.py home page is at

    <http://monsoon.harvard.edu/~mhagger/Gnuplot/Gnuplot.html>.


For information about how to use this module:

1.  Check the README file.
2.  Look at the example code in demo.py and try running it by typing
    'python demo.py' or 'python __init__.py'.
3a. For more details see the extensive documentation strings
    throughout this file and gp.py.
3b. The docstrings have also been turned into html which can be read
    at <http://monsoon.harvard.edu/~mhagger/Gnuplot/Gnuplot-doc/>.
    However, the formatting is not perfect; when in doubt,
    double-check the docstrings.

You should import this file with 'import Gnuplot', not with 'from
Gnuplot import *', because the module and the main class have the same
name, `Gnuplot'.

To obtain the gnuplot plotting program itself, see
<ftp://ftp.gnuplot.vt.edu/pub/gnuplot/faq/index.html>.  Obviously you
need to have gnuplot installed if you want to use Gnuplot.py.

The old command-based interface to gnuplot has been separated out into
a separate module, oldplot.py.  If you are still using that interface
you should import Gnuplot.oldplot; otherwise you should stick to the
more flexible object-oriented interface contained here.

Features:

 o  Allows the creation of two or three dimensional plots from
    python.

 o  A gnuplot session is an instance of class 'Gnuplot'.  Multiple
    sessions can be open at once.

    Example:

        g1 = Gnuplot.Gnuplot()
        g2 = Gnuplot.Gnuplot()

    Note that due to limitations on those platforms, opening multiple
    simultaneous sessions on Windows or Macintosh may not work
    correctly.  (Feedback?)

 o  The implicitly-generated gnuplot commands can be stored to a file
    instead of executed immediately.

    Example:

        g = Gnuplot.Gnuplot('commands.gnuplot')

    The file can then be run later with gnuplot's 'load' command.
    Beware, however: the plot commands may depend on the existence of
    temporary files, which will probably be deleted before you use the
    command file.

 o  Can pass arbitrary commands to the gnuplot command interpreter.

    Example:

        g('set pointsize 2')

    (If this is all you want to do, you might consider using the
    lightweight GnuplotProcess class defined in gp.py.)

 o  A Gnuplot object knows how to plot objects of type 'PlotItem'.
    Any PlotItem can have optional 'title' and/or 'with' suboptions.
    Builtin PlotItem types:
        
    * 'Data(array1)' -- data from a Python list or NumPy array
                        (permits additional option 'cols' )

    * 'File('filename')' -- data from an existing data file (permits
                            additional option 'using' )

    * 'Func('exp(4.0 * sin(x))')' -- functions (passed as a string,
                                     evaluated by gnuplot)

    * 'GridData(m, x, y)' -- data tabulated on a grid of (x,y) values
                             (usually to be plotted in 3-D)

    * 'GridFunc(f, xvals, yvals)' -- a function f which is to be
                                     tabulated on a grid of (x,y) pairs.

    See the documentation strings for those classes for more details.

 o  PlotItems are implemented as objects that can be assigned to
    variables and plotted repeatedly.  Most of their plot options can
    also be changed with the new 'set_option()' member functions then
    they can be replotted with their new options.

 o  Communication of commands to gnuplot is via a one-way pipe.
    Communication of data from python to gnuplot is via inline data
    (through the command pipe) or via temporary files.  Temp files are
    deleted automatically when their associated 'PlotItem' is deleted.
    The PlotItems in use by a Gnuplot object at any given time are
    stored in an internal list so that they won't be deleted
    prematurely.

 o  Can use 'replot' method to add datasets to an existing plot.

 o  Can make persistent gnuplot windows by using the constructor option
    'persist=1'.  Such windows stay around even after the gnuplot
    program is exited.  Note that only newer version of gnuplot support
    this option.

 o  Can plot either directly to a postscript printer or to a
    postscript file via the 'hardcopy' method.

 o  Grid data for the splot command can be sent to gnuplot in binary
    format, saving time and disk space.

 o  Should work under Unix, Macintosh, and Windows.

Restrictions:
    
 -  Relies on the Numeric Python extension.  This can be obtained
    from LLNL (See ftp://ftp-icf.llnl.gov/pub/python/README.html).
    If you're interested in gnuplot, you would probably also want
    NumPy anyway.

 -  Only a small fraction of gnuplot functionality is implemented as
    explicit method functions.  However, you can give arbitrary
    commands to gnuplot manually.

    Example:

        g = Gnuplot.Gnuplot()
        g('set data style linespoints')
        g('set pointsize 5')

 -  There is no provision for missing data points in array data (which
    gnuplot allows via the 'set missing' command).

Bugs:

 -  No attempt is made to check for errors reported by gnuplot.  On
    unix any gnuplot error messages simply appear on stderr.  (I don't
    know what happens under Windows.)

 -  All of these classes perform their resource deallocation when
    '__del__' is called.  Normally this works fine, but there are
    well-known cases when Python's automatic resource deallocation
    fails, which can leave temporary files around.

"""

__version__ = '1.4'
__cvs_version__ = '$Revision$'

# Other modules that should be loaded for 'from Gnuplot import *':
__all__ = ['oldplot']

import sys, os, string, tempfile
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

# The Numeric package (also known as NumPy):
import Numeric

# Low-level communication with gnuplot is platform-dependent.  Pick an
# implementation of GnuplotProcess based on the platform:
if sys.platform == 'mac':
    from gp_mac import GnuplotOpts, GnuplotProcess, test_persist
elif sys.platform == 'win32':
    from gp_win32 import GnuplotOpts, GnuplotProcess, test_persist
else:
    from gp import GnuplotOpts, GnuplotProcess, test_persist


class _unset:
    """Used to represent unset keyword arguments."""

    pass


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


def grid_function(f, xvals, yvals, typecode=None, ufunc=0):
    """Evaluate and tabulate a function on a grid.

    'xvals' and 'yvals' should be 1-D arrays listing the values of x
    and y at which 'f' should be tabulated.  'f' should be a function
    taking two floating point arguments.  The return value is a matrix
    M where 'M[i,j] = f(xvals[i],yvals[j])', which can for example be
    used in the 'GridData' constructor.

    If 'ufunc=0', then 'f' is evaluated at each pair of points using a
    Python loop.  This can be slow if the number of points is large.
    If speed is an issue, you should write 'f' in terms of Numeric
    ufuncs and use the 'ufunc=1' feature described next.

    If called with 'ufunc=1', then 'f' should be a function that is
    composed entirely of ufuncs (i.e., a function that can operate
    element-by-element on whole matrices).  It will be passed the
    xvals and yvals as rectangular matrices.

    """

    xvals = Numeric.asarray(xvals, typecode)
    yvals = Numeric.asarray(yvals, typecode)

    if ufunc:
        return f(xvals[:,Numeric.NewAxis], yvals[Numeric.NewAxis,:])
    else:
        if typecode is None:
            # choose a result typecode based on what '+' would return
            # (yecch!):
            typecode = (Numeric.zeros((1,), xvals.typecode()) +
                        Numeric.zeros((1,), yvals.typecode())).typecode()

        m = Numeric.zeros((len(xvals), len(yvals)), typecode)
        for xi in range(len(xvals)):
            x = xvals[xi]
            for yi in range(len(yvals)):
                y = yvals[yi]
                m[xi,yi] = f(x,y)
        return m


class OptionException(Exception):
    """Raised for unrecognized option(s)"""
    pass

class DataException(Exception):
    """Raised for data in the wrong format"""
    pass


class PlotItem:
    """Plotitem represents an item that can be plotted by gnuplot.

    For the finest control over the output, you can create 'PlotItems'
    yourself with additional keyword options, or derive new classes
    from 'PlotItem'.

    Members:
    
      '_basecommand' -- a string holding the elementary argument that
                        must be passed to gnuplot's `plot' command for
                        this item; e.g., 'sin(x)' or '"filename.dat"'.
      '_options' -- a dictionary of (<option>,<string>) tuples
                    corresponding to the plot options that have been
                    specified for this object.  <option> is the option
                    as specified by the user; <string> is the string
                    that needs to be set in the command line to set
                    that option (or None if no string is needed).
                    E.g., {'title':'Data', 'with':'linespoints'}.

    """

    def __init__(self, basecommand, **keyw):
        """Construct a 'PlotItem'.

        Keyword options:

          'with=<string>' -- choose how item will be plotted, e.g.,
                             with='points 3 3'.
          'title=<string>' -- set the title to be associated with the item
                              in the plot legend.
          'title=None' -- choose 'notitle' option (omit item from legend).

        Note that omitting the title option is different than setting
        `title=None'; the former chooses gnuplot's default whereas the
        latter chooses `notitle'.

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

    def set_option(self, with=_unset, title=_unset, **keyw):
        """Set or change a plot option for this PlotItem.

        See documentation for __init__ for information about allowed
        options.  This function should be overridden by derived
        classes to allow additional options.

        """

        if with is not _unset:
            if with is None:
                self._options['with'] = (None, None)
            elif type(with) is type(''):
                self._options['with'] = (with, 'with %s' % with)
            else:
                OptionException('with=%s' % (with,))
        if title is not _unset:
            if title is None:
                self._options['title'] = (None, 'notitle')
            elif type(title) is type(''):
                self._options['title'] = (title, 'title "%s"' % title)
            else:
                OptionException('title=%s' % (title,))
        if keyw:
            # one or more unrecognized options; give error for one of them:
            (name,value) = keyw.items()[0]
            raise OptionException('%s=%s' % (name,value))

    def clear_option(self, name):
        """Clear (unset) a plot option.  No error if option was not set."""

        try:
            del self._options[name]
        except KeyError:
            pass

    # order in which options need to be passed to gnuplot:
    _option_sequence = ['binary', 'using', 'title', 'with']

    def command(self):
        """Build the 'plot' command to be sent to gnuplot.

        Build and return the 'plot' command, with options, necessary
        to display this item.

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
    gnuplot itself, as if you would type for example

        gnuplot> plot sin(x)

    into gnuplot itself.  The argument to the contructor is a string
    that should be a mathematical expression.  Example:

        g.plot(Func('sin(x)', with='line 3'))

    or a shorthand example:

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
        """Make an 'AnyFile' referencing the file with name 'filename'.

        If 'filename' is not specified, choose a random filename (but
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
        write_array(open(self.filename, 'w'), set)


class TempArrayFile(ArrayFile, TempFile):
    """An ArrayFile that is deleted automatically."""

    def __init__(self, set, filename=None):
        """Create a temporary file and write an array to it.

        Arguments:

          'set' -- a Numeric array of arbitrary dimension.
          'filename' -- the (optional) name of the file to which the
                        array should be written.  If 'filename' is not
                        specified, a random filename is chosen.

        When the 'TempArrayFile' is destroyed, the file is deleted
        automatically.

        """

        ArrayFile.__init__(self, set, filename)


class File(PlotItem):
    """A PlotItem representing a file that contains gnuplot data."""

    def __init__(self, file, **keyw):
        """Construct a File object.

        '<file>' can be either a string holding the filename of an
        existing file, or it can be an object of any class derived
        from 'AnyFile' (such as a 'TempArrayFile').

        Keyword arguments:

            'using=<int>' -- plot that column against line number
            'using=<tuple>' -- plot using a:b:c:d etc.
            'using=<string>' -- plot `using <string>' (allows gnuplot's
                                arbitrary column arithmetic)
            'binary=<boolean>' -- data in file is in binary format
                                  (only recognized for grid data for
                                  splot).

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
            raise OptionException
        # Use single-quotes so that pgnuplot can handle DOS filenames:
        apply(PlotItem.__init__, (self, "'%s'" % self.file.filename), keyw)

    def set_option(self, using=_unset, binary=_unset, **keyw):
        """Set or change options associated with this plotitem."""

        if using is not _unset:
            if using is None:
                self.clear_option('using')
            elif type(using) in [type(''), type(1)]:
                self._options['using'] = (using, 'using %s' % using)
            elif type(using) is type(()):
                self._options['using'] = (using,
                                          'using %s' %
                                          string.join(map(repr, using), ':'))
            else:
                raise OptionException('using=%s' % (using,))
        if binary is not _unset:
            if binary:
                assert GnuplotOpts.recognizes_binary_splot, \
                       OptionException('Gnuplot.py is currently configured to '
                                       'reject binary data!')
                self._options['binary'] = (1, 'binary')
            else:
                self._options['binary'] = (0, None)
        apply(PlotItem.set_option, (self,), keyw)


class Data(PlotItem):
    """Represents data from memory to be plotted with Gnuplot.

    Takes a numeric array from memory and outputs it to a temporary
    file that can be plotted by gnuplot.

    """

    def __init__(self, *set, **keyw):
        """Construct a 'Data' object from a numeric array.

        Create a 'Data' object (which is a type of 'PlotItem') out of
        one or more Float Python Numeric arrays (or objects that can
        be converted to a Float Numeric array).  If the routine is
        passed one array, the last index ranges over the values
        comprising a single data point (e.g., [x, y, and sigma]) and
        the rest of the indices select the data point.  If the routine
        is passed more than one array, they must have identical
        shapes, and then each data point is composed of one point from
        each array.  E.g., 'Data(x,x**2)' is a 'PlotItem' that
        represents x squared as a function of x.  For the output
        format, see the comments for 'write_array()'.

        The array is first written to a temporary file, then that file
        is plotted.  No copy is kept in memory.

        Keyword arguments:

            cols=<tuple> -- write only the specified columns from each
                data point to the file.  Since cols is used by python,
                the columns should be numbered in the python style
                (starting from 0), not the gnuplot style (starting
                from 1).
            inline=<bool> -- transmit the data to gnuplot "inline"
                rather than through a temporary file.  The default is
                the value of GnuplotOpts.prefer_inline_data.

        The keyword arguments recognized by 'PlotItem' can also be
        used here.

        """

        if len(set) == 1:
            # set was passed as a single structure
            set = float_array(set[0])
        else:
            # set was passed column by column (for example,
            # Data(x,y)); pack it into one big array (this will test
            # that sizes are all the same):
            set = float_array(set)
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
            self.inline = GnuplotOpts.prefer_inline_data

        if self.inline:
            f = StringIO()
            write_array(f, set)
            f.write('e\n')
            self._data = f.getvalue()
            apply(PlotItem.__init__, (self, "'-'"), keyw)
        else:
            self.file = TempFile()
            write_array(open(self.file.filename, 'w'), set)
            self._data = None
            apply(PlotItem.__init__, (self, "'%s'" % self.file.filename), keyw)

    def set_option(self, cols=_unset, inline=_unset, **keyw):
        """Set or change options associated with this plotitem.

        Note that the 'cols' and the 'inline' options cannot be
        changed via this routine.

        """

        if cols is not _unset:
            raise OptionException('Cannot modify cols option!')
        elif inline is not _unset:
            raise OptionException('Cannot modify inline option!')
        else:
            apply(PlotItem.set_option, (self,), keyw)

    def pipein(self, f):
        if self._data:
            f.write(self._data)


class GridData(PlotItem):
    """Holds data representing a function of two variables, for use in splot.

    'GridData' represents a function that has been tabulated on a
    rectangular grid.  The data are written to a file; no copy is kept
    in memory.

    """

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
        'GnuplotOpts.recognizes_binary_splot=0' in the appropriate
        gp*.py file.

        Thus if you have three arrays in the above format and a
        Gnuplot instance called g, you can plot your data by typing
        'g.splot(Gnuplot.GridData(data,xvals,yvals))'.

        """

        # Try to interpret data as an array:
        data = float_array(data)
        assert len(data.shape) == 2
        (numx, numy) = data.shape

        if xvals is None:
            xvals = Numeric.arange(numx)
        else:
            xvals = float_array(xvals)
            assert xvals.shape == (numx,)

        if yvals is None:
            yvals = Numeric.arange(numy)
        else:
            yvals = float_array(yvals)
            assert yvals.shape == (numy,)

        if inline is _unset:
            inline = (not binary) and GnuplotOpts.prefer_inline_data

        # xvals, yvals, and data are now all filled with arrays of data.
        if binary and GnuplotOpts.recognizes_binary_splot:
            assert not inline, \
                   OptionException('binary inline data not supported!')
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
                write_array(f, set)
                f.write('e\n')
                self._data = f.getvalue()
                apply(PlotItem.__init__, (self, "'-'"), keyw)
            else:
                self.file = TempFile()
                write_array(open(self.file.filename, 'w'), set)
                apply(PlotItem.__init__,
                      (self, "'%s'" % self.file.filename), keyw)
                self._data = None

            self._options['binary'] = (0, None)

    def set_option(self, binary=_unset, inline=_unset, **keyw):
        """Set or change options associated with this plotitem.

        Note that the binary and inline options cannot be changed."""

        if binary is not _unset:
            raise OptionException('Cannot modify binary option!')
        if inline is not _unset:
            raise OptionException('Cannot modify inline option!')
        apply(PlotItem.set_option, (self,), keyw)

    def pipein(self, f):
        if self._data:
            f.write(self._data)


class GridFunc(GridData):
    """Holds data representing a function of two variables, for use in splot.

    'GridFunc' computes a function f of two variables on a rectangular
    grid using grid_function.  After calculation the data are written
    to a file; no copy is kept in memory.  Note that this is quite
    different than 'Func' (which tells gnuplot to evaluate the
    function).

    """

    def __init__(self, f, xvals, yvals, ufunc=0, **keyw):
        """GridFunc constructor.

        Arguments:

            'f' -- the function to plot--a callable object for which
                   f(x,y) returns a number.
            'xvals' -- a 1-d array with dimension 'numx'
            'yvals' -- a 1-d array with dimension 'numy'
            'binary=<bool>' -- send data to gnuplot in binary format?
            'inline=<bool>' -- send data to gnuplot "inline"?
            'ufunc=<bool>' -- evaluate 'f' as a ufunc?

        'f' should be a callable object taking two arguments.
        'f(x,y)' will be computed at all grid points obtained by
        combining elements from 'xvals' and 'yvals'.

        If called with 'ufunc=1', then 'f' should be a function that
        is composed entirely of ufuncs, and it will be passed the
        xvals and yvals as rectangular matrices.

        See the documentation for GridData for an explanation of the
        'binary' and 'inline' arguments.

        Thus if you have a function f and two vectors xvals and yvals
        and a Gnuplot instance called g, you can plot the function by
        typing 'g.splot(Gnuplot.GridFunc(data,xvals,yvals))'.

        """

        xvals = float_array(xvals)
        (numx,) = xvals.shape

        yvals = float_array(yvals)
        (numy,) = yvals.shape

        # evaluate function:
        data = grid_function(f, xvals, yvals, ufunc=ufunc)

        apply(GridData.__init__, (self, data, xvals, yvals), keyw)


class GnuplotFile:
    """A file to which gnuplot commands can be written.

    Sometimes it is convenient to write gnuplot commands to a command
    file for later evaluation.  In that case, one of these objects is
    used as a mock gnuplot process.  Note that temporary files may be
    deleted before you have time to execute the file!

    Members:

    'gnuplot' -- the file object gathering the commands.

    Methods:

    '__init__' -- open the file.
    '__call__' -- write a gnuplot command to the file, followed by a
                  newline.
    'write' -- write an arbitrary string to the file.
    'flush' -- cause pending output to be written immediately.

    """

    def __init__(self, filename):
        """Open the file for writing."""

        self.gnuplot = open(filename, 'w')
        # forward write and flush methods:
        self.write = self.gnuplot.write
        self.flush = self.gnuplot.flush

    def __call__(self, s):
        """Write a command string to the file, followed by newline."""

        self.write(s + '\n')
        self.flush()


class Gnuplot(GnuplotProcess):
    """Interface to a gnuplot program.

    A Gnuplot represents a higher-level interface to a gnuplot
    program.  It can plot 'PlotItem's, which represent each thing to
    be plotted on the current graph.  It keeps a reference to each of
    the PlotItems used in the current plot, so that they (and their
    associated temporary files) are not deleted prematurely.

    Members:

    'itemlist' -- a list of the PlotItems that are associated with the
                  current plot.  These are deleted whenever a new plot
                  command is issued via the `plot' method.
    'plotcmd' -- 'plot' or 'splot', depending on what was the last
                 plot command.

    Methods:

    '__init__' -- if a filename argument is specified, the commands
                  will be written to that file instead of being piped
                  to gnuplot.
    'plot' -- clear the old plot and old PlotItems, then plot the
              arguments in a fresh plot command.  Arguments can be: a
              PlotItem, which is plotted along with its internal
              options; a string, which is plotted as a Func; or
              anything else, which is plotted as a Data.
    'splot' -- like 'plot', except for 3-d plots.
    'hardcopy' -- replot the plot to a postscript file (if filename
                  argument is specified) or pipe it to the printer as
                  postscript othewise.  If the option `color' is set
                  to true, then output color postscript.
    'replot' -- replot the old items, adding any arguments as
                additional items as in the plot method.
    'refresh' -- issue (or reissue) the plot command using the current
                 PlotItems.
    '__call__' -- pass an arbitrary string to the gnuplot process,
                  followed by a newline.
    'xlabel', 'ylabel', 'title' -- set corresponding plot attribute.
    'interact' -- read lines from stdin and send them, one by one, to
                  the gnuplot interpreter.  Basically you can type
                  commands directly to the gnuplot command processor.
    'load' -- load a file (using the gnuplot `load' command).
    'save' -- save gnuplot commands to a file (using gnuplot `save'
              command) If any of the PlotItems is a temporary file, it
              will be deleted at the usual time and the save file will
              be pretty useless :-).
    'clear' -- clear the plot window (but not the itemlist).
    'reset' -- reset all gnuplot settings to their defaults and clear
               the current itemlist.
    'set_string' -- set or unset a gnuplot option whose value is a
                    string.
    '_clear_queue' -- clear the current PlotItem list.
    '_add_to_queue' -- add the specified items to the current
                       PlotItem list.

    """

    def __init__(self, filename=None, persist=None, debug=0):
        """Create a Gnuplot object.

        Create a 'Gnuplot' object.  By default, this starts a gnuplot
        process and prepares to write commands to it.

        Keyword arguments:

          'filename=<string>' -- if a filename is specified, the
                                 commands are instead written to that
                                 file (e.g., for later use using
                                 'load').
          'persist=1' -- start gnuplot with the '-persist' option
                         (which creates a new plot window for each
                         plot command).  (This option is not available
                         on older versions of gnuplot.)
          'debug=1' -- echo the gnuplot commands to stderr as well as
                       sending them to gnuplot.

        """

        if filename is None:
            self.gnuplot = GnuplotProcess(persist=persist)
        else:
            assert persist is None, \
                   OptionException('Gnuplot with output to file does not '
                                   'allow persist option.')
            self.gnuplot = GnuplotFile(filename)
        self._clear_queue()
        self.debug = debug
        self.plotcmd = 'plot'

    def __call__(self, s):
        """Send a command string to gnuplot.

        Send the string s as a command to gnuplot, followed by a
        newline.  All communication with the gnuplot process (except
        for inline data) is through this method.

        """

        self.gnuplot(s)
        if self.debug:
            # also echo to stderr for user to see:
            sys.stderr.write('gnuplot> %s\n' % (s,))

    def refresh(self):
        """Refresh the plot, using the current PlotItems.

        Refresh the current plot by reissuing the gnuplot plot command
        corresponding to the current itemlist.

        """

        plotcmds = []
        for item in self.itemlist:
            plotcmds.append(item.command())
        self(self.plotcmd + ' ' + string.join(plotcmds, ', '))
        for item in self.itemlist:
            # Uses self.gnuplot.write():
            item.pipein(self.gnuplot)
        self.gnuplot.flush()

    def _clear_queue(self):
        """Clear the PlotItems from the queue."""

        self.itemlist = []

    def _add_to_queue(self, items):
        """Add a list of items to the itemlist (but don't plot them).

        'items' is a sequence of items, each of which should be a
        'PlotItem' of some kind, a string (interpreted as a function
        string for gnuplot to evaluate), or a Numeric array (or
        something that can be converted to a Numeric array).

        """

        for item in items:
            if isinstance(item, PlotItem):
                self.itemlist.append(item)
            elif type(item) is type(''):
                self.itemlist.append(Func(item))
            else:
                # assume data is an array:
                self.itemlist.append(Data(item))

    def plot(self, *items):
        """Draw a new plot.

        Clear the current plot and create a new 2-d plot containing
        the specified items.  Each arguments should be of the
        following types:

        'PlotItem' (e.g., 'Data', 'File', 'Func') -- This is the most
                   flexible way to call plot because the PlotItems can
                   contain suboptions.  Moreover, PlotItems can be
                   saved to variables so that their lifetime is longer
                   than one plot command; thus they can be replotted
                   with minimal overhead.

        'string' (e.g., 'sin(x)') -- The string is interpreted as
                 'Func(string)' (a function that is computed by
                 gnuplot).

        Anything else -- The object, which should be convertible to an
                         array, is converted to a 'Data' item, and
                         thus plotted as data.  If the conversion
                         fails, an exception is raised.

        """

        self.plotcmd = 'plot'
        self._clear_queue()
        self._add_to_queue(items)
        self.refresh()

    def splot(self, *items):
        """Draw a new three-dimensional plot.

        Clear the current plot and create a new 3-d plot containing
        the specified items.  Arguments can be of the following types:

        'PlotItem' (e.g., 'Data', 'File', 'Func', 'GridData' ) -- This
                   is the most flexible way to call plot because the
                   PlotItems can contain suboptions.  Moreover,
                   PlotItems can be saved to variables so that their
                   lifetime is longer than one plot command--thus they
                   can be replotted with minimal overhead.

        'string' (e.g., 'sin(x*y)') -- The string is interpreted as a
                 'Func()' (a function that is computed by gnuplot).

        Anything else -- The object is converted to a Data() item, and
                thus plotted as data.  Note that each data point
                should normally have at least three values associated
                with it (i.e., x, y, and z).  If the conversion fails,
                an exception is raised.

        """

        self.plotcmd = 'splot'
        self._clear_queue()
        self._add_to_queue(items)
        self.refresh()

    def replot(self, *items):
        """Replot the data, possibly adding new PlotItems.

        Replot the existing graph, using the items in the current
        itemlist.  If arguments are specified, they are interpreted as
        additional items to be plotted alongside the existing items on
        the same graph.  See 'plot' for details.

        """

        self._add_to_queue(items)
        self.refresh()

    def interact(self):
        """Allow user to type arbitrary commands to gnuplot.

        Read stdin, line by line, and send each line as a command to
        gnuplot.  End by typing C-d.

        """

        import time
        if sys.platform == 'win32':
            sys.stderr.write('Press Ctrl-z twice to end interactive input\n')
        else:
            # What should this be for the Macintosh?
            sys.stderr.write('Press C-d to end interactive input\n')
        while 1:
            try:
                line = raw_input('gnuplot>>> ')
            except EOFError:
                break
            self(line)
            time.sleep(0.2) # give a little time for errors to be written
        sys.stderr.write('\n')

    def clear(self):
        """Clear the plot window (without affecting the current itemlist)."""

        self('clear')

    def reset(self):
        """Reset all gnuplot settings to their defaults and clear itemlist."""

        self('reset')
        self.itemlist = []

    def load(self, filename):
        """Load a file using gnuplot's 'load' command."""

        self("load '%s'" % (filename,))

    def save(self, filename):
        """Save the current plot commands using gnuplot's 'save' command."""

        self("save '%s'" % (filename,))

    def set_string(self, option, s=None):
        """Set a string option, or if s is omitted, unset the option."""

        if s is None:
            self('set %s' % (option,))
        else:
            self('set %s "%s"' % (option, s))

    def xlabel(self, s=None):
        """Set the plot's xlabel."""

        self.set_string('xlabel', s)

    def ylabel(self, s=None):
        """Set the plot's ylabel."""

        self.set_string('ylabel', s)

    def title(self, s=None):
        """Set the plot's title."""

        self.set_string('title', s)

    def hardcopy(self, filename=None,
                 mode=None,
                 eps=None,
                 enhanced=None,
                 color=None,
                 solid=None,
                 duplexing=None,
                 fontname=None,
                 fontsize=None,
                 ):
        """Create a hardcopy of the current plot.

        Create a postscript hardcopy of the current plot to the
        default printer (if configured) or to the specified filename.

        Note that gnuplot remembers the postscript suboptions across
        terminal changes.  Therefore if you set, for example, color=1
        for one hardcopy then the next hardcopy will also be color
        unless you explicitly choose color=0.  Alternately you can
        force all of the options to their defaults by setting
        mode='default'.  I consider this a bug in gnuplot.

        Keyword arguments:

          'filename=<string>' -- if a filename is specified, save the
              output in that file; otherwise print it immediately
              using the 'default_lpr' configuration option.
          'mode=<string>' -- set the postscript submode ('landscape',
              'portrait', 'eps', or 'default').  The default is
              to leave this option unspecified.
          'eps=<bool>' -- shorthand for 'mode="eps"'; asks gnuplot to
              generate encapsulated postscript.
          'enhanced=<bool>' -- if set (the default), then generate
              enhanced postscript, which allows extra features like
              font-switching, superscripts, and subscripts in axis
              labels.  (Some old gnuplot versions do not support
              enhanced postscript; if this is the case set
              GnuplotOpts.prefer_enhanced_postscript=None.)
          'color=<bool>' -- if set, create a plot with color.  Default
              is to leave this option unchanged.
          'solid=<bool>' -- if set, force lines to be solid (i.e., not
              dashed).
          'duplexing=<string>' -- set duplexing option ('defaultplex',
              'simplex', or 'duplex').  Only request double-sided
              printing if your printer can handle it.  Actually this
              option is probably meaningless since hardcopy() can only
              print a single plot at a time.
          'fontname=<string>' -- set the default font to <string>,
              which must be a valid postscript font.  The default is
              to leave this option unspecified.
          'fontsize=<double>' -- set the default font size, in
              postscript points.

        Note that this command will return immediately even though it
        might take gnuplot a while to actually finish working.  Be
        sure to pause briefly before issuing another command that
        might cause the temporary files to be deleted.

        """

        if filename is None:
            assert GnuplotOpts.default_lpr is not None, \
                   OptionException('default_lpr is not set, so you can only '
                                   'print to a file.')
            filename = GnuplotOpts.default_lpr

        # Be careful processing the options.  If the user didn't
        # request an option explicitly, do not specify it on the 'set
        # terminal' line (don't even specify the default value for the
        # option).  This is to avoid confusing older versions of
        # gnuplot that do not support all of these options.  The
        # exception is 'enhanced', which is just too useful to have to
        # specify each time!

        setterm = ['set', 'terminal', 'postscript']
        if eps:
            assert mode is None or mode=='eps', \
                   OptionException('eps option and mode are incompatible')
            setterm.append('eps')
        else:
            if mode is not None:
                assert mode in ['landscape', 'portrait', 'eps', 'default'], \
                       OptionException('illegal mode "%s"' % mode)
                setterm.append(mode)
        if enhanced is None:
            enhanced = GnuplotOpts.prefer_enhanced_postscript
        if enhanced is not None:
            if enhanced: setterm.append('enhanced')
            else: setterm.append('noenhanced')
        if color is not None:
            if color: setterm.append('color')
            else: setterm.append('monochrome')
        if solid is not None:
            if solid: setterm.append('solid')
            else: setterm.append('dashed')
        if duplexing is not None:
            assert duplexing in ['defaultplex', 'simplex', 'duplex'], \
                   OptionException('illegal duplexing mode "%s"' % duplexing)
            setterm.append(duplexing)
        if fontname is not None:
            setterm.append('"%s"' % fontname)
        if fontsize is not None:
            setterm.append('%s' % fontsize)
        self(string.join(setterm))
        self.set_string('output', filename)
        # replot the current figure (to the printer):
        self.refresh()
        # reset the terminal to its `default' setting:
        self('set terminal %s' % GnuplotOpts.default_term)
        self.set_string('output')


if __name__ == '__main__':
    import demo
    demo.demo()


