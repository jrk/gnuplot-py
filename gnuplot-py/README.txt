Gnuplot.py -- A pipe-based interface to the gnuplot plotting program.

Documentation
-------------

The module is documented extensively, but the documentation is all
inside Gnuplot.py in the form of documentation strings and comments.
Don't be shy, just open up Gnuplot.py with your favorite text editor
and take a look.  Especially look at the demo() subroutine and learn
by example.

To run a demo, type `python Gnuplot.py'.  This should pop up three
gnuplot windows on your screen containing simple graphs, and also
write a postscript file called `gnuplot_test_plot.ps' to the current
directory.

Installation
------------

Naturally, you must have the gnuplot program installed for this module
to be of use to you.  Gnuplot can be obtained via
<http://www.cs.dartmouth.edu/gnuplot_info.html>.

This module itself consists of only one file, Gnuplot.py, which is
pure Python.  There are a few configuration options near the beginning
of the file that you might need to change (see the comments for
details).  If your copy of gnuplot is started by typing something
other than `gnuplot' you will have to specify the correct command
there.  Otherwise most things will probably work OK without changes.

To install the module, just place Gnuplot.py in any directory on your
python path.  You can import it into your python programs using
`import Gnuplot'.

Feedback
--------

Gnuplot.py was developed on a unix computer and should work without
much problem on other unix computers.  I've heard from users that it
doesn't run under windows without modifications, but since I don't use
windows myself I'm relying one somebody else to share their windows
mods with me.

I would love to have feedback from people letting me know whether they
find this module useful.  Let me know about any problems, suggestions,
or enhancements.

License
-------

See the file LICENSE for license info.  Basically Gnuplot is GPL.


Michael Haggerty
<mhagger@blizzard.harvard.edu>
