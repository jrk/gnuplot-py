Gnuplot.py -- A pipe-based interface to the gnuplot plotting program.

The current version of Gnuplot.py can be obtained from

    http://monsoon.harvard.edu/~mhagger/Gnuplot/Gnuplot.html


Documentation
-------------

The best way to get started is to run the demo by typing `python
demo.py'.  This should pop up a few gnuplot windows, one after
another, on your screen containing simple graphs, and also write a
postscript file called `gp_test.ps' to the current directory.  Then
look at the code for the demo which is in the function `demo()' at the
bottom of demo.py.  This should be enough to get you started making
simple plots of your own.

More detailed documentation is contained in the package itself, as
documentation strings and comments.  Don't be shy, just open up
__init__.py with your favorite text editor and take a look.
Alternatively you can check out the documentation online at
<http://monsoon.harvard.edu/~mhagger/Gnuplot/Gnuplot-doc/>, which
contains the same docstrings but in a prettier format.

For a relatively thorough test of Gnuplot.py, type `python test.py'
which goes systematically through most Gnuplot.py features.


Installation
------------

Obviously, you must have the gnuplot program if Gnuplot.py is to be of
any use to you.  Gnuplot can be obtained via
<http://www.cs.dartmouth.edu/gnuplot_info.html>.

You can try out the demonstration before installing the package.  Just
untar or unzip the package, change to the directory that was created,
and type `python demo.py'.

Gnuplot.py is structured as a python package.  That means that it must
be installed as a subdirectory called `Gnuplot' within a directory
that is in your python path.  Usually this means you should install it
within your site-packages directory, which may be in
/usr/local/lib/python1.5.  The easiest thing is to change to that
directory and untar or unzip the distribution there.  This will create
a directory called `Gnuplot-<version>'.  Then either create a symbolic
link to that directory called `Gnuplot' or change the name of that
directory to `Gnuplot'.

The Gnuplot.py package is pure Python.  The main file is __init__.py.
Aside from that are the platform-dependent files gp.py (Unix),
gp_mac.py (Macintosh), and gp_win32.py (Windows).  Near the top of
each of these files are some configuration options that you can
change.  (Obviously, you should change the version appropriate to your
platform.)  See the extensive comments in gp.py for a description of
the meaning of each configuration variable.  Sensible values are
already chosen, so it is quite possible that you won't have to change
anything.

You can import the main part of the package into your python programs
using `import Gnuplot'.

The function-based interface (i.e., the plot() command) inherited from
Konrad Hinsen's original Gnuplot.py has been separated into a separate
file, `plot.py'.  You can import it using `import Gnuplot.oldplot' or
`from Gnuplot.oldplot import plot'.  However, it is recommended that
you try out the object-oriented interface since it is far more
flexible and the old interface will no longer be developed.


Installation on Windows
-----------------------

I don't run Windows, but thanks to the help of users there is now a
way to use Gnuplot.py on that platform.  Any feedback or additional
suggestions having to do with Windows would be especially appreciated.

First make sure you have the quasi-standard Win32 extensions
installed.  This can be obtained from the main Windows download page:

    http://www.python.org/download/download_windows.html

Because the main MS-Windows gnuplot executable (wgnuplot.exe) doesn't
accept commands on standard input, Gnuplot.py cannot communicate with
it directly.  However, there is a simple little program called
`pgnuplot.exe' that accepts commands on stdin and passes them to
wgnuplot.  So to run Gnuplot.py on Windows, you need to make sure that
pgnuplot.exe is installed.  It comes with the latest version of
gnuplot (3.7.1).  Or (if you don't want to install the latest version
of gnuplot) you can get pgnuplot.exe by downloading
`testing/windows-stdin.zip' from one of the gnuplot archives (e.g.,
<ftp://ftp.gnuplot.vt.edu/pub/gnuplot/testing/windows-stdin.zip>).

Assuming pgnuplot.exe is installed, install Gnuplot.py as described in
the previous section.


Installation on the Macintosh
-----------------------------

Thanks to more user help, Gnuplot.py should now work on the Macintosh
too.  Since pipes don't exist on the Mac, communication with gnuplot
is via a python module called gnuplot_Suites.py (included) which uses
AppleEvents.  Note that you will have to convert the python files to
Mac text files (different end-of-line character).  Currently it is not
possible to print directly to a printer; however, it should be
possible to print to a postscript file and print that file manually.
Also, inline data does not seem to be supported.  Let me know if you
find other problems.


Feedback
--------

I would love to have feedback from people letting me know whether they
find Gnuplot.py useful.  And certainly let me know about any problems,
suggestions, or enhancements.  My address is at the bottom of this
file.

Gnuplot.py has been tested with gnuplot version 3.7, and I believe it
should work with version 3.5 (though some features, like enhanced
postscript mode and binary splot mode, will not work).  Let me know if
you have trouble.

Gnuplot.py was developed under Linux and Digital Unix; it should work
without much problem on other unix computers.  If you need to modify
it for your system tell me what was necessary and I'll include your
changes in a future release.

Gnuplot.py should now work under Windows and Macintosh (see above).
Feedback for these platforms is especially appreciated since I can't
test them myself.


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

Tony Ingraldi <a.m.ingraldi@larc.nasa.gov> got Gnuplot.py to work on
the Macintosh.


Michael Haggerty
<mhagger@blizzard.harvard.edu>
