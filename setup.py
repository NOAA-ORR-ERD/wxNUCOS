#!/usr/bin/env python

"""
Script to build an app bundle from the converter wxPython application
on OS-X, or a windows executable on windows.

% python setup.py py2app

or

% python setup.py py2exe

"""

import sys
import os
from setuptools import setup

# from my_copy_tree import copy_tree


def get_version(pkg_name):
    """
    Reads the version string from the package __init__ and returns it
    """
    with open(os.path.join(pkg_name, "__init__.py")) as init_file:
        for line in init_file:
            parts = line.strip().partition("=")
            if parts[0].strip() == "__version__":
                return parts[2].strip().strip("'").strip('"')
    return None


# Common stuff:
MainScript = 'nucos/NUCOS.py'
description = "Unit conversion GUI utility: designed for Oil Spills",
author = "Christopher H. Barker",
author_email = "Chris.Barker@noaa.gov",


setup(name="wxnucos",
      description=('GUI app for unit conversion'
                   ' -- units useful for oil and chemical spill response'),
      author='Christopher H. Barker',
      author_email='Chris.Barker@noaa.gov',
      url='https://github.com/NOAA-ORR-ERD/wxnucos',
      version=get_version("wxnucos"),
      packages=['wxnucos', ],
      )


# Executable building stuff -- needs updating!
# if sys.platform == 'darwin':
#     DATA_FILES = ['nucos/Help']

#     Plist = {}
#     OPTIONS = {'argv_emulation': False, # this puts the names of dropped files into sys.argv when starting the app.
#                'iconfile': 'Icons/NUCOS.icns',
#                'plist': Plist,
#                }

#     setup(
#         name="wxnucos",
#         app=[MainScript, ],
#         packages=['wxnucos'],
#         data_files=DATA_FILES,
#         version=get_version("wxnucos"),
#         description=description,
#         author=author,
#         author_email=author_email,
#         options={'py2app': OPTIONS},
#         # setup_requires=['py2app'],
#     )

# elif sys.platform == 'win32':
#     print("Building EXE")
#     from distutils.core import setup
#     import py2exe
#     manifest="""
# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <assembly xmlns="urn:schemas-microsoft-com:asm.v1"
# manifestVersion="1.0">
# <assemblyIdentity
#     version="0.64.1.0"
#     processorArchitecture="x86"
#     name="Controls"
#     type="win32"
# />
# <description>ERD Unit Converter</description>
# <dependency>
#     <dependentAssembly>
#         <assemblyIdentity
#             type="win32"
#             name="Microsoft.Windows.Common-Controls"
#             version="6.0.0.0"
#             processorArchitecture="X86"
#             publicKeyToken="6595b64144ccf1df"
#             language="*"
#         />
#     </dependentAssembly>
# </dependency>
# </assembly>
# """
#     EXCLUDES = []
#     DATA_FILES = [('.',['C:\\windows\\system32\\msvcp71.dll'])] # required by wxPython -- on most systems, but not all!
#     DLL_EXCLUDES = ['wxmsw28uh_stc_vc.dll',
#                     'wxmsw28uh_aui_vc.dll',
#                     ]

#     OPTIONS = {"py2exe": {"compressed": 1,
#                           "optimize": 2,
#                           "excludes": EXCLUDES,
#                           "dll_excludes": DLL_EXCLUDES,
#                           "bundle_files": 1,
#                           }}

#     setup(
#         windows=[
#             {"script": MainScript,  # Main Python script
#              "icon_resources": [(1, "Icons/NUCOS.ico")],  # Icon to embed into the PE file.
#              "other_resources": [(24, 1, manifest)]  # manifest (gives the WinXP look)
#              }
#                  ],
#         packages=['wxnucos'],
#         zipfile=None,
#         options=OPTIONS,
#         data_files=DATA_FILES,
#         #version=__version__,
#         description=description,
#         author=author,
#         author_email=author_email,
#         )
#     print("copying help folder:")
#     # for dir in ['Help']: # note: I could add this to DATA_FILES...
#     #     copy_tree(dir, os.path.join('dist',dir), update=1, verbose=False, exclude_patterns="*.svn*")

# else:
#     raise Exception("I don't know how to build for platform:%s"%sys.platfrom)

