# $Id$

# This Makefile shouldn't be needed by end users.  I use it to
# remember the commands to generate the documentation and create a
# distribution.

# happydoc seems to need to run from the parent directory to
# understand the module structure.  This will be a problem if the
# directory name is not "Gnuplot".
.PHONY : documentation
documentation :
	(cd ..; happydoc -d Gnuplot/doc Gnuplot docset_title='Gnuplot.py')

.PHONY : distribution
distribution :
	python setup.py sdist --formats=gztar,zip

.PHONY : rpm
rpm :
	python setup.py bdist_rpm

