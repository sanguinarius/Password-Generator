#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Inspired of SV source code

__app__ = "PasswordGenerator"
__author__ = "Sanguinarius"
__credits__ = ["Sanguinarius", "SV"]
__maintainer__ = "Sanguinarius"
__email__ = "sanguinarius.contact@gmail.com"
__version__ = "0.0.7"



import wx
import os
import sys

class myApp(wx.Frame):
    #__init__:begin
    def __init__(self, parent, id, title):

        ## CHARSET LIST
        charset_dico = ['abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!:/;.,?@=+-}])[({%&*$',
                        'abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                        'abcdefghijklmnopqrstuvwxyz0123456789!:/;.,?@=+-}])[({%&*$',
                        'abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        'abcdefghijklmnopqrstuvwxyz0123456789',
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        '0123456789abcdef',
                        '0123456789']
                
        wx.Frame.__init__(self, parent, id, title, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        icon = wx.Icon(name=os.path.join(sys.path[0],"icon_secure.ico"), type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        panel = wx.Panel(self, -1) # voir style=wx.SIMPLE_BORDER ou autre

        #### START content

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        TopBox = wx.BoxSizer(wx.HORIZONTAL)
        InTopBoxRight = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.GridBagSizer(5,5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        Logo = os.path.join(sys.path[0],'icon-main.gif')
        img = wx.Image(Logo, wx.BITMAP_TYPE_ANY)
        sb = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img))

        TopBox.Add(sb, 0)

        # Length init
        ST_PwLength = wx.StaticText(panel, -1, "Key Length")
        self.SC_PwLength = wx.SpinCtrl(panel, -1, "", size=(60,-1))
        self.SC_PwLength.SetRange(2,512)
        self.SC_PwLength.SetValue(12)

        # LIST init
        ST_Charset = wx.StaticText(panel, -1, "Charset")
        self.C_Charset = wx.Choice(panel, -1, (85, 18), choices=charset_dico)
        self.C_Charset.SetSelection(0)
        
        # RESULT init
        self.TC_Result = wx.TextCtrl(panel, -1, "", size=(700, -1), style=wx.TE_READONLY)
        BTN_Generate = wx.Button(panel, -1, "Generate")
        BTN_Generate.Bind(wx.EVT_BUTTON, self.onGenerate)

        BTN_Copy = wx.Button(panel, -1, "Copy")
        BTN_Copy.Bind(wx.EVT_BUTTON, self.onCopy)
        
        #COPYRIGHT
        ST_Copyright = wx.StaticText(panel, -1, "Copyleft (C) Sanguinarius 2011")


        ## Position

        # Length position
        hbox0.Add(ST_PwLength, (0,0), (1,1), wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        hbox0.Add(self.SC_PwLength, (0,1), (1,1), wx.RIGHT | wx.TOP, 5)

        # LIST position
        hbox0.Add(ST_Charset,(1,0), (1,1), wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        hbox0.Add(self.C_Charset, (1,1), (1,1), wx.RIGHT | wx.TOP, 5)
        
        # RESULT position
        hbox1.Add(self.TC_Result, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        hbox1.Add(BTN_Generate, 0, wx.RIGHT | wx.TOP, 10)
        hbox1.Add(BTN_Copy, 0, wx.RIGHT | wx.TOP, 10)
        
        #COPYRIGHT position
        hbox2.Add(ST_Copyright, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)


        InTopBoxRight.Add(hbox0, 0)
        InTopBoxRight.Add(hbox1, 0)
        InTopBoxRight.Add(hbox2, 0)

        TopBox.Add(InTopBoxRight, 0)

        MainSizer.Add(TopBox, 0)

        #### END content

        panel.SetSizer(MainSizer)


        self.Centre()
        self.Show(True)
        MainSizer.Fit(self)

    ## Generate random string
    def onGenerate(self, event):
        import random
        length = self.SC_PwLength.GetValue()
        charset = self.C_Charset.GetStringSelection()
        result = ''.join(random.choice(charset) for i in xrange(length))                                  
        self.TC_Result.SetValue(result)

    ## Paste the random string in clipboard
    def onCopy(self, event):
        text = self.TC_Result.GetValue()
        clipdata = wx.TextDataObject()
        clipdata.SetText(text)
        if not wx.TheClipboard.IsOpened():  # may crash, otherwise
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(clipdata)
            wx.TheClipboard.Close()

    ## Generate warning       
    def GenerateWarning(self, titre, content):
        dialog = wx.MessageDialog(None, content, titre, wx.OK | wx.ICON_EXCLAMATION)
        dialog.ShowModal()
        dialog.Destroy()

app = wx.App()
myApp(None, -1, 'Password Generator')
app.MainLoop()
