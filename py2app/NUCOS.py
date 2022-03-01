#!/usr/bin/env pythonw

"""
Script used to kick off wxNUCOS for py2app and py2exe

e.g. not installed by setuptools
"""

import wxnucos.gui

print(wxnucos.__file__)


if __name__ == "__main__":
    wxnucos.gui.main()

