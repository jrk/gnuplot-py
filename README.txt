Gnuplot.py -- A pipe-based interface to the gnuplot plotting program.

The Gnuplot.py home page is

    http://gnuplot-py.sourceforge.net

There you can get the latest version, view the documentation, or
report bugs.


Documentation
-------------

The best way to get started is to install it then run the demo by
typing `python demo.py'.  This should pop up a few gnuplot windows,
one after another, containing simple graphs, and also write a
postscript file called `gp_test.ps' to the current directory.  Then
look at the code for the demo which is in the function `demo()' at the
bottom of demo.py.  This should be enough to get you started making
simple plots of your own.

Documentation for Gnuplot.py is in the doc/ subdirectory (which is
generated automatically from the docstrings using happydoc).  And
don't be shy, just open up the Python files with your favorite text
editor and take a look.

For a relatively thorough test of Gnuplot.py, type `python test.py'
which goes systematically through most Gnuplot.py features.


Installation
------------

Obviously, you must have the gnuplot program if Gnuplot.py is to be of
any use to you.  Gnuplot can be obtained via
<http://www.cs.dartmouth.edu/gnuplot_info.html>.  You also need
Python's Numerical extension, which is available from
<http://numpy.sourceforge.net>.

Gnuplot.py uses Python distutils
<http://www.python.org/doc/current/inst/inst.html> and can be
installed by untarring the package, changing into the top-level
directory, and typing "python setup.py install".  The Gnuplot.py
package is pure Python--no compilation is necessary.

Gnuplot.py is structured as a python package.  That means that it
installs itself as a subdirectory called `Gnuplot' under a directory
of your python path (usually site-packages).  If you don't want to use
distutils you can just move the main Gnuplot.py directory there and
rename it to "Gnuplot".

There are some configuration options that can be set near the top of
the platform-dependent files gp-unix.py (Unix), gp_mac.py (Macintosh),
and gp_win32.py (Windows).  (Obviously, you should change the file
corresponding to your platform.)  See the extensive comments in
gp_unix.py for a description of the meaning of each configuration
variable.  Sensible values are already chosen, so it is quite possible
that you don't have to change anything.

Import the main part of the package into your python programs using
`import Gnuplot'.  Some other features can be found in the modules
Gnuplot.funcutils and Gnuplot.PlotItems.

For backwards compatibility, an old function-based interface to
Gnuplot.py (derived from Konrad Hinsen's original Gnuplot.py) is
available in a separate file, oldplot.py.  However, this old interface
is deprecated and will no longer be developed.


Installation on Windows
-----------------------

I don't run Windows, but thanks to the help of users there is now a
way to use Gnuplot.py on that platform.  Any feedback or additional
suggestions having to do with Windows would be especially appreciated.

If you are using a version of Python prior to 2.0, you must install
the quasi-standard Win32 extensions.  This can be obtained from the
main Windows download page:

    http://www.python.org/download/download_windows.html

Because the main MS-Windows gnuplot executable (wgnuplot.exe) doesn't
accept commands on standard input, Gnuplot.py cannot communicate with
it directly.  However, there is a simple little program called
`pgnuplot.exe' that accepts commands on stdin and passes them to
wgnuplot.  So to run Gnuplot.py on Windows, you need to make sure that
pgnuplot.exe is installed.  It comes with gnuplot since at least
version 3.7.1.  Alternatively you can get pgnuplot.exe alone by
downloading `testing/windows-stdin.zip' from one of the gnuplot
archives (e.g.,
<ftp://ftp.gnuplot.vt.edu/pub/gnuplot/testing/windows-stdin.zip>).

Continue installing Gnuplot.py by following the instructions in the
previous section.


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
find other problems or have patches to fix Mac limitations.


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

Gnuplot.py should also work under Windows and Macintosh (see above).
Feedback for these platforms is especially appreciated since I can't
test them myself.


License
-------

See the file LICENSE for license info.  In brief, Gnuplot is GPL.


Credits
-------

See CREDITS.txt for a list of people who have contributed code and/or
ideas to Gnuplot.py.  Thanks especially to Konrad Hinsen
<hinsen@ibs.ibs.fr>, who wrote the first, procedural interface version
of Gnuplot.py.


--
Michael Haggerty
<mhagger@alum.mit.edu>
