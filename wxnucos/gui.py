#!/usr/bin/env python

import sys

import os
import webbrowser
from pathlib import Path
import wx

import unit_conversion as UC

# the GUI imports
from . import __version__
from . import oil_quantity
from . import icons
from .about_dialog import AboutDialog
from .bringing_up_help_dialog import BringingUpHelpDialog
from .utilities import SignificantFigures


class ConverterPanel(wx.Panel):
    def __init__(self, parent, id, UnitType):

        wx.Panel.__init__(self, parent, id, wx.DefaultPosition, style=wx.SUNKEN_BORDER)

        self.UnitType = UnitType
        Units = UC.GetUnitNames(UnitType)
        Units.sort(key=str.lower)

        self.FromUnits = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Units)
        self.FromUnits.SetSelection(0)

        self.ToUnits = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Units)
        self.ToUnits.SetSelection(0)

        self.InputBox = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, (100, -1))
        self.OutBox = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, (100, -1), style = wx.TE_READONLY)

        Grid = wx.FlexGridSizer(6, 2, 5, 20)

        Grid.Add(wx.StaticText(self, -1, "Convert From:", wx.DefaultPosition, wx.DefaultSize),0,wx.ALIGN_LEFT)
        Grid.Add((20, 1), 1) # adding a spacer

        Grid.Add(self.InputBox, 0, wx.ALIGN_LEFT)
        Grid.Add(self.FromUnits, 0, wx.ALIGN_RIGHT)

        Grid.Add((20, 20), 1)  # adding a spacer
        Grid.Add((20, 20), 1)  # adding a spacer

        Grid.Add(wx.StaticText(self, -1, "Convert To:", wx.DefaultPosition, wx.DefaultSize),0,wx.ALIGN_LEFT)
        Grid.Add((20, 1), 1)  # adding a spacer

        Grid.Add(self.OutBox, 0, wx.ALIGN_LEFT)
        Grid.Add(self.ToUnits, 0, wx.ALIGN_RIGHT)

        Grid.Layout()
        OuterBox = wx.BoxSizer(wx.VERTICAL)
        OuterBox.Add((20, 20), 0)
        Label = wx.StaticText(self, -1, UnitType, wx.DefaultPosition, wx.DefaultSize)
        of = Label.GetFont()
        Font = wx.Font(int(of.GetPointSize() * 2), of.GetFamily(), wx.NORMAL, wx.NORMAL)
        Label.SetFont(Font)

        IconBox = wx.BoxSizer(wx.HORIZONTAL)
        IconBox.Add(wx.StaticBitmap(self,bitmap=icons.NUCOS64.GetBitmap()),
                                    0,
                                    wx.ALIGN_LEFT | wx.LEFT,
                                    30)
        IconBox.Add((1, 1), 1, wx.EXPAND)
        IconBox.Add(Label, 0, wx.ALIGN_CENTER)
        IconBox.Add((1, 1), 1, wx.EXPAND)
        IconBox.Add(wx.StaticBitmap(self, bitmap=icons.NOAA64.GetBitmap()), 0, wx.ALIGN_RIGHT | wx.RIGHT, 30)

        OuterBox.Add(IconBox, 0, wx.EXPAND)
        OuterBox.Add(Grid, 0, wx.ALIGN_CENTER | wx.ALL, 30)
        OuterBox.Layout()

        self.SetAutoLayout(True)
        self.SetSizer(OuterBox)
        self.Fit()

        self.InputBox.Bind(wx.EVT_TEXT, self.Recalculate)
        self.FromUnits.Bind(wx.EVT_CHOICE, self.Recalculate)
        self.ToUnits.Bind(wx.EVT_CHOICE, self.Recalculate)

    def Recalculate(self,event):
        try:
            from_string = self.InputBox.GetValue()
            from_val = float(from_string)

            from_unit = self.FromUnits.GetStringSelection()
            to_unit = self.ToUnits.GetStringSelection()

            to_val = UC.Convert(self.UnitType, from_unit, to_unit, from_val)

            format_string = "%%.%ig"%SignificantFigures(from_string)
            self.OutBox.SetValue(format_string%(to_val,))
        except ValueError:
            self.OutBox.SetValue("")

class LatLongPanel(wx.Panel):
    def __init__(self, *args, **kwargs):

        kwargs['style'] = wx.SUNKEN_BORDER

        wx.Panel.__init__(self, *args, **kwargs)


        self.TopPanel = wx.Panel(self, style = wx.TAB_TRAVERSAL | wx.NO_BORDER)

        self.DegreesBox = wx.TextCtrl(self.TopPanel, size=(80, -1))
        self.MinutesBox = wx.TextCtrl(self.TopPanel, size=(80, -1))
        self.SecondsBox = wx.TextCtrl(self.TopPanel, size=(80, -1))

        self.DecimalDegreesBox = wx.TextCtrl(self, size=(100, -1), style=wx.TE_READONLY)
        self.DegreesMinBox = wx.TextCtrl(self, size=(100, -1), style=wx.TE_READONLY)
        self.DegMinSecBox = wx.TextCtrl(self, size=(100, -1), style=wx.TE_READONLY)

        DMSSizer = wx.GridSizer(2, 4, 1, 5)
        DMSSizer.Add((1, 1),)
        DMSSizer.Add(wx.StaticText(self.TopPanel, label="Degrees:"))
        DMSSizer.Add(wx.StaticText(self.TopPanel, label="Minutes:"))
        DMSSizer.Add(wx.StaticText(self.TopPanel, label="Seconds:"))


        Label = wx.StaticText(self.TopPanel, label="Input:")
        of = Label.GetFont()
        Font = wx.Font(int(of.GetPointSize() * 1.2), of.GetFamily(), style=wx.NORMAL, weight=wx.FONTWEIGHT_BOLD)
        Label.SetFont(Font)

        DMSSizer.Add(Label, 0, wx.RIGHT)
        DMSSizer.Add(self.DegreesBox, 0, wx.RIGHT, 5)
        DMSSizer.Add(self.MinutesBox, 0, wx.RIGHT, 5)
        DMSSizer.Add(self.SecondsBox, 0, )

        self.TopPanel.SetSizerAndFit(DMSSizer)

        OutputSizer = wx.FlexGridSizer(3, 3, 5, 5)
        OutputSizer.AddGrowableCol(2)

        Label = wx.StaticText(self, label="Output:")
        of = Label.GetFont()
        Font = wx.Font(int(of.GetPointSize() * 1.2), of.GetFamily(), style=wx.NORMAL, weight=wx.FONTWEIGHT_BOLD)
        Label.SetFont(Font)

        OutputSizer.Add(Label, 0, wx.RIGHT, 20)
        OutputSizer.Add(wx.StaticText(self, label="Decimal Degrees:"))
        OutputSizer.Add(self.DecimalDegreesBox, 1, wx.EXPAND)

        OutputSizer.Add((1,1))
        OutputSizer.Add(wx.StaticText(self, label="Deg - Min:"))
        OutputSizer.Add(self.DegreesMinBox, 1, wx.EXPAND)

        OutputSizer.Add((1,1))
        OutputSizer.Add(wx.StaticText(self, label="Deg - Min - Sec:"))
        OutputSizer.Add(self.DegMinSecBox, 1, wx.EXPAND)

        VertBox = wx.BoxSizer(wx.VERTICAL)

        VertBox.Add((20, 20), 0)
        Label = wx.StaticText(self, label="Latitude/Longitude")
        of = Label.GetFont()
        Font = wx.Font(int(of.GetPointSize() * 2), of.GetFamily(), wx.NORMAL, wx.NORMAL)
        Label.SetFont(Font)

        IconBox = wx.BoxSizer(wx.HORIZONTAL)
        IconBox.Add(wx.StaticBitmap(self, bitmap=icons.NUCOS64.GetBitmap()), 0, wx.ALIGN_LEFT | wx.RIGHT,20)
        IconBox.Add((1,1), 1, wx.EXPAND)
        IconBox.Add(Label, 0, wx.ALIGN_CENTER)
        IconBox.Add((1,1), 1, wx.EXPAND)
        IconBox.Add(wx.StaticBitmap(self, bitmap=icons.NOAA64.GetBitmap()), 0, wx.ALIGN_RIGHT | wx.LEFT,20)

        VertBox.Add((20, 20), 1)
        VertBox.Add(IconBox, 0, wx.EXPAND)
        VertBox.Add(self.TopPanel, 0, wx.ALL, 10)
        VertBox.Add(OutputSizer, 0, wx.ALL | wx.EXPAND, 10)
        VertBox.Add((20, 20), 1)



        OuterBox = wx.BoxSizer(wx.HORIZONTAL)
        OuterBox.Add((1,1), 1)
        OuterBox.Add(VertBox, 0)
        OuterBox.Add((1,1), 1)

        self.DegreesBox.Bind(wx.EVT_TEXT, self.Recalculate)
        self.MinutesBox.Bind(wx.EVT_TEXT, self.Recalculate)
        self.SecondsBox.Bind(wx.EVT_TEXT, self.Recalculate)

        self.SetSizerAndFit(OuterBox)
        #self.SetSizerAndFit(VertBox)

    LLC = UC.LatLongConverter

    def OnDDFocus(self, event=None):
        if sys.platform == "linux2":
            # this is needed on GTK, not on win32
            self.DegreesBox.SetFocus()
        pass

    def Recalculate(self,event):
        try:
            values = []
            for box in (self.DegreesBox, self.MinutesBox, self.SecondsBox ):
                t = box.GetValue()
                if t.strip() == "":
                    values.append(0.0)
                else:
                    values.append(float(t))

            DecDeg = self.LLC.ToDecDeg(*values)

            self.DecimalDegreesBox.SetValue(self.LLC.ToDecDeg(DecDeg, ustring=True))
            self.DegreesMinBox.SetValue(self.LLC.ToDegMin(DecDeg, True))
            self.DegMinSecBox.SetValue(self.LLC.ToDegMinSec(DecDeg, True))

        except ValueError:
            self.DecimalDegreesBox.SetValue("")
            self.DegreesMinBox.SetValue("")
            self.DegMinSecBox.SetValue("")


class MainPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.MainSizer = MainSizer

        ButtonSizer = wx.BoxSizer(wx.VERTICAL)

        self.Panels = {}
        BiggestSize = (0,0)
        for UnitType in UC.GetUnitTypes():
            # create Panel
            Panel = ConverterPanel(self, -1, UnitType)
            Panel.Show(False)
            size = Panel.GetBestSize()
            BiggestSize = ( max(size[0], BiggestSize[0]), max(size[1], BiggestSize[1]))

            # create Button
            button = wx.Button(self, wx.ID_ANY, UnitType)
            ButtonSizer.Add(button,
                            0,
                            wx.EXPAND | wx.ALL,
                            3)
            self.Panels[button.Id] = Panel

            # set up the events:
            button.Bind(wx.EVT_BUTTON, self.OnButtonPress)
        # Add the LatLonPanel:
        Panel = LatLongPanel(self)
        Panel.Show(False)
        size = Panel.GetBestSize()
        BiggestSize = (max(size[0], BiggestSize[0]), max(size[1], BiggestSize[1]))
        # create Button
        ID = wx.NewId()
        button = wx.Button(self, wx.ID_ANY, "Lat-Long")
        ButtonSizer.Add(button,
                        0,
                        wx.EXPAND | wx.ALL,
                        3)
        self.Panels[ID] = Panel

        # set up the button event:
        button.Bind(wx.EVT_BUTTON, self.OnButtonPress)

        # Add the OilQuantity Panel:
        Panel = oil_quantity.OilQuantityPanel(self)
        Panel.Show(False)
        size = Panel.GetBestSize()
        BiggestSize = (max(size[0], BiggestSize[0]), max(size[1], BiggestSize[1]))

        # create Button
        # ID = wx.NewId()
        button = wx.Button(self, wx.ID_ANY, "Oil Quantity")
        ButtonSizer.Add(button,
                        0,
                        wx.EXPAND | wx.ALL,
                        3)
        self.Panels[ID] = Panel
        # set up the button event:
        button.Bind(wx.EVT_BUTTON, self.OnButtonPress)

        ButtonSizer.Layout()
        MainSizer.Add(ButtonSizer, 0, wx.ALIGN_TOP | wx.ALL, 6)

        # Reset the sizes of all the Panels to match the biggest one
        for Panel in self.Panels.values():
            Panel.SetSize(BiggestSize)
            Panel.SetSizeHints(BiggestSize)

        # Add all the Panels
        for ID in self.Panels:
            CurrentPanel = self.Panels[ID]
            MainSizer.Add(CurrentPanel, 1, wx.GROW | wx.ALL, 4)
            MainSizer.Show(CurrentPanel, False)
        self.CurrentPanel = list(self.Panels.values())[0]
        MainSizer.Show(self.CurrentPanel)
        self.SetSizerAndFit(MainSizer)
        self.SetSizeHints(self.GetSize(), self.GetSize())

    def OnButtonPress(self, event):
        ID = event.GetId()
        self.MainSizer.Show(self.CurrentPanel, False)
        self.CurrentPanel = self.Panels[ID]
        self.MainSizer.Show(self.CurrentPanel)
        self.MainSizer.Layout()


class ConverterFrame(wx.Frame):
    def __init__(self, parent, id, title, position, size):
        wx.Frame.__init__(self, parent, id, title, position, size)

        self.AboutDialog = None
        # set icon on Frame:
        if sys.platform == 'win32':
            self.SetIcon(wx.IconFromBitmap(icons.NUCOS16.GetBitmap()))

        # Set up the MenuBar
        MenuBar = wx.MenuBar()
        if sys.platform != "darwin":  # no file menu for Mac -- quit goes in app menu
            file_menu = wx.Menu()
            file_menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
            MenuBar.Append(file_menu, "&File")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "&About",
                         "More information About this program")
        item = help_menu.Append(wx.ID_HELP, "&NUCOS Help",
                                "Bring up NUCOS help in your browser")
        MenuBar.Append(help_menu, "&Help")

#        self.Bind(wx.EVT_MENU, self.OnHelp, item)

        self.SetMenuBar(MenuBar)

        # Is there a better way to do this ??
        wx.EVT_MENU.Bind(self, self.GetId(), wx.ID_EXIT, self.OnQuit)
        wx.EVT_MENU.Bind(self, self.GetId(), wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU.Bind(self, self.GetId(), wx.ID_HELP, self.OnHelp)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # put on the MainPanel:
        MainPanel(self)

        self.HelpFrame = None

        self.Fit()

    def OnHelp(self, event):

        d = BringingUpHelpDialog(self)
        d.Show()
        d.Refresh()
        d.Update()
        wx.CallLater(3000, lambda d: d.Close(), d)

        # open the help html in the system browser
        # # old code for frozen app -- still needed??
        # if sys.platform == 'darwin':
        #     print(os.getcwd())
        #     url = "file://" + os.path.join(os.getcwd(), "Help/help.html")
        # else:  # for windows
        #     exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
        #     # print "exe path is:", exe_path
        #     url = "file://" + os.path.join(exe_path, "Help/help.html")
        help_file = Path(__file__).parent / "help" / "Help.html"

        webbrowser.open_new("file://" + str(help_file))

    def OnQuit(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnAbout(self, event):
        if self.AboutDialog is None:
            self.AboutDialog = AboutDialog(self,
                                           icon1=icons.NUCOS64.GetBitmap(),
                                           icon2=icons.NOAA64.GetBitmap(),
                                           short_name='NUCOS',
                                           long_name='NOAA Unit Converter for Oil Spills',
                                           version=__version__,
                                           description=description,
                                           urls=["http://response.restoration.noaa.gov/NUCOS",
                                                 "mailto://orr.nucos@noaa.gov"],
                                           licence=("NUCOS was developed by an agency of the "
                                                    "US government and is in the public "
                                                    "domain"),
                                           developers=["Christopher Barker, PhD"])

        self.AboutDialog.ShowModal()


description = """
NOAA Unit Converter for Oil Spills (NUCOS) is a small program was designed to aid oil spill
esponders; however, we expect it to be helpful to other users.

It was developed by the National Oceanic and Atmospheric Administration,
Office of Response and Restoration,
Emergency Response Division
"""


class App(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)

        # This catches events when the app is asked to activate by some other
        # process
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)

    def OnInit(self):
        frame = ConverterFrame(None,
                               wx.ID_ANY,
                               "NUCOS",
                               wx.DefaultPosition,
                               wx.DefaultSize)
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

    def BringWindowToFront(self):
        try:  # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass

    def OnActivate(self, event):
        # if this is an activate event, rather than something else, like iconize.
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()


def main():
    app = App(False)
#    import wx.lib.inspection
#    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()



















