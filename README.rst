#######
wxNUCOS
#######

wxPython based graphical user interface for the NOAA Unit Converter for Oil Spills.

Installation
============

wxNUCOS depends on the wxPython GUI framework, and the pynucos unit conversion code.

It should be all installable via conda (and also pip)

conda_requirements.txt

pip install ./

PyInstaller is used to build the executable(s)


Running:
========

The startup script is NUCOS.py::

pythonw NUCOS.py


Building the Executable
=======================

The executable is built with PyInstaller. It should have been installed by the conda_requirements.

1) Set up the conda environment

2) Install the wxNUCOS python package:
   - `pip install .` (you can do editable as well, if you like)

3) test it:
   - `python NUCOS.py` should run it.

   Be sure to see if the help works -- it should open the help in your system browser.

If there is a spec file ready to go:

4) Build the exe:
  - `pyinstaller NUCOS.mac.spec`
  or
  - `pyinstaller NUCOS.win.spec`

If there is not a spec file -- or it needs updating:

5) set up the spec file:

 - `pyinstaller NUCOS.py` will run PyInstaller, and make a spec file for you.

 You can either hand-edit the spec file, if needed, or pass parameters to Py2exe, and it will save them in the spec file, which you can then save.

6) Build the installer:

Mac:

`./build_disk_image.sh`

NOTE: the executable really should be signed -- get someone to do that for you, if you don't know how.


Windows: Run Inno Setup:

  -  If there's a up-to-date script -- use it
  -  If there isn't -- run Inno Setup to do it for you :-)


