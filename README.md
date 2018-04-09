# labcontrol

Controls the lab equipment in the UCL ultrafast laser lab (room 910).

Files in this repository
  Main.py - this is the main file for running this application. The application can be started using this file and python 3.6. (I think)
    requires a number of python libaries, availible through pip
     
     1. matplotlib
     
     2. pyvisa 
     
     3. numpy
     
     4. time
     
     5. pyserial
     
     6. sys
     
     7. PyQt4
     
     8. datetime
    
    it also requires a python libary from zurich instruments for the MFLI lockin amplifier. availible https://www.zhinst.com/downloads. download precompiled for the correct python version and system. This appplication is based on 17.06 at the momen
 
 canvas.py - a short file used to inlude matplotlib plots within the PyQt4 gui framework
 
 gui.ui - this is an XML file created by the the PyQt4 gui designer. These can be converted to .py for use with the command " C:\Python34\Lib\site-packages\PyQt4\pyuic4.bat -x filename.ui -o filename.py" or something to that effect.
 
 Gui.py - the converted .ui file
 
 README.md - this file
 
 __pycache__ - for bytecode compiled files (automatic, standard)
 
 Date files - raw data. Will be stored here as long as this repo is private. To be deleted if repo made public.
      
