#!/usr/local/bin/python
# $Id$

# Simple Gnuplot interface.

# Written by Michael Haggerty <mhagger@blizzard.harvard.edu>
# Derived from earlier version by Konrad Hinsen <hinsen@ibs.ibs.fr>

# New restrictions:

# Can only plot 2-d numeric arrays or python sequences which are
# convertable (via Numeric.asarray) to such.

# Does not try to make persistent windows; instead simply leaves
# gnuplot running for as long as the gnuplot object is in existence.

# Cannot plot to a postscript file with the `plot' method; use
# `hardcopy' instead.

# Doesn't plot using 1:2, 1:3, 1:4, etc for multi-columned data as did
# the old version.  Instead make a data file then the `using=' option.

import sys, os, string, tempfile, Numeric

debug = 0

# raised for unrecognized option(s):
class OptionException(Exception):
    pass

# plotitem represents an item that can be plotted by gnuplot.
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

    # return the `plot' command necessary to print out this item:
    def command(self):
	if self.options:
	    return self.basecommand + ' ' + string.join(self.options, ' ')
	else:
	    return self.basecommand

    # if the plot command requires data to be put on stdin (i.e.,
    # `plot ""'), this method will put that data there.
    def pipein(self, file):
	pass


class func(plotitem):
    def __init__(self, funcstring, **keyw):
	apply(plotitem.__init__, (self, funcstring), keyw)


# represents a file that holds data in a format readable by gnuplot.
#   self.filename -- the filename of the temp file
class anyfile:
    def __init__(self, filename):
	self.filename = filename


# create a file and write set (which must be a 2-D Numeric
# array) to the file.
class arrayfile(anyfile):
    def __init__(self, set):
	# <set> must be a Numeric array
	assert(len(set.shape) == 2)
	(points, columns) = set.shape
	assert(points > 0)
	assert(columns > 0)
	filename = tempfile.mktemp()
	f = open(filename, 'w')
	for point in set:
	    f.write(string.join(map(repr, point.tolist()), ' ') + '\n')
	f.close()
	anyfile.__init__(self, filename)


# an arrayfile that deletes the referred-to file when it is deleted.
class temparrayfile(arrayfile):
    def __init__(self, set):
	arrayfile.__init__(self, set)

    def __del__(self):
	os.unlink(self.filename)


# <file> is a temparrayfile
# Keyword arguments recognized:
#   using=<n> -- plot that column against line number
#   using=<tuple> -- plot using a:b:c:d etc.
# Other keyword arguments are passed along to plotitem.
class file(plotitem):
    def __init__(self, file, using=None, **keyw):
	if isinstance(file, anyfile):
	    self.file = file
	elif type(file) == type(""):
	    self.file = anyfile(file)
	else:
	    raise OptionException
	# By default, notitle for these plots:
	if not keyw.has_key('title'):
	    keyw['title'] = None
	apply(plotitem.__init__, (self, '"' + self.file.filename + '"'), keyw)
	self.using = using
	if self.using is None:
	    pass
	elif type(self.using) == type(""):
	    self.options.insert(0, "using " + self.using)
	elif type(self.using) == type(()):
	    self.options.insert(0,
				"using " + string.join(map(repr, self.using),
						       ':'))
	elif type(self.using) == type(1):
	    self.options.insert(0, "using " + `self.using`)
	else:
	    raise OptionException, 'using=' + `self.using`

    def __del__(self):
	pass


class data(file):
    def __init__(self, set, **keyw):
	set = Numeric.asarray(set, Numeric.Float)
	apply(file.__init__, (self, temparrayfile(set)), keyw)


# gnuplot plotting object.  A gnuplot basically represents a running
# gnuplot process, while keeping track of the temporary files
# etc. that have been created for communication with that process.
#
# Members:
#   gnuplot -- a pipe to gnuplot or a file gathering the commands
#   itemlist -- a list of the plotitems that are associated with the
#               current plot.  These are deleted whenever a new plot
#               command is issued.
#
class gnuplot:
    def __init__(self, filename=None):
	if filename == None:
	    self.gnuplot = os.popen('gnuplot', 'w')
	else:
	    # put gnuplot commands into a file:
	    self.gnuplot = open(filename, 'w')
    	self.itemlist = []

    def __del__(self):
	self('quit')
	self.gnuplot.close()

    # send a string to the gnuplot process, followed by a newline:
    def __call__(self, s):
	self.gnuplot.write(s + "\n")
	self.gnuplot.flush()
	if debug:
	    sys.stderr.write("gnuplot> " + s + "\n")

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
	    if line == "":
		break
	    if line[-1] == "\n": line = line[:-1]
	    self(line)

    def load(self, filename=None):
	if filename is None:
	    self.interact()
	else:
	    self('load "' + filename + '"')

    def xlabel(self, s=None):
	if s==None:
	    self('set ylabel')
	else:
	    self('set xlabel "' + s + '"')

    def ylabel(self, s=None):
	if s==None:
	    self('set ylabel')
	else:
	    self('set ylabel "' + s + '"')

    def hardcopy(self, filename = '| lpr'):
	self('set term postscript enhanced')
	self('set output "' + filename + '"')
	self('replot')
	self('set term x11')
	self('set output')


#
# Demo code
#
if __name__ == '__main__':
    from Numeric import *
    import sys

    debug = 1

    g1 = gnuplot()
    # List of (x, y) pairs
    g1.plot([(0.,1),(1.,5),(2.,3),(3.,4)])


    # Two plots given by arrays and one by a gnuplot function:
    x = arange(10)
    y1 = x**2
    y2 = (10-x)**2
    g2 = gnuplot()
    g2.plot(data(transpose((x, y1)), title="calculated by python"),
	    func("x**2", title="calculated by gnuplot"),
	    data(transpose((x, y2)), with="linesp")
	    )
    print "Generating postscript file 'junk.ps'"
    g2.hardcopy('junk.ps')

    sys.stderr.write("Press return to continue...\n")
    sys.stdin.readline()

    del g1, g2

