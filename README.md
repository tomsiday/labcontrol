# labcontrol

Controls the lab equipment in the UCL Ultrafast Laser Lab (room 910).

### Files in this repository
-  `Main.py` - this is the main file for running this application. The application can be started using this file and python 3.6. (I think)
    requires a number of python libraries, available through 'pip' (https://pypi.org/project/pip/)
     
     1. matplotlib
     
     2. pyvisa 
     
     3. numpy
     
     4. time
     
     5. pyserial
     
     6. sys
     
     7. PyQt4
     
     8. datetime
 
   It also requires a python library from *Zurich Instruments* for the *MFLI lock-in amplifier*. Available https://www.zhinst.com/downloads. download precompiled for the correct python version and system. This application is based on 17.06 at the moment
 
- `canvas.py` - a short file used to include matplotlib plots within the PyQt4 GUI framework
 
- `gui.ui` - this is an XML file created by the the PyQt4 GUI designer. These can be converted to `.py` for use with the command
`C:\Python34\Lib\site-packages\PyQt4\pyuic4.bat -x filename.ui -o filename.py` or something to that effect.
 
- `Gui.py` - the converted `.ui` file
 
- `README.md` - this file
 
-  `__pycache__` - for bytecode compiled files (automatic, standard)
 
- *Date files* - raw data. Will be stored here as long as this repo is private. To be deleted if repo made public.
      
