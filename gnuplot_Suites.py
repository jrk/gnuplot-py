# $Id$

# This file is provided as part of the Gnuplot.py package for the
# convenience of Mac users.  It was originally part of
# MacGnuplot.2.0b4.  Thanks to Anthony M. Ingraldi and Noboru Yamamoto
# for helping with this.

# file contains
#
#  class gnuplot_Suite
#  class odds_and_ends
#  class Standard_Suite
#  class Miscellaneous_Events
#
"""Suite gnuplot Suite: Events supplied by gnuplot
Level 1, version 1

Generated from Power HD:Applications:Analysis/Plotting:gnuplot.2.0a34:gnuplot (PPC)
AETE/AEUT resource version 1/0, language 0, script 0
"""

__cvs_version__ = '$Revision$'

import aetools
import MacOS

_code = 'GPSE'

_Enum_DIAG = {
   'label' : 'labl', # label dialog
   'offsets' : 'oset',  # offsets dialog
   'textformat' : 'text',  # text format dialog
   'gxtextformat' : 'gxtx',   # gx text format dialog
   'linestyles' : 'line',  # line styles dialog
   'preferences' : 'pref', # preferences dialog
}

_Enum_lyty = {
   'lines' : 'typ1', # lines
   'points' : 'typ2',   # points
   'impulses' : 'typ3', # impulses
   'linespoints' : 'typ4', # lines with points
   'dots' : 'typ5',  # dots
   'steps' : 'typ6', # steps
   'fsteps' : 'typ7',   # use two line segments
   'errorbars' : 'typ8',   # error bars
   'xerrorbars' : 'typ9',  # horizontal error bars
   'yerrorbars' : 'ty10',  # vertical error bars
   'xyerrorbars' : 'ty11', # horizontal and vertical error bars
   'boxes' : 'ty12', # boxes
   'boxerrorbars' : 'ty13',   # boxes and error bars
   'boxxyerrorbars' : 'ty14', # boxes and xy error bars
   'vector' : 'ty19',   # vector
}

class gnuplot_Suite:

   _argmap_exec = {
      'with_client' : 'CLIE',
      'with_creator' : 'CREA',
      'with_type' : 'TYPE',
   }

   def gnuexec(self, _object=None, _attributes={}, **_arguments):
      """gnuexec: execute a gnuplot command
      Required argument: a gnuplot command
      Keyword argument with_client: client application
      Keyword argument with_creator: creator code for any output
      Keyword argument with_type: file type for any output
      Keyword argument _attributes: AppleEvent attribute dictionary
      Returns: what gnuplot said
      """
      _code = 'GPSE'
      _subcode = 'exec'

      aetools.keysubst(_arguments, self._argmap_exec)
      _arguments['----'] = _object

      aetools.enumsubst(_arguments, 'with_client', self._argmap_exec)
      aetools.enumsubst(_arguments, 'with_creator', self._argmap_exec)
      aetools.enumsubst(_arguments, 'with_type', self._argmap_exec)

      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']

   def halt(self, _no_object=None, _attributes={}, **_arguments):
      """halt: halt any processing
      Keyword argument _attributes: AppleEvent attribute dictionary
      """
      _code = 'GPSE'
      _subcode = 'HALT'

      if _arguments: raise TypeError, 'No optional args expected'
      if _no_object != None: raise TypeError, 'No direct arg expected'


      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']

   def open_dialog(self, _object=None, _attributes={}, **_arguments):
      """open dialog: open a gnuplot dialog
      Required argument: the dialog to open
      Keyword argument _attributes: AppleEvent attribute dictionary
      """
      _code = 'GPLT'
      _subcode = 'DIAG'

      if _arguments: raise TypeError, 'No optional args expected'
      _arguments['----'] = _object


      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']

   _argmap_plot = {
      'with' : 'line',
   }

   def plot(self, _object=None, _attributes={}, **_arguments):
      """plot: do a 2d plot of files or data
      Required argument: the data to plot
      Keyword argument with: line style
      Keyword argument _attributes: AppleEvent attribute dictionary
      Returns: what gnuplot said
      """
      _code = 'GPLT'
      _subcode = 'plot'

      aetools.keysubst(_arguments, self._argmap_plot)
      _arguments['----'] = _object

      aetools.enumsubst(_arguments, 'line', _Enum_lyty)

      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']

   _argmap_splot = {
      'with' : 'line',
   }

   def splot(self, _object=None, _attributes={}, **_arguments):
      """splot: do a 3d plot files or data
      Required argument: the data to plot
      Keyword argument with: line style
      Keyword argument _attributes: AppleEvent attribute dictionary
      Returns: what gnuplot said
      """
      _code = 'GPLT'
      _subcode = 'splt'

      aetools.keysubst(_arguments, self._argmap_splot)
      _arguments['----'] = _object

      aetools.enumsubst(_arguments, 'line', _Enum_lyty)

      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']


#    Class 'graph' ('cGRF') -- 'graph - subclass of window'
#        property 'picture' ('PICT') 'PICT' -- 'the graph picture' [enum]
#        property 'graph number' ('NUMB') 'shor' -- 'the number of the graph' [enum]
#        property 'title' ('TITL') 'TEXT' -- 'the title of the graph' [enum]
"""Suite odds and ends: Things that should be in some standard suite, but aren't
Level 1, version 1

Generated from Power HD:Applications:Analysis/Plotting:gnuplot.2.0a34:gnuplot (PPC)
AETE/AEUT resource version 1/0, language 0, script 0
"""

_code = 'Odds'

class odds_and_ends:

   def select(self, _object=None, _attributes={}, **_arguments):
      """select: select the specified object
      Required argument: the object to select
      Keyword argument _attributes: AppleEvent attribute dictionary
      """
      _code = 'misc'
      _subcode = 'slct'

      if _arguments: raise TypeError, 'No optional args expected'
      _arguments['----'] = _object


      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']

"""Suite Standard Suite: Common terms for most applications
Level 1, version 1

Generated from Power HD:Applications:Analysis/Plotting:gnuplot.2.0a34:gnuplot (PPC)
AETE/AEUT resource version 1/0, language 0, script 0
"""

_code = 'CoRe'

class Standard_Suite:

   _argmap_save = {
      '_in' : 'kfil',
   }

   def save(self, _object, _attributes={}, **_arguments):
      """save: save an object
      Required argument: the object to save
      Keyword argument _in: the file in which to save the object
      Keyword argument _attributes: AppleEvent attribute dictionary
      """
      _code = 'core'
      _subcode = 'save'

      aetools.keysubst(_arguments, self._argmap_save)
      _arguments['----'] = _object

      aetools.enumsubst(_arguments, 'kfil', _Enum_fss )

      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']

   def get(self, _object, _attributes={}, **_arguments):
      """get: get the data for an object
      Required argument: the object whose data is to be returned
      Keyword argument _attributes: AppleEvent attribute dictionary
      Returns: the data from the object
      """
      _code = 'core'
      _subcode = 'getd'

      if _arguments: raise TypeError, 'No optional args expected'
      _arguments['----'] = _object


      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']

   _argmap_set = {
      'to' : 'data',
   }

   def set(self, _object, _attributes={}, **_arguments):
      """set: set an objects data
      Required argument: the object whose data is to be changed
      Keyword argument to: the new value
      Keyword argument _attributes: AppleEvent attribute dictionary
      """
      _code = 'core'
      _subcode = 'setd'

      aetools.keysubst(_arguments, self._argmap_set)
      _arguments['----'] = _object


      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']


#    Class 'application' ('capp') -- 'application properties'
#        property 'clipboard' ('clip') '****' -- "gnuplot's clipboard" [mutable]
#        property 'terminals' ('TLST') 'TEXT' -- 'list of the currently available terminals' [list]
#        property 'graph creator' ('QDCR') 'fltp' -- 'creator code for QuickDraw graphs' [mutable]
#        property 'file creator' ('CREA') 'fltp' -- 'creator code for text plots' [mutable]
#        property 'file type' ('TYPE') 'fltp' -- 'file type for text plots' [mutable]
#        property 'working folder' ('wfdr') 'alis' -- 'the path to the default folder for the command\320line plot and load commands' [mutable]
#        property 'current terminal' ('TERM') 'TEXT' -- 'the name of the current terminal' []
#        property 'text font' ('FONT') 'TEXT' -- 'the font for graphs' [mutable]
#        property 'text size' ('SIZE') 'shor' -- 'the text size for graphs' [mutable]
#        property 'graph size' ('GSIZ') 'QDpt' -- 'dimensions of the next graph' [mutable]
#        element 'cwin' as ['indx', 'name']

#    Class 'window' ('cwin') -- 'a window'
#        property 'bounds' ('pbnd') 'qdrt' -- 'the boundary rectangle for the window' [enum]
#        property 'closeable' ('hclb') 'bool' -- 'does the window have a close box?' [enum]
#        property 'index' ('pidx') 'shor' -- 'the number of the window' [enum]
#        property 'floating' ('isfl') 'bool' -- 'does the window float?' [enum]
#        property 'modal' ('pmod') 'bool' -- 'is the window modal?' [enum]
#        property 'resizable' ('prsz') 'bool' -- 'is the window resizable?' [enum]
#        property 'zoomable' ('iszm') 'bool' -- 'is the window zoomable?' [enum]
#        property 'zoomed' ('pzum') 'bool' -- 'is the window zoomed?' [mutable enum]
#        property 'name' ('pnam') 'TEXT' -- 'the title of the window' [enum]
#        property 'visible' ('pvis') 'bool' -- 'is the window visible?' [mutable enum]
#        property 'position' ('ppos') 'QDpt' -- 'upper left coordinates of window' [mutable enum]

"""Suite Miscelaneous Events: Some other events
Level 1, version 1

Generated from Power HD:Applications:Analysis/Plotting:gnuplot.2.0a34:gnuplot (PPC)
AETE/AEUT resource version 1/0, language 0, script 0
"""

_code = 'misc'

class Miscellaneous_Events:

   _argmap_DoScript = {
      'with_client' : 'CLIE',
      'with_creator' : 'CREA',
      'with_type' : 'TYPE',
   }

   def DoScript(self, _object=None, _attributes={}, **_arguments):
      """DoScript: execute a gnuplot script
      Required argument: a gnuplot script to execute
      Keyword argument with_client: client application
      Keyword argument with_creator: creator code for any output
      Keyword argument with_type: file type for any output
      Keyword argument _attributes: AppleEvent attribute dictionary
      Returns: what gnuplot said
      """
      _code = 'misc'
      _subcode = 'dosc'

      aetools.keysubst(_arguments, self._argmap_DoScript)
      _arguments['----'] = _object

      aetools.enumsubst(_arguments, 'with_client', self._argmap_DoScript)
      aetools.enumsubst(_arguments, 'with_creator', self._argmap_DoScript)
      aetools.enumsubst(_arguments, 'with_type', self._argmap_DoScript)

      _reply, _arguments, _attributes = self.send(_code, _subcode,
            _arguments, _attributes)
      if _arguments.has_key('errn'):
         raise aetools.Error, aetools.decodeerror(_arguments)
      # XXXX Optionally decode result
      if _arguments.has_key('----'):
         # XXXX Should do enum remapping here...
         return _arguments['----']

