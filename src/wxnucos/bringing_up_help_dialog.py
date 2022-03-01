#!/usr/bin/env python

"""
Dialog to let folks know that the help will come up in their browser.
"""

import wx
from .import icons


class BringingUpHelpDialog(wx.Dialog):
    """

    """
    def __init__(self, *args, **kwargs):

        kwargs['style'] = wx.DEFAULT_DIALOG_STYLE  # |wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwargs)

        Header = wx.BoxSizer(wx.HORIZONTAL)
        Header.Add(wx.StaticBitmap(self, bitmap=icons.NUCOS64.GetBitmap()), 0)
        Header.Add((1, 1), 1)

        Label = wx.StaticText(self, label="NUCOS")
        of = Label.GetFont()
        Font = wx.Font(int(of.GetPointSize() * 2.0), of.GetFamily(), wx.NORMAL, wx.BOLD)
        Label.SetFont(Font)
        Header.Add(Label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Header.Add((1, 1), 1)
        Header.Add(wx.StaticBitmap(self, bitmap=icons.NOAA64.GetBitmap()), 0)

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(Header, 0, wx.ALL | wx.EXPAND, 5)

        Label = wx.StaticText(self,
                              label=("NUCOS Help should come up in your system "
                                     "browser momentarily"),
                              style=wx.ALIGN_CENTRE)
        of = Label.GetFont()
        Font = wx.Font(int(of.GetPointSize() * 1.5), of.GetFamily(), wx.NORMAL, wx.NORMAL)
        Label.SetFont(Font)
        MainSizer.Add(Label, 0, wx.TOP | wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER, 5)
        Label.Wrap(300)

        MainSizer.Add((1, 5), 1)
        MainSizer.Add(wx.Button(self, id=wx.ID_OK, label="Dismiss"),
                      0, wx.ALL | wx.ALIGN_RIGHT, 5)

        SpaceSizer = wx.BoxSizer(wx.VERTICAL)
        SpaceSizer.Add(MainSizer, 0, wx.ALL, 10)

        self.SetSizerAndFit(SpaceSizer)


if __name__ == "__main__":

    a = wx.App(False)
    d = BringingUpHelpDialog(None)

    d.Show()
    a.MainLoop()
