#!/usr/local/bin/python
# $Id$

# Simple Gnuplot interface.

# Written by Michael Haggerty <mhagger@blizzard.harvard.edu>
# Derived from earlier version by Konrad Hinsen <hinsen@ibs.ibs.fr>

import os, string, tempfile

# gnuplot plotting object:
class gnuplot:
    def __init__(self, filename=None):
	if filename == None:
	    self.gnuplot = os.popen('gnuplot', 'w')
	else:
	    self.gnuplot = open(filename, 'w')
	self('set terminal x11')
    	self.filelist = []

    def rmfiles(self):
	for file in self.filelist:
	    os.unlink(file)
	self.filelist = []

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
    	plotlist = []
    	for set in data:
    	    filename = tempfile.mktemp()
    	    file = open(filename, 'w')
    	    is_sequence = self._isSequence(set[0])
    	    for point in set:
    		if is_sequence:
    		    for coordinate in point:
    			file.write(`coordinate` + ' ')
    		else:
    		    file.write(`point`)
    		file.write('\n')
    	    file.close()
    	    if is_sequence:
    		plotlist.append((filename, len(set[0])))
    	    else:
    		plotlist.append((filename, 1))
    	    self.filelist.append(filename)
    	command = 'plot '
    	for item in plotlist:
    	    filename, n = item
    	    if n == 1:
    		command = command + '"' + filename + '" notitle, '
    	    else:
    		for i in range(n-1):
    		    command = command + '"' + filename + \
    			      '" using 1:' + `i+2` + ' notitle, '
    	command = command[:-2]
    	if keywords.has_key('file'):
    	    self('set terminal postscript')
    	    self('set output "' + keywords['file'] + '"')
    	    self(command)
	    self('set terminal x11')
	    self('set output')
    	else:
	    self('set terminal x11')
	    self(command)

    def xlabel(self, s=None):
	if s==None:
	    self("set ylabel")
	else:
	    self("set xlabel '" + s + "'")

    def ylabel(self, s=None):
	if s==None:
	    self("set ylabel")
	else:
	    self("set ylabel '" + s + "'")

    def replot(self):
	self("replot")

    def _isSequence(self, object):
	n = -1
	try: n = len(object)
	except: pass
	return n >= 0

#
# Demo code
#
if __name__ == '__main__':

    g1 = gnuplot()
    # List of (x, y) pairs
    g1.plot([(0.,1),(1.,5),(2.,3),(3.,4)])

    g2 = gnuplot()
    # List of y values, file output
    g2.plot([1, 5, 3, 4], file = 'junk.ps')

    # Two plots; each given by a 2d array
    from Numeric import *
    x = arange(10)
    y1 = x**2
    y2 = (10-x)**2
    g3 = gnuplot()
    g3.plot(transpose(array([x, y1])), transpose(array([x, y2])))

