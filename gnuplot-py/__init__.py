# Simple Gnuplot interface.
#
# Written by Konrad Hinsen <hinsen@ibs.ibs.fr>
# last revision: 1997-5-23
#
# Caution: If you use a Gnuplot version earlier than 3.6beta,
# every call for a screen display creates another gnuplot
# process; these processes are never closed. There seems to be no
# other way to make gnuplot behave as it should.

import os, string, tempfile

#
# Test if Gnuplot is new enough to know the option -persist
#
filename = tempfile.mktemp()
file = open(filename, 'w')
file.write('\n')
file.close()
gnuplot = os.popen('gnuplot -persist ' + filename + ' 2>&1', 'r')
response = gnuplot.readlines()
gnuplot.close()
os.unlink(filename)
old_version = response and string.index(response[0], '-persist') >= 0

#
# Generate a plot
#
class gnuplot:
    def __init__(self):
	self.gnuplot = os.popen('gnuplot', 'w')
	self.gnuplot.write('set terminal x11\n')
    	self.filelist = []

    def rmfiles(self):
	for file in self.filelist:
	    os.unlink(file)
	self.filelist = []

    def __del__(self):
	self.gnuplot.write('quit\n')
	self.gnuplot.close()
	self.rmfiles()

    def __call__(self, s):
	self.gnuplot.write(s)
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
    		command = command + '"' + filename + '", '
    	    else:
    		for i in range(n-1):
    		    command = command + '"' + filename + \
    			      '"  using 1:' + `i+2` + ', '
    	command = command[:-2] + '\n'
    	if keywords.has_key('file'):
    	    self('set terminal postscript\n')
    	    self('set output "' + keywords['file'] + '"\n')
    	    self(command)
	    self('set terminal x11\n')
	    self('set output\n')
    	else:
	    self('set terminal x11\n')
	    self(command)

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

