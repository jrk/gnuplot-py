#!/usr/local/bin/python
# $Id$

# Simple Gnuplot interface.

# Written by Michael Haggerty <mhagger@blizzard.harvard.edu>
# Derived from earlier version by Konrad Hinsen <hinsen@ibs.ibs.fr>

# New restrictions: can only plot 2-d numeric arrays or python
# sequences which are convertable (via Numeric.asarray) to such.

# Does not try to make persistent windows; instead simply leaves
# gnuplot running for as long as the gnuplot object is in existence.

import os, string, tempfile, Numeric

class plottable:
    def __init__(self):
	pass

    def __del__(self):
	pass

    def commands(self):
	return []

class plotfile:
    def __init__(self, set):
	# ensure that the argument is a Numeric array:
	set = Numeric.asarray(set, Float)
	self.filename = tempfile.mktemp()
	file = open(self.filename, 'w')
	assert(len(set.shape) == 2)
	(points,self.len) = set.shape
	assert(points > 0)
	assert(self.len > 0)
	for point in set:
	    file.write(string.join(map(repr, point.tolist()), ' ') + '\n')
	file.close()

    def __del__(self):
	os.unlink(self.filename)

    # return a list of the `plot' command(s) necessary to print out
    # this item:
    def commands(self):
    	if self.len == 1:
    	    return ['"' + self.filename + '" notitle']
	else:
	    c = ['"' + self.filename + '" using 1:2 notitle']
	    # for additional columns, filename can be abbreviated to '""':
	    for i in range(3, self.len + 1):
    		c.append('"" using 1:' + `i` + ' notitle')
	    return c


# gnuplot plotting object:
class gnuplot:
    def __init__(self, filename=None):
	if filename == None:
	    self.gnuplot = os.popen('gnuplot', 'w')
	else:
	    self.gnuplot = open(filename, 'w')
	self('set terminal x11')
    	self.itemlist = []

    def rmfiles(self):
	# Should delete plotfile objects automatically:
	self.itemlist = []

    def __del__(self):
	self('quit')
	self.gnuplot.close()
	self.rmfiles()

    def __call__(self, s):
	self.gnuplot.write(s + "\n")
	self.gnuplot.flush()

    def plot(self, *data, **keywords):
	# remove old files:
	self.rmfiles()
    	for set in data:
    	    self.itemlist.append(plotfile(set))
	plotcmds = []
	for item in self.itemlist:
	    plotcmds = plotcmds + item.commands()
    	command = 'plot ' + string.join(plotcmds, ', ')
    	if keywords.has_key('file'):
    	    self('set terminal postscript enhanced')
    	    self('set output "' + keywords['file'] + '"')
    	    self(command)
	    self('set terminal x11')
	    self('set output')
    	else:
	    self(command)

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
	g('set term postscript enhanced')
	g('set output "' + filename + '"')
	g('replot')
	g('set term x11')
	g('set output')

    def replot(self):
	self('replot')


#
# Demo code
#
if __name__ == '__main__':
    from Numeric import *
    import sys

    g1 = gnuplot()
    # List of (x, y) pairs
    g1.plot([(0.,1),(1.,5),(2.,3),(3.,4)])

    g2 = gnuplot()
    # List of y values, file output
    print "Generating postscript file 'junk.ps'"
    g2.plot([[1], [5], [3], [4]], file = 'junk.ps')

    # Two plots; each given by a 2d array
    x = arange(10)
    y1 = x**2
    y2 = (10-x)**2
    g3 = gnuplot()
    g3.plot(transpose(array([x, y1])), transpose(array([x, y2])))

    sys.stdout.write("Press return to continue...\n")
    sys.stdin.readline()

    del g1, g2, g3

