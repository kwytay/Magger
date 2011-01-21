'''
Created on 18/01/2011

@author: Patrick
'''
import wx, os, sys

sys.path.append("mutagen")

from mutagen.mp3 import MP3 # mp3 tagging support
from k7agger import k7agger # my meat

class K7MainPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        #b = wx.Button(self, -1, "Create and Show an ImageDialog", (50,50))
        #self.Bind(wx.EVT_BUTTON, self.OnButton, b)

class K7AdvancedFindFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'k7agger advanced find')
        #self.CenterOnScreen()
        self.SetSizeHints(250,200,700,300)
        blahLabel = wx.StaticText(self, wx.ID_ANY, 'Advanced Find')
        
        self.cb_dir_only = wx.CheckBox(self, -1, "Show directories only")
        
        
class K7MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'k7agger')
        self.CenterOnScreen()
        self.CreateStatusBar()
        self.SetStatusText("Ready for action")
        
        
        # outer menu container
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu2 = wx.Menu()
        menu1.Append(101, "&Exit")
        menu2.Append(201, "&Find directories")
        menuBar.Append(menu1, "&File")
        menuBar.Append(menu2, "&Tools")
        
        
        self.Bind(wx.EVT_MENU, self.exit, id=101)
        self.Bind(wx.EVT_MENU, self.menu_advanced_find, id=201)
        
        self.SetMenuBar(menuBar)
        self.frame = wx.Frame(None, wx.ID_ANY, title='k7agger')
        self.panel = K7MainPanel(self, wx.ID_ANY) # create a panel bound to the frame
    
        #self.frame.Show()
        self.Show()
        
    def exit(self, event):
        sys.exit(0)
    def menu_advanced_find(self, event):
        adv_frame = K7AdvancedFindFrame()
        adv_frame.Show()
        
class K7App(wx.App):
    "K7App"
    """"call superclass constructor, create my type of panel, a standard frame, 
    and put the panel inside the frame"""
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = K7MainFrame()
        
if __name__=="__main__":
    testdir = "E:\\MUSIC_TEST"
    
    #mainApp = K7App()
    #mainApp.MainLoop()
    k7agger.parse_outer_directory(testdir)
    
    #mp3file = MP3("..\\testfiles\\1000Hz-5sec.mp3")
    #print mp3file.info.length