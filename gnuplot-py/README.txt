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
directory.  For a more thorough test, type `python Gnuplot_test.py'
which goes systematically through most Gnuplot.py features.


Installation
------------

Obviously, you must have the gnuplot program if Gnuplot.py is to be of
any use to you.  Gnuplot can be obtained via
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


Installation on Windows
-----------------------

I don't run Windows, but thanks to the help of users there is now a
scheme that supposedly works on Windows.  Any feedback or additional
suggestions having to do with Windows would be especially appreciated,
especially if you know how to make Gnuplot.py work under Windows
without having to install pgnuplot.exe.

Apparently the MS-Windows gnuplot executable (wgnuplot.exe) doesn't
accept commands on standard input, and so Gnuplot.py cannot
communicate with it directly.  However, recent beta versions of
gnuplot (version 3.7.0.8, for example) include a simple little
self-contained program called `pgnuplot.exe' that accepts commands on
stdin and passes them to wgnuplot.  So to run Gnuplot.py on Windows,
first install pgnuplot.exe.  This can be done, for example, by
downloading a beta version of gnuplot from
<ftp://ftp.gnuplot.vt.edu/pub/gnuplot/beta/> and compiling pgnuplot.c.

[Does anybody know if it is possible to use pgnuplot.exe with earlier
versions of gnuplot?  That would save users the trouble of
reinstalling the whole gnuplot package.]

After pgnuplot.exe is installed, install Gnuplot.py as described
in the previous section.


Feedback
--------

I would love to have feedback from people letting me know whether they
find Gnuplot.py useful.  And certainly let me know about any problems,
suggestions, or enhancements.  My address is at the bottom of this
file.

Gnuplot.py has been tested with gnuplot version 3.7, and I believe it
should work with version 3.5 (though some features, like enhanced
postscript mode, aren't available).  Let me know if you have trouble.

Gnuplot.py was developed on a unix computer and should work without
much problem on other unix computers.  If you need to modify it for
your system tell me what was necessary.

Gnuplot.py should now work under windows (see above).  Feedback in
this area is especially appreciated since I can't test it.


License
-------

See the file LICENSE for license info.  Basically Gnuplot is GPL.


Credits
-------

Thanks to the following people:

Konrad Hinsen <hinsen@ibs.ibs.fr> wrote the first, procedural
interface version of Gnuplot.py.

Berthold Hoellmann <se6y095@public.uni-hamburg.de> contributed some
docstring changes to allow docs to be generated with pythondoc.

Francois Ladouceur <f.ladouceur@virtualphotonics.com> and Craig
Schardt <lazrnerd@ufl.edu> contributed changes that enable Gnuplot.py
to work under MS-Windows.


Michael Haggerty
<mhagger@blizzard.harvard.edu>
