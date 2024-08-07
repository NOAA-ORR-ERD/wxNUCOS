#!/usr/bin/env pythonw

"""
Simple about Dialog class -- I like it better than the one that wxPython comes with
"""

import wx
# fixme -- figure out where HyperLinkCtrl is now
from wx.lib.agw.hyperlink import HyperLinkCtrl


class AboutDialog(wx.Dialog):
    """

    """
    def __init__(self,
                 parent,
                 icon1=None,
                 icon2=None,
                 short_name=None,
                 long_name=None,
                 version=None,
                 description=None,
                 urls=None,
                 licence=None,
                 developers=[]):
        wx.Dialog.__init__(self, parent)

        self.icon1 = icon1
        self.icon2 = icon2
        self.short_name = short_name
        self.long_name = long_name
        self.version = version
        self.description = description
        self.urls = urls
        self.licence = licence
        self.developers = developers

        self.Build()

    def Build(self):

        # Build the header
        Header = wx.BoxSizer(wx.HORIZONTAL)
        Header.Add((64, 1), 1)
        if self.icon1:
            Header.Add(wx.StaticBitmap(self, bitmap=self.icon1), 0)
        else:
            Header.Add((64, 64))
        Header.Add((1, 1), 1)
        if self.short_name:
            Label = wx.StaticText(self, label=self.short_name)
            of = Label.GetFont()
            Font = wx.Font(int(of.GetPointSize() * 2),
                           of.GetFamily(),
                           wx.NORMAL,
                           wx.FONTWEIGHT_BOLD)
            Label.SetFont(Font)
            Header.Add(Label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        else:
            Header.Add((1, 1), 1)
        Header.Add((1, 1), 1)
        if self.icon2:
            Header.Add(wx.StaticBitmap(self, bitmap=self.icon2), 0)
        else:
            Header.Add((64, 64))
        Header.Add((64, 1), 1)
        width = Header.MinSize[0]

        # Now the rest;
        MainSizer = wx.BoxSizer(wx.VERTICAL)

        MainSizer.Add(Header, 0, wx.EXPAND | wx.ALL, 5)

        if self.long_name:
            Label = wx.StaticText(self, label=self.long_name)
            of = Label.GetFont()
            Font = wx.Font(int(of.GetPointSize() * 1.5), of.GetFamily(), wx.NORMAL, wx.NORMAL)
            Label.SetFont(Font)
            MainSizer.Add(Label, 0, wx.TOP | wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER, 5)
            width = max(width, Label.Size[0])

        if self.version:
            Label = wx.StaticText(self, label="version: " + self.version)
            MainSizer.Add(Label, 0, wx.BOTTOM | wx.ALIGN_CENTER, 5)

        if self.description:
            Label = wx.StaticText(self, label=self.description)

            Label.Wrap(max(250, int(0.9 * width)))
            MainSizer.Add(Label, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        if self.licence:
            Label = wx.StaticText(self, label="License:")
            of = Label.GetFont()
            Font = wx.Font(of.GetPointSize(), of.GetFamily(), wx.NORMAL, wx.BOLD)
            Label.SetFont(Font)
            MainSizer.Add(Label, 0, wx.ALL | wx.ALIGN_LEFT, 5)
            Label = wx.StaticText(self, label=self.licence)
            Label.Wrap(max(250, int(0.9 * width)))
            MainSizer.Add(Label, 0, wx.ALL | wx.ALIGN_CENTER, 2)

        if self.developers:
            Label = wx.StaticText(self, label="Developed by:")
            of = Label.GetFont()
            Font = wx.Font(of.GetPointSize(), of.GetFamily(), wx.NORMAL, wx.BOLD)
            Label.SetFont(Font)
            MainSizer.Add(Label, 0, wx.ALL | wx.ALIGN_LEFT, 5)

            for developer in self.developers:
                Label = wx.StaticText(self, label="          " + developer)
                MainSizer.Add(Label, 0, wx.ALL | wx.ALIGN_LEFT, 0)

        if self.urls:
            Label = wx.StaticText(self, label="For more information:")
            of = Label.GetFont()
            Font = wx.Font(of.GetPointSize(), of.GetFamily(), wx.NORMAL, wx.BOLD)
            Label.SetFont(Font)
            MainSizer.Add(Label, 0, wx.ALL | wx.ALIGN_LEFT, 5)
            for url in self.urls:
                Link = HyperLinkCtrl(self,
                                     label=url,
                                     URL=url)
                MainSizer.Add(Link, 0, wx.ALL | wx.ALIGN_CENTER, 2)

        MainSizer.Add((1, 5), 1)
        MainSizer.Add(wx.Button(self, id=wx.ID_OK, label="Dismiss"),
                      0, wx.ALL | wx.ALIGN_RIGHT, 5)
        SpaceSizer = wx.BoxSizer(wx.VERTICAL)
        SpaceSizer.Add(MainSizer, 0, wx.ALL, 10)
        self.SetSizerAndFit(SpaceSizer)


if __name__ == "__main__":
    import icons

    a = wx.App(False)
    d = AboutDialog(None,
                    icon1=icons.NUCOS64.GetBitmap(),
                    icon2=icons.NOAA64.GetBitmap(),
                    short_name='NUCOS',
                    long_name='NOAA Unit Converter for Oil Spills',
                    version="1.3.4",
                    description=("A description of the program. "
                                 "This could be a pretty long bit of text. "
                                 "How shall I know how long to make it? "
                                 "How will it fit in?"),
                    urls=["http://www.response.restoration.noaa.gov",
                          "mailto:nucos@noaa.gov"],
                    licence=("NUCOS was developed by an agency of the "
                             "US government and is in the public domain"),
                    developers=["Chris Barker", "Christopher Barker, PhD"])

    d.ShowModal()
