#!/usr/local/bin/python -tO
# $Id$

# A more complicated gnuplot interface.

# Written by Michael Haggerty <mhagger@blizzard.harvard.edu>
# Derived from earlier version by Konrad Hinsen <hinsen@ibs.ibs.fr>

# New features:
#  +  A gnuplot session is an instance of class `gnuplot', so multiple
#     sessions can be open at once:
#         g = gnuplot()
#  +  The implicitly-generated gnuplot commands can be stored to a file
#     instead of executed immediately:
#         g = gnuplot("commands.gnuplot")
#  +  Can pass arbitrary commands to the gnuplot command interpreter:
#         g("set pointsize 2")
#  +  A gnuplot object knows how to plot three types of `plotitem':
#     `data', `file', and `func'tion.
#  +  Any plotitem can have optional `title' and/or `with' suboptions
#  +  Builtin plotitem types:
#      *  data(array1) -- data from a Python list or NumPy array
#         (option: `cols')
#      *  file("filename") -- data from an existing data file (option:
#         `using')
#      *  func("exp(4.0 * sin(x))") -- functions (passed as a string
#         for gnuplot to evaluate)
#  +  Communication of data between python and gnuplot is via
#     temporary files, which are deleted automatically when their
#     associated plotitem is deleted.
#  +  Plotitems can be created as objects that are kept around and
#     plotted multiple times---temporary files need only be written
#     once.
#  +  Can use `replot' method to add traces to an existing plot.
#  +  Can make persistent gnuplot windows by using the constructor
#     option `persist=1'.

# Restrictions:
#  -  Only 2-d plots are supported
#  -  There is no provision for missing data points in array data
#  -  Does not check whether persistent windows are really supported
#     by the version of gnuplot used (but persistent windows are
#     anyway not the default).
#  -  Plotting to a postscript file is via new `hardcopy' method
#     instead of a option on the `plot' method as in the older
#     version.
#  -  Doesn't automatically plot using 1:2, 1:3, 1:4, etc for
#     multi-columned data as did the old version.  Instead make a
#     temporary data file then plot that file multiple times with
#     different `using=' options:
#         a = temparrayfile(array_nx3)
#         g.plot(file(a, using=(1,2)), file(a, using=(1,3)))
#  -  All of these classes perform their resource deallocation when
#     __del__ is called.  I understand this is not completely
#     reliable, so it is possible that temporary files will be left
#     around.
#  -  There is no way to change the plotting options of plotitems
#     after they are created.


import sys, os, string, tempfile, Numeric


# raised for unrecognized option(s):
class OptionException(Exception):
    pass

# plotitem represents an item that can be plotted by gnuplot.  For the
# finest control over the output, you can create the plotitems yourself
# with additional options or derive new classes from plotitem.
# Members:
#     basecommand -- a string holding the elementary argument that
#                    must be passed to gnuplot's `plot' command for
#                    this item; e.g., 'sin(x)' or '"filename.dat"'.
#     options -- a list of strings that need to be passed as options
#                to the plot command (in the order required); e.g.,
#                ['title "data"', 'with linespoints'].
#     title -- the title requested (undefined if not requested).  Note
#              that `title=None' implies the `notitle' option, whereas
#              omitting the title option implies no option (the
#              gnuplot default is then used).
#     with -- the string requested as a `with' option (undefined if
#             not requested)
class plotitem:
    def __init__(self, basecommand, **keyw):
        self.basecommand = basecommand
        self.options = []
        if keyw.has_key('title'):
            self.title = keyw['title']
            del keyw['title']
            if self.title is None:
                self.options.append('notitle')
            else:
                self.options.append('title "' + self.title + '"')
        if keyw.has_key('with'):
            self.with = keyw['with']
            del keyw['with']
            self.options.append('with ' + self.with)
        if keyw:
            raise OptionException, keyw

    # return the `plot' command, with options, necessary to print out
    # this item:
    def command(self):
        if self.options:
            return self.basecommand + ' ' + string.join(self.options, ' ')
        else:
            return self.basecommand

    # if the plot command requires data to be put on stdin (i.e.,
    # `plot ""'), this method will put that data there.
    def pipein(self, file):
        pass


# represents a mathematical expression that is to be computed by
# gnuplot itself, as in
#     gnuplot> plot sin(x)
# The argument to the contructor is a string which is a gnuplot
# expression.  Example:
#     g.plot(func("sin(x)", with="line 3"))
# or shorthand
#     g.plot("sin(x)")
class func(plotitem):
    def __init__(self, funcstring, **keyw):
        apply(plotitem.__init__, (self, funcstring), keyw)


# An anyfile represents any kind of file, but presumably one that
# holds data in a format readable by gnuplot.  This class simply
# remembers the filename; the existence and format of the file are not
# checked whatsoever.  Note that this is not a plotitem, though it is
# used by the `file' plotitem.  Members:
#   self.filename -- the filename of the file
class anyfile:
    def __init__(self, filename):
        self.filename = filename


# A temp_file is a file that is deleted when the python object is
# deleted.  WARNING: whatever filename you pass to this constructor
# WILL BE DELETED when the temp_file object is deleted, even if it was
# a pre-existing file!  This is intended to be used as a parent class
# of temparrayfile.
class temp_file(anyfile):
    def __del__(self):
        os.unlink(self.filename)


# When an arrayfile is constructed, it creates a file and fills it
# with the contents of a 2-d Numeric array in the format expected by
# gnuplot.  The filename can be specified, otherwise a random filename
# is chosen.  The file is NOT deleted automatically.
class arrayfile(anyfile):
    def __init__(self, set, filename=None):
        # <set> must be a Numeric array
        assert(len(set.shape) == 2)
        (points, columns) = set.shape
        assert(points > 0)
        assert(columns > 0)
        if not filename:
            filename = tempfile.mktemp()
        f = open(filename, 'w')
        for point in set:
            f.write(string.join(map(repr, point.tolist()), ' ') + '\n')
        f.close()
        anyfile.__init__(self, filename)


# Just like an arrayfile except that the file is deleted automatically
# when the python object is deleted.
class temparrayfile(arrayfile, temp_file):
    def __init__(self, set, filename=None):
        arrayfile.__init__(self, set, filename)


# file is a plotitem that represents a file that should be plotted by
# gnuplot.  <file> can be either a string holding the filename of a
# file that already exists, or it can be any kind of anyfile (such as
# a temparrayfile).  Keyword arguments recognized (in addition to
# those supplied by plotitem):
#     using=<n> -- plot that column against line number
#     using=<tuple> -- plot using a:b:c:d etc.
#     using=<string> -- plot `using <string>' (allows gnuplot's
#                       arbitrary column arithmetic) 
# Note that the `using' option is interpreted by gnuplot, so columns
# must be numbered starting with 1.  Other keyword arguments are
# passed along to plotitem.  The default `title' for an anyfile
# plotitem is `notitle'.
class file(plotitem):
    def __init__(self, file, using=None, **keyw):
        if isinstance(file, anyfile):
            self.file = file
            # If no title is specified, then use `notitle' for
            # temp_files (to avoid using the temporary filename as the
            # title.)
            if isinstance(file, temp_file) and not keyw.has_key('title'):
                keyw['title'] = None
        elif type(file) == type(""):
            self.file = anyfile(file)
        else:
            raise OptionException
        apply(plotitem.__init__, (self, '"' + self.file.filename + '"'), keyw)
        self.using = using
        if self.using is None:
            pass
        elif type(self.using) == type(""):
            self.options.insert(0, "using " + self.using)
        elif type(self.using) == type(()):
            self.options.insert(0,
                                "using " +
                                string.join(map(repr, self.using), ':'))
        elif type(self.using) == type(1):
            self.options.insert(0, "using " + `self.using`)
        else:
            raise OptionException, 'using=' + `self.using`


# Create a plotitem out of a Python numeric array (or something that
# can be converted to a Float numeric array).  The array is first
# written to a temporary file, then that file is plotted.  Keyword
# arguments recognized (in addition to those supplied by plotitem):
#     cols=<tuple>
# which outputs only the specified columns of the array to the file.
# Columns are of course numbered in the python style, not the gnuplot
# style.  The data are written to the temp file; no copy is kept in
# memory.
class data(file):
    def __init__(self, set, cols=None, **keyw):
        set = Numeric.asarray(set, Numeric.Float)
        if cols is not None:
            set = Numeric.take(set, cols, 1)
        apply(file.__init__, (self, temparrayfile(set)), keyw)


# gnuplot plotting object.  A gnuplot represents a running gnuplot
# process and a pipe to communicate with it.  It keeps a reference to
# each of the plotitems used in the current plot, so that they (and
# their associated temporary files) are not deleted prematurely.
# Members:
#     gnuplot -- the pipe to gnuplot or a file gathering the commands
#     itemlist -- a list of the plotitems that are associated with the
#                 current plot.  These are deleted whenever a new plot
#                 command is issued via the `plot' method.
# Methods:
#     __init__ -- if a filename argument is specified, the commands
#                 will be written to that file instead of being piped
#                 to gnuplot immediately.
#     __call__ -- pass an arbitrary string to the gnuplot process,
#                 followed by a newline.
#     refresh -- issue (or reissue) the plot command using the current
#                plotitems.
#     plot -- clear the old plot and old plotitems, then plot its
#             arguments in a fresh plot command.  Arguments can be: a
#             plotitem, which is plotted along with its internal
#             options; a string, which is plotted as a func(); or
#             anything else, which is plotted as a data().
#     replot -- replot the old items, adding any arguments as
#               additional items as in the plot method.
#     interact -- read lines from stdin and send them, one by one, to
#                 the gnuplot interpreter.  Basically you can type
#                 commands directly to the gnuplot command processor
#                 (though without command-line editing).
#     load -- load a file (using the gnuplot `load' command).
#     save -- save gnuplot commands to a file (using gnuplot `save'
#             command, not the saved plotitems).
#     xlabel,ylabel --  set xlabel or ylabel to be a string.
#     hardcopy -- replot the plot to a postscript file (if filename
#                 argument is specified) or pipe it to lpr othewise.
#                 If the option `color' is set to true, then output
#                 color postscript.
class gnuplot:
    def __init__(self, filename=None, persist=0, debug=0):
        if filename:
            # put gnuplot commands into a file:
            self.gnuplot = open(filename, 'w')
        else:
            if persist:
                self.gnuplot = os.popen('gnuplot -persist', 'w')
            else:
                self.gnuplot = os.popen('gnuplot', 'w')
        self.itemlist = []
        self.debug = debug

    def __del__(self):
        self('quit')
        self.gnuplot.close()

    # send a string to the gnuplot process, followed by a newline:
    def __call__(self, s):
        self.gnuplot.write(s + "\n")
        self.gnuplot.flush()
        if self.debug:
            # also echo to stderr for user to see:
            sys.stderr.write("gnuplot> %s\n" % (s,))

    # refresh the plot, using the current plotitems:
    def refresh(self):
        plotcmds = []
        for item in self.itemlist:
            plotcmds.append(item.command())
        self('plot ' + string.join(plotcmds, ', '))
        for item in self.itemlist:
            item.pipein(self.gnuplot)

    # call the gnuplot `plot' command:
    def plot(self, *data):
        # remove old files:
        self.itemlist = []
        apply(self.replot, data)

    # replot the data, possibly adding new plotitems:
    def replot(self, *items):
        for item in items:
            if isinstance(item, plotitem):
                self.itemlist.append(item)
            elif type(item) is type(""):
                self.itemlist.append(func(item))
            else:
                # assume data is an array:
                self.itemlist.append(data(item))
        self.refresh()

    def interact(self):
        sys.stderr.write("Press C-d to end interactive input\n")
        while 1:
            sys.stderr.write("gnuplot>>> ")
            line = sys.stdin.readline()
            if not line:
                break
            if line[-1] == "\n": line = line[:-1]
            self(line)

    def load(self, filename=None):
        if filename is None:
            self.interact()
        else:
            self('load "%s"' % (filename,))

    def save(self, filename):
        self('save "%s"' % (filename,))

    # Set a string option, or if s is omitted, unset the option.
    def set_string(self, option, s=None):
        if s is None:
            self('set %s' % (option,))
        else:
            self('set %s "%s"' % (option, s))

    def xlabel(self, s=None): self.set_string('xlabel', s)
    def ylabel(self, s=None): self.set_string('ylabel', s)
    def title(self, s=None): self.set_string('title', s)

    def hardcopy(self, filename = '| lpr', eps = 0, color = 0):
        setterm = ['set', 'term', 'postscript']
        if eps: setterm.append('eps')
        else: setterm.append('default')
        setterm.append('enhanced')
        if color: setterm.append('color')
        self(string.join(setterm))
        self('set output "%s"' % (filename,))
        self('replot')
        self('set term x11')
        self('set output')


#
# Demo code
#
if __name__ == '__main__':
    from Numeric import *
    import sys

    g1 = gnuplot(debug=1)
    # List of (x, y) pairs
    g1.plot([(0.,1.1),(1.,5.8),(2.,3.3),(3.,4.2)])


    # Two plots given by arrays and one by a gnuplot function:
    g2 = gnuplot(debug=1)
    x = arange(10)
    y1 = x**2
    y2 = (10-x)**2
    g2.plot(data(transpose((x, y1)), title="calculated by python"),
            func("x**2", title="calculated by gnuplot"),
            data(transpose((x, y2)), with="linesp")
            )
    print "Generating postscript file 'junk.ps'"
    g2.hardcopy('junk.ps', color=1)

    sys.stderr.write("Press return to continue...\n")
    sys.stdin.readline()

    del g1, g2

