#!/usr/bin/env python

"""
Oil Quantity converter for Unitconverter

test code, here. May be merged with main code.
"""
import wx

import unit_conversion as UC
from . import icons
from .utilities import NoCaseCompare, SignificantFigures

# standard Oil types and their APIs
OilTypes = {u"Crude - Light" : 36.0, # from "Conversion Factors Used in Oil Industry"
            u"Crude - Medium": 26.7, # from "Conversion Factors Used in Oil Industry"
            u"Crude - Heavy" : 17.0, # from "Conversion Factors Used in Oil Industry"
            u"Gasoline"    : 57.0, # from "Conversion Factors Used in Oil Industry"
            u"Kerosene"    : 43.2, # from "Conversion Factors Used in Oil Industry"
            u"Gas Oil"     : 33.0, # from "Conversion Factors Used in Oil Industry"
            u"Diesel"      : 31.14, # from "Conversion Factors Used in Oil Industry"
            u"Lube Oil"    : 25.7, # from "Conversion Factors Used in Oil Industry"
            u"Bitumen"     : 3.3, # from "Conversion Factors Used in Oil Industry"
            u"IFO 180"     : 14.7, # from NOAA Adios library
            u"IFO 300"     : 11.9, # from NOAA Adios library
            u"Fuel Oil 6"  : 12.3, # from NOAA Adios library
            u"Fuel Oil 4"  : 25.72, # from Env. Canada, 1996
            #u"Fuel Oil 2"  : 30.0, # from Env. Canada, 1996
            u"Unknown": None}


class OilQuantityPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        kwargs['style'] = wx.SUNKEN_BORDER
        wx.Panel.__init__(self, *args, **kwargs)

        DensityUnits = UC.GetUnitNames("Density")
        DensityUnits.sort(key=str.lower)
        VolUnits = UC.GetUnitNames("Volume")
        VolUnits.sort(key=str.lower)
        MassUnits = UC.GetUnitNames("Mass")
        MassUnits.sort(key=str.lower)

        OilTypeNames = sorted(OilTypes.keys(), key=str.lower)
        self.OilTypeLabel = wx.StaticText(self, label="Oil Type:")
        self.OilType = wx.Choice(self, choices=OilTypeNames)
        self.OilType.SetStringSelection(u"Unknown")

        self.DensityLabel = wx.StaticText(self, label="Oil Density:")
        self.DensityBox = wx.TextCtrl(self, value="")
        self.DensityUnits = wx.Choice(self, choices=DensityUnits)
        self.DensityUnits.SetStringSelection("API degree")

        OilTypeSizer = wx.FlexGridSizer(7, 3, 5, 5)
        OilTypeSizer.AddGrowableCol(1)
        OilTypeSizer.Add(self.OilTypeLabel, 0)
        OilTypeSizer.Add(self.OilType, 0)
        OilTypeSizer.Add((1, 1), 1)
        OilTypeSizer.Add(self.DensityLabel, 0)
        OilTypeSizer.Add(self.DensityBox, 1, wx.EXPAND)
        OilTypeSizer.Add(self.DensityUnits, 0)

        OilTypeSizer.Add((20, 20), 0)
        OilTypeSizer.Add((20, 20), 0)
        OilTypeSizer.Add((20, 20), 0)

        MassLabel = wx.StaticText(self, label="Mass:")
        self.MassBox = wx.TextCtrl(self)
        self.MassUnits = wx.Choice(self, choices=MassUnits)
        self.MassUnits.SetStringSelection("metric ton (tonne)")

        VolLabel = wx.StaticText(self, label="Volume:")
        self.VolBox = wx.TextCtrl(self)
        self.VolUnits = wx.Choice(self, choices=VolUnits)
        self.VolUnits.SetStringSelection("barrel (petroleum)")


        OilTypeSizer.Add(MassLabel, 0)
        OilTypeSizer.Add(self.MassBox, 0, wx.EXPAND)
        OilTypeSizer.Add(self.MassUnits, 0, wx.EXPAND)

        OilTypeSizer.Add(VolLabel, 0)
        OilTypeSizer.Add(self.VolBox, 0, wx.EXPAND)
        OilTypeSizer.Add(self.VolUnits, 0, wx.EXPAND)


        VertBox = wx.BoxSizer(wx.VERTICAL)

        Label = wx.StaticText(self, label="Oil Quantity")
        of = Label.GetFont()
        Font = wx.Font(int(of.GetPointSize() * 2), of.GetFamily(), wx.NORMAL, wx.NORMAL)
        Label.SetFont(Font)


        IconBox = wx.BoxSizer(wx.HORIZONTAL)
        IconBox.Add(wx.StaticBitmap(self, bitmap=icons.NUCOS64.GetBitmap()), 0, wx.ALIGN_LEFT|wx.RIGHT|wx.LEFT,20)
        IconBox.Add((1,1), 1, wx.EXPAND)
        IconBox.Add(Label, 0, wx.ALIGN_CENTER)
        IconBox.Add((1,1), 1, wx.EXPAND)
        IconBox.Add(wx.StaticBitmap(self, bitmap=icons.NOAA64.GetBitmap()), 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT,20)

        VertBox.Add((20, 20), 1)
        VertBox.Add(IconBox, 0, wx.EXPAND)
        VertBox.Add((20, 20), 1)
        VertBox.Add(OilTypeSizer, 0, wx.ALIGN_LEFT|wx.ALL, 10)
        VertBox.Add((20, 20), 1)

        OuterBox = wx.BoxSizer(wx.HORIZONTAL)
        OuterBox.Add((5,5), 1)
        OuterBox.Add(VertBox, 0)
        OuterBox.Add((5,5), 1)

        self.OilType.Bind(wx.EVT_CHOICE, self.OnOilType)
        self.DensityBox.Bind(wx.EVT_TEXT, self.OnDensity)
        self.DensityUnits.Bind(wx.EVT_CHOICE, self.OnDensityUnits)
        self.VolBox.Bind(wx.EVT_TEXT, self.OnVolume)
        self.VolUnits.Bind(wx.EVT_CHOICE, self.Calculate)
        self.MassBox.Bind(wx.EVT_TEXT, self.OnMass)
        self.MassUnits.Bind(wx.EVT_CHOICE, self.Calculate)

        self.SetSizerAndFit(OuterBox)

        self.LastTyped = "Mass" # could be "Mass" or "Volume"

    def OnOilType(self, event):
        self.SetDensity()
        self.Calculate()

    def OnDensity(self, event):
        self.OilType.SetStringSelection(u"Unknown")
        self.Calculate()

    def OnDensityUnits(self, event):
        DensityUnits =  self.DensityUnits.GetStringSelection()
        OilType = self.OilType.GetStringSelection()
        if OilType == u"Unknown":
            # don't change the value in the box
            self.Calculate()
        else:
            # it's a "standard" oil -- re-calculate value
            API = float(OilTypes[OilType])
            Density = UC.convert("Density", "API", DensityUnits, API)
            self.DensityBox.ChangeValue("%.4g"%Density)
            self.Calculate()

    def OnVolume(self, event):
        self.LastTyped = "Volume"
        self.Calculate()

    def OnMass(self, event):
        self.LastTyped = "Mass"
        self.Calculate()

    def SetDensity(self):
        OilType = self.OilType.GetStringSelection()
        API = OilTypes[OilType]
        if API is None:
            pass
            ## this now lets the value stay whatever it was when shifting to "unkown", rather than going blank.
            #self.DensityBox.ChangeValue("")
        else:
            API = u"%.2f"%API
            self.DensityBox.ChangeValue(API)
            self.DensityUnits.SetStringSelection("API degree")
        self.MassBox.SetFocus()
        self.DensityBox.Refresh()
        self.DensityBox.Update()

    def Calculate(self, event=None):
        if self.LastTyped == "Mass":
            try:
                Density = float(self.DensityBox.GetValue())
                massString = self.MassBox.GetValue()
                Mass = float(massString)
                Volume = UC.OilQuantityConverter.ToVolume(Mass,
                                                 self.MassUnits.GetStringSelection(),
                                                 Density,
                                                 self.DensityUnits.GetStringSelection(),
                                                 self.VolUnits.GetStringSelection()
                                                 )
                format_string = u"%%.%ig"%SignificantFigures(massString)
                self.VolBox.ChangeValue(format_string%Volume)

            except ValueError:
                self.VolBox.ChangeValue("")
        elif self.LastTyped == "Volume":
            try:
                Density = float(self.DensityBox.GetValue())
                volString = self.VolBox.GetValue()
                Volume = float(volString)
                Mass = UC.OilQuantityConverter.ToMass(Volume,
                                                      self.VolUnits.GetStringSelection(),
                                                      Density,
                                                      self.DensityUnits.GetStringSelection(),
                                                      self.MassUnits.GetStringSelection())
                format_string = u"%%.%ig"%SignificantFigures(volString)
                self.MassBox.ChangeValue(format_string%Mass)
                #self.MassBox.ChangeValue(u"%.4g"%Mass)
            except ValueError:
                self.MassBox.ChangeValue("")

if __name__ == "__main__":
    a = wx.App(False)
    f = wx.Frame(None)
    p = OilQuantityPanel(f)
    f.Fit()
    f.Show()
    a.MainLoop()


